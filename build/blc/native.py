# -*- coding: utf-8 -*-
"""Adds the real Hebrew and Greek script beside transliterations in the grammar and comparison chapters."""
import re
from data import NOUNS, VERBS

HE = {
 "ha-": "הַ", "ve-": "וְ", "be-": "בְּ", "le-": "לְ", "min": "מִן", "mi-": "מִ",
 "melakhim": "מְלָכִים", "torah": "תּוֹרָה", "torot": "תּוֹרוֹת", "yadayim": "יָדַיִם", "banim": "בָּנִים", "ish": "אִישׁ", "anashim": "אֲנָשִׁים",
 "ha-melekh": "הַמֶּלֶךְ", "ha-aretz": "הָאָרֶץ", "gadol": "גָּדוֹל", "bet": "בֵּית", "devar": "דְּבַר", "adonai": "אֲדֹנָי",
 "tov": "טוֹב", "tovah": "טוֹבָה", "tovim": "טוֹבִים", "ishah": "אִשָּׁה", "ba-bayit": "בַּבַּיִת", "be-reshit": "בְּרֵאשִׁית", "bereshit": "בְּרֵאשִׁית",
 "bara": "בָּרָא", "ha-ish": "הָאִישׁ", "beti": "בֵּיתִי", "beto": "בֵּיתוֹ", "bit-kha": "בֵּיתְךָ", "derekh": "דֶּרֶךְ",
 "katav": "כָּתַב", "ktav": "כְּתָב", "mikhtav": "מִכְתָּב", "sofer": "סוֹפֵר", "shamar": "שָׁמַר", "mishmar": "מִשְׁמָר", "shalem": "שָׁלֵם", "shlomo": "שְׁלֹמֹה",
 "katavti": "כָּתַבְתִּי", "katavnu": "כָּתַבְנוּ", "katavta": "כָּתַבְתָּ", "katavt": "כָּתַבְתְּ", "ketavtem": "כְּתַבְתֶּם", "katvah": "כָּתְבָה", "katvu": "כָּתְבוּ",
 "ekhtov": "אֶכְתֹּב", "tikhtov": "תִּכְתֹּב", "yikhtov": "יִכְתֹּב", "nikhtov": "נִכְתֹּב", "nikhtav": "נִכְתַּב", "lamad": "לָמַד", "limed": "לִמֵּד",
 "malakh": "מָלַךְ", "himlikh": "הִמְלִיךְ", "vayomer": "וַיֹּאמֶר", "elohenu": "אֱלֹהֵינוּ", "hayah": "הָיָה",
 "ani": "אֲנִי", "atah": "אַתָּה", "anachnu": "אֲנַחְנוּ", "atem": "אַתֶּם",
 "echad": "אֶחָד", "shtayim": "שְׁתַּיִם", "shalosh": "שָׁלוֹשׁ", "arba": "אַרְבַּע", "chamesh": "חָמֵשׁ", "shesh": "שֵׁשׁ", "sheva": "שֶׁבַע", "shmoneh": "שְׁמוֹנֶה", "tesha": "תֵּשַׁע", "eser": "עֶשֶׂר",
 "eifo": "אֵיפֹה", "toda": "תּוֹדָה", "bevakasha": "בְּבַקָּשָׁה", "sefer": "סֵפֶר", "ahavah": "אַהֲבָה",
}
for r in NOUNS + VERBS:
    if len(r[2]) >= 5:
        HE.setdefault(r[2], r[1])
# short words that are also English words: only replaced in tables, pairs and listed phrases
HE_AMB = {"lo": "לֹא", "mi": "מִי", "mah": "מָה", "ken": "כֵּן", "hu": "הוּא", "hi": "הִיא", "hem": "הֵם", "at": "אַתְּ", "ve": "וְ", "ha": "הַ", "ben": "בֵּן", "am": "עַם", "or": "אוֹר", "em": "אֵם", "av": "אָב", "ir": "עִיר", "yad": "יָד"}

