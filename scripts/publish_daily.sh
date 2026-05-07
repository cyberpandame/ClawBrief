#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO"
TODAY="$(date -u +%F)"
python3 scripts/build_daily_report.py

git add data/*.md index.html monitoring.html
if ! git diff --cached --quiet; then
  git commit -m "report: auto publish ${TODAY} daily brief"
  git push
fi
