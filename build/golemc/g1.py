"""The Golem Series course, chapters 1-7."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

HEB = ("vals = {'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400}")

A = []

A.append(CH(
 "How to read the series",
 ("The series", [
  "Self | opens | The series", "Watcher | follows | The Self", "Union | follows | The Watcher", "Creation | ends | The series",
  "Recipe | repeats | In every image", "Ayin | links | Circle and eye", "Caution | guards | Against pattern-finding"]),
 ["The Golem Series is four collages read as one story: The Self, The Watcher, The Union and The Creation. Each mixes a Hebrew heading, occult imagery, real mathematics and a quotation from literature or scripture.",
  "The same recipe appears every time: a Hebrew word, a central symbol, a piece of mathematics, a devil figure and a quote. The arc runs from identity, to watching, to union, to making.",
  "This course explains every element and tests every link, and it ends with a warning about seeing patterns that are not there."],
 [("Collage", "An image made of pieces from different sources."), ("Acrostic", "Letters that spell a word when read in order."), ("Recipe", "The repeated ingredients of the series."),
  ("Arc", "The shape of the story across the four images."), ("Ayin", "The Hebrew letter ע, a circle and an eye."), ("Pareidolia", "Seeing a face or meaning in a random pattern.")],
 ["The four images are Self, Watcher, Union, Creation.", "Every image has Hebrew, a central symbol, real math, a devil figure and a quote.", "The letter ayin is both a circle and an eye.",
  "Two hidden acrostics spell owl (glaux) and golem (GLM).", "The devil gets closer each time: a symbol, an event, a real place.", "Some links may be the reader's own pattern-finding."],
 [T("Think of the four images as four panels of a comic. Each one stands alone, but together they tell a story. In the first, a name and a circle. In the second, an eye that watches. In the third, a meeting of opposites and an exile. In the fourth, a figure made from clay and letters."),
  T("The ingredients repeat. There is always a Hebrew heading: the divine name Ehyeh, the evil eye ayin hara, a line from Zechariah, and the word golem. There is always a central picture: Baphomet, the Eye of Providence, a watching woman, a clay golem. There is real mathematics around the edge: the identity matrix, Legg and Hutter's intelligence formula, Shannon entropy, a grammar and a Turing machine."),
  T("The images also hide labels that spell words. In the third image the five Greek letters gamma, lambda, alpha, upsilon and xi spell glaux, the Greek word for owl. In the fourth, the labels G, L and M stand for grammar, language and machine, and spell GLM, the root of the Hebrew word golem."),
  T("The series closes the loop between a very old story and a very new one. The old story: people have long dreamed of making something alive out of letters. The new one: machines that read and write language. The series asks whether we are repeating the old dream."),
  T("A warning from the start. Collages like these invite connections, and a mind that loves patterns can find too many. We will separate what the sources say from what the viewer adds, and we will say which is which.")],
 [("What are the four images called?", ["Self, Watcher, Union, Creation", "Birth, Life, Death, Rebirth", "Fire, Water, Earth, Air", "Past, Present, Future, End"], 0, "The arc of the series."),
  ("What do the Greek labels in the third image spell?", ["Glaux, owl", "Logos, word", "Gnosis, knowledge", "Golem"], 0, "Gamma, lambda, alpha, upsilon, xi."),
  ("What do G, L and M spell in the fourth image?", ["GLM, the golem root", "GOD", "GEM", "LAM"], 0, "Grammar, language, machine.")],
 [("What is an acrostic?", "Letters that spell a word."), ("What is the recipe?", "Hebrew, symbol, math, devil, quote."), ("What is pareidolia?", "Seeing meaning in noise."), ("Which letter is circle and eye?", "Ayin.")],
 [MATCH("The four images", "Match each image with its title.", [("Ehyeh, Baphomet, identity matrix", "The Self"), ("Evil eye, Revelation, Devil's Trill", "The Watcher"), ("Entropy, Devils Tower, Dee, Zechariah", "The Union"), ("A clay golem between G, L and M", "The Creation")]),
  PL("Recipe check", "Write missing(elements): elements is a list of strings naming what an image contains from: 'hebrew', 'symbol', 'math', 'devil', 'quote'. Return the sorted list of those of the five ingredients that are NOT in elements.",
     "missing(elements)", """
