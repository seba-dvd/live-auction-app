#!/usr/bin/env bash
# Renders every PlantUML diagram (docs/uml/*.puml, docs/database/*.puml) to docs/diagrams/png/ (150 dpi).
# Needs only Java 21 (already required for the backend). The first run downloads PlantUML (MIT build, ~13 MB)
# from Maven Central into tools/diagrams/ (git-ignored) and verifies its SHA-1. No Graphviz needed (smetana layout).
#   bash tools/diagrams/render.sh                 # all diagrams
#   bash tools/diagrams/render.sh docs/uml/use-case.puml   # only some
set -euo pipefail
cd "$(dirname "$0")/../.."

VERSION=1.2026.9
JAR="tools/diagrams/plantuml-mit-$VERSION.jar"
BASE="https://repo1.maven.org/maven2/net/sourceforge/plantuml/plantuml-mit/$VERSION/plantuml-mit-$VERSION.jar"

if [ ! -f "$JAR" ]; then
  echo "Downloading PlantUML $VERSION (MIT) from Maven Central..."
  curl -fsSL -o "$JAR.part" "$BASE"
  expected=$(curl -fsSL "$BASE.sha1" | cut -c1-40)
  actual=$(sha1sum "$JAR.part" | cut -c1-40)
  if [ "$expected" != "$actual" ]; then
    rm -f "$JAR.part"
    echo "SHA-1 mismatch for $JAR (expected $expected, got $actual)" >&2
    exit 1
  fi
  mv "$JAR.part" "$JAR"
fi

if [ "$#" -gt 0 ]; then
  files=("$@")
else
  files=(docs/uml/[!_]*.puml docs/database/*.puml)
fi

mkdir -p docs/diagrams/png
# -o is relative to each source file: docs/uml/../diagrams/png and docs/database/../diagrams/png
java -Djava.awt.headless=true -DPLANTUML_LIMIT_SIZE=8192 -jar "$JAR" \
  -charset UTF-8 -tpng -failfast2 -o ../diagrams/png "${files[@]}"
echo "Rendered ${#files[@]} diagram(s) into docs/diagrams/png/"
