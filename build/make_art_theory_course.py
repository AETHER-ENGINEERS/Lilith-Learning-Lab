#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Art Theory course. Usage: python3 make_art_theory_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "art"))
import cmk, ar1, ar2, make_apps  # noqa: E402
make_apps.main()
CHS = ar1.CHS + ar2.CHS
PRONOUNCE = {"chiaroscuro": "kee ah ro skoor oh", "Caravaggio": "kah rah vah joh", "Rembrandt": "rem brant", "Monet": "moh nay", "Renoir": "ren wahr", "Picasso": "pih kah soh", "Braque": "brack",
    "Kandinsky": "kan din skee", "Mondrian": "mon dree an", "Dali": "dah lee", "Rubens": "roo benz", "Raphael": "raf ay el", "Michelangelo": "my kel an jel oh", "Leonardo": "lee oh nar doh",
    "Baroque": "buh roke", "Impressionism": "im presh un izm", "Cubism": "kyoo bizm", "Surrealism": "sur ee al izm", "hue": "hyoo", "tint": "tint", "saturation": "sat you ray shun",
    "analogous": "uh nal uh gus", "triadic": "try ad ik", "foreshortening": "for short en ing", "halftone": "half tone", "CMYK": "C M Y K", "RGB": "R G B", "phi": "fie", "Fibonacci": "fib uh nah chee"}
SANDBOX = cmk.terminal("Art cheat sheet", "art>", "A scripted lookup. Try: elements, principles, color, thirds, golden, perspective", [
    ("elements", ["Line, shape, form, space, value, texture, colour."]),
    ("principles", ["Balance, contrast, emphasis, movement, rhythm, proportion, unity."]),
    ("color", ["Tint = hue + white. Shade = hue + black. Tone = hue + grey. Complement = hue + 180 degrees."]),
    ("thirds", ["Grid lines at 1/3 and 2/3; place the subject on an intersection."]),
    ("golden", ["Golden section: 0.618 of the length. Ratio about 1.618."]),
    ("perspective", ["Horizon = eye level. Parallel lines meet at vanishing points on the horizon."]),
])
EXAM = [
 ("What are the elements of art?", ["Basic building blocks of an image", "Ways to arrange a picture", "Paint brands", "Art periods"], 0, "Line, shape, form and more."),
 ("What are the principles of design?", ["Ways to organise the elements", "Types of paint", "Names of artists", "Frame styles"], 0, "Balance, contrast and so on."),
 ("What comes first in a critique?", ["Describe", "Judge", "Look up the price", "Copy"], 0, "Describe before you judge."),
 ("What is the difference between shape and form?", ["Form has depth", "Shape has colour", "Form is flat", "None"], 0, "2D versus 3D."),
 ("What is negative space?", ["The area around the subject", "A dark colour", "A mistake", "A frame"], 0, "Not the subject."),
 ("What is hue?", ["The pure colour name", "How light a colour is", "How vivid", "The brand"], 0, "Red, blue and so on."),
 ("Adding white to a hue makes a...", ["Tint", "Shade", "Tone", "Primary"], 0, "Lighter."),
 ("What are screen primaries?", ["Red, green, blue", "Red, yellow, blue", "Cyan, magenta, yellow", "Black, white, grey"], 0, "Light mixing."),
 ("How far apart are complementary hues?", ["180 degrees", "30 degrees", "120 degrees", "90 degrees"], 0, "Opposite."),
 ("Analogous colours are...", ["Neighbours on the wheel", "Opposites", "Evenly spaced thirds", "The same hue"], 0, "Within about 30 degrees."),
 ("The 60-30-10 rule gives...", ["Dominant, secondary, accent", "Three brushes", "A frame size", "A pencil grade"], 0, "Proportions."),
 ("What is a focal point?", ["The place that grabs attention first", "The frame", "The signature", "The background"], 0, "The lead."),
 ("What does rhythm do?", ["Creates a beat by repeating elements", "Hides the subject", "Removes colour", "Adds frames"], 0, "Fence posts."),
 ("What does the rule of thirds divide?", ["The frame into a 3 x 3 grid", "The canvas in halves", "Colours in three", "Layers"], 0, "Two lines each way."),
 ("About what is the golden ratio?", ["1.618", "1.414", "2.718", "3.14"], 0, "Phi."),
 ("What is lead room?", ["Space in front of a looking or moving subject", "A studio", "The border", "A pencil"], 0, "Room to look into."),
 ("Where is the horizon line?", ["At the viewer's eye level", "At the page bottom", "At the top of the sky", "Behind the subject"], 0, "It moves when you crouch."),
 ("Parallel receding lines meet at...", ["A vanishing point", "The page edge", "Nowhere", "The viewer"], 0, "On the horizon."),
 ("What is atmospheric perspective?", ["Distant things look paler and bluer", "Weather", "A grid", "A frame"], 0, "Air softens."),
 ("An object twice as far looks...", ["Half as big", "Twice as big", "The same", "Upside down"], 0, "Inverse with distance."),
 ("Where is the core shadow?", ["On the form, away from the light", "On the table", "At the highlight", "Nowhere"], 0, "Darkest band."),
 ("What is chiaroscuro?", ["Strong light and dark contrast", "A soft pastel style", "A colour system", "A tool"], 0, "Caravaggio."),
 ("What did Renaissance artists develop?", ["Linear perspective", "Cubism", "Digital art", "Pointillism"], 0, "A geometry of depth."),
 ("What did the Impressionists paint?", ["Fleeting light and colour", "Dreams", "Only portraits", "Only gods"], 0, "Monet."),
 ("What does Cubism show?", ["Several viewpoints at once", "One view", "Only light", "Only landscapes"], 0, "Picasso and Braque."),
 ("What is a thumbnail?", ["A tiny sketch to test composition", "A finished painting", "A frame", "A brush"], 0, "Quick and small."),
]
CFG = dict(id="art-theory", title="Art Theory",
    subtitle="Elements, colour, composition, perspective, light and a tour of movements, with Python labs and two interactive tools",
    description="A beginner-friendly course in art theory: the elements of art and principles of design, colour basics and harmonies, composition with the rule of thirds and the golden ratio, perspective and depth, light and shadow, and a quick tour of art movements from the Renaissance to the present. Python labs turn colour, composition and perspective into numbers, and two interactive tools let you pick colour harmonies and try composition grids.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="art", apps={"__HARMONY__": "harmony.html", "__COMPOSE__": "compose.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "art-theory.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
