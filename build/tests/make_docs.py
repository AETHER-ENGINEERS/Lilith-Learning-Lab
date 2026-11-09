"""Creates sample documents in the given folder for the upload tests: notes.txt, .md, .html, .docx, .pptx, .pdf"""
import sys, os, zipfile
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
TXT = ("# Bees\n\nA honeybee colony has one queen, thousands of workers and a few hundred drones. The queen lays the eggs.\n\n"
       "## Honey\n\nWorkers turn nectar into honey by passing it between them and fanning it with their wings until the water evaporates.\n\n"
       "## The waggle dance\n\nA forager that finds flowers dances to tell the others the direction and the distance.\n")
open(out + "/notes.txt", "w").write(TXT); open(out + "/notes.md", "w").write(TXT)
open(out + "/notes.html", "w").write("<html><head><style>x{}</style></head><body><h1>Bees</h1><p>A honeybee colony has one queen, thousands of workers and a few hundred drones.</p><h2>Honey</h2><p>Workers turn nectar into honey by fanning it &amp; passing it around.</p></body></html>")
import docx
d = docx.Document(); d.add_heading("Bees", 1)
for p in TXT.split("\n\n")[1:]: d.add_paragraph(p.lstrip("# "))
d.save(out + "/notes.docx")
from pptx import Presentation
pr = Presentation()
for t, b in (("Bees", "One queen, many workers"), ("Honey", "Nectar becomes honey when the water evaporates")):
    s = pr.slides.add_slide(pr.slide_layouts[1]); s.shapes.title.text = t; s.placeholders[1].text = b
pr.save(out + "/deck.pptx")
from reportlab.pdfgen import canvas
c = canvas.Canvas(out + "/notes.pdf"); y = 800
for line in ("Bees", "A honeybee colony has one queen, thousands of workers and a few hundred drones.", "Workers turn nectar into honey by fanning it until the water evaporates.", "A forager tells the others the direction and distance of flowers with a waggle dance."):
    c.drawString(60, y, line); y -= 20
c.save(); print("ok")