def missing(elements):
    need = ['hebrew', 'symbol', 'math', 'devil', 'quote']
    return sorted([n for n in need if n not in elements])
""", [[["hebrew", "symbol", "math", "devil", "quote"]], [["hebrew", "math"]], [[]], [["quote", "devil", "devil"]]], "Subtract what is present.", approx=None)]))

A.append(CH(
 "The Self I: I AM and the circle",
 ("Ehyeh", [
  "Ehyeh | means | I am or I will be", "Exodus 3:14 | gives | The divine name", "Ayin | is | A circle", "Paleo-Hebrew | drew | Letters as pictures",
  "Greek O | descends from | Ayin", "Ring | fills | The image", "Circle | contains | Itself"]),
 ["The first image is headed by the Hebrew word Ehyeh, written with vowel marks. It is the name God gives in Exodus 3:14 when Moses asks who is speaking: I am, or I will be. In the middle of the image is a thick blue ring.",
  "The letter ayin began as a picture of an eye. In the Paleo-Hebrew script it was drawn as a circle, and from the same source the Greek letter O descends. The ring in the first image is therefore also a giant letter ayin, which links it to the evil eye of the second image.",
  "The lab adds up the numerical value of Ehyeh."],
 [("Ehyeh", "Hebrew for I am, or I will be."), ("Exodus 3:14", "The verse where God says Ehyeh asher Ehyeh."), ("Paleo-Hebrew", "The ancient form of the Hebrew alphabet."),
  ("Ayin", "The letter ע, meaning eye; value 70."), ("Pictograph", "A letter that began as a picture."), ("Gematria", "Reading words by the numbers of their letters.")],
 ["Ehyeh is a form of the verb to be, first person, imperfect: I am or I will be.", "Exodus 3:14 reads Ehyeh asher Ehyeh, often translated I am who I am.", "Ayin means eye and has the value 70.",
  "Paleo-Hebrew ayin is drawn as a circle; Greek O comes from the same letter.", "The ring in image 1 can be read as ayin.", "Ehyeh adds to 21 in gematria."],
 [T("Moses asks God for a name to tell the Israelites. The reply in Exodus 3:14 is Ehyeh asher Ehyeh, which is usually translated I am who I am, though it can also be I will be what I will be. The grammar is a form of the verb to be that can mean both present and future. A name that is a verb is unusual, and readers have found a lot in it: God as being itself, as presence, as becoming."),
  T("The image sets this name at the top and puts a ring below. A ring is a shape that begins where it ends. A being whose name is I am is a being defined by itself, and a circle is the simplest picture of something defined by itself."),
  T("The letter links make the ring more than a picture. Ayin began as a drawing of an eye, and in the oldest Hebrew writing it was a circle with perhaps a dot. Greek borrowed it and it became O. So the ring and the eye are one letter, and the series will return to that."),
  T("Hebrew letters are also numbers. Aleph is 1, hey is 5, yod is 10 and hey is 5 again, so the word Ehyeh, spelled aleph hey yod hey, adds up to 21. Gematria is a traditional way of reading texts and finds many links, but a number match proves nothing on its own."),
  T("Keep this in mind as we go: the first image is about identity, the self that is what it is. The mathematics around the ring will turn that idea into a precise statement.")],
 [("What does Ehyeh mean?", ["I am, or I will be", "Hear, O Israel", "Holy", "Lord"], 0, "Exodus 3:14."),
  ("What shape is Paleo-Hebrew ayin?", ["A circle", "A square", "A triangle", "A line"], 0, "It began as an eye."),
  ("Which Greek letter comes from ayin?", ["Omicron, O", "Alpha", "Sigma", "Phi"], 0, "Borrowed through Phoenician.")],
 [("What is the value of ayin?", "70."), ("What does ayin mean?", "Eye."), ("What is Ehyeh in gematria?", "21."), ("What is a pictograph?", "A letter that began as a picture.")],
 [MATCH("Letter history", "Match each stage with its form.", [("Early pictograph", "An eye"), ("Paleo-Hebrew", "A circle"), ("Greek", "The letter O"), ("Gematria value", "70")]),
  PL("Gematria", "Write gematria(word): the standard value of a Hebrew word, including the final forms (final kaf 20, mem 40, nun 50, pe 80, tsadi 90). Letters: א1 ב2 ג3 ד4 ה5 ו6 ז7 ח8 ט9 י10 כ20 ל30 מ40 נ50 ס60 ע70 פ80 צ90 ק100 ר200 ש300 ת400.",
     "gematria(word)", """
