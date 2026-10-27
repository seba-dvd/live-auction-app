"""Generate scripts/github/issues.json from the guides (docs/team/<ID>.md) and the backlog (docs/product/backlog.md).

    python scripts/github/build_issues.py

One issue per guide task ("- [ ] **K-S2-03 · Title**" + "Ce / Gata când / Depinde de / Etichete" sub-items)
and one per user story ("### US-07 · Title"). Re-run after editing the guides, then scripts/github/setup.sh
(creation is idempotent: issues are matched by title).
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
REPO_BLOB = "https://github.com/seba-dvd/live-auction-app/blob/main/"
MILESTONES = {
    "S0": "S0 Setup",
    "S1": "S1 Design & fundații",
    "S2": "S2 Fluxuri de bază",
    "S3": "S3 Timp real & integrare",
    "S4": "S4 Cloud & final",
}
AREA_BY_COMPONENT = {
    "frontend": "area:frontend", "user-service": "area:user", "auction-service": "area:auction",
    "bidding-service": "area:bidding", "notification-service": "area:notification", "api-gateway": "area:gateway",
}
RE_TASK = re.compile(r"^- \[ \] \*\*(?P<id>([DMKAR])-(S\d)-\d{2}) · (?P<title>.+?)\*\*\s*$")
RE_STORY = re.compile(r"^### (?P<id>US-\d{2}) · (?P<title>.+?)\s*$")


def guide_tasks(owner: str) -> list[dict]:
    path = ROOT / "docs" / "team" / f"{owner}.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    issues, i = [], 0
    while i < len(lines):
        m = RE_TASK.match(lines[i])
        if not m:
            i += 1
            continue
        block, i = [], i + 1
        while i < len(lines) and lines[i].startswith("  "):
            block.append(lines[i][2:])
            i += 1
        labels = []
        body_lines = []
        for line in block:
            if line.startswith("- **Etichete:**"):
                labels = re.findall(r"`([a-z]+:[A-Za-z]+)`", line)
            else:
                body_lines.append(line)
        sprint = m.group(3)
        body = "\n".join(body_lines).strip()
        body += (f"\n\n---\nResponsabil: **{owner}** · Sprint: **{sprint}** · "
                 f"Ghid: [docs/team/{owner}.md]({REPO_BLOB}docs/team/{owner}.md#6-plan-pe-sprinturi)")
        issues.append({
            "title": f"[{m.group('id')}] {m.group('title')}",
            "body": body,
            "labels": sorted(set([f"owner:{owner}"] + labels)),
            "milestone": MILESTONES[sprint],
        })
    return issues


def backlog_stories() -> list[dict]:
    text = (ROOT / "docs" / "product" / "backlog.md").read_text(encoding="utf-8")
    parts = re.split(r"(?m)^(?=### US-\d{2} · )", text)
    stories = []
    for part in parts:
        lines = part.strip().splitlines()
        if not lines or not RE_STORY.match(lines[0]):
            continue
        m = RE_STORY.match(lines[0])
        meta = lines[1] if len(lines) > 1 else ""
        priority = re.search(r"\*\*Prioritate:\*\*\s*(\w+)", meta).group(1).lower()
        sprint = re.search(r"\*\*Sprint țintă:\*\*\s*(S\d)", meta).group(1)
        components = re.search(r"\*\*Componente:\*\*\s*(.+)$", meta).group(1)
        areas = sorted({AREA_BY_COMPONENT[c.strip()] for c in components.split(",") if c.strip() in AREA_BY_COMPONENT})
        body = "\n".join(lines[1:]).strip()
        body += f"\n\n---\nProduct Owner: **A** · Backlog: [docs/product/backlog.md]({REPO_BLOB}docs/product/backlog.md)"
        stories.append({
            "title": f"[{m.group('id')}] {m.group('title')}",
            "body": body,
            "labels": sorted(["owner:A", "type:story", f"priority:{priority}"] + areas),
            "milestone": MILESTONES[sprint],
        })
    return stories


def main() -> None:
    issues = []
    for owner in ("D", "M", "K", "A", "R"):
        issues += guide_tasks(owner)
    issues += backlog_stories()
    titles = [i["title"] for i in issues]
    duplicates = {t for t in titles if titles.count(t) > 1}
    if duplicates:
        sys.exit(f"duplicate titles: {duplicates}")
    out = ROOT / "scripts" / "github" / "issues.json"
    out.write_text(json.dumps(issues, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    by_owner = {}
    for i in issues:
        owner = next(l for l in i["labels"] if l.startswith("owner:"))
        by_owner[owner] = by_owner.get(owner, 0) + 1
    print(f"{len(issues)} issues -> {out.relative_to(ROOT)}  {by_owner}")


if __name__ == "__main__":
    main()
