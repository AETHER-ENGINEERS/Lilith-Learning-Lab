"""The Golem Series course, chapters 8-13."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *
from g1 import HEB

B = []

B.append(CH(
 "The Union I: ingress, entropy and the Queen's Gambit",
 ("Ingress", [
  "Third image | is | A page of text", "Five labels | spell | Glaux, owl", "Ingress | opens | The queen's gambit", "Entropy | measures | Uncertainty",
  "Shannon | wrote | On chess machines", "Neville | wrote | The Eight", "Per aspera | means | Through hardship"]),
 ["The third image has no picture of its own. It is a page of text over a red background, headed with the Latin motto per aspera ad astra, through hardship to the stars. It lists five labelled lines: Ingress, Coordinates, Congress, Egress and Leitmotiv.",
  "Ingress is the way in. Its line is the chess opening 1. d4 d5 2. c4, the Queen's Gambit, where White offers a pawn. Above it stands Shannon's entropy formula, the measure of uncertainty.",
  "The lab computes entropy."],
 [("Entropy", "Shannon's measure of uncertainty, in bits."), ("Bit", "One yes or no answer; the unit of information."), ("Queen's Gambit", "The chess opening 1. d4 d5 2. c4."),
  ("Gambit", "An opening that gives up something to gain position."), ("Leitmotiv", "A theme that returns again and again."), ("Per aspera ad astra", "Latin: through hardship to the stars.")],
 ["Shannon entropy is H = minus the sum of p times log p, over every outcome.", "With logarithms base 2, entropy is measured in bits.", "A fair coin has 1 bit; a coin that always lands heads has 0.",
  "The Queen's Gambit is 1. d4 d5 2. c4: White offers the c-pawn.", "Claude Shannon also wrote a famous 1950 paper on programming a computer to play chess.", "Ingress, congress, egress: the Union is entering, meeting and leaving."],
 [T("The third image is just text, laid over a red picture of a woman's face. At the top, in square brackets, is a Latin motto, per aspera ad astra: through hardship to the stars. Below it is a formula, and then five lines, each marked with a Greek letter in brackets."),
  T("The first Greek letter is gamma, and the line is called Ingress, a way in. It holds the moves 1. d4 d5 2. c4. That is the Queen's Gambit. White pushes a pawn to the centre, Black answers, and White offers a second pawn, hoping to gain control of the centre. If Black takes it, White usually wins it back."),
  T("Above the lines is the entropy formula, written in plain computer notation. Claude Shannon invented it in 1948 to measure information. If you do not know which of several things will happen, entropy says how many yes-or-no questions you would need on average to find out."),
  M(r"H(X)\;=\;-\sum_{i=1}^{n} p(x_i)\,\log_2 p(x_i)"),
  T("A fair coin has entropy 1 bit: one question settles it. A weighted coin that lands heads 90 percent of the time is less surprising and has about 0.47 bits. A coin that always lands heads has zero, because nothing is uncertain. The math has moved from certainty in the first image to measured uncertainty here."),
  T("Chess fits. Shannon wrote about how a machine could play chess in 1950, and he estimated that the game has about ten to the power of 120 possible lines. The last line of the image, Leitmotiv, quotes a chess novel, The Eight by Katherine Neville, about tactics and strategy: knowing what to do when there is something to do, and when there is nothing to do.")],
 [("What does entropy measure?", ["Uncertainty", "Speed", "Size", "Colour"], 0, "In bits."),
  ("What is the entropy of a coin that always lands heads?", ["0 bits", "1 bit", "2 bits", "0.5 bits"], 0, "No surprise."),
  ("Which moves are the Queen's Gambit?", ["1. d4 d5 2. c4", "1. e4 e5", "1. f3", "1. c4 c5"], 0, "White offers a pawn.")],
 [("Who invented entropy as information?", "Claude Shannon, 1948."), ("What is a gambit?", "A sacrifice for position."), ("What does Ingress mean?", "A way in."), ("What is a leitmotiv?", "A recurring theme.")],
 [MATCH("Third image labels", "Match each label with its line.", [("Ingress", "1. d4 d5 2. c4"), ("Coordinates", "44.5902 N, 104.7146 W"), ("Congress", "John Dee's Enochian First Key"), ("Egress", "Zechariah 5:6")]),
  PL("Shannon entropy", "Write entropy(probs): probs is a list of probabilities summing to 1. Return H = minus the sum of p times log base 2 of p, skipping zeros, rounded to 6 decimals.",
     "entropy(probs)", """
