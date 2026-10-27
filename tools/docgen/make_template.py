"""Derive docs/templates/unitbv-template.docx from the UNITBV/IESC diploma template (Documentatie_Licenta.docx).

Kept from the original: styles, heading numbering, theme, settings (different odd/even headers), headers and footers
(page numbers), page size and margins, the faculty logo on the cover.
Dropped: the diploma-only parts (second cover page, FISA/VIZE tables, the guidance text, annexes).
The cover is rebuilt with placeholders ({{DOC_TYPE}}, {{TITLE}}, ...) that build_docx.py fills in.

Usage (run once, the result is committed):
    python tools/docgen/make_template.py "<path>/Documentatie_Licenta.docx" docs/templates/unitbv-template.docx
"""
import copy
import sys

from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def text_of(el) -> str:
    return "".join(t.text or "" for t in el.iter(qn("w:t")))


def make_paragraph(proto, text: str, size_half_points: int | None = None, bold: bool | None = None,
                   italic: bool | None = None, align: str | None = None):
    """Copy the paragraph/run formatting of `proto` and put `text` in a single run."""
    p = copy.deepcopy(proto)
    ppr = p.find(qn("w:pPr"))
    run_props = copy.deepcopy(p.find(".//" + qn("w:r") + "/" + qn("w:rPr")))
    for child in list(p):
        if child.tag != qn("w:pPr"):
            p.remove(child)
    if run_props is None:
        run_props = etree.SubElement(etree.Element(qn("w:r")), qn("w:rPr"))
    for rpr in [run_props] + ([ppr.find(qn("w:rPr"))] if ppr is not None and ppr.find(qn("w:rPr")) is not None else []):
        for tag in ("w:lang",):
            for el in rpr.findall(qn(tag)):
                rpr.remove(el)
        if size_half_points is not None:
            for tag in ("w:sz", "w:szCs"):
                el = rpr.find(qn(tag))
                if el is None:
                    el = etree.SubElement(rpr, qn(tag))
                el.set(qn("w:val"), str(size_half_points))
        for flag, tags in ((bold, ("w:b", "w:bCs")), (italic, ("w:i", "w:iCs"))):
            if flag is None:
                continue
            for tag in tags:
                for el in rpr.findall(qn(tag)):
                    rpr.remove(el)
                if flag:
                    rpr.insert(1, etree.Element(qn(tag)))
    if align and ppr is not None:
        jc = ppr.find(qn("w:jc"))
        if jc is None:
            jc = etree.SubElement(ppr, qn("w:jc"))
        jc.set(qn("w:val"), align)
    if text:
        r = etree.SubElement(p, qn("w:r"))
        r.append(run_props)
        t = etree.SubElement(r, qn("w:t"))
        t.text = text
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return p