GR = {
 "ho": "ὁ", "tou": "τοῦ", "tes": "τῆς", "ton": "τόν", "theos": "θεός", "theou": "θεοῦ", "theon": "θεόν", "kosmon": "κόσμον", "kosmos": "κόσμος",
 "logos": "λόγος", "logou": "λόγου", "logo": "λόγῳ", "logon": "λόγον", "loge": "λόγε", "logoi": "λόγοι", "logois": "λόγοις", "logous": "λόγους",
 "agape": "ἀγάπη", "agapes": "ἀγάπης", "agapen": "ἀγάπην", "agapai": "ἀγάπαι", "agapa": "ἀγαπᾷ", "agapo": "ἀγαπῶ", "agapon": "ἀγαπῶν",
 "pros": "πρός", "dia": "διά", "luo": "λύω", "lueis": "λύεις", "luei": "λύει", "luomen": "λύομεν", "luete": "λύετε", "luousi": "λύουσι",
 "eluon": "ἔλυον", "eluse": "ἔλυσε", "luso": "λύσω", "luomai": "λύομαι", "luson": "λῦσον", "eimi": "εἰμί", "esti": "ἐστί", "esmen": "ἐσμέν", "este": "ἐστέ", "esti(n)": "ἐστί(ν)", "eisi(n)": "εἰσί(ν)", "shmone": "שְׁמוֹנֶה", "eisi": "εἰσί", "estin": "ἐστίν",
 "ego": "ἐγώ", "autos": "αὐτός", "hemeis": "ἡμεῖς", "autoi": "αὐτοί", "heis": "εἷς", "dyo": "δύο", "treis": "τρεῖς", "tessares": "τέσσαρες", "pente": "πέντε",
 "hepta": "ἑπτά", "okto": "ὀκτώ", "ennea": "ἐννέα", "chaire": "χαῖρε", "eucharisto": "εὐχαριστῶ", "parakalo": "παρακαλῶ", "eirene": "εἰρήνη", "hemera": "ἡμέρα", "kyrios": "κύριος",
}
for r in NOUNS + VERBS:
    if len(r[4]) >= 5:
        GR.setdefault(r[4], r[3])
GR_AMB = {"he": "ἡ", "to": "τό", "te": "τῇ", "en": "ἦν", "ei": "εἶ", "se": "σέ", "su": "σύ", "ou": "οὐ", "nai": "ναί", "hex": "ἕξ", "deka": "δέκα", "pater": "πατήρ", "dike": "δίκη", "phos": "φῶς"}

# exact prose snippets where an ambiguous short word is clearly the foreign one
PHRASES = {
 "ani, I; atah, you (m); at, you (f); hu, he; hi, she; anachnu, we; atem, you (pl); hem, they": "ani (אֲנִי), I; atah (אַתָּה), you (m); at (אַתְּ), you (f); hu (הוּא), he; hi (הִיא), she; anachnu (אֲנַחְנוּ), we; atem (אַתֶּם), you (pl); hem (הֵם), they",
 "Hebrew uses ani.": "Hebrew uses ani (אֲנִי).", "is atah (masculine, singular) in Hebrew, su in Greek and tu in Latin": "is atah (אַתָּה, masculine singular) in Hebrew, su (σύ) in Greek and tu in Latin",
 "Greek su and Latin tu": "Greek su (σύ) and Latin tu", "'We' is anachnu, hemeis and nos": "'We' is anachnu (אֲנַחְנוּ), hemeis (ἡμεῖς) and nos",
 "Greek says eimi, Latin says sum": "Greek says eimi (εἰμί), Latin says sum", "ha-melekh gadol": "ha-melekh gadol (הַמֶּלֶךְ גָּדוֹל)",
 "ho theos agapa ton kosmon": "ho theos agapa ton kosmon (ὁ θεὸς ἀγαπᾷ τὸν κόσμον)", "tou theou is of God": "tou theou (τοῦ θεοῦ) is of God", "to logo is by the word": "to logo (τῷ λόγῳ) is by the word",
 "pros ton theon": "pros ton theon (πρὸς τὸν θεόν)", "ho theos, God": "ho theos (ὁ θεός), God", "ton kosmon, the world": "ton kosmon (τὸν κόσμον), the world",
 "agapo se": "agapo se (ἀγαπῶ σε)", "the pronoun se (you)": "the pronoun se (σέ, you)", "Greek en ho logos": "Greek en ho logos (ἦν ὁ λόγος)", "ho theos agape estin": "ho theos agape estin (ὁ θεὸς ἀγάπη ἐστίν)",
 "ei, you are": "ei (εἶ), you are", "as en, was": "as en (ἦν), was", "En ho logos": "En ho logos (Ἦν ὁ λόγος)",
 "Bara elohim": "Bara elohim (בָּרָא אֱלֹהִים)", "bara elohim": "bara elohim (בָּרָא אֱלֹהִים)",
 "ha-ish tov": "ha-ish tov (הָאִישׁ טוֹב)", "ish tov": "ish tov (אִישׁ טוֹב)", "ishah tovah": "ishah tovah (אִשָּׁה טוֹבָה)", "anashim tovim": "anashim tovim (אֲנָשִׁים טוֹבִים)",
 "Vayomer elohim": "Vayomer elohim (וַיֹּאמֶר אֱלֹהִים)", "hayah (Hebrew), en (Greek, from eimi)": "hayah (הָיָה, Hebrew), en (ἦν, Greek, from eimi)",
 "devar adonai": "devar adonai (דְּבַר יְהוָה)", "bet ha-melekh": "bet ha-melekh (בֵּית הַמֶּלֶךְ)", "bet melekh": "bet melekh (בֵּית מֶלֶךְ)",
}