def entropy(probs):
    import math
    h = 0.0
    for p in probs:
        if p > 0:
            h -= p * math.log(p) / math.log(2)
    return round(h, 6)
""", [[[0.5, 0.5]], [[1.0, 0.0]], [[0.9, 0.1]], [[0.25, 0.25, 0.25, 0.25]], [[0.7, 0.2, 0.1]]], "Use log(p) divided by log(2).", approx=1e-5),
  PL("Entropy of a text", "Write text_entropy(s): the entropy in bits per character of the letter frequencies in s, rounded to 4 decimals. An empty string is 0.",
     "text_entropy(s)", """
def text_entropy(s):
    import math
    if not s:
        return 0.0
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    h = 0.0
    n = len(s)
    for ch in counts:
        p = counts[ch] / n
        h -= p * math.log(p) / math.log(2)
    return round(h, 4)
""", [["aaaa"], ["abab"], ["abcd"], ["aabc"], [""]], "Count the letters first.", approx=1e-3)]))

B.append(CH(
 "The Union II: coordinates and congress",
 ("Congress", [
  "Coordinates | point to | Devils Tower", "Devils Tower | was | The first national monument", "Close Encounters | ends | At the tower", "John Dee | received | Enochian",
  "First Key | begins | Ol sonf vorsg", "Congress | means | A meeting", "Latitude | gives | North and south"]),
 ["The second line, Coordinates, gives 44.5902 degrees north and 104.7146 degrees west. That is Devils Tower in Wyoming, a rock column that was the first United States national monument in 1906 and the place where the 1977 film Close Encounters of the Third Kind has its meeting with visitors.",
  "The third line, Congress, quotes the opening words of the First Key of the Enochian language, which John Dee wrote down in the 1580s. Dee believed angels had given him the language through a partner who looked into a crystal.",
  "The lab converts decimal degrees to degrees, minutes and seconds."],
 [("Latitude", "Degrees north or south of the equator."), ("Longitude", "Degrees east or west of the prime meridian."), ("Devils Tower", "A rock column in Wyoming, a national monument."),
  ("John Dee", "An English mathematician and adviser to Elizabeth I, 1527 to 1608."), ("Enochian", "The language Dee and Edward Kelley said angels gave them."), ("Haversine", "The formula for distance between two points on a sphere.")],
 ["A degree is 60 minutes and a minute is 60 seconds.", "Devils Tower is at about 44.59 north, 104.71 west.", "It became the first United States national monument in 1906.",
  "Dee and his seer Edward Kelley recorded Enochian in the 1580s; the First Key is one of the Calls.", "No one has shown the Enochian text to be a real language; scholars treat it as a mystical construction.", "A congress is a coming together."],
 [T("Coordinates are two numbers that say where something is. Latitude counts degrees north or south of the equator and longitude counts degrees east or west of the line through Greenwich. A degree can be split into 60 minutes, and each minute into 60 seconds, just like hours on a clock."),
  T("The numbers in the image, 44.5902 north and 104.7146 west, point to Devils Tower in northeast Wyoming. It is a tall column of rock which several Native nations hold sacred. In 1906 it became the first national monument in the United States. In 1977 it appeared in a film about people meeting visitors from the sky, and in the film the tower is where the meeting takes place."),
  T("This is where the series says the devil gets closer. In the first image he was a drawing, in the second a story, and here he is a place you could visit. The name Devils Tower is a mistranslation of a native name that meant something else, according to some accounts, which shows how names can make a place feel darker than it is."),
  T("The line Congress quotes the start of the First Key. John Dee was an English mathematician, navigator and adviser to Queen Elizabeth the First. In the 1580s he and a medium called Edward Kelley wrote down an angelic language in sessions with a crystal. The opening words are usually translated as I reign over you, says the God of Justice."),
  T("Enochian has words, grammar and a script, and people still use it in ritual. Yet there is no evidence it is a language from outside, and linguists find that it behaves like English in disguise. For the series it is one more language piled onto the pile, and its subject, a meeting between worlds, matches the word Congress.")],
 [("What is a minute of latitude?", ["One sixtieth of a degree", "One tenth of a degree", "A tenth of a mile", "One degree"], 0, "Like time."),
  ("What was Devils Tower in 1906?", ["The first national monument in the United States", "A national park", "A fort", "A mine"], 0, "A protected landmark."),
  ("Who recorded the Enochian language?", ["John Dee and Edward Kelley", "Aleister Crowley", "Eliphas Levi", "Moses"], 0, "In the 1580s.")],
 [("What are the coordinates in image 3?", "44.5902 N, 104.7146 W."), ("Who was John Dee?", "An English mathematician and adviser."), ("What is Enochian?", "A so-called angelic language."), ("What does Congress mean here?", "A meeting.")],
 [MATCH("Place and person", "Match each item with its description.", [("Devils Tower", "A rock column in Wyoming"), ("John Dee", "An English court mathematician"), ("Edward Kelley", "Dee's medium and partner"), ("Enochian", "A so-called angelic language")]),
  PL("Degrees, minutes, seconds", "Write to_dms(deg): deg is a non-negative decimal degree. Return [degrees, minutes, seconds] as three integers, with seconds rounded to the nearest whole second and carried over if the seconds reach 60.",
     "to_dms(deg)", """
