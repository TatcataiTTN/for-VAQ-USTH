#!/bin/bash
# Second OCR method for the EASA scan: render 300 dpi gray PNG, tesseract --psm 4, one txt per page.
cd "$(dirname "$0")/../../OCR_output/easa_m04"
for p in $(seq 1 126); do
  f=$(printf "pages300/p%03d" $p)
  [ -f $f.png ] || pdftoppm -gray -r 300 -f $p -l $p -singlefile -png ../../sources/easa_m04.pdf $f
  tesseract $f.png ocr_raw/psm4/$(printf "p%03d" $p) --psm 4 -l eng >/dev/null 2>&1
done
echo done
