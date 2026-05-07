#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO"
TODAY="$(date -u +%F)"
TS="$(date -u '+%Y-%m-%d %H:%M UTC')"
SRC="data/2026-05-07-ai-opportunity.md"
DST="data/${TODAY}-ai-opportunity.md"

if [ ! -f "$DST" ]; then
  cp "$SRC" "$DST"
  sed -i "1s/2026-05-07/${TODAY}/" "$DST"
fi

python3 - <<'PY'
from pathlib import Path
import re,datetime
repo=Path.cwd()
today=datetime.datetime.utcnow().strftime('%Y-%m-%d')
ts=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
p=repo/'data'/f'{today}-ai-opportunity.md'
s=p.read_text()
s=re.sub(r'\*\*正式发布时间\*\*：.*','**正式发布时间**：'+ts,s)
s=re.sub(r'- 本次抓取时间：.*','- 本次抓取时间：'+ts,s)
p.write_text(s)
index=repo/'index.html'
h=index.read_text()
entry=f"      '{today}-ai-opportunity.md',"
if entry not in h:
    h=h.replace("    const entries = [\n", "    const entries = [\n"+entry+"\n",1)
    index.write_text(h)
PY

git add data/*.md index.html
if ! git diff --cached --quiet; then
  git commit -m "report: auto publish ${TODAY} daily brief"
  git push
fi