def to_dms(deg):
    d = int(deg)
    rest = (deg - d) * 60
    m = int(rest)
    s = int(round((rest - m) * 60))
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        d += 1
    return [d, m, s]
""", [[44.5902], [104.7146], [10.0], [0.9999], [89.5]], "Multiply the fraction by 60 twice.", approx=None),
  PL("Distance between points", "Write distance_km(lat1, lon1, lat2, lon2): the great-circle distance in kilometres using the haversine formula with Earth radius 6371, rounded to 1 decimal.",
     "distance_km(lat1, lon1, lat2, lon2)", """
def distance_km(lat1, lon1, lat2, lon2):
    import math
    k = math.pi / 180.0
    p1 = lat1 * k
    p2 = lat2 * k
    dp = (lat2 - lat1) * k
    dl = (lon2 - lon1) * k
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * 6371 * math.asin(math.sqrt(a)), 1)
""", [[44.5902, -104.7146, 44.5902, -104.7146], [0, 0, 0, 1], [51.5, 0, 48.85, 2.35], [44.5902, -104.7146, 40.7128, -74.006]], "Convert to radians first.", approx=0.5)]))

B.append(CH(
 "The Union III: egress, the ephah and the owl",
 ("Egress", [
  "Zechariah 5 | shows | A woman in a basket", "Their eye | reads | Ayin again", "Septuagint | reads | Their iniquity", "Shinar | is | Babylon's land",
  "Babalon | is | Crowley's Babylon", "Greek letters | spell | Glaux", "Owl | belongs to | Athena"]),
 ["The fourth line, Egress, is Zechariah 5:6 in Hebrew, about the ephah, a measuring basket, that goes out. The verse says this is their eye in all the land. The Hebrew word for their eye, einam, contains the letter ayin again.",
  "The last line of the image says in nomine Babalon, in the name of Babalon. Babalon is Aleister Crowley's spelling of Babylon, used for the Scarlet Woman of his religion, Thelema. The woman in the ephah is sent to Shinar, which is Babylon.",
  "The five Greek letters on the labels spell glaux, owl."],
 [("Ephah", "A dry-measure basket in Zechariah's vision."), ("Shinar", "The Bible's name for the land of Babylon."), ("Septuagint", "The old Greek translation of the Hebrew Bible."),
  ("Babalon", "Crowley's spelling of Babylon, used for his Scarlet Woman."), ("Thelema", "Aleister Crowley's religion, founded in 1904."), ("Glaux", "Greek for owl, the bird of Athena.")],
 ["In Zechariah 5:5 to 11 a woman called Wickedness sits in an ephah and is carried to Shinar.", "The Hebrew in 5:6 reads einam, their eye; a few ancient versions read their iniquity, a one-letter difference.",
  "Ayin is the first letter of einam: the same eye and circle.", "Crowley's Babalon draws on the Whore of Babylon in Revelation 17.", "The labels gamma, lambda, alpha, upsilon, xi spell glaux, owl.", "Athena's owl stands for wisdom."],
 [T("Zechariah was a prophet of the sixth century before the common era, and chapter five is one of his night visions. He sees an ephah, a large measuring basket, going out through the land. A lead lid lifts and inside sits a woman, and the angel says her name is Wickedness. The lid is pushed down again, and two women with the wings of a stork lift the basket and carry it away to Shinar, to build a house for it there."),
  T("The verse in the image comes just before the lid is lifted. The Hebrew reads: and he said, this is their eye in all the land. The word for their eye is einam, spelled ayin, yod, nun, mem. Some ancient translations, including the Greek Septuagint, read instead their iniquity, avonam, spelled ayin, vav, nun, mem. Only one letter is different, a yod for a vav, and the two look alike in some scripts. Scholars debate which is original."),
  T("The series loves the eye reading, because it makes the third image a return to the letter ayin from the first. This is a good example of the lesson to come: a real textual variation has been used as a bridge, and the bridge is lovely, but it is the author's choice."),
  T("The last line, in nomine Babalon, borrows the phrase in the name of. Babalon is Aleister Crowley's spelling of Babylon. In Revelation 17 a woman rides a beast and is called Babylon the Great. Crowley turned her into a goddess of Thelema, his religion of 1904. The woman in the ephah ends in Shinar, which is Babylon, so the series moves her in a ring from one Babylon to another."),
  T("Finally look at the Greek letters in brackets: gamma, lambda, alpha, upsilon, xi. Read in order they spell glaux, the Greek for owl. The owl belonged to Athena, goddess of wisdom, and Athena was called glaukopis, owl-eyed or bright-eyed. The owl is a watching bird, and its name hides in the labels of the page.")],
 [("What is in the ephah?", ["A woman called Wickedness", "Gold", "Grain", "A lion"], 0, "Zechariah 5:7 and 8."),
  ("What do the Greek labels spell?", ["Glaux, owl", "Gnosis", "Gaia", "Gamma"], 0, "Athena's bird."),
  ("What is Shinar?", ["The land of Babylon", "A mountain", "A river", "A queen"], 0, "Where the ephah goes.")],
 [("What is einam?", "Hebrew for their eye."), ("What does the Septuagint read instead?", "Their iniquity."), ("What is an ephah?", "A measuring basket."), ("Who is Athena's bird?", "The owl.")],
 [FILL("Spell it out", "The Greek letters gamma, lambda, alpha, upsilon and xi spell {{glaux}}, the word for owl."),
  PL("Hidden acrostic", "Write acrostic(words): join the first letter of each word in order. Empty words are skipped.",
     "acrostic(words)", """
