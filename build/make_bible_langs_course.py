#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Bible languages course (Biblical Hebrew, Koine Greek, Latin). Usage: python3 make_bible_langs_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "blc"))
import cmk, bl1, bl2, make_apps  # noqa: E402

make_apps.main()
CHS = bl1.CHS + bl2.CHS

PRONOUNCE = {"Septuagint": "sep too a gint", "Vulgate": "vul gate", "Koine": "coy nay", "Masoretes": "mass oh reets", "Masoretic": "mass oh ret ic",
    "niqqud": "nee kood", "shva": "shwah", "dagesh": "dah gesh", "gematria": "geh may tree uh", "isopsephy": "eye sop sef ee", "alef": "ah lef",
    "kamets": "kah mets", "binyan": "bin yan", "binyanim": "bin yah neem", "Qal": "kahl", "Piel": "pee el", "Hiphil": "hif eel", "Niphal": "nif al",
    "Elohim": "el oh heem", "Shalom": "shah lome", "shalom": "shah lome", "Eucharist": "you ka rist", "aorist": "air ist", "ecclesiastical": "ee klee zee ass tick al",
    "ablative": "ab luh tiv", "Leitner": "lite ner", "Jerome": "jeh rome", "logos": "low goss", "theos": "thay oss", "agape": "ah gah pay", "kyrios": "kew ree oss",
    "Vayomer": "vah yo mer", "vayomer": "vah yo mer", "Shema": "shuh mah", "eimi": "ay mee", "luo": "loo oh", "Septuagint's": "sep too a gints", "Pater": "pah ter", "Noster": "nos ter",
    "interlinear": "inter lin ee er", "cognate": "cog nate", "cognates": "cog nates", "mnemonic": "nuh mon ick", "loci": "low sigh", "Alexandria": "al ex an dree uh"}

SANDBOX = cmk.terminal("Phrase lookup", "bib>", "A scripted phrasebook, not a translator. Try: hello, thanks, peace, name, love, light", [
    ("hello", ["Hebrew: shalom | Greek: chaire | Latin: salve"]),
    ("thanks", ["Hebrew: toda | Greek: eucharisto | Latin: gratias"]),
    ("peace", ["Hebrew: shalom | Greek: eirene | Latin: pax"]),
    ("name", ["Hebrew: shem | Greek: onoma | Latin: nomen"]),
    ("love", ["Hebrew: ahavah | Greek: agape | Latin: amor or caritas"]),
    ("light", ["Hebrew: or | Greek: phos | Latin: lux"]),
])

