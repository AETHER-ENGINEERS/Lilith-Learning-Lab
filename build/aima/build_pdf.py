#!/usr/bin/env python3
"""Build the AIMA tutorial PDF (tutorialspoint style) from part*.md. Usage: python3 build_pdf.py out.pdf"""
import re, sys, glob, html, markdown
from playwright.sync_api import sync_playwright
out = sys.argv[1]
md = "\n\n".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob("part*.md")))
extra = "extra.md"
import os
from extra import EX
if os.path.exists(extra): md += "\n\n" + open(extra, encoding="utf-8").read()
md = re.sub(r"(?m)^([^\s\-\*\d|#>`].*)\n(?=(?:- |\* |\d+\. ))", r"\1\n\n", md)
# split into chapters (# heading) so each starts on a new page; number the h2s
chs = re.split(r"(?m)^# ", md)[1:]
body, toc = [], []
for i, c in enumerate(chs):
    title, rest = c.split("\n", 1)
    cid = "c%d" % i
    toc.append((cid, title.strip()))
    m0 = re.match(r"(\d+)\.", title)
    if m0 and int(m0.group(1)) in EX:
        t_, q_ = EX[int(m0.group(1))]
        rest += "\n\n## Key terms\n\n| Term | Meaning |\n|---|---|\n" + "\n".join("| **%s** | %s |" % x for x in t_)
        rest += "\n\n## Check your understanding\n\n" + "\n\n".join("**Q%d. %s**\n\n*Answer:* %s" % (j + 1, q, a) for j, (q, a) in enumerate(q_))
    h = markdown.markdown(rest, extensions=["tables", "sane_lists", "fenced_code"])
    h = re.sub(r"<h2>(.*?)</h2>", lambda m: "<h2>%s</h2>" % m.group(1), h)
    body.append('<section class="chap" id="%s"><div class="chno">%s</div><h1>%s</h1>%s</section>' % (cid, "Appendix" if title.startswith("Appendix") else "Chapter " + title.split(".")[0], html.escape(re.sub(r"^(Appendix )?[A-Z0-9]+\.\s*", "", title)), h))
tocH = "".join('<li><a href="#%s">%s</a></li>' % (cid, html.escape(t)) for cid, t in toc)
CSS = """
@page{size:A4;margin:22mm 18mm 20mm 18mm}
*{box-sizing:border-box}
body{font:11.5pt/1.62 'DejaVu Serif',Georgia,serif;color:#222;margin:0}
.cover{height:250mm;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;page-break-after:always;background:linear-gradient(180deg,#2c1a52,#150d27);color:#fff;margin:-22mm -18mm;padding:30mm;height:297mm;width:210mm}
.cover h1{font:700 34pt/1.15 'DejaVu Sans',sans-serif;margin:0 0 10mm;color:#e0c8ff}
.cover .sub{font:16pt 'DejaVu Sans',sans-serif;color:#c9b5f0;margin-bottom:30mm}
.cover .note{font:10pt/1.5 'DejaVu Sans',sans-serif;color:#b3a2d6;max-width:130mm;border-top:1px solid #6d52a8;padding-top:6mm}
.tocpage{page-break-after:always;padding-top:4mm}
.tocpage h1{font:700 24pt 'DejaVu Sans',sans-serif;color:#4b2a8a;border-bottom:3px solid #b26bff;padding-bottom:3mm}
.tocpage ol{list-style:none;padding:0;columns:1}
.tocpage li{padding:2.2mm 0;border-bottom:1px dotted #ccc;font:11.5pt 'DejaVu Sans',sans-serif}
.tocpage a{color:#222;text-decoration:none}
.chap{page-break-before:always}
.chno{font:700 11pt 'DejaVu Sans',sans-serif;letter-spacing:2px;text-transform:uppercase;color:#b26bff;margin-top:8mm}
.chap>h1{font:700 26pt/1.15 'DejaVu Sans',sans-serif;color:#2c1a52;margin:2mm 0 8mm;padding-bottom:3mm;border-bottom:3px solid #b26bff}
h2{font:700 15pt 'DejaVu Sans',sans-serif;color:#4b2a8a;margin:8mm 0 3mm;padding-left:3mm;border-left:5px solid #b26bff;page-break-after:avoid}
h3{font:700 12.5pt 'DejaVu Sans',sans-serif;color:#6b3fb8;margin:6mm 0 2mm;page-break-after:avoid}
p{margin:0 0 3.5mm;text-align:left}
ul,ol{margin:0 0 4mm;padding-left:7mm}li{margin:1.2mm 0}
table{border-collapse:collapse;width:100%;margin:4mm 0 5mm;font:10pt/1.4 'DejaVu Sans',sans-serif;page-break-inside:avoid}
th{background:#4b2a8a;color:#fff;text-align:left;padding:2mm 3mm}td{border:1px solid #d8cbef;padding:2mm 3mm;vertical-align:top}
tr:nth-child(even) td{background:#f6f1ff}
code{font:10pt 'DejaVu Sans Mono',monospace;background:#f1ecfa;padding:0 1mm;border-radius:2px}
strong{color:#2c1a52}
h2:contains(Summary){}
"""
cover = '<div class="cover"><h1>Artificial Intelligence<br>A Condensed Tutorial</h1><div class="sub">Agents, search, logic, uncertainty, learning, language, vision, robotics and safety</div><div class="note">A study guide in original wording, organised after the chapters of <i>Artificial Intelligence: A Modern Approach</i> (Russell &amp; Norvig, 4th edition). It condenses ideas, not text: read the book for depth and exercises.</div></div>'
doc = "<!doctype html><meta charset=utf-8><style>%s</style>%s<div class='tocpage'><h1>Contents</h1><ol>%s</ol></div>%s" % (CSS, cover, tocH, "".join(body))
open("tutorial.html", "w", encoding="utf-8").write(doc)
foot = "<div style=\"font:8pt 'DejaVu Sans',sans-serif;color:#777;width:100%;padding:0 18mm;display:flex;justify-content:space-between\"><span>AI: A Condensed Tutorial</span><span>Page <span class='pageNumber'></span> of <span class='totalPages'></span></span></div>"
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(); pg.goto("file://" + os.path.abspath("tutorial.html")); pg.wait_for_timeout(500)
    pg.pdf(path=out, format="A4", print_background=True, display_header_footer=True, header_template="<span></span>", footer_template=foot, margin={"top": "22mm", "bottom": "20mm", "left": "18mm", "right": "18mm"}, prefer_css_page_size=False)
    b.close()
print("wrote", out)
