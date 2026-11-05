# Brief for module agents — AE2.025 Electronics 2 self-study site

Project root: `/home/user/e2/Electronics-2` (call it `$P`). Static bilingual site (vi/ + en/), built by
`python3 build/assemble.py && python3 build/build_site.py` (prefix both with `ONLY=mXX,mYY` to build only your modules).
Read `build/modules.py` (module list + mapping), `build/hx.py` (HTML helpers), `build/build_site.py` (how your files are used).
Reference example of a module content file (other course, Vietnamese only, same helpers):
`/root/.claude/skills/synced/b70dbdc7-329f-4fb7-bd71-363889fbbb45_3b60fab7-8cc4-43a4-994a-7f1fd8357944/self-study-ptit-practice-template/templates/ptit-interactive/examples/content_module_example.py`

## Sources (already downloaded, text layer available)
| key | file | notes |
|---|---|---|
| Floyd 9e | `$P/sources/floyd.pdf` (976 p) | pdf page = printed page + 18 (verify at your chapter with ≥2 pages). Full text: `$P/OCR_output/floyd/text/full_layout.txt`. Chapter end = SUMMARY, KEY TERMS, KEY FORMULAS, TRUE/FALSE QUIZ, CIRCUIT-ACTION QUIZ, SELF-TEST, PROBLEMS. **The book prints NO answers for True/False, Circuit-Action and Self-Test** ("answers at pearsonhighered.com") → you solve and verify each one. Odd-numbered Problems answers: pdf pages 949–961. |
| Jaeger 5e (2015) | `$P/sources/jaeger_2015.pdf` (1355 p) | primary Jaeger edition (has Digital ch.6–9). End of chapter = Problems (no answers in book). Get page offsets from `fitz` TOC. |
| Jaeger 6e | `$P/sources/jaeger.pdf` | analog-only edition, use only if needed. |
| EASA M04 (B2) | `$P/sources/easa_m04_ocr.pdf` (OCR'd scan, 126 p) | per-page OCR text: `$P/OCR_output/easa_m04/ocr_raw/ocrmypdf/pNNN.txt` and second method `.../ocr_raw/psm4/pNNN.txt` (being generated; may lag); 300-dpi images `.../pages300/pNNN.png`. SM01 IC/logic p55–75, Q p76/78/80/82/84/86, A p77/79/…/87. SM02 PCB p88–97, Q p98,100, A p99,101. SM03 Servo p102–114, Q p116,118, A p117,119. Questions are open questions with printed answers. |

`pdftotext` drops symbols (=, Ω→"Æ", μ, ≥, subscripts). For ANY question/formula with symbols or a figure, render the page
(`pdftoppm -r 150 -f N -l N -png src.pdf out`) and READ THE IMAGE (Read tool) before writing it. Do not guess.

## What you produce (only these paths; never edit shared files `_shared/*`, `build/*.py`, other modules' files)
1. `build/content/mNN.py` — `def module(lang):` returns
   `dict(subtitle=str, time=str, objectives=[str], parts=[dict(title, bullets=[str], slides=[html])], notes=html)`
   built with `from hx import *` (`sl, formula, callout, ex, table, ul, code, fig, tr`). Use `tr('vi text','en text')` or `if lang=='vi'`.
   Both languages fully written (Vietnamese natural academic style, English technical). Images: `fig('assets/figs/mNN/x.png', alt, caption)`.
   - Deck = 5 parts (1 Foundations · 2 Methods/analysis · 3 Worked examples from the books · 4 Pitfalls & extensions · 5 Aircraft application & summary), 3–5 slides each,
     slide titles are noun phrases (no question marks), every content slide has `explain=` (beginner explanation).
   - `notes` (HTML): 1 detailed content mapped to book sections (cite "Floyd §12–3", "Jaeger §10.9", "EASA M04 p.1.62" — only pages you actually read),
     2 five worked examples with full numeric solutions (numbers computed by your verify script), 3 history/theory context, 4 aircraft case study
     (real, non-invented systems; if unsure say "minh hoạ/illustrative"), 5 exam pitfalls.
   - Keep it dense and useful, no filler. Plain HTML; math in Unicode (Av = −Rf/Ri, f₀ = 1/(2πRC)).
2. `data/qsrc/mNN.json` — ORIGINAL questions (origin `"goc"`), list of items:
   ```json
   {"kind":"mcq|tf|ca|ess","q":{"vi":"..","en":".."},"opts":[{"vi":"..","en":".."}],"correct":0,
    "explain":{"vi":"..","en":".."},"level":1,"topic":{"vi":"..","en":".."},
    "src":{"vi":"Floyd 9e, Ch.12, Self-Test câu 8 (tr.654)","en":"Floyd 9e, Ch.12, Self-Test Q8 (p.654)"},
    "origin":"goc","fixed_order":false,"fig":"assets/figs/m02/fig12_18.png","check":"script|chapter text p.632|EASA printed answer"}
   ```
   - kinds: `mcq` Self-Test (3–4 options), `tf` True/False (opts True/False = Đúng/Sai), `ca` Circuit-Action (increase/decrease/not change), `ess` worked problem (`sol` instead of opts/explain/correct).
   - Take ALL Self-Test, True/False and Circuit-Action items of your Floyd chapters (for m04: only items of the sections in modules.py). `en` text = book wording (fix only OCR glitches); `vi` = faithful translation.
   - `fixed_order: true` when an option refers to other options ("answers (a) and (c)", "all of the above") or for tf/ca. Explanations must never cite option letters; cite the option text.
   - Circuit-action / figure-dependent items: crop the referenced figure (render pdf page at 150 dpi, crop with PIL to the figure, save `assets/figs/mNN/<name>.png`, look at it) and set `fig`.
   - Explanations: why correct + why the main distractor is wrong, with numbers when numeric.
   - `ess`: 8–15 per module chosen from end-of-chapter Problems (Floyd and/or Jaeger) and EASA questions, with full step-by-step `sol`. Floyd odd problems → compare with the book's answer section.
3. `build/verify/verify_mNN.py` — recomputes every numeric answer/solution with Python (sympy/numpy), `assert`s it matches what is stored in the JSON, prints a table. Must run clean.
4. `build/gen/gen_mNN.py` → writes `data/qsrc/mNN_gen.json` — GENERATED similar questions (origin `"bo_sung"`, src `{"vi":"Bổ sung – sinh theo dạng <Floyd Self-Test Q8>","en":"Generated – modelled on <…>"}`), `random.Random(fixed seed)`.
   Mostly numeric variants of the book items (gain, CMRR, f_c, slew rate, …): answer computed by formula, 3 distractors = typical mistakes (forgot +1, used wrong formula, unit/decade slip), all distinct, same formatting as the correct one.
   Also conceptual variants (bilingual) where numeric is impossible. Target: originals + generated ≥ 80 MCQ per module. Write JSON atomically (tmp + os.replace).
5. `data/verify/mNN_notes.json` — `{"vi":[..],"en":[..]}`: errata/doubts found in the source (ambiguous items, misprints, OCR damage, items removed and why). Empty lists if none.
6. Notebook: `build/nb/make_mNN.py` builds BOTH `notebooks/mNN_<slug-without-number-with-underscores>_vi.ipynb` and `_en.ipynb` (e.g. `m02_op_amp_vi.ipynb`) with nbformat,
   then executes them: `jupyter nbconvert --to notebook --execute --inplace <file>` (must succeed). Each method cell: markdown "what question it answers" → code with prints/plots (numpy/scipy/matplotlib) → markdown interpreting the REAL output. 6–10 sections reproducing the module's key calculations / book examples (gain, frequency response, waveforms…).
7. Figures for slides (matplotlib) → `assets/figs/mNN/*.png`, figsize = displayed px/100, dpi 100, fonts ≥ 14 pt, both languages if labels contain words (`_vi.png`/`_en.png`).

## Quality rules
- Never invent numbers, page numbers or facts; unclear → note it in mNN_notes.json and drop the item.
- Every original answer you store must be justified (chapter text or computation). If the book item is defective (no correct option / two correct), keep it only if you can fix it transparently in the explanation, else drop it and log it.
- Vietnamese: dùng thuật ngữ chuẩn (khuếch đại thuật toán, hồi tiếp âm, hệ số khuếch đại vòng kín, tần số cắt, độ dốc biến thiên (slew rate), …), giữ ký hiệu tiếng Anh trong ngoặc lần đầu.
- After finishing: `cd $P && ONLY=<your ids> python3 build/assemble.py && ONLY=<your ids> python3 build/build_site.py` must succeed; open one generated page file to sanity-check;
  run your verify script and notebook execution. Check bias line printed by assemble (correct_is_longest should be < 0.35 for generated mcq; fix distractor lengths if not).
- Be token-efficient: do not read whole chapters; use the chapter summary, key formulas, section headings and the quiz pages; use grep on full_layout.txt.

## Final report (keep it short, < 250 words)
Counts per module (originals by kind, generated, ess), verify script result, notebook execution result, list of errata, anything you could not do.