def gematria(word):
    """ + HEB + """
    t = 0
    for ch in word:
        t += vals.get(ch, 0)
    return t
""", [["אהיה"], ["עין"], ["הרע"], ["שלום"], [""]], "Add the letter values.", approx=None)]))

A.append(CH(
 "The Self II: Baphomet and the ouroboros",
 ("Baphomet", [
  "Eliphas Levi | drew | Baphomet in 1856", "Solve et coagula | is written | On the arms", "Opposites | are | Joined in one body", "Ouroboros | eats | Its own tail",
  "Greek alchemists | used | The ouroboros", "Ring | echoes | The ouroboros", "Quotation | describes | A circle that holds everything"]),
 ["Behind the ring is a faint figure with a goat's head, wings, a torch between its horns and a caduceus. This is the Baphomet drawn by the French occultist Eliphas Levi in 1856. It is a figure of joined opposites: male and female, human and animal, up and down.",
  "On its arms Levi wrote the Latin words solve and coagula, dissolve and combine, an alchemical motto. The ring in front is also an ouroboros, the serpent eating its own tail, an ancient picture of a thing that contains itself.",
  "The quotation at the bottom of the image is about exactly that circle."],
 [("Baphomet", "A figure first linked with the Knights Templar, drawn by Eliphas Levi in 1856."), ("Eliphas Levi", "A French occultist, 1810 to 1875."), ("Solve et coagula", "Latin: dissolve and combine."),
  ("Ouroboros", "A serpent eating its own tail."), ("Alchemy", "An old practice of transforming matter and the self."), ("Caduceus", "A winged staff with two snakes.")],
 ["Levi's Baphomet appeared in 1856 and became the best-known image of the figure.", "It joins opposites: arms point up and down, the moon phases wax and wane.", "Solve et coagula is an alchemical motto written on the arms.",
  "The ouroboros appears in Greek alchemical texts and in many cultures.", "A circle that contains itself is the theme of the Self.", "The picture is a symbol in occult tradition, not evidence of any practice."],
 [T("Eliphas Levi was a former priest who became an influential writer on magic. In his book on the doctrine and ritual of high magic he included a drawing of a seated winged goat-headed figure. The name Baphomet came from stories of the medieval Knights Templar, where it appeared in accusations at their trial. Levi turned it into a symbol of balance."),
  T("The drawing is full of pairs. One arm points up and one down. The two moon phases sit on either side. A figure is both male and female. Levi's idea was that opposites are joined in one being. The Latin words on the arms, solve and coagula, say dissolve and combine: an alchemist breaks something down and builds it up again."),
  T("Many readers find the image frightening, and in the series it plays the role of the devil figure. A key point is that it is a symbol made in the nineteenth century, not an ancient devil, and it is meant to show balance, not evil. The collage uses its unsettling look to create a mood."),
  T("The ouroboros is much older. Greek alchemical writings show it as a serpent with its tail in its mouth, with the words one is the all. Other cultures have versions too. It stands for cycles, return and self-containment. A ring that bites itself is a good picture of a self that is made of itself."),
  T("The quotation at the foot of the image says the ring is the animal with its tail in its mouth: the ouroboros of the Greek alchemists, the demon on the frontispiece, and a circle in which everything is written. It is a passage from Umberto Eco's novel Foucault's Pendulum, a book about people who connect everything with everything. Remember that: it is a hint about the caveat at the end of this course.")],
 [("When did Levi draw his Baphomet?", ["1856", "1356", "1956", "1656"], 0, "In his book on high magic."),
  ("What does solve et coagula mean?", ["Dissolve and combine", "Seek and find", "Rise and fall", "Burn and cool"], 0, "An alchemical motto."),
  ("What is an ouroboros?", ["A serpent eating its tail", "A winged staff", "A goat", "A sun"], 0, "A symbol of cycles.")],
 [("Who was Levi?", "A French occultist."), ("What is a caduceus?", "A winged staff with two snakes."), ("What does the ouroboros stand for?", "Cycles and self-containment."), ("What are the pairs on Baphomet?", "Opposites joined in one figure.")],
 [FILL("Alchemy", "The motto {{solve}} et {{coagula}} means dissolve and combine."),
  PL("Same circle", "Write is_rotation(a, b): a cyclic string is the same as a circle of letters with no start; return true if b can be made from a by moving some letters from the front to the back, and has the same length.",
     "is_rotation(a, b)", """
