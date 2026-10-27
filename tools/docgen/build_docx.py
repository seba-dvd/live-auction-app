"""Build UNITBV-style Word documents (cover, TOC, lists of figures, numbered chapters) from Markdown sources.

    python tools/docgen/build_docx.py docs/raport-tehnic/document.toml [more .toml files]

Each .toml describes one document (or several, as [[documents]] entries sharing the top-level keys).
Supported Markdown (see tools/docgen/README.md): headings (# .. ####, "{-}" = unnumbered), paragraphs with
**bold**, *italic*, `code` and [links](url), bullet / numbered / checkbox lists (nested by 2 spaces), pipe tables
(caption: a "Tabelul: ..." paragraph right before), fenced code (caption: a "Codul: ..." paragraph right after),
images "![caption](path)" with optional "{landscape}", "> " callout boxes, "<!-- pagebreak -->".
Run tools/docgen/update_fields.ps1 afterwards (Word) to fill the TOC / lists and export the PDF.
"""
from __future__ import annotations

import copy
import pathlib
import re
import sys
import tomllib
from dataclasses import dataclass, field

from docx import Document
from docx.image.image import Image as DocxImage
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.shared import Emu, Twips
from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"

# Page geometry of the template (twips). 1 twip = 635 EMU.
PAGE_W, PAGE_H = 11906, 16838
MARGIN_L, MARGIN_R, MARGIN_T, MARGIN_B = 1418, 849, 1134, 1135
TEXT_W_PORTRAIT = PAGE_W - MARGIN_L - MARGIN_R          # 9639 twips = 17.0 cm
TEXT_W_LANDSCAPE = PAGE_H - MARGIN_L - MARGIN_R         # 14571 twips = 25.7 cm
EMU_PER_TWIP = 635
EMU_PER_CM = 360000
MAX_IMG = {False: (16.5 * EMU_PER_CM, 21.0 * EMU_PER_CM), True: (25.0 * EMU_PER_CM, 14.5 * EMU_PER_CM)}

BULLET_NUM_ID = "20"     # bullet list definition of the template ( / o / )
CODE_FONT = "Courier New"


def w(tag: str) -> str:
    return qn(tag)


def el(tag: str, attrs: dict | None = None, *children) -> etree._Element:
    e = etree.Element(w(tag))
    for k, v in (attrs or {}).items():
        e.set(w(k), str(v))
    for c in children:
        e.append(c)
    return e


def xml(fragment: str) -> etree._Element:
    return etree.fromstring(f'<root xmlns:w="{W_NS}">{fragment}</root>')[0]


# ----------------------------------------------------------------------------------------------- Markdown model
@dataclass
class Heading:
    level: int
    text: str
    numbered: bool = True


@dataclass
class Para:
    text: str


@dataclass
class ListBlock:
    items: list = field(default_factory=list)   # (level, ordered, text)


@dataclass
class Table:
    rows: list
    caption: str | None = None


@dataclass
class Code:
    lines: list
    caption: str | None = None


@dataclass
class Image:
    caption: str
    path: str
    landscape: bool = False


@dataclass
class Quote:
    lines: list


@dataclass
class PageBreak:
    pass


@dataclass
class Landscape:
    start: bool   # <!-- landscape-start --> ... <!-- landscape-end -->: everything in between on landscape pages


RE_FENCE = re.compile(r"^\s*```")
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*(\{-\}|\{\.unnumbered\})?\s*$")
RE_IMAGE = re.compile(r"^!\[(.*?)\]\((.+?)\)\s*(\{landscape\})?\s*$")
RE_LIST = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
RE_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
RE_TABLE_SEP = re.compile(r"^\s*\|?(\s*:?-{3,}:?\s*\|)+\s*(:?-{3,}:?\s*)?\|?\s*$")
RE_QUOTE = re.compile(r"^\s*>\s?(.*)$")
RE_HR = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
RE_TABLE_CAPTION = re.compile(r"^Tabelul:\s*(.+)$")
RE_CODE_CAPTION = re.compile(r"^Codul:\s*(.+)$")


def split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    cells, cur, i = [], "", 0
    in_code = False
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            cur += "|"
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
        i += 1
    cells.append(cur.strip())
    return cells


