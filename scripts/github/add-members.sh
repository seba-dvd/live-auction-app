#!/usr/bin/env bash
# Invite the team as collaborators with push access (idempotent) and print the CODEOWNERS lines to enable.
#   bash scripts/github/add-members.sh                  # usernames from scripts/github/team.env
#   bash scripts/github/add-members.sh M=ana K=bogdan   # or pass them (also saved into team.env)
# After everyone accepted the invitation: bash scripts/github/assign-issues.sh
set -uo pipefail
cd "$(dirname "$0")/../.."
ENV_FILE=scripts/github/team.env

for pair in "$@"; do
  id="${pair%%=*}"; user="${pair#*=}"
  case "$id" in D|M|K|A|R) sed -i "s/^$id=.*/$id=$user/" "$ENV_FILE" ;; *) echo "ignored: $pair" ;; esac
done
# shellcheck disable=SC1090
source "$ENV_FILE"
OWNER="$(gh api user --jq .login)"
FULL="$OWNER/${REPO_NAME:-live-auction-app}"

invited=0
for id in D M K A R; do
  user="${!id:-}"
  if [ -z "$user" ]; then echo "  $id: no username yet (edit $ENV_FILE)"; continue; fi
  if [ "$user" = "$OWNER" ]; then echo "  $id: $user is the owner"; continue; fi
  if gh api -X PUT "repos/$FULL/collaborators/$user" -f permission=push --silent; then
    echo "  $id: invited $user (push)"; invited=$((invited + 1))
  else
    echo "  $id: could not invite $user"
  fi
done

cat <<EOF

CODEOWNERS lines to enable (open a PR that edits .github/CODEOWNERS and $ENV_FILE):
  /bidding-service/  /docs/api-contracts.md  /docs/architecture.md  /docs/decisions/  /docs/uml/   -> @${M:-<M>}
  /auction-service/  /docs/database/                                                            -> @${K:-<K>}
  /frontend/  /docs/product/                                                                    -> @${A:-<A>}
  /notification-service/  /db/  /docker-compose*.yml  /.github/  /postman/  /tools/ws-test.html -> @${R:-<R>}
Invitations sent now: $invited. When accepted, run: bash scripts/github/assign-issues.sh
EOF
