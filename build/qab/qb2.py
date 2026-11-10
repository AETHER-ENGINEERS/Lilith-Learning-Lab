# -*- coding: utf-8 -*-
"""Hermetic Qabalah course, part 2: paths and Tarot, correspondences, methods, history, critical study."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

PATHS = '''
PATHS = [
 [11, "Aleph", 1, 2, "The Fool"], [12, "Beth", 1, 3, "The Magician"], [13, "Gimel", 1, 6, "The High Priestess"], [14, "Daleth", 2, 3, "The Empress"],
 [15, "Heh", 2, 6, "The Emperor"], [16, "Vav", 2, 4, "The Hierophant"], [17, "Zayin", 3, 6, "The Lovers"], [18, "Cheth", 3, 5, "The Chariot"],
 [19, "Teth", 4, 5, "Strength"], [20, "Yod", 4, 6, "The Hermit"], [21, "Kaph", 4, 7, "Wheel of Fortune"], [22, "Lamed", 5, 6, "Justice"],
 [23, "Mem", 5, 8, "The Hanged Man"], [24, "Nun", 6, 7, "Death"], [25, "Samekh", 6, 9, "Temperance"], [26, "Ayin", 6, 8, "The Devil"],
 [27, "Peh", 7, 8, "The Tower"], [28, "Tzaddi", 7, 9, "The Star"], [29, "Qoph", 7, 10, "The Moon"], [30, "Resh", 8, 9, "The Sun"],
 [31, "Shin", 8, 10, "Judgement"], [32, "Tav", 9, 10, "The World"]]
'''


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "The 22 paths and the Tarot",
 ("Paths and Tarot", [
  "Path | links | Two sephiroth",
  "Letter | names | A path",
  "Major Arcana | has | 22 cards",
  "Card | matches | A path",
  "Golden Dawn | fixed | The attributions",
  "Crowley | swapped | Heh and Tzaddi",
  "Pictures | carry | Symbols"]),
 ["The Hermetic Qabalah pairs each of the 22 paths with a letter and with one of the 22 trumps of the Tarot, the Major Arcana. The most common table is from the Golden Dawn.",
  "This pairing is a 19th-century invention. Tarot cards first appeared in the 15th century as a card game, and the link to Kabbalah was proposed by French occultists such as Eliphas Levi and refined by the Golden Dawn.",
  "As a symbolic system it works as a memory aid: each path becomes an image with associated letters, planets and meanings."],
 [("Major Arcana", "The 22 trump cards of the Tarot, numbered 0 to 21."),
  ("Path attribution", "The link between a path of the Tree, a letter and a Tarot card."),
  ("Golden Dawn", "The Hermetic Order of the Golden Dawn, founded in 1888, which fixed the standard correspondences."),
  ("Memory aid", "A system of linked images used to remember information.")],
 ["22 letters = 22 paths = 22 Major Arcana.",
  "Aleph = The Fool; Beth = The Magician; Gimel = The High Priestess.",
  "Tav = The World; Shin = Judgement; Resh = The Sun.",
  "Crowley swapped Heh (Star) and Tzaddi (Emperor).",
  "The pairing dates from the 19th century."],
 [T("Take the 22 Major Arcana cards of the Tarot, from the Fool (0) to the World (21). The Golden Dawn matched each to one of the 22 paths. The Fool goes with Aleph, the first letter, and the World with Tav, the last. The Magician goes with Beth, the High Priestess with Gimel, and the Empress with Daleth."),
  T("The matching is not simple counting. It follows the Golden Dawn's own view of what each card means. The Fool, number zero, is matched with Aleph, which means ox but has the value one. The Wheel of Fortune goes with Kaph, a planetary Jupiter letter. The Sun goes with Resh, and the Moon with Qoph."),
  T("Two cards created a famous quarrel. In the Golden Dawn's table, Heh goes with the Emperor and Tzaddi with the Star. Aleister Crowley, in his Book of Thoth, swapped them, saying a line in his Book of the Law required it. Waite and Crowley also swapped the order of Strength and Justice. So tables in books can differ."),
  T("Where did the link come from? Tarot cards were first made in Italy in the fifteenth century for a card game. In 1781 Antoine Court de Gebelin claimed they were Egyptian wisdom, and in the 1850s Eliphas Levi tied them to the Hebrew alphabet. The Golden Dawn built out the details. Historians find no evidence for earlier ties."),
  T("So the table is best seen as a creative design. It is a way to place twenty-two pictures on a diagram, so that each picture has a position, a letter, a number and a sign. If you want to remember the Tarot, or the Tree, this provides hooks. Whether it also reveals any hidden truth is a matter of belief, not of evidence.")],
 [("How many Major Arcana cards are there?", ["22", "21", "78", "10"], 0, "Fool to World."),
  ("Which letter goes with The Fool?", ["Aleph", "Beth", "Tav", "Shin"], 0, "The first letter."),
  ("Which card goes with Tav?", ["The World", "The Fool", "The Sun", "Death"], 0, "Path 32."),
  ("When did Tarot cards first appear?", ["15th century, as a card game", "Ancient Egypt", "12th century", "20th century"], 0, "Northern Italy."),
  ("Who first tied Tarot to the Hebrew alphabet?", ["French occultists such as Levi", "Moses", "Pico", "Agrippa"], 0, "19th century."),
  ("What did Crowley swap?", ["Heh and Tzaddi", "Aleph and Tav", "Beth and Gimel", "Mem and Shin"], 0, "Emperor and Star.")],
 [("Aleph", "The Fool"), ("Beth", "The Magician"), ("Gimel", "The High Priestess"), ("Resh", "The Sun"), ("Tav", "The World")],
 [MATCH("Match the path", "Pair each letter with its Golden Dawn Tarot card.", [("Aleph", "The Fool"), ("Beth", "The Magician"), ("Gimel", "The High Priestess"), ("Daleth", "The Empress"), ("Resh", "The Sun"), ("Tav", "The World")]),
  PL("Card for a letter", "Write card_for(letter): return the Golden Dawn Tarot trump for a Hebrew letter name from this table (letter, card): Aleph The Fool, Beth The Magician, Gimel The High Priestess, Daleth The Empress, Heh The Emperor, Vav The Hierophant, Zayin The Lovers, Cheth The Chariot, Teth Strength, Yod The Hermit, Kaph Wheel of Fortune, Lamed Justice, Mem The Hanged Man, Nun Death, Samekh Temperance, Ayin The Devil, Peh The Tower, Tzaddi The Star, Qoph The Moon, Resh The Sun, Shin Judgement, Tav The World. Return 'unknown' for anything else.", "card_for(letter)", PATHS + '''
def card_for(letter):
    for p in PATHS:
        if p[1] == letter:
            return p[4]
    return "unknown"
''', [["Aleph"], ["Tav"], ["Heh"], ["Tzaddi"], ["Kaph"], ["Shin"], ["Omega"]], "Search the table for the letter."),
  PL("Path between two sephiroth", "Write path_between(a, b): the number of the direct path that joins the sephiroth a and b (numbers 1 to 10), in either order, or 0 if there is none. Use the table of 22 paths (path number, letter, from, to, card): 11 1-2, 12 1-3, 13 1-6, 14 2-3, 15 2-6, 16 2-4, 17 3-6, 18 3-5, 19 4-5, 20 4-6, 21 4-7, 22 5-6, 23 5-8, 24 6-7, 25 6-9, 26 6-8, 27 7-8, 28 7-9, 29 7-10, 30 8-9, 31 8-10, 32 9-10.", "path_between(a, b)", PATHS + '''
def path_between(a, b):
    for p in PATHS:
        if (p[2] == a and p[3] == b) or (p[2] == b and p[3] == a):
            return p[0]
    return 0
''', [[1, 2], [2, 1], [9, 10], [1, 10], [6, 9], [4, 7], [3, 4]], "Compare the two ends in both orders."),
  PL("Paths at a sephirah", "Write paths_at(n): the sorted list of path numbers that touch sephirah n (1 to 10), using the same table.", "paths_at(n)", PATHS + '''
def paths_at(n):
    out = []
    for p in PATHS:
        if p[2] == n or p[3] == n:
            out.append(p[0])
    return sorted(out)
''', [[1], [6], [10], [5], [8]], "Collect every path with n at either end.")]
))

CHS.append(CH(
 "Correspondences: planets, elements and the zodiac",
 ("Correspondences", [
  "Sephirah | has | A planet",
  "Path | has | A zodiac sign",
  "Letter | has | A value",
  "Planet | links | A metal and colour",
  "Table | collects | Correspondences",
  "777 | tabulates | Them all",
  "Memory | uses | The table"]),
 ["The Hermetic system builds big tables of correspondence. Every sephirah and path gets a planet, element or zodiac sign, a colour, a metal, a stone, a god or angel, and a number.",
  "The planets on the Tree are Saturn (Binah), Jupiter (Chesed), Mars (Geburah), the Sun (Tiphareth), Venus (Netzach), Mercury (Hod) and the Moon (Yesod). Kether is the Primum Mobile, Chokmah the zodiac, and Malkuth the Earth.",
  "These come from medieval and Renaissance sources such as Agrippa, and were tabulated by Crowley in 777 (1909)."],
 [("Primum Mobile", "In old astronomy, the outermost sphere that moves all the others."),
  ("Planetary sephirah", "A sephirah linked with one of the seven classical planets."),
  ("Table of correspondences", "A chart linking items in different systems that share a symbolic character."),
  ("777", "Crowley's 1909 book of tables of correspondences."),
  ("Classical planets", "The seven wanderers visible to the naked eye: Moon, Mercury, Venus, Sun, Mars, Jupiter, Saturn.")],
 ["Saturn: Binah. Jupiter: Chesed. Mars: Geburah.",
  "Sun: Tiphareth. Venus: Netzach. Mercury: Hod. Moon: Yesod.",
  "Kether: Primum Mobile. Chokmah: zodiac. Malkuth: earth.",
  "Path doubles: planets. Simples: zodiac. Mothers: elements.",
  "Tables are tools for memory."],
 [T("Imagine a giant spreadsheet. Rows are things like Binah, Chesed or the path of Peh. Columns are systems: planet, metal, colour, god, angel, plant, stone, Tarot card. The Hermetic Qabalah is the dream of filling every cell, so that any symbol connects to many others."),
  T("The seven planets of the Tree are the classical wanderers. Saturn is Binah, the dark mother. Jupiter is Chesed, mercy, and Mars is Geburah, strength. The Sun is Tiphareth at the centre. Venus is Netzach, Mercury is Hod and the Moon is Yesod. This gives a rough ladder from Saturn at the top to the Moon below."),
  T("Kether, the Crown, is called the Primum Mobile, the sphere that sets all the others turning. Chokmah is the sphere of the fixed stars or zodiac. Malkuth is the Earth. So the Tree from top to bottom runs from the whole sky down to the ground."),
  T("The same pattern appears in colours, called colour scales. In the Golden Dawn's system the same sephirah has four colours, one for each of the four worlds. For example, Tiphareth is shown as clear pink rose in the King scale and yellow in the Queen scale. Pupils paint these on flash cards, so they remember them."),
  T("Aleister Crowley collected many of these in 777 in 1909, with hundreds of rows. Some of the entries come from medieval sources and some are his own. This shows that the table is a living creation. Different authors make different choices, so you should treat any table as one author's design, and not as fixed truth.")],
 [("Which planet goes with Tiphareth?", ["The Sun", "The Moon", "Mars", "Saturn"], 0, "Heart of the Tree."),
  ("Which planet goes with Yesod?", ["The Moon", "Mercury", "Venus", "Jupiter"], 0, "Foundation."),
  ("What goes with Malkuth?", ["The Earth", "The Sun", "Saturn", "The zodiac"], 0, "Bottom of the Tree."),
  ("What are the simple letters linked to?", ["Zodiac signs", "Planets", "Pillars", "Worlds"], 0, "Twelve of each."),
  ("Who wrote 777?", ["Aleister Crowley", "A. E. Waite", "Agrippa", "Scholem"], 0, "1909."),
  ("What is a table of correspondences?", ["A chart linking symbols across systems", "A tax form", "A map", "A diary"], 0, "Rows and columns.")],
 [("Binah", "Saturn"), ("Chesed", "Jupiter"), ("Geburah", "Mars"), ("Tiphareth", "Sun"), ("Netzach", "Venus"), ("Hod", "Mercury"), ("Yesod", "Moon")],
 [MATCH("Match the sephirah to its planet", "Pair each sephirah with its Hermetic planet.", [("Binah", "Saturn"), ("Chesed", "Jupiter"), ("Geburah", "Mars"), ("Tiphareth", "Sun"), ("Netzach", "Venus"), ("Hod", "Mercury"), ("Yesod", "Moon")]),
  MATCH("Match the letter to its correspondence", "Pair each letter with its element, planet or sign.", [("Aleph", "air"), ("Mem", "water"), ("Shin", "fire"), ("Peh", "Mars"), ("Heh", "Aries"), ("Qoph", "Pisces")]),
  PL("Planet of a sephirah", "Write planet(n): for a sephirah number 1 to 10 return its Hermetic planet or sphere: 1 'Primum Mobile', 2 'Zodiac', 3 'Saturn', 4 'Jupiter', 5 'Mars', 6 'Sun', 7 'Venus', 8 'Mercury', 9 'Moon', 10 'Earth'. Otherwise 'unknown'.", "planet(n)", '''
def planet(n):
    names = ["Primum Mobile", "Zodiac", "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Earth"]
    if 1 <= n <= 10:
        return names[n - 1]
    return "unknown"
''', [[1], [3], [6], [9], [10], [0], [11]], "Index into the list."),
  PL("Letters by type", "Write letter_type(name): return 'mother' for Aleph, Mem or Shin; 'double' for Beth, Gimel, Daleth, Kaph, Peh, Resh or Tav; 'simple' for the other twelve letters (Heh, Vav, Zayin, Cheth, Teth, Yod, Lamed, Nun, Samekh, Ayin, Tzaddi, Qoph); otherwise 'unknown'.", "letter_type(name)", '''
def letter_type(name):
    if name in ["Aleph", "Mem", "Shin"]:
        return "mother"
    if name in ["Beth", "Gimel", "Daleth", "Kaph", "Peh", "Resh", "Tav"]:
        return "double"
    if name in ["Heh", "Vav", "Zayin", "Cheth", "Teth", "Yod", "Lamed", "Nun", "Samekh", "Ayin", "Tzaddi", "Qoph"]:
        return "simple"
    return "unknown"
''', [["Aleph"], ["Peh"], ["Qoph"], ["Tav"], ["Yod"], ["Omega"]], "Three lists, three answers.")]
))

CHS.append(CH(
 "Methods: gematria, notarikon and temurah",
 ("Methods", [
  "Gematria | adds | Letter values",
  "Notarikon | forms | Acronyms",
  "Temurah | swaps | Letters",
  "Atbash | reverses | The alphabet",
  "Word | has | A number",
  "Equal sums | suggest | A link",
  "Method | is | A reading game"]),
 ["Kabbalists developed three classic methods of reading hidden links in words. Gematria adds the numerical values of letters. Notarikon treats each letter of a word as the start of another word, or builds one word from the first letters of many. Temurah swaps letters by a rule.",
  "Atbash is the best-known temurah: it swaps the first letter with the last, the second with the second last, and so on. The word Sheshach in the Book of Jeremiah has been read as an Atbash form of Babel.",
  "Used as a game, these methods reveal wordplay and links between ideas. As evidence, they prove nothing, because with enough words you can find a match for any number."],
 [("Gematria", "Finding the numerical value of a word from its letters and linking words with equal sums."),
  ("Notarikon", "Reading a word as an acronym, or forming a word from initials."),
  ("Temurah", "Rearranging or substituting letters by a rule."),
  ("Atbash", "A substitution that swaps the first and last letters of the alphabet, and so on inward."),
  ("Isopsephy", "The Greek counterpart of gematria.")],
 ["Gematria: add letter values.",
  "Notarikon: initials make a phrase.",
  "Temurah: swap letters by a rule; Atbash reverses the alphabet.",
  "Equal sums are links in play, not proof.",
  "Shalom שלום = 376."],
 [T("Gematria is the most famous. The word shalom, peace, is spelled שלום, shin (300), lamed (30), vav (6) and mem (40), which adds to 376. Words with the same sum are said to be linked. For example, the Hebrew words for love, ahavah (13), and one, echad (13), share a value, which commentators have enjoyed."),
  T("Notarikon works with initials. The Hebrew phrase Adonai Melech Ne'eman, meaning Lord, faithful King, is abbreviated to Amen. Going the other way, a word is expanded into a phrase made of words starting with its letters. This was used for prayers, and also in the Christian world for slogans such as INRI."),
  T("Temurah means change. In the simplest form, letters swap by a fixed rule. In Atbash, aleph swaps with tav, beth with shin, gimel with resh, and so on, from the name of the first and last two letters, aleph-tav-beth-shin. Applying it to a word gives a new word, and readers hunt for meaning in it."),
  T("A caution from mathematics: with a language full of short words and sums limited to a few thousand, many coincidences are bound to happen. If you have enough words, you can find a match for nearly any number. So the methods work well as creative and memory games, but a found match is not evidence for any claim."),
  T("The Greek world had the same game, called isopsephy, and Christian and Gnostic authors used it. The number of the beast in the Book of Revelation, 666, is a well-known example in the Greek form. Observing the method across cultures shows how widely people have played with letters and numbers.")],
 [("What does gematria compute?", ["The numerical value of a word", "A rhyme", "A key signature", "A date"], 0, "Add the letter values."),
  ("What is the value of shalom שלום?", ["376", "346", "306", "400"], 0, "300 + 30 + 6 + 40."),
  ("What is notarikon?", ["Reading initials as words", "Counting letters", "Swapping letters", "Drawing the Tree"], 0, "Acronyms."),
  ("What does Atbash swap?", ["First letter with last, and so on", "Vowels", "Words", "Numbers"], 0, "Aleph with Tav."),
  ("Do equal gematria sums prove a link?", ["No, they are wordplay", "Yes, always", "Only in Hebrew", "Only for names"], 0, "Coincidences are common."),
  ("What is the Greek counterpart of gematria?", ["Isopsephy", "Notarikon", "Atbash", "Temurah"], 0, "Letters as numbers.")],
 [("Gematria", "letter values added"), ("Notarikon", "initials as words"), ("Temurah", "letter substitution"), ("Atbash", "aleph with tav, beth with shin")],
 [MATCH("Match the method", "Pair each method with its idea.", [("Gematria", "add the letter values"), ("Notarikon", "initials form words"), ("Temurah", "substitute letters by a rule"), ("Atbash", "reverse the alphabet")]),
  PL("Atbash", "Write atbash(word): apply Atbash to a Hebrew word by swapping each letter with the one at the mirrored position in the 22-letter alphabet אבגדהוזחטיכלמנסעפצקרשת (א swaps with ת, ב with ש, and so on). Final forms ך ם ן ף ץ should first be read as כ מ נ פ צ. Return the new string.", "atbash(word)", '''
ALPHA = "אבגדהוזחטיכלמנסעפצקרשת"
FINALS = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}
def atbash(word):
    out = ""
    for ch in word:
        if ch in FINALS:
            ch = FINALS[ch]
        i = ALPHA.find(ch)
        if i >= 0:
            out = out + ALPHA[21 - i]
        else:
            out = out + ch
    return out
''', [["בבל"], ["א"], ["ת"], ["ששך"], ["אבג"]], "Mirror the index: position i goes to 21 minus i."),
  PL("Notarikon", "Write notarikon(words): given a list of words in Latin letters, return the string of their first letters in uppercase. For ['Adonai', 'Melech', 'Neeman'] the result is 'AMN'.", "notarikon(words)", '''
def notarikon(words):
    out = ""
    for w in words:
        out = out + w[0].upper()
    return out
''', [[["Adonai", "Melech", "Neeman"]], [["a", "b"]], [[]], [["Iesus", "Nazarenus", "Rex", "Iudaeorum"]]], "Take the first letter of each word."),
  PL("Same value?", "Write same_value(a, b): True if two Hebrew words have the same standard gematria. Values: א 1, ב 2, ג 3, ד 4, ה 5, ו 6, ז 7, ח 8, ט 9, י 10, כ ך 20, ל 30, מ ם 40, נ ן 50, ס 60, ע 70, פ ף 80, צ ץ 90, ק 100, ר 200, ש 300, ת 400.", "same_value(a, b)", '''
VALUES = {"א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7, "ח": 8, "ט": 9, "י": 10,
  "כ": 20, "ך": 20, "ל": 30, "מ": 40, "ם": 40, "נ": 50, "ן": 50, "ס": 60, "ע": 70,
  "פ": 80, "ף": 80, "צ": 90, "ץ": 90, "ק": 100, "ר": 200, "ש": 300, "ת": 400}
def value(w):
    t = 0
    for ch in w:
        if ch in VALUES:
            t = t + VALUES[ch]
    return t
def same_value(a, b):
    return value(a) == value(b)
''', [["אהבה", "אחד"], ["שלום", "מלך"], ["א", "א"], ["ב", "ג"]], "Compute both values and compare.")]
))

CHS.append(CH(
 "Golden Dawn and after: a short history",
 ("Modern history", [
  "Eliphas Levi | linked | Tarot and Hebrew letters",
  "Golden Dawn | founded | 1888",
  "Mathers Westcott Woodman | founded | The Order",
  "Waite | published | Tarot",
  "Crowley | wrote | 777",
  "Fortune | wrote | Mystical Qabalah",
  "Jung | read | Symbols as psyche"]),
 ["The Hermetic Order of the Golden Dawn was founded in London in 1888 by three Freemasons: William Wynn Westcott, William Robert Woodman and Samuel Liddell MacGregor Mathers. It taught Qabalah, astrology, Tarot and ritual in graded degrees.",
  "Its members included W. B. Yeats, A. E. Waite and Aleister Crowley. After it split in the early 1900s, Waite produced the Rider-Waite Tarot (1909), and Crowley, the Thoth Tarot (1944) and the tables of 777.",
  "Dion Fortune's The Mystical Qabalah (1935) gave a popular, psychological reading, and Carl Jung's work encouraged reading such symbols as maps of the psyche."],
 [("Hermetic Order of the Golden Dawn", "A British magical order founded in 1888 that systematised Hermetic Qabalah."),
  ("Eliphas Levi", "A French occultist (1810-1875) who tied the Tarot to the Hebrew alphabet."),
  ("A. E. Waite", "A scholar and Golden Dawn member who co-created the Rider-Waite Tarot."),
  ("Aleister Crowley", "An English occultist (1875-1947) who wrote 777 and the Book of Thoth."),
  ("Dion Fortune", "A British author (1890-1946) whose Mystical Qabalah made the system popular.")],
 ["Levi: 1850s. Golden Dawn: 1888.",
  "Rider-Waite Tarot: 1909. 777: 1909.",
  "Fortune: 1935. Thoth Tarot: 1944.",
  "The Golden Dawn was a secret society with degrees.",
  "Jung gave a psychological reading of symbols."],
 [T("In the 1850s, the French writer Eliphas Levi said that the twenty-two Tarot trumps matched the twenty-two Hebrew letters. This was a new claim, and nothing earlier ties them. But it caught on, and when later groups needed a framework, this was ready."),
  T("In 1888 the Golden Dawn opened in London. Its founders were Freemasons with a deep interest in old manuscripts. Westcott claimed to have found a cipher manuscript that led to the order. Historians doubt the story. Whatever its origins, the order built out the complete system of tables and graded initiations."),
  T("Famous members make a long list: the poet W. B. Yeats, the actress Florence Farr, A. E. Waite and Aleister Crowley. The order split over leadership in 1900. Waite and Pamela Colman Smith then made the Rider-Waite Tarot in 1909, and Crowley published 777 in the same year. Later on Crowley made the Thoth Tarot with Lady Frieda Harris."),
  T("Dion Fortune, a British psychologist and author, wrote The Mystical Qabalah in 1935. She presented the Tree as a map of the whole person, the world and the divine, in plain language. Her book still sits on many shelves, and helped bring the Qabalah to a wider audience."),
  T("Carl Jung, who knew the esoteric tradition well, argued that symbols like these are products of the psyche, a view that has led many readers to treat the Tree as a map of inner life. This is another way to read it: not as a claim about the cosmos, but as a tool for self-reflection and imagination.")],
 [("When was the Golden Dawn founded?", ["1888", "1788", "1950", "1620"], 0, "In London."),
  ("Who tied the Tarot to the Hebrew letters in the 1850s?", ["Eliphas Levi", "Pico", "Fortune", "Jung"], 0, "French occultist."),
  ("What did Waite and Pamela Colman Smith produce in 1909?", ["The Rider-Waite Tarot", "777", "The Zohar", "The Hermetica"], 0, "A popular deck."),
  ("What is 777?", ["Crowley's tables of correspondences", "A prayer", "A Tarot deck", "A Hebrew book"], 0, "1909."),
  ("Who wrote The Mystical Qabalah?", ["Dion Fortune", "Crowley", "Agrippa", "Waite"], 0, "1935."),
  ("How did Jung's ideas influence the reading of the Tree?", ["As a map of the psyche", "As proof of magic", "As a calendar", "As a recipe"], 0, "Symbols as inner life.")],
 [("1850s", "Levi links Tarot and Hebrew letters"), ("1888", "Golden Dawn founded"), ("1909", "Rider-Waite Tarot and 777"), ("1935", "The Mystical Qabalah"), ("1944", "Thoth Tarot")],
 [ORDER("Modern timeline", "Order these events from earliest to latest.", ["Levi links Tarot to Hebrew letters", "Golden Dawn founded", "Rider-Waite Tarot published", "Fortune's Mystical Qabalah", "Thoth Tarot published"]),
  MATCH("Match the person", "Pair each person with what they are known for.", [("Eliphas Levi", "linked Tarot to the Hebrew alphabet"), ("Mathers", "co-founded the Golden Dawn"), ("A. E. Waite", "Rider-Waite Tarot"), ("Aleister Crowley", "777 and the Thoth Tarot"), ("Dion Fortune", "The Mystical Qabalah")]),
  PL("Years apart", "Write years_between(a, b): the number of years between two dates, as a non-negative number (the absolute difference).", "years_between(a, b)", '''
def years_between(a, b):
    d = b - a
    if d < 0:
        d = 0 - d
    return d
''', [[1888, 1909], [1935, 1888], [1850, 1850], [1944, 1909]], "Subtract and take the absolute value."),
  PL("Which era?", "Write era(year): return 'before the Golden Dawn' for years up to 1887, 'Golden Dawn era' for 1888 to 1914, 'after' for later years.", "era(year)", '''
def era(year):
    if year <= 1887:
        return "before the Golden Dawn"
    if year <= 1914:
        return "Golden Dawn era"
    return "after"
''', [[1850], [1888], [1909], [1914], [1935]], "Test the ranges in order.")]
))

CHS.append(CH(
 "Reading critically and using the Tree as a symbol map",
 ("Critical study", [
  "Historian | checks | Origin claims",
  "Scholem | studied | Jewish Kabbalah",
  "Yates | studied | Hermetic tradition",
  "Hanegraaff | studies | Western esotericism",
  "Claims | need | Evidence",
  "Respect | for | Living traditions",
  "Symbol map | aids | Memory and reflection"]),
 ["Hermetic Qabalah is best studied with a historian's care. Many claims of ancient origin, such as that the Tarot is Egyptian or that the Golden Dawn tables are millennia old, do not survive checking. The system is a creative modern synthesis built from older parts.",
  "It is also wise to respect the living Jewish tradition of Kabbalah, which is a different thing: a scholarly and devotional discipline within Judaism, with a long, rigorous history. The Hermetic system borrows its vocabulary, often loosely.",
  "As a personal tool, the Tree can serve as a map of symbols for memory, reflection and creative work, without needing to believe in any hidden powers."],
 [("Historiography", "The study of how history is written and what the sources support."),
  ("Western esotericism", "The academic field that studies traditions such as Hermeticism, astrology and alchemy."),
  ("Syncretism", "Blending ideas from different traditions into one system."),
  ("Cultural borrowing", "Using ideas, words or symbols from another living tradition."),
  ("Symbol map", "A diagram that organises images and ideas so they can be remembered and reflected on.")],
 ["Check the date of every claim of ancient origin.",
  "Hermetic Qabalah is a 19th-century synthesis.",
  "Jewish Kabbalah is a living tradition; credit it.",
  "Equal sums and matching tables are not proofs.",
  "Use the Tree as a memory and reflection tool."],
 [T("Good scholarship begins with questions. Where does this idea first appear? Who wrote it down? Is there a manuscript, or only a story? The historians Gershom Scholem on Kabbalah, Frances Yates on Renaissance Hermeticism and Wouter Hanegraaff on Western esotericism set the standard of asking these questions."),
  T("Asked of the Hermetic Qabalah, the answers are interesting. The Tree of Life and the letters are medieval and older. The Hermetic texts are from the early centuries CE. The pairing with Tarot is from the nineteenth century. The tables of correspondence are mostly from the Golden Dawn and Crowley. Each layer has its own date."),
  T("It is fair to see the Qabalah as a form of syncretism: many traditions poured into one container. That is not a flaw. Much of human culture works that way. But it helps to separate what the Jewish tradition holds, what Renaissance scholars said, and what modern occultists added, and to say which is which."),
  T("A respectful approach acknowledges that Kabbalah is a living religious tradition for many Jewish people, with its own teachers and its own methods of study. Treating it only as raw material for other systems can seem shallow. If it interests you, try to read some of the Jewish scholarship too."),
  T("What can you do with the Tree? Use it as a memory palace: a place for each idea, each with a name, a number and an image. Use it as a prompt for writing or drawing, or for reflecting on yourself. You do not need to accept any claim about unseen powers to enjoy it. Where to read next: Scholem's Major Trends in Jewish Mysticism, Yates's Giordano Bruno and the Hermetic Tradition, and Hanegraaff's Western Esotericism.")],
 [("What is the best first question about a claim of ancient origin?", ["Where does it first appear in the sources?", "Who likes it?", "How old is the paper?", "How pretty is it?"], 0, "Look for the earliest evidence."),
  ("When did the Tarot-letter link originate?", ["19th century", "Ancient Egypt", "Medieval Spain", "Classical Greece"], 0, "French occultists."),
  ("What is syncretism?", ["Blending traditions into one", "Splitting a text", "A kind of ritual", "A Hebrew letter"], 0, "A blend."),
  ("Who wrote Major Trends in Jewish Mysticism?", ["Gershom Scholem", "Crowley", "Fortune", "Waite"], 0, "A historian."),
  ("Is a gematria match evidence for a claim?", ["No, it is wordplay", "Yes", "Only in Hebrew", "Only for names"], 0, "Coincidences abound."),
  ("A reasonable use of the Tree today is...", ["As a symbol map for memory and reflection", "As a medical guide", "As a legal source", "As a weather forecast"], 0, "A tool for thinking.")],
 [("Scholem", "Jewish Kabbalah scholar"), ("Yates", "Hermetic Renaissance"), ("Hanegraaff", "Western esotericism"), ("Syncretism", "blending traditions")],
 [MATCH("Match the scholar", "Pair each scholar with their field.", [("Gershom Scholem", "Jewish Kabbalah"), ("Frances Yates", "Renaissance Hermeticism"), ("Wouter Hanegraaff", "Western esotericism")]),
  ORDER("Check a claim", "Put the steps in order.", ["State the claim", "Find the earliest source", "Check its date", "Compare other evidence", "Decide how confident to be"]),
  FILL("Wrap up", "The Hermetic Qabalah is a {{modern}} synthesis built from older parts. Treat matching sums and tables as {{wordplay}} and symbols, not as proof."),
  PL("Layers of the system", "Write layer_date(layer): return the approximate earliest date for each layer as a string: 'letters and sephiroth' '2nd-6th century', 'Zohar' '13th century', 'Hermetica' '2nd-3rd century', 'Tarot cards' '15th century', 'Tarot-letter link' '19th century', 'Golden Dawn' '1888'. Return 'unknown' for anything else.", "layer_date(layer)", '''
def layer_date(layer):
    table = {"letters and sephiroth": "2nd-6th century", "Zohar": "13th century", "Hermetica": "2nd-3rd century", "Tarot cards": "15th century", "Tarot-letter link": "19th century", "Golden Dawn": "1888"}
    if layer in table:
        return table[layer]
    return "unknown"
''', [["Zohar"], ["Tarot cards"], ["Tarot-letter link"], ["Golden Dawn"], ["Emerald Tablet"]], "A lookup table."),
  PL("Newest layer", "Write newest(years): a list of [name, year] pairs. Return the name with the largest year. If the list is empty return an empty string.", "newest(years)", '''
def newest(years):
    best = ""
    by = -1
    for p in years:
        if p[1] > by:
            by = p[1]
            best = p[0]
    return best
''', [[[["Zohar", 1290], ["Tarot cards", 1440], ["Golden Dawn", 1888]]], [[]], [[["a", 5]]]], "Keep track of the largest year seen.")]
))
