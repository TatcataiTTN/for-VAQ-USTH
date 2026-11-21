#!/bin/bash
# Usage: build/push.sh "commit message"      (DRY=1 build/push.sh  -> chi in danh sach rsync, khong ghi gi)
# Dong bo ban lam viec (khong .venv, scratch, anh chup test) vao clone for-VAQ-USTH/Aircraft-Systems/, commit va push main. Khong bao gio --force.
# Chi chay khi nguoi dung da xac nhan quyen push cho hop phan nay (prompt AE2.021 muc 0).
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)"; R="${REPO:-/Users/tuannghiat/Downloads/USTH - Aircraft Systems/site/for-VAQ-USTH}"
[ -d "$R/.git" ] || { echo "no clone at $R"; exit 1; }
cd "$R" && git pull --ff-only -q
EX=(--exclude '.venv/' --exclude 'scratch/' --exclude 'tests/shots/' --exclude '__pycache__/' --exclude '.DS_Store' --exclude '*.pyc' --exclude '*.ipynb_checkpoints/')
if [ -n "$DRY" ]; then rsync -an --delete --itemize-changes "${EX[@]}" "$SRC/" "$R/Aircraft-Systems/" ; exit 0; fi
rsync -a --delete "${EX[@]}" "$SRC/" "$R/Aircraft-Systems/"
git add -A Aircraft-Systems
if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
git commit -q -m "$1"; git push -q origin main; git log --oneline -1
