# -*- coding: utf-8 -*-
"""Hermetic Qabalah course, part 1: history, sources, the Tree, worlds, letters."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


GEM = '''
VALUES = {"א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7, "ח": 8, "ט": 9, "י": 10,
  "כ": 20, "ך": 20, "ל": 30, "מ": 40, "ם": 40, "נ": 50, "ן": 50, "ס": 60, "ע": 70,
  "פ": 80, "ף": 80, "צ": 90, "ץ": 90, "ק": 100, "ר": 200, "ש": 300, "ת": 400}
'''

CHS.append(CH(
 "What Hermetic Qabalah is: a historical map",
 ("Three streams", [
  "Kabbalah | is | Jewish mystical tradition",
  "Cabala | is | Christian Renaissance reading",
  "Qabalah | is | Hermetic Western esotericism",
  "Golden Dawn | systematised | Hermetic Qabalah",
  "Tree of Life | organises | Correspondences",
  "Scholars | study | It as history",
  "Practitioners | use | It as symbolism"]),
 ["The word Qabalah means 'received tradition'. Three spellings mark three streams. Kabbalah is the Jewish mystical tradition. Cabala is the Christian reading of the Renaissance. Qabalah is the Hermetic system of Western esotericism.",
  "Hermetic Qabalah blends Jewish Kabbalah, Renaissance Hermetism, astrology, alchemy and Tarot, and was systematised in the 19th century by groups such as the Hermetic Order of the Golden Dawn.",
  "This course treats it as a historical and symbolic study: where the ideas come from, how the Tree of Life is organised, and how people have used it as a map of symbols."],
 [("Kabbalah", "The Jewish mystical tradition, with texts such as the Zohar."),
  ("Christian Cabala", "A Renaissance reading of Kabbalah by Christian scholars such as Pico della Mirandola."),
  ("Hermetic Qabalah", "A Western esoteric system that links the Tree of Life to astrology, Tarot and other symbols."),
  ("Hermeticism", "A tradition based on writings attributed to Hermes Trismegistus."),
  ("Correspondence", "A symbolic link between items in different systems, such as a planet and a sephirah.")],
 ["Kabbalah, Cabala, Qabalah: three streams.",
  "Hermetic Qabalah is a 19th-century synthesis.",
  "Its Tree has 10 sephiroth and 22 paths.",
  "Study it as history and symbolism.",
  "Claims of results are beliefs, not tested facts."],
 [T("Qabalah comes from a Hebrew root meaning to receive. The idea is of a teaching handed down. But different groups have received very different things, and the spelling is a handy way to tell them apart."),
  T("Kabbalah, with K, is the Jewish mystical tradition. It grew in medieval Spain and France and found classic expression in the Zohar, a late thirteenth-century book. It deals with how the infinite God relates to the world, and has been studied through the Torah by Jewish scholars for centuries."),
  T("Cabala, with C, is how Christian thinkers of the Renaissance read it. In 1486 the Italian Pico della Mirandola put forward nine hundred theses and said that Kabbalah confirms Christian truths. Johannes Reuchlin and Cornelius Agrippa followed, mixing Kabbalah with Neoplatonism, astrology and natural magic."),
  T("Qabalah, with Q, names the Hermetic form. In the nineteenth century, Eliphas Levi, the Golden Dawn, A. E. Waite, Aleister Crowley and Dion Fortune matched the Tree of Life with Tarot, planets and elements. This is the system that most people mean today by the Qabalah."),
  T("Scholars such as Gershom Scholem, Frances Yates and Wouter Hanegraaff study these streams as history. They show where ideas really came from, and which claims of ancient origin hold up. This course follows that approach, and treats the symbols as a cultural tradition, with no claim about their power.")],
 [("What does Qabalah mean?", ["Received tradition", "Magic book", "Tree of Life", "Hidden name"], 0, "From a Hebrew root meaning to receive."),
  ("Which spelling marks the Jewish tradition?", ["Kabbalah", "Cabala", "Qabalah", "Kabala only"], 0, "With K."),
  ("Who wrote nine hundred theses in 1486?", ["Pico della Mirandola", "Crowley", "Fortune", "Scholem"], 0, "A Renaissance scholar."),
  ("Which group systematised Hermetic Qabalah?", ["The Golden Dawn", "The Zohar", "The Sanhedrin", "The Vulgate"], 0, "Founded in 1888."),
  ("How does this course treat the subject?", ["As history and symbolism", "As a proven science", "As a religion to join", "As a game"], 0, "Cultural study."),
  ("Who is a major scholar of Kabbalah?", ["Gershom Scholem", "Aleister Crowley", "Eliphas Levi", "Dion Fortune"], 0, "Jerusalem, 20th century.")],
 [("Kabbalah", "Jewish mystical tradition"), ("Cabala", "Christian Renaissance reading"), ("Qabalah", "Hermetic system"), ("Golden Dawn", "founded 1888"), ("Scholem", "historian of Kabbalah")],
 [MATCH("Match the spelling", "Pair each spelling with its stream.", [("Kabbalah", "Jewish mystical tradition"), ("Cabala", "Christian Renaissance reading"), ("Qabalah", "Hermetic Western esotericism")]),
  ORDER("A rough timeline", "Order these events from earliest to latest.", ["The Zohar appears (late 13th century)", "Pico's nine hundred theses (1486)", "Agrippa's Occult Philosophy (1533)", "The Golden Dawn is founded (1888)", "Fortune's Mystical Qabalah (1935)"]),
  PL("Which stream?", "Write stream(spelling): return 'Jewish' for 'Kabbalah', 'Christian' for 'Cabala', 'Hermetic' for 'Qabalah', otherwise 'unknown'.", "stream(spelling)", '''
def stream(spelling):
    if spelling == "Kabbalah":
        return "Jewish"
    if spelling == "Cabala":
        return "Christian"
    if spelling == "Qabalah":
        return "Hermetic"
    return "unknown"
''', [["Kabbalah"], ["Cabala"], ["Qabalah"], ["Kabala"]], "A simple chain of checks.")]
))

CHS.append(CH(
 "Sources: Hermes, Sefer Yetzirah and the Zohar",
 ("Sources", [
  "Sefer Yetzirah | describes | Letters and numbers",
  "Zohar | comments | On the Torah",
  "Bahir | teaches | Early sephiroth",
  "Hermetica | attributes | To Hermes",
  "Emerald Tablet | says | As above so below",
  "Lurianic | adds | Shattering and repair",
  "Kabbala Denudata | translates | For Christians"]),
 ["The Hebrew letters and the ten sephiroth first appear together in the Sefer Yetzirah, the Book of Formation, a short text of uncertain date, probably between the second and sixth centuries.",
  "The Bahir (12th century) and the Zohar (13th) developed the sephiroth into a map of the divine. In the 16th century, Isaac Luria added the ideas of the breaking of vessels and the repair of the world.",
  "The Hermetic side comes from the Corpus Hermeticum, Greek texts of the early centuries CE attributed to Hermes Trismegistus, and from a short Arabic text called the Emerald Tablet."],
 [("Sefer Yetzirah", "The Book of Formation, an early short text on the 32 paths of wisdom: ten sephiroth and 22 letters."),
  ("Zohar", "The Book of Splendour, a late 13th-century commentary on the Torah, central to Kabbalah."),
  ("Corpus Hermeticum", "Greek writings of the early centuries CE, attributed to Hermes Trismegistus."),
  ("Emerald Tablet", "A short alchemical text, first known in Arabic, with the line 'as above, so below'."),
  ("Kabbala Denudata", "A 17th-century Latin collection of Kabbalistic texts by Knorr von Rosenroth.")],
 ["Sefer Yetzirah: 10 sephiroth + 22 letters = 32 paths.",
  "Zohar: 13th century, Moses de Leon.",
  "Luria: 16th century, shattering and repair.",
  "Hermetica: Greek, early centuries CE.",
  "Emerald Tablet: 'as above, so below'."],
 [T("The oldest source for the Tree's building blocks is the Sefer Yetzirah. It speaks of thirty-two paths of wisdom: the ten sephiroth, meaning numbers or spheres, and the twenty-two letters of the Hebrew alphabet. It says the world was formed by letters and numbers, and divides the letters into three mothers, seven doubles and twelve simples."),
  T("In the twelfth and thirteenth centuries, the Bahir and the Zohar gave the sephiroth their well-known names and meanings. The Zohar was published in Spain by Moses de Leon. Tradition says it is much older, but modern historians date it to the late thirteenth century. It reads the Torah as a layered symbolic text."),
  T("Isaac Luria of Safed in the sixteenth century offered a dramatic story. The divine light filled vessels that shattered, scattering sparks, and human actions help to repair the world. This is called tikkun. It is one of the most influential ideas in later Jewish thought."),
  T("A different tradition, Hermeticism, comes from Greek writings that claim to record the teachings of Hermes Trismegistus, the thrice-greatest Hermes. The Florentine scholar Marsilio Ficino translated them in 1463, thinking they were ancient Egyptian. In 1614 Isaac Casaubon showed they were written in the early centuries CE."),
  T("The Emerald Tablet is a short, riddling text on alchemy. Its best-known line says that what is below is like what is above, and what is above is like what is below. That idea of correspondence, a mirror between heaven and earth, is the core of the Hermetic Qabalah. The Qabalah is a table of such mirrors.")],
 [("What does the Sefer Yetzirah describe?", ["Ten sephiroth and 22 letters", "A Tarot deck", "A ritual", "A recipe"], 0, "32 paths."),
  ("When is the Zohar usually dated by historians?", ["Late 13th century", "1st century", "16th century", "19th century"], 0, "Spain."),
  ("Who added the idea of the breaking of vessels?", ["Isaac Luria", "Pico", "Agrippa", "Fortune"], 0, "Safed, 16th century."),
  ("Who translated the Hermetica into Latin in 1463?", ["Marsilio Ficino", "Casaubon", "Reuchlin", "Crowley"], 0, "Florence."),
  ("What did Casaubon show in 1614?", ["The Hermetica are late, not ancient Egyptian", "The Zohar is forged", "The Tree has 12 sephiroth", "Tarot is Greek"], 0, "Dating."),
  ("What does the Emerald Tablet's key line express?", ["Correspondence between above and below", "A recipe for gold", "A calendar", "A law code"], 0, "As above, so below.")],
 [("Sefer Yetzirah", "Book of Formation"), ("Zohar", "Book of Splendour"), ("Luria", "shattering and repair"), ("Corpus Hermeticum", "Hermes writings"), ("Emerald Tablet", "as above, so below")],
 [MATCH("Match the source", "Pair each source with its description.", [("Sefer Yetzirah", "letters and numbers form the world"), ("Zohar", "mystical Torah commentary"), ("Corpus Hermeticum", "Greek writings of Hermes"), ("Emerald Tablet", "as above, so below"), ("Kabbala Denudata", "Latin collection of 1677")]),
  PL("Count the paths", "Write paths_of_wisdom(sephiroth, letters): the Sefer Yetzirah's number of paths is the number of sephiroth plus the number of letters. Return that sum. With 10 and 22 it is 32.", "paths_of_wisdom(sephiroth, letters)", '''
def paths_of_wisdom(sephiroth, letters):
    return sephiroth + letters
''', [[10, 22], [10, 0], [0, 22], [7, 12]], "Add the two counts."),
  PL("Divide the letters", "Write letter_groups(): return the Sefer Yetzirah's division of the 22 letters as [mothers, doubles, simples] counts, which are [3, 7, 12]. Compute the number of simples as 22 minus the mothers minus the doubles.", "letter_groups()", '''
def letter_groups():
    mothers = 3
    doubles = 7
    return [mothers, doubles, 22 - mothers - doubles]
''', [[]], "The simples are what remains.")]
))

CHS.append(CH(
 "The Tree of Life: ten sephiroth",
 ("The Tree", [
  "Tree | has | Ten sephiroth",
  "Pillar of Mercy | holds | Chokmah Chesed Netzach",
  "Pillar of Severity | holds | Binah Geburah Hod",
  "Middle Pillar | holds | Kether Tiphareth Yesod Malkuth",
  "Kether | is | The Crown",
  "Malkuth | is | The Kingdom",
  "Lightning Flash | descends | Through the Tree"]),
 ["The Tree of Life is a diagram of ten spheres, the sephiroth, joined by twenty-two paths. Read from the top, it shows how the unity of Kether, the Crown, unfolds step by step into the world of Malkuth, the Kingdom.",
  "The sephiroth sit on three pillars. The right pillar is Mercy, the left is Severity, and the middle pillar balances them. Each sephirah has a name, a number, a Divine Name, an archangel and, in the Hermetic system, a planet.",
  "Names with Hebrew spelling: Kether כתר, Chokmah חכמה, Binah בינה, Chesed חסד, Geburah גבורה, Tiphareth תפארת, Netzach נצח, Hod הוד, Yesod יסוד, Malkuth מלכות."],
 [("Sephirah", "One of the ten spheres on the Tree of Life; plural sephiroth."),
  ("Pillar", "One of the three vertical columns of the Tree: Mercy, Severity and Balance."),
  ("Lightning Flash", "The zigzag path from Kether to Malkuth that visits each sephirah in order."),
  ("Daath", "A hidden 'knowledge' sphere sometimes drawn between Chokmah and Binah, not one of the ten."),
  ("Ain Soph", "The unlimited, 'without end', beyond Kether.")],
 ["10 sephiroth, 22 paths, 3 pillars.",
  "Mercy (right): Chokmah, Chesed, Netzach.",
  "Severity (left): Binah, Geburah, Hod.",
  "Balance (middle): Kether, Tiphareth, Yesod, Malkuth.",
  "Order: Kether 1 to Malkuth 10."],
 [T("Picture a tree-shaped diagram: ten circles, linked by lines. At the top is Kether (כתר, the Crown), the highest point and the source. At the bottom is Malkuth (מלכות, the Kingdom), the world we live in. Between them are eight more spheres."),
  T("The first triad is Kether, Chokmah (חכמה, Wisdom) and Binah (בינה, Understanding). Wisdom is a flash of insight, and Understanding is the form that shapes it. Below them are Chesed (חסד, Mercy), Geburah (גבורה, Strength) and Tiphareth (תפארת, Beauty), where mercy and severity are balanced."),
  T("The lowest triad is Netzach (נצח, Victory), Hod (הוד, Splendour) and Yesod (יסוד, Foundation). Netzach stands for feeling and desire, Hod for thought and speech, and Yesod for the images that connect them. All of this lands in Malkuth. Hermetic authors link Yesod with the Moon and Malkuth with the Earth."),
  T("The spheres lie on three vertical columns. On the right is the Pillar of Mercy, with Chokmah, Chesed and Netzach, linked with expansion. On the left is the Pillar of Severity, with Binah, Geburah and Hod, linked with limits. The Middle Pillar of Balance holds Kether, Tiphareth, Yesod and Malkuth."),
  T("A path called the Lightning Flash zigzags from Kether down through Chokmah, Binah, Chesed, Geburah, Tiphareth, Netzach, Hod and Yesod to Malkuth, in number order. It is a picture of creation descending. Going back up the Tree, the 'Path of the Serpent', is the symbolic journey of return.")],
 [("How many sephiroth are on the Tree?", ["10", "22", "7", "32"], 0, "Plus 22 paths."),
  ("Which sephirah is the Crown?", ["Kether", "Malkuth", "Yesod", "Hod"], 0, "At the top."),
  ("Which pillar holds Chokmah?", ["Mercy", "Severity", "Balance", "None"], 0, "Right-hand pillar."),
  ("Which sephirah is the Kingdom?", ["Malkuth", "Kether", "Tiphareth", "Binah"], 0, "At the bottom."),
  ("What is the Lightning Flash?", ["The zigzag from Kether to Malkuth", "A ritual", "A Tarot spread", "A prayer"], 0, "Creation descending."),
  ("Which sephirah is Beauty?", ["Tiphareth", "Hod", "Netzach", "Chesed"], 0, "Heart of the Tree.")],
 [("Kether כתר", "Crown"), ("Chokmah חכמה", "Wisdom"), ("Binah בינה", "Understanding"), ("Tiphareth תפארת", "Beauty"), ("Malkuth מלכות", "Kingdom")],
 [APP("TREE", "Tree of Life explorer", "Tap each sephirah to see its Hebrew name, meaning, pillar and the Hermetic planet linked to it. Visit 6 different sephiroth to complete this lab.", 720),
  MATCH("Match the sephirah", "Pair each sephirah with its meaning.", [("Kether כתר", "Crown"), ("Chokmah חכמה", "Wisdom"), ("Binah בינה", "Understanding"), ("Chesed חסד", "Mercy"), ("Geburah גבורה", "Strength"), ("Tiphareth תפארת", "Beauty"), ("Malkuth מלכות", "Kingdom")]),
  MATCH("Match the pillar", "Pair each sephirah with its pillar.", [("Chokmah", "Mercy"), ("Chesed", "Mercy"), ("Binah", "Severity"), ("Geburah", "Severity"), ("Tiphareth", "Balance"), ("Malkuth", "Balance")]),
  PL("Which pillar?", "Write pillar(n): n is a sephirah number 1 to 10 (1 Kether, 2 Chokmah, 3 Binah, 4 Chesed, 5 Geburah, 6 Tiphareth, 7 Netzach, 8 Hod, 9 Yesod, 10 Malkuth). Return 'Mercy' for 2, 4 and 7; 'Severity' for 3, 5 and 8; 'Balance' for 1, 6, 9 and 10.", "pillar(n)", '''
def pillar(n):
    if n in [2, 4, 7]:
        return "Mercy"
    if n in [3, 5, 8]:
        return "Severity"
    return "Balance"
''', [[1], [2], [3], [6], [7], [8], [10]], "Test membership in the two side lists."),
  PL("Lightning Flash", "Write flash(): return the list of sephirah numbers that the Lightning Flash visits, in order. It goes 1 to 10 in number order, so return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], built with a loop.", "flash()", '''
def flash():
    out = []
    for i in range(1, 11):
        out.append(i)
    return out
''', [[]], "Use range(1, 11).")]
))

CHS.append(CH(
 "Four Worlds, divine names and the planes of the Tree",
 ("Four Worlds", [
  "Atziluth | is | Emanation",
  "Briah | is | Creation",
  "Yetzirah | is | Formation",
  "Assiah | is | Action",
  "Tetragrammaton | has | Four letters",
  "Ain Soph | is | Beyond the Tree",
  "Divine Names | belong | To sephiroth"]),
 ["Kabbalah describes four worlds, or levels: Atziluth (emanation), Briah (creation), Yetzirah (formation) and Assiah (action). In the Hermetic system each has its own Tree, and each links to an element, a card suit and a letter of the Divine Name.",
  "The four-letter Name of God, the Tetragrammaton, Yod Heh Vav Heh (יהוה), is traditionally not pronounced. The letters map to the four worlds and the four elements: fire, water, air and earth.",
  "Each sephirah also has a Divine Name, an archangel, and an angelic order in Hermetic tables."],
 [("Atziluth", "The world of emanation, linked with fire and the Divine Names."),
  ("Briah", "The world of creation, linked with water and the archangels."),
  ("Yetzirah", "The world of formation, linked with air and the angelic orders."),
  ("Assiah", "The world of action, linked with earth and the material world."),
  ("Tetragrammaton", "The four-letter name Yod Heh Vav Heh.")],
 ["Atziluth (Yod, fire, wands).",
  "Briah (Heh, water, cups).",
  "Yetzirah (Vav, air, swords).",
  "Assiah (final Heh, earth, pentacles).",
  "Ain Soph lies beyond Kether."],
 [T("Most Qabalists describe reality in layers. The highest is Atziluth, the world of emanation, where the first spark is nearest its source. Then Briah, the world of creation, then Yetzirah, the world of formation, and last Assiah, the world of action, which includes physical things."),
  T("These four worlds line up with the four letters of the Tetragrammaton (יהוה). The first letter Yod (י) stands for Atziluth, the first Heh (ה) for Briah, Vav (ו) for Yetzirah, and the last Heh (ה) for Assiah. Many traditions avoid saying the Name out loud, and say Adonai or HaShem instead."),
  T("The Hermetic system adds elements and Tarot suits. Atziluth is fire, with the suit of Wands. Briah is water, with Cups. Yetzirah is air, with Swords. Assiah is earth, with Pentacles. This makes a little table in which four sets of symbols are lined up."),
  T("Each sephirah is given a Divine Name in Atziluth. Kether is Eheieh (אהיה, I Am), Chokmah is Yah (יה), and Binah is YHVH Elohim. Malkuth is Adonai ha-Aretz (Lord of the Earth). An archangel is paired with each sephirah in Briah, such as Metatron for Kether, Raphael for Tiphareth, Michael for Hod and Sandalphon for Malkuth."),
  T("Beyond Kether the sources speak of Ain (nothing), Ain Soph (limitless) and Ain Soph Aur (limitless light), three veils of negative existence. They are not part of the Tree. They express that the source of all is beyond description, which is why the Tree starts with a crown and not with a name.")],
 [("What is Atziluth?", ["The world of emanation", "The world of action", "A sephirah", "A path"], 0, "Fire."),
  ("Which letter stands for Assiah?", ["The final Heh", "Yod", "Vav", "The first Heh"], 0, "Earth."),
  ("Which Tarot suit goes with Briah?", ["Cups", "Wands", "Swords", "Pentacles"], 0, "Water."),
  ("What is Eheieh?", ["The Divine Name of Kether", "A path", "A card", "An archangel"], 0, "I Am."),
  ("What lies beyond Kether?", ["Ain Soph", "Malkuth", "Yesod", "Daath"], 0, "The limitless."),
  ("Which element goes with Yetzirah?", ["Air", "Fire", "Water", "Earth"], 0, "Swords.")],
 [("Atziluth", "emanation, fire, Wands"), ("Briah", "creation, water, Cups"), ("Yetzirah", "formation, air, Swords"), ("Assiah", "action, earth, Pentacles"), ("YHVH יהוה", "Tetragrammaton")],
 [MATCH("Match the world", "Pair each world with its element.", [("Atziluth", "fire"), ("Briah", "water"), ("Yetzirah", "air"), ("Assiah", "earth")]),
  MATCH("Match the letter", "Pair each letter of the Name with its world.", [("Yod י", "Atziluth"), ("Heh ה", "Briah"), ("Vav ו", "Yetzirah"), ("final Heh ה", "Assiah")]),
  PL("World for an element", "Write world(element): return 'Atziluth' for 'fire', 'Briah' for 'water', 'Yetzirah' for 'air', 'Assiah' for 'earth', otherwise 'unknown'.", "world(element)", '''
def world(element):
    table = {"fire": "Atziluth", "water": "Briah", "air": "Yetzirah", "earth": "Assiah"}
    if element in table:
        return table[element]
    return "unknown"
''', [["fire"], ["water"], ["air"], ["earth"], ["spirit"]], "A dictionary lookup."),
  PL("Suit for a world", "Write suit(world): return 'Wands' for 'Atziluth', 'Cups' for 'Briah', 'Swords' for 'Yetzirah', 'Pentacles' for 'Assiah', otherwise 'unknown'.", "suit(world)", '''
def suit(world):
    table = {"Atziluth": "Wands", "Briah": "Cups", "Yetzirah": "Swords", "Assiah": "Pentacles"}
    if world in table:
        return table[world]
    return "unknown"
''', [["Atziluth"], ["Briah"], ["Yetzirah"], ["Assiah"], ["Daath"]], "Look it up in a table.")]
))

CHS.append(CH(
 "The Hebrew letters and the 22 paths",
 ("Letters and paths", [
  "Alphabet | has | 22 letters",
  "Letter | joins | Two sephiroth",
  "Mothers | are | Three letters",
  "Doubles | are | Seven letters",
  "Simples | are | Twelve letters",
  "Letter | has | A number value",
  "Path | has | A Tarot card"]),
 ["The 22 letters of the Hebrew alphabet correspond to the 22 paths linking the sephiroth. The Sefer Yetzirah divides the letters into three mothers (Aleph א, Mem מ, Shin ש), seven doubles (Beth ב, Gimel ג, Daleth ד, Kaph כ, Peh פ, Resh ר, Tav ת) and twelve simples.",
  "The Golden Dawn linked the mothers with the elements air, water and fire, the doubles with the seven classical planets, and the twelve simples with the signs of the zodiac.",
  "Each letter also has a numerical value, which is the basis of gematria."],
 [("Mother letters", "Aleph, Mem and Shin, linked with the elements air, water and fire."),
  ("Double letters", "The seven letters that have a hard and a soft sound, linked with the planets."),
  ("Simple letters", "The twelve remaining letters, linked with the zodiac signs."),
  ("Path", "A line on the Tree that joins two sephiroth and is linked with a letter."),
  ("Gematria", "The practice of finding the number value of words from their letters.")],
 ["Mothers: Aleph (air), Mem (water), Shin (fire).",
  "Doubles: Beth Mercury, Gimel Moon, Daleth Venus, Kaph Jupiter, Peh Mars, Resh Sun, Tav Saturn.",
  "Simples: Heh Aries to Qoph Pisces.",
  "Values run 1 to 10, then 20 to 90, then 100 to 400.",
  "Paths are numbered 11 to 32."],
 [T("There are twenty-two letters and twenty-two paths. The first ten paths are the sephiroth themselves, numbered 1 to 10, and the paths between them are numbered 11 to 32. So path 11 is the first letter Aleph (א), joining Kether and Chokmah, and path 32 is Tav (ת), joining Yesod and Malkuth."),
  T("The three mother letters are Aleph (א), Mem (מ) and Shin (ש). In the Sefer Yetzirah they stand for the elemental forces. The Golden Dawn matched Aleph with air, Mem with water and Shin with fire, and these three paths are the most basic ones."),
  T("The seven double letters have a hard and soft sound: Beth (ב), Gimel (ג), Daleth (ד), Kaph (כ), Peh (פ), Resh (ר) and Tav (ת). The Hermetic tables assign them to the seven classical planets: Mercury, the Moon, Venus, Jupiter, Mars, the Sun and Saturn."),
  T("The remaining twelve are the simple letters: Heh (ה), Vav (ו), Zayin (ז), Cheth (ח), Teth (ט), Yod (י), Lamed (ל), Nun (נ), Samekh (ס), Ayin (ע), Tzaddi (צ) and Qoph (ק). They are matched with the twelve zodiac signs from Aries to Pisces."),
  T("Letters were also numbers in the ancient Hebrew system. Aleph is 1, Beth 2, up to Yod 10, then Kaph 20, Lamed 30 and so on to Tzaddi 90, then Qoph 100, Resh 200, Shin 300 and Tav 400. Five letters have a final form used at the end of a word, with the same value in the standard system.")],
 [("How many letters and paths?", ["22", "10", "32", "12"], 0, "One letter per path."),
  ("Which letters are the three mothers?", ["Aleph, Mem, Shin", "Beth, Gimel, Daleth", "Heh, Vav, Zayin", "Yod, Kaph, Lamed"], 0, "Air, water, fire."),
  ("How many double letters?", ["7", "3", "12", "5"], 0, "Linked with planets."),
  ("What do the 12 simple letters match?", ["Zodiac signs", "Planets", "Elements", "Pillars"], 0, "Aries to Pisces."),
  ("What is the value of Shin?", ["300", "30", "3", "3000"], 0, "Value of ש."),
  ("What joins Yesod and Malkuth?", ["Tav, path 32", "Aleph, path 11", "Mem, path 23", "Resh, path 30"], 0, "The last path.")],
 [("Aleph א", "1, air, path 11"), ("Mem מ", "40, water, path 23"), ("Shin ש", "300, fire, path 31"), ("Tav ת", "400, Saturn, path 32"), ("Yod י", "10, Virgo, path 20")],
 [MATCH("Match the letter to its value", "Pair each letter with its number value.", [("א Aleph", "1"), ("ב Beth", "2"), ("י Yod", "10"), ("כ Kaph", "20"), ("ק Qoph", "100"), ("ת Tav", "400")]),
  MATCH("Match the mother letters", "Pair each mother letter with its element.", [("א Aleph", "air"), ("מ Mem", "water"), ("ש Shin", "fire")]),
  PL("Gematria", "Write gematria(word): the sum of the standard values of the Hebrew letters in the word. Values: א 1, ב 2, ג 3, ד 4, ה 5, ו 6, ז 7, ח 8, ט 9, י 10, כ ך 20, ל 30, מ ם 40, נ ן 50, ס 60, ע 70, פ ף 80, צ ץ 90, ק 100, ר 200, ש 300, ת 400. Ignore any other character, such as vowel points.", "gematria(word)", GEM + '''
def gematria(word):
    total = 0
    for ch in word:
        if ch in VALUES:
            total = total + VALUES[ch]
    return total
''', [["שלום"], ["אהבה"], ["אחד"], ["יהוה"], ["מלך"], ["א"]], "Look up each letter and add."),
  PL("Reduce a number", "Write reduce(n): repeatedly add the digits of n until one digit remains (the theosophical reduction, used to compare sums). reduce(376) is 3 + 7 + 6 = 16, then 1 + 6 = 7.", "reduce(n)", '''
def reduce(n):
    while n >= 10:
        s = 0
        for ch in str(n):
            s = s + int(ch)
        n = s
    return n
''', [[376], [26], [10], [9], [999], [0]], "Loop until the number is under 10.")]
))