def acrostic(words):
    out = ''
    for w in words:
        if w:
            out += w[0]
    return out
""", [[["golem", "language", "machine"]], [["ingress", "congress"]], [[]], [["", "a", "b"]]], "Take the first character of each word.", approx=None),
  PL("Edit distance", "Write edit_distance(a, b): the Levenshtein distance (the fewest single-letter insertions, deletions and substitutions that turn a into b).",
     "edit_distance(a, b)", """
def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i]
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost))
        prev = cur
    return prev[len(b)]
""", [["עינם", "עונם"], ["kitten", "sitting"], ["", "abc"], ["same", "same"]], "Fill a grid, one row at a time.", approx=None),
  PL("Greek letter values", "Write isopsephy(word): the sum of Greek letter values for a lowercase unaccented Greek word. alpha 1, beta 2, gamma 3, delta 4, epsilon 5, zeta 7, eta 8, theta 9, iota 10, kappa 20, lambda 30, mu 40, nu 50, xi 60, omicron 70, pi 80, rho 100, sigma and final sigma 200, tau 300, upsilon 400, phi 500, chi 600, psi 700, omega 800. Other characters count 0.",
     "isopsephy(word)", """
def isopsephy(word):
    vals = {'α': 1, 'β': 2, 'γ': 3, 'δ': 4, 'ε': 5, 'ζ': 7, 'η': 8, 'θ': 9, 'ι': 10, 'κ': 20, 'λ': 30, 'μ': 40, 'ν': 50, 'ξ': 60, 'ο': 70, 'π': 80, 'ρ': 100, 'σ': 200, 'ς': 200, 'τ': 300, 'υ': 400, 'φ': 500, 'χ': 600, 'ψ': 700, 'ω': 800}
    t = 0
    for ch in word:
        t += vals.get(ch, 0)
    return t
