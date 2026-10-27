"""Create the issues of scripts/github/issues.json that do not exist yet (matched by title). Idempotent.

    python scripts/github/create_issues.py <owner>/<repo>

Uses the GitHub CLI (gh). Pauses ~1 s between creations to respect GitHub's secondary rate limits.
"""
import json
import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent


def gh(*args: str, stdin: str | None = None) -> str:
    result = subprocess.run(["gh", *args], input=stdin, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def main(repo: str) -> None:
    issues = json.loads((HERE / "issues.json").read_text(encoding="utf-8"))
    existing = set(json.loads(gh("issue", "list", "-R", repo, "--state", "all", "--limit", "1000", "--json", "title",
                                 "--jq", "[.[].title]")))
    milestones = json.loads(gh("api", f"repos/{repo}/milestones?state=all&per_page=100",
                               "--jq", "[.[] | {title, number}]"))
    number_of = {m["title"]: m["number"] for m in milestones}
    created = 0
    for issue in issues:
        if issue["title"] in existing:
            continue
        payload = {"title": issue["title"], "body": issue["body"], "labels": issue["labels"]}
        if issue.get("milestone") in number_of:
            payload["milestone"] = number_of[issue["milestone"]]
        gh("api", f"repos/{repo}/issues", "-X", "POST", "--input", "-", stdin=json.dumps(payload, ensure_ascii=False))
        created += 1
        print(f"  created {issue['title']}")
        time.sleep(1.1)
    print(f"issues: {created} created, {len(issues) - created} already existed")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