def set_style_fonts(styles, style_id: str, font: str, size_half_points: int | None = None, lang: str | None = None):
    st = styles.find(f"{{{W}}}style[@{{{W}}}styleId='{style_id}']")
    if st is None:
        return
    rpr = st.find(qn("w:rPr"))
    if rpr is None:
        rpr = etree.SubElement(st, qn("w:rPr"))
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = etree.Element(qn("w:rFonts"))
        rpr.insert(0, fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        fonts.set(qn(attr), font)
    if size_half_points:
        for tag in ("w:sz", "w:szCs"):
            el = rpr.find(qn(tag))
            if el is None:
                el = etree.SubElement(rpr, qn(tag))
            el.set(qn("w:val"), str(size_half_points))
    if lang:
        el = rpr.find(qn("w:lang"))
        if el is None:
            el = etree.SubElement(rpr, qn("w:lang"))
        el.set(qn("w:val"), lang)


def main(src: str, dst: str) -> None:
    doc = Document(src)
    body = doc.element.body
    els = list(body)

    # --- locate the parts of the original ------------------------------------------------------
    logo = els[0]
    doc_type_proto = next(e for e in els if text_of(e).strip() == "PROIECT DE DIPLOMĂ")
    left_label_proto = next(e for e in els if text_of(e).strip() == "Conducător științific:")
    right_label_proto = next(e for e in els if text_of(e).strip() == "Absolvent:")
    city_proto = next(e for e in els if text_of(e).strip().startswith("BRAȘOV, 202"))
    blank_proto = els[1]
    section_paras = [e for e in els if e.tag == qn("w:p") and e.find(qn("w:pPr") + "/" + qn("w:sectPr")) is not None]
    cover_section_para, main_section_para = section_paras[0], section_paras[1]
    body_sectpr = body.find(qn("w:sectPr"))

    # --- rebuild the cover with placeholders --------------------------------------------------
    cover = [logo] + [copy.deepcopy(blank_proto) for _ in range(9)]
    cover.append(make_paragraph(doc_type_proto, "{{DOC_TYPE}}"))
    cover.append(make_paragraph(doc_type_proto, "{{TITLE}}", size_half_points=40))
    cover.append(make_paragraph(doc_type_proto, "{{SUBTITLE}}", size_half_points=28, bold=False))
    cover.append(make_paragraph(doc_type_proto, "{{COURSE}}", size_half_points=24, bold=False, italic=True))
    cover += [copy.deepcopy(blank_proto) for _ in range(3)]
    cover.append(make_paragraph(left_label_proto, "{{COORDINATOR_LABEL}}"))
    cover.append(make_paragraph(left_label_proto, "{{COORDINATOR}}", size_half_points=28, bold=False))
    cover.append(copy.deepcopy(blank_proto))
    cover.append(make_paragraph(right_label_proto, "{{TEAM_LABEL}}"))
    cover.append(make_paragraph(right_label_proto, "{{TEAM}}", size_half_points=24, bold=False))
    cover.append(make_paragraph(blank_proto, "{{COVER_FILL}}"))
    cover.append(make_paragraph(city_proto, "{{CITY_YEAR}}"))

    # cover section break: keep its sectPr (first page without header/footer, numbering from 0), drop its text
    for child in list(cover_section_para):
        if child.tag != qn("w:pPr"):
            cover_section_para.remove(child)

    new_body_sectpr = copy.deepcopy(main_section_para.find(qn("w:pPr") + "/" + qn("w:sectPr")))
    for child in list(body):
        body.remove(child)
    for el in cover:
        body.append(el)
    body.append(cover_section_para)
    body.append(new_body_sectpr)  # the main section: odd/even headers, page-number footers
    _ = body_sectpr  # the annex section of the original is dropped

    # --- headers: placeholders for the document title (odd pages) and the team (even pages) -------
    for rel in list(doc.part.rels.values()):
        if rel.reltype == RT.HEADER:
            hdr = rel.target_part.element
            first_t = next(hdr.iter(qn("w:t")), None)
            if first_t is None:
                continue
            jc = hdr.find(".//" + qn("w:jc"))
            first_t.text = "{{HEADER_EVEN}}" if jc is not None and jc.get(qn("w:val")) == "right" else "{{HEADER_ODD}}"
            for t in list(hdr.iter(qn("w:t")))[1:]:
                t.getparent().getparent().remove(t.getparent())

    # --- drop relationships nothing references anymore (example images, OLE objects, links) ------
    referenced = set()
    xml = etree.tostring(doc.element, encoding="unicode")
    for rid in list(doc.part.rels):
        if f'"{rid}"' in xml:
            referenced.add(rid)
    droppable = {RT.IMAGE, RT.OLE_OBJECT, RT.HYPERLINK, RT.CHART, RT.HEADER, RT.FOOTER}
    for rid, rel in list(doc.part.rels.items()):
        if rel.reltype in droppable and rid not in referenced:
            doc.part.drop_rel(rid)

    # --- styles: UT Sans as the body font (the original sets it on every run), TOC entries in UT Sans
    styles = doc.part.styles.element
    set_style_fonts(styles, "Normal", "UT Sans", lang="ro-RO")
    for toc in ("TOC1", "TOC2", "TOC3"):
        set_style_fonts(styles, toc, "UT Sans", size_half_points=22)
    if styles.find(f"{{{W}}}style[@{{{W}}}styleId='TableofFigures']") is None:
        styles.append(etree.fromstring(
            f'<w:style xmlns:w="{W}" w:type="paragraph" w:styleId="TableofFigures">'
            '<w:name w:val="table of figures"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>'
            '<w:uiPriority w:val="99"/><w:unhideWhenUsed/>'
            '<w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9498"/></w:tabs><w:spacing w:after="60"/></w:pPr>'
            '<w:rPr><w:rFonts w:ascii="UT Sans" w:hAnsi="UT Sans" w:cs="UT Sans"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
            '</w:style>'))

    props = doc.core_properties
    props.title = "{{TITLE}}"
    props.author = "Echipa Live Auction App"
    props.subject = "Proiect de Software pentru Telecomunicații"
    props.comments = "Derived from the UNITBV IESC diploma template (Documentatie_Licenta.docx)"
    props.keywords = ""
    props.last_modified_by = "docgen"
    doc.save(dst)
    print(f"template written: {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
