#!/bin/bash
# Usage: build/push.sh "commit message"   — sync site (without 80 MB sources / OCR_output) into the local for-VAQ-USTH clone, commit, push.
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)"; R="${REPO:-/Users/tuannghiat/Downloads/USTH - Aircraft Systems/site/for-VAQ-USTH}"
cd "$R" && git pull --ff-only -q
rsync -a --delete --exclude 'sources/' --exclude 'OCR_output/' --exclude 'tests/shots/' --exclude '__pycache__/' --exclude '.DS_Store' --exclude '*.pyc' "$SRC/" "$R/Electronics-2/"
git add -A; if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
git commit -q -m "$1"; git push -q origin main; git log --oneline -1
