#!/usr/bin/env python3
"""Build The Golem Series course. Usage: python3 make_golem_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "golemc"))
import cmk, g1, g2  # noqa: E402

PRONOUNCE = {
    "Ehyeh": "eh yeh", "Baphomet": "baf oh met", "ouroboros": "oo roh boh ross", "Ouroboros": "oo roh boh ross", "Eliphas": "el ih fass", "Levi": "lay vee", "ayin": "ah yeen", "Ayin": "ah yeen",
    "Tartini": "tar tee nee", "Kolmogorov": "kol mo gor off", "AIXI": "ay ix ee", "Hutter": "hut ter", "Legg": "leg", "Enochian": "ee noh kee un", "Babalon": "bab uh lon", "ephah": "ee fah", "Ephah": "ee fah",
    "Shinar": "shy nar", "glaux": "glowks", "Glaux": "glowks", "Zechariah": "zek uh rye uh", "Sefer": "say fer", "Yetzirah": "yets ee rah", "Abulafia": "ab oo lah fee uh", "Maharal": "mah ha rahl",
    "gematria": "guh may tree uh", "Gematria": "guh may tree uh", "golem": "go lem", "Golem": "go lem", "emet": "eh met", "Emet": "eh met", "Septuagint": "sep too uh jint", "Thelema": "thuh lee muh",
    "Chomsky": "chom skee", "Sanhedrin": "san hed rin", "Kabbalist": "kab uh list", "Kabbalah": "kab uh luh", "HoTT": "H O T T", "SO(2)": "S O two", "refl": "reff el", "isopsephy": "eye sop sef ee",
    "Foucault": "foo koh", "Neville": "nev il", "Kelley": "kell ee", "Dee": "dee", "Athena": "uh thee nuh", "Schwartz": "shwarts", "IEEE": "I triple E", "chokhmah": "khokh mah", "einam": "ay nahm",
    "avonam": "ah voh nahm", "Mandorla": "man dor luh", "Wyoming": "wy oh ming", "Larghetto": "lar get oh", "ELI5": "E L I five", "RGB": "R G B", "Jude": "jude", "Upsilon": "up sih lon", "upsilon": "up sih lon",
    "Trill": "trill", "Lalande": "luh land", "Ingress": "in gress", "Egress": "ee gress", "Leitmotiv": "light moh teef", "ayin hara": "ah yeen hah rah", "Elijah": "ee lie juh", "pareidolia": "pair eye doh lee uh",
    "apophenia": "ap oh fee nee uh", "Pareidolia": "pair eye doh lee uh", "Apophenia": "ap oh fee nee uh", "Ω": "omega", "Υ": "upsilon", "SO": "S O",
}

SANDBOX = cmk.terminal("Series cheat sheet", "series>", "A scripted lookup, not a real program. Try: ehyeh, ayin, loop, eye, entropy, owl, golem, gml", [
    ("ehyeh", ["Exodus 3:14: I am, or I will be", "gematria 21; the first image"]),
    ("ayin", ["ע: an eye, then a circle, then Greek O", "value 70; ring, evil eye and their eye"]),
    ("loop", ["Omega of the circle is the integers", "refl is the trivial path; loop goes around once"]),
    ("eye", ["Evil eye: ayin hara; Eye of Providence in RGB light", "red + green + blue make white"]),
    ("entropy", ["H = minus the sum of p log p", "a fair coin has 1 bit"]),
    ("owl", ["gamma lambda alpha upsilon xi spell glaux", "Athena's bird; value 494"]),
    ("golem", ["emet, truth, minus aleph is met, dead", "Sanhedrin 65b: Rava's man cannot speak"]),
    ("gml", ["G grammar, L language, M machine", "golem is 73, the same as wisdom"]),
])

EXAM = [
 ("What are the four images, in order?", ["Self, Watcher, Union, Creation", "Fire, water, earth, air", "Birth, life, death, rebirth", "Past, present, future, end"], 0, "The arc."),
 ("What is common to all four images?", ["Hebrew, a symbol, math, a devil figure and a quote", "A face", "A song", "A date"], 0, "The recipe."),
 ("What does Ehyeh mean?", ["I am, or I will be", "Hear", "Holy", "Light"], 0, "Exodus 3:14."),
 ("What is the shape of Paleo-Hebrew ayin?", ["A circle", "A square", "A line", "A cross"], 0, "An eye, then a circle."),
 ("Who drew the 1856 Baphomet?", ["Eliphas Levi", "John Dee", "Aleister Crowley", "Tartini"], 0, "A French occultist."),
 ("What does solve et coagula mean?", ["Dissolve and combine", "Seek and find", "Rise and fall", "Give and take"], 0, "Alchemy."),
 ("What does the identity matrix do to a vector?", ["Leaves it unchanged", "Doubles it", "Rotates it", "Deletes it"], 0, "I times v is v."),
 ("What does x squared plus y squared equal one describe?", ["The unit circle", "A line", "A parabola", "A square"], 0, "Distance one."),
 ("What is SO(2)?", ["The group of plane rotations", "A matrix of ones", "A number", "A letter"], 0, "A circle itself."),
 ("What is refl?", ["The trivial path a equals a", "The circle", "A loop", "An integer"], 0, "Nothing happens."),
 ("What are the loops of the circle counted by?", ["The integers", "The reals", "Only 0 and 1", "The primes"], 0, "Omega S1 is Z."),
 ("What do red, green and blue light make together?", ["White", "Black", "Brown", "Grey"], 0, "Additive."),
 ("What does ayin hara mean?", ["The evil eye", "Holy light", "Blue bead", "Red thread"], 0, "Bad eye."),
 ("What does Revelation 20:7 describe?", ["Satan released after a thousand years", "The new Jerusalem", "A flood", "A trumpet"], 0, "The Watcher's text."),
 ("What does the weight 2 to the minus K favour?", ["Simple environments", "Complex ones", "Big rewards", "Late rewards"], 0, "Occam's razor."),
 ("Who defined universal intelligence?", ["Legg and Hutter", "Turing", "Shannon", "Chomsky"], 0, "2007."),
 ("What does entropy measure?", ["Uncertainty in bits", "Speed", "Size", "Heat only"], 0, "Shannon."),
 ("What is the Queen's Gambit?", ["1. d4 d5 2. c4", "1. e4 e5", "1. f3", "1. c4 c5"], 0, "A pawn offered."),
 ("Which place has 44.5902 N, 104.7146 W?", ["Devils Tower", "Mount Rushmore", "Yellowstone", "Area 51"], 0, "Wyoming."),
 ("Who recorded Enochian?", ["John Dee and Edward Kelley", "Crowley", "Levi", "Moses"], 0, "1580s."),
 ("What is in the ephah of Zechariah 5?", ["A woman called Wickedness", "Gold", "Grain", "A lion"], 0, "Carried to Shinar."),
 ("What does einam mean?", ["Their eye", "Their house", "Their king", "Their name"], 0, "Zechariah 5:6."),
 ("What do the Greek labels in image 3 spell?", ["Glaux, owl", "Gaia", "Gnosis", "Gamma"], 0, "Athena's bird."),
 ("Whose spelling is Babalon?", ["Aleister Crowley's", "John Dee's", "Zechariah's", "Eco's"], 0, "Thelema."),
 ("How many gates does Sefer Yetzirah count?", ["231", "22", "32", "613"], 0, "22 choose 2."),
 ("Could Rava's man in Sanhedrin 65b speak?", ["No", "Yes", "Only Hebrew", "Only at night"], 0, "He was sent back to dust."),
 ("What does erasing the aleph in emet give?", ["Met, dead", "Truth", "Golem", "Nothing"], 0, "The golem is deactivated."),
 ("What do G, L and M stand for in image 4?", ["Grammar, language, machine", "God, light, man", "Gate, letter, mem", "Gold, lead, mercury"], 0, "Also the golem root."),
 ("What is golem in gematria?", ["73", "70", "21", "441"], 0, "3 + 30 + 40."),
 ("Which golem story is a later legend?", ["The Maharal of Prague", "Rava's man", "Psalm 139", "Adam's first hour"], 0, "Retellings from the 1800s."),
 ("Which claim is an interpretation, not a source?", ["I AM is a nontrivial loop", "Exodus 3:14 says Ehyeh", "Zechariah mentions an eye", "Rava made a man"], 0, "The HoTT reading."),
 ("How many pairs do 40 ideas make?", ["780", "40", "400", "1600"], 0, "n times n minus 1 over 2."),
 ("What is emet in gematria?", ["441, which is 21 squared", "73", "70", "21"], 0, "A coincidence."),
]

CFG = dict(id="the-golem-series", title="The Golem Series: Letters, Eyes and Machines", subtitle="Four collages, read as one story from Ehyeh to the golem, with the math, texts and Python behind each",
    description="Read a series of four esoteric collages as one story: The Self, The Watcher, The Union and The Creation. Each image mixes Hebrew, occult symbols, real mathematics and a quotation. You will learn the sources behind every element: Exodus 3:14, the ouroboros and Baphomet, the identity matrix and homotopy type theory, the evil eye, Tartini and Legg-Hutter universal intelligence, Shannon entropy, the Queen's Gambit, Devils Tower, Enochian, Zechariah 5, the golem legend, grammars and Turing machines. It also teaches how to tell a source from an interpretation. Each chapter has an ELI5 block and Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="golemc", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "the-golem-series.course.json")
    cmk.main(CFG, g1.A + g2.B, [sys.argv[0], out])