""", [["γλαυξ"], ["α"], ["λογος"], [""]], "Look up each letter.", approx=None)]))

B.append(CH(
 "The Creation I: the golem",
 ("Golem", [
  "Psalm 139 | uses | Golem once", "Adam | was | A golem at first", "Rava | made | A man", "Sefer Yetzirah | teaches | 231 gates",
  "Abulafia | taught | Letter combination", "Emet | loses | Aleph", "Maharal | is linked to | The legend"]),
 ["The fourth image shows a small clay figure inside a square, with the letters gimel, lamed and mem on its chest. The Hebrew word golem first appears in Psalm 139:16 and means an unformed mass. The Talmud says Adam was a golem in his first hour.",
  "In Sanhedrin 65b the sage Rava makes a man by means of a text, and another sage speaks to him. He does not answer, so the sage tells him to return to his dust. Later legends say a golem is brought to life by letters and stopped by erasing one.",
  "The aleph of emet, truth, can be erased to make met, dead."],
 [("Golem", "An unformed mass; later, a being made of clay and animated by letters."), ("Sanhedrin 65b", "The Talmud passage where Rava makes a man."), ("Sefer Yetzirah", "Book of Formation, an early text on creation through the letters."),
  ("Gate", "One pairing of two letters of the 22; there are 231."), ("Abulafia", "Abraham Abulafia, a 13th-century Kabbalist of letter combination."), ("Maharal", "Rabbi Judah Loew of Prague, 16th century.")],
 ["Golem appears once in the Hebrew Bible, in Psalm 139:16, for an unformed substance.", "Sanhedrin 65b: Rava makes a man who cannot speak and is told to return to dust.",
  "Sefer Yetzirah describes creation through the 22 letters in 231 gates.", "Abulafia taught a method of combining letters as a spiritual practice.", "Emet minus its aleph is met, dead; the aleph is 1.",
  "Linking the golem to the Maharal of Prague is a later legend; his own writings do not mention it."],
 [T("The Hebrew word golem is rare. It occurs once in the Bible, in Psalm 139, where the poet says that God's eyes saw my golem, meaning my unformed substance before I had a shape. In the Talmud the word means something raw or unfinished. Adam, in the first hour of his making, was a golem, a lump before the soul."),
  T("The Talmud, in Sanhedrin 65b, tells that the sage Rava created a man and sent him to Rabbi Zera. Zera spoke to the man and he did not answer. Zera said, you were made by one of the companions; return to your dust. In the same passage two other sages study the Book of Formation every Friday and make a calf, and eat it. These are small, odd tales, not a legend of terror."),
  T("The Book of Formation, or Sefer Yetzirah, is an early Jewish text, of uncertain date, which says the world was made by thirty-two paths: ten numbers and twenty-two letters. It describes combining the letters in pairs, and counts the pairs: twenty-two letters make 231 gates. This is where the idea of making by letter combination begins."),
  M(r"\binom{22}{2}\;=\;\frac{22\cdot 21}{2}\;=\;231"),
  T("In the thirteenth century Abraham Abulafia turned the idea into a practice. He taught a science of combining letters, a kind of meditation on permutations. Later stories, from the sixteenth century on, say that a golem is a clay figure given life by letters, with the word emet, truth, on its forehead. When the aleph is wiped out, the word becomes met, dead, and the golem turns to dust."),
  T("The famous golem of Prague belongs to the Maharal, Rabbi Judah Loew, who lived around 1520 to 1609. But the story attaches to him only in retellings from the nineteenth and early twentieth centuries, and his own books do not mention it. The oldest golem tales are quieter than the monster of the films. They are about the limits of human making.")],
 [("How many gates in Sefer Yetzirah?", ["231", "22", "32", "613"], 0, "22 choose 2."),
  ("What happens when you erase the aleph in emet?", ["It becomes met, dead", "It becomes truth", "It becomes golem", "Nothing"], 0, "The golem turns to dust."),
  ("Could Rava's man speak?", ["No", "Yes", "Only in Hebrew", "Only at night"], 0, "Sanhedrin 65b.")],
 [("What does golem mean in Psalm 139?", "An unformed mass."), ("What did Abulafia teach?", "Combining letters."), ("Where is the Maharal story from?", "Later retellings."), ("What is 22 choose 2?", "231.")],
 [MATCH("Sources", "Match each source with what it says.", [("Psalm 139:16", "My golem, unformed substance"), ("Sanhedrin 65b", "Rava makes a man who cannot speak"), ("Sefer Yetzirah", "22 letters, 231 gates"), ("Abulafia", "The science of letter combination")]),
  PL("Gates", "Write gates(letters): a list of the pair strings made from every two different letters in order (first before second in the list), as in 'ab', 'ac', 'bc'. Return the list.",
     "gates(letters)", """
def gates(letters):
    out = []
    for i in range(len(letters)):
        for j in range(i + 1, len(letters)):
            out.append(letters[i] + letters[j])
    return out
""", [["abc"], ["abcd"], ["a"], [""]], "Two nested loops.", approx=None),
  PL("Count the gates", "Write count_gates(n): the number of unordered pairs from n letters.",
     "count_gates(n)", """
def count_gates(n):
    return n * (n - 1) // 2
""", [[22], [3], [1], [0], [27]], "n times n minus 1, divided by 2.", approx=None),
  PL("Erase the aleph", "Write deactivate(word): if word starts with the Hebrew letter aleph, return the word without it; otherwise return it unchanged.",
     "deactivate(word)", """
