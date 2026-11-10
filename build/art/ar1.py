# -*- coding: utf-8 -*-
"""Art theory course, part 1: seeing, elements, colour, harmony, principles."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=680):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Learning to see: what art theory is for",
 ("Art theory", [
  "Art theory | gives | Vocabulary",
  "Elements | are | Building blocks",
  "Principles | are | Ways to arrange",
  "Composition | arranges | The picture",
  "Critique | describes | Then judges",
  "Practice | trains | The eye",
  "Style | reflects | Choices"]),
 ["Art theory gives names to what you see and a way to talk about why a picture works. It does not tell you what to make, but it gives you tools to choose with.",
  "Most theory splits into elements, the building blocks (line, shape, form, space, value, texture, colour), and principles, the ways to arrange them (balance, contrast, emphasis, rhythm, unity).",
  "The best way to learn is to look closely, name what you see, and try small studies."],
 [("Element of art", "A basic ingredient of an image, such as line, shape, form, space, value, texture or colour."),
  ("Principle of design", "A way of organising elements, such as balance, contrast, emphasis, movement, rhythm and unity."),
  ("Composition", "The arrangement of elements within the picture."),
  ("Critique", "A structured look at a work: describe, analyse, interpret, judge."),
  ("Study", "A small practice drawing or painting made to learn one thing.")],
 ["Elements are the ingredients; principles are the recipe.",
  "Describe before you judge.",
  "Compare works to see choices.",
  "Small studies beat big plans.",
  "Rules are tools, not laws."],
 [T("When you look at a painting you like, you may only feel that it works. Theory lets you say why. Is it the strong diagonal, the single red coat in a grey crowd, or the way the dark corner holds your eye? Naming these helps you do them yourself."),
  T("Artists have used the same toolbox for centuries. The elements are what is on the canvas: lines, shapes, forms, spaces, values, textures and colours. The principles are what the artist does with them: balance, contrast, emphasis, movement, rhythm, pattern and unity."),
  T("A good habit is the four-step critique. Describe what you see without judging. Analyse how the elements are used. Interpret what the work seems to mean or feel like. Then judge it, with reasons. Most people start with the last step, but the first one is where learning happens."),
  T("Rules like the rule of thirds are guides that work most of the time. Great artists break them on purpose, and the result works because they knew what they broke. Learn the rule, try it, then see what happens when you do the opposite."),
  T("This course mixes ideas with small calculations. Python labs turn colour and composition into numbers, so you can see how a warm tone is built or where the golden section falls. Two interactive tools let you pick colour harmonies and try composition grids on your own canvas.")],
 [("What are the elements of art?", ["The basic building blocks of an image", "The ways to arrange a picture", "A list of paint brands", "Art history periods"], 0, "Line, shape, colour and others."),
  ("What are the principles of design?", ["Ways to organise the elements", "Types of paint", "Names of artists", "Frame styles"], 0, "Balance, contrast, rhythm."),
  ("What comes first in a critique?", ["Describe what you see", "Judge the work", "Look up the price", "Copy it"], 0, "Describe before you judge."),
  ("Are composition rules laws?", ["No, they are guides", "Yes, always", "Only for photos", "Only for sculpture"], 0, "Break them on purpose."),
  ("What is a study?", ["A small practice piece", "A large finished mural", "A museum", "A frame"], 0, "Practice for one skill."),
  ("What is composition?", ["The arrangement of elements", "A kind of paint", "A colour", "A tool"], 0, "How the parts fit together.")],
 [("Elements", "line, shape, form, space, value, texture, colour"), ("Principles", "balance, contrast, emphasis, movement, rhythm, unity"), ("Critique", "describe, analyse, interpret, judge"), ("Composition", "the arrangement of the picture")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Element", "a building block"), ("Principle", "a way to arrange"), ("Composition", "the arrangement"), ("Critique", "a structured look at a work")]),
  ORDER("The four-step critique", "Put the steps in order.", ["Describe what you see", "Analyse how elements are used", "Interpret the meaning or mood", "Judge with reasons"]),
  FILL("Seeing", "The {{elements}} are the ingredients and the {{principles}} are how you arrange them.")]
))

CHS.append(CH(
 "The elements of art",
 ("Elements", [
  "Line | leads | The eye",
  "Shape | is | Flat and enclosed",
  "Form | is | Three-dimensional",
  "Space | holds | Positive and negative",
  "Value | is | Light to dark",
  "Texture | is | Surface quality",
  "Colour | has | Hue value saturation"]),
 ["Line is a mark between two points; it can be straight, curved, thick, thin, actual or implied. Shape is a flat area enclosed by a line or a colour change. Form is a shape with depth.",
  "Space is the area around and inside things, both positive (the subject) and negative (the empty area). Value is how light or dark something is. Texture is the feel of a surface, real or drawn.",
  "Colour is the seventh element and has its own chapters. Each element can be used in a drawing to build mood and meaning."],
 [("Line", "A mark that connects points; it can show edge, movement or direction."),
  ("Shape", "A flat, enclosed area, geometric or organic."),
  ("Form", "A three-dimensional shape with height, width and depth."),
  ("Negative space", "The empty area around and between subjects."),
  ("Value", "The lightness or darkness of a colour or tone.")],
 ["Line: straight, curved, thick, thin, implied.",
  "Shape is 2D; form is 3D.",
  "Negative space shapes the subject.",
  "Value: white to black in steps.",
  "Texture can be real or implied."],
 [T("Draw a line with a pencil and you have already made choices. A straight line feels calm, a zigzag nervous, a curve gentle. A thick line is bold and a thin one delicate. Lines can lead the eye across the page, or hint at a shape that is not drawn, called an implied line."),
  T("Close a line into a loop and you get a shape. Geometric shapes like circles and squares feel man-made and orderly. Organic shapes like leaves and clouds feel natural and free. Shading a shape so it seems to have thickness turns it into a form, like a sphere from a circle."),
  T("Space includes the room around objects. The subject takes the positive space and the leftover is the negative space. Look at the shape of the empty space between a chair's legs, and it is easier to draw the chair right. Overlap, size and position create the feeling of depth."),
  T("Value is the range from light to dark. A drawing in only pencil can look fully 3D just from value. Squint at a picture, and the details melt into a few big value shapes. If the value structure works, the picture works, whatever the colour."),
  T("Texture is how a surface feels or seems to feel: rough, smooth, soft, hard. Real texture is thick paint or paper grain. Implied texture is drawn marks that make you imagine touching fur or stone. Contrasting textures next to each other, like silk and rock, make a picture feel alive.")],
 [("What is the difference between shape and form?", ["Form has depth", "Shape has colour", "Form is flat", "There is none"], 0, "2D vs 3D."),
  ("What is negative space?", ["The area around the subject", "A dark colour", "A mistake", "A frame"], 0, "Not the subject itself."),
  ("What is value?", ["How light or dark something is", "How warm a colour is", "The price", "The size"], 0, "White to black."),
  ("What is an implied line?", ["A line the eye connects without drawing it", "A thick line", "A broken pencil", "A border"], 0, "Not drawn but felt."),
  ("What does a squint test show?", ["The main value shapes", "The colour names", "The brush size", "The artist"], 0, "Details melt."),
  ("Real texture is...", ["Actual surface feel", "Only drawn", "A colour", "A shape"], 0, "Thick paint or paper grain.")],
 [("Line", "mark between two points"), ("Shape", "flat enclosed area"), ("Form", "shape with depth"), ("Value", "light to dark"), ("Negative space", "area around the subject")],
 [MATCH("Match the element", "Pair each element with its description.", [("Line", "connects points"), ("Shape", "flat enclosed area"), ("Form", "has depth"), ("Value", "light to dark"), ("Texture", "surface quality")]),
  PL("Value steps", "Write value_scale(n): a list of n evenly spaced grey values from 0 (black) to 255 (white), n at least 2. Each value is round(255 x i / (n - 1)) for i from 0 to n - 1.", "value_scale(n)", '''
def value_scale(n):
    out = []
    for i in range(n):
        out.append(int(round(255.0 * i / (n - 1))))
    return out
''', [[2], [5], [9], [3]], "Divide 255 into n minus 1 equal steps."),
  PL("Negative space ratio", "Write negative_ratio(canvas_w, canvas_h, shapes): shapes is a list of [w, h] rectangles that do not overlap. Return the fraction of the canvas not covered, rounded to 3 decimals.", "negative_ratio(canvas_w, canvas_h, shapes)", '''
def negative_ratio(canvas_w, canvas_h, shapes):
    area = canvas_w * canvas_h
    used = 0
    for s in shapes:
        used = used + s[0] * s[1]
    return round((area - used) / float(area), 3)
''', [[100, 100, [[50, 50]]], [10, 20, []], [100, 50, [[10, 10], [20, 20]]], [8, 8, [[8, 8]]]], "Subtract the used area from the canvas area.", approx=0.001)]
))

CHS.append(CH(
 "Colour basics",
 ("Colour", [
  "Hue | names | The colour",
  "Saturation | is | Intensity",
  "Value | is | Lightness",
  "Primary | mix | Others",
  "Warm | advances | Cool recedes",
  "RGB | is | Light mixing",
  "CMYK | is | Ink mixing"]),
 ["Every colour has three properties: hue (which colour it is), saturation (how vivid) and value (how light). Changing one gives a tint, shade or tone of the same hue.",
  "The traditional primaries are red, yellow and blue. Mixing two gives a secondary (orange, green, violet), and mixing a primary with a neighbouring secondary gives a tertiary. Screens use red, green and blue light; printers use cyan, magenta, yellow and black ink.",
  "Warm colours (reds, oranges, yellows) seem to come forward, and cool colours (blues, greens) seem to recede."],
 [("Hue", "The pure colour name, such as red or blue."),
  ("Saturation", "How vivid or grey a colour is."),
  ("Tint, shade, tone", "A hue mixed with white, black or grey."),
  ("Primary colours", "Colours that cannot be mixed from others; traditionally red, yellow, blue."),
  ("Complementary colours", "Colours opposite each other on the wheel.")],
 ["Hue, saturation, value.",
  "Tint = + white. Shade = + black. Tone = + grey.",
  "Primaries: RYB (paint), RGB (light), CMY (ink).",
  "Warm advances; cool recedes.",
  "Opposites on the wheel are complementary."],
 [T("Take a tube of red paint. Its hue is red. Add white and it gets lighter, a tint, like pink. Add black and it gets darker, a shade, like maroon. Add grey and it gets duller, a tone. The hue never changed, only its value or saturation."),
  T("Painters learn three primaries, red, yellow and blue, that mix to give the other hues. Red and yellow give orange. Yellow and blue give green. Blue and red give violet. Put these on a circle and you have a colour wheel with twelve steps."),
  T("The wheel has a warm half and a cool half. Warm colours feel like sun and fire, and they seem to step toward the viewer. Cool colours feel like water and shade, and they seem to step back. Painters use this to build depth: warm in front, cool in the distance."),
  T("Screens work differently. They mix light, not paint. Red, green and blue light added together make white. Each colour is written as three numbers from 0 to 255, such as 255, 0, 0 for pure red. A web colour like FF8800 is the same three numbers in hexadecimal."),
  T("Printers subtract light instead. Cyan, magenta and yellow inks soak up parts of white light, and black ink adds depth. This is CMYK. Colours that look fine on screen can look duller in print, because ink cannot reach every colour that light can.")],
 [("What is hue?", ["The pure colour name", "How light a colour is", "How vivid it is", "The paint brand"], 0, "Red, blue, and so on."),
  ("What does adding white to a hue make?", ["A tint", "A shade", "A tone", "A primary"], 0, "Lighter."),
  ("Which colours seem to come forward?", ["Warm colours", "Cool colours", "Grey colours", "None"], 0, "Reds and oranges."),
  ("What are the screen primaries?", ["Red, green, blue", "Red, yellow, blue", "Cyan, magenta, yellow", "Black, white, grey"], 0, "Light mixing."),
  ("What is FF0000 in hex?", ["Pure red", "Pure green", "Pure blue", "White"], 0, "255, 0, 0."),
  ("What are complementary colours?", ["Opposites on the wheel", "Neighbours on the wheel", "Same hue", "Black and white"], 0, "Red and green, blue and orange.")],
 [("Tint", "hue + white"), ("Shade", "hue + black"), ("Tone", "hue + grey"), ("RGB", "light, additive"), ("CMYK", "ink, subtractive")],
 [MATCH("Match the term", "Pair each colour term with its meaning.", [("Tint", "hue plus white"), ("Shade", "hue plus black"), ("Saturation", "how vivid"), ("Complement", "opposite on the wheel")]),
  PL("Hex to RGB", "Write hex_to_rgb(h): h is a string like '#FF8800' or 'FF8800'. Return the list [r, g, b] with each value 0 to 255. Use int(text, 16).", "hex_to_rgb(h)", '''
def hex_to_rgb(h):
    if h[0] == "#":
        h = h[1:]
    return [int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)]
''', [["#FF8800"], ["00ff00"], ["#000000"], ["#336699"], ["FFFFFF"]], "Cut the string into three pairs of hex digits."),
  PL("RGB to hex", "Write rgb_to_hex(r, g, b): return the colour as an uppercase string starting with '#', two hex digits per channel, for example '#FF8800'.", "rgb_to_hex(r, g, b)", '''
def rgb_to_hex(r, g, b):
    digits = "0123456789ABCDEF"
    out = "#"
    for v in [r, g, b]:
        out = out + digits[v // 16] + digits[v % 16]
    return out
''', [[255, 136, 0], [0, 0, 0], [255, 255, 255], [51, 102, 153], [10, 20, 30]], "Split each value into two hex digits."),
  PL("Tint and shade", "Write mix_with(rgb, other, amount): mix a colour with another (white [255,255,255] for a tint, black [0,0,0] for a shade). Return [round(c + (o - c) x amount) for each channel], amount from 0 to 1, as ints.", "mix_with(rgb, other, amount)", '''
def mix_with(rgb, other, amount):
    out = []
    for i in range(3):
        out.append(int(round(rgb[i] + (other[i] - rgb[i]) * amount)))
    return out
''', [[[255, 0, 0], [255, 255, 255], 0.5], [[255, 0, 0], [0, 0, 0], 0.5], [[100, 150, 200], [255, 255, 255], 0.0], [[100, 150, 200], [0, 0, 0], 1.0], [[0, 128, 255], [255, 255, 255], 0.25]], "Move each channel part of the way to the other colour.", approx=1)]
))

CHS.append(CH(
 "Colour harmony and palettes",
 ("Harmony", [
  "Colour wheel | arranges | Hues",
  "Complementary | pairs | Opposites",
  "Analogous | uses | Neighbours",
  "Triadic | uses | Three evenly spaced",
  "Palette | limits | Colours",
  "Contrast | needs | Value difference",
  "60-30-10 | guides | Proportion"]),
 ["Colour harmonies are ways of picking colours that sit well together, found by distances on the colour wheel. Complementary uses opposites, analogous uses neighbours, triadic uses three evenly spaced, and split-complementary uses one hue and the two next to its opposite.",
  "A palette is a limited set of colours for one work. Limiting the palette gives unity.",
  "Contrast matters too: colours with similar values read poorly together, even if the hues contrast."],
 [("Complementary harmony", "Two hues opposite each other on the colour wheel."),
  ("Analogous harmony", "Hues that sit next to each other on the wheel."),
  ("Triadic harmony", "Three hues evenly spaced around the wheel, 120 degrees apart."),
  ("Palette", "The set of colours chosen for a work."),
  ("Contrast ratio", "A number comparing the lightness of two colours; higher means easier to read.")],
 ["Complementary: hue + 180 degrees.",
  "Analogous: hue +/- 30 degrees.",
  "Triadic: hue + 120 and + 240.",
  "60-30-10: dominant, secondary, accent.",
  "Value contrast matters more than hue contrast for legibility."],
 [T("Imagine the colour wheel as a clock face with 360 degrees. Red is at 0, yellow near 60, green at 120, cyan at 180, blue at 240 and magenta at 300. Any harmony is just a pattern of angles on this wheel."),
  T("Complementary colours are 180 degrees apart, like red and cyan or blue and orange. Side by side they make each other look brighter, which is great for accents. Mixed together they cancel to grey. Analogous colours are neighbours, within about 30 degrees, and they make a calm, unified look, like a sunset of reds, oranges and yellows."),
  T("Triadic harmony picks three colours 120 degrees apart, like red, green and blue. It is lively and balanced, often used in children's art. Split-complementary takes a hue and the two colours on either side of its complement. It has contrast, but is less harsh than a pure complement."),
  T("A palette works best when it is limited. A common recipe is 60-30-10: sixty percent a dominant colour, thirty percent a secondary and ten percent an accent. The accent is the pop. Many posters, rooms and websites follow this pattern without saying so."),
  T("Do not forget value. Two bright colours of the same value, like red and green at the same lightness, seem to vibrate and are hard to read together. Convert a picture to grey to test it. If shapes vanish, the values are too close. Design tools measure it with a contrast ratio, and good body text needs a ratio of at least 4.5 to 1.")],
 [("How far apart are complementary hues?", ["180 degrees", "30 degrees", "120 degrees", "90 degrees"], 0, "Opposite."),
  ("Which harmony uses neighbouring hues?", ["Analogous", "Complementary", "Triadic", "Split"], 0, "Within about 30 degrees."),
  ("How far apart are triadic hues?", ["120 degrees", "180 degrees", "60 degrees", "90 degrees"], 0, "Three evenly spaced."),
  ("What is the 60-30-10 rule?", ["Dominant, secondary, accent", "Three paints", "A frame ratio", "A brush size"], 0, "Proportions."),
  ("Why convert a picture to grey?", ["To check value contrast", "To change hue", "To print", "To add texture"], 0, "Shapes should still read."),
  ("What do complementary colours do side by side?", ["Make each other brighter", "Turn grey", "Vanish", "Become identical"], 0, "Strong contrast.")],
 [("Complementary", "hue + 180"), ("Analogous", "hue +/- 30"), ("Triadic", "hue + 120, + 240"), ("60-30-10", "dominant, secondary, accent")],
 [APP("HARMONY", "Colour harmony picker", "Pick a base hue and a harmony. The swatches show the hues and their hex codes. Try 4 different harmonies to complete this lab.", 640),
  MATCH("Match the harmony", "Pair each harmony with its rule.", [("Complementary", "opposite, 180 degrees"), ("Analogous", "neighbours, about 30 degrees"), ("Triadic", "three at 120 degrees"), ("Split-complementary", "base plus two beside its opposite")]),
  PL("Harmony hues", "Write harmony(hue, kind): hue is in degrees 0 to 359. Return the list of hues (each 0 to 359, base first): 'complementary' is [h, h + 180], 'analogous' is [h - 30, h, h + 30], 'triadic' is [h, h + 120, h + 240], 'split' is [h, h + 150, h + 210]. Take every value modulo 360.", "harmony(hue, kind)", '''
def harmony(hue, kind):
    if kind == "complementary":
        offs = [0, 180]
    elif kind == "analogous":
        offs = [-30, 0, 30]
    elif kind == "triadic":
        offs = [0, 120, 240]
    else:
        offs = [0, 150, 210]
    return [(hue + o) % 360 for o in offs]
''', [[0, "complementary"], [20, "analogous"], [210, "triadic"], [330, "split"], [0, "analogous"], [120, "triadic"]], "List the offsets, then add them and wrap at 360."),
  PL("Contrast ratio", "Write contrast(a, b) for two colours as [r, g, b] lists of 0 to 255. Convert each channel c to c/255; if it is at most 0.03928 divide by 12.92, otherwise compute ((c + 0.055) / 1.055) ** 2.4. Luminance L = 0.2126 R + 0.7152 G + 0.0722 B. The ratio is (Lhigh + 0.05) / (Llow + 0.05). Return it rounded to 2 decimals.", "contrast(a, b)", '''
def contrast(a, b):
    def lum(c):
        vals = []
        for v in c:
            x = v / 255.0
            if x <= 0.03928:
                vals.append(x / 12.92)
            else:
                vals.append(((x + 0.055) / 1.055) ** 2.4)
        return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]
    la = lum(a)
    lb = lum(b)
    if la < lb:
        la, lb = lb, la
    return round((la + 0.05) / (lb + 0.05), 2)
''', [[[0, 0, 0], [255, 255, 255]], [[255, 255, 255], [255, 255, 255]], [[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]], [[119, 119, 119], [255, 255, 255]]], "Compute the luminance of each colour, then divide.", approx=0.02)]
))

CHS.append(CH(
 "Principles of design",
 ("Principles", [
  "Balance | spreads | Visual weight",
  "Contrast | creates | Interest",
  "Emphasis | picks | A focal point",
  "Movement | guides | The eye",
  "Rhythm | repeats | Elements",
  "Proportion | relates | Sizes",
  "Unity | holds | It together"]),
 ["The principles of design are ways of organising the elements. Balance spreads visual weight. Contrast sets differences against each other. Emphasis creates a focal point. Movement leads the eye. Rhythm and pattern repeat things. Proportion relates sizes. Unity makes it all feel like one piece.",
  "Balance can be symmetrical (mirror-like), asymmetrical (different things of equal weight) or radial (around a centre).",
  "Good design balances unity with variety: enough sameness to feel whole, enough difference to stay interesting."],
 [("Balance", "An even distribution of visual weight across the picture."),
  ("Focal point", "The place that grabs attention first."),
  ("Rhythm", "A visual beat made by repeating elements."),
  ("Proportion", "The size relationship between parts and the whole."),
  ("Unity and variety", "The tension between sameness that holds a work together and differences that keep it interesting.")],
 ["Balance: symmetrical, asymmetrical, radial.",
  "Emphasis: one thing should lead.",
  "Movement follows lines, edges and gaze.",
  "Rhythm: regular, random, flowing, progressive.",
  "Unity with variety."],
 [T("Picture a seesaw. A big weight near the middle balances a small weight far out. Pictures work like this. A large pale shape can balance a small dark one, because the dark one pulls harder. Symmetrical balance mirrors both sides, and asymmetrical balance uses different elements of equal pull."),
  T("Contrast is difference: light against dark, big against small, smooth against rough, warm against cool. High contrast draws attention, and low contrast calms. A single bright patch in a muted scene becomes the focal point without anything else being said."),
  T("Emphasis decides what you see first. Artists make a focal point by contrast, isolation or size. Everything else supports it. If everything shouts, nothing is heard. In a portrait, the face often has the sharpest detail and strongest value contrast."),
  T("Movement is how the eye travels. Lines, edges, a pointing arm or a gaze lead the viewer through the picture. Rhythm repeats elements to create a beat: regular like fence posts, flowing like waves, progressive like shapes growing larger. Pattern is rhythm laid across a surface."),
  T("Proportion relates sizes, such as head to body, or a figure to its landscape. Unity ties it together by repeating colour, shape or style. Variety keeps it from being dull. The best work has both: a limited palette and a few changes of scale. Test any picture by asking: what leads, what supports, and what could go.")],
 [("What does balance spread?", ["Visual weight", "Paint", "Light", "Sound"], 0, "Weight, not mass."),
  ("What is a focal point?", ["The place that grabs attention first", "The frame", "The signature", "The background"], 0, "The lead."),
  ("What is symmetrical balance?", ["Mirrored sides", "Random placement", "One heavy side", "No balance"], 0, "Like a face."),
  ("What does rhythm do?", ["Creates a beat by repetition", "Hides the subject", "Removes colour", "Adds depth only"], 0, "Fence posts."),
  ("How do artists make emphasis?", ["Contrast, isolation or size", "Using more colours", "Making it smaller and duller", "Adding frames"], 0, "Make one thing stand out."),
  ("What does unity need alongside it?", ["Variety", "More frames", "A signature", "Larger paper"], 0, "Sameness plus difference.")],
 [("Balance", "even visual weight"), ("Emphasis", "a clear focal point"), ("Rhythm", "repetition makes a beat"), ("Unity", "the work feels like one piece")],
 [MATCH("Match the principle", "Pair each principle with its effect.", [("Balance", "even visual weight"), ("Contrast", "draws attention by difference"), ("Emphasis", "sets a focal point"), ("Rhythm", "repeats elements"), ("Unity", "holds the work together")]),
  PL("Visual balance", "Write balance(items): items is a list of [weight, x] pairs where x is the distance from the centre of the picture (negative left, positive right). Return the net torque, the sum of weight x x, as a number. Zero means balanced.", "balance(items)", '''
def balance(items):
    total = 0
    for it in items:
        total = total + it[0] * it[1]
    return total
''', [[[[5, -2], [5, 2]]], [[[10, 1], [2, -5]]], [[[3, 3], [1, -1]]], [[]]], "Multiply each weight by its distance and add."),
  PL("Rhythm", "Write rhythm(sizes): sizes is a list of element sizes in a row. Return 'regular' if all are equal, 'progressive' if they strictly increase or strictly decrease, otherwise 'varied'. A list with one item is 'regular'.", "rhythm(sizes)", '''
def rhythm(sizes):
    same = True
    up = True
    down = True
    for i in range(1, len(sizes)):
        if sizes[i] != sizes[i - 1]:
            same = False
        if sizes[i] <= sizes[i - 1]:
            up = False
        if sizes[i] >= sizes[i - 1]:
            down = False
    if same:
        return "regular"
    if up or down:
        return "progressive"
    return "varied"
''', [[[3, 3, 3]], [[1, 2, 4, 8]], [[8, 4, 2]], [[2, 5, 3]], [[7]]], "Track whether the list is all equal, always rising or always falling.")]
))
