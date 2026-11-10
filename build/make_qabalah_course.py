#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Hermetic Qabalah course. Usage: python3 make_qabalah_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "qab"))
import cmk, qb1, qb2, make_apps  # noqa: E402
make_apps.main()
CHS = qb1.CHS + qb2.CHS
PRONOUNCE = {"Qabalah": "kah bah lah", "Kabbalah": "kah bah lah", "Cabala": "kab uh luh", "Kether": "keh ter", "Chokmah": "khok mah", "Binah": "bee nah", "Chesed": "kheh sed", "Geburah": "geh boo rah",
    "Tiphareth": "tif ah reth", "Netzach": "net zakh", "Hod": "hode", "Yesod": "yeh sode", "Malkuth": "mal kooth", "sephirah": "seh fee rah", "sephiroth": "seh fee roth", "Atziluth": "at zee looth",
    "Briah": "bree ah", "Yetzirah": "yet zee rah", "Assiah": "ah see ah", "Tetragrammaton": "tet ra gram uh ton", "Ain": "ah yin", "Soph": "sofe", "Zohar": "zo har", "Bahir": "bah heer",
    "Yetzirah's": "yet zee rahs", "Sefer": "say fer", "Hermetica": "her met ih kah", "Trismegistus": "tris meh jis tus", "Agrippa": "uh grip uh", "Mirandola": "meer an doh lah", "Reuchlin": "roy klin",
    "Levi": "leh vee", "Eliphas": "el ih fass", "Mathers": "math ers", "Westcott": "west kut", "Woodman": "wood man", "Crowley": "crow lee", "Scholem": "sho lem", "Hanegraaff": "han eh grahf",
    "Aleph": "ah lef", "Beth": "bayt", "Gimel": "gih mel", "Daleth": "dah leth", "Heh": "hay", "Vav": "vahv", "Zayin": "zah yin", "Cheth": "khet", "Teth": "tet", "Yod": "yode", "Kaph": "kahf",
    "Lamed": "lah med", "Mem": "mem", "Nun": "noon", "Samekh": "sah mekh", "Ayin": "ah yin", "Peh": "pay", "Tzaddi": "tsah dee", "Qoph": "kofe", "Resh": "raysh", "Shin": "sheen", "Tav": "tahv",
    "gematria": "geh may tree uh", "notarikon": "no tah ree kon", "temurah": "teh moo rah", "Atbash": "at bash", "isopsephy": "eye sop sef ee", "Eheieh": "eh heh yeh", "Metatron": "met uh tron",
    "Sandalphon": "san dal fon", "Raphael": "raf ay el", "Primum": "pree mum", "Mobile": "moh bee lay", "Luria": "loor ee uh", "tikkun": "tee koon", "Daath": "dah ath", "syncretism": "sin kre tizm",
    "esotericism": "ess oh ter ih sizm", "Ficino": "fih chee noh", "Casaubon": "ka saw bon", "Yeats": "yates", "Waite": "wait"}