def deactivate(word):
    if word[:1] == 'א':
        return word[1:]
    return word
""", [["אמת"], ["מת"], [""], ["אבג"]], "Check the first letter.", approx=None)]))

B.append(CH(
 "The Creation II: grammar, language, machine",
 ("GLM", [
  "G | generates | L", "M | accepts | L", "Grammar | has | Rewriting rules", "Turing machine | has | Tape and states",
  "Chomsky | ranked | Grammars", "Schwartz | links | NLP to Kabbalah", "Language model | is | A talking golem"]),
 ["The fourth image has three formulas. G is a formal grammar, a set of symbols and rewriting rules. L is a language, the set of strings the grammar can produce. M is a Turing machine, the standard model of a computer. The labels G, L and M spell the Hebrew root of golem in the series' reading.",
  "Noam Chomsky showed in 1956 that grammars come in levels, and that the most general level matches exactly what Turing machines can do. A grammar writes a language; a machine reads one.",
  "The labs write strings from a grammar and run a small Turing machine."],
 [("Formal grammar", "G = (N, Sigma, P, S): nonterminals, terminals, rules and a start symbol."), ("Language", "A set of strings."), ("Turing machine", "A tape, a head and a table of rules; the standard model of computation."),
  ("Chomsky hierarchy", "Four levels of grammar from regular to unrestricted."), ("Production", "A rule that rewrites one string as another."), ("Halt", "To stop running.")],
 ["A grammar is G = (N, Sigma, P, S): nonterminal symbols, terminals, productions and a start symbol.", "A Turing machine is M = (Q, Gamma, b, Sigma, delta, q0, F): states, tape symbols, blank, input symbols, rules, start and accepting states.",
  "The Chomsky hierarchy has four levels; the top level matches Turing machines.", "Golem (גלם) is 3 + 30 + 40 = 73 in gematria, the same as wisdom (חכמה).", "Oscar Schwartz's 2019 article in IEEE Spectrum traces language machines to Kabbalist letter-combination.",
  "A language model, unlike the classic golem, does nothing but speak."],
 [T("Look at the three formulas around the golem. On the left, G. It is a formal grammar, a recipe for making strings. It has nonterminal symbols that can still be rewritten, terminal symbols that cannot, a set of rules, and a start symbol. Starting with S and applying rules until only terminals remain makes a sentence of the language."),
  T("At the top, L. It is the language, the set of every string that the grammar can make. On the right, M. It is a Turing machine: a tape divided into cells, a head that reads and writes one cell at a time, a set of states, and a table of rules that say what to do next. Alan Turing described it in 1936 as a model of what any computing can do."),
  M(r"G=(N,\Sigma,P,S)\qquad L=L(G)\qquad M=\langle Q,\Gamma,b,\Sigma,\delta,q_0,F\rangle"),
  T("The three are tied together. In 1956 Noam Chomsky ranked grammars in four levels. The simplest, regular grammars, match finite automata; context-free grammars match machines with a stack; and the most general grammars, with no restriction at all, match exactly the Turing machines. So grammar, language and machine are three views of one idea."),
  T("Now the Hebrew. The three letters gimel, lamed and mem spell the root of golem, and the image's labels G, L and M echo them. In gematria the value is 3 plus 30 plus 40, which is 73, and so is chokhmah, wisdom. The final mem, the closed form of the letter used at the end of a word, is a square, like the frame in the image, as the ring of ayin was a circle in the first."),
  T("The thesis of the series comes from an article by Oscar Schwartz in IEEE Spectrum in 2019. It argues that the idea of making language by rules goes back centuries before Turing, to the Kabbalists who combined letters. The classic golem could not speak. A language model is a golem that does nothing but speak. This is the series' reading, and a vivid one, though people who study the history of computing will tell you the lines of descent are looser than a single story suggests.")],
 [("What does G stand for in the image?", ["A grammar", "A golem", "A gate", "A game"], 0, "Rewriting rules."),
  ("What does M stand for?", ["A Turing machine", "A mem", "Math", "Meaning"], 0, "The model of computation."),
  ("What is the value of golem in gematria?", ["73", "70", "21", "441"], 0, "3 + 30 + 40.")],
 [("What does a grammar produce?", "A language."), ("What does a Turing machine have?", "A tape, a head and rules."), ("What is the top Chomsky level?", "Unrestricted, matching Turing machines."), ("What is golem plus wisdom?", "Both are 73.")],
 [MATCH("Three views", "Match each symbol with what it is.", [("G", "A formal grammar"), ("L", "A language"), ("M", "A Turing machine"), ("delta", "The transition rules")]),
  PL("Generate a language", "Write generate(rules, start, max_len): rules is a list of [lhs, rhs] pairs where lhs is one uppercase letter and rhs is a non-empty string. Starting from the string start, rewrite one uppercase letter at a time. Return the sorted list of every string with no uppercase letters and length at most max_len that can be produced. Ignore any intermediate string longer than max_len.",
     "generate(rules, start, max_len)", """