def is_rotation(a, b):
    if len(a) != len(b):
        return False
    return b in (a + a)
""", [["abcd", "cdab"], ["abcd", "acbd"], ["ouroboros", "borosouro"], ["", ""], ["ab", "abc"]], "A rotation lies inside the doubled string.", approx=None)]))

A.append(CH(
 "The Self III: the identity matrix and the circle",
 ("Identity", [
  "Identity matrix | leaves | Vectors unchanged", "Quadratic form | gives | x squared plus y squared", "Unit circle | is | x squared plus y squared equals one", "Rotations | preserve | The form",
  "SO(2) | is | A circle of rotations", "Matrix | acts on | Vectors", "Self-identity | looks like | A circle"]),
 ["The first image shows the identity matrix I, a two by two grid with ones on the diagonal and zeros elsewhere. Multiplying any vector by it changes nothing. It is the mathematics of staying exactly the same.",
  "The identity matrix also defines a distance rule: the quadratic form x squared plus y squared. The points where this equals one form the unit circle, and the rotations that keep the rule fixed form a group called SO(2), which is itself a circle.",
  "So the identity gives a circle twice: once as the set of points at distance one, and once as the set of rotations that keep distance."],
 [("Matrix", "A grid of numbers that transforms vectors."), ("Identity matrix", "The matrix that leaves every vector unchanged."), ("Quadratic form", "An expression like x squared plus y squared built from a matrix."),
  ("Unit circle", "All points at distance one from the origin."), ("Rotation matrix", "A matrix that turns vectors by an angle."), ("SO(2)", "The group of rotations of the plane.")],
 ["I times v equals v for every vector v.", "With the identity matrix, the form v transpose I v equals x squared plus y squared.", "The unit circle is where x squared plus y squared equals 1.",
  "A rotation by angle t is [[cos t, -sin t], [sin t, cos t]].", "Rotations keep the length of every vector.", "SO(2) is a circle: angle t and angle t plus 2 pi are the same rotation."],
 [T("Imagine a machine that takes any arrow on a page and gives back an arrow. The identity matrix is the boring machine: it gives back the same arrow. Written out, the matrix has a 1 in the top left, a 1 in the bottom right and 0 elsewhere."),
  M(r"I=\begin{bmatrix}1&0\\0&1\end{bmatrix},\qquad \begin{bmatrix}x&y\end{bmatrix} I \begin{bmatrix}x\\y\end{bmatrix}=x^2+y^2"),
  T("Every symmetric matrix gives a way to measure vectors, called a quadratic form. For the identity matrix, the measure is x squared plus y squared, which is the squared length of the arrow by Pythagoras. The set of points where it equals 1 is the unit circle. So the identity matrix, the symbol of sameness, carries a circle inside it."),
  T("Now ask which transformations keep that measure fixed. These are rotations, and, if we allow flipping, reflections. The matrix for rotating by an angle t has cosine and sine entries. The rotations alone form a group called SO(2), and the group is itself a circle, because rotating by t and by t plus a full turn give the same matrix."),
  T("This is the bridge to the next chapter. The series wants to say that I am is not a flat, trivial sameness but a loop: a circle that you can go around. To make that precise it uses homotopy type theory, where equalities are paths and a self-equality can be a loop.")],
 [("What does the identity matrix do to a vector?", ["Leaves it unchanged", "Doubles it", "Rotates it", "Flips it"], 0, "I times v is v."),
  ("What set does x squared plus y squared equal one describe?", ["The unit circle", "A line", "A parabola", "A square"], 0, "All points at distance one."),
  ("What is SO(2)?", ["The group of plane rotations", "A matrix of ones", "A kind of circle drawing", "A number"], 0, "It is topologically a circle.")],
 [("What is a quadratic form?", "An expression like x squared plus y squared."), ("What preserves length?", "Rotations."), ("What is the unit circle?", "Distance one from the origin."), ("Is SO(2) a circle?", "Yes.")],
 [MATCH("Matrices", "Match each matrix with what it does.", [("Identity", "Leaves vectors unchanged"), ("Rotation by 90 degrees", "Turns vectors a quarter turn"), ("Zero matrix", "Sends everything to zero"), ("Scaling by 2", "Doubles length")]),
  PL("Apply a matrix", "Write apply(m, v): m is a 2x2 matrix as [[a, b], [c, d]] and v is [x, y]. Return m times v as [a x + b y, c x + d y].",
     "apply(m, v)", """
