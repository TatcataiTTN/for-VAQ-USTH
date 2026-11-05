# -*- coding: utf-8 -*-
"""Quality check of the deck in a real browser (Selenium + Chrome).
For every slide: overflow outside the 1280x720 canvas, smallest rendered text size (must be >= 20 px),
free space at the bottom (content should reach at least y = 600 px), broken images. Saves a screenshot per slide.
Usage: python3 check_deck.py [screenshot_dir] [url_or_file_url]   (needs: pip install selenium; Chrome installed)
"""
import os, sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HERE = os.path.dirname(os.path.abspath(__file__))
URL = sys.argv[2] if len(sys.argv) > 2 else "file://" + os.path.abspath(os.path.join(HERE, "index.html"))   # arg 2: URL or file:// path of the deck page
SHOTS = sys.argv[1] if len(sys.argv) > 1 else None
if SHOTS: os.makedirs(SHOTS, exist_ok=True)
JS = """
var s=document.querySelectorAll('.mdeck-slide')[arguments[0]];var r0=s.getBoundingClientRect();var k=r0.width/1280;
var maxB=0,minF=999,minWho='',over=0;
s.querySelectorAll('*').forEach(function(e){var r=e.getBoundingClientRect();if(!r.width||!r.height)return;
  var cs=getComputedStyle(e);
  var hasText=[].some.call(e.childNodes,function(n){return n.nodeType===3&&n.textContent.trim().length>0});
  if(hasText){var fs=parseFloat(cs.fontSize);if(e.closest('svg')){fs=fs}if(fs<minF){minF=fs;minWho=e.tagName+':'+e.textContent.trim().slice(0,25)}}
  var isBg=(e.tagName==='H2')||e.classList.contains('logo-chip')||e.closest('.logo-chip');
  var b=(r.bottom-r0.top)/k; if(!isBg&&e.tagName!=='LI'&&b>maxB&&b<=800)maxB=b;
  var o=Math.max((r.bottom-r0.bottom)/k,(r.right-r0.right)/k);if(o>over)over=o;});
var broken=[].filter.call(s.querySelectorAll('img'),function(i){return !i.complete||i.naturalWidth===0}).length;
return [Math.round(over),Math.round(minF*10)/10,minWho,Math.round(maxB),broken,s.querySelector('h2').textContent.slice(0,40)];
"""
o = Options(); o.add_argument("--headless=new"); o.add_argument("--window-size=1400,900"); o.add_argument("--hide-scrollbars")
d = webdriver.Chrome(options=o); d.get(URL); time.sleep(2)
n = d.execute_script("return document.querySelectorAll('.mdeck-slide').length"); bad = 0
print("slides:", n)
for i in range(n):
    d.execute_script("document.querySelectorAll('.mdeck-slide').forEach(function(s,k){s.classList.toggle('active',k==%d)})" % i); time.sleep(0.25)
    over, minf, who, bottom, broken, title = d.execute_script(JS, i)
    edge = i in (0, n - 1)
    flags = []
    if over > 2: flags.append("OVERFLOW %dpx" % over)
    if minf < 20: flags.append("SMALL TEXT %.1fpx (%s)" % (minf, who))
    if not edge and bottom < 600: flags.append("EMPTY BOTTOM: content ends at y=%d" % bottom)
    if broken: flags.append("BROKEN IMAGES %d" % broken)
    if flags: bad += 1
    print("%2d %-40s bottom=%3d minfont=%4.1f %s" % (i + 1, title, bottom, minf, " | ".join(flags)))
    if SHOTS: d.find_element("css selector", ".mdeck-canvas-wrap").screenshot(os.path.join(SHOTS, "s%02d.png" % (i + 1)))
print("slides with problems:", bad); d.quit()