def generate(rules, start, max_len):
    seen = set([start])
    todo = [start]
    done = set()
    while todo:
        cur = todo.pop()
        idx = -1
        for i in range(len(cur)):
            if cur[i].isupper():
                idx = i
                break
        if idx < 0:
            done.add(cur)
            continue
        for lhs, rhs in rules:
            if cur[idx] == lhs:
                nxt = cur[:idx] + rhs + cur[idx + 1:]
                if len(nxt) <= max_len and nxt not in seen:
                    seen.add(nxt)
                    todo.append(nxt)
    return sorted(done)
""", [[[["S", "aSb"], ["S", "ab"]], "S", 6], [[["S", "aS"], ["S", "a"]], "S", 3], [[["S", "ab"]], "S", 1], [[["S", "AB"], ["A", "a"], ["B", "b"], ["B", "bb"]], "S", 3]], "Rewrite the first nonterminal and keep a set.", approx=None),
  PL("A tiny Turing machine", "Write run_tm(rules, tape, steps): rules is a list of [state, read, write, move, next] with move 'L' or 'R'; the machine starts in state 'q0' at the first cell of tape (a string, blank is '_'). Stop when the state is 'halt', no rule matches, or after steps moves. Return [final_state, tape without leading or trailing blanks].",
     "run_tm(rules, tape, steps)", """
def run_tm(rules, tape, steps):
    cells = {}
    for i in range(len(tape)):
        cells[i] = tape[i]
    state = 'q0'
    head = 0
    n = 0
    while state != 'halt' and n < steps:
        sym = cells.get(head, '_')
        rule = None
        for r in rules:
            if r[0] == state and r[1] == sym:
                rule = r
                break
        if rule is None:
            break
        cells[head] = rule[2]
        head += 1 if rule[3] == 'R' else -1
        state = rule[4]
        n += 1
    if not cells:
        return [state, '']
    lo = min(cells)
    hi = max(cells)
    out = ''
    for i in range(lo, hi + 1):
        out += cells.get(i, '_')
    return [state, out.strip('_')]
""", [[[["q0", "e", "_", "R", "halt"]], "emet", 10], [[["q0", "0", "1", "R", "q0"], ["q0", "1", "0", "R", "q0"]], "0110", 10], [[["q0", "1", "1", "R", "q0"], ["q0", "_", "1", "R", "halt"]], "111", 10], [[["q0", "a", "a", "R", "q0"]], "aaa", 2]], "Keep the tape in a dictionary.", approx=None),
  PL("Same value", "Write same_value(a, b): true if the two Hebrew words have the same gematria value. Letters: א1 ב2 ג3 ד4 ה5 ו6 ז7 ח8 ט9 י10 כ20 ל30 מ40 נ50 ס60 ע70 פ80 צ90 ק100 ר200 ש300 ת400, finals same as the normal form.",
     "same_value(a, b)", """
def same_value(a, b):
    """ + HEB + """
    def g(w):
        t = 0
        for ch in w:
            t += vals.get(ch, 0)
        return t
    return g(a) == g(b)