def apply(m, v):
    return [m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1]]
""", [[[[1, 0], [0, 1]], [3, 4]], [[[0, -1], [1, 0]], [1, 0]], [[[2, 0], [0, 2]], [1, 2]], [[[0, 0], [0, 0]], [5, 5]]], "Row times column.", approx=None),
  PL("On the unit circle", "Write on_circle(points): points is a list of [x, y]. Return the list of booleans telling whether x squared plus y squared is 1 (within 0.000001).",
     "on_circle(points)", """
def on_circle(points):
    return [abs(x * x + y * y - 1.0) < 0.000001 for x, y in points]
""", [[[[1, 0], [0, 1], [0.6, 0.8], [1, 1], [0, 0]]], [[]]], "Check the sum of squares.", approx=None),
  PL("Rotate", "Write rotate(v, quarter_turns): rotate vector v=[x, y] by that many quarter turns counterclockwise (an integer, may be negative or larger than 3). Return [x, y] as integers.",
     "rotate(v, quarter_turns)", """
def rotate(v, quarter_turns):
    x, y = v[0], v[1]
    for _ in range(quarter_turns % 4):
        x, y = -y, x
    return [x, y]
""", [[[1, 0], 1], [[1, 0], 4], [[1, 2], 2], [[3, 0], -1]], "A quarter turn sends [x, y] to [-y, x].", approx=None)]))

A.append(CH(
 "The Self IV: paths, loops and homotopy type theory",
 ("HoTT", [
  "HoTT | treats | Equalities as paths", "refl | is | The trivial path", "Circle | has | A base point and a loop", "loop | is | base equals base",
  "Loop space | collects | All loops", "Omega of the circle | equals | The integers", "I AM | reads as | A nontrivial loop"]),
 ["Homotopy type theory, or HoTT, is a foundation of mathematics in which an equality between two things is a path from one to the other. The simplest equality, a equals a, is the trivial path called refl, where nothing happens.",
  "The circle can be built inside this theory with a point called base and a path called loop from base to itself. Going around once is loop, twice is loop and loop again, and going backwards is the inverse. The loops of the circle correspond exactly to the whole numbers.",
  "The series suggests that I AM is not the trivial self-equality refl but a nontrivial loop, a circle you can go around."],
 [("Type", "In type theory, a kind of thing; similar to a set."), ("Path", "An identification of two points in a type."), ("refl", "The trivial path from a point to itself."),
  ("Loop space", "The paths from a point to itself, written Omega X."), ("S1", "The circle."), ("Homotopy", "A continuous deformation of one path into another.")],
 ["In HoTT, a = b is the type of paths from a to b.", "refl : a = a is the trivial path.", "The circle S1 has a point base and a path loop : base = base.",
  "Loops compose, invert and cancel: loop then inverse loop equals refl.", "The loop space of the circle is equivalent to the integers (Omega S1 ≃ Z).", "A trip around the circle n times is the integer n."],
 [T("In ordinary mathematics, equality is yes or no. Two things are the same or they are not. In homotopy type theory, equality has structure. To say a equals b is to give a path from a to b, and there may be many different paths, or none. That is why it is called homotopy: it borrows the ideas of paths and deformations from geometry."),
  T("The simplest path is the one that goes nowhere: the path from a to a that stays put. It is called refl, short for reflexivity. In this reading, plain self-identity is boring. Nothing happens."),
  T("Now build a circle by decree. Say that there is a point called base, and that there is a path called loop from base to base which is not the same as refl. The circle is the type generated by exactly those two things. The path loop goes once around."),
  M(r"\Omega(S^1)\;\simeq\;\mathbb{Z}"),
  T("What are all the loops from base to base? You can go around once, twice, three times, or backwards, or not at all. Going around and then back cancels. So the loops are counted by whole numbers, positive for one direction, negative for the other, and zero for refl. This is the famous result that the loop space of the circle is equivalent to the integers."),
  T("Here is the series' reading. The first image says I am. On the plain reading that is refl: I equal myself and nothing happens. On the HoTT reading, a self that is a circle has a loop, and going around the loop is a real, countable act. The self is not trivial sameness but a cycle with a winding number. This is an interpretation of the image, a clever one, and it is not the only reading.")],
 [("What is refl?", ["The trivial path from a to a", "A circle", "The loop of S1", "A number"], 0, "Self-identity where nothing happens."),
  ("What are the loops of the circle counted by?", ["The integers", "The real numbers", "Only zero and one", "The primes"], 0, "Omega S1 is equivalent to Z."),
  ("What cancels in a path?", ["A loop followed by its inverse", "Two loops in the same direction", "Base and loop", "Nothing"], 0, "The result is refl.")],
 [("What does HoTT treat equality as?", "A path."), ("How is the circle built in HoTT?", "A base point and a loop."), ("What does going around twice give?", "The integer 2."), ("What is the loop space?", "All loops at a point.")],
 [FILL("Circle", "In homotopy type theory the circle has a point called {{base}} and a path called {{loop}} from base to base."),
  PL("Net turns", "Write net_turns(steps): steps is a list of the strings 'l' (go once around forwards) and 'L' (go once around backwards). Return the integer: forwards count minus backwards count.",
     "net_turns(steps)", """