SANDBOX = cmk.terminal("Qabalah cheat sheet", "qab>", "A scripted lookup. Try: tree, pillars, worlds, letters, tarot, gematria", [
    ("tree", ["10 sephiroth: Kether, Chokmah, Binah, Chesed, Geburah, Tiphareth, Netzach, Hod, Yesod, Malkuth. 22 paths."]),
    ("pillars", ["Mercy: Chokmah, Chesed, Netzach | Severity: Binah, Geburah, Hod | Balance: Kether, Tiphareth, Yesod, Malkuth"]),
    ("worlds", ["Atziluth (fire, Wands) | Briah (water, Cups) | Yetzirah (air, Swords) | Assiah (earth, Pentacles)"]),
    ("letters", ["Mothers: Aleph Mem Shin | Doubles: Beth Gimel Daleth Kaph Peh Resh Tav | Simples: the other twelve"]),
    ("tarot", ["Golden Dawn: Aleph The Fool, Beth The Magician, Gimel The High Priestess ... Tav The World. A 19th-century pairing."]),
    ("gematria", ["Shalom: shin 300 + lamed 30 + vav 6 + mem 40 = 376. A word game, not proof."]),
])
EXAM = [
 ("What does Qabalah mean?", ["Received tradition", "Magic book", "Tree of Life", "Hidden name"], 0, "Root meaning to receive."),
 ("Which spelling marks the Jewish tradition?", ["Kabbalah", "Cabala", "Qabalah", "Kabala only"], 0, "With K."),
 ("When was the Golden Dawn founded?", ["1888", "1788", "1950", "1620"], 0, "London."),
 ("Roughly when is the Zohar dated by historians?", ["Late 13th century", "1st century", "16th century", "19th century"], 0, "Spain."),
 ("What does the Sefer Yetzirah describe?", ["Ten sephiroth and 22 letters", "A Tarot deck", "A ritual", "A recipe"], 0, "32 paths."),
 ("Who translated the Hermetica into Latin in 1463?", ["Marsilio Ficino", "Casaubon", "Reuchlin", "Crowley"], 0, "Florence."),
 ("What did Casaubon show in 1614?", ["The Hermetica are late, not ancient Egyptian", "The Zohar is forged", "The Tree has 12 sephiroth", "Tarot is Greek"], 0, "Dating."),
 ("How many sephiroth are on the Tree?", ["10", "22", "7", "32"], 0, "Plus 22 paths."),
 ("Which sephirah is the Crown?", ["Kether", "Malkuth", "Yesod", "Hod"], 0, "At the top."),
 ("Which pillar holds Chokmah?", ["Mercy", "Severity", "Balance", "None"], 0, "Right-hand pillar."),
 ("Which sephirah is the Kingdom?", ["Malkuth", "Kether", "Tiphareth", "Binah"], 0, "Bottom."),
 ("What is Atziluth?", ["The world of emanation", "The world of action", "A sephirah", "A path"], 0, "Fire."),
 ("Which element goes with Yetzirah?", ["Air", "Fire", "Water", "Earth"], 0, "Swords."),
 ("How many Hebrew letters and paths on the Tree?", ["22", "10", "32", "12"], 0, "One letter per path."),
 ("Which are the three mother letters?", ["Aleph, Mem, Shin", "Beth, Gimel, Daleth", "Heh, Vav, Zayin", "Yod, Kaph, Lamed"], 0, "Air, water, fire."),
 ("What do the 12 simple letters match?", ["Zodiac signs", "Planets", "Elements", "Pillars"], 0, "Aries to Pisces."),
 ("What is the value of Shin?", ["300", "30", "3", "3000"], 0, "The letter shin."),
 ("Which card goes with Tav?", ["The World", "The Fool", "The Sun", "Death"], 0, "Path 32."),
 ("When did Tarot cards first appear?", ["15th century, as a card game", "Ancient Egypt", "12th century", "20th century"], 0, "Northern Italy."),
 ("Which planet goes with Tiphareth?", ["The Sun", "The Moon", "Mars", "Saturn"], 0, "Heart of the Tree."),
 ("What does Atbash swap?", ["First letter with last, and so on", "Vowels", "Words", "Numbers"], 0, "Aleph with Tav."),
 ("What is the gematria of shalom?", ["376", "346", "306", "400"], 0, "300 + 30 + 6 + 40."),
 ("Do equal gematria sums prove a link?", ["No, they are wordplay", "Yes, always", "Only in Hebrew", "Only for names"], 0, "Coincidences are common."),
 ("Who wrote The Mystical Qabalah (1935)?", ["Dion Fortune", "Crowley", "Agrippa", "Waite"], 0, "A British author."),
 ("What is 777?", ["Crowley's tables of correspondences", "A prayer", "A Tarot deck", "A Hebrew book"], 0, "1909."),
 ("How does this course treat the subject?", ["As history and symbolism", "As proven science", "As a religion to join", "As a game"], 0, "Cultural study."),
]
CFG = dict(id="hermetic-qabalah", title="Hermetic Qabalah: A Historical and Symbolic Study",
    subtitle="The Tree of Life, the Hebrew letters, Tarot correspondences and where they came from, taught as history and symbolism",
    description="A beginner-friendly study of Hermetic Qabalah as a historical and symbolic tradition: how Jewish Kabbalah, Renaissance Hermeticism and the Golden Dawn fed into it, the ten sephiroth and 22 paths of the Tree of Life, the four worlds, the Hebrew letters with real script and number values, Tarot and planetary correspondences, the methods of gematria, notarikon and temurah, and how to read the whole thing critically. Python labs encode the tables; an interactive Tree of Life lets you explore the spheres. No claims of supernatural effect are made.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="qab", apps={"__TREE__": "tree.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "hermetic-qabalah.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