EXTRA_CELL = {"ten": "τήν", "ou(k)": "οὐ(κ)", "ve-": "וְ"}
ENG = {"he", "to", "at", "or", "am", "en", "ei", "no"}
_ALL = {}
_ALL.update(HE); _ALL.update(GR)
_AMB = {}
_AMB.update(HE_AMB); _AMB.update(GR_AMB)
_WORD = re.compile(r"(?<![\w\-])(" + "|".join(sorted((re.escape(k) for k in _ALL), key=len, reverse=True)) + r")(?![\w])", re.I)
_HAS_NATIVE = re.compile(r"[֐-׿Ͱ-Ͽἀ-῿]")


_CACHE = {}


def _rx(d):
    key = id(d)
    if key not in _CACHE:
        _CACHE[key] = re.compile(r"(?<![\w\-])(" + "|".join(sorted((re.escape(k) for k in d), key=len, reverse=True)) + r")(?![\w])", re.I)
    return _CACHE[key]


def prose(s, extra=None):
    """Add script after the first use of each safe word, plus listed phrases."""
    if not isinstance(s, str):
        return s
    d = _ALL if not extra else dict(_ALL, **extra)
    if extra:
        d = _CACHE.setdefault(("d", id(extra)), d)
    held = []
    for k, v in PHRASES.items():
        if k in s and v not in s:
            s = s.replace(k, "\x00%d\x00" % len(held), 1)
            held.append(v)
    seen = set()

    def rep(m):
        w = m.group(1).lower()
        nxt = s[m.end():m.end() + 14]
        if w in seen or (nxt[:2] == " (" or nxt[:1] == " ") and _HAS_NATIVE.search(nxt[:4]) and not nxt.lstrip().startswith("ha"):
            return m.group(0)
        seen.add(w)
        return "%s (%s)" % (m.group(1), d[w])
    s = _rx(d).sub(rep, s)
    for i, v in enumerate(held):
        s = s.replace("\x00%d\x00" % i, v)
    return s


def node(s, extra):
    """Concept-map node: add script after its first word when it is a letter or sign."""
    words = s.split(" ", 1)
    v = extra.get(words[0].lower()) if words else None
    if v and not _HAS_NATIVE.search(s):
        return "%s %s%s" % (words[0], v, " " + words[1] if len(words) > 1 else "")
    return s


def table(s):
    """Code blocks laid out in columns: a cell that is exactly one known word gets its script; other cells use the safe list."""
    if _HAS_NATIVE.search(s):
        return s
    out = []
    skip_first = s.lstrip().lower().startswith("english") or s.lstrip().lower().startswith("number")
    for line in s.split("\n"):
        parts = re.split(r"(\s{2,})", line)
        for i in range(2 if skip_first else 0, len(parts), 2):
            cell = parts[i]
            k = cell.strip().lower()
            if not k:
                continue
            v = _ALL.get(k) or _AMB.get(k) or EXTRA_CELL.get(k)
            if v:
                parts[i] = "%s %s" % (cell, v)
            else:
                parts[i] = _WORD.sub(lambda m: "%s %s" % (m.group(1), _ALL[m.group(1).lower()]), cell, count=1)
        out.append("".join(parts))
    return "\n".join(out)


