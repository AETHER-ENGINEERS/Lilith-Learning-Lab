# -*- coding: utf-8 -*-
"""Bible languages, part 1: overview, Hebrew, Greek."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clib import *
from data import NOUNS, VERBS

CHS = []

def APP(key, title, intro, h=640):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}

# ---------------------------------------------------------------- 1
CHS.append(CH(
 "Three languages, one library",
 ("The three languages", [
  "Hebrew | wrote | Most of the Old Testament",
  "Greek | wrote | The New Testament",
  "Greek | translated | The Septuagint",
  "Latin | translated | The Vulgate",
  "Hebrew | reads | Right to left",
  "Greek | has | Five cases",
  "Latin | has | Six cases",
  "Memory | needs | Repetition"]),
 ["The Bible was written mostly in Hebrew, with a little Aramaic, and the New Testament in Koine Greek. Early Greek and Latin translations, the Septuagint and the Vulgate, shaped the church for a thousand years and still hold many of its words.",
  "The three languages work differently. Hebrew builds words from three-letter roots and reads right to left. Greek and Latin both use endings (cases) to show who does what to whom, so word order is flexible.",
  "This course teaches the alphabets and sounds, the grammar, the core vocabulary side by side, common phrases, and how to translate between the three, with memory tools in every chapter."],
 [("Koine Greek", "The common Greek of the Mediterranean world, about 300 BC to 300 AD, the language of the New Testament."),
  ("Septuagint", "The Greek translation of the Hebrew Scriptures, made in Alexandria from about 250 BC."),
  ("Vulgate", "The Latin Bible translated mostly by Jerome around 400 AD."),
  ("Interlinear", "A text with a word-by-word gloss written under each word of the original."),
  ("Cognate", "A word that shares an origin with a word in another language, like Latin pater and English paternal."),
  ("Root", "In Hebrew, the usually three consonants that carry a word's core meaning.")],
 ["Hebrew: right to left, consonants first, roots of three letters.",
  "Greek: 24 letters, five cases, three genders, flexible word order.",
  "Latin: no alphabet to learn, six cases, no articles, verb at the end.",
  "A Greek or Latin ending tells you the job of the word; Hebrew uses small words and word order.",
  "You learn fastest by short daily sessions, not long rare ones.",
  "Link every new word to something you know: an English word, a picture or a story."],
 [T("Imagine a library with three doors. Behind the first is Hebrew, the language of the Law, the Prophets and the Psalms. Behind the second is Koine Greek, the plain, widely spoken Greek in which the Gospels and letters were written. Behind the third is Latin, the language of Rome and of the church in the West. Most of the Bible can be read in at least two of these, which is why learning them together pays off."),
  T("The Old Testament was written in Hebrew, with small parts in Aramaic. About 250 years before Christ, Jewish scholars in Alexandria translated it into Greek, the Septuagint. The New Testament was written in Greek, and the apostles often quote the Septuagint. Around 400 AD Jerome translated the Bible into Latin, the Vulgate, working from the Hebrew and Greek. So the same verse often exists in all three, and we can lay them side by side."),
  T("The languages are built differently. Hebrew is a Semitic language, related to Arabic. It is written right to left, and a word grows from a root of usually three consonants. The root k-t-v means writing: katav is he wrote, ktav is a writing, sefer is a book. Greek and Latin are Indo-European, cousins of English. They show a word's job with an ending, called its case. In Latin, Deus creavit caelum and caelum creavit Deus both mean that God made heaven, because the endings say who is the subject."),
  T("How do you remember so many new words? Three tools run through the whole course. First, spaced repetition: review a word after one day, then two, then four, then eight. The flashcard labs use exactly this system, called Leitner boxes. Second, hooks: tie each word to an English word, such as photo for the Greek phos, light, or pacify for the Latin pax, peace. Third, stories: a vivid little picture sticks far better than a bare list."),
  T("A word on pronunciation. Scholars read these languages in slightly different ways. This course uses a simple, widely used reading for each: standard modern Hebrew sounds, a school reading of Koine Greek, and the Latin of the Church, which is easy for English speakers. Learn one way well, and the others follow quickly.")],
 [("Which language wrote most of the Old Testament?", ["Hebrew", "Greek", "Latin", "Aramaic only"], 0, "With small Aramaic parts."),
  ("What is the Septuagint?", ["The Greek translation of the Hebrew Scriptures", "The Latin Bible", "A Hebrew grammar", "The Gospels"], 0, "Made in Alexandria."),
  ("Who produced the Vulgate?", ["Jerome", "Paul", "Constantine", "Augustine"], 0, "Around 400 AD."),
  ("Which direction does Hebrew read?", ["Right to left", "Left to right", "Top to bottom", "Either way"], 0, "Start at the right edge."),
  ("How do Greek and Latin show a word's job?", ["Endings called cases", "Word order only", "Tone", "Special letters"], 0, "Nominative, accusative and the rest."),
  ("Why use spaced repetition?", ["Reviewing just before you forget builds long memory", "It is faster to cram", "It avoids learning grammar", "It needs no time"], 0, "The Leitner boxes.")],
 [("Hebrew root", "Usually three consonants carrying the core meaning."), ("Greek and Latin word jobs", "Shown by case endings."), ("Septuagint", "The Greek Old Testament."), ("Vulgate", "Jerome's Latin Bible."),
  ("The Leitner system", "Cards move up a box when you know them and back to box 1 when you miss them."), ("A cognate", "A related word in another language, like pater and paternal.")],
 [MATCH("Match the text to its language", "Match each work to the language it was written or translated into.", [("Most of the Old Testament", "Hebrew"), ("The New Testament", "Koine Greek"), ("The Septuagint", "Greek"), ("The Vulgate", "Latin")]),
  ORDER("Put these in order in time", "From earliest to latest.", ["The Hebrew Scriptures are written", "The Septuagint translation is made in Alexandria", "The New Testament is written in Greek", "Jerome writes the Vulgate in Latin"]),
  FILL("Directions and endings", "Hebrew reads from {{right}} to left. Greek and Latin show a word's job with {{endings}}. The Leitner system is a form of {{spaced}} repetition.")]
))

# ---------------------------------------------------------------- 2
CHS.append(CH(
 "Hebrew: the alphabet",
 ("The Hebrew alphabet", [
  "Hebrew | has | 22 letters",
  "Hebrew | reads | Right to left",
  "Five letters | have | Final forms",
  "Alef | is | A silent letter",
  "Bet | is | B or V",
  "Shin | is | Sh or S",
  "Letters | are | Numbers"]),
 ["Hebrew has 22 letters, all of them consonants, written and read from right to left. Five letters change shape at the end of a word. Letters double as numbers, so every word has a numeric value, called gematria.",
  "A few letters sound alike (tet and tav, kaf and qof). Learning each one with a picture-name and a sound makes them stick.",
  "The labs match letters to sounds and compute gematria in Python."],
 [("Alef-bet", "The Hebrew alphabet, named for its first two letters, alef and bet."),
  ("Final form", "A different shape for kaf, mem, nun, pe and tsade at the end of a word."),
  ("Gematria", "The numeric value of a word, found by adding its letters' values."),
  ("Consonantal script", "A script that writes the consonants and leaves most vowels to the reader."),
  ("Begadkefat", "The six letters bet, gimel, dalet, kaf, pe and tav, which can be hard or soft.")],
 ["22 letters, no capitals, read right to left.",
  "Final forms: kaf ך, mem ם, nun ן, pe ף, tsade ץ.",
  "Alef and ayin are silent carriers of a vowel; chet is a rough h.",
  "Vav ו and yod י can be vowel letters as well as consonants.",
  "Values: alef 1 to yod 10, then 20, 30 ... 90, then 100 to 400 (qof, resh, shin, tav)."],
 [T("Open a Hebrew book at what an English reader calls the back. Hebrew starts at the right edge of the page and the line runs to the left. The alphabet has 22 letters, all consonants, and no capital letters. The first four are alef, bet, gimel and dalet, which gave Greek its alpha, beta, gamma and delta, and gave us our A, B, C and D."),
  C("א alef  silent     | ב bet  b/v     | ג gimel g   | ד dalet d\nה he    h          | ו vav  v/o/u   | ז zayin z   | ח chet  kh (rough h)\nט tet   t          | י yod  y/i     | כ kaf   k/kh| ל lamed l\nמ mem   m          | נ nun  n       | ס samekh s  | ע ayin  silent/guttural\nפ pe    p/f        | צ tsade ts     | ק qof   k   | ר resh  r\nש shin  sh/s      | ת tav  t", "text"),
  T("Five letters have a second shape used only at the end of a word: kaf ך, mem ם, nun ן, pe ף and tsade ץ. The final forms reach below the line. This makes it easy to see where a word stops, since Hebrew has no space-saving capitals. Some letters look alike, so learn them in pairs: bet ב has a rounded corner and kaf כ a round back; dalet ד and resh ר differ by a small corner; vav ו and zayin ז differ by a crown."),
  T("The letters bet, gimel, dalet, kaf, pe and tav can be hard or soft. Bet is b when it carries a dot called a dagesh and v without it. Kaf is k with a dagesh and kh without, and pe is p with a dagesh and f without. The letter shin is sh with a dot on the right and s with a dot on the left, which is then called sin."),
  T("Because Hebrew letters were also the numbers, every word has a value. Alef is one, bet two, up to yod ten, then tens up to tsade at ninety, then hundreds: qof one hundred, resh two hundred, shin three hundred, tav four hundred. Shalom, shin lamed vav mem, is 300 plus 30 plus 6 plus 40, which is 376. People have found hidden connections in such sums for centuries; here it is a fun way to drill the letters and the numbers."),
  T("Memory tip: say the letter names aloud in order, like a song, twice a day for a week. Then draw each letter once while saying its sound. The ancient letter pictures help too: alef was an ox, bet a house, gimel a camel, dalet a door.")],
 [("How many letters are in the Hebrew alphabet?", ["22", "24", "26", "27"], 0, "All consonants."),
  ("Which direction is Hebrew read?", ["Right to left", "Left to right", "Top to bottom", "Spiral"], 0, "From the right edge."),
  ("Which of these has a final form?", ["Mem", "Alef", "Bet", "Dalet"], 0, "Mem ם."),
  ("What is gematria?", ["The numeric value of a word", "A vowel sign", "A verb form", "A kind of poem"], 0, "Alef 1, bet 2 ..."),
  ("Which letters are silent carriers?", ["Alef and ayin", "Bet and gimel", "Resh and shin", "Mem and nun"], 0, "They hold a vowel.")],
 [("א", "Alef, silent, value 1"), ("ב", "Bet, b or v, value 2"), ("ש", "Shin, sh, value 300"), ("ת", "Tav, t, value 400"), ("Which letters change at the end of a word?", "Kaf, mem, nun, pe, tsade")],
 [MATCH("Match the letter to its name", "Pair each Hebrew letter with its name.", [("א", "alef"), ("ב", "bet"), ("ג", "gimel"), ("ד", "dalet"), ("ה", "he"), ("ו", "vav"), ("ז", "zayin"), ("ח", "chet")]),
  MATCH("Match the letter to its value", "Pair each letter with its number.", [("א", "1"), ("י", "10"), ("כ", "20"), ("ק", "100"), ("ר", "200"), ("ש", "300"), ("ת", "400")]),
  PL("Gematria", "Write gematria(word): add the value of each Hebrew letter. Alef 1 to tet 9, yod 10, kaf 20 ... tsade 90, qof 100, resh 200, shin 300, tav 400. The final forms ם ן ף ץ ך have the same values as mem 40, nun 50, pe 80, tsade 90, kaf 20. Ignore any other character.", "gematria(word)", '''
def gematria(word):
    v = {"א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7, "ח": 8, "ט": 9, "י": 10, "כ": 20, "ך": 20, "ל": 30, "מ": 40, "ם": 40, "נ": 50, "ן": 50, "ס": 60, "ע": 70, "פ": 80, "ף": 80, "צ": 90, "ץ": 90, "ק": 100, "ר": 200, "ש": 300, "ת": 400}
    total = 0
    for ch in word:
        total += v.get(ch, 0)
    return total
''', [["אב"], ["שלום"], ["אדם"], ["אמת"], ["חי"], ["מלך"], ["בן"]], "Use a dictionary from letter to value and add with a loop. Skip letters not in the dictionary.")]
))

# ---------------------------------------------------------------- 3
CHS.append(CH(
 "Hebrew: vowels and reading",
 ("Reading Hebrew", [
  "Niqqud | adds | Vowels",
  "Kamets | sounds | ah",
  "Hiriq | sounds | ee",
  "Holam | sounds | oh",
  "Shva | is | A short e or silent",
  "Dagesh | doubles | Or hardens",
  "Syllable | needs | One vowel"]),
 ["Early Hebrew wrote only consonants. Later scribes added little dots and dashes, the niqqud, to show vowels. With them a beginner can read any word aloud.",
  "There are five vowel sounds in several shapes, plus the half-vowel shva and the dot called dagesh. Every syllable has exactly one vowel.",
  "The labs match vowel signs to sounds and ask you to read real words."],
 [("Niqqud", "The system of dots and dashes written with the consonants to mark vowels."),
  ("Shva", "A sign that marks either a very short e or no vowel at all."),
  ("Dagesh", "A dot inside a letter that makes it hard, or doubles it."),
  ("Syllable", "A beat of sound; in Hebrew each syllable has one vowel."),
  ("Matres lectionis", "Letters like vav and yod used to show vowels.")],
 ["Vowel signs sit below, above or inside the consonant.",
  "ַ patach and ָ kamets sound like ah; ֵ tsere and ֶ segol like eh.",
  "ִ hiriq is ee, ֹ holam is oh, ֻ kubbuts and וּ shureq are oo.",
  "ְ shva at the start of a word is a quick e; between syllables it is silent.",
  "Most words are stressed on the last syllable."],
 [T("The earliest Hebrew texts have no vowel marks. Readers knew the words, so consonants were enough, as you can read 'Pls rd ths' in English. A few centuries after Christ, scribes called the Masoretes added a system of dots and dashes, the niqqud, to preserve the exact reading. Printed Bibles and learner books still use it."),
  C("ַ patach  ah  (בַּ ba)     ָ kamets ah  (בָּ ba)\nֵ tsere   ay  (בֵּ bay)    ֶ segol  eh  (בֶּ be)\nִ hiriq   ee  (בִּ bee)    ֹ holam  oh  (בֹּ bo)\nֻ kubbuts oo  (בֻּ boo)    וּ shureq oo (בוּ boo)\nְ shva    short e or silent", "text"),
  T("The sign sits under most letters, over a few, and inside the vav. Say a consonant plus a vowel as one beat: bet plus kamets is ba. Add the next letter, and you have a word: ba plus yod plus tav gives bayit, a house, from the vocabulary list. Every syllable needs exactly one vowel sound, so count the vowels to count the beats."),
  T("The shva, two dots stacked under a letter, is the only sign that behaves in two ways. At the beginning of a word, or after a long vowel, it is a very short e as in the first syllable of the English word 'again'. After a short vowel it is silent and just closes the syllable. The dagesh, a dot inside a letter, hardens the begadkefat letters and doubles other letters, as in the article ha plus a doubled letter."),
  T("Practice reading with words you already know. Shalom is shin kamets, lamed holam vav, mem: sha-lom. Melekh, king, is mem segol, lamed segol, final kaf: me-lekh. Elohim has the alef carrying a segol (the e), then a shva-holam: e-lo-him. Say each aloud slowly three times, then at speed. Reading aloud is the best way to turn the signs into habit.")],
 [("What do the niqqud mark?", ["Vowels", "Numbers", "Stress only", "Punctuation"], 0, "Added by the Masoretes."),
  ("How does kamets sound in simple reading?", ["ah", "ee", "oh", "oo"], 0, "Like patach."),
  ("What does holam sound like?", ["oh", "ah", "ee", "eh"], 0, "As in 'shalom'."),
  ("What is the dagesh?", ["A dot that hardens or doubles a letter", "A vowel", "A stress mark", "A final form"], 0, "Inside the letter."),
  ("How many vowels does a syllable have?", ["One", "Two", "None", "Three"], 0, "Count the vowels to count the beats.")],
 [("ָ", "Kamets, ah"), ("ֵ", "Tsere, ay"), ("ִ", "Hiriq, ee"), ("ֹ", "Holam, oh"), ("ְ", "Shva, short e or silent")],
 [MATCH("Match the vowel sign to its sound", "Pair each vowel with how it sounds.", [("ַ patach", "ah"), ("ֵ tsere", "ay"), ("ִ hiriq", "ee"), ("ֹ holam", "oh"), ("ֻ kubbuts", "oo")]),
  MATCH("Read the word", "Match each Hebrew word with its reading.", [("שָׁלוֹם", "shalom"), ("מֶלֶךְ", "melekh"), ("בַּיִת", "bayit"), ("אָדָם", "adam"), ("בֵּן", "ben")]),
  FILL("Fill in the rule", "Each syllable has exactly one {{vowel}}. A dot in a letter is a {{dagesh}}. A shva between syllables is {{silent}}."),
  PL("Syllables", "Write syllables_he(translit): count the syllables in a transliterated word by counting groups of vowels (a, e, i, o, u). Treat the word as lowercase. A run like 'ai' counts as one beat.", "syllables_he(translit)", '''
def syllables_he(translit):
    n = 0
    prev = False
    for ch in translit.lower():
        v = ch in "aeiou"
        if v and not prev:
            n += 1
        prev = v
    return n
''', [["shalom"], ["bereshit"], ["elohim"], ["bayit"], ["melekh"], ["shamayim"]], "Walk through the letters; count a vowel only when the previous letter was not a vowel.")]
))

# ---------------------------------------------------------------- 4
CHS.append(CH(
 "Hebrew grammar: nouns, articles and sentences",
 ("Hebrew nouns", [
  "Noun | has | Gender",
  "Noun | has | Number",
  "Masculine plural | ends | im",
  "Feminine plural | ends | ot",
  "Article | is | ha",
  "No | indefinite article | Hebrew",
  "Verb to be | is left out | In the present",
  "Construct | joins | Two nouns"]),
 ["Hebrew nouns are masculine or feminine and singular, plural or dual. The plural usually ends in -im for masculine and -ot for feminine, and pairs of things use the dual -ayim.",
  "There is one article, ha-, meaning 'the'. There is no word for 'a'. The verb 'is' is usually left out: 'The man good' means 'the man is good'. Two nouns joined together, as in 'house of the king', form a construct chain.",
  "Small words are attached to the front: ve- and, be- in, le- to or for, min from. Pronouns can attach to the end: -i my, -kha your, -o his."],
 [("Gender", "Whether a noun is masculine or feminine."),
  ("Dual", "A special plural for natural pairs, ending in -ayim."),
  ("Definite article", "The word 'the'; in Hebrew the prefix ha-."),
  ("Construct state", "A noun linked to the noun that follows, meaning 'X of Y'."),
  ("Nominal sentence", "A sentence with no verb, where 'is' is understood."),
  ("Inseparable preposition", "A short word, like be- or le-, written as part of the next word.")],
 ["Masculine plural -im: melekh, melakhim (kings).",
  "Feminine often ends in -ah; plural -ot: torah, torot.",
  "Dual -ayim: yad hand, yadayim two hands; mayim, shamayim.",
  "Definite: ha- plus the noun, ha-melekh = the king. No word for 'a'.",
  "Present 'is' is not written: ha-ish tov means the man is good.",
  "Construct: bet melekh = house of a king; devar adonai = word of the LORD."],
 [T("Every Hebrew noun has a gender. Most nouns for males and many others are masculine; many feminine nouns end in -ah or -et, such as ahavah, love, and torah, teaching. The plural of a masculine noun is usually -im, so melekh, king, becomes melakhim, kings. Feminine nouns usually take -ot, so torah becomes torot. Natural pairs use the dual ending -ayim: yad is hand and yadayim is two hands. Mayim, water, and shamayim, heaven, only exist in this plural shape."),
  T("To say 'the', put ha- in front, and double the first letter of the noun when the sound allows: ha-melekh is the king and ha-aretz, the earth. To say 'a king', just say melekh. Hebrew has no indefinite article. The present tense of 'to be' is also usually omitted, so ha-melekh gadol is literally 'the king great', meaning 'the king is great'. This is called a nominal sentence. The Shema works this way: 'the LORD our God, the LORD one' says that the LORD is one."),
  T("Words are chained by the construct state. Put the possessed noun first, then the possessor: bet ha-melekh is the house of the king, and devar adonai is the word of the LORD. The first noun is often slightly shortened. Add a pronoun ending instead for 'my' or 'his': beti, my house; beto, his house; bit-kha, your house."),
  T("Small words attach to the front of a noun. Ve- means and. Be- means in or with, le- means to or for, and min or mi- means from. So be-reshit is in beginning, which opens Genesis. Another handy prefix is ha- for the article, so ba-bayit is in the house. Learn these as sounds first, then spot them at the start of words as you read."),
  T("The typical sentence order is verb, subject, object, which differs from English. In the first line of Genesis, bara elohim means created God. Adjectives follow their nouns and agree in gender and number: ish tov, a good man; ishah tovah, a good woman; anashim tovim, good men.")],
 [("What is the usual masculine plural ending?", ["-im", "-ot", "-ayim", "-ah"], 0, "Melekh, melakhim."),
  ("How do you say 'the' in Hebrew?", ["ha-", "ve-", "le-", "min"], 0, "A prefix."),
  ("How is 'a king' written?", ["Just melekh", "ha-melekh", "echad melekh only", "melekh-ha"], 0, "No indefinite article."),
  ("What does bet melekh mean?", ["House of a king", "King of the house", "The king's day", "A good king"], 0, "Construct chain."),
  ("What word order is typical in Hebrew?", ["Verb, subject, object", "Subject, verb, object", "Object first", "Verb last"], 0, "Bara elohim."),
  ("What does ve- mean?", ["and", "in", "from", "not"], 0, "As in vayomer.")],
 [("ha-", "the"), ("ve-", "and"), ("be-", "in"), ("le-", "to, for"), ("-im", "masculine plural ending"), ("-ot", "feminine plural ending")],
 [MATCH("Match the prefix to its meaning", "Pair each Hebrew prefix or word with its meaning.", [("ha-", "the"), ("ve-", "and"), ("be-", "in, with"), ("le-", "to, for"), ("min", "from")]),
  MATCH("Make it plural", "Pair each singular with its plural.", [("melekh", "melakhim"), ("yad", "yadayim"), ("ben", "banim"), ("ish", "anashim"), ("torah", "torot")]),
  FILL("Hebrew sentence rules", "Hebrew has no indefinite {{article}}. The verb 'to be' is usually {{omitted}} in the present. The usual order is verb, {{subject}}, object."),
  PL("Build the plural", "Write plural_he(word, gender): a transliterated Hebrew noun and 'm' or 'f'. Return word + 'im' for masculine; for feminine drop a final 'ah' and add 'ot' (torah gives torot), otherwise add 'ot'.", "plural_he(word, gender)", '''
def plural_he(word, gender):
    if gender == "m":
        return word + "im"
    if word.endswith("ah"):
        return word[:-2] + "ot"
    return word + "ot"
''', [["melekh", "m"], ["torah", "f"], ["ahavah", "f"], ["sefer", "m"], ["derekh", "m"]], "Use endswith and slicing.")]
))

# ---------------------------------------------------------------- 5
CHS.append(CH(
 "Hebrew grammar: verbs, roots and pronouns",
 ("Hebrew verbs", [
  "Root | has | Three consonants",
  "Pattern | adds | Vowels",
  "Perfect | shows | Completed action",
  "Imperfect | shows | Incomplete action",
  "Vav-consecutive | tells | A story",
  "Binyan | is | A verb stem",
  "Pronoun | attaches | To nouns and verbs"]),
 ["Hebrew verbs are built on roots of three consonants. Vowel patterns and prefixes turn the root into a tense or a stem. The two basic tenses are the perfect (completed) and the imperfect (incomplete).",
  "Seven stems, called binyanim, give the basic, intensive, causative and reflexive meanings of the same root. Pronoun endings attach to nouns (my, your) and to prepositions.",
  "The lab builds the perfect paradigm from a root in Python."],
 [("Root", "The three consonants that carry the core meaning of a word family."),
  ("Perfect", "A tense for completed actions, formed with suffixes; katav, he wrote."),
  ("Imperfect", "A tense for incomplete or future actions, formed with prefixes; yikhtov, he will write."),
  ("Binyan", "One of seven verb stems, such as Qal (simple), Piel (intensive), Hiphil (causative)."),
  ("Vav-consecutive", "A vav at the start of a verb that turns it into the next step of a story.")],
 ["Root k-t-v: katav wrote, ktav writing, mikhtav letter, sofer scribe.",
  "Perfect suffixes: -ti I, -ta you (m), - he, -ah she, -nu we, -u they.",
  "Imperfect prefixes: e- I, ti- you, yi- he, ni- we.",
  "Seven binyanim: Qal, Niphal, Piel, Pual, Hiphil, Hophal, Hitpael.",
  "Vayomer = and he said: vav plus imperfect tells a story in sequence.",
  "Pronouns: ani I, atah you, hu he, hi she, anachnu we, hem they."],
 [T("Hebrew vocabulary is easiest to see through roots. The three letters k-t-v give the sense of writing: katav, he wrote; ktav, writing; mikhtav, a letter; sofer, scribe (related). The root sh-m-r means guarding: shamar, he guarded; mishmar, a watch. The root sh-l-m gives shalom, peace, shalem, whole, and Shlomo, Solomon. Learning a root unlocks a whole family."),
  C("katavti   I wrote        katavnu   we wrote\nkatavta   you wrote (m)  ketavtem  you wrote (pl)\nkatavt    you wrote (f)\nkatav     he wrote        katvu     they wrote\nkatvah    she wrote", "text"),
  T("The perfect tense describes an action that is finished. You add a suffix to the stem: -ti for I, -ta for you, nothing for he, -ah for she, -nu for we, -u for they. Notice that the vowel in the stem shortens when a vowel suffix is added, so katav becomes katvah and katvu. The imperfect tense uses prefixes: ekhtov, I will write; tikhtov, you will write; yikhtov, he will write; nikhtov, we will write."),
  T("A Hebrew verb also has a stem, called a binyan. The basic one is the Qal: katav, he wrote. The Niphal is often passive, nikhtav, it was written. The Piel makes an intensive sense, so lamad, he learned, becomes limed, he taught. The Hiphil is causative: malakh, he reigned, becomes himlikh, he made king. The other three, Pual, Hophal and Hitpael, are passive and reflexive counterparts."),
  T("In stories the verb often begins with vav. Vayomer elohim means and God said. A vav joined to an imperfect form turns it into a past narrative: and he said, and he saw, and he went. This is the backbone of Genesis. The pronouns are ani, I; atah, you (m); at, you (f); hu, he; hi, she; anachnu, we; atem, you (pl); hem, they. They attach as endings: -i my, -kha your, -o his, -ah her, -enu our. So Elohenu is our God, from elohim and -enu.")],
 [("How many consonants does a Hebrew root usually have?", ["Three", "Two", "Four", "Five"], 0, "Like k-t-v."),
  ("What does the perfect tense express?", ["A completed action", "A command", "A question", "A wish"], 0, "Katav, he wrote."),
  ("What does the prefix yi- show?", ["He will (imperfect)", "I wrote", "They wrote", "A question"], 0, "Yikhtov."),
  ("What is a binyan?", ["A verb stem", "A noun ending", "A vowel", "A letter"], 0, "Seven in all."),
  ("What does vayomer mean?", ["And he said", "He will say", "Say!", "I say"], 0, "Vav plus imperfect."),
  ("What is the Hebrew for 'we'?", ["anachnu", "hem", "ani", "atah"], 0, "Sounds a little like 'a-nach-noo'.")],
 [("katav", "He wrote"), ("katvah", "She wrote"), ("katavti", "I wrote"), ("Qal", "The simple verb stem"), ("hem", "they")],
 [MATCH("Match the pronoun", "Pair each Hebrew pronoun with its meaning.", [("ani", "I"), ("atah", "you (m)"), ("hu", "he"), ("hi", "she"), ("anachnu", "we"), ("hem", "they")]),
  MATCH("Match the stem to its sense", "Pair the binyan with its usual meaning.", [("Qal", "simple action"), ("Niphal", "passive or reflexive"), ("Piel", "intensive"), ("Hiphil", "causative"), ("Hitpael", "reflexive")]),
  PL("The perfect of a root", "Write perfect_he(c1, c2, c3): given the three transliterated root letters, return the list [3ms, 3fs, 2ms, 1cs, 1cp, 3cp]: 3ms = c1+'a'+c2+'a'+c3; 3fs = c1+'a'+c2+c3+'ah'; 2ms = c1+'a'+c2+'a'+c3+'ta'; 1cs = c1+'a'+c2+'a'+c3+'ti'; 1cp = c1+'a'+c2+'a'+c3+'nu'; 3cp = c1+'a'+c2+c3+'u'. For katav this gives katav, katvah, katavta, katavti, katavnu, katvu.", "perfect_he(c1, c2, c3)", '''
def perfect_he(c1, c2, c3):
    base = c1 + "a" + c2 + "a" + c3
    short = c1 + "a" + c2 + c3
    return [base, short + "ah", base + "ta", base + "ti", base + "nu", short + "u"]
''', [["k", "t", "v"], ["sh", "m", "r"], ["z", "k", "r"], ["l", "m", "d"]], "Build the full stem and the shortened stem once, then add the endings."),
  FILL("Fill in the verb rules", "A Hebrew root usually has {{three}} consonants. The perfect uses {{suffixes}} and the imperfect uses prefixes. A vav at the start of a verb can make it a {{story}} verb.")]
))

# ---------------------------------------------------------------- 6
CHS.append(CH(
 "Greek: the alphabet and sounds",
 ("The Greek alphabet", [
  "Greek | has | 24 letters",
  "Letter | has | Capital and small",
  "Sigma | has | A final form",
  "Rough breathing | adds | An h sound",
  "Diphthong | joins | Two vowels",
  "Accent | marks | The stress",
  "Greek letters | are | Numbers"]),
 ["Greek has 24 letters, each with a capital and a small form, and it reads left to right. You already know many of them from mathematics: alpha, beta, pi, sigma, omega.",
  "Words that begin with a vowel carry a breathing mark: smooth (no h) or rough (an h sound). Marks above the word show stress and are learned with each word. Diphthongs like ou and ai give single sounds.",
  "The labs match letters and compute isopsephy, the Greek counterpart of gematria."],
 [("Breathing mark", "A sign over an initial vowel: rough (h) or smooth (no h)."),
  ("Diphthong", "Two vowels pronounced as one sound, like ai or ou."),
  ("Final sigma", "The form ς used for sigma at the end of a word."),
  ("Accent", "A mark (acute, grave or circumflex) showing which syllable is stressed."),
  ("Isopsephy", "Adding the number values of the Greek letters in a word.")],
 ["24 letters: alpha to omega, left to right.",
  "Final sigma ς appears only at the end of a word.",
  "Rough breathing ῾ means an h before the vowel; smooth ᾿ means none.",
  "Diphthongs: ai, ei, oi, au, eu, ou.",
  "Gamma before gamma, kappa, xi or chi sounds like n: aggelos is angelos.",
  "Every word of two or more syllables carries an accent."],
 [T("The Greek alphabet came from the Phoenician alphabet, the same family as Hebrew, but Greek added letters for vowels. It has 24 letters: alpha, beta, gamma, delta, epsilon, zeta, eta, theta, iota, kappa, lambda, mu, nu, xi, omicron, pi, rho, sigma, tau, upsilon, phi, chi, psi and omega. Each has a capital and a small form. Most capitals look like English letters, but beware Rho, which looks like P and sounds like r, and Eta, like H but sounding like ay."),
  C("Α α alpha a    | Β β beta b     | Γ γ gamma g   | Δ δ delta d\nΕ ε epsilon e  | Ζ ζ zeta z     | Η η eta e(ay) | Θ θ theta th\nΙ ι iota i     | Κ κ kappa k    | Λ λ lambda l  | Μ μ mu m\nΝ ν nu n       | Ξ ξ xi x       | Ο ο omicron o | Π π pi p\nΡ ρ rho r      | Σ σ ς sigma s  | Τ τ tau t     | Υ υ upsilon u(y)\nΦ φ phi ph     | Χ χ chi kh     | Ψ ψ psi ps    | Ω ω omega o(long)", "text"),
  T("Some sounds need two letters in English. Theta is th, phi is ph or f, chi is kh as in Scottish loch, and psi is ps. The letter sigma has two small shapes: σ in the middle of a word and ς at the end, as in λόγος. Gamma before another gamma, kappa, xi or chi sounds like n, so ἄγγελος, messenger, is angelos, the source of our word angel."),
  T("A word that starts with a vowel carries a breathing mark. The rough breathing, which looks like a small backwards comma, adds an h sound: ὁ is ho, and ἡμέρα is hemera. The smooth breathing, like a small comma, adds nothing. A word starting with rho always takes a rough breathing, giving the sound rh. Some vowel pairs, the diphthongs, are one sound: αι as in 'aisle', ει as in 'eight', οι as in 'oil', αυ as in 'cow', ευ as in 'eh-oo' and ου as in 'soup'."),
  T("Accents are three little marks: acute ´, grave ` and circumflex ˜. They record where the stress falls. Beginners do not need to master the rules yet; learn each word with its accents, as you would the spelling of an English word. Greek letters also serve as numbers: alpha is 1, beta 2, up to iota 10, then kappa 20, and so on to omega 800. The isopsephy lab adds up a word's letters, like gematria in Hebrew.")],
 [("How many letters are in the Greek alphabet?", ["24", "22", "26", "28"], 0, "Alpha to omega."),
  ("What does a rough breathing add?", ["An h sound", "A stress", "Nothing", "A long vowel"], 0, "As in ho and hemera."),
  ("Where does the final sigma ς appear?", ["At the end of a word", "At the start", "Only in names", "Never"], 0, "Logos ends with ς."),
  ("How does the letter chi sound?", ["kh", "ch as in church", "s", "x"], 0, "Like Scottish loch."),
  ("What is a diphthong?", ["Two vowels making one sound", "A breathing mark", "A capital", "A number"], 0, "Ou, ai, ei."),
  ("Which Greek letter looks like P but sounds r?", ["Rho", "Pi", "Psi", "Phi"], 0, "Rho.")],
 [("α β γ δ", "alpha, beta, gamma, delta"), ("ς", "Final sigma"), ("ου", "The diphthong oo"), ("ἡ", "he (rough breathing: h)"), ("ρ", "Rho: r (looks like p)")],
 [MATCH("Match the Greek letter to its name", "Small letters to names.", [("α", "alpha"), ("β", "beta"), ("γ", "gamma"), ("δ", "delta"), ("θ", "theta"), ("λ", "lambda"), ("π", "pi"), ("ω", "omega")]),
  MATCH("Read the Greek word", "Match each Greek word with how it sounds.", [("θεός", "theos"), ("λόγος", "logos"), ("κύριος", "kyrios"), ("ἀγάπη", "agape"), ("εἰρήνη", "eirene")]),
  PL("Isopsephy", "Write isopsephy(word) for a lowercase Greek word without accents: alpha 1, beta 2, gamma 3, delta 4, epsilon 5, zeta 7, eta 8, theta 9, iota 10, kappa 20, lambda 30, mu 40, nu 50, xi 60, omicron 70, pi 80, rho 100, sigma and final sigma 200, tau 300, upsilon 400, phi 500, chi 600, psi 700, omega 800. Return the sum.", "isopsephy(word)", '''
def isopsephy(word):
    v = {"α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5, "ζ": 7, "η": 8, "θ": 9, "ι": 10, "κ": 20, "λ": 30, "μ": 40, "ν": 50, "ξ": 60, "ο": 70, "π": 80, "ρ": 100, "σ": 200, "ς": 200, "τ": 300, "υ": 400, "φ": 500, "χ": 600, "ψ": 700, "ω": 800}
    t = 0
    for ch in word:
        t += v.get(ch, 0)
    return t
''', [["λογος"], ["θεος"], ["αγαπη"], ["ζωη"], ["φως"], ["ιησους"]], "A dictionary lookup per letter, summed.")]
))

# ---------------------------------------------------------------- 7
CHS.append(CH(
 "Greek grammar: nouns, articles and cases",
 ("Greek nouns", [
  "Noun | has | A case",
  "Nominative | is | The subject",
  "Accusative | is | The object",
  "Genitive | means | Of",
  "Dative | means | To or for",
  "Article | changes | With the noun",
  "Preposition | takes | A case"]),
 ["Greek nouns have gender (masculine, feminine, neuter), number and one of five cases. The case, not the position, shows the role: nominative for the subject, accusative for the object, genitive for 'of', dative for 'to or for' and vocative for calling out.",
  "The article (the) changes with the noun, and it agrees in gender, number and case. Prepositions take certain cases, and the case changes the meaning.",
  "The labs match case to function and build the endings of a typical noun."],
 [("Case", "The form of a noun that shows its job in the sentence."),
  ("Nominative", "The case of the subject."),
  ("Genitive", "The case showing possession or 'of'."),
  ("Dative", "The case of the indirect object: to, for, in, by."),
  ("Accusative", "The case of the direct object."),
  ("Vocative", "The case used to address someone.")],
 ["Five cases: nominative, genitive, dative, accusative, vocative.",
  "Article (nominative): ho masculine, he feminine, to neuter; ton, ten, to in the accusative.",
  "Second declension masculine: logos, logou, logo, logon.",
  "First declension feminine: agape, agapes, agape, agapen.",
  "Plural nominative: logoi, agapai.",
  "Word order is flexible because endings show roles."],
 [T("In English, 'the dog bites the man' and 'the man bites the dog' differ only by word order. In Greek, the endings show who bites whom. The subject takes the nominative, the object the accusative. In the sentence ho theos agapa ton kosmon, God loves the world, ho theos, God, is nominative and ton kosmon, the world, is accusative. You could shuffle the words and the meaning would not change."),
  C("            masc    fem    neut\nnominative   ho      he     to\ngenitive     tou     tes    tou\ndative       to      te     to\naccusative   ton     ten    to", "text"),
  T("The article changes in the same way, and it tells you the gender, number and case at a glance. A typical masculine noun of the second declension is logos, word. Its singular is logos (nominative), logou (genitive, of the word), logo (dative, to the word) and logon (accusative), and its vocative is loge. The plural is logoi, logon, logois and logous. A typical feminine noun of the first declension is agape, love: agape, agapes, agape, agapen. The plural begins agapai."),
  C("logos   word (sg)     logoi    words (pl)\nlogou   of the word    logon    of the words\nlogo    to the word    logois   to the words\nlogon   the word (obj) logous   the words (obj)", "text"),
  T("The cases cover a wide range of meanings. The genitive is of, so tou theou is of God. The dative is to, for, in or by, so to logo is by the word. The accusative is the object, and also direction, so pros ton theon is toward God. Prepositions take certain cases, and the case alters the sense: dia with the genitive is through, but with the accusative it is because of. Learn each preposition with its case.")],
 [("Which case marks the subject?", ["Nominative", "Accusative", "Genitive", "Dative"], 0, "The doer."),
  ("Which case is the object?", ["Accusative", "Nominative", "Genitive", "Vocative"], 0, "Ton kosmon."),
  ("What does the genitive show?", ["Possession, 'of'", "The subject", "Calling out", "The object"], 0, "Tou theou, of God."),
  ("What is the accusative singular of logos?", ["logon", "logou", "logo", "logoi"], 0, "Add -on."),
  ("The article agrees with the noun in...", ["Gender, number and case", "Gender only", "Tense", "Voice"], 0, "Always three things."),
  ("What does the vocative do?", ["Addresses someone", "Marks the subject", "Marks the object", "Marks possession"], 0, "Kyrie, Lord!")],
 [("Nominative", "Subject"), ("Genitive", "Of"), ("Dative", "To, for, in, by"), ("Accusative", "Object"), ("logos / logon", "word / the word (obj)")],
 [MATCH("Match case to function", "Pair each Greek case with what it does.", [("Nominative", "the subject"), ("Genitive", "possession, of"), ("Dative", "to, for, by"), ("Accusative", "the object"), ("Vocative", "addressing someone")]),
  MATCH("Match the form", "Pair each form of logos with its role.", [("λόγος", "nominative singular"), ("λόγου", "genitive singular"), ("λόγῳ", "dative singular"), ("λόγον", "accusative singular"), ("λόγοι", "nominative plural")]),
  FILL("Fill in the rules", "The {{nominative}} marks the subject and the accusative marks the {{object}}. The {{genitive}} means 'of'. Word order is flexible because {{endings}} show the role."),
  PL("Decline a second declension noun", "Write decline_os(stem): for a masculine second declension noun like λόγος given its stem λογ, return [nom sg, gen sg, dat sg, acc sg, nom pl, gen pl, dat pl, acc pl] as stem plus ος, ου, ω, ον, οι, ων, οις, ους (no accents).", "decline_os(stem)", '''
def decline_os(stem):
    ends = ["ος", "ου", "ω", "ον", "οι", "ων", "οις", "ους"]
    return [stem + e for e in ends]
''', [["λογ"], ["ανθρωπ"], ["θε"], ["οικ"]], "Make a list of endings and add each to the stem.")]
))

# ---------------------------------------------------------------- 8
CHS.append(CH(
 "Greek grammar: verbs",
 ("Greek verbs", [
  "Verb | has | Tense",
  "Verb | has | Voice",
  "Verb | has | Mood",
  "Present | shows | Ongoing action",
  "Aorist | shows | A simple event",
  "Augment | marks | The past",
  "Participle | acts | As verb and adjective"]),
 ["A Greek verb shows tense, voice, mood, person and number. Tense in Greek is as much about the kind of action (ongoing, simple, completed) as about time.",
  "The regular present active has endings -ō, -eis, -ei, -omen, -ete, -ousi. Past tenses add an augment (e-) at the front. Voice can be active, middle or passive. The verb 'to be' is irregular.",
  "The lab conjugates the present of regular verbs."],
 [("Tense", "When or how an action takes place: present, imperfect, future, aorist, perfect."),
  ("Aorist", "A past tense for a simple, single event."),
  ("Voice", "Whether the subject acts (active), acts on itself (middle), or is acted on (passive)."),
  ("Mood", "The way a statement is made: indicative, subjunctive, optative, imperative."),
  ("Augment", "An e- added to the front of a past-tense indicative verb."),
  ("Participle", "A verb form that works like an adjective, such as 'loving'.")],
 ["Present active of luo: luo, lueis, luei, luomen, luete, luousi.",
  "Imperfect: eluon, ongoing past; aorist: eluse, simple past.",
  "Future: luso; perfect: leluka, a past act with present result.",
  "Voices: active, middle, passive. Moods: indicative, subjunctive, optative, imperative.",
  "Eimi, to be: eimi, ei, esti, esmen, este, eisi.",
  "The verb form shows the person, so the subject pronoun is often left out."],
 [T("Greek verbs are rich, but their core is regular. We learn them on a model verb, luo, which means loose or release. Remove the ending -o to find the stem lu-. The present active indicative adds -o for I, -eis for you, -ei for he or she, -omen for we, -ete for you all and -ousi for they. So luo is I loose, lueis you loose, luei he looses, luomen we loose, luete you loose and luousi they loose."),
  C("luo    I loose        luomen  we loose\nlueis  you loose      luete   you (pl) loose\nluei   he looses      luousi  they loose", "text"),
  T("Because the ending shows the person, the pronoun is usually left out: agapo se means I love you, with the pronoun se (you) as the object. Tense in Greek is about the kind of action. The present means ongoing or repeated, the aorist is a simple event, and the perfect is a finished action with lasting results. In the indicative, past tenses add an augment, a small e- in front of the stem: eluon (imperfect, I was loosing) and eluse (aorist, he loosed). The future adds -s-: luso, I will loose."),
  T("Voice shows the relationship between the subject and the action. In the active voice the subject acts: luo, I loose. In the passive the subject receives it: luomai, I am being loosed. In the middle voice, found in Greek and not in English, the subject acts on or for itself: luomai can also mean I loose for myself. The moods include the indicative for facts, the subjunctive for possibilities, the optative for wishes and the imperative for commands, as in luson, loose!"),
  T("The verb to be, eimi, is irregular and very frequent: eimi, I am; ei, you are; esti(n), he or she is; esmen, we are; este, you are; eisi(n), they are. We have seen it in John 1:1 as en, was, and in 1 John 4:8, ho theos agape estin. Participles, such as agapon, loving, act as both verbs and adjectives and are the most common way of building longer sentences in the New Testament.")],
 [("What does the aorist usually express?", ["A simple event", "Ongoing action", "A command", "A wish"], 0, "Eluse."),
  ("What is the 'I' form of the regular present?", ["-o", "-eis", "-ei", "-ete"], 0, "Luo."),
  ("What is an augment?", ["An e- added to past tenses", "An ending", "A breathing", "A case"], 0, "Eluon."),
  ("Which voice has the subject receive the action?", ["Passive", "Active", "Middle only", "Subjunctive"], 0, "Luomai, I am loosed."),
  ("What is 'they are' in Greek?", ["eisi(n)", "esmen", "este", "ei"], 0, "From eimi."),
  ("Why is the pronoun often left out?", ["The ending shows the person", "It does not exist", "It is rude", "It is replaced by the article"], 0, "Agapo means I love.")],
 [("luo", "I loose"), ("agapas", "you love"), ("eimi", "I am"), ("aorist", "A simple past event"), ("middle voice", "Subject acts for itself")],
 [MATCH("Match the form to its person", "Pair each form of luo with its meaning.", [("λύω", "I loose"), ("λύεις", "you loose"), ("λύει", "he looses"), ("λύομεν", "we loose"), ("λύετε", "you all loose"), ("λύουσι", "they loose")]),
  MATCH("Match tense to its sense", "Pair each Greek tense with its main idea.", [("Present", "ongoing action"), ("Imperfect", "ongoing past action"), ("Aorist", "a simple event"), ("Perfect", "done, with a lasting result"), ("Future", "will happen")]),
  PL("Conjugate the present", "Write present_omega(verb): for a Greek verb ending in ω (no accents), return the six present active forms: stem + ω, εις, ει, ομεν, ετε, ουσιν, where stem is the verb without its final ω.", "present_omega(verb)", '''
def present_omega(verb):
    stem = verb[:-1]
    ends = ["ω", "εις", "ει", "ομεν", "ετε", "ουσιν"]
    return [stem + e for e in ends]
''', [["λυω"], ["λεγω"], ["γραφω"], ["ακουω"]], "Strip the last letter, then add six endings."),
  FILL("Greek verb rules", "The present active ending for 'I' is {{ω}}. Past tenses add an {{augment}}. A verb that acts on or for itself is in the {{middle}} voice.")]
))