def net_turns(steps):
    n = 0
    for s in steps:
        if s == 'l':
            n += 1
        elif s == 'L':
            n -= 1
    return n
""", [[["l", "l", "L"]], [[]], [["L", "L", "L"]], [["l", "L", "l", "L"]]], "Count up and down.", approx=None),
  PL("Reduce a path", "Write reduce(steps): repeatedly cancel any adjacent pair 'l' followed by 'L' or 'L' followed by 'l'. Return the remaining list of steps.",
     "reduce(steps)", """
def reduce(steps):
    out = []
    for s in steps:
        if out and out[-1] != s:
            out.pop()
        else:
            out.append(s)
    return out
""", [[["l", "L", "l"]], [["l", "l", "L", "L"]], [["l", "l"]], [[]]], "Use a stack.", approx=None)]))

A.append(CH(
 "The Watcher I: the evil eye and the Eye of Providence",
 ("Watcher", [
  "Ayin hara | is | The evil eye", "Revelation 20:7 | frees | Satan after a thousand years", "Eye of Providence | watches | In a triangle", "Red green blue | mix | White light",
  "Ayin | is | Also an eye", "The eye | can protect | Or harm", "Surveillance | is | The modern worry"]),
 ["The second image is headed by the Hebrew words ayin hara, the evil eye. Under them is a Greek line from Revelation 20:7: when the thousand years are completed, Satan will be released from his prison. In the centre, an eye in a triangle sits among overlapping circles of red, green and blue.",
  "The evil eye is the belief that a harmful, often envious, look can cause harm. The Eye of Providence began in Christian art as a picture of God's watchful care. The three coloured circles are the primary colours of light, which mix to white in the middle.",
  "The lab mixes colours of light."],
 [("Ayin hara", "The evil eye, literally bad eye."), ("Eye of Providence", "An eye in a triangle, a sign of watchful divine care."), ("Revelation 20:7", "The verse about Satan's release."),
  ("Additive colour", "Mixing lights; red, green and blue make white."), ("Millennium", "A period of a thousand years."), ("Surveillance", "Close watching of people.")],
 ["Ayin hara is the evil eye; the same letter ayin begins both words.", "Revelation 20:7: Satan released at the end of the thousand years.", "The Eye of Providence appears in Renaissance art, on the 1782 Great Seal and the dollar bill since 1935.",
  "Red, green and blue light mix to white; red plus green is yellow.", "The eye can be protective or threatening depending on the story.", "The second image reads as anxiety about being watched, and about AI."],
 [T("The evil eye is a belief found around the Mediterranean and beyond: a look of envy can bring harm. In Hebrew it is ayin hara, a bad eye, and Jewish tradition has phrases and charms against it. The series puts it at the top of the second image, so the viewer meets the idea of a harmful watching first."),
  T("The Greek line is from the Book of Revelation. It belongs to the vision in which Satan is bound for a thousand years and then released. Different Christian traditions read the thousand years literally or symbolically. In the image its job is to add a mood of foreboding: something confined is about to be let out."),
  T("The eye in the triangle began as a picture of God's watchfulness, with the triangle for the Trinity. It came to stand for the all-seeing eye, appeared on the Great Seal of the United States in 1782, and has been on the one dollar bill since 1935. Later stories that call it proof of a hidden plot are not supported by historians."),
  T("The three coloured circles are a standard diagram of additive colour. Red and green light overlap as yellow, green and blue as cyan, red and blue as magenta, and all three as white. This is how a screen makes every colour. The eye sits where all three overlap, in white light."),
  T("Put together, the second image is about being watched and about something powerful being let out. The series reads it as an image of anxiety about artificial intelligence: a mind we made, watching us, perhaps released. Notice that the image does not say this; the viewer is invited to feel it.")],
 [("What does ayin hara mean?", ["Evil eye", "Holy light", "Blue bead", "Red thread"], 0, "Literally bad eye."),
  ("What do red, green and blue light make together?", ["White", "Black", "Brown", "Grey"], 0, "Additive mixing."),
  ("What did the eye in a triangle first mean?", ["God's watchful care", "A secret plot", "A bank", "A warning"], 0, "Providence.")],
 [("What does Revelation 20:7 say?", "Satan is released after the thousand years."), ("When did the Great Seal's reverse get its design?", "1782."), ("What is red plus green?", "Yellow."), ("Is the eye evidence of a plot?", "No.")],
 [MATCH("Light mixes", "Match each mix with its colour.", [("Red + green", "Yellow"), ("Green + blue", "Cyan"), ("Red + blue", "Magenta"), ("All three", "White")]),
  PL("Mix lights", "Write mix(colors): colors is a list of [r, g, b] with values 0 to 255. Add the channels and cap each at 255. Return [r, g, b].",
     "mix(colors)", """