PRON = {"she", "he", "i", "they", "we", "you", "you (m)", "you (f)", "you (pl)"}


def single(s, force=False):
    """A whole string that is exactly one transliterated word (match pairs, cards)."""
    if not isinstance(s, str) or _HAS_NATIVE.search(s):
        return s
    k = s.strip().lower()
    if k in ENG and not force:
        return s
    v = _ALL.get(k) or _AMB.get(k)
    return "%s  %s" % (s, v) if v else s


def _cut(x):
    out = []
    while len(x) > 420:
        i = x.rfind("), ", 0, 380)
        if i < 0:
            break
        out.append(x[:i + 2].rstrip(",") + ".")
        x = x[i + 3:]
        x = x[0].upper() + x[1:]
    return out + [x]


def apply(chs):
    for ci, ch in enumerate(chs):
        ex = LETTER_CH.get(ci)
        for blk in ch["lesson"]:
            if blk["type"] == "text":
                blk["items"] = [y for x in blk["items"] for y in _cut(prose(x, ex))]
            elif blk["type"] == "code" and blk.get("lang", "text") == "text":
                blk["code"] = table(blk["code"])
        ch["summary"] = [prose(x, ex) for x in ch["summary"]]
        ch["keyPoints"] = [prose(x, ex) for x in ch["keyPoints"]]
        for g in ch["glossary"]:
            g["def"] = prose(g["def"], ex)
            if ex:
                g["term"] = node(g["term"], ex)
        if ex:
            for m in ch["maps"]:
                m["links"] = [" | ".join(node(part, ex) for part in l.split(" | ")) for l in m["links"]]
        for q in ch["quiz"]:
            q["q"] = prose(q["q"])
            q["options"] = [single(o) for o in q["options"]]
        for c in ch["cards"]:
            c["q"] = prose(c["q"]); c["a"] = prose(c["a"])
        for p in ch["practice"]:
            if p.get("type") == "match":
                p["pairs"] = [[single(a, b.lower() in PRON), single(b)] for a, b in p["pairs"]]
    return chs


HE_LETTERS = {"alef": "א", "bet": "ב", "gimel": "ג", "dalet": "ד", "vav": "ו", "zayin": "ז", "chet": "ח", "tet": "ט", "yod": "י", "kaf": "כ", "lamed": "ל",
 "mem": "מ", "nun": "נ", "samekh": "ס", "ayin": "ע", "pe": "פ", "tsade": "צ", "qof": "ק", "resh": "ר", "shin": "ש", "tav": "ת", "sin": "שׂ"}
HE_VOWELS = {"patach": "◌ַ", "kamets": "◌ָ", "tsere": "◌ֵ", "segol": "◌ֶ", "hiriq": "◌ִ", "holam": "◌ֹ", "kubbuts": "◌ֻ", "shureq": "וּ", "shva": "◌ְ", "dagesh": "◌ּ", "niqqud": "נִקּוּד"}
GR_LETTERS = {"alpha": "Α α", "beta": "Β β", "gamma": "Γ γ", "delta": "Δ δ", "epsilon": "Ε ε", "zeta": "Ζ ζ", "eta": "Η η", "theta": "Θ θ", "iota": "Ι ι", "kappa": "Κ κ",
 "lambda": "Λ λ", "mu": "Μ μ", "nu": "Ν ν", "xi": "Ξ ξ", "omicron": "Ο ο", "pi": "Π π", "rho": "Ρ ρ", "sigma": "Σ σ ς", "tau": "Τ τ", "upsilon": "Υ υ", "phi": "Φ φ",
 "chi": "Χ χ", "psi": "Ψ ψ", "omega": "Ω ω"}
LETTER_CH = {1: dict(HE_LETTERS), 2: dict(HE_LETTERS, **HE_VOWELS), 5: dict(GR_LETTERS)}
