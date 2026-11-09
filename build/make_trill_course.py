#!/usr/bin/env python3
"""Build 'The Devil's Trill: Decoding an Image'. Usage: python3 make_trill_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "trillc"))
import cmk, tr1  # noqa: E402

PRONOUNCE = {"ayin": "eye in", "hara": "ha ra", "Tartini": "tar tee nee", "Lalande": "la lond", "Trille": "treel", "Diable": "dee abl", "Sonata": "so nah ta", "hamsa": "ham sa",
    "mati": "mah tee", "kinehora": "kin uh hora", "Pontormo": "pon tor mo", "Annuit": "an wit", "Coeptis": "kep tis", "chilia": "kill ya", "chiliasm": "kill ee az um", "Koine": "koy nay",
    "lythesetai": "lee thay say tie", "Satanas": "sa ta nas", "Kolmogorov": "kol mo gor of", "Hutter": "hoot er", "Legg": "leg", "AIXI": "A I X I", "ELI5": "E L I five", "Upsilon": "up si lon",
    "mu": "mew", "pi": "pie", "gamma": "gam uh", "RGB": "R G B", "MIDI": "middy", "Eschatology": "es ka tol o jee", "Apophenia": "ap oh fee nee uh", "gematria": "geh may tree uh",
    "Providence": "prov i dence", "Masonic": "ma son ik", "Freemasons": "free may sons", "tritone": "try tone", "amillennial": "ay mill en ee al"}

SANDBOX = cmk.terminal("Decoder", "decode>", "A scripted lookup. Try: eye, verse, colour, trill, formula", [
    ("eye", ["ayin hara = evil eye (Hebrew)", "Eye of Providence = God's watching care (Christian art, 1500s)"]),
    ("verse", ["Revelation 20:7: when the thousand years are completed, Satan will be released from his prison"]),
    ("colour", ["red + green = yellow, green + blue = cyan, red + blue = magenta, all three = white"]),
    ("trill", ["Tartini, Violin Sonata in G minor, the Devil's Trill", "legend told to Lalande in 1766"]),
    ("formula", ["Upsilon(pi) = sum over mu of 2^(-K(mu)) V(pi, mu)", "Legg and Hutter, 2007"]),
])

EXAM = [
 ("What is the first step in reading a layered image?", ["Identify each element on its own terms", "Decide the hidden plan", "Ignore text", "Pick a colour"], 0, "Facts before interpretation."),
 ("What does ayin hara mean?", ["Evil eye", "Holy light", "Blue bead", "Red sea"], 0, "Literally bad eye."),
 ("What is gematria?", ["Adding the number values of letters", "A prayer", "A charm", "A scripture"], 0, "A traditional practice."),
 ("Which protective object is a hand shape?", ["Hamsa", "Mati", "Red thread", "Seal"], 0, "Used in several communities."),
 ("What does Revelation 20:7 say?", ["Satan is released after the thousand years", "The world ends", "A temple is built", "Judgement begins"], 0, "The line in the image."),
 ("Which reading treats the thousand years as symbolic?", ["Amillennial", "Premillennial", "Postmillennial", "None"], 0, "Reading the period symbolically."),
 ("What did the eye in a triangle first mean in Christian art?", ["God's watchful care and the Trinity", "A secret plot", "A bank", "A formula"], 0, "Providence."),
 ("When was the Great Seal reverse designed?", ["1782", "1492", "1935", "1620"], 0, "It reached the dollar in 1935."),
 ("What do red and green light make?", ["Yellow", "Brown", "White", "Purple"], 0, "Additive mixing."),
 ("What do all three light primaries make?", ["White", "Black", "Grey", "Brown"], 0, "At full strength."),
 ("What is #0000ff?", ["Pure blue", "Pure red", "Black", "White"], 0, "Blue channel full."),
 ("Who composed the Devil's Trill sonata?", ["Giuseppe Tartini", "Bach", "Vivaldi", "Mozart"], 0, "G. Tartini."),
 ("What is a trill?", ["Quick alternation of two neighbouring notes", "A loud chord", "A slow tune", "A tuning"], 0, "Often with the note above."),
 ("How many semitones in a tritone?", ["Six", "Three", "Seven", "Twelve"], 0, "Half an octave."),
 ("What is the frequency of A4?", ["440 Hz", "220 Hz", "880 Hz", "400 Hz"], 0, "The standard pitch."),
 ("What does an octave do to frequency?", ["Doubles it", "Halves it", "Adds 12", "Nothing"], 0, "A ratio of two."),
 ("Who defined universal intelligence?", ["Legg and Hutter", "Turing", "Shannon", "McCarthy"], 0, "In 2007."),
 ("What does the weight 2^(-K) favour?", ["Simple environments", "Complex ones", "Large rewards", "Late rewards"], 0, "Occam's razor."),
 ("What does gamma do?", ["Discounts later rewards", "Adds noise", "Sets the policy", "Counts steps"], 0, "It keeps the sum finite."),
 ("Can universal intelligence be computed exactly?", ["No", "Yes", "Only on GPUs", "Only for small games"], 0, "K is not computable."),
 ("What is apophenia?", ["Seeing patterns in unrelated things", "A music form", "A colour", "A formula"], 0, "A natural bias."),
 ("In a group of 23, how likely is a shared birthday?", ["About 50 percent", "About 6 percent", "About 99 percent", "Impossible"], 0, "The birthday problem."),
 ("What is the best habit with symbol claims?", ["Check original sources", "Share quickly", "Trust the loudest", "Ignore context"], 0, "Provenance."),
 ("Is the dream legend of the sonata proven?", ["No, it was told years later", "Yes, signed by Tartini", "Yes, in the score", "It is law"], 0, "Lalande's account from 1766."),
]

CFG = dict(id="devils-trill-decoding-an-image", title="The Devil's Trill: Decoding an Image", subtitle="The evil eye, Revelation, the Eye of Providence, light, Tartini and universal intelligence",
    description="A course built from one collage: a Hebrew evil-eye title, a Greek verse from Revelation, red-green-blue circles around an eye in a triangle, Tartini's Devil's Trill, and formulas for universal intelligence. Learn what each element really is, with Python labs on gematria, additive colour, equal temperament, discounted reward and the birthday problem, and end with tools for reading symbols critically.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="trillc", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "devils-trill-decoding-an-image.course.json")
    cmk.main(CFG, tr1.A, [sys.argv[0], out])
