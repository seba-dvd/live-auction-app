#!/usr/bin/env bash
# Builds the Word documents in the UNITBV template style from the Markdown sources, then (on Windows with
# Microsoft Word) refreshes the table of contents / lists and exports PDFs.
#   bash tools/docgen/build.sh                    # everything
#   bash tools/docgen/build.sh raport             # one or more of: raport charter guides
#   NO_WORD=1 bash tools/docgen/build.sh          # .docx only (fields refresh when the file is opened in Word)
set -euo pipefail
cd "$(dirname "$0")/../.."

VENV=tools/docgen/.venv
python_in_venv() {
  if [ -x "$VENV/Scripts/python.exe" ]; then echo "$VENV/Scripts/python.exe"; else echo "$VENV/bin/python"; fi
}
if [ ! -x "$(python_in_venv)" ]; then
  echo "Creating $VENV and installing python-docx..."
  (python -m venv "$VENV" 2>/dev/null || python3 -m venv "$VENV")
  "$(python_in_venv)" -m pip install --quiet --disable-pip-version-check -r tools/docgen/requirements.txt
fi
PY="$(python_in_venv)"

declare -A CONFIG=(
  [raport]=docs/raport-tehnic/document.toml
  [charter]=docs/project-charter/document.toml
  [guides]=docs/team/documents.toml
)
targets=("$@")
[ ${#targets[@]} -eq 0 ] && targets=(charter raport guides)

configs=()
for t in "${targets[@]}"; do
  [ -n "${CONFIG[$t]:-}" ] || { echo "unknown target: $t (use: raport charter guides)" >&2; exit 1; }
  configs+=("${CONFIG[$t]}")
done

mapfile -t outputs < <("$PY" -X utf8 tools/docgen/build_docx.py "${configs[@]}" | tee /dev/stderr | sed -n 's/^built //p')

if [ "${NO_WORD:-}" = "1" ] || ! command -v powershell.exe >/dev/null 2>&1; then
  echo "Skipping the Word refresh (TOC, lists, PDF). Open the .docx in Word and press F9 on the TOC, or run update_fields.ps1."
  exit 0
fi
win_paths=()
for o in "${outputs[@]}"; do win_paths+=("$(cygpath -w "$o" 2>/dev/null || echo "$o")"); done
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w tools/docgen/update_fields.ps1 2>/dev/null || echo tools/docgen/update_fields.ps1)" "${win_paths[@]}"