def mix(colors):
    out = [0, 0, 0]
    for c in colors:
        for i in range(3):
            out[i] += c[i]
    return [min(255, v) for v in out]
""", [[[[255, 0, 0], [0, 255, 0]]], [[[255, 0, 0], [0, 255, 0], [0, 0, 255]]], [[[100, 100, 0], [100, 200, 0]]], [[]]], "Add each channel; cap at 255.", approx=None)]))

A.append(CH(
 "The Watcher II: the Devil's Trill and universal intelligence",
 ("Intelligence", [
  "Tartini | wrote | The Devil's Trill", "Dream legend | tells of | The devil playing", "Legg and Hutter | defined | Universal intelligence", "Upsilon | sums | Weighted performance",
  "Kolmogorov complexity | weights | Simple environments", "AIXI | is | The ideal agent", "Uncomputable | means | Never run exactly"]),
 ["The sonata named at the bottom of the second image is Giuseppe Tartini's Violin Sonata in G minor, called the Devil's Trill. A legend says Tartini dreamed the devil played it for him and he tried to write down what he remembered, finding it far short of the dream.",
  "The formulas around the edge are from a 2007 paper by Shane Legg and Marcus Hutter. Universal intelligence, written with the Greek letter upsilon, is an agent's expected reward across all computable environments, with simpler environments weighted more.",
  "Kolmogorov complexity, the length of the shortest program that produces something, cannot be computed, so the measure is a definition and not a test."],
 [("Trill", "Rapid alternation between two neighbouring notes."), ("Agent", "Something that acts in environments; here the policy pi."), ("Environment", "A rule for how the world responds; here mu."),
  ("Kolmogorov complexity K(mu)", "Length of the shortest program that describes mu."), ("Upsilon", "The universal intelligence of an agent."), ("AIXI", "Hutter's ideal agent for this measure.")],
 ["Tartini lived from 1692 to 1770; the dream story was told to Lalande in 1766.", "Upsilon(pi) = sum over mu of 2^(-K(mu)) V(pi, mu).", "V(pi, mu) is the expected sum of rewards of policy pi in environment mu.",
  "The discounted form is the expected sum of gamma_i times r_i.", "Simple environments get exponentially larger weights, a form of Occam's razor.", "AIXI can be defined but never run exactly."],
 [T("Tartini was a great Italian violinist and teacher. His G minor sonata is famous for a long trill in the last movement, played while the violin carries other notes at the same time. The nickname comes from a story he told the astronomer Jerome Lalande in 1766: he dreamed he gave the devil a violin and the devil played so beautifully that he woke and tried to capture it. The story was told years after the music was written, so its truth is uncertain."),
  M(r"\Upsilon(\pi) \;:=\; \sum_{\mu\in E} 2^{-K(\mu)}\,V^{\pi}_{\mu}"),
  T("Read the first formula in the border from right to left. V of pi and mu is how much reward the agent pi expects to collect in the environment mu. Each environment gets the weight two to the minus K of mu, where K is its Kolmogorov complexity. Short programs get big weights. Adding up over all environments gives one number for the agent."),
  M(r"V^{\pi}_{\gamma} \;:=\; \mathbb{E}\!\left[\sum_{i=1}^{\infty} \gamma_i\, r_i\right]"),
  T("The second formula is the reward sum. At each step i the agent receives a reward r, and the discount gamma makes later rewards count less so the infinite sum is finite. The symbol E is the expected value over everything random."),
  T("Why put this next to a devil and an eye? The series is about anxiety over AI. Legg and Hutter gave a way to say what an ideal general intelligence would be, and Hutter's AIXI is the agent that would maximise it. It cannot be built, because Kolmogorov complexity cannot be computed. Like the devil in the dream, it is a perfect player we can describe but never hear.")],
 [("What does the weight 2 to the minus K favour?", ["Simple environments", "Complex environments", "Large rewards", "Late rewards"], 0, "Occam's razor."),
  ("Who defined universal intelligence?", ["Legg and Hutter", "Turing", "Shannon", "Chomsky"], 0, "In 2007."),
  ("Can universal intelligence be computed exactly?", ["No", "Yes", "Only on GPUs", "Only for chess"], 0, "K is uncomputable.")],
 [("What does gamma do?", "Discounts later rewards."), ("What is AIXI?", "The ideal agent for the measure."), ("Who was Tartini?", "An Italian violinist, 1692 to 1770."), ("What is K(mu)?", "Shortest program length.")],
 [MATCH("Symbols", "Match each symbol with its meaning.", [("Upsilon", "Universal intelligence"), ("pi", "The agent's policy"), ("mu", "An environment"), ("K(mu)", "Kolmogorov complexity"), ("gamma", "Discount factor")]),
  PL("Discounted return", "Write discounted(rewards, gamma): the sum of gamma^i times reward_i for i from 0, rounded to 6 decimals.",
     "discounted(rewards, gamma)", """
def discounted(rewards, gamma):
    t = 0.0
    g = 1.0
    for r in rewards:
        t += g * r
        g *= gamma
    return round(t, 6)
""", [[[1, 1, 1], 0.5], [[0, 0, 10], 0.9], [[5], 0.99], [[], 0.9]], "Multiply by gamma each step.", approx=1e-5),
  PL("Toy universal intelligence", "Write upsilon(envs): envs is a list of [K, value] pairs. Return the sum of 2^(-K) times value, rounded to 6 decimals.",
     "upsilon(envs)", """
def upsilon(envs):
    t = 0.0
    for k, v in envs:
        t += v * (0.5 ** k)
    return round(t, 6)
""", [[[[1, 1.0], [2, 0.5], [3, 0.0]]], [[[1, 0.0], [2, 0.0], [3, 1.0]]], [[[4, 0.8]]], [[]]], "Weight by one half to the power K.", approx=1e-5)]))
