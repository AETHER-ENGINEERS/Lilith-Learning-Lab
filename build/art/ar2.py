# -*- coding: utf-8 -*-
"""Art theory course, part 2: composition, perspective, light, movements, practice."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=680):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Composition: arranging the picture",
 ("Composition", [
  "Frame | holds | The picture",
  "Rule of thirds | places | Subjects on lines",
  "Golden ratio | divides | By 1.618",
  "Leading lines | guide | The eye",
  "Negative space | gives | Room to breathe",
  "Format | sets | Shape of the canvas",
  "Focal point | sits | Off centre"]),
 ["Composition is how you place things inside the frame. A simple guide is the rule of thirds: divide the frame into a three by three grid, and place the subject on a line or where two lines meet.",
  "The golden ratio, about 1.618, is another old guide. Dividing a length in golden proportion puts the dividing point about 0.618 of the way along. Leading lines, framing and negative space help guide the eye.",
  "None of these are laws. They give a starting point and a reason, and good work often bends them."],
 [("Rule of thirds", "A guide that divides the frame into thirds in each direction, with the strongest points at the four intersections."),
  ("Golden ratio", "The proportion of about 1.618 to 1, also written phi."),
  ("Leading line", "A line in the picture that leads the eye toward the focal point."),
  ("Format", "The shape and orientation of the canvas, such as portrait, landscape or square."),
  ("Framing", "Using elements inside the picture to surround the subject.")],
 ["Thirds: lines at 1/3 and 2/3 across and down.",
  "Golden section: 0.618 of the length.",
  "Leading lines lead to the focal point.",
  "Centred = stable; off-centre = dynamic.",
  "Give a moving subject space to move into."],
 [T("Place a dot in the exact centre of a rectangle. It is stable, but also static and a little dull. Move it to one of the points one third across and one third down, and the picture wakes up. This is the rule of thirds, and cameras still show it as a grid."),
  T("To use the grid, put the horizon on the upper or lower line and not in the middle. Put the main subject on an intersection. In a portrait, the eyes often sit on the upper line. Give a person looking left a little more room on the left, called lead room, so the glance has somewhere to go."),
  T("The golden ratio comes from dividing a line so that the whole is to the longer part as the longer part is to the shorter. The number is about 1.618. The longer part is then 0.618 of the whole. Many artists use it as a slightly less rigid cousin of thirds. You can find it in spirals and in the Fibonacci numbers."),
  T("Lines carry the eye. A road, river, fence or row of trees can lead from the edge of the frame to the subject. Diagonals feel energetic and horizontals feel calm, while verticals feel strong. A frame within the frame, like an arch or window, adds depth and focus."),
  T("The shape of the canvas matters too. Landscape format suits wide scenes and calm. Portrait suits a standing figure and height. A square is neutral and centred. Crop a photo to different shapes and you will see how the mood changes, which is a quick way to practise.")],
 [("What does the rule of thirds divide?", ["The frame into a 3 x 3 grid", "The canvas into halves", "The colours into three", "The sketch into layers"], 0, "Two lines each way."),
  ("About what is the golden ratio?", ["1.618", "1.414", "2.718", "3.14"], 0, "Phi."),
  ("Where does a golden section fall along a length of 100?", ["About 61.8", "50", "33", "75"], 0, "0.618."),
  ("What do leading lines do?", ["Guide the eye to the subject", "Hide the subject", "Add colour", "Frame the paper"], 0, "Roads, rivers."),
  ("What is lead room?", ["Space in front of a moving or looking subject", "A studio", "The border", "A pencil grade"], 0, "Room to move into."),
  ("A centred subject feels...", ["Stable and static", "Chaotic", "Distant", "Unfinished"], 0, "Calm but plain.")],
 [("Thirds", "lines at 1/3 and 2/3"), ("Phi", "about 1.618"), ("Leading line", "guides the eye"), ("Lead room", "space the subject looks or moves into")],
 [APP("COMPOSE", "Composition grid", "Tap or drag on the canvas to place the subject. Switch between thirds and golden grids, and place the subject on 3 different strong points to complete this lab.", 680),
  MATCH("Match the guide", "Pair each composition guide with its idea.", [("Rule of thirds", "3 x 3 grid"), ("Golden ratio", "about 0.618 of the length"), ("Leading lines", "guide the eye"), ("Lead room", "space to look into")]),
  PL("Thirds points", "Write thirds_points(w, h): the four strong intersection points of the rule-of-thirds grid for a w by h canvas. Return them as [[x, y], ...] in the order top-left, top-right, bottom-left, bottom-right, with x = w/3 or 2w/3 and y = h/3 or 2h/3, each rounded to 1 decimal.", "thirds_points(w, h)", '''
def thirds_points(w, h):
    xs = [round(w / 3.0, 1), round(2 * w / 3.0, 1)]
    ys = [round(h / 3.0, 1), round(2 * h / 3.0, 1)]
    return [[xs[0], ys[0]], [xs[1], ys[0]], [xs[0], ys[1]], [xs[1], ys[1]]]
''', [[300, 300], [1920, 1080], [90, 60], [100, 100]], "Compute thirds along each side, then combine.", approx=0.1),
  PL("Golden section", "Write golden_split(length): the point that divides the length in the golden ratio, measured from the start: length x 0.6180339887, rounded to 2 decimals. Also return the other piece. Give [longer, shorter] as a list, with longer = round(length x 0.6180339887, 2) and shorter = round(length - longer, 2).", "golden_split(length)", '''
def golden_split(length):
    longer = round(length * 0.6180339887, 2)
    shorter = round(length - longer, 2)
    return [longer, shorter]
''', [[100], [1], [50], [1000], [8]], "The longer piece is 0.618 of the whole.", approx=0.01),
  PL("Which strong point?", "Write nearest_third(w, h, x, y): the index (0 to 3, in the same order top-left, top-right, bottom-left, bottom-right) of the thirds intersection nearest to the point (x, y). Break ties by the lower index.", "nearest_third(w, h, x, y)", '''
def nearest_third(w, h, x, y):
    pts = [[w / 3.0, h / 3.0], [2 * w / 3.0, h / 3.0], [w / 3.0, 2 * h / 3.0], [2 * w / 3.0, 2 * h / 3.0]]
    best = 0
    bestd = (pts[0][0] - x) ** 2 + (pts[0][1] - y) ** 2
    for i in range(1, 4):
        d = (pts[i][0] - x) ** 2 + (pts[i][1] - y) ** 2
        if d < bestd:
            bestd = d
            best = i
    return best
''', [[300, 300, 90, 90], [300, 300, 210, 100], [300, 300, 100, 210], [300, 300, 220, 220], [300, 300, 150, 150]], "Compare squared distances to all four points.")]
))

CHS.append(CH(
 "Perspective and space",
 ("Perspective", [
  "Horizon line | is | Eye level",
  "Vanishing point | gathers | Parallel lines",
  "One-point | has | One vanishing point",
  "Two-point | has | Two vanishing points",
  "Overlap | shows | Depth",
  "Atmospheric | fades | Distant objects",
  "Foreshortening | shrinks | Receding forms"]),
 ["Perspective is the art of showing three-dimensional space on a flat surface. The horizon line is your eye level. Parallel lines that go away from you seem to meet at a vanishing point on the horizon.",
  "One-point perspective has a single vanishing point, as when looking straight down a road. Two-point perspective shows a building corner, with two vanishing points.",
  "Without lines, depth also comes from overlap, size, position and atmospheric perspective, where far things become lighter, bluer and less sharp."],
 [("Horizon line", "The line at the viewer's eye level where sky and ground appear to meet."),
  ("Vanishing point", "A point on the horizon where parallel lines going away appear to meet."),
  ("One-point perspective", "A system with one vanishing point, used for views straight on."),
  ("Atmospheric perspective", "Distant objects look paler, bluer and softer because of the air."),
  ("Foreshortening", "The shortening of forms that point toward the viewer.")],
 ["Horizon = your eye level.",
  "Parallel lines meet at a vanishing point.",
  "One-point: straight-on. Two-point: corner view.",
  "Far objects: smaller, higher, lighter, bluer.",
  "Overlap shows what is in front."],
 [T("Stand on a straight railway track and look down it. The rails seem to come closer together and meet at a point far away. That point is the vanishing point, and it sits on the horizon, at the height of your eyes. If you crouch, the horizon drops with you."),
  T("In one-point perspective, a box seen from the front has one face flat to you and its side edges run to a single vanishing point. It suits corridors, roads and rooms. Vertical lines stay vertical and horizontal ones stay horizontal, except those going back in depth."),
  T("In two-point perspective, you look at a corner of a box. The vertical edge nearest you is tallest. The top and bottom edges on each side run to separate vanishing points on the horizon. This is the usual setting for buildings. Three-point perspective adds a third point above or below, for looking up at a tower."),
  T("Size shrinks with distance. An object twice as far away appears half the size. You can calculate it: project a point at depth z onto a picture plane at distance d by multiplying its x and y by d divided by z. This is how computer graphics draw 3D worlds."),
  T("Even without lines, painters hint at depth. Overlap shows what is in front. Objects higher on the page seem farther away when they stand on the ground. Atmospheric perspective makes far hills pale, blue and soft. Warm, sharp, dark details come forward. Combining these cues feels more natural than lines alone.")],
 [("Where is the horizon line?", ["At the viewer's eye level", "Always at the page bottom", "At the top of the sky", "Behind the subject"], 0, "It moves when you crouch."),
  ("What do parallel receding lines do in perspective?", ["Meet at a vanishing point", "Stay parallel", "Cross twice", "Curve away"], 0, "On the horizon."),
  ("How many vanishing points in one-point perspective?", ["1", "2", "3", "0"], 0, "Straight-on views."),
  ("What is atmospheric perspective?", ["Distant things look paler and bluer", "A kind of weather", "A grid", "A frame"], 0, "Air softens the far view."),
  ("An object twice as far looks...", ["Half as big", "Twice as big", "The same size", "Upside down"], 0, "Inverse with distance."),
  ("Which view is typical for a building corner?", ["Two-point perspective", "One-point perspective", "Flat view", "Isometric only"], 0, "Two vanishing points.")],
 [("Horizon", "eye level"), ("Vanishing point", "where parallels meet"), ("Two-point", "corner view"), ("Atmospheric", "far means pale and blue")],
 [MATCH("Match the depth cue", "Pair each cue with what it does.", [("Overlap", "shows what is in front"), ("Size", "smaller means farther"), ("Height on page", "higher means farther"), ("Atmospheric perspective", "pale and bluish means far"), ("Vanishing point", "parallels meet")]),
  PL("Project a point", "Write project(x, y, z, d): the perspective projection of a 3D point (x, y, z) onto a picture plane at distance d from the eye, with z the depth. Return [x x d / z, y x d / z] rounded to 2 decimals. Assume z is greater than 0.", "project(x, y, z, d)", '''
def project(x, y, z, d):
    return [round(x * d / z, 2), round(y * d / z, 2)]
''', [[2, 1, 4, 2], [1, 1, 1, 1], [3, 6, 6, 1], [-2, 4, 8, 4], [10, 5, 20, 2]], "Divide by the depth.", approx=0.01),
  PL("Apparent size", "Write apparent_size(size, distance, ref_distance): the apparent size of an object that has the given size when seen at ref_distance, if moved to distance. The size scales as ref_distance divided by distance. Return it rounded to 3 decimals.", "apparent_size(size, distance, ref_distance)", '''
def apparent_size(size, distance, ref_distance):
    return round(size * ref_distance / float(distance), 3)
''', [[10, 20, 10], [6, 3, 3], [1, 4, 1], [100, 50, 25]], "Twice as far means half the size.", approx=0.001),
  PL("Fade with distance", "Write haze(colour, sky, distance, max_distance): mix a colour [r, g, b] toward the sky colour as distance grows. t = min(distance / max_distance, 1). Return [round(c + (s - c) x t)] for each channel as ints.", "haze(colour, sky, distance, max_distance)", '''
def haze(colour, sky, distance, max_distance):
    t = distance / float(max_distance)
    if t > 1:
        t = 1.0
    out = []
    for i in range(3):
        out.append(int(round(colour[i] + (sky[i] - colour[i]) * t)))
    return out
''', [[[0, 100, 0], [180, 200, 255], 0, 100], [[0, 100, 0], [180, 200, 255], 50, 100], [[0, 100, 0], [180, 200, 255], 100, 100], [[0, 100, 0], [180, 200, 255], 300, 100]], "Reuse the mixing idea with a limit at 1.", approx=1)]
))

CHS.append(CH(
 "Light, shadow and value",
 ("Light and value", [
  "Light | makes | Form visible",
  "Highlight | is | Brightest area",
  "Core shadow | is | Darkest on the form",
  "Cast shadow | falls | On other surfaces",
  "Reflected light | softens | The shadow side",
  "Value scale | has | Steps",
  "Chiaroscuro | uses | Strong contrast"]),
 ["Light is what lets us see form. On a rounded object lit from one side, the surface goes from highlight through light and halftone to a core shadow, then a touch of reflected light at the edge, and finally a cast shadow on the ground.",
  "A value scale of five to nine steps from white to black helps judge values. Most strong drawings simplify the many values they see into three or four main groups.",
  "Chiaroscuro, light and dark contrast, was used by painters such as Caravaggio and Rembrandt to give drama and depth."],
 [("Highlight", "The brightest spot where light reflects most strongly."),
  ("Core shadow", "The darkest band on the form, away from the light source."),
  ("Cast shadow", "The shadow an object throws onto another surface."),
  ("Reflected light", "A faint light bounced back into the shadow side from nearby surfaces."),
  ("Chiaroscuro", "A strong use of light and dark to model form and create drama.")],
 ["Order on a sphere: highlight, light, halftone, core shadow, reflected light.",
  "Cast shadow is darkest near the object.",
  "Light direction decides every value.",
  "Simplify to 3 or 4 value groups.",
  "Squint to see the big pattern."],
 [T("Put an egg on a table and shine a lamp from the upper left. You will see a bright highlight, a broad light area, a gradual halftone, and then a darker band on the side away from the lamp. That darkest band is the core shadow, and it is not at the very edge."),
  T("Right at the edge, a bit of light bounces back from the table. This reflected light is weaker than the main light, so it never gets as bright as the lit side. Ignoring it makes forms look flat and cut out. Add it and the form turns round."),
  T("The egg also throws a cast shadow on the table. It is darkest and sharpest next to the egg, and softer farther away. The shape of the cast shadow tells you the direction of the light and the shape of the ground it falls on."),
  T("To judge values, use a value scale of squares from white to black. Hold a pencil up to compare. Beginners tend to use too few dark values, so everything looks pale. A good plan is to separate the picture into light, middle and dark groups, and give each its own sweep."),
  T("Rembrandt and Caravaggio pushed this to the extreme, with figures emerging from deep darkness into a pool of light. The technique is called chiaroscuro, Italian for light-dark. You can use it with a single lamp and a dark background for striking still lifes.")],
 [("What is the brightest spot on a shiny object?", ["The highlight", "The core shadow", "The cast shadow", "The halftone"], 0, "Direct reflection."),
  ("Where is the core shadow?", ["On the form, away from the light", "On the table", "At the highlight", "Nowhere"], 0, "Darkest band on the form."),
  ("What does reflected light do?", ["Softens the shadow side", "Removes the shadow", "Brightens the highlight", "Hides the form"], 0, "Light bounced from nearby surfaces."),
  ("What is chiaroscuro?", ["Strong light and dark contrast", "A soft pastel style", "A colour system", "A drawing tool"], 0, "Caravaggio."),
  ("Where is a cast shadow darkest?", ["Next to the object", "Far away", "On the highlight", "Everywhere equally"], 0, "Near the contact point."),
  ("What do beginners often do with values?", ["Use too few dark values", "Use too many", "Skip the white", "Draw only lines"], 0, "Everything looks pale.")],
 [("Highlight", "brightest spot"), ("Core shadow", "darkest band on the form"), ("Cast shadow", "shadow on another surface"), ("Chiaroscuro", "strong light and dark")],
 [ORDER("Light on a sphere", "Put the zones in order from the light source around the sphere.", ["Highlight", "Light", "Halftone", "Core shadow", "Reflected light"]),
  MATCH("Match the zone", "Pair each zone with its description.", [("Highlight", "brightest spot"), ("Halftone", "the turn from light to dark"), ("Core shadow", "darkest band on the form"), ("Reflected light", "faint bounce in the shadow"), ("Cast shadow", "falls on the table")]),
  PL("Lambert shading", "Write shade(nx, ny, lx, ly, ambient): the brightness of a surface point on a circle. (nx, ny) is the unit surface normal and (lx, ly) the unit direction toward the light. brightness = max(0, nx x lx + ny x ly), then add ambient and return min(1, brightness + ambient), rounded to 3 decimals.", "shade(nx, ny, lx, ly, ambient)", '''
def shade(nx, ny, lx, ly, ambient):
    b = nx * lx + ny * ly
    if b < 0:
        b = 0.0
    b = b + ambient
    if b > 1:
        b = 1.0
    return round(b, 3)
''', [[1, 0, 1, 0, 0.1], [0, 1, 1, 0, 0.1], [-1, 0, 1, 0, 0.1], [0.7071, 0.7071, 1, 0, 0.0], [1, 0, 1, 0, 0.5]], "Dot product of the normal and the light direction.", approx=0.002),
  PL("Quantise values", "Write posterize(values, levels): reduce a list of values 0 to 255 to the given number of levels, 2 or more. Each value maps to round(v / 255 x (levels - 1)) and then back to the grey round(index x 255 / (levels - 1)). Return the list of ints.", "posterize(values, levels)", '''
def posterize(values, levels):
    out = []
    for v in values:
        idx = int(round(v / 255.0 * (levels - 1)))
        out.append(int(round(idx * 255.0 / (levels - 1))))
    return out
''', [[[0, 60, 128, 200, 255], 3], [[10, 250], 2], [[0, 100, 200], 5], [[128], 4]], "Pick the nearest of the evenly spaced greys.")]
))

CHS.append(CH(
 "Art movements: a quick tour",
 ("Movements", [
  "Renaissance | studied | Perspective and anatomy",
  "Baroque | added | Drama and light",
  "Impressionism | caught | Fleeting light",
  "Cubism | broke | Single viewpoint",
  "Surrealism | explored | Dreams",
  "Abstract art | drops | Recognisable subjects",
  "Contemporary | mixes | Many media"]),
 ["Art movements are groups of artists who shared ideas in a time and place. Knowing the main ones shows how the elements and principles have been used differently.",
  "The Renaissance perfected perspective and anatomy. The Baroque added drama with light. Impressionism painted fleeting light and colour. Cubism showed objects from many viewpoints, and abstract art dropped the subject altogether.",
  "A timeline is a map. Place each artist or movement on it, and you start to see how one idea led to the next."],
 [("Renaissance", "A period from the 14th to 16th century that revived classical ideas and developed linear perspective."),
  ("Baroque", "A 17th-century style of drama, movement and strong light and dark."),
  ("Impressionism", "A 19th-century movement that painted light and colour with quick visible brushstrokes."),
  ("Cubism", "An early 20th-century movement that showed subjects from several viewpoints at once."),
  ("Abstract art", "Art that does not try to show the visible world.")],
 ["Renaissance: perspective, proportion, realism.",
  "Baroque: drama, movement, chiaroscuro.",
  "Impressionism: light, colour, outdoors.",
  "Cubism: many viewpoints, flattened space.",
  "Abstract: form and colour for their own sake."],
 [T("In fifteenth-century Italy artists rediscovered the classical world and developed the geometry of perspective. Figures got real weight, and rooms got real depth. Leonardo, Raphael and Michelangelo are the names most people know. The goal was to show the world as it looks, and as it ideally could be."),
  T("The Baroque that followed turned up the drama. Figures twist, light cuts through darkness, and everything seems about to move. Caravaggio, Rembrandt and Rubens used chiaroscuro and diagonal compositions to put the viewer in the middle of the action."),
  T("In the nineteenth century Impressionists such as Monet and Renoir took their easels outdoors. They painted the changing light, with quick brushstrokes and bright colours placed side by side. A picture became a record of an instant, rather than a polished scene."),
  T("In the early twentieth century, Picasso and Braque broke objects into planes seen from several sides, which is Cubism. Others went further. Kandinsky and Mondrian made art from colour, line and shape alone. Surrealists like Dali mixed dream images with precise painting."),
  T("Today art uses nearly every medium: photography, video, installation, digital tools. The elements and principles remain. A good way to learn them is to copy a small study from each movement, to feel the choices that artist made, and then make your own.")],
 [("What did Renaissance artists develop?", ["Linear perspective", "Cubism", "Digital art", "Pointillism"], 0, "A geometry of depth."),
  ("What marks Baroque art?", ["Drama and strong light and dark", "Flat colours", "No subject", "Tiny dots"], 0, "Caravaggio."),
  ("What did the Impressionists paint?", ["Fleeting light and colour", "Dreams", "Only portraits", "Only gods"], 0, "Monet."),
  ("What does Cubism show?", ["Several viewpoints at once", "One view only", "Only landscapes", "Only light"], 0, "Picasso and Braque."),
  ("Who made art from pure line and colour?", ["Mondrian", "Raphael", "Rembrandt", "Monet"], 0, "Abstract art."),
  ("Which movement mixes dream images with precise painting?", ["Surrealism", "Baroque", "Renaissance", "Realism"], 0, "Dali.")],
 [("Renaissance", "perspective and anatomy"), ("Baroque", "drama and chiaroscuro"), ("Impressionism", "light and colour"), ("Cubism", "many viewpoints"), ("Surrealism", "dreams")],
 [MATCH("Match the movement", "Pair each movement with its idea.", [("Renaissance", "perspective and realism"), ("Baroque", "drama and chiaroscuro"), ("Impressionism", "fleeting light"), ("Cubism", "many viewpoints"), ("Surrealism", "dream images")]),
  ORDER("Put the movements in time order", "Order them from earliest to latest.", ["Renaissance", "Baroque", "Impressionism", "Cubism", "Surrealism"]),
  PL("Movement for a year", "Write movement(year): return the movement that best matches the year: 'Renaissance' for 1400 to 1599, 'Baroque' for 1600 to 1749, 'Impressionism' for 1860 to 1889, 'Cubism' for 1907 to 1919, 'Surrealism' for 1924 to 1950, otherwise 'other'.", "movement(year)", '''
def movement(year):
    if 1400 <= year <= 1599:
        return "Renaissance"
    if 1600 <= year <= 1749:
        return "Baroque"
    if 1860 <= year <= 1889:
        return "Impressionism"
    if 1907 <= year <= 1919:
        return "Cubism"
    if 1924 <= year <= 1950:
        return "Surrealism"
    return "other"
''', [[1500], [1650], [1874], [1912], [1930], [1800], [2000], [1599]], "Check each range in turn.")]
))

CHS.append(CH(
 "Critique and a practice routine",
 ("Practice", [
  "Observation | comes | First",
  "Study | isolates | One skill",
  "Thumbnail | tests | Compositions",
  "Reference | informs | Drawing",
  "Critique | improves | Next work",
  "Routine | builds | Habit",
  "Sketchbook | records | Progress"]),
 ["Skill grows by looking carefully and making many small studies. A daily routine of ten to twenty minutes beats an occasional long session.",
  "Before a large piece, make several small thumbnail sketches to try different compositions quickly. Use reference, and then change it to make it your own.",
  "Finish by looking at your own work as a critic. Describe, analyse, interpret, judge, and then pick one thing to try next."],
 [("Thumbnail", "A tiny quick sketch used to test a composition."),
  ("Study", "A small focused exercise on one problem, such as value or colour."),
  ("Reference", "A photo or object you draw from."),
  ("Master copy", "A copy of a work by an artist you admire, done to learn their choices."),
  ("Sketchbook", "A book where you practise and record ideas.")],
 ["Ten minutes a day beats once a month.",
  "Thumbnails first, big piece after.",
  "One skill per study.",
  "Copy to learn, then create.",
  "Keep dated work to see progress."],
 [T("Most art skills come from seeing better, not from talent. A short daily routine trains the eye. Draw a household object in ten minutes with a pencil. Next day, the same object with only three values. The day after, in a limited palette. Small repeated tries beat rare big ones."),
  T("Before you start a big piece, make thumbnails. Draw six small rectangles and sketch the idea in each with a different composition: the subject on the left, on the right, high, low, close, far. Pick the best. This costs five minutes and saves hours."),
  T("Study one thing at a time. A value study ignores colour. A colour study ignores detail. A perspective study uses a simple box. Isolating a skill makes it easier to see progress. Combine skills only when each one feels comfortable."),
  T("Copy to learn. A master copy of a small part of a painting you admire shows you the choices behind it: why the dark goes there, how the edge is soft. Do it for practice, label it as a study, and then make an original piece that uses what you learned."),
  T("Review your work every month. Lay out the pages side by side and use the four-step critique. What improved? What keeps going wrong? Pick one thing to focus on next. Over a year, you will have a record of your progress, and a clearer sense of your own style.")],
 [("What is a thumbnail?", ["A tiny sketch to test composition", "A finished painting", "A frame", "A brush"], 0, "Quick and small."),
  ("Why isolate one skill in a study?", ["To see progress", "To avoid drawing", "To save paper", "To use more colours"], 0, "Focus."),
  ("What is a master copy for?", ["Learning another artist's choices", "Selling", "Avoiding practice", "Making a forgery"], 0, "Study."),
  ("How often should you practise?", ["A little each day", "Once a year", "Only in school", "Never"], 0, "Habit beats bursts."),
  ("What do you do in a monthly review?", ["Critique and pick a focus", "Throw things away", "Buy new paint", "Stop drawing"], 0, "Four steps."),
  ("What is reference?", ["A photo or object you draw from", "A signature", "A brush brand", "A frame"], 0, "Looking helps.")],
 [("Thumbnail", "small test sketch"), ("Study", "one skill at a time"), ("Master copy", "copy to learn"), ("Review", "critique monthly")],
 [MATCH("Match the practice", "Pair each exercise with its purpose.", [("Thumbnails", "test compositions"), ("Value study", "judge light and dark"), ("Master copy", "learn another artist's choices"), ("Monthly review", "track progress")]),
  ORDER("A study session", "Put the steps in order.", ["Pick one skill", "Make thumbnails", "Draw the study", "Critique it", "Choose the next focus"]),
  PL("Weekly plan", "Write plan(days, minutes): a list of 'days' items where item i (starting at 1) reads 'Day ' + str(i) + ': ' + str(minutes) + ' min'. Return the list.", "plan(days, minutes)", '''
def plan(days, minutes):
    out = []
    for i in range(1, days + 1):
        out.append("Day " + str(i) + ": " + str(minutes) + " min")
    return out
''', [[3, 10], [1, 20], [0, 15], [5, 5]], "Build the strings in a loop."),
  PL("Total practice", "Write total_minutes(sessions): sessions is a list of [days, minutes_per_day] pairs. Return the total minutes practised.", "total_minutes(sessions)", '''
def total_minutes(sessions):
    t = 0
    for s in sessions:
        t = t + s[0] * s[1]
    return t
''', [[[[7, 10], [3, 20]]], [[]], [[[30, 15]]], [[[1, 60], [2, 30]]]], "Multiply days by minutes and add.")]
))
