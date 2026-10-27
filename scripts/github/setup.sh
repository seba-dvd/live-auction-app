#!/usr/bin/env bash
# One-time (idempotent, re-runnable) GitHub setup for live-auction-app. Run from the repository root, in Git Bash:
#   bash scripts/github/setup.sh
# Needs: git, gh (logged in, scopes repo + workflow; "project" optional), python.
# Steps: repo -> branches -> settings -> protection -> labels -> milestones -> issues -> invitations -> project.
set -uo pipefail
cd "$(dirname "$0")/../.."
# shellcheck disable=SC1091
source scripts/github/team.env

OWNER="$(gh api user --jq .login)"
FULL="$OWNER/${REPO_NAME:-live-auction-app}"
PERSONAL_BRANCHES=(d/user-gateway m/bidding k/auction a/frontend r/devops)
PY="$(command -v python || command -v python3)"
step() { printf '\n==> %s\n' "$*"; }

step "1. Repository $FULL (private)"
if gh repo view "$FULL" >/dev/null 2>&1; then
  echo "exists"
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$FULL.git"
  git push -u origin main
else
  gh repo create "$FULL" --private --source . --remote origin --push \
    --description "Live auction platform with virtual coins (Spring Boot microservices, React, MySQL, Docker)"
fi

step "2. Branches: develop from main, personal branches from develop"
git fetch origin --quiet
for branch in develop "${PERSONAL_BRANCHES[@]}"; do
  if git ls-remote --exit-code --heads origin "$branch" >/dev/null 2>&1; then
    echo "  $branch exists"
  else
    base=main; [ "$branch" != develop ] && base=develop
    git push --quiet origin "origin/$base:refs/heads/$branch" && echo "  $branch created from $base"
    git fetch origin --quiet
  fi
done

step "3. Settings: merge commits only, keep head branches, default branch main"
gh api -X PATCH "repos/$FULL" -F allow_merge_commit=true -F allow_squash_merge=false -F allow_rebase_merge=false \
  -F delete_branch_on_merge=false -f default_branch=main --silent && echo "  ok"

step "4. Branch protection on main and develop"
PROTECTION='{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}'
PROTECTION_OK=true
for branch in main develop; do
  if out=$(gh api -X PUT "repos/$FULL/branches/$branch/protection" --input - <<<"$PROTECTION" 2>&1); then
    echo "  $branch protected"
  else
    PROTECTION_OK=false
    echo "  $branch NOT protected: $(echo "$out" | head -1)"
  fi
done
if [ "$PROTECTION_OK" = false ]; then
  cat <<'MSG'
  Branch protection on a PRIVATE repository needs GitHub Pro (or Team). Options:
    a) activate GitHub Pro for free with the GitHub Student Developer Pack (https://education.github.com/pack),
       then re-run this script;
    b) make the repository public: gh repo edit --visibility public --accept-visibility-change-consequences
MSG
fi

step "5. Labels"
create_label() { gh label create "$1" --color "$2" --description "$3" --force -R "$FULL" >/dev/null && echo "  $1"; }
for id in D M K A R; do create_label "owner:$id" "5319e7" "Owned by $id (see docs/team/$id.md)"; done
for area in gateway user auction bidding notification frontend devops docs; do create_label "area:$area" "1d76db" "Area: $area"; done
create_label "type:feature" "0e8a16" "New functionality"
create_label "type:story" "fbca04" "User story (Product Owner)"
create_label "type:bug" "d73a4a" "Something does not work as specified"
create_label "type:docs" "c5def5" "Documentation"
create_label "type:infra" "bfd4f2" "Docker, CI/CD, cloud"
create_label "type:uml" "d4c5f9" "UML / ER diagrams"
create_label "type:chore" "ededed" "Project chores"
create_label "priority:must" "b60205" "MoSCoW: must have"
create_label "priority:should" "d93f0b" "MoSCoW: should have"
create_label "priority:could" "e99695" "MoSCoW: could have"

step "6. Milestones (due 23:59 Europe/Bucharest = 21:59Z)"
existing_ms="$(gh api "repos/$FULL/milestones?state=all&per_page=100" --jq '.[].title')"
create_milestone() {
  if grep -Fxq "$1" <<<"$existing_ms"; then echo "  $1 exists"; else
    gh api "repos/$FULL/milestones" -f title="$1" -f due_on="$2" -f description="$3" --silent && echo "  $1 created"
  fi
}
create_milestone "S0 Setup" "2026-11-08T21:59:00Z" "28.10–08.11.2026: everyone runs the stack; topic and roles presented"
create_milestone "S1 Design & fundații" "2026-11-22T21:59:00Z" "09.11–22.11.2026: UML, DB design, contracts v1, entities, auth"
create_milestone "S2 Fluxuri de bază" "2026-12-06T21:59:00Z" "23.11–06.12.2026: auctions, bidding with reservations, WebSocket; report 30.11"
create_milestone "S3 Timp real & integrare" "2026-12-20T21:59:00Z" "07.12–20.12.2026: anti-sniping, settlement, notifications, Postman"
create_milestone "S4 Cloud & final" "2027-01-17T21:59:00Z" "04.01–17.01.2027: cloud deployment, CD, demo"

step "7. Issues (from scripts/github/issues.json)"
"$PY" scripts/github/create_issues.py "$FULL"

step "8. Collaborators (push access)"
bash scripts/github/add-members.sh

step "9. GitHub Project (optional)"
if gh auth status 2>&1 | grep -q "'project'"; then
  number="$(gh project list --owner "$OWNER" --format json --jq '.projects[] | select(.title=="Live Auction – Scrum") | .number' | head -1)"
  if [ -z "$number" ]; then
    number="$(gh project create --owner "$OWNER" --title "Live Auction – Scrum" --format json --jq .number)"
    echo "  project #$number created"
  fi
  gh project link "$number" --owner "$OWNER" --repo "$FULL" >/dev/null 2>&1 || true
  for url in $(gh issue list -R "$FULL" --state open --limit 500 --json url --jq '.[].url'); do
    gh project item-add "$number" --owner "$OWNER" --url "$url" >/dev/null 2>&1 || true
  done
  echo "  issues added to project #$number"
else
  echo "  skipped: the gh token has no 'project' scope. Run: gh auth refresh -s project   then re-run this script."
fi

step "Done: https://github.com/$FULL"
