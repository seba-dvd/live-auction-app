#!/usr/bin/env bash
# Assign every open issue to its owner, using the owner:<ID> label and the usernames in scripts/github/team.env.
# Run AFTER the members accepted their invitations (GitHub only assigns collaborators). Idempotent.
#   bash scripts/github/assign-issues.sh
set -uo pipefail
cd "$(dirname "$0")/../.."
# shellcheck disable=SC1091
source scripts/github/team.env
OWNER="$(gh api user --jq .login)"
FULL="$OWNER/${REPO_NAME:-live-auction-app}"

for id in D M K A R; do
  user="${!id:-}"
  if [ -z "$user" ]; then echo "$id: no username in team.env, skipped"; continue; fi
  count=0
  for number in $(gh issue list -R "$FULL" --label "owner:$id" --state open --limit 500 --json number --jq '.[].number'); do
    if gh issue edit "$number" -R "$FULL" --add-assignee "$user" >/dev/null 2>&1; then
      count=$((count + 1))
    else
      echo "  #$number: could not assign $user (invitation not accepted yet?)"
    fi
    sleep 0.5
  done
  echo "$id ($user): $count issues assigned"
done
