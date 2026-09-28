#!/bin/bash
# Render 1 hoac nhieu trang PDF o DPI cao de doc bang mat / crop hinh.
# Dung: ./render_pages.sh <file.pdf> <first_page> <last_page> [dpi=600]
set -e
PDF="$1"; FIRST="$2"; LAST="${3:-$FIRST}"; DPI="${4:-600}"
OUT=/tmp/page_render
mkdir -p "$OUT"
rm -f "$OUT"/p-*.png
pdftoppm -r "$DPI" -f "$FIRST" -l "$LAST" -png "$PDF" "$OUT/p"
echo "Rendered pages $FIRST-$LAST at ${DPI}dpi to $OUT/"
ls -la "$OUT"