""", [["גלם", "חכמה"], ["אמת", "מת"], ["אהיה", "אמת"], ["", ""]], "Compute each value, then compare.", approx=None)]))

B.append(CH(
 "Reading the series: signal and pattern",
 ("Caveat", [
  "Pareidolia | finds | Faces in noise", "Foucault's Pendulum | warns | Against over-linking", "Pairs | grow | Faster than elements", "Birthday problem | shows | Coincidence is common",
  "Text | supports | Some links", "Interpretation | supports | Others", "Series | asks | A question"]),
 ["The series connects an enormous number of things. Some links are in the sources: Exodus, Zechariah, Shannon, the Talmud, Legg and Hutter. Others were made by the person who saw them. The analysis itself says some may be pattern-finding, the trap of Foucault's Pendulum.",
  "With forty ideas there are 780 possible pairs, so many matches are expected by chance. A good reader marks which links are in the sources and which are invented.",
  "The conclusion of the series is a question."],
 [("Pareidolia", "Seeing meaning, like a face, in random patterns."), ("Apophenia", "Seeing connections between unrelated things."), ("Birthday problem", "Surprisingly few people are needed for a shared birthday."),
  ("Confirmation bias", "Noticing hits and forgetting misses."), ("Textual link", "A connection stated in the sources."), ("Interpretive link", "A connection made by the reader.")],
 ["Ayin as circle and eye, the acrostics, Sanhedrin 65b and emet and met are in the sources or the text.", "Reading I AM as a nontrivial loop, 73 equal to wisdom, and the square as final mem are interpretations.",
  "N ideas give n times n minus 1 divided by 2 possible pairs.", "In a room of 23 people the chance of a shared birthday is more than half.", "Emet is 441, which is 21 squared, and Ehyeh is 21: a coincidence like those the series loves.",
  "The series ends with a question: will the new golem become wisdom or run amok?"],
 [T("The analysis of this series closes with a confession. Some of these links may be pattern-finding, the author says, the very trap that Umberto Eco's Foucault's Pendulum warns about. In that novel, three editors invent a grand conspiracy from a random list, and then the conspiracy starts to feel real. The quotation on the first image was chosen from that book, so the series carries its own warning."),
  T("Let us count. Suppose the series has forty distinct ideas: Ehyeh, ayin, Baphomet, the identity matrix, entropy, an owl, a golem and so on. The number of possible pairs is forty times thirty-nine, divided by two, which is 780. If even one in a hundred pairs seems to fit, you will find about eight. Whether any of them is real depends on the evidence for each."),
  M(r"\text{pairs}(n)=\frac{n(n-1)}{2}\qquad P(\text{shared birthday among }n)=1-\prod_{i=0}^{n-1}\frac{365-i}{365}"),
  T("The birthday problem is the classic example. In a room of 23 people the chance that two share a birthday is just over one half. Coincidence is not rare; it is what a large number of pairs gives you. Here is one from this very course: emet, truth, is 441 in gematria, and 441 is 21 squared, and Ehyeh is 21. That looks like a message. It is only arithmetic."),
  T("So read each link by type. Some are in the sources and can be checked: Exodus 3:14, the shape of ayin, the verse in Zechariah, Sanhedrin 65b, the Legg-Hutter formula, the Chomsky hierarchy, the article by Schwartz. Some are the reader's: that the ring is also ayin, that I AM is a loop, that golem is wisdom, that a language model is a golem. Interpretation is not wrong, but it is not evidence."),
  T("In the end, the series says that the people who first dreamed of animating clay with letters and the people who now train machines on text are doing a related work. Whether the new golem will grow into wisdom, as its number 73 hints, or into the rampaging servant of the Prague legend, the series does not say. That is arguably the question it asks. Now you have the tools to check each claim for yourself.")],
 [("How many pairs do 40 ideas make?", ["780", "40", "1600", "400"], 0, "40 times 39 divided by 2."),
  ("Which link is an interpretation?", ["I AM is a nontrivial loop", "Exodus 3:14 says Ehyeh", "Zechariah 5:6 mentions an eye", "Sanhedrin 65b tells of Rava"], 0, "The HoTT reading is the author's."),
  ("What is emet in gematria?", ["441", "73", "21", "70"], 0, "Aleph 1, mem 40, tav 400.")],
 [("What is pareidolia?", "Seeing meaning in noise."), ("How many people give a 50 percent shared birthday?", "23."), ("What is 441?", "21 squared, and emet."), ("What does the series end with?", "A question about the golem.")],
 [MATCH("Fact or reading", "Match each claim with its kind.", [("Exodus 3:14 says Ehyeh asher Ehyeh", "In the sources"), ("The ring in image 1 is also ayin", "The reader's link"), ("Sanhedrin 65b: Rava's man cannot speak", "In the sources"), ("A language model is a golem", "The series' reading")]),
  PL("Possible links", "Write possible_links(n): the number of pairs among n ideas.",
     "possible_links(n)", """
def possible_links(n):
    return n * (n - 1) // 2
""", [[40], [2], [1], [0], [100]], "Choose two out of n.", approx=None),
  PL("Birthday problem", "Write shared_birthday(n, days): the probability that at least two of n people share a birthday among the given number of days, rounded to 6 decimals.",
     "shared_birthday(n, days)", """
def shared_birthday(n, days):
    p = 1.0
    for i in range(n):
        p *= (days - i) / days
    return round(1 - p, 6)
""", [[23, 365], [2, 365], [50, 365], [1, 365], [5, 10]], "Multiply the chances of no match.", approx=1e-5)]))