EXAM = [
 ("Which language wrote most of the Old Testament?", ["Hebrew", "Greek", "Latin", "Syriac"], 0, "With small Aramaic parts."),
 ("What is the Septuagint?", ["The Greek Old Testament", "The Latin Bible", "A Hebrew grammar", "A Gospel"], 0, "From Alexandria."),
 ("Who wrote the Vulgate?", ["Jerome", "Paul", "Origen", "Luther"], 0, "In Latin, about 400 AD."),
 ("How many letters does the Hebrew alphabet have?", ["22", "24", "26", "23"], 0, "All consonants."),
 ("Which direction is Hebrew read?", ["Right to left", "Left to right", "Both", "Top down"], 0, "From the right edge."),
 ("What is the gematria of shalom (300+30+6+40)?", ["376", "346", "306", "400"], 0, "Add the letters."),
 ("What does the dagesh do?", ["Hardens or doubles a letter", "Marks stress", "Marks a vowel", "Marks a final form"], 0, "A dot inside."),
 ("What is the Hebrew masculine plural ending?", ["-im", "-ot", "-ah", "-ayim"], 0, "Melekh, melakhim."),
 ("How do you say 'the' in Hebrew?", ["ha-", "ve-", "le-", "min"], 0, "A prefix."),
 ("What is typical Hebrew word order?", ["Verb, subject, object", "Subject, verb, object", "Subject, object, verb", "Free"], 0, "Bara elohim."),
 ("What is a Hebrew root?", ["Usually three consonants", "A vowel pattern", "A suffix", "A prefix"], 0, "K-t-v."),
 ("What does vayomer mean?", ["And he said", "He will say", "Say!", "They said"], 0, "Vav-consecutive."),
 ("How many letters does the Greek alphabet have?", ["24", "22", "26", "27"], 0, "Alpha to omega."),
 ("What does the rough breathing add?", ["An h sound", "A stress", "A long vowel", "Nothing"], 0, "Ho, hemera."),
 ("Which Greek case marks the subject?", ["Nominative", "Accusative", "Genitive", "Dative"], 0, "Ho theos."),
 ("What is the accusative singular of logos?", ["logon", "logou", "logo", "logoi"], 0, "Add -on."),
 ("What does the Greek genitive mean?", ["Of", "To", "By", "Object"], 0, "Tou theou."),
 ("What is the present 'I' ending of a regular Greek verb?", ["-o", "-eis", "-ei", "-ousi"], 0, "Luo."),
 ("What does the aorist show?", ["A simple event", "Ongoing action", "A wish", "A command"], 0, "Eluse."),
 ("What is Greek for 'God is love'?", ["ho theos agape estin", "agape theos", "theos logos", "kyrios agape"], 0, "1 John 4:8."),
 ("How is Church Latin 'ce' said?", ["che", "ke", "se", "ze"], 0, "Caelum."),
 ("How many cases does Latin have?", ["Six", "Four", "Five", "Seven"], 0, "Nom, gen, dat, acc, abl, voc."),
 ("What is the genitive singular of puella?", ["puellae", "puellam", "puella", "puellis"], 0, "First declension."),
 ("Which case follows 'cum'?", ["Ablative", "Accusative", "Genitive", "Nominative"], 0, "Cum Deo."),
 ("What is 'we love' in Latin?", ["amamus", "amatis", "amant", "amat"], 0, "The -mus ending."),
 ("What does 'erat' mean?", ["was", "is", "will be", "be"], 0, "Imperfect of sum."),
 ("What is Latin for 'six'?", ["sex", "septem", "octo", "novem"], 0, "Like Greek hex."),
 ("How is 'is' handled in a Hebrew present sentence?", ["Left out", "Written as hayah", "Written as eimi", "Written as sum"], 0, "Nominal sentence."),
 ("Which is Hebrew for 'peace'?", ["shalom", "toda", "lechem", "bayit"], 0, "Also hello."),
 ("What is Latin for 'light'?", ["lux", "nox", "aqua", "dies"], 0, "Lucid."),
 ("What is the Latin greeting?", ["salve", "vale", "gratias", "quaeso"], 0, "Be well."),
 ("What does 'toda' mean?", ["Thank you", "Please", "Hello", "Yes"], 0, "Hebrew."),
 ("What does an interlinear show?", ["A gloss under each word", "Only a smooth translation", "The original only", "A dictionary"], 0, "Word by word."),
 ("Where does the verb stand in Hebrew Genesis 1:1?", ["First", "Last", "Absent", "Middle"], 0, "Bara."),
 ("What is the first step of the translation method?", ["Find the verb", "Smooth the English", "Memorise", "Check the dictionary"], 0, "The verb anchors it."),
 ("What does a missed Leitner card do?", ["Returns to box 1", "Moves up", "Is dropped", "Stays"], 0, "Spaced practice."),
 ("What is a cognate?", ["A related word in another language", "A verb ending", "A vowel mark", "A number"], 0, "Pater and paternal."),
 ("Why is the pronoun often left out in Greek and Latin?", ["The ending shows the person", "It does not exist", "It is rude", "It is silent"], 0, "Amo, agapo."),
 ("Which is a Hebrew loanword in English?", ["amen", "logic", "pacify", "photo"], 0, "Also sabbath."),
]

CFG = dict(id="bible-languages", title="Bible Languages: Biblical Hebrew, Koine Greek and Latin",
    subtitle="Alphabets, grammar, core vocabulary, everyday phrases and how to translate between the three, with flashcards and an interlinear reader",
    description="A beginner-friendly course in the three languages of the Bible. Learn the Hebrew alphabet and vowels, the Greek alphabet and cases, and Latin nouns and verbs; build a core vocabulary of 45 words and 16 phrases side by side with memory hooks; read thirteen parallel passages with an interlinear reader; and practise translating between the languages with spaced-repetition flashcards and Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="blc",
    apps={"__CARDS__": "cards.html", "__READER__": "reader.html"})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "bible-languages.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