def parse_markdown(text: str) -> list:
    lines = text.replace("\r\n", "\n").split("\n")
    blocks: list = []
    i, n = 0, len(lines)

    def starts_block(s: str) -> bool:
        return bool(RE_FENCE.match(s) or RE_HEADING.match(s) or RE_IMAGE.match(s) or RE_LIST.match(s)
                    or RE_TABLE_ROW.match(s) or RE_QUOTE.match(s) or RE_HR.match(s) or s.strip().startswith("<!--"))

    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("<!--"):
            if "pagebreak" in stripped:
                blocks.append(PageBreak())
            elif "landscape-start" in stripped:
                blocks.append(Landscape(True))
            elif "landscape-end" in stripped:
                blocks.append(Landscape(False))
            while i < n and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        if RE_FENCE.match(line):
            code, i = [], i + 1
            while i < n and not RE_FENCE.match(lines[i]):
                code.append(lines[i].rstrip("\n"))
                i += 1
            i += 1
            block = Code(code)
            j = i
            while j < n and not lines[j].strip():
                j += 1
            if j < n and RE_CODE_CAPTION.match(lines[j].strip()):
                block.caption = RE_CODE_CAPTION.match(lines[j].strip()).group(1)
                i = j + 1
            blocks.append(block)
            continue
        m = RE_HEADING.match(line)
        if m:
            blocks.append(Heading(len(m.group(1)), m.group(2), numbered=m.group(3) is None))
            i += 1
            continue
        m = RE_IMAGE.match(stripped)
        if m:
            blocks.append(Image(m.group(1), m.group(2), landscape=m.group(3) is not None))
            i += 1
            continue
        if RE_TABLE_ROW.match(line) and i + 1 < n and RE_TABLE_SEP.match(lines[i + 1]):
            rows = [split_row(line)]
            i += 2
            while i < n and RE_TABLE_ROW.match(lines[i]):
                rows.append(split_row(lines[i]))
                i += 1
            caption = None
            if blocks and isinstance(blocks[-1], Para) and RE_TABLE_CAPTION.match(blocks[-1].text):
                caption = RE_TABLE_CAPTION.match(blocks.pop().text).group(1)
            blocks.append(Table(rows, caption))
            continue
        if RE_LIST.match(line):
            block = ListBlock()
            while i < n:
                cur = lines[i]
                lm = RE_LIST.match(cur)
                if lm:
                    level = min(len(lm.group(1).replace("\t", "    ")) // 2, 2)
                    block.items.append([level, lm.group(2)[0].isdigit(), lm.group(3).strip()])
                    i += 1
                elif cur.strip() and cur.startswith("  ") and block.items and not starts_block(cur.strip()):
                    block.items[-1][2] += " " + cur.strip()
                    i += 1
                elif not cur.strip() and i + 1 < n and RE_LIST.match(lines[i + 1]) and lines[i + 1].startswith(" "):
                    i += 1   # blank line inside a nested list
                else:
                    break
            blocks.append(block)
            continue
        if RE_QUOTE.match(line):
            quote = []
            while i < n and RE_QUOTE.match(lines[i]):
                quote.append(RE_QUOTE.match(lines[i]).group(1))
                i += 1
            blocks.append(Quote(quote))
            continue
        if RE_HR.match(line):
            i += 1
            continue
        para = [line.rstrip()]
        i += 1
        while i < n and lines[i].strip() and not starts_block(lines[i]):
            para.append(lines[i].rstrip())
            i += 1
        text = ""
        for k, p in enumerate(para):
            hard_break = p.endswith("  ") or p.endswith("\\")
            text += p.rstrip(" \\") + ("\n" if hard_break and k < len(para) - 1 else " ")
        blocks.append(Para(text.strip()))
    return blocks


# ----------------------------------------------------------------------------------------------- inline rendering
RE_INLINE = re.compile(
    r"(?P<code>`[^`]+`)"
    r"|(?P<bold>\*\*(?=\S)(?:[^*]|\*(?!\*))+?\*\*)"
    r"|(?P<link>\[(?P<ltext>[^\]]+)\]\((?P<lurl>[^)\s]+)\))"
    r"|(?P<italic>(?<![\w*])\*(?=\S)[^*\n]+?(?<=\S)\*(?![\w*]))"
    r"|(?P<uitalic>(?<![\w])_(?=\S)[^_\n]+?(?<=\S)_(?![\w]))"
)


class Builder:
    def __init__(self, cfg: dict, cfg_path: pathlib.Path):
        self.cfg = cfg
        self.base = cfg_path.parent
        self.repo_root = (self.base / cfg.get("repo_root", "../..")).resolve()
        self.repo_url = cfg.get("repo_url", "")
        self.doc = Document(str(self.base / cfg["template"]))
        self.body = self.doc.element.body
        self.final_sectpr = self.body.find(w("w:sectPr"))
        self.counters = {"Figura": 0, "Tabelul": 0, "Codul": 0}
        self.current_md: pathlib.Path | None = None
        self.numbering = self.doc.part.numbering_part.element
        self.ordered_abstract_id = self._add_ordered_abstract()
        self.next_num_id = max(int(n.get(w("w:numId"))) for n in self.numbering.findall(w("w:num"))) + 1
        self.in_landscape = False

    # ---------- low level helpers
    def append(self, element):
        self.body.insert(len(self.body) - 1, element)   # before the final sectPr
        return element

    def run(self, text: str, bold=False, italic=False, code=False, size=None, color=None, style=None):
        r = el("w:r")
        rpr = el("w:rPr")
        if style:
            rpr.append(el("w:rStyle", {"w:val": style}))
        if code:
            rpr.append(el("w:rFonts", {"w:ascii": CODE_FONT, "w:hAnsi": CODE_FONT, "w:cs": CODE_FONT}))
        if bold:
            rpr.append(el("w:b"))
            rpr.append(el("w:bCs"))
        if italic:
            rpr.append(el("w:i"))
            rpr.append(el("w:iCs"))
        if color:
            rpr.append(el("w:color", {"w:val": color}))
        sz = size or (20 if code else None)
        if sz:
            rpr.append(el("w:sz", {"w:val": sz}))
            rpr.append(el("w:szCs", {"w:val": sz}))
        if len(rpr):
            r.append(rpr)
        parts = text.split("\n")
        for k, part in enumerate(parts):
            if k:
                r.append(el("w:br"))
            for j, chunk in enumerate(part.split("\t")):
                if j:
                    r.append(el("w:tab"))
                if chunk:
                    t = el("w:t")
                    t.text = chunk
                    t.set(XML_SPACE, "preserve")
                    r.append(t)
        return r

    def field(self, instr: str, cached: str, size=None, dirty=False) -> list:
        begin = el("w:fldChar", {"w:fldCharType": "begin"})
        if dirty:
            begin.set(w("w:dirty"), "true")
        r1, r2, r3, r5 = el("w:r"), el("w:r"), el("w:r"), el("w:r")
        r1.append(begin)
        it = el("w:instrText")
        it.text = f" {instr} "
        it.set(XML_SPACE, "preserve")
        r2.append(it)
        r3.append(el("w:fldChar", {"w:fldCharType": "separate"}))
        r4 = self.run(cached, size=size)
        r5.append(el("w:fldChar", {"w:fldCharType": "end"}))
        return [r1, r2, r3, r4, r5]

    def hyperlink(self, text: str, url: str, **fmt):
        rid = self.doc.part.relate_to(url, RT.HYPERLINK, is_external=True)
        h = el("w:hyperlink")
        h.set(qn("r:id"), rid)
        h.set(w("w:history"), "1")
        h.append(self.run(text, style="Hyperlink", **fmt))
        return h

    def resolve_link(self, url: str) -> str | None:
        if re.match(r"^(https?:|mailto:)", url):
            return url
        if url.startswith("#") or not self.repo_url or self.current_md is None:
            return None
        path, _, anchor = url.partition("#")
        target = (self.current_md.parent / path).resolve()
        try:
            rel = target.relative_to(self.repo_root).as_posix()
        except ValueError:
            return None
        return self.repo_url + rel + (f"#{anchor}" if anchor else "")

    def inline(self, text: str, bold=False, italic=False, size=None) -> list:
        out, pos = [], 0
        text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|<>])", r"\1", text)
        for m in RE_INLINE.finditer(text):
            if m.start() > pos:
                out.append(self.run(text[pos:m.start()], bold=bold, italic=italic, size=size))
            if m.group("code"):
                out.append(self.run(m.group("code")[1:-1], bold=bold, italic=italic, code=True,
                                    size=(size - 2 if size else 22)))
            elif m.group("bold"):
                out += self.inline(m.group("bold")[2:-2], bold=True, italic=italic, size=size)
            elif m.group("link"):
                target = self.resolve_link(m.group("lurl"))
                label = m.group("ltext").strip("`")
                if target:
                    out.append(self.hyperlink(label, target, bold=bold, italic=italic, size=size))
                else:
                    out += self.inline(m.group("ltext"), bold=bold, italic=italic, size=size)
            elif m.group("italic") or m.group("uitalic"):
                inner = (m.group("italic") or m.group("uitalic"))[1:-1]
                out += self.inline(inner, bold=bold, italic=True, size=size)
            pos = m.end()
        if pos < len(text):
            out.append(self.run(text[pos:], bold=bold, italic=italic, size=size))
        return out

    def paragraph(self, ppr_xml: str, runs: list):
        p = el("w:p")
        p.append(xml(f"<w:pPr>{ppr_xml}</w:pPr>"))
        for r in runs:
            p.append(r)
        return self.append(p)

    # ---------- numbering
    def _add_ordered_abstract(self) -> str:
        ids = [int(a.get(w("w:abstractNumId"))) for a in self.numbering.findall(w("w:abstractNum"))]
        new_id = str(max(ids) + 1)
        levels = ""
        for lvl, (fmt, txt) in enumerate((("decimal", "%1."), ("lowerLetter", "%2)"), ("lowerRoman", "%3."))):
            levels += (f'<w:lvl w:ilvl="{lvl}"><w:start w:val="1"/><w:numFmt w:val="{fmt}"/><w:lvlText w:val="{txt}"/>'
                       f'<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="{720 * (lvl + 1)}" w:hanging="360"/></w:pPr></w:lvl>')
        abstract = xml(f'<w:abstractNum w:abstractNumId="{new_id}"><w:multiLevelType w:val="hybridMultilevel"/>{levels}</w:abstractNum>')
        last = self.numbering.findall(w("w:abstractNum"))[-1]
        last.addnext(abstract)
        return new_id

    def new_ordered_num(self) -> str:
        num_id = str(self.next_num_id)
        self.next_num_id += 1
        self.numbering.append(xml(
            f'<w:num w:numId="{num_id}"><w:abstractNumId w:val="{self.ordered_abstract_id}"/>'
            f'<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'))
        return num_id

    # ---------- blocks
    PPR_BODY = '<w:spacing w:line="288" w:lineRule="auto"/><w:ind w:firstLine="709"/><w:jc w:val="both"/>'
    PPR_H1 = ('<w:pStyle w:val="Heading1"/><w:pageBreakBefore/><w:pBdr><w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
              '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/><w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
              '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/><w:between w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
              '</w:pBdr><w:ind w:right="169" w:firstLine="709"/><w:jc w:val="right"/>')
    PPR_H1_UNNUMBERED = ('<w:pStyle w:val="Heading1"/><w:pageBreakBefore/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'
                         '<w:pBdr><w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/><w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                         '<w:bottom w:val="double" w:sz="4" w:space="1" w:color="auto"/><w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                         '<w:between w:val="none" w:sz="0" w:space="0" w:color="auto"/></w:pBdr><w:ind w:right="169" w:firstLine="709"/>'
                         '<w:jc w:val="right"/>')
    PPR_H2 = '<w:pStyle w:val="Heading2"/><w:spacing w:line="288" w:lineRule="auto"/><w:ind w:left="0" w:firstLine="0"/>'
    PPR_H3 = '<w:pStyle w:val="Heading3"/><w:spacing w:line="288" w:lineRule="auto"/><w:ind w:left="0" w:firstLine="0"/>'
    PPR_CAPTION = '<w:pStyle w:val="Caption"/><w:keepLines/><w:spacing w:before="60" w:after="200"/><w:jc w:val="center"/>'
    PPR_TABLE_CAPTION = '<w:pStyle w:val="Caption"/><w:keepNext/><w:keepLines/><w:spacing w:before="120" w:after="60"/><w:jc w:val="right"/>'
    PPR_FIGURE = '<w:keepNext/><w:spacing w:before="120" w:after="0"/><w:jc w:val="center"/>'

    def heading(self, h: Heading):
        text = h.text
        if self.cfg.get("strip_heading_numbers", True):
            text = re.sub(r"^\d+(\.\d+)*[.)]?\s+", "", text)
        level = h.level + self.cfg.get("heading_offset", 0)
        no_number = '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'
        if level <= 1:
            ppr = self.PPR_H1 if h.numbered else self.PPR_H1_UNNUMBERED
            if not self.cfg.get("h1_page_break", True):
                ppr = ppr.replace("<w:pageBreakBefore/>", "")
        elif level == 2:
            ppr = self.PPR_H2 if h.numbered else self.PPR_H2.replace("<w:spacing", no_number + "<w:spacing", 1)
        elif level == 3:
            ppr = self.PPR_H3 if h.numbered else self.PPR_H3.replace("<w:spacing", no_number + "<w:spacing", 1)
        else:   # deeper levels: bold run-in paragraph
            self.paragraph('<w:keepNext/><w:spacing w:before="160" w:line="288" w:lineRule="auto"/>', self.inline(text, bold=True))
            return
        self.paragraph(ppr, self.inline(text))

    def body_paragraph(self, text: str):
        self.paragraph(self.PPR_BODY, self.inline(text))

    def list_block(self, block: ListBlock):
        ordered_ids: dict[int, str] = {}
        prev_level = -1
        for level, ordered, text in block.items:
            if level <= prev_level:
                for deeper in [k for k in ordered_ids if k > level]:
                    del ordered_ids[deeper]
            if ordered:
                if level not in ordered_ids:
                    ordered_ids[level] = self.new_ordered_num()
                num_id = ordered_ids[level]
            else:
                num_id = BULLET_NUM_ID
            check = re.match(r"^\[( |x|X)\]\s+(.*)$", text)
            runs = []
            if check:
                runs.append(self.run("☑ " if check.group(1).lower() == "x" else "☐ "))
                text = check.group(2)
            runs += self.inline(text)
            ilvl = level if not ordered else 0 if level == 0 else level
            self.paragraph(f'<w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="{ilvl}"/><w:numId w:val="{num_id}"/></w:numPr>'
                           f'<w:spacing w:after="60" w:line="276" w:lineRule="auto"/><w:ind w:left="{720 * (level + 1)}" w:hanging="360"/>',
                           runs)
            prev_level = level

    def caption(self, kind: str, text: str, ppr: str):
        self.counters[kind] += 1
        runs = [self.run(f"{kind} ")]
        runs += self.field(f"SEQ {kind} \\* ARABIC", str(self.counters[kind]))
        runs.append(self.run(". "))
        runs += self.inline(text)
        for r in runs:   # captions in black, like the template's own captions (style colour is blue)
            if r.tag == w("w:r"):
                rpr = r.find(w("w:rPr"))
                if rpr is None:
                    rpr = el("w:rPr")
                    r.insert(0, rpr)
                if rpr.find(w("w:color")) is None:
                    color = el("w:color", {"w:val": "auto"})
                    sz = rpr.find(w("w:sz"))
                    if sz is not None:
                        sz.addprevious(color)
                    else:
                        rpr.append(color)
        self.paragraph(ppr, runs)

    def section_break(self, landscape: bool):
        sect = copy.deepcopy(self.final_sectpr)
        pg = sect.find(w("w:pgSz"))
        if landscape:
            pg.set(w("w:w"), str(PAGE_H))
            pg.set(w("w:h"), str(PAGE_W))
            pg.set(w("w:orient"), "landscape")
        p = el("w:p")
        ppr = el("w:pPr")
        ppr.append(sect)
        p.append(ppr)
        self.append(p)

    def image(self, block: Image):
        path = (self.current_md.parent / block.path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"{self.current_md}: image not found: {block.path}")
        own_section = block.landscape and not self.in_landscape
        if own_section:
            self.section_break(landscape=False)
        info = DocxImage.from_file(str(path))
        natural_w = info.px_width / (info.horz_dpi or 96) * 914400
        natural_h = info.px_height / (info.vert_dpi or 96) * 914400
        max_w, max_h = MAX_IMG[block.landscape or self.in_landscape]
        if self.in_landscape:
            max_h = min(max_h, 11.5 * EMU_PER_CM)   # leave room for the subsection heading and text
        scale = min(1.0, max_w / natural_w, max_h / natural_h)
        para = self.doc.add_paragraph()   # inserted before the final sectPr
        para._p.insert(0, xml(f"<w:pPr>{self.PPR_FIGURE}</w:pPr>"))
        para.add_run().add_picture(str(path), width=Emu(int(natural_w * scale)), height=Emu(int(natural_h * scale)))
        self.caption("Figura", block.caption, self.PPR_CAPTION)
        if own_section:
            self.section_break(landscape=True)

    @staticmethod
    def column_widths(rows: list, total: int) -> list[int]:
        """Every column gets at least its longest word (no broken words), the rest is shared by content length."""
        plain = [[re.sub(r"[`*_\[\]]|\(http[^)]*\)", "", c) for c in r] for r in rows]
        ncols = len(plain[0])
        min_w, weights = [], []
        for c in range(ncols):
            words = [wd for r in plain for wd in r[c].split()] or [""]
            longest_word = max(len(wd) for wd in words)
            # ~105 twips per character at 10 pt (header row is bold) + cell padding
            min_w.append(min(longest_word, 28) * 108 + 230)
            longest = max(len(r[c]) for r in plain)
            weights.append(min(max(longest, 4), 60) ** 0.9)
        if sum(min_w) >= total:
            return [int(m * total / sum(min_w)) for m in min_w]
        rest = total - sum(min_w)
        return [int(m + rest * wgt / sum(weights)) for m, wgt in zip(min_w, weights)]

    def table(self, block: Table):
        if block.caption:
            self.caption("Tabelul", block.caption, self.PPR_TABLE_CAPTION)
        rows = [r for r in block.rows]
        ncols = max(len(r) for r in rows)
        rows = [r + [""] * (ncols - len(r)) for r in rows]
        widths = self.column_widths(rows, TEXT_W_PORTRAIT)
        table = self.doc.add_table(rows=len(rows), cols=ncols)
        table.style = self.doc.styles["Table Grid"]
        table.alignment = WD_TABLE_ALIGNMENT.CENTER    # python-docx keeps the schema order of tblPr
        table.autofit = False                          # fixed layout
        tbl = table._tbl
        for gc, wd in zip(tbl.tblGrid.findall(w("w:gridCol")), widths):
            gc.set(w("w:w"), str(wd))
        for ri, row in enumerate(rows):
            tr = table.rows[ri]._tr
            if ri == 0:
                trpr = tr.get_or_add_trPr()
                trpr.append(el("w:cantSplit"))     # CT_TrPr order: cantSplit before tblHeader
                trpr.append(el("w:tblHeader"))
            for ci, cell_text in enumerate(row):
                cell = table.rows[ri].cells[ci]
                cell.width = Twips(widths[ci])
                tc = cell._tc
                tcpr = tc.get_or_add_tcPr()
                if ri == 0:
                    tcw = tcpr.find(w("w:tcW"))
                    shd = el("w:shd", {"w:val": "clear", "w:color": "auto", "w:fill": "E3E8F0"})
                    if tcw is not None:
                        tcw.addnext(shd)
                    else:
                        tcpr.insert(0, shd)
                p = tc.find(w("w:p"))
                p.append(xml('<w:pPr><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/>'
                             '<w:ind w:firstLine="0"/><w:jc w:val="left"/></w:pPr>'))
                for r in self.inline(cell_text, bold=(ri == 0), size=20):
                    p.append(r)
        # spacing after the table
        self.paragraph('<w:spacing w:after="60"/>', [])

    def code(self, block: Code):
        keep = len(block.lines) <= 25
        for k, line in enumerate(block.lines or [""]):
            last = k == len(block.lines) - 1
            ppr = ('<w:pStyle w:val="PlainText"/>' + ('<w:keepNext/>' if keep and not last else '')
                   + '<w:shd w:val="clear" w:color="auto" w:fill="F2F4F7"/>'
                   + f'<w:spacing w:before="{60 if k == 0 else 0}" w:after="{60 if last else 0}" w:line="240" w:lineRule="auto"/>'
                   + '<w:ind w:left="284" w:right="284" w:firstLine="0"/>')
            self.paragraph(ppr, [self.run(line.replace("\t", "    ") or " ", code=True, size=17)])
        if block.caption:
            self.caption("Codul", block.caption, self.PPR_CAPTION)

    def quote(self, block: Quote):
        box = ('<w:keepNext/><w:keepLines/><w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="1F3A68"/></w:pBdr>'
               '<w:shd w:val="clear" w:color="auto" w:fill="EEF2F8"/>'
               '<w:spacing w:before="{before}" w:after="0" w:line="264" w:lineRule="auto"/>'
               '<w:ind w:left="284" w:right="284"/><w:jc w:val="left"/>')
        ppr = box.format(before=0)
        paras, cur = [], []
        for line in block.lines:
            if not line.strip():
                if cur:
                    paras.append(" ".join(cur))
                    cur = []
            elif RE_LIST.match(line):
                if cur:
                    paras.append(" ".join(cur))
                paras.append("• " + RE_LIST.match(line).group(3))
                cur = []
            else:
                cur.append(line.strip())
        if cur:
            paras.append(" ".join(cur))
        self.paragraph(box.format(before=120), [])           # top padding of the box
        for p in paras:
            self.paragraph(ppr, self.inline(p, size=22))
        self.paragraph(ppr.replace("<w:keepNext/>", ""), [])   # bottom padding
        self.paragraph('<w:spacing w:after="60"/>', [])

    def page_break(self):
        self.paragraph("", [xml('<w:r><w:br w:type="page"/></w:r>')])

    # ---------- documents parts
    def render_markdown(self, md_path: pathlib.Path, skip_first_h1=False):
        self.current_md = md_path.resolve()
        blocks = parse_markdown(md_path.read_text(encoding="utf-8"))
        skipped = False
        for b in blocks:
            if isinstance(b, Heading):
                if skip_first_h1 and not skipped and b.level == 1:
                    skipped = True
                    continue
                self.heading(b)
            elif isinstance(b, Para):
                self.body_paragraph(b.text)
            elif isinstance(b, ListBlock):
                self.list_block(b)
            elif isinstance(b, Table):
                self.table(b)
            elif isinstance(b, Code):
                self.code(b)
            elif isinstance(b, Image):
                self.image(b)
            elif isinstance(b, Quote):
                self.quote(b)
            elif isinstance(b, PageBreak):
                self.page_break()
            elif isinstance(b, Landscape):
                if b.start and not self.in_landscape:
                    self.section_break(landscape=False)    # ends the portrait section before the region
                    self.in_landscape = True
                elif not b.start and self.in_landscape:
                    self.section_break(landscape=True)     # ends the landscape region
                    self.in_landscape = False

    def count_captions(self, files: list[pathlib.Path]) -> dict:
        counts = {"Figura": 0, "Tabelul": 0, "Codul": 0}
        for f in files:
            for b in parse_markdown(f.read_text(encoding="utf-8")):
                if isinstance(b, Image):
                    counts["Figura"] += 1
                elif isinstance(b, Table) and b.caption:
                    counts["Tabelul"] += 1
                elif isinstance(b, Code) and b.caption:
                    counts["Codul"] += 1
        return counts

    def toc(self):
        title = el("w:p")
        title.append(xml('<w:pPr><w:pStyle w:val="Header"/><w:pBdr><w:bottom w:val="double" w:sz="4" w:space="1" w:color="auto"/></w:pBdr>'
                         '<w:spacing w:after="240"/><w:ind w:right="310" w:firstLine="709"/><w:jc w:val="right"/></w:pPr>'))
        title.append(self.run("Cuprins", bold=True, size=52))
        self.append(title)
        self.paragraph('<w:pStyle w:val="TOC1"/>', self.field('TOC \\o "1-3" \\h \\z \\u',
                                                              "Cuprinsul se generează automat (în Word: clic dreapta → Update Field).",
                                                              size=22, dirty=True))

    def lists_of_figures(self, counts: dict):
        if not any(counts.values()):
            return
        self.heading(Heading(1, "Lista de figuri, tabele și coduri sursă", numbered=False))
        for kind, label in (("Figura", "FIGURI"), ("Tabelul", "TABELE"), ("Codul", "CODURI SURSĂ")):
            if counts[kind]:
                self.paragraph('<w:keepNext/><w:spacing w:before="240" w:after="120"/>', [self.run(label, bold=True, size=22)])
                self.paragraph('<w:pStyle w:val="TableofFigures"/>',
                               self.field(f'TOC \\h \\z \\c "{kind}"', "Lista se generează automat (Update Field).", size=22, dirty=True))

    def acronyms(self, md_path: pathlib.Path):
        self.current_md = md_path.resolve()
        self.heading(Heading(1, "Lista de acronime", numbered=False))
        for b in parse_markdown(md_path.read_text(encoding="utf-8")):
            if isinstance(b, ListBlock):
                for _, _, text in b.items:
                    self.paragraph('<w:spacing w:after="40"/>', self.inline(text, size=22))
            elif isinstance(b, Para):
                self.paragraph('<w:spacing w:after="120"/>', self.inline(b.text, size=22, italic=True))

    def bibliography(self, md_path: pathlib.Path):
        self.current_md = md_path.resolve()
        for b in parse_markdown(md_path.read_text(encoding="utf-8")):
            if isinstance(b, Heading):
                self.heading(b)
            elif isinstance(b, (Para, ListBlock)):
                entries = [b.text] if isinstance(b, Para) else [t for _, _, t in b.items]
                for entry in entries:
                    m = re.match(r"^\[(\d+)\]\s*(.*)$", entry)
                    runs = [self.run(f"[{m.group(1)}]\t", size=22)] + self.inline(m.group(2), size=22) if m else self.inline(entry, size=22)
                    self.paragraph('<w:spacing w:after="120" w:line="288" w:lineRule="auto"/><w:ind w:left="709" w:hanging="709"/>'
                                   '<w:jc w:val="both"/>', runs)

    # ---------- cover and headers
    def fill_cover(self, team_lines: list[str]):
        replacements = {
            "{{DOC_TYPE}}": self.cfg.get("doc_type", ""),
            "{{TITLE}}": self.cfg.get("title", ""),
            "{{SUBTITLE}}": self.cfg.get("subtitle", ""),
            "{{COURSE}}": self.cfg.get("course", ""),
            "{{COORDINATOR_LABEL}}": self.cfg.get("coordinator_label", "Coordonator:"),
            "{{COORDINATOR}}": self.cfg.get("coordinator", ""),
            "{{TEAM_LABEL}}": self.cfg.get("team_label", "Echipa:"),
            "{{CITY_YEAR}}": self.cfg.get("city_year", "BRAȘOV, 2026"),
        }
        for t in list(self.body.iter(w("w:t"))):
            if t.text in replacements:
                t.text = replacements[t.text]
            elif t.text == "{{TEAM}}":
                p = t.getparent().getparent()
                for line in reversed(team_lines):
                    clone = copy.deepcopy(p)
                    next(clone.iter(w("w:t"))).text = line
                    p.addnext(clone)
                p.getparent().remove(p)
            elif t.text == "{{COVER_FILL}}":
                p = t.getparent().getparent()
                fill = int(self.cfg.get("cover_fill_lines", max(1, 11 - len(team_lines))))
                for _ in range(fill):
                    p.addnext(el("w:p"))
                p.getparent().remove(p)
        for rel in self.doc.part.rels.values():
            if rel.reltype == RT.HEADER:
                for t in rel.target_part.element.iter(w("w:t")):
                    t.text = t.text.replace("{{HEADER_ODD}}", self.cfg.get("header_odd", "")).replace(
                        "{{HEADER_EVEN}}", self.cfg.get("header_even", ""))
        props = self.doc.core_properties
        props.title = f'{self.cfg.get("doc_type", "")} — {self.cfg.get("title", "")}'.strip(" —")
        props.subject = self.cfg.get("course", "")
        props.author = "Echipa Live Auction App"
        props.comments = "Generat cu tools/docgen/build_docx.py din sursele Markdown; nu edita direct, editează sursele."

    def build(self):
        team_lines = load_team_lines(self.base / self.cfg.get("team_file", "../../tools/docgen/team.toml"),
                                     self.cfg.get("team_ids"))
        self.fill_cover(team_lines)
        chapters = [self.base / c for c in self.cfg.get("chapters", [])]
        front = self.cfg.get("front_matter", ["toc"])
        if "toc" in front:
            self.toc()
        if "lists" in front:
            self.lists_of_figures(self.count_captions(chapters))
        if "acronyms" in front and self.cfg.get("acronyms"):
            self.acronyms(self.base / self.cfg["acronyms"])
        for ch in chapters:
            self.render_markdown(ch, skip_first_h1=self.cfg.get("skip_first_h1", False))
        for extra in self.cfg.get("back_matter", []):
            path = self.base / extra
            if "bibliograf" in path.name:
                self.bibliography(path)
            else:
                self.render_markdown(path)
        out = self.base / self.cfg["output"]
        out.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(out))
        return out


def load_team_lines(path: pathlib.Path, ids: list | None) -> list[str]:
    team = tomllib.loads(path.read_text(encoding="utf-8"))["member"]
    lines = []
    for m in team:
        if ids and m["id"] not in ids:
            continue
        who = f'{m["name"]} ({m["id"]})' if m.get("name") else m["id"]
        lines.append(f'{who} — {m["role"]}')
    return lines


def load_configs(path: pathlib.Path) -> list[dict]:
    cfg = tomllib.loads(path.read_text(encoding="utf-8"))
    docs = cfg.pop("documents", None)
    if not docs:
        return [cfg]
    return [{**cfg, **d} for d in docs]


def main(argv: list[str]) -> None:
    if not argv:
        sys.exit(__doc__)
    for arg in argv:
        path = pathlib.Path(arg)
        for cfg in load_configs(path):
            out = Builder(cfg, path).build()
            print(f"built {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
