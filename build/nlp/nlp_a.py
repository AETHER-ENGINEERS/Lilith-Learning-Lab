# -*- coding: utf-8 -*-
"""NLP course, part 1: text basics, TF-IDF, n-gram models, classification, linguistic structure."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Text as data: tokens, normalisation and patterns",
 ("Text basics", [
  "Corpus | is | A collection of texts",
  "Token | is | A unit of text",
  "Normalisation | reduces | Variation",
  "Stopword | is | A very common word",
  "Stemming | chops | Suffixes",
  "Lemma | is | Dictionary form",
  "Regex | matches | Patterns"]),
 ["Natural language processing (NLP) lets computers work with human language. Text is first split into tokens (words, pieces of words or characters) and normalised: lower-cased, stripped of punctuation, perhaps reduced to stems or lemmas.",
  "Counting words already reveals a lot, and Zipf's law says a few words are extremely common while most are rare.",
  "Classical NLP is a pipeline of such steps; modern NLP learns many of them end to end, but tokenisation and data hygiene still matter."],
 [("Token", "A unit of text produced by tokenisation: a word, subword, punctuation mark or character."),
  ("Corpus", "A large collection of texts used for analysis or training."),
  ("Stemming", "Cutting off word endings by rule, so 'running' and 'runs' become 'run'."),
  ("Lemmatisation", "Reducing a word to its dictionary form using vocabulary and grammar, so 'better' becomes 'good'."),
  ("Regular expression", "A compact pattern language for matching text.")],
 ["Tokenise, lower-case, remove noise.",
  "Stem is a chopped root; lemma is a real word.",
  "Zipf: frequency is about 1 / rank.",
  "Out-of-vocabulary words are a problem for word-level models.",
  "Subword tokens fix that."],
 [T("A tweet, a medical report, a legal contract, a novel: all are strings of characters. To compute with them we must decide what the pieces are. The first step is tokenisation. In English, splitting on spaces and peeling off punctuation gets you far, but 'don't', 'New York', 'state-of-the-art' and a URL all raise questions. Languages without spaces, such as Chinese or Japanese, need other methods."),
  T("Normalisation reduces variation. Lower-casing makes 'The' and 'the' one word. Stripping accents, expanding contractions and fixing spelling help in some tasks and hurt in others: 'US' and 'us' are different. Stopwords such as 'the', 'of' and 'and' carry little meaning for search and topic tasks and are often removed, though modern models keep them."),
  C("import re, collections\ntext = 'The cats are running. The dog runs fast!'\ntokens = re.findall(r\"[a-z']+\", text.lower())\nprint(tokens)\nprint(collections.Counter(tokens).most_common(3))\n\nimport nltk\nfrom nltk.stem import PorterStemmer, WordNetLemmatizer\nprint(PorterStemmer().stem('running'))          # run\nprint(WordNetLemmatizer().lemmatize('geese'))   # goose", "python"),
  T("Stemming and lemmatisation merge forms of one word. A stemmer such as Porter's chops suffixes by rules, so 'caresses' becomes 'caress' and 'running' becomes 'run', sometimes producing non-words like 'happi'. A lemmatiser uses a dictionary and the part of speech to return real forms: 'geese' becomes 'goose' and 'better' becomes 'good'. Stemmers are fast; lemmatisers are more accurate."),
  T("Counting words reveals Zipf's law: the most frequent word occurs about twice as often as the second, three times as often as the third, and so on, leaving a long tail of rare words, many appearing once. This is why word-level vocabularies struggle with unseen words, and why modern systems split text into subword pieces. Regular expressions, patterns such as digits followed by a percent sign, remain the Swiss army knife for extracting dates, prices and codes.")],
 [("What is tokenisation?", ["Splitting text into units", "Translating", "Deleting words", "Counting letters only"], 0, "First step."),
  ("What is a stopword?", ["A very common low-content word", "A rare word", "A verb", "A name"], 0, "The, of, and."),
  ("How does a stemmer differ from a lemmatiser?", ["It chops endings by rule", "It uses a neural network", "It translates", "It sorts"], 0, "May give non-words."),
  ("What does Zipf's law say?", ["A few words are very frequent, most are rare", "All words are equal", "Words are random", "Long words dominate"], 0, "Long tail."),
  ("Why subword tokens?", ["They handle unseen words", "They are shorter", "They remove punctuation", "They are alphabetical"], 0, "Out-of-vocabulary."),
  ("What are regular expressions for?", ["Matching text patterns", "Training models", "Drawing", "Sorting"], 0, "Extract dates and prices.")],
 [("re.findall(r'\\w+', s)", "split into words"), ("Counter(tokens)", "word counts"), ("PorterStemmer().stem(w)", "stem a word")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Token", "unit of text"), ("Stopword", "very common word"), ("Stemming", "chop endings by rule"), ("Lemma", "dictionary form"), ("Corpus", "collection of texts")]),
  PL("Tokenise", "Write tokenize(text): lower-case the text and return the list of tokens, where a token is a maximal run of letters, digits or apostrophes. Everything else separates tokens.", "tokenize(text)", '''
def tokenize(text):
    out = []
    cur = ''
    for ch in text.lower():
        if ch.isalpha() or ch.isdigit() or ch == "'":
            cur = cur + ch
        else:
            if cur != '':
                out.append(cur)
            cur = ''
    if cur != '':
        out.append(cur)
    return out
''', [['The cats are running. The dog runs fast!'], ["Don't stop, it's 5 o'clock"], [''], ['A-B  C']], "Build tokens character by character."),
  PL("Word frequencies", "Write top_words(tokens, n): the n most frequent tokens as [token, count] pairs, ordered by count descending then token alphabetically.", "top_words(tokens, n)", '''
def top_words(tokens, n):
    d = {}
    for t in tokens:
        d[t] = d.get(t, 0) + 1
    items = sorted(d.items(), key=lambda p: (-p[1], p[0]))
    return [[k, v] for k, v in items[:n]]
''', [[['a', 'b', 'a', 'c', 'b', 'a'], 2], [['x'], 3], [['b', 'a'], 2]], "Sort by count then by word."),
  PL("Remove stopwords", "Write remove_stop(tokens, stop): the tokens that are not in the list stop.", "remove_stop(tokens, stop)", '''
def remove_stop(tokens, stop):
    return [t for t in tokens if t not in stop]
''', [[['the', 'cat', 'sat', 'on', 'the', 'mat'], ['the', 'on']], [['a'], []], [['a', 'b'], ['a', 'b']]], "Filter by membership."),
  PL("Tiny stemmer", "Write stem(word): remove the first matching suffix from this list in order: 'ing', 'ed', 'ly', 'es', 's', but only if at least 3 letters remain; if the word then ends in two identical consonant letters (like 'runn'), drop one of them.", "stem(word)", '''
def stem(word):
    for suf in ['ing', 'ed', 'ly', 'es', 's']:
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            w = word[:-len(suf)]
            if len(w) >= 2 and w[-1] == w[-2] and w[-1] not in 'aeiou':
                w = w[:-1]
            return w
    return word
''', [['running'], ['jumped'], ['quickly'], ['cats'], ['boxes'], ['sing'], ['class']], "Check suffixes in order."),
  PL("Character n-grams", "Write char_ngrams(word, n): all substrings of length n of the word padded with '<' at the start and '>' at the end.", "char_ngrams(word, n)", '''
def char_ngrams(word, n):
    w = '<' + word + '>'
    return [w[i:i + n] for i in range(len(w) - n + 1)]
''', [['cat', 3], ['hi', 2], ['a', 3]], "Slide a window over the padded word."),
  PL("Sentence split", "Write sentences(text): split the text into sentences at '.', '!' or '?' followed by a space or the end; strip surrounding spaces and drop empty pieces. Keep the ending punctuation with its sentence.", "sentences(text)", '''
def sentences(text):
    out = []
    cur = ''
    n = len(text)
    for i in range(n):
        cur = cur + text[i]
        if text[i] in '.!?' and (i == n - 1 or text[i + 1] == ' '):
            s = cur.strip()
            if s != '':
                out.append(s)
            cur = ''
    s = cur.strip()
    if s != '':
        out.append(s)
    return out
''', [['Hello there. How are you? Fine!'], ['No end'], ['One.']], "Cut after sentence-ending marks."),
  PL("Zipf check", "Write zipf(counts): given word counts sorted descending, return the list of count x rank for each word, which should be roughly constant for Zipfian text.", "zipf(counts)", '''
def zipf(counts):
    return [counts[i] * (i + 1) for i in range(len(counts))]
''', [[[100, 50, 33, 25]], [[10]], [[8, 4, 2]]], "Rank starts at 1.")]
))

CHS.append(CH(
 "Bag of words, TF-IDF and similarity",
 ("Vectors", [
  "Bag of words | counts | Words per document",
  "TF | is | Term frequency",
  "IDF | down-weights | Common terms",
  "TF-IDF | scores | Importance",
  "Cosine | compares | Direction",
  "Edit distance | counts | Character edits",
  "Search | ranks | Documents"]),
 ["The bag-of-words model describes a document by how often each word occurs, ignoring order. TF-IDF multiplies term frequency by inverse document frequency, so words that are common everywhere count for little and distinctive words count for a lot.",
  "Cosine similarity compares two document vectors by the angle between them, regardless of document length. Ranking documents by similarity to a query is the basis of classic search.",
  "Edit distance (Levenshtein) measures how many insertions, deletions and substitutions turn one string into another, useful for spelling correction."],
 [("Bag of words", "A representation of text as word counts, discarding order."),
  ("TF-IDF", "Term frequency times inverse document frequency; high for words frequent in a document but rare overall."),
  ("Cosine similarity", "The cosine of the angle between two vectors; 1 means the same direction."),
  ("Sparse vector", "A vector with mostly zeros, as in bag-of-words with a large vocabulary."),
  ("Levenshtein distance", "The minimum number of single-character edits to turn one string into another.")],
 ["tfidf = tf x log(N / df).",
  "cos = a.b / (|a||b|).",
  "Sparse vectors: store only non-zeros.",
  "Query and documents in the same space.",
  "Edit distance by dynamic programming."],
 [T("How would you find the document most about 'volcano' in a library of ten thousand? A first idea: count the word. But long documents win, and 'the' wins everything. TF-IDF fixes both. The term frequency, how often a word appears in this document, is divided by the length. The inverse document frequency is the logarithm of the number of documents divided by the number containing the word. A word in every document has IDF zero; a rare, telling word has a large one."),
  C("from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.metrics.pairwise import cosine_similarity\n\ndocs = ['the volcano erupted', 'the cat sat on the mat', 'volcano ash covered the town']\nvec = TfidfVectorizer()\nX = vec.fit_transform(docs)\nq = vec.transform(['volcano ash'])\nprint(cosine_similarity(q, X))", "python"),
  T("Each document becomes a vector with one position per vocabulary word. The vectors are huge and nearly all zeros, so we store them sparsely. To compare two vectors we use the cosine of the angle between them: the dot product divided by the product of their lengths. Two documents using the same words in similar proportions point the same way, however long they are."),
  T("A search engine of this kind embeds the query as a vector too and ranks documents by cosine similarity, or by refinements such as BM25. It knows nothing about meaning: 'car' and 'automobile' share no dimension, so a query for one misses the other. That limitation motivates the embeddings of Chapter 6."),
  T("A different kind of similarity is between spellings. The Levenshtein edit distance counts the fewest single-character insertions, deletions and substitutions that turn one string into another: 'kitten' to 'sitting' is three. A table filled by dynamic programming computes it. Spell checkers suggest the dictionary words within one or two edits of what you typed.")],
 [("What does bag of words ignore?", ["Word order", "Word counts", "Vocabulary", "Spelling"], 0, "Only counts."),
  ("What does a high IDF mean?", ["The word is rare across documents", "The word is common", "The document is long", "The word is a name"], 0, "Distinctive."),
  ("What does cosine similarity of 1 mean?", ["Same direction", "Opposite", "Unrelated", "Zero length"], 0, "Angle 0."),
  ("Why divide by vector length in cosine?", ["To ignore document length", "To add noise", "To sort", "To stem"], 0, "Normalise."),
  ("What is a limitation of TF-IDF?", ["It knows no synonyms", "It is slow", "It needs images", "It ignores counts"], 0, "Car vs automobile."),
  ("What is the edit distance from kitten to sitting?", ["3", "1", "7", "0"], 0, "s, e->i, add g.")],
 [("tf x log(N/df)", "TF-IDF"), ("cos = a.b/(|a||b|)", "cosine similarity"), ("TfidfVectorizer()", "scikit-learn TF-IDF")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("TF", "count in this document"), ("IDF", "rarity across documents"), ("Cosine", "angle between vectors"), ("Sparse", "mostly zeros"), ("Levenshtein", "character edit count")]),
  PL("Bag of words vector", "Write bow(tokens, vocab): the list of counts of each vocab word in the tokens.", "bow(tokens, vocab)", '''
def bow(tokens, vocab):
    return [tokens.count(w) for w in vocab]
''', [[['a', 'b', 'a'], ['a', 'b', 'c']], [[], ['x']], [['z', 'z'], ['z']]], "Count each vocabulary word."),
  PL("Inverse document frequency", "Write idf(docs, term): log(N / df) where N is the number of documents (lists of tokens) and df the number containing the term; rounded to 4 decimals. If df is 0 return 0.", "idf(docs, term)", '''
import math
def idf(docs, term):
    df = 0
    for d in docs:
        if term in d:
            df = df + 1
    if df == 0:
        return 0
    return round(math.log(len(docs) / float(df)), 4)
''', [[[['a', 'b'], ['a', 'c'], ['d']], 'a'], [[['a', 'b'], ['a', 'c'], ['d']], 'd'], [[['a']], 'z'], [[['a'], ['a']], 'a']], "Natural log of N over df.", approx=0.0002),
  PL("TF-IDF vector", "Write tfidf(doc, docs, vocab): for each vocab word, tf x idf where tf = count in doc / len(doc) and idf = log(N / df) (0 if df = 0); each rounded to 4 decimals.", "tfidf(doc, docs, vocab)", '''
import math
def tfidf(doc, docs, vocab):
    out = []
    for w in vocab:
        df = 0
        for d in docs:
            if w in d:
                df = df + 1
        idf = 0 if df == 0 else math.log(len(docs) / float(df))
        tf = doc.count(w) / float(len(doc))
        out.append(round(tf * idf, 4))
    return out
''', [[['a', 'b', 'a'], [['a', 'b', 'a'], ['a', 'c'], ['d']], ['a', 'b', 'c']], [['d'], [['a'], ['d']], ['a', 'd']], [['x', 'y'], [['x', 'y']], ['x']]], "Multiply the two factors.", approx=None),
  PL("Cosine similarity", "Write cosine(a, b): cosine similarity of two vectors rounded to 4 decimals (0 if either vector has zero length).", "cosine(a, b)", '''
import math
def cosine(a, b):
    dot = sum([a[i] * b[i] for i in range(len(a))])
    na = math.sqrt(sum([v * v for v in a]))
    nb = math.sqrt(sum([v * v for v in b]))
    if na == 0 or nb == 0:
        return 0
    return round(dot / (na * nb), 4)
''', [[[1, 0], [0, 1]], [[1, 2, 3], [2, 4, 6]], [[0, 0], [1, 1]], [[1, 1], [1, 0]]], "Guard against zero length.", approx=0.0002),
  PL("Rank documents", "Write rank(query_vec, doc_vecs): the document indexes sorted by cosine similarity to the query, highest first (ties by lower index).", "rank(query_vec, doc_vecs)", '''
import math
def rank(query_vec, doc_vecs):
    def cos(a, b):
        dot = sum([a[i] * b[i] for i in range(len(a))])
        na = math.sqrt(sum([v * v for v in a]))
        nb = math.sqrt(sum([v * v for v in b]))
        if na == 0 or nb == 0:
            return 0
        return dot / (na * nb)
    scores = [(-round(cos(query_vec, d), 6), i) for i, d in enumerate(doc_vecs)]
    scores.sort()
    return [i for s, i in scores]
''', [[[1, 0, 1], [[1, 1, 0], [1, 0, 1], [0, 1, 0]]], [[0, 1], [[1, 0], [0, 2]]], [[1, 1], [[1, 1], [2, 2]]]], "Sort by similarity."),
  PL("Edit distance", "Write edit_distance(a, b): the Levenshtein distance between two strings.", "edit_distance(a, b)", '''
def edit_distance(a, b):
    m = len(a)
    n = len(b)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
    return d[m][n]
''', [['kitten', 'sitting'], ['', 'abc'], ['same', 'same'], ['flaw', 'lawn']], "Fill the table row by row."),
  PL("Jaccard similarity", "Write jaccard(a, b): the size of the intersection of two token lists (as sets) divided by the size of the union, rounded to 4 decimals (1.0 if both are empty).", "jaccard(a, b)", '''
def jaccard(a, b):
    sa = set(a)
    sb = set(b)
    if len(sa | sb) == 0:
        return 1.0
    return round(len(sa & sb) / float(len(sa | sb)), 4)
''', [[['a', 'b', 'c'], ['b', 'c', 'd']], [[], []], [['x'], ['y']]], "Overlap over union.", approx=0.0002)]
))

CHS.append(CH(
 "N-gram language models",
 ("Language models", [
  "Language model | assigns | Probabilities to text",
  "N-gram | conditions on | Previous n-1 words",
  "Markov assumption | limits | History",
  "Smoothing | fixes | Zero counts",
  "Perplexity | measures | Surprise",
  "Backoff | falls to | Shorter context",
  "Generation | samples | Next words"]),
 ["A language model assigns a probability to a sequence of words, or equivalently predicts the next word. An n-gram model assumes that the next word depends only on the previous n-1 words, and estimates probabilities by counting in a corpus.",
  "Unseen word pairs would get probability zero, so we smooth: add-one (Laplace) smoothing, or back off to shorter contexts. Quality is measured by perplexity, the model's average surprise on held-out text; lower is better.",
  "Language modelling is the idea behind autocomplete, speech recognition and, at a much larger scale, today's large language models."],
 [("Language model", "A model that assigns probabilities to sequences of words or predicts the next word."),
  ("Bigram", "A pair of consecutive words; a bigram model conditions each word on the one before."),
  ("Smoothing", "Adjusting counts so unseen events get non-zero probability."),
  ("Perplexity", "The exponential of the average negative log-probability per word; roughly the effective number of choices."),
  ("Markov assumption", "The assumption that the future depends only on a limited recent past.")],
 ["P(w | prev) = count(prev w) / count(prev).",
  "Add-k: (count + k) / (total + k V).",
  "log P(sentence) = sum of log P(w | prev).",
  "Perplexity = exp(-mean log P).",
  "Larger n: more context, more sparsity."],
 [T("Your phone suggests the next word as you type. Behind it is a language model. 'I am going to' is often followed by 'be' or 'the' or 'bed', rarely by 'purple'. Language models turn that intuition into numbers."),
  T("The chain rule says the probability of a sentence is the product of each word's probability given everything before it. That is too much history to count. The bigram model keeps only the previous word: the probability of 'sat' after 'cat' is the number of times 'cat sat' appears divided by the number of times 'cat' appears. Trigram models keep two words, and so on. This is the Markov assumption."),
  T("Counting has a trap. A perfectly good sentence may contain a word pair never seen in training, giving probability zero and, because probabilities multiply, probability zero for the whole sentence. Smoothing shares out some probability to unseen events. Add-one smoothing adds one to every count. Kneser-Ney smoothing, which backs off to shorter contexts in a smarter way, was the best n-gram method for decades."),
  C("from collections import Counter, defaultdict\nimport math\n\ntokens = '<s> the cat sat on the mat </s>'.split()\nbigrams = Counter(zip(tokens, tokens[1:]))\nunigrams = Counter(tokens)\ndef p(w, prev, k=1, V=len(unigrams)):\n    return (bigrams[(prev, w)] + k) / (unigrams[prev] + k * V)\nprint(p('cat', 'the'))", "python"),
  T("To judge a language model, compute how surprised it is by text it has not seen. The perplexity is the exponential of the average negative log probability per word. A perplexity of 100 means the model is as unsure as if it had to choose among 100 equally likely words at each step. You can also run the model forwards: pick a next word from its distribution, append, repeat. N-gram generation gives locally sensible but globally rambling text, as the playground shows.")],
 [("What does a bigram model condition on?", ["The previous word", "The next word", "The sentence length", "The author"], 0, "n-1 = 1."),
  ("Why smooth counts?", ["Unseen pairs would get probability zero", "To speed up", "To remove stopwords", "To stem"], 0, "Zero kills the product."),
  ("What does lower perplexity mean?", ["A better model", "A worse model", "A longer text", "More words"], 0, "Less surprise."),
  ("What is add-one smoothing?", ["Add one to every count", "Remove one word", "Add one word", "Square the counts"], 0, "Laplace."),
  ("What is the downside of a large n?", ["Sparse counts", "Too fast", "Too little memory use", "No context"], 0, "Rare n-grams."),
  ("What is a language model used for?", ["Predicting the next word", "Resizing images", "Sorting", "Compression only"], 0, "Autocomplete.")],
 [("P(w|prev)", "bigram probability"), ("exp(-mean log p)", "perplexity"), ("(c + k)/(N + kV)", "add-k smoothing")],
 [APP("NGRAM", "N-gram text generator", "Pick a small corpus and an order (bigram or trigram), then generate text and look at the counts. Generate text with at least two different corpora or orders to complete the lab.", 800),
  MATCH("Match the term", "Pair each term with its meaning.", [("Bigram", "two consecutive words"), ("Smoothing", "give unseen events some probability"), ("Perplexity", "average surprise"), ("Markov assumption", "limited history"), ("Language model", "probabilities of text")]),
  PL("Bigram counts", "Write bigram_counts(tokens): all distinct bigrams with counts as [w1, w2, count] triples sorted by w1 then w2.", "bigram_counts(tokens)", '''
def bigram_counts(tokens):
    d = {}
    for i in range(len(tokens) - 1):
        k = (tokens[i], tokens[i + 1])
        d[k] = d.get(k, 0) + 1
    return [[k[0], k[1], d[k]] for k in sorted(d.keys())]
''', [[['a', 'b', 'a', 'b', 'c']], [['x']], [['the', 'cat', 'the', 'dog']]], "Count adjacent pairs."),
  PL("Bigram probability", "Write bigram_prob(tokens, prev, w, k): the add-k smoothed probability (count(prev w) + k) / (count(prev as first of a pair) + k V) where V is the number of distinct tokens; rounded to 4 decimals.", "bigram_prob(tokens, prev, w, k)", '''
def bigram_prob(tokens, prev, w, k):
    V = len(set(tokens))
    c = 0
    cp = 0
    for i in range(len(tokens) - 1):
        if tokens[i] == prev:
            cp = cp + 1
            if tokens[i + 1] == w:
                c = c + 1
    return round((c + k) / float(cp + k * V), 4)
''', [[['the', 'cat', 'sat', 'the', 'cat', 'ran'], 'the', 'cat', 0], [['the', 'cat', 'sat', 'the', 'cat', 'ran'], 'the', 'dog', 1], [['a', 'b'], 'a', 'b', 1]], "Smoothed relative frequency.", approx=0.0002),
  PL("Sentence log-probability", "Write sent_logprob(sentence, tokens, k): the log of the product of add-k bigram probabilities for consecutive words of sentence, using counts from tokens (V = distinct tokens in tokens), rounded to 3 decimals.", "sent_logprob(sentence, tokens, k)", '''
import math
def sent_logprob(sentence, tokens, k):
    V = len(set(tokens))
    total = 0.0
    for j in range(len(sentence) - 1):
        prev = sentence[j]
        w = sentence[j + 1]
        c = 0
        cp = 0
        for i in range(len(tokens) - 1):
            if tokens[i] == prev:
                cp = cp + 1
                if tokens[i + 1] == w:
                    c = c + 1
        total = total + math.log((c + k) / float(cp + k * V))
    return round(total, 3)
''', [[['the', 'cat', 'sat'], ['the', 'cat', 'sat', 'the', 'cat', 'ran'], 1], [['the', 'cat'], ['the', 'cat', 'the', 'cat'], 1], [['cat', 'the'], ['the', 'cat', 'the', 'cat'], 0.5]], "Sum logs instead of multiplying.", approx=0.003),
  PL("Perplexity", "Write perplexity(probs): given the list of probabilities the model gave to each word, exp(-mean(log p)) rounded to 3 decimals.", "perplexity(probs)", '''
import math
def perplexity(probs):
    s = 0.0
    for p in probs:
        s = s + math.log(p)
    return round(math.exp(-s / len(probs)), 3)
''', [[[0.5, 0.5, 0.5]], [[1.0, 1.0]], [[0.1, 0.2, 0.4]], [[0.25]]], "Inverse geometric mean.", approx=0.003),
  PL("Most likely next word", "Write next_word(tokens, prev): the word that most often follows prev in tokens (ties: alphabetically first); return None if prev never appears as a non-final token.", "next_word(tokens, prev)", '''
def next_word(tokens, prev):
    d = {}
    for i in range(len(tokens) - 1):
        if tokens[i] == prev:
            d[tokens[i + 1]] = d.get(tokens[i + 1], 0) + 1
    if not d:
        return None
    best = None
    for w in sorted(d.keys()):
        if best is None or d[w] > d[best]:
            best = w
    return best
''', [[['a', 'b', 'a', 'c', 'a', 'b'], 'a'], [['x', 'y'], 'y'], [['p', 'q', 'p', 'r'], 'p']], "Count followers."),
  PL("Greedy generation", "Write generate(tokens, start, n): starting from the word start, repeatedly append the most frequent following word (ties alphabetical) up to n extra words; stop early if no follower exists. Return the list of words including start.", "generate(tokens, start, n)", '''
def generate(tokens, start, n):
    out = [start]
    for step in range(n):
        d = {}
        for i in range(len(tokens) - 1):
            if tokens[i] == out[-1]:
                d[tokens[i + 1]] = d.get(tokens[i + 1], 0) + 1
        if not d:
            break
        best = None
        for w in sorted(d.keys()):
            if best is None or d[w] > d[best]:
                best = w
        out.append(best)
    return out
''', [[['the', 'cat', 'sat', 'on', 'the', 'mat', 'the', 'cat', 'ran'], 'the', 4], [['a', 'b'], 'b', 3], [['x', 'y', 'x', 'y'], 'x', 5]], "Follow the most common next word.")]
))

CHS.append(CH(
 "Text classification: Naive Bayes and sentiment",
 ("Classification", [
  "Classification | assigns | A label",
  "Naive Bayes | multiplies | Word likelihoods",
  "Prior | is | Class frequency",
  "Likelihood | is | P(word | class)",
  "Sentiment | is | Opinion polarity",
  "Lexicon | scores | Words",
  "F1 | balances | Precision and recall"]),
 ["Text classification assigns a label to a document: spam or not, topic, sentiment, language. A strong classical baseline is Naive Bayes, which combines the class prior with the likelihood of each word given the class, assuming words are independent.",
  "Logistic regression or linear SVMs on TF-IDF features are usually stronger. Sentiment analysis can also use lexicons of positive and negative words, with care over negation.",
  "Evaluate with held-out data and per-class precision, recall and F1, especially when classes are imbalanced."],
 [("Naive Bayes", "A classifier that picks the class maximising prior times the product of word likelihoods, assuming conditional independence."),
  ("Prior", "The probability of a class before seeing the document."),
  ("Likelihood", "The probability of the words given a class."),
  ("Sentiment analysis", "Determining whether text expresses a positive, negative or neutral opinion."),
  ("Macro F1", "The average of the F1 scores of each class.")],
 ["class = argmax log P(c) + sum log P(w | c).",
  "P(w | c) = (count + 1) / (total + V).",
  "Work in logs to avoid underflow.",
  "Negation flips polarity: 'not good'.",
  "Macro F1 treats classes equally."],
 [T("Is this review positive or negative? Is this email spam? Which topic does this article belong to? Each is classification of text, and a simple method works surprisingly well. Naive Bayes asks: given the label, how likely would the words be? Spam emails use 'free' and 'winner' more; ham emails use 'meeting' and 'attached'."),
  T("Bayes' rule turns this around. The probability of a class given the words is proportional to the prior probability of the class times the probability of the words given the class. The naive assumption treats words as independent given the class, so the likelihood is a product of per-word probabilities. They are not independent, but the result ranks classes well. Counting gives the probabilities; adding one to every count, Laplace smoothing, handles unseen words; working with logarithms avoids multiplying many tiny numbers."),
  C("from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\nfrom sklearn.naive_bayes import MultinomialNB\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.metrics import classification_report\n\nclf = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000))\nclf.fit(train_texts, train_labels)\nprint(classification_report(test_labels, clf.predict(test_texts)))", "python"),
  T("Sentiment analysis is a favourite task. A lexicon method adds up scores of words from a list: 'wonderful' plus two, 'dull' minus one. It is transparent but trips on negation, 'not good', sarcasm and domain: 'unpredictable' praises a thriller and damns a car. Handling negation, for instance by flipping the score of words after 'not' until punctuation, fixes some mistakes."),
  T("Measure on data the model has not seen. Accuracy can mislead with imbalanced classes. Precision, recall and their balance, F1, per class, and the macro average of them show where the model fails. Pre-trained transformers, which you meet in later chapters, now beat these classical models on most benchmarks, but Naive Bayes and logistic regression remain fast, cheap, explainable baselines.")],
 [("What does Naive Bayes assume?", ["Words are independent given the class", "Words are in order", "Classes are equal", "Documents are short"], 0, "Naive."),
  ("Why use logs?", ["Avoid underflow from tiny products", "Make it slower", "Remove words", "Add features"], 0, "Sums of logs."),
  ("What does Laplace smoothing do?", ["Adds one to counts", "Removes rare words", "Squares counts", "Sorts words"], 0, "Unseen words."),
  ("What breaks a simple lexicon method?", ["Negation and sarcasm", "Long words", "Spaces", "Numbers"], 0, "Not good."),
  ("What is a prior?", ["Class probability before seeing the text", "A word list", "A filter", "A token"], 0, "Class frequency."),
  ("Why macro F1?", ["It weighs classes equally", "It is faster", "It ignores errors", "It uses accuracy"], 0, "Imbalanced classes.")],
 [("argmax_c log P(c) + sum log P(w|c)", "Naive Bayes rule"), ("MultinomialNB()", "scikit-learn Naive Bayes"), ("classification_report", "per-class metrics")],
 [MATCH("Match the term", "Pair each classification idea with its meaning.", [("Prior", "class probability alone"), ("Likelihood", "words given class"), ("Laplace smoothing", "add one"), ("Lexicon", "list of scored words"), ("Macro F1", "average over classes")]),
  PL("Train Naive Bayes", "Write train_nb(docs, labels): docs are lists of tokens. Return [priors, counts] where priors is a list of [label, count of docs] sorted by label and counts is a list of [label, word, count] sorted by label then word.", "train_nb(docs, labels)", '''
def train_nb(docs, labels):
    pri = {}
    cnt = {}
    for d, l in zip(docs, labels):
        pri[l] = pri.get(l, 0) + 1
        for w in d:
            k = (l, w)
            cnt[k] = cnt.get(k, 0) + 1
    return [[[l, pri[l]] for l in sorted(pri.keys())], [[k[0], k[1], cnt[k]] for k in sorted(cnt.keys())]]
''', [[[['good', 'film'], ['bad', 'film']], ['pos', 'neg']], [[['a', 'a']], ['x']]], "Count documents per label and words per label."),
  PL("Predict with Naive Bayes", "Write predict_nb(doc, docs, labels): train add-one-smoothed Naive Bayes on docs and labels and return the label with the highest log P(c) + sum over the doc's words of log((count(c, w) + 1) / (total words in c + V)), where V is the number of distinct words in docs. Ties go to the alphabetically first label.", "predict_nb(doc, docs, labels)", '''
import math
def predict_nb(doc, docs, labels):
    vocab = set()
    for d in docs:
        for w in d:
            vocab.add(w)
    V = len(vocab)
    best = None
    bs = None
    for c in sorted(set(labels)):
        n = len([l for l in labels if l == c])
        s = math.log(n / float(len(labels)))
        words = []
        for d, l in zip(docs, labels):
            if l == c:
                words = words + d
        tot = len(words)
        for w in doc:
            s = s + math.log((words.count(w) + 1) / float(tot + V))
        if bs is None or s > bs + 1e-12:
            bs = s
            best = c
    return best
''', [[['good', 'fun'], [['good', 'film'], ['fun', 'good'], ['bad', 'film'], ['dull', 'bad']], ['pos', 'pos', 'neg', 'neg']], [['bad'], [['good', 'film'], ['fun', 'good'], ['bad', 'film'], ['dull', 'bad']], ['pos', 'pos', 'neg', 'neg']], [['film'], [['good', 'film'], ['bad', 'film']], ['pos', 'neg']]], "Compare the log scores of each class."),
  PL("Lexicon sentiment", "Write sentiment(tokens, lexicon): lexicon is a list of [word, score]. Sum the scores of tokens found in it; a token's score is multiplied by -1 if the previous token is 'not'. Return the label 'positive' if the total is above 0, 'negative' if below 0, else 'neutral'.", "sentiment(tokens, lexicon)", '''
def sentiment(tokens, lexicon):
    d = {}
    for w, s in lexicon:
        d[w] = s
    total = 0
    for i in range(len(tokens)):
        if tokens[i] in d:
            s = d[tokens[i]]
            if i > 0 and tokens[i - 1] == 'not':
                s = -s
            total = total + s
    if total > 0:
        return 'positive'
    if total < 0:
        return 'negative'
    return 'neutral'
''', [[['a', 'great', 'film'], [['great', 2], ['dull', -1]]], [['not', 'great'], [['great', 2], ['dull', -1]]], [['fine'], [['great', 2]]], [['dull', 'but', 'great'], [['great', 2], ['dull', -1]]]], "Flip after a negation."),
  PL("Per-class F1", "Write f1_for(y_true, y_pred, label): the F1 score for one label, rounded to 3 decimals (0 if undefined).", "f1_for(y_true, y_pred, label)", '''
def f1_for(y_true, y_pred, label):
    tp = 0
    fp = 0
    fn = 0
    for i in range(len(y_true)):
        if y_pred[i] == label and y_true[i] == label:
            tp = tp + 1
        elif y_pred[i] == label:
            fp = fp + 1
        elif y_true[i] == label:
            fn = fn + 1
    p = tp / float(tp + fp) if tp + fp else 0
    r = tp / float(tp + fn) if tp + fn else 0
    if p + r == 0:
        return 0
    return round(2 * p * r / (p + r), 3)
''', [[['a', 'a', 'b', 'b'], ['a', 'b', 'b', 'b'], 'a'], [['a', 'b'], ['b', 'a'], 'a'], [['a', 'a'], ['a', 'a'], 'a']], "Count the three cases.", approx=0.002),
  PL("Macro F1", "Write macro_f1(y_true, y_pred): the average over all labels (sorted) of the per-class F1, rounded to 3 decimals.", "macro_f1(y_true, y_pred)", '''
def macro_f1(y_true, y_pred):
    labels = sorted(set(y_true) | set(y_pred))
    total = 0.0
    for label in labels:
        tp = 0
        fp = 0
        fn = 0
        for i in range(len(y_true)):
            if y_pred[i] == label and y_true[i] == label:
                tp = tp + 1
            elif y_pred[i] == label:
                fp = fp + 1
            elif y_true[i] == label:
                fn = fn + 1
        p = tp / float(tp + fp) if tp + fp else 0
        r = tp / float(tp + fn) if tp + fn else 0
        f = 0 if p + r == 0 else 2 * p * r / (p + r)
        total = total + f
    return round(total / len(labels), 3)
''', [[['a', 'a', 'b', 'b'], ['a', 'b', 'b', 'b']], [['x', 'y', 'z'], ['x', 'y', 'z']], [['a', 'a', 'a', 'b'], ['a', 'a', 'a', 'a']]], "Average the class scores.", approx=0.003),
  PL("Language detection", "Write detect(text, profiles): profiles is a list of [language, characters] where characters is a string of that language's typical letters. Return the language whose profile contains the most of the text's letters (count letters of the text that appear in the profile string; ties go to the first language).", "detect(text, profiles)", '''
def detect(text, profiles):
    best = None
    bs = -1
    for lang, chars in profiles:
        s = 0
        for ch in text.lower():
            if ch != " " and ch in chars:
                s = s + 1
        if s > bs:
            bs = s
            best = lang
    return best
''', [['hello world', [['en', 'abcdefghijklmnopqrstuvwxyz'], ['de', 'abcdefghijklmnopqrstuvwxyzäöüß']]], ['grüße', [['en', 'abcdefghijklmnopqrstuvwxyz'], ['de', 'abcdefghijklmnopqrstuvwxyzäöüß']]], ['', [['a', 'x'], ['b', 'y']]]], "Count matching letters.")]
))

CHS.append(CH(
 "Linguistic structure: tagging, parsing and entities",
 ("Structure", [
  "POS tag | labels | Word class",
  "HMM | models | Tag sequences",
  "Viterbi | finds | Best tag path",
  "Grammar | generates | Sentences",
  "Parse tree | shows | Structure",
  "NER | finds | Names",
  "Dependency | links | Heads and dependents"]),
 ["Language has structure. Part-of-speech tagging labels each word as noun, verb and so on; context matters, since 'duck' can be either. A hidden Markov model with the Viterbi algorithm finds the most probable tag sequence.",
  "A context-free grammar describes how phrases build sentences, and a parser recovers the tree, for example with the CKY algorithm. Dependency parsing links each word to its head.",
  "Named entity recognition finds names of people, places and organisations, usually by tagging tokens with B-I-O labels."],
 [("Part of speech (POS)", "The grammatical category of a word, such as noun, verb or adjective."),
  ("Hidden Markov model", "A model with hidden states (tags) that emit observed words and move by transition probabilities."),
  ("Viterbi algorithm", "A dynamic programming method that finds the most probable hidden state sequence."),
  ("Context-free grammar", "A set of rewrite rules such as S -> NP VP that generate sentences."),
  ("Named entity recognition", "Finding and classifying names of people, organisations, locations and so on in text.")],
 ["Viterbi: best[t][s] = max over p of best[t-1][p] T[p][s] E[s][w].",
  "CKY fills a chart for spans.",
  "BIO tags: B-PER begins, I-PER continues, O outside.",
  "Dependency: each word has one head.",
  "Neural taggers now give the best accuracy."],
 [T("Read 'Time flies like an arrow' and 'Fruit flies like a banana'. The same words get different structures. Understanding language requires more than a bag of words. The first layer of structure is the part of speech. 'Flies' might be a verb or a noun, and neighbours decide. A tagger assigns each word a tag using the surrounding words."),
  T("The classic model is the hidden Markov model. Tags are hidden states. Each tag tends to follow certain tags, determiner then noun, which gives transition probabilities, and each tag emits certain words, which gives emission probabilities. Given a sentence, the number of possible tag sequences is huge, but the Viterbi algorithm finds the best one in time proportional to the length times the square of the number of tags, by keeping, for each position and tag, only the best path ending there."),
  T("Above tags sit phrases. A context-free grammar has rules such as a sentence is a noun phrase followed by a verb phrase, and a noun phrase is a determiner followed by a noun. A parser finds the tree that the grammar assigns to a sentence. The CKY algorithm fills a triangular chart with every constituent for every span of words, working from short spans to long. Ambiguity, as in 'I saw the man with the telescope', produces several trees, and probabilistic grammars choose the likeliest."),
  C("import spacy\nnlp = spacy.load('en_core_web_sm')\ndoc = nlp('Apple is looking at buying a U.K. startup for $1 billion.')\nfor t in doc:\n    print(t.text, t.pos_, t.dep_, t.head.text)\nfor ent in doc.ents:\n    print(ent.text, ent.label_)   # Apple ORG, U.K. GPE, $1 billion MONEY", "python"),
  T("Dependency grammars take another view. Instead of nested phrases, each word depends on exactly one head word, with a labelled link such as subject or object, giving a tree of word-to-word arrows. Named entity recognition finds mentions of people, organisations, places and dates. It is usually treated as tagging with BIO labels: B marks the beginning of an entity, I its continuation, O everything outside. Today these tasks are done by neural networks trained on annotated treebanks, and later chapters show how pre-trained transformers made them much more accurate.")],
 [("What does POS tagging assign?", ["A grammatical category to each word", "A sentiment", "A translation", "A frequency"], 0, "Noun, verb."),
  ("What does the Viterbi algorithm find?", ["The most probable tag sequence", "The shortest word", "The most common word", "A grammar"], 0, "Dynamic programming."),
  ("What does a context-free grammar contain?", ["Rewrite rules", "Word vectors", "Images", "Counts"], 0, "S -> NP VP."),
  ("What does BIO tagging mark?", ["Entity boundaries", "Sentiment", "Stopwords", "Verbs"], 0, "Begin, inside, outside."),
  ("What is a dependency link?", ["From a word to its head", "Between letters", "A synonym", "A suffix"], 0, "Head and dependent."),
  ("Why is parsing hard?", ["Ambiguity", "Short sentences", "Too few words", "Spelling only"], 0, "Many trees.")],
 [("S -> NP VP", "grammar rule"), ("B-PER, I-PER, O", "BIO tags"), ("nlp(text).ents", "spaCy entities")],
 [MATCH("Match the term", "Pair each structure idea with its meaning.", [("POS tag", "word class"), ("Viterbi", "best hidden path"), ("CKY", "chart parsing"), ("NER", "find names"), ("Dependency", "word to head link")]),
  PL("Most frequent tag baseline", "Write tag_baseline(words, lexicon, default): lexicon is a list of [word, tag]; return the list of tags for the words (the lexicon tag if known, else default).", "tag_baseline(words, lexicon, default)", '''
def tag_baseline(words, lexicon, default):
    d = {}
    for w, t in lexicon:
        d[w] = t
    return [d.get(w, default) for w in words]
''', [[['the', 'dog', 'barks'], [['the', 'DET'], ['dog', 'NOUN']], 'VERB'], [[], [], 'X'], [['a'], [['a', 'DET']], 'N']], "Look each word up."),
  PL("Viterbi", "Write viterbi(obs, states, start_p, trans_p, emit_p): the most probable state path for the observation list. start_p is a list aligned with states, trans_p a matrix [from][to], emit_p a list (per state) of dictionaries given as lists of [observation, probability] pairs (missing observation = probability 0). On ties choose the lower state index. Return the list of state names.", "viterbi(obs, states, start_p, trans_p, emit_p)", '''
def viterbi(obs, states, start_p, trans_p, emit_p):
    n = len(states)
    E = []
    for lst in emit_p:
        d = {}
        for o, p in lst:
            d[o] = p
        E.append(d)
    V = [[0.0] * n for _ in obs]
    B = [[0] * n for _ in obs]
    for s in range(n):
        V[0][s] = start_p[s] * E[s].get(obs[0], 0.0)
    for t in range(1, len(obs)):
        for s in range(n):
            best = -1.0
            arg = 0
            for p in range(n):
                v = V[t - 1][p] * trans_p[p][s]
                if v > best + 1e-15:
                    best = v
                    arg = p
            V[t][s] = best * E[s].get(obs[t], 0.0)
            B[t][s] = arg
    last = 0
    bv = -1.0
    for s in range(n):
        if V[-1][s] > bv + 1e-15:
            bv = V[-1][s]
            last = s
    path = [last]
    for t in range(len(obs) - 1, 0, -1):
        last = B[t][last]
        path.append(last)
    path.reverse()
    return [states[i] for i in path]
''', [[['dogs', 'bark'], ['N', 'V'], [0.7, 0.3], [[0.3, 0.7], [0.6, 0.4]], [[['dogs', 0.6], ['bark', 0.1]], [['dogs', 0.05], ['bark', 0.7]]]], [['bark', 'dogs'], ['N', 'V'], [0.5, 0.5], [[0.3, 0.7], [0.8, 0.2]], [[['dogs', 0.6], ['bark', 0.3]], [['dogs', 0.05], ['bark', 0.6]]]], [['dogs'], ['N', 'V'], [0.5, 0.5], [[0.5, 0.5], [0.5, 0.5]], [[['dogs', 0.4]], [['dogs', 0.1]]]]], "Keep the best predecessor for each state."),
  PL("CKY recognition", "Write cky(words, lexicon, rules): lexicon is a list of [word, category]; rules is a list of [parent, left, right] binary rules (Chomsky normal form). Return True if the start symbol 'S' can be derived over the whole sentence.", "cky(words, lexicon, rules)", '''
def cky(words, lexicon, rules):
    n = len(words)
    chart = [[set() for _ in range(n + 1)] for _ in range(n + 1)]
    for i in range(n):
        for w, c in lexicon:
            if w == words[i]:
                chart[i][i + 1].add(c)
    for span in range(2, n + 1):
        for i in range(0, n - span + 1):
            j = i + span
            for k in range(i + 1, j):
                for p, l, r in rules:
                    if l in chart[i][k] and r in chart[k][j]:
                        chart[i][j].add(p)
    return 'S' in chart[0][n]
''', [[['the', 'dog', 'barks'], [['the', 'Det'], ['dog', 'N'], ['barks', 'V']], [['S', 'NP', 'V'], ['NP', 'Det', 'N']]], [['dog', 'the', 'barks'], [['the', 'Det'], ['dog', 'N'], ['barks', 'V']], [['S', 'NP', 'V'], ['NP', 'Det', 'N']]], [['dogs', 'bark'], [['dogs', 'NP'], ['bark', 'V']], [['S', 'NP', 'V']]]], "Fill the chart by span length."),
  PL("Decode BIO entities", "Write entities(tokens, tags): tags use B-X, I-X and O. Return the list of [text, type] where text joins the tokens of an entity with spaces.", "entities(tokens, tags)", '''
def entities(tokens, tags):
    out = []
    cur = None
    typ = None
    for t, g in zip(tokens, tags):
        if g.startswith('B-'):
            if cur is not None:
                out.append([cur, typ])
            cur = t
            typ = g[2:]
        elif g.startswith('I-') and cur is not None and g[2:] == typ:
            cur = cur + ' ' + t
        else:
            if cur is not None:
                out.append([cur, typ])
            cur = None
            typ = None
    if cur is not None:
        out.append([cur, typ])
    return out
''', [[['Ada', 'Lovelace', 'visited', 'London'], ['B-PER', 'I-PER', 'O', 'B-LOC']], [['a', 'b'], ['O', 'O']], [['New', 'York', 'City'], ['B-LOC', 'I-LOC', 'I-LOC']]], "Open an entity on B, extend on I."),
  PL("Regex-like entity finder", "Write find_money(tokens): the indexes of tokens that start with '$' followed by digits (digits may include commas or a decimal point).", "find_money(tokens)", '''
def find_money(tokens):
    out = []
    for i, t in enumerate(tokens):
        if len(t) > 1 and t[0] == '$':
            body = t[1:]
            ok = True
            has_digit = False
            for ch in body:
                if ch.isdigit():
                    has_digit = True
                elif ch not in ',.':
                    ok = False
            if ok and has_digit:
                out.append(i)
    return out
''', [[['pay', '$5', 'or', '$1,200.50', 'or', '$abc']], [['no', 'money']], [['$', '$9']]], "Check the body characters."),
  PL("Dependency heads", "Write root_and_children(heads): heads[i] is the index of word i's head, with -1 for the root. Return [root index, list of the children counts per word].", "root_and_children(heads)", '''
def root_and_children(heads):
    root = heads.index(-1)
    counts = [0] * len(heads)
    for h in heads:
        if h >= 0:
            counts[h] = counts[h] + 1
    return [root, counts]
''', [[[1, -1, 1]], [[-1]], [[2, 2, -1, 2]]], "Count how often each index is a head."),
  PL("Tagging accuracy", "Write tag_accuracy(gold, pred): the fraction of positions where the tags agree, rounded to 3 decimals.", "tag_accuracy(gold, pred)", '''
def tag_accuracy(gold, pred):
    ok = 0
    for i in range(len(gold)):
        if gold[i] == pred[i]:
            ok = ok + 1
    return round(ok / float(len(gold)), 3)
''', [[['N', 'V', 'N'], ['N', 'N', 'N']], [['A'], ['A']], [['x', 'y'], ['y', 'x']]], "Count agreements.", approx=0.002)]
))
