#!/bin/bash
# Usage: build/push.sh "commit message"
# Sync the site (without .venv, scratch, test screenshots) into the local for-VAQ-USTH clone as Thermal-Systems/, commit and push to main.
# The user authorised a push after each finished component (module, tool set, QA); never use --force.
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)"; R="${REPO:-/Users/tuannghiat/Downloads/USTH - Aircraft Systems/site/for-VAQ-USTH}"
[ -d "$R/.git" ] || { echo "no clone at $R"; exit 1; }
cd "$R" && git pull --ff-only -q
mkdir -p "$R/Thermal-Systems"
rsync -a --delete --exclude '.venv/' --exclude 'scratch/' --exclude 'tests/shots/' --exclude '__pycache__/' --exclude '.DS_Store' --exclude '*.pyc' --exclude '*.ipynb_checkpoints/' --exclude '_shared/analyse.js' --exclude '_shared/exercises.js' --exclude '_shared/written.js' --exclude '_shared/concepts.js' --exclude 'tests/site_test.py' --exclude 'tests/site_test.js' --exclude 'tests/tools_test.py' --exclude 'tests/concepts_test.py' --exclude 'tests/exam_test.py' --exclude 'tests/check_deck.py' "$SRC/" "$R/Thermal-Systems/"
python3 - <<'PY'
import re
p='index.html'; t=open(p,encoding='utf-8').read()
if 'Thermal-Systems/' not in t:
    card='''<a class="card" href="Thermal-Systems/vi/index.html">
  <h2>🔥 AE2.013 — Thermal Systems (Hệ thống nhiệt)</h2>
  <p>Chu trình công suất khí, chu trình lạnh và điều hoà trên tàu bay, quá trình cháy, dòng nén được: bám slide giảng viên + Cengel + El-Sayed + Farokhi — song ngữ VI/EN, bảng thuộc tính tra được, máy tính chu trình.</p>\n</a>\n'''
    t=t.replace('<a class="card" href="mechanics-2/">',card+'<a class="card" href="mechanics-2/">',1); open(p,'w',encoding='utf-8').write(t)
PY
git add -A Thermal-Systems index.html
if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
git commit -q -m "$1"; git push -q origin main; git log --oneline -1
