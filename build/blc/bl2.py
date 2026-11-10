# -*- coding: utf-8 -*-
"""Bible languages, part 2: Latin, comparison, vocabulary, phrases, reading, memory."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clib import *
from data import NOUNS, VERBS, PHRASES
from bl1 import APP

CHS = []

# ---------------------------------------------------------------- 9
CHS.append(CH(
 "Latin: sounds, nouns and cases",
 ("Latin nouns", [
  "Latin | has | No articles",
  "Noun | has | Gender",
  "Noun | has | Six cases",
  "Noun | has | Five declensions",
  "Ending | shows | The role",
  "Adjective | agrees | With its noun",
  "Preposition | takes | Accusative or ablative"]),
 ["Latin uses the same letters as English, so you can start reading at once. The Church pronounces them softly (ci as chi) and the classical way is harder (ci as ki); this course uses the Church reading. Latin has no word for 'the' or 'a'.",
  "Nouns have gender and number and six cases: nominative, genitive, dative, accusative, ablative and vocative. Five declensions group the nouns by their endings. Adjectives agree with their noun in gender, number and case. The verb tends to come last.",
  "The labs decline the first declension and match cases to their functions."],
 [("Declension", "A group of nouns that share the same set of case endings."),
  ("Ablative", "A case for by, with, from or in; the 'by means of' case."),
  ("Ecclesiastical Latin", "The pronunciation used in the Church, close to Italian."),
  ("Agreement", "Adjectives match their noun's gender, number and case."),
  ("Stem", "The part of the word that stays the same when endings change.")],
 ["Church sounds: c before e or i is 'ch'; ae and oe are 'e'; gn is 'ny'; j and i are 'y'.",
  "No articles: puella means girl, a girl or the girl.",
  "Six cases: nom, gen, dat, acc, abl, voc.",
  "First declension (puella): -a -ae -ae -am -a; plural -ae -arum -is -as -is.",
  "Second declension (dominus): -us -i -o -um -o; voc -e.",
  "Stress: the next-to-last syllable if it is long or closed, otherwise the one before it."],
 [T("Latin looks easy, because its alphabet is yours. There are 23 letters, without j, u and w, which came later. Pronunciation has two traditions. Classical Latin, as Caesar spoke it, says c as k, v as w, and ae as in 'eye'. Church Latin, used in the Vulgate readings and hymns, says ci as chi, ce as che, v as v and ae as e. Church Latin sounds close to Italian. We use it here: Caelum is chay-lum, Deus is day-oos, and Pax Vobiscum is pahks vo-bees-kum."),
  T("Stress is predictable. In a word of two syllables, stress the first: Do-mi-nus has three, so look at the next-to-last. If that syllable is long (a long vowel, or a vowel followed by two consonants), stress it. Otherwise stress the one before it. So do-MI-nus, since the i is long, but A-ni-ma, with a short i."),
  T("Nouns have six cases, as in Greek (plus the ablative). The nominative is the subject, the genitive means 'of', the dative 'to or for', the accusative is the object, the ablative 'by, with, from, in' and the vocative is for calling. The first declension has endings -a, -ae, -ae, -am, -a. So puella, girl, goes: puella (nom), puellae (of the girl), puellae (to the girl), puellam (the girl as object), puella (by the girl). The plural is puellae, puellarum, puellis, puellas, puellis."),
  C("1st decl.      puella    2nd decl.     dominus    3rd decl.    rex\nnom           puella              dominus               rex\ngen           puellae             domini                regis\ndat           puellae             domino                regi\nacc           puellam             dominum               regem\nabl           puella              domino                rege\nvoc           puella              domine                rex", "text"),
  T("The second declension masculine, dominus, has -us, -i, -o, -um, -o. Its vocative is domine, as in Kyrie and Domine, Lord. The third declension is the largest and takes -is for the genitive: rex, regis, king. Adjectives take the same endings and match their noun: Deus bonus, a good God; filia bona, a good daughter; verbum bonum, a good word. Prepositions take the accusative (ad, to; in, into; per, through) or the ablative (in, in; cum, with; de, about; ex, from). Latin has no articles, and the word order is flexible: Deus creavit caelum and caelum creavit Deus both mean that God created heaven.")],
 [("How many cases does Latin have?", ["Six", "Four", "Five", "Eight"], 0, "With the ablative and vocative."),
  ("How do you say 'the' in Latin?", ["There is no article", "ille always", "hic always", "ut"], 0, "Context supplies it."),
  ("In Church Latin, how is ce said?", ["che", "ke", "se", "ze"], 0, "Caelum: chay-lum."),
  ("Which case is the object?", ["Accusative", "Nominative", "Ablative", "Genitive"], 0, "Puellam."),
  ("What is the genitive singular of puella?", ["puellae", "puellam", "puella", "puellis"], 0, "First declension."),
  ("Which case follows 'cum' (with)?", ["Ablative", "Accusative", "Genitive", "Nominative"], 0, "Cum Deo.")],
 [("puella", "girl, first declension"), ("dominus", "lord, second declension"), ("rex, regis", "king, third declension"), ("-ae", "genitive singular of the first declension"), ("ablative", "by, with, from")],
 [MATCH("Match case to function", "Pair each Latin case with its main job.", [("Nominative", "the subject"), ("Genitive", "of"), ("Dative", "to or for"), ("Accusative", "the object"), ("Ablative", "by, with, from"), ("Vocative", "addressing")]),
  MATCH("Match the form of puella", "Pair each form with its case and number.", [("puella", "nominative singular"), ("puellae", "genitive singular"), ("puellam", "accusative singular"), ("puellarum", "genitive plural"), ("puellas", "accusative plural")]),
  FILL("Latin rules", "Latin has no {{articles}}. The ending shows the {{case}}. An adjective must agree with its {{noun}}."),
  PL("Decline the first declension", "Write decline_first(noun): for a first-declension noun in the nominative singular like puella, return [nom sg, gen sg, dat sg, acc sg, abl sg, nom pl, gen pl, dat pl, acc pl, abl pl]. The stem is the noun without its final a. Endings: a, ae, ae, am, a, ae, arum, is, as, is.", "decline_first(noun)", '''
def decline_first(noun):
    stem = noun[:-1]
    ends = ["a", "ae", "ae", "am", "a", "ae", "arum", "is", "as", "is"]
    return [stem + e for e in ends]
''', [["puella"], ["rosa"], ["terra"], ["vita"]], "Cut the final a, then add ten endings.")]
))

# ---------------------------------------------------------------- 10
CHS.append(CH(
 "Latin grammar: verbs",
 ("Latin verbs", [
  "Verb | has | Four conjugations",
  "Verb | has | Principal parts",
  "Present | uses | Personal endings",
  "Perfect | shows | A completed act",
  "Sum | is | To be",
  "Verb | goes | Last",
  "Imperative | gives | A command"]),
 ["Latin verbs belong to four conjugations, told apart by the vowel before -re in the infinitive: amare, monere, regere, audire. Personal endings -o, -s, -t, -mus, -tis, -nt show the person, so the pronoun is not needed.",
  "Each verb is listed with four principal parts from which every form can be built. The tenses include the present, imperfect, future and perfect. The verb sum, to be, is irregular and common.",
  "The lab conjugates a first-conjugation verb in Python."],
 [("Conjugation", "A group of verbs sharing the same pattern of endings."),
  ("Principal parts", "Four forms listed in the dictionary, from which all others are built."),
  ("Infinitive", "The 'to' form: amare, to love."),
  ("Imperfect", "A past tense for ongoing action: amabat, he was loving."),
  ("Perfect", "A past tense for a completed act: amavit, he loved.")],
 ["Present of amo: amo, amas, amat, amamus, amatis, amant.",
  "Four conjugations: amare, monere, regere, audire.",
  "Sum: sum, es, est, sumus, estis, sunt; imperfect eram, erat; perfect fui.",
  "Perfect endings: -i, -isti, -it, -imus, -istis, -erunt.",
  "Principal parts of amo: amo, amare, amavi, amatum.",
  "Imperative: ama! (love!), audi! (hear!)."],
 [T("A Latin verb contains a lot in one word. Amamus means we love. The ending -mus says we, so no pronoun is needed. The four conjugations differ by the vowel in the infinitive. The first is -are, as in amare, to love. The second is -ere with a long e, as in monere, to warn. The third is -ere with a short e, as in regere, to rule. The fourth is -ire, as in audire, to hear. Each takes the same personal endings."),
  C("amo      I love         amamus   we love\namas     you love       amatis   you (pl) love\namat     he/she loves   amant    they love", "text"),
  T("The personal endings are -o or -m for I, -s for you, -t for he or she, -mus for we, -tis for you all and -nt for they. The vowel before them depends on the conjugation: amas, mones, regis, audis. The verb is listed in a dictionary by four principal parts: amo (I love), amare (to love), amavi (I loved) and amatum (loved). From these you can build every form. The perfect uses its own endings: amavi, amavisti, amavit, amavimus, amavistis, amaverunt."),
  T("The verb sum, to be, is irregular: sum, es, est, sumus, estis, sunt. The imperfect is eram, eras, erat and the perfect fui, fuisti, fuit. It appears in John 1:1 as erat: in principio erat Verbum, in the beginning was the Word. Latin puts the verb at the end of the clause more often than not: Deus caelum creavit, God heaven created. The Vulgate often follows the Greek order, though, so the verb sometimes comes earlier."),
  T("The imperative gives commands. The singular is the stem: ama, love! audi, hear! as in the Shema, Audi, Israel. Add -te for the plural: amate, audite. The passive voice has its own endings, such as amatur, he is loved. The passive explains forms in the Bible like facta est, was made. Participles and the subjunctive come later, but even now you can read simple verse once you know the person endings and sum.")],
 [("What is the 'we' ending in the present?", ["-mus", "-tis", "-nt", "-s"], 0, "Amamus."),
  ("What is the infinitive of 'to hear'?", ["audire", "amare", "monere", "regere"], 0, "Fourth conjugation."),
  ("How is 'he is' written?", ["est", "es", "sunt", "sum"], 0, "From sum."),
  ("What does amavit mean?", ["He loved", "He loves", "He will love", "Love!"], 0, "Perfect."),
  ("What is the imperative singular of audire?", ["audi", "audite", "audit", "audis"], 0, "Audi, Israel."),
  ("Where does the verb often go in Latin?", ["At the end", "At the start", "Always second", "In the middle"], 0, "SOV.")],
 [("amo, amare", "I love, to love"), ("sum, esse", "I am, to be"), ("amavi", "I loved"), ("-nt", "they (ending)"), ("audi!", "hear!")],
 [MATCH("Match the form to the person", "Pair each form of amo with its meaning.", [("amo", "I love"), ("amas", "you love"), ("amat", "he loves"), ("amamus", "we love"), ("amatis", "you all love"), ("amant", "they love")]),
  MATCH("Match the form of sum", "Pair the form with its meaning.", [("sum", "I am"), ("es", "you are"), ("est", "he is"), ("sumus", "we are"), ("sunt", "they are")]),
  PL("Conjugate the present", "Write conjugate_first(verb): given a first-conjugation verb in the form amo (first person), return the six present forms: stem + o, as, at, amus, atis, ant, where stem is the verb without its final o. For amo that is amo, amas, amat, amamus, amatis, amant.", "conjugate_first(verb)", '''
def conjugate_first(verb):
    stem = verb[:-1]
    return [stem + "o", stem + "as", stem + "at", stem + "amus", stem + "atis", stem + "ant"]
''', [["amo"], ["laudo"], ["porto"], ["voco"]], "Take the stem by cutting the o, then add the endings."),
  PL("Roman numerals", "Write roman_to_int(s) for Roman numerals I V X L C D M. When a smaller numeral comes before a larger, subtract it (IV is 4, XC is 90).", "roman_to_int(s)", '''
def roman_to_int(s):
    v = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, ch in enumerate(s):
        n = v[ch]
        if i + 1 < len(s) and v[s[i + 1]] > n:
            total -= n
        else:
            total += n
    return total
''', [["III"], ["IV"], ["IX"], ["XLII"], ["MCMXCIV"], ["MMXXVI"]], "Subtract a numeral if the next one is bigger.")]
))

# ---------------------------------------------------------------- 11
CHS.append(CH(
 "Comparing the three: pronouns, numbers and 'to be'",
 ("Side by side", [
  "Hebrew | omits | Present is",
  "Greek | uses | Eimi",
  "Latin | uses | Sum",
  "Greek | has | The article",
  "Latin | has | No article",
  "Hebrew | has | Prefix ha",
  "Numbers | differ | In each language"]),
 ["The same ideas are expressed in different ways in the three languages. This chapter lays them side by side: pronouns, numbers 1 to 10, the verb 'to be', questions and negatives.",
  "Hebrew has one article and no case endings, Greek has an article and five cases, and Latin has no article and six cases. Seeing the contrasts makes each language easier to remember.",
  "The labs ask you to match the same word across the three languages."],
 [("Pronoun", "A word like I or you that stands for a noun."),
  ("Negative", "A word that denies: lo, ou, non."),
  ("Numeral", "A number word."),
  ("Article", "Hebrew ha-, Greek ho/he/to; Latin has none."),
  ("Copula", "The linking verb 'to be'.")],
 ["I: ani, ego, ego; you: atah, su, tu; we: anachnu, hemeis, nos.",
  "To be: Hebrew leaves it out in the present, Greek eimi, Latin sum.",
  "No/not: lo, ou(k) or me, non.",
  "Question words: who mi, tis, quis; what mah, ti, quid; where eifo, pou, ubi.",
  "Numbers 1 to 10 side by side are below.",
  "An article tells definiteness; Latin relies on context."],
 [T("Seeing the three side by side shows both the differences and the surprising family ties. The English 'I' is ego in both Greek and Latin, as in 'ego' in English. Hebrew uses ani. 'You' is atah (masculine, singular) in Hebrew, su in Greek and tu in Latin. Notice that Greek su and Latin tu are close cousins, while Hebrew uses a different root. 'We' is anachnu, hemeis and nos."),
  C("English   Hebrew      Greek        Latin\nI         ani          ego          ego\nyou       atah         su           tu\nhe        hu           autos        is / ille\nwe        anachnu      hemeis       nos\nthey      hem          autoi        illi\nnot       lo           ou(k)        non", "text"),
  T("The verb 'to be' behaves differently. In Hebrew, the present is simply left out, so 'the man good' is the man is good. Greek uses eimi (I am) and Latin uses sum. In the past, hayah (Hebrew), en (Greek, from eimi) and erat (Latin) all mean was. Note the match in John 1:1: Greek en ho logos and Latin erat Verbum. The articles also differ. Hebrew attaches ha- to a noun. Greek has ho, he, to. Latin has no article, so Verbum is a Word, the Word or simply Word, depending on context."),
  C("number  Hebrew      Greek    Latin\n1       echad        heis     unus\n2       shtayim      dyo      duo\n3       shalosh      treis    tres\n4       arba         tessares quattuor\n5       chamesh      pente    quinque\n6       shesh        hex      sex\n7       sheva        hepta    septem\n8       shmone       okto     octo\n9       tesha        ennea    novem\n10      eser         deka     decem", "text"),
  T("Look for the cognates. Greek hex and Latin sex both give six, and hepta and septem give seven. English took octagon and octopus from okto and octo, while December, the tenth month in the old calendar, comes from decem. The Hebrew numbers belong to the Semitic family and look quite different, but shesh, six, and sheva, seven, are close to the Arabic sitta and sab'a. The question words follow: mi, tis, quis (who); mah, ti, quid (what); eifo, pou, ubi (where). In Latin, quis and quid are the roots of the English words quiz and quiddity.")],
 [("How is 'I' said in Greek and Latin?", ["ego in both", "su and tu", "ani and ego", "nos and hemeis"], 0, "A shared root."),
  ("What does Hebrew do with the present 'is'?", ["Leaves it out", "Uses hayah", "Uses eimi", "Uses sum"], 0, "Nominal sentence."),
  ("What is Latin for 'six'?", ["sex", "septem", "octo", "decem"], 0, "Same as Greek hex."),
  ("Which has no article?", ["Latin", "Greek", "Hebrew", "All have one"], 0, "Verbum."),
  ("What is 'who' in Latin?", ["quis", "mi", "tis", "quid"], 0, "Quiz."),
  ("What does 'lo' mean?", ["not, no", "and", "to", "with"], 0, "Hebrew negative.")],
 [("ego", "I (Greek and Latin)"), ("ani", "I (Hebrew)"), ("lo / ou / non", "not"), ("mi / tis / quis", "who"), ("shesh / hex / sex", "six")],
 [MATCH("Match the pronoun", "English to Latin.", [("I", "ego"), ("you", "tu"), ("we", "nos"), ("he/she/it", "is"), ("they", "illi")]),
  MATCH("Match the numbers", "Pair Greek numbers with Latin numbers.", [("heis", "unus"), ("dyo", "duo"), ("treis", "tres"), ("pente", "quinque"), ("hex", "sex"), ("deka", "decem")]),
  MATCH("Match the question words", "English to Hebrew.", [("who", "mi"), ("what", "mah"), ("where", "eifo"), ("not", "lo"), ("and", "ve-")]),
  FILL("To be", "Hebrew {{omits}} the present 'is'. Greek uses {{eimi}} and Latin uses {{sum}}.")]
))

# ---------------------------------------------------------------- 12
def triple_labs(rows, n_start, n_end, title):
    return MATCH(title, "Match each English word to its Latin form; then learn the Greek and Hebrew from the flashcards.", [(r[0], r[5]) for r in rows[n_start:n_end]])

CHS.append(CH(
 "Core vocabulary I: nouns in three languages",
 ("Core nouns", [
  "Word | has | A hook",
  "Hook | links | An English word",
  "Cognate | helps | Memory",
  "Flashcards | use | Leitner boxes",
  "Direction | can | Reverse",
  "Short sessions | beat | Long ones"]),
 ["Thirty common nouns, each in Hebrew, Greek and Latin, with a memory hook. Many of them became English words through Greek and Latin, which makes them easy to remember.",
  "The flashcard lab uses Leitner boxes: you move up a box when you know a card and back to box 1 when you miss it. You can choose any direction, such as English to Hebrew or Greek to Latin, so that you can translate between the languages directly.",
  "Three matching labs drill the words in groups."],
 [("Hook", "A link between a new word and something you already know."),
  ("Leitner box", "A level in a spaced-repetition system; the higher the box, the longer you wait."),
  ("Loanword", "A word copied from another language, like amen or hallelujah."),
  ("Derivative", "An English word built from a Greek or Latin one, like theology."),
  ("Recall", "Retrieving a word from memory without looking.")],
 ["Learn 5 words at a time and revisit them tomorrow.",
  "Say each word aloud with its English hook.",
  "Greek and Latin give English hundreds of words; Hebrew gives shalom, amen, sabbath.",
  "Reverse the direction once you know a card.",
  "Review every day, a little, instead of once a week for a long time."],
 [T("The nouns in this list are the core of the Bible's vocabulary: God, Lord, man, woman, father, mother, son, day, night, light, water, earth, heaven, word, love, life, death, king, house, peace, spirit, name, people, hand, heart, truth, bread, city, sin and book. For each one you get the Hebrew, the Greek and the Latin with a short hook. Learn them in groups of five, and say the three forms together, aloud."),
  T("Here are some memory stories. Light: Greek phos gives us photo, a picture made from light, and Latin lux gives lucid. Peace: Latin pax gives pacify and Pacific, the peaceful ocean, and the Hebrew shalom has a close Arabic cousin, salaam. Bread: Latin panis gives pantry, and the Hebrew lechem hides in Bethlehem, house of bread. Heart: Greek kardia is cardiac and Latin cor is cordial and core. Word: Greek logos gives logic and dialogue, Latin verbum gives verb and verbal."),
  T("The first group is God, Lord, man, woman, father. The Greek theos gives theology and the Latin Deus gives deity. The Greek anthropos gives anthropology; the Latin homo gives human. The Greek pater and Latin pater are twins; both give paternal. The Hebrew av is the same as the Aramaic abba. The second group is mother, son, day, night, light. Greek meter and Latin mater share a root with English mother. Notice that Greek and Latin words often resemble English words in the same family, but Hebrew words need the repetition and the story."),
  T("Use the flashcards every day. The deck is chosen at the top, as are the two languages: pick English and Hebrew, then flip it to Hebrew and English. Missing a card sends it back to box 1, where you see it soon. A card you know moves up and returns later. The goal is to get twelve cards to box 3. Short sessions of five to ten minutes are better than one long one.")],
 [("What does the hook for pax suggest?", ["pacify", "pantry", "photo", "cardiac"], 0, "Peace."),
  ("Which Hebrew word hides in Bethlehem?", ["lechem, bread", "bayit, house", "bet, son", "shem, name"], 0, "House of bread."),
  ("What is Latin for light?", ["lux", "nox", "dies", "aqua"], 0, "Lucid."),
  ("What does Greek kardia give English?", ["cardiac", "logic", "pacify", "photo"], 0, "Heart."),
  ("What happens when you miss a flashcard?", ["It goes back to box 1", "It moves up", "It is deleted", "Nothing"], 0, "Leitner."),
  ("How often should you review?", ["A little, every day", "Once a month", "Only before exams", "Never"], 0, "Spaced practice.")],
 [("lux / phos / or", "light"), ("pax / eirene / shalom", "peace"), ("verbum / logos / davar", "word"), ("panis / artos / lechem", "bread"), ("cor / kardia / lev", "heart")],
 [triple_labs(NOUNS, 0, 6, "Match: God, Lord, man, woman, father, mother"),
  triple_labs(NOUNS, 6, 12, "Match: son, day, night, light, water, earth"),
  triple_labs(NOUNS, 12, 18, "Match: heaven, word, love, life, death, king"),
  APP("CARDS", "Flashcards: nouns", "Choose Nouns, then pick two languages. Know a card to move it up a box; miss it and it returns to box 1. Get twelve cards to box 3 to finish.")]
))

# ---------------------------------------------------------------- 13
CHS.append(CH(
 "Core vocabulary II: verbs and adjectives",
 ("Core verbs", [
  "Verb | acts | In a sentence",
  "Verb | has | A root or stem",
  "Say | is | amar, lego, dico",
  "See | is | raah, horao, video",
  "Hear | is | shama, akouo, audio",
  "Be | is | hayah, eimi, sum"]),
 ["Fifteen of the most frequent verbs and adjectives in the Bible, in all three languages: say, see, hear, go, come, give, know, be, do, write, love, live, good, great and one.",
  "Verbs change form: in Hebrew by root and pattern, in Greek and Latin by ending. We list the dictionary form of each (Hebrew past he-form, Greek 'I' form, Latin 'I' form) and drill them with flashcards.",
  "The lab matches verbs across the languages and uses the cards."],
 [("Dictionary form", "The form under which a word is listed: Hebrew 3rd person perfect, Greek and Latin 'I' form."),
  ("Stem", "The part of a verb that stays the same."),
  ("Irregular verb", "A verb whose forms do not follow the regular pattern, like sum."),
  ("Frequency list", "A list of words ranked by how often they appear."),
  ("Active vocabulary", "Words you can produce, not just recognise.")],
 ["Hebrew lists a verb by its 3rd masculine singular perfect: amar, he said.",
  "Greek and Latin list the 'I' form: lego, dico; Latin also gives the infinitive.",
  "Frequent verbs are often irregular: sum, eo, do, facio.",
  "Good and great are adjectives and agree with their nouns.",
  "Learn a verb with a sample phrase: audi, Israel; ho theos agape estin."],
 [T("A small number of verbs make up a large part of the Bible. To say, see, hear, go, come, give, know and be cover most of the stories, and to love is the big word of the New Testament. Learn these, and you can follow a lot of the text. The Hebrew dictionary form is the third masculine singular perfect: amar, he said; raah, he saw; shama, he heard. The Greek and Latin dictionary form is the first person: lego, dico; horao, video; akouo, audio."),
  T("Some of these have clear hooks. Latin video gives video and vision; audio gives audio and audience; dico gives dictate and diction; scribo gives scribe and script; vivo gives vivid. Greek grapho gives graph and graphic; ginosko gives agnostic, one who does not know; poieo gives poem and poet, a maker. The Hebrew verbs ask for the story technique: halakh, he went, lives on in the word Halakha, the way one walks. Natan, he gave, is in names like Nathan and Jonathan."),
  T("Adjectives follow their nouns in Hebrew and agree with them: tov, good; gadol, great. In Greek agathos and megas follow the article and noun pattern, so ho agathos anthropos is the good man. In Latin bonus, magnus and unus change with the noun. Good is a nice test: Deus bonus, filia bona, verbum bonum. The Hebrew phrase mazal tov, good luck, uses tov, good, and Latin bene is good in 'benefit' and 'benediction'."),
  T("Learn a verb together with a little phrase. Audi, Israel gives audio. Ho theos agape estin gives you eimi, estin. Dixit Deus: Fiat lux gives dico and facio. Vayomer elohim gives amar. The flashcards in this chapter use the Verbs deck. Run it in both directions, and then try going from Greek to Latin, which trains you to translate directly.")],
 [("What is the Hebrew dictionary form of a verb?", ["3rd masculine singular perfect", "The infinitive", "The imperative", "The participle"], 0, "Like katav."),
  ("What is 'to say' in Latin?", ["dico", "video", "audio", "scribo"], 0, "Dictate."),
  ("Which verb is the base of 'agnostic'?", ["ginosko, to know", "grapho, to write", "lego, to say", "horao, to see"], 0, "A-gnostic: not knowing."),
  ("What does Hebrew tov mean?", ["good", "great", "one", "bread"], 0, "Mazal tov."),
  ("What does Latin audio give English?", ["audio, audience", "dictate", "vision", "graph"], 0, "To hear."),
  ("Why learn a verb with a phrase?", ["Context helps memory", "It is shorter", "It avoids grammar", "It is required"], 0, "Memory hooks.")],
 [("amar / lego / dico", "say"), ("raah / horao / video", "see"), ("shama / akouo / audio", "hear"), ("natan / didomi / do", "give"), ("hayah / eimi / sum", "be")],
 [triple_labs(VERBS, 0, 6, "Match: say, see, hear, go, come, give"),
  triple_labs(VERBS, 6, 12, "Match: know, be, make, write, love, live"),
  triple_labs(VERBS, 12, 15, "Match: good, great, one"),
  APP("CARDS", "Flashcards: verbs and adjectives", "Choose the Verbs deck. Try English to Greek, then Greek to Latin. Twelve cards in box 3 finishes the lab.")]
))

# ---------------------------------------------------------------- 14
CHS.append(CH(
 "Conversational phrases",
 ("Everyday phrases", [
  "Greeting | opens | A conversation",
  "Shalom | means | Peace and hello",
  "Chaire | means | Rejoice, hello",
  "Salve | means | Be well",
  "Thank you | is | toda, eucharisto, gratias",
  "Question | uses | Who what where"]),
 ["Sixteen useful phrases: greetings, thanks, yes and no, asking a name, asking where, and a few blessings. Each is given in Hebrew, Greek and Latin so you can say it in whichever language you like.",
  "Most of these phrases are formed from the vocabulary and grammar you have seen. Hebrew and Greek greetings were wishes of peace and joy. Latin greetings wish health.",
  "The flashcard lab includes a Phrases deck. Go through it in both directions."],
 [("Greeting", "A word or phrase to meet someone."),
  ("Farewell", "A word or phrase to part."),
  ("Blessing", "A wish of good for someone."),
  ("Imperative", "The form used to give a command or wish: salve, vale."),
  ("Register", "The level of formality of language.")],
 ["Shalom, chaire, salve open a conversation.",
  "Shalom aleichem, eirene hymin, pax vobis: peace be with you.",
  "Toda, eucharisto, gratias: thank you.",
  "Mah shimkha, ti onoma soi, quod nomen tibi est: what is your name?",
  "Te amo, agapo se, ani ohev otkha: I love you.",
  "Barukh elohim, eulogetos ho theos, benedictus Deus: blessed be God."],
 [T("A language is easiest to learn if you use it. Begin with greetings. In Hebrew you say shalom, peace; in Greek chaire, rejoice, which is also the word an angel says to Mary; in Latin salve, be well. For parting, Hebrew says lekh leshalom, go in peace, Greek says errhoso, be strong, and Latin says vale, be strong and well. The idea is the same in each: a wish for the other's wellbeing."),
  T("The blessing peace be with you is shalom aleichem in Hebrew, eirene hymin in Greek and pax vobis in Latin. In the Mass, pax vobiscum, peace be with you, is the same wish. Thanks is toda in Hebrew, eucharisto in Greek, and gratias in Latin. The Greek word became the Eucharist, the thanksgiving, and the Latin gives gratitude. Please is bevakasha, parakalo and quaeso."),
  T("To ask a name, Hebrew says mah shimkha, what your name. Greek says ti onoma soi, what name to you. Latin says quod nomen tibi est, what name to you is. To answer, use the same pattern: shemi, my name; onoma moi, name to me; nomen mihi est, name to me is. Notice how the Greek and Latin both use the dative, to me, while the Hebrew attaches the ending -i. The question words from the previous chapter, mi, tis, quis, mah, ti, quid, eifo, pou and ubi, now appear in sentences."),
  T("Finally, a few phrases of faith. Barukh elohim, eulogetos ho theos, benedictus Deus is blessed be God. Deus caritas est, God is love, from 1 John 4:8, is ho theos agape estin in Greek. The Hebrew line, a plain rendering, is not a verse of the Hebrew Bible. Say the phrases out loud, and try answering a greeting in a different language than the one you heard. That is the quickest way to become comfortable with all three.")],
 [("What is a Latin greeting?", ["salve", "vale", "gratias", "quaeso"], 0, "Be well."),
  ("What does 'vale' mean?", ["Goodbye", "Hello", "Thank you", "Please"], 0, "Valediction."),
  ("What is 'thank you' in Greek?", ["eucharisto", "chaire", "parakalo", "ou"], 0, "Eucharist."),
  ("How do you say 'peace be with you' in Latin?", ["pax vobis", "salve", "deus est", "quis"], 0, "Pax vobiscum."),
  ("What does 'mah shimkha' ask?", ["What is your name?", "Where are you?", "Who are you?", "How are you?"], 0, "Shem, name."),
  ("What is Latin for 'God is love'?", ["Deus caritas est", "Pax Deus est", "Deus amat", "Amor est"], 0, "1 John 4:8.")],
 [("shalom / chaire / salve", "hello"), ("toda / eucharisto / gratias", "thank you"), ("lo / ou / non", "no"), ("ken / nai / ita", "yes"), ("vale", "goodbye (Latin)")],
 [MATCH("Match the greeting", "English to Latin.", [("hello", "salve"), ("goodbye", "vale"), ("thank you", "gratias"), ("please", "quaeso"), ("yes", "ita"), ("no", "non")]),
  MATCH("Match to Greek", "English to Greek.", [("hello", "chaire"), ("thank you", "eucharisto"), ("please", "parakalo"), ("yes", "nai"), ("no", "ou")]),
  MATCH("Match to Hebrew", "English to Hebrew.", [("hello", "shalom"), ("thank you", "toda"), ("yes", "ken"), ("no", "lo"), ("please", "bevakasha")]),
  APP("CARDS", "Flashcards: phrases", "Choose the Phrases deck. Run it both ways. Get twelve cards to box 3 across all decks.")]
))

# ---------------------------------------------------------------- 15
CHS.append(CH(
 "Reading with an interlinear",
 ("Interlinear reading", [
  "Interlinear | glosses | Each word",
  "Reading | starts | With words",
  "Case endings | give | Roles",
  "Parallel texts | show | The same idea",
  "Original | sits above | Its gloss",
  "Smooth translation | comes | Last"]),
 ["An interlinear shows the original word, its sound, and a gloss, one under the other. It lets you read real verses before you know the whole grammar.",
  "The reader lab holds thirteen passages: Genesis 1:1 in Hebrew, Greek and Latin, John 1:1 in Greek and Latin, Genesis 1:3, the Shema, Psalm 23:1, 1 John 4:8 and the Pater Noster. Tap a word to see its sound and meaning, then show the smooth translation and the grammar notes.",
  "You learn the most by comparing: the same verse in three languages."],
 [("Interlinear", "A text with each word glossed directly beneath."),
  ("Gloss", "A short English meaning attached to a word."),
  ("Parallel text", "Two or more versions of the same text side by side."),
  ("Smooth translation", "A natural English version of the whole sentence."),
  ("Parsing", "Naming the part of speech, case, tense, person and so on of a word.")],
 ["Read the original aloud before you look at the gloss.",
  "Tap each word: sound, then meaning.",
  "Find the verb first, then the subject, then the object.",
  "Compare the same verse in two languages.",
  "Parse the endings you know: case for nouns, person for verbs."],
 [T("A good way to begin reading is an interlinear. Each word of the original is shown with its sound and a short English gloss. You see Hebrew bereshit bara elohim as in-beginning, created, God. The reading order stays that of the original, which teaches you to think in Hebrew, Greek or Latin order rather than English order."),
  T("Take Genesis 1:1 in three languages. In Hebrew, bereshit bara elohim et hashamayim ve-et ha-arets: in-beginning created God the heavens and the earth. The verb comes first. In Greek, en arche epoiesen ho theos ton ouranon kai ten gen: in beginning made the God the heaven and the earth; the cases show ho theos as subject and ton ouranon as object. In Latin, in principio creavit Deus caelum et terram: in beginning created God heaven and earth. In all three, the words for beginning, God, heaven and earth match the vocabulary you learned."),
  T("John 1:1 shows the connection between Greek and Latin: en arche en ho logos, kai ho logos en pros ton theon; in principio erat Verbum, et Verbum erat apud Deum. The two versions follow each other word for word, since the Latin translators kept the Greek order. The Shema has the Hebrew nominal sentence, with no verb: the LORD our God, the LORD one. The Latin adds est. The Greek adds the verb estin in the Septuagint as well."),
  T("Here is a routine. First read the original aloud. Second, tap each word and say its gloss. Third, spot the verb and the subject. Fourth, look at the notes for a grammar point. Fifth, show the smooth translation and compare it with your own guess. Open all thirteen passages to finish the lab, then come back and read them again without the glosses. That is when you will notice how much you now recognise.")],
 [("What does an interlinear show?", ["A gloss under each word", "Only a smooth translation", "Only the original", "A dictionary"], 0, "Word by word."),
  ("Where does the verb stand in Hebrew Genesis 1:1?", ["First", "Last", "Second", "Missing"], 0, "Bara elohim."),
  ("Why do the Greek and Latin of John 1:1 match?", ["The Latin follows the Greek order", "They are the same language", "They are both Hebrew", "It is chance"], 0, "A close translation."),
  ("What does the Hebrew Shema lack?", ["A verb 'is'", "A subject", "The word God", "The word one"], 0, "Nominal sentence."),
  ("What is a good first step in reading?", ["Read the original aloud", "Look only at the English", "Skip the verbs", "Memorise the grammar"], 0, "Sound before sense."),
  ("What does 'ton ouranon' show?", ["Accusative: the object", "Nominative: the subject", "Genitive: of", "Vocative: addressing"], 0, "The heaven, object.")],
 [("bara", "created"), ("in principio", "in the beginning"), ("en arche", "in the beginning"), ("bereshit", "in the beginning"), ("estin / est", "is")],
 [APP("READER", "Reader: parallel passages", "Open each of the thirteen passages. Tap the words, then show the smooth translation and read the grammar notes. Open them all to finish.", 760),
  MATCH("Genesis 1:1 across languages", "Match each word in Latin to its Hebrew word.", [("principio", "bereshit"), ("creavit", "bara"), ("Deus", "elohim"), ("caelum", "shamayim"), ("terram", "erets")]),
  ORDER("Put the Latin words in order", "Genesis 1:1 in the Vulgate.", ["In", "principio", "creavit", "Deus", "caelum", "et", "terram"]),
  ORDER("Put the Hebrew words in reading order", "Genesis 1:1, right to left, in transliteration.", ["bereshit", "bara", "elohim", "et", "hashamayim", "ve-et", "ha-arets"])]
))

# ---------------------------------------------------------------- 16
CHS.append(CH(
 "Translating and remembering",
 ("A translation method", [
  "Find | the verb | First",
  "Find | the subject | Next",
  "Check | the endings | For roles",
  "Gloss | each word | Literally",
  "Then | smooth | The English",
  "Review | with spacing | Leitner",
  "Link | to stories | Hooks"]),
 ["A reliable method for translating a sentence: find the verb, find the subject, use the endings to work out the roles, gloss each word literally, then smooth into good English. The same steps work for Hebrew, Greek and Latin.",
  "Translating between the languages teaches you quickly, because you compare structures: the same idea turns up with different grammar. Cognates and hooks help you remember, and spaced repetition makes it last.",
  "The labs include a Leitner scheduler in Python and a translation exercise."],
 [("Literal gloss", "A word-for-word translation that keeps the original order."),
  ("Smooth translation", "A natural version in good English."),
  ("Spaced repetition", "Reviewing at increasing intervals to build long memory."),
  ("Mnemonic", "A memory aid, like a rhyme, picture or hook."),
  ("Loci", "The method of placing items in a familiar place in your mind.")],
 ["Method: verb, subject, object, endings, literal gloss, smooth English.",
  "Compare the same sentence in three languages to see the structure.",
  "Use hooks: connect to English words, pictures and stories.",
  "Space your reviews: 1, 2, 4, 8, 16 days.",
  "Say words aloud, and write them by hand.",
  "Use the words in your own sentences."],
 [T("To translate, follow a method. Step one: find the verb. In Hebrew, it is often first. In Latin, it is often last. In Greek, it can be anywhere. Step two: find the subject. In Greek and Latin it is in the nominative; in Hebrew it usually follows the verb. Step three: find the objects, using endings or the Hebrew object marker et. Step four: gloss each remaining word literally. Step five: write a smooth English version. Never skip the literal gloss, because it shows you what the original really says."),
  T("Try a Latin example. Deus creavit caelum et terram. Verb: creavit, he created. Subject: Deus, in the nominative. Objects: caelum and terram, both in the accusative, joined by et, and. Smooth: God created heaven and earth. Now try the Greek: ho theos ten gen epoiesen. The article ho is nominative, so theos is the subject; ten gen is accusative feminine, the object; epoiesen is the verb, he made. You can read it, even though the order is different from the Latin."),
  T("Memory is a skill. Spaced repetition says to review a word just before you forget it: after a day, then two days, then four, eight and sixteen. The Leitner boxes you used in the flashcard lab are a physical version of this: each box has a longer wait, and a miss sends the card back to box 1. The loci method places each word in a familiar room: put a lux, a lamp, on the table, a panis, a loaf, on the shelf. Hooks tie a word to something you already know, such as photo for phos."),
  T("Make the languages work together. A Latin word often tells you a Greek one: sex and hex, septem and hepta. Greek words show up in English theology: theos, logos, kardia. Hebrew words survive in English as amen, sabbath, hallelujah, messiah, jubilee and cherub. Write ten short sentences of your own, such as Deus est bonus, ho theos agathos estin. Say them out loud, and then translate each into a different language. That is real translation practice, and it is how learners become readers.")],
 [("What is the first step in translating a sentence?", ["Find the verb", "Look up every word", "Write the English", "Memorise the grammar"], 0, "The verb anchors the sentence."),
  ("Why gloss literally first?", ["It shows what the original says", "It is shorter", "It is required", "It avoids grammar"], 0, "Then smooth it."),
  ("What does spaced repetition do?", ["Reviews just before you forget", "Reviews everything daily", "Avoids review", "Only repeats errors"], 0, "1, 2, 4, 8, 16."),
  ("What happens to a missed Leitner card?", ["It returns to box 1", "It moves up", "It is dropped", "It stays"], 0, "Back to the start."),
  ("Which tells a Greek subject?", ["The nominative case", "Word order only", "The article's position", "The verb tense"], 0, "Ho theos."),
  ("Which is a Hebrew loanword in English?", ["amen", "logic", "pacify", "photo"], 0, "Also hallelujah.")],
 [("verb, subject, object", "The order of translation"), ("1, 2, 4, 8, 16", "Spacing in days"), ("hook", "Link to an English word"), ("loci", "Placing words in a familiar place"), ("amen", "A Hebrew word in English")],
 [ORDER("The translation method", "Put the steps in order.", ["Find the verb", "Find the subject", "Find the objects from the endings", "Gloss each word literally", "Write a smooth translation"]),
  MATCH("Match the memory tool", "Pair each tool with what it does.", [("Spaced repetition", "reviews at growing intervals"), ("Hook", "links a word to one you know"), ("Loci", "puts words in a mental room"), ("Cognate", "a related word in another language"), ("Gloss", "a short meaning under a word")]),
  PL("The Leitner scheduler", "Write leitner(box, correct): box is 1 to 5. If correct is True, move up one box (but not above 5); if False, go back to box 1. Return [new_box, days], where days is the wait for the new box: 1, 2, 4, 8 or 16 days for boxes 1 to 5.", "leitner(box, correct)", '''
def leitner(box, correct):
    nb = min(box + 1, 5) if correct else 1
    return [nb, [1, 2, 4, 8, 16][nb - 1]]
''', [[1, True], [2, True], [5, True], [3, False], [1, False], [4, True]], "Compute the new box first, then look up the interval."),
  PL("Translate word by word", "Write gloss_line(sentence, dictionary): split the sentence on spaces and return the list of glosses, using the dictionary; if a word is missing, return '?' for it. Compare the Latin line 'Deus creavit caelum' with a dictionary of English glosses.", "gloss_line(sentence, dictionary)", '''
def gloss_line(sentence, dictionary):
    out = []
    for w in sentence.split(" "):
        out.append(dictionary.get(w, "?"))
    return out
''', [["Deus creavit caelum", {"Deus": "God", "creavit": "created", "caelum": "heaven"}], ["Pax vobis", {"Pax": "peace", "vobis": "to-you"}], ["Verbum erat Deus", {"Verbum": "Word", "erat": "was"}], ["", {}]], "Use dict.get with a default.")]
))
