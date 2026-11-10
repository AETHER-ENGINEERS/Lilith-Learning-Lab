# -*- coding: utf-8 -*-
"""NLP course, part 2: embeddings, neural sequences, transformers, pretrained models, applications."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Word embeddings: meaning as geometry",
 ("Embeddings", [
  "Distributional hypothesis | links | Context to meaning",
  "Co-occurrence | counts | Neighbours",
  "PMI | measures | Association",
  "Word2vec | predicts | Context words",
  "Embedding | is | A dense vector",
  "Analogy | uses | Vector arithmetic",
  "Bias | is learned | From text"]),
 ["You shall know a word by the company it keeps. Words that appear in similar contexts have similar meanings. Counting co-occurrences and reducing the table to dense vectors gives word embeddings, in which similar words are close together.",
  "Word2vec and GloVe learn vectors of a few hundred numbers. Cosine similarity finds neighbours, and directions encode relations: king minus man plus woman lands near queen.",
  "Embeddings reflect the text they were trained on, including its social biases, which must be audited."],
 [("Distributional hypothesis", "The idea that words used in similar contexts have similar meanings."),
  ("Word embedding", "A dense vector of real numbers representing a word, learned from text."),
  ("PPMI", "Positive pointwise mutual information: how much more often two words co-occur than chance, floored at zero."),
  ("Skip-gram", "A word2vec training task: predict the context words around a given word."),
  ("Out-of-vocabulary", "A word not seen in training and so lacking a vector.")],
 ["PMI = log P(w, c) / (P(w) P(c)).",
  "Similar words, similar contexts.",
  "Skip-gram pairs (centre, context) in a window.",
  "king - man + woman is about queen.",
  "Contextual embeddings replaced static ones."],
 [T("The bag-of-words view treats 'car' and 'automobile' as strangers. But they appear among the same neighbours: drive, road, engine, parked. The linguist J. R. Firth put it as a slogan: you shall know a word by the company it keeps. If we describe each word by the words around it, similar words get similar descriptions."),
  T("Build a table with a row per word and a column per context word, counting how often they appear within a few words of each other. Raw counts are dominated by common words, so replace them by pointwise mutual information, which asks how much more often the pair occurs than if the words were independent. Table rows are long sparse vectors. Reduce them, for instance with singular value decomposition, to 100 or 300 dense dimensions, and you have embeddings."),
  T("Word2vec, from Tomas Mikolov and colleagues at Google in 2013, learns the vectors directly with a tiny neural network. In the skip-gram variant, the network reads a word and tries to predict the words in a window around it. Training pushes words that share contexts toward similar vectors. With negative sampling, random wrong words serve as the contrast. GloVe fits vectors to the log co-occurrence counts. Both train in minutes on a laptop."),
  C("from gensim.models import Word2Vec\nsentences = [['the', 'king', 'rules'], ['the', 'queen', 'rules'], ['a', 'dog', 'barks']]\nmodel = Word2Vec(sentences, vector_size=50, window=2, min_count=1, sg=1, epochs=50)\nprint(model.wv.most_similar('king'))\n# with pretrained vectors:\n# print(wv.most_similar(positive=['king', 'woman'], negative=['man']))", "python"),
  T("The resulting space has remarkable regularities. Differences between vectors capture relations, so the vector for king minus man plus woman lies near queen, and Paris minus France plus Italy lies near Rome. But the space also absorbs the prejudice of its training text: 'doctor' sits closer to 'he' and 'nurse' closer to 'she'. Static embeddings give one vector per word, even for 'bank' of a river and 'bank' of money. Chapters ahead replace them with contextual embeddings from transformers, which give each occurrence its own vector.")],
 [("What is the distributional hypothesis?", ["Similar contexts imply similar meanings", "Words are random", "Meaning is fixed", "Only nouns matter"], 0, "Company it keeps."),
  ("What does PMI measure?", ["Association beyond chance", "Word length", "Frequency only", "Spelling"], 0, "Pointwise mutual information."),
  ("What does skip-gram predict?", ["Context words from a centre word", "The next sentence", "A label", "Spelling"], 0, "Word2vec."),
  ("What does king - man + woman approximate?", ["queen", "kings", "men", "crown"], 0, "Analogy."),
  ("What problem do static embeddings have?", ["One vector per word, ignoring sense", "Too long", "Too sparse", "Not numeric"], 0, "Bank."),
  ("Why audit embeddings?", ["They absorb biases of the text", "They are slow", "They are sparse", "They need labels"], 0, "Social bias.")],
 [("cos(a, b)", "vector similarity"), ("log P(w,c)/(P(w)P(c))", "PMI"), ("Word2Vec(sentences)", "train embeddings")],
 [MATCH("Match the term", "Pair each embedding idea with its meaning.", [("Co-occurrence", "words near each other"), ("PMI", "association beyond chance"), ("Skip-gram", "predict context words"), ("Analogy", "vector arithmetic"), ("OOV", "unseen word")]),
  PL("Co-occurrence counts", "Write cooc(tokens, window): for each unordered pair of distinct words appearing within window positions of each other, count the co-occurrences; return [w1, w2, count] triples with w1 < w2, sorted.", "cooc(tokens, window)", '''
def cooc(tokens, window):
    d = {}
    for i in range(len(tokens)):
        for j in range(i + 1, min(len(tokens), i + window + 1)):
            a = tokens[i]
            b = tokens[j]
            if a == b:
                continue
            k = (a, b) if a < b else (b, a)
            d[k] = d.get(k, 0) + 1
    return [[k[0], k[1], d[k]] for k in sorted(d.keys())]
''', [[['a', 'b', 'c', 'a'], 1], [['x', 'y', 'x', 'y'], 2], [['p'], 3]], "Look ahead at most window positions."),
  PL("PMI", "Write pmi(count_xy, count_x, count_y, total): log2((count_xy / total) / ((count_x / total) x (count_y / total))), rounded to 3 decimals; return 0 if count_xy is 0.", "pmi(count_xy, count_x, count_y, total)", '''
import math
def pmi(count_xy, count_x, count_y, total):
    if count_xy == 0:
        return 0
    p = count_xy / float(total)
    return round(math.log(p / ((count_x / float(total)) * (count_y / float(total))), 2), 3)
''', [[10, 20, 25, 100], [1, 50, 50, 100], [0, 5, 5, 10], [5, 10, 10, 100]], "Compare joint with product of marginals.", approx=0.003),
  PL("Nearest neighbours", "Write nearest(word, vocab, vectors, k): the k words (excluding word itself) with the highest cosine similarity to the vector of word; vocab and vectors are parallel lists. Ties by vocab order. Return the list of words.", "nearest(word, vocab, vectors, k)", '''
import math
def nearest(word, vocab, vectors, k):
    def cos(a, b):
        dot = sum([a[i] * b[i] for i in range(len(a))])
        return dot / (math.sqrt(sum([v * v for v in a])) * math.sqrt(sum([v * v for v in b])))
    q = vectors[vocab.index(word)]
    scored = []
    for i in range(len(vocab)):
        if vocab[i] != word:
            scored.append((-round(cos(q, vectors[i]), 6), i))
    scored.sort()
    return [vocab[i] for s, i in scored[:k]]
''', [['cat', ['cat', 'dog', 'car', 'truck'], [[1, 0.1], [0.9, 0.2], [0.1, 1], [0.2, 0.9]], 1], ['car', ['cat', 'dog', 'car', 'truck'], [[1, 0.1], [0.9, 0.2], [0.1, 1], [0.2, 0.9]], 2], ['a', ['a', 'b'], [[1, 1], [2, 2]], 1]], "Rank by cosine."),
  PL("Analogy", "Write analogy(a, b, c, vocab, vectors): find the word (excluding a, b, c) whose vector is nearest by cosine similarity to vec(b) - vec(a) + vec(c). Return the word (first on ties).", "analogy(a, b, c, vocab, vectors)", '''
import math
def analogy(a, b, c, vocab, vectors):
    va = vectors[vocab.index(a)]
    vb = vectors[vocab.index(b)]
    vc = vectors[vocab.index(c)]
    t = [vb[i] - va[i] + vc[i] for i in range(len(va))]
    best = None
    bs = None
    for i in range(len(vocab)):
        if vocab[i] in (a, b, c):
            continue
        v = vectors[i]
        dot = sum([t[j] * v[j] for j in range(len(t))])
        s = dot / (math.sqrt(sum([x * x for x in t])) * math.sqrt(sum([x * x for x in v])))
        if bs is None or s > bs + 1e-12:
            bs = s
            best = vocab[i]
    return best
''', [['man', 'king', 'woman', ['man', 'woman', 'king', 'queen', 'apple'], [[1, 0], [1, 1], [0, 0.5], [0.1, 1.4], [3, 3]]], ['a', 'b', 'c', ['a', 'b', 'c', 'd'], [[0, 0], [1, 0], [0, 1], [1, 1]]]], "Do the vector arithmetic first."),
  PL("Skip-gram pairs", "Write skipgram_pairs(tokens, window): all [centre, context] pairs where the context is within window positions on either side, ordered by centre position then context position.", "skipgram_pairs(tokens, window)", '''
def skipgram_pairs(tokens, window):
    out = []
    for i in range(len(tokens)):
        for j in range(max(0, i - window), min(len(tokens), i + window + 1)):
            if j != i:
                out.append([tokens[i], tokens[j]])
    return out
''', [[['a', 'b', 'c'], 1], [['x', 'y'], 2], [['p'], 2]], "Training data for word2vec."),
  PL("Sentence vector", "Write sentence_vec(tokens, vocab, vectors): the average of the vectors of the tokens found in vocab (skip unknown tokens); rounded to 3 decimals. Return a list of zeros if none are known.", "sentence_vec(tokens, vocab, vectors)", '''
def sentence_vec(tokens, vocab, vectors):
    dim = len(vectors[0])
    acc = [0.0] * dim
    n = 0
    for t in tokens:
        if t in vocab:
            v = vectors[vocab.index(t)]
            for j in range(dim):
                acc[j] = acc[j] + v[j]
            n = n + 1
    if n == 0:
        return [0.0] * dim
    return [round(a / n, 3) for a in acc]
''', [[['a', 'b', 'zzz'], ['a', 'b'], [[1, 2], [3, 4]]], [['q'], ['a'], [[1, 1]]], [['a', 'a'], ['a'], [[0.5, 2]]]], "Average over known tokens.", approx=None),
  PL("Bias score", "Write bias_score(word, a, b, vocab, vectors): cosine(word, a) minus cosine(word, b), rounded to 3 decimals, a simple measure of whether word sits closer to a than to b.", "bias_score(word, a, b, vocab, vectors)", '''
import math
def bias_score(word, a, b, vocab, vectors):
    def cos(u, v):
        dot = sum([u[i] * v[i] for i in range(len(u))])
        return dot / (math.sqrt(sum([x * x for x in u])) * math.sqrt(sum([x * x for x in v])))
    w = vectors[vocab.index(word)]
    return round(cos(w, vectors[vocab.index(a)]) - cos(w, vectors[vocab.index(b)]), 3)
''', [['nurse', 'she', 'he', ['nurse', 'she', 'he'], [[0.9, 0.2], [1, 0], [0, 1]]], ['doctor', 'she', 'he', ['doctor', 'she', 'he'], [[0.5, 0.5], [1, 0], [0, 1]]]], "Difference of two cosines.", approx=0.003)]
))

CHS.append(CH(
 "Neural sequence models: RNNs, LSTMs and attention",
 ("Sequences", [
  "RNN | carries | A hidden state",
  "Hidden state | remembers | The past",
  "Vanishing gradient | forgets | Long range",
  "LSTM | gates | Memory",
  "Seq2seq | maps | Sequence to sequence",
  "Beam search | keeps | Several hypotheses",
  "Attention | looks back | At inputs"]),
 ["A recurrent neural network reads text one token at a time, updating a hidden state that summarises everything so far. It can predict the next word, tag every word or encode a whole sentence.",
  "Plain RNNs forget over long distances because gradients shrink; LSTMs and GRUs add gates that control what to keep. Sequence-to-sequence models use an encoder RNN and a decoder RNN for translation and summarisation.",
  "Attention lets the decoder look back at every encoder state and focus on the relevant ones. It removed the bottleneck of squeezing a sentence into one vector and led directly to the transformer."],
 [("Recurrent neural network", "A network that processes a sequence step by step, passing a hidden state from one step to the next."),
  ("LSTM", "Long short-term memory: an RNN with gates that decide what to forget, write and output."),
  ("Seq2seq", "An encoder-decoder model that maps an input sequence to an output sequence."),
  ("Beam search", "A decoding method keeping the k best partial outputs at each step."),
  ("Attention", "A mechanism that computes a weighted average of states, with weights depending on relevance to the current need.")],
 ["h_t = tanh(W x_t + U h_{t-1} + b).",
  "LSTM: forget, input and output gates.",
  "Teacher forcing: feed the true previous token in training.",
  "Beam search keeps top-k hypotheses.",
  "Attention weights = softmax(scores)."],
 [T("Language comes in order, so it is natural to process it in order. A recurrent neural network keeps a small memory, the hidden state, a vector. At each step it reads the next word's embedding, mixes it with the old memory through a weight matrix, and squashes the result with tanh to produce the new memory. The same weights are reused at every step, so the network handles sentences of any length."),
  T("The trouble is long distance. Training adjusts weights by passing gradients back through all the steps, and multiplying many numbers below one makes them vanish, so the network cannot learn that the verb at the end agrees with the subject at the start. The LSTM, from Hochreiter and Schmidhuber in 1997, adds a cell state and three gates, learned numbers between zero and one that decide what to forget, what to write and what to reveal. The GRU is a leaner relative."),
  C("import tensorflow as tf\nfrom tensorflow.keras import layers\nmodel = tf.keras.Sequential([\n    layers.Embedding(20000, 128),\n    layers.Bidirectional(layers.LSTM(64)),\n    layers.Dense(1, activation='sigmoid'),\n])\nmodel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])", "python"),
  T("For translation, the sequence-to-sequence model of 2014 uses one RNN, the encoder, to read the source sentence into a vector, and another, the decoder, to write the target one word at a time. At test time the decoder must choose words. Greedy decoding takes the best word each step and can paint itself into a corner, so beam search keeps the k best partial sentences and extends them all."),
  T("Squeezing a long sentence into one vector was a bottleneck. Bahdanau, Cho and Bengio proposed in 2014 that the decoder, at each step, look back over all encoder states and take a weighted average, with weights from a learned score of how relevant each source word is right now. This is attention. It sharply improved translation and also produced pleasing alignment pictures. Within three years, researchers asked what would happen if attention were the only mechanism and the recurrence was thrown out. The answer was the transformer.")],
 [("What does an RNN pass between steps?", ["A hidden state", "A word list", "A label", "A gradient only"], 0, "Memory."),
  ("Why do plain RNNs forget?", ["Vanishing gradients", "Too few words", "Wrong tokens", "Small vocabularies"], 0, "Long chains."),
  ("What do LSTM gates do?", ["Control what to keep, write and output", "Split words", "Reduce vocabulary", "Sort tokens"], 0, "Learned 0..1 switches."),
  ("What does beam search keep?", ["The k best partial outputs", "Only the best word", "All outputs", "Random words"], 0, "k hypotheses."),
  ("What does attention compute?", ["A weighted average of states", "A count", "A sum of letters", "A sort"], 0, "Relevance weights."),
  ("Why did attention help translation?", ["It avoided squeezing a sentence into one vector", "It made words shorter", "It removed the decoder", "It used images"], 0, "Bottleneck.")],
 [("h_t = tanh(Wx + Uh + b)", "RNN update"), ("softmax(score)", "attention weights"), ("beam width k", "hypotheses kept")],
 [MATCH("Match the term", "Pair each sequence idea with its meaning.", [("Hidden state", "network memory"), ("LSTM gate", "learned keep or forget switch"), ("Seq2seq", "encoder then decoder"), ("Beam search", "keep top-k outputs"), ("Attention", "focus on relevant inputs")]),
  PL("RNN step", "Write rnn_step(x, h, Wx, Wh, b): the new hidden state tanh(Wx x + Wh h + b) for vectors, with Wx and Wh given as lists of rows; round to 4 decimals.", "rnn_step(x, h, Wx, Wh, b)", '''
import math
def rnn_step(x, h, Wx, Wh, b):
    out = []
    for i in range(len(b)):
        s = b[i]
        for j in range(len(x)):
            s = s + Wx[i][j] * x[j]
        for j in range(len(h)):
            s = s + Wh[i][j] * h[j]
        out.append(round(math.tanh(s), 4))
    return out
''', [[[1, 0], [0, 0], [[0.5, 0.1], [0.2, 0.3]], [[0.1, 0], [0, 0.1]], [0, 0]], [[0, 1], [0.5, -0.5], [[1, 1]], [[0.5, 0.5]], [0.1]], [[0], [0], [[1]], [[1]], [0]]], "Two matrix products plus bias, then tanh.", approx=None),
  PL("Unroll an RNN", "Write run_rnn(xs, w, u, b): a scalar RNN h_t = tanh(w x_t + u h_{t-1} + b) with h_0 = 0 over the list xs; return the list of hidden states rounded to 3 decimals.", "run_rnn(xs, w, u, b)", '''
import math
def run_rnn(xs, w, u, b):
    h = 0.0
    out = []
    for x in xs:
        h = math.tanh(w * x + u * h + b)
        out.append(round(h, 3))
    return out
''', [[[1, 0, 0], 1.0, 0.5, 0], [[1, 1, 1], 0.5, 0.5, 0.1], [[0, 0], 1, 1, 0]], "Carry h forward.", approx=None),
  PL("Gate", "Write lstm_cell_update(c_prev, f, i, g): the LSTM cell state update c = f x c_prev + i x g (all scalars), rounded to 4 decimals.", "lstm_cell_update(c_prev, f, i, g)", '''
def lstm_cell_update(c_prev, f, i, g):
    return round(f * c_prev + i * g, 4)
''', [[1.0, 0.9, 0.1, 0.5], [2.0, 0.0, 1.0, -1.0], [0.5, 1.0, 0.0, 9.0]], "Forget part of the old, write part of the new.", approx=0.0002),
  PL("Attention weights over states", "Write attend(query, states): scores are dot products of query with each state; return the softmax weights rounded to 4 decimals.", "attend(query, states)", '''
import math
def attend(query, states):
    scores = []
    for s in states:
        scores.append(sum([query[i] * s[i] for i in range(len(query))]))
    m = max(scores)
    e = [math.exp(v - m) for v in scores]
    t = sum(e)
    return [round(v / t, 4) for v in e]
''', [[[1, 0], [[1, 0], [0, 1], [1, 1]]], [[0, 0], [[1, 2], [3, 4]]], [[2, 0], [[1, 0], [0, 5]]]], "Softmax of dot products.", approx=None),
  PL("Context vector", "Write context(weights, states): the weighted sum of the state vectors, rounded to 4 decimals.", "context(weights, states)", '''
def context(weights, states):
    dim = len(states[0])
    out = [0.0] * dim
    for w, s in zip(weights, states):
        for j in range(dim):
            out[j] = out[j] + w * s[j]
    return [round(v, 4) for v in out]
''', [[[0.5, 0.5], [[1, 0], [0, 1]]], [[1, 0, 0], [[3, 4], [1, 1], [0, 0]]], [[0.2, 0.8], [[10], [20]]]], "Blend the encoder states.", approx=None),
  PL("Beam search step", "Write beam_step(beams, next_probs, k): beams is a list of [sequence (list), score (log prob)]; next_probs is a list of probabilities of each vocabulary index. Extend every beam with every token; the new score is score + log(p). Return the k best as [sequence, score rounded to 3 decimals], sorted by score descending (ties: lower token index first, earlier beam first).", "beam_step(beams, next_probs, k)", '''
import math
def beam_step(beams, next_probs, k):
    cand = []
    for bi in range(len(beams)):
        seq = beams[bi][0]
        sc = beams[bi][1]
        for t in range(len(next_probs)):
            if next_probs[t] > 0:
                cand.append((-(sc + math.log(next_probs[t])), bi, t, seq + [t], sc + math.log(next_probs[t])))
    cand.sort(key=lambda c: (round(c[0], 9), c[1], c[2]))
    return [[c[3], round(c[4], 3)] for c in cand[:k]]
''', [[[[[], 0.0]], [0.5, 0.3, 0.2], 2], [[[[0], -0.5], [[1], -0.7]], [0.6, 0.4], 3], [[[[2], -1.0]], [1.0], 1]], "Keep the k highest-scoring extensions.", approx=None),
  PL("Greedy decode", "Write greedy(table, start, steps): table maps each token index to a list of next-token probabilities (a list of lists). Starting at token start, repeatedly append the index of the highest probability (lowest index on ties) for steps steps. Return the list of tokens including start.", "greedy(table, start, steps)", '''
def greedy(table, start, steps):
    out = [start]
    for s in range(steps):
        row = table[out[-1]]
        best = 0
        for i in range(len(row)):
            if row[i] > row[best]:
                best = i
        out.append(best)
    return out
''', [[[[0.1, 0.9], [0.8, 0.2]], 0, 4], [[[0.5, 0.5], [0.5, 0.5]], 1, 2], [[[0, 1, 0], [0, 0, 1], [1, 0, 0]], 0, 5]], "Always take the arg max.")]
))

CHS.append(CH(
 "Transformers: self-attention, positions and tokenisers",
 ("Transformers", [
  "Self-attention | relates | All tokens",
  "Query key value | define | Attention",
  "Multi-head | looks | In several ways",
  "Positional encoding | adds | Order",
  "Causal mask | hides | The future",
  "BPE | merges | Frequent pairs",
  "Layer norm | stabilises | Training"]),
 ["The transformer replaces recurrence with self-attention: every token compares its query with every token's key and takes a weighted average of their values. All positions are processed in parallel, which makes training fast on GPUs.",
  "Because attention ignores order, positional information is added. Several attention heads run in parallel, followed by feed-forward layers, residual connections and layer normalisation, repeated in a stack of blocks.",
  "Text enters as subword tokens, built by algorithms such as byte-pair encoding, which merges the most frequent adjacent pairs to make a vocabulary of tens of thousands of pieces."],
 [("Self-attention", "A layer where each token's output is a weighted mix of all tokens' values, with weights from query-key similarity."),
  ("Multi-head attention", "Several attention operations in parallel, each with its own projections, whose outputs are concatenated."),
  ("Positional encoding", "Extra information added to token embeddings so the model knows their order."),
  ("Causal mask", "A mask that prevents a position from attending to later positions, used for left-to-right generation."),
  ("Byte-pair encoding", "A tokenisation method that repeatedly merges the most frequent pair of symbols.")],
 ["Attention(Q, K, V) = softmax(QK^T / sqrt(d)) V.",
  "Block = attention + MLP, each with residual and norm.",
  "Causal mask: position i sees positions up to i.",
  "Sinusoidal positions: sin and cos at many frequencies.",
  "BPE: merge most frequent pair, repeat."],
 [T("The 2017 paper 'Attention Is All You Need' began a revolution. Its idea: let every token look directly at every other token. Each token produces three vectors from its embedding: a query, saying what it is looking for; a key, saying what it offers; and a value, the content to pass on. The match between a query and each key, the dot product, scaled down by the square root of the vector length, is turned into weights by a softmax. The output is the weighted sum of values."),
  T("Compare with the RNN. A recurrent network passes information along a chain, so a word at the start reaches the end only through many steps. In self-attention any two tokens interact in one step, so long-range dependencies are easy. And since no step waits for the previous one, a whole sentence is computed in parallel, which is why transformers could be trained on far more data than RNNs."),
  C("import torch, math\ndef attention(Q, K, V, mask=None):\n    scores = Q @ K.transpose(-2, -1) / math.sqrt(Q.size(-1))\n    if mask is not None:\n        scores = scores.masked_fill(mask == 0, float('-inf'))\n    return torch.softmax(scores, dim=-1) @ V\n\nL = 5\ncausal = torch.tril(torch.ones(L, L))   # position i sees j <= i", "python"),
  T("Attention treats the input as a set, so a sentence and its scrambled version would look alike. Positional information fixes this. The original paper added sinusoids of many frequencies to the embeddings; modern models rotate the query and key vectors by position-dependent angles (rotary embeddings) or learn the positions. For text generation a causal mask blocks each position from seeing later ones, so the model can be trained to predict every next word in parallel. A full block adds a position-wise feed-forward network, a residual connection around each part, and layer normalisation. Multi-head attention runs several smaller attentions side by side so each can specialise."),
  T("How does text become the model's input? Word-level vocabularies fail on rare words and typos; character-level sequences are too long. Byte-pair encoding splits the difference. Start with characters. Count adjacent pairs, merge the most frequent into a new symbol, and repeat tens of thousands of times. Common words become single tokens, rare ones split into pieces, and anything can be spelled with bytes. The model never sees spelling directly, which explains odd failures such as counting the letters of a word.")],
 [("What does a query match against?", ["Keys", "Values", "Positions", "Labels"], 0, "Q dot K."),
  ("Why divide by sqrt(d)?", ["To keep scores moderate for softmax", "To add noise", "To mask", "To sort"], 0, "Stabilise."),
  ("Why positional encodings?", ["Attention alone ignores order", "To shrink vectors", "To add vocabulary", "To remove noise"], 0, "Order."),
  ("What does a causal mask do?", ["Blocks attention to later tokens", "Blocks attention to earlier tokens", "Removes padding", "Doubles the heads"], 0, "Left to right."),
  ("What does BPE merge?", ["The most frequent adjacent pair", "The rarest word", "Two sentences", "Heads"], 0, "Repeatedly."),
  ("Why is a transformer fast to train?", ["Positions are processed in parallel", "It has no weights", "It uses fewer data", "It is recurrent"], 0, "No sequential chain.")],
 [("softmax(QK^T/sqrt(d)) V", "scaled dot-product attention"), ("tril(ones(L, L))", "causal mask"), ("BPE merges", "learned tokeniser")],
 [APP("ATTN", "Self-attention explorer", "Pick a sentence and a token and see where it attends. Change the temperature and turn the causal mask on and off. Explore three different tokens to complete the lab.", 800),
  MATCH("Match the term", "Pair each transformer part with its job.", [("Query", "what a token looks for"), ("Key", "what a token offers"), ("Value", "content passed on"), ("Causal mask", "hide the future"), ("BPE", "build subword vocabulary")]),
  PL("Scaled dot-product attention", "Write sdpa(Q, K, V): for lists of vectors compute softmax(Q K^T / sqrt(d)) V where d is the vector length; return the output vectors rounded to 3 decimals.", "sdpa(Q, K, V)", '''
import math
def sdpa(Q, K, V):
    d = len(Q[0])
    out = []
    for q in Q:
        sc = [sum([q[i] * k[i] for i in range(d)]) / math.sqrt(d) for k in K]
        m = max(sc)
        e = [math.exp(s - m) for s in sc]
        t = sum(e)
        w = [x / t for x in e]
        dv = len(V[0])
        o = [0.0] * dv
        for a in range(len(V)):
            for j in range(dv):
                o[j] = o[j] + w[a] * V[a][j]
        out.append([round(x, 3) for x in o])
    return out
''', [[[[1, 0]], [[1, 0], [0, 1]], [[10, 0], [0, 10]]], [[[0, 0]], [[1, 2], [3, 4]], [[1, 1], [3, 3]]], [[[1, 0], [0, 1]], [[1, 0], [0, 1]], [[1, 2], [3, 4]]]], "Scores, softmax, weighted sum of values.", approx=None),
  PL("Causal mask", "Write causal_mask(L): an L x L matrix of 1 where column j <= row i (allowed) and 0 elsewhere.", "causal_mask(L)", '''
def causal_mask(L):
    return [[1 if j <= i else 0 for j in range(L)] for i in range(L)]
''', [[3], [1], [4]], "Lower triangle."),
  PL("Masked softmax row", "Write masked_softmax(scores, mask): softmax of the scores where mask is 1; masked positions get weight 0. Round to 4 decimals.", "masked_softmax(scores, mask)", '''
import math
def masked_softmax(scores, mask):
    vals = [scores[i] for i in range(len(scores)) if mask[i] == 1]
    m = max(vals)
    e = [math.exp(scores[i] - m) if mask[i] == 1 else 0.0 for i in range(len(scores))]
    t = sum(e)
    return [round(v / t, 4) for v in e]
''', [[[1, 2, 3], [1, 1, 0]], [[0, 0, 0], [1, 0, 0]], [[1, 1], [1, 1]]], "Ignore masked entries."),
  PL("Sinusoidal positions", "Write pos_encoding(pos, d): the sinusoidal position vector of even length d: for i = 0, 2, 4, ... the pair [sin(pos / 10000^(i/d)), cos(pos / 10000^(i/d))]. Return the flat list rounded to 4 decimals.", "pos_encoding(pos, d)", '''
import math
def pos_encoding(pos, d):
    out = []
    for i in range(0, d, 2):
        a = pos / (10000.0 ** (i / float(d)))
        out.append(round(math.sin(a), 4))
        out.append(round(math.cos(a), 4))
    return out
''', [[0, 4], [1, 4], [5, 2], [3, 6]], "Frequencies fall with the index.", approx=None),
  PL("One BPE merge", "Write bpe_merge(words): words is a list of token lists (each word a list of symbols). Find the most frequent adjacent pair across all words (ties: alphabetically first pair) and merge every occurrence into one symbol (the two joined). Return [pair as [a, b], new list of words].", "bpe_merge(words)", '''
def bpe_merge(words):
    counts = {}
    for w in words:
        for i in range(len(w) - 1):
            k = (w[i], w[i + 1])
            counts[k] = counts.get(k, 0) + 1
    best = None
    for k in sorted(counts.keys()):
        if best is None or counts[k] > counts[best]:
            best = k
    new = []
    for w in words:
        out = []
        i = 0
        while i < len(w):
            if i < len(w) - 1 and (w[i], w[i + 1]) == best:
                out.append(w[i] + w[i + 1])
                i = i + 2
            else:
                out.append(w[i])
                i = i + 1
        new.append(out)
    return [[best[0], best[1]], new]
''', [[[['l', 'o', 'w'], ['l', 'o', 'w', 'e', 'r'], ['n', 'e', 'w']]], [[['a', 'b', 'a', 'b']]], [[['x', 'y'], ['y', 'x']]]], "Count pairs, then merge them."),
  PL("Greedy subword tokenise", "Write wordpiece(word, vocab): split the word by repeatedly taking the longest prefix that is in vocab (single characters are always allowed). Return the list of pieces.", "wordpiece(word, vocab)", '''
def wordpiece(word, vocab):
    out = []
    i = 0
    while i < len(word):
        j = len(word)
        while j > i + 1 and word[i:j] not in vocab:
            j = j - 1
        out.append(word[i:j])
        i = j
    return out
''', [['unhappiness', ['un', 'happi', 'ness', 'happy']], ['lowest', ['low', 'est', 'lo']], ['xyz', ['xy']]], "Longest match first."),
  PL("Parameter count of a block", "Write block_params(d, ff): the weights (no biases) of one transformer block: four d x d attention matrices (Q, K, V, output) plus a feed-forward network d x ff and ff x d.", "block_params(d, ff)", '''
def block_params(d, ff):
    return 4 * d * d + 2 * d * ff
''', [[768, 3072], [512, 2048], [4096, 11008]], "Attention plus feed-forward.")]
))

CHS.append(CH(
 "Pretrained language models: BERT, GPT and beyond",
 ("Pretraining", [
  "Pretraining | learns | From raw text",
  "Fine-tuning | adapts | To a task",
  "BERT | is | An encoder",
  "GPT | is | A decoder",
  "Masked LM | fills | Blanks",
  "Next token | predicts | Left to right",
  "Prompting | steers | Without training"]),
 ["Modern NLP follows pretrain then adapt. A transformer is first trained on huge text with a self-supervised goal, then fine-tuned or prompted for tasks. Encoder models like BERT read the whole text both ways and produce contextual embeddings, suited to classification and tagging. Decoder models like GPT, Llama and Claude generate text left to right, one token at a time.",
  "Scaling model size, data and compute improved quality predictably and revealed abilities such as in-context learning, where the model follows examples in its prompt.",
  "Large models are further aligned with instruction tuning and human feedback so they follow requests helpfully and safely."],
 [("Pretraining", "Training a large model on unlabeled data with a self-supervised objective such as predicting masked or next tokens."),
  ("Masked language modelling", "Hiding some tokens and training the model to recover them from context in both directions."),
  ("Causal language modelling", "Training the model to predict each token from the ones before it."),
  ("In-context learning", "Performing a new task from instructions and examples given in the prompt, without weight updates."),
  ("Instruction tuning and RLHF", "Further training so the model follows instructions, using demonstrations and human preference feedback.")],
 ["Encoder: BERT, bidirectional, masked LM.",
  "Decoder: GPT, Llama, Claude, causal LM.",
  "Fine-tune with a small labelled set.",
  "Prompt: instructions plus examples.",
  "Temperature, top-k and top-p control sampling."],
 [T("Before 2018, each NLP task trained its own model from scratch on its own small labelled dataset. Then came a new recipe. Pretrain one large model on enormous amounts of plain text using a goal that needs no labels, then adapt it to each task cheaply. This is transfer learning, as in vision, and it lifted every benchmark at once."),
  T("BERT, from Google in 2018, is an encoder. It sees a whole sentence at once with attention flowing both ways. It is pretrained by masking about fifteen percent of the tokens and asking the model to fill them in, which forces it to use left and right context. The result is a contextual embedding for every token: the vector for 'bank' differs by sentence. To classify, add a small head on top and fine-tune on a few thousand labelled examples. Encoder models and their successors, such as RoBERTa and ModernBERT, remain the efficient workhorses for classification, tagging, search and embeddings."),
  C("from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification\nclf = pipeline('sentiment-analysis')\nprint(clf('The plot was thin but the acting was wonderful.'))\n\ngen = pipeline('text-generation', model='gpt2')\nprint(gen('Natural language processing is', max_new_tokens=20, do_sample=True, temperature=0.8))", "python"),
  T("GPT, from OpenAI, is a decoder. It reads left to right under a causal mask and is trained to predict the next token. That one simple goal, applied to a large part of the written internet, teaches grammar, facts, style and a lot of reasoning. Scaling up gave GPT-2, GPT-3 and the line of large language models, including Llama and Claude. The surprise was in-context learning: show a big model a few examples in the prompt and it performs the task with no training."),
  T("A raw pretrained model continues text; it does not obey. Instruction tuning on prompt and answer pairs, then reinforcement learning from human feedback or similar preference methods, turns it into an assistant that follows requests and refuses harmful ones. At generation time, sampling settings matter: temperature scales how adventurous choices are, and top-k or top-p keep only the likeliest tokens. Evaluation is hard, since open-ended answers have no single right text. Later in your studies, a dedicated course on decision models looks at a new use of encoders and decoders: instead of writing text, answering fixed questions with calibrated probabilities in one pass.")],
 [("How does BERT pretrain?", ["By filling in masked tokens", "By predicting the next word only", "By translating", "By labelling images"], 0, "Masked LM."),
  ("How does GPT pretrain?", ["By predicting the next token", "By masking", "By clustering", "By parsing"], 0, "Causal LM."),
  ("What is in-context learning?", ["Doing a task from prompt examples without training", "Fine-tuning weights", "Learning in class", "Tokenising"], 0, "Few-shot."),
  ("What does instruction tuning add?", ["Following instructions", "More vocabulary", "Smaller models", "Image input"], 0, "Assistant behaviour."),
  ("What does temperature control?", ["How random sampling is", "Model size", "Speed of training", "Vocabulary"], 0, "Higher is more varied."),
  ("Which models suit classification and tagging?", ["Encoders like BERT", "Only decoders", "Only RNNs", "None"], 0, "Contextual embeddings.")],
 [("[MASK]", "BERT's blank token"), ("pipeline('text-generation')", "Hugging Face generation"), ("temperature, top_p", "sampling controls")],
 [MATCH("Match the model idea", "Pair each model type with its feature.", [("BERT", "encoder, masked LM"), ("GPT", "decoder, next token"), ("RLHF", "learn from human preferences"), ("Few-shot prompt", "examples in the prompt"), ("Fine-tuning", "adapt weights to a task")]),
  PL("Mask tokens", "Write mask_tokens(tokens, positions): replace the tokens at the given positions with '[MASK]'; return the new list and the list of original tokens at those positions as [masked, targets].", "mask_tokens(tokens, positions)", '''
def mask_tokens(tokens, positions):
    out = list(tokens)
    targets = []
    for p in positions:
        targets.append(tokens[p])
        out[p] = '[MASK]'
    return [out, targets]
''', [[['the', 'cat', 'sat'], [1]], [['a', 'b', 'c', 'd'], [0, 3]], [['x'], []]], "Hide and remember."),
  PL("Temperature", "Write apply_temperature(logits, T): the softmax of logits divided by T, rounded to 4 decimals.", "apply_temperature(logits, T)", '''
import math
def apply_temperature(logits, T):
    scaled = [v / T for v in logits]
    m = max(scaled)
    e = [math.exp(v - m) for v in scaled]
    t = sum(e)
    return [round(v / t, 4) for v in e]
''', [[[2, 1, 0], 1], [[2, 1, 0], 0.5], [[2, 1, 0], 2], [[0, 0], 1]], "Low T sharpens, high T flattens.", approx=None),
  PL("Top-k filter", "Write top_k(probs, k): keep the k largest probabilities (ties: lower index first), set the rest to 0 and renormalise; round to 4 decimals.", "top_k(probs, k)", '''
def top_k(probs, k):
    order = sorted(range(len(probs)), key=lambda i: (-probs[i], i))
    keep = set(order[:k])
    s = sum([probs[i] for i in keep])
    return [round(probs[i] / s, 4) if i in keep else 0 for i in range(len(probs))]
''', [[[0.5, 0.3, 0.2], 2], [[0.25, 0.25, 0.25, 0.25], 1], [[0.6, 0.4], 5]], "Keep the biggest few."),
  PL("Top-p (nucleus)", "Write top_p(probs, p): sort probabilities descending (ties: lower index first) and keep the smallest set whose cumulative probability reaches p; set the others to 0 and renormalise; round to 4 decimals.", "top_p(probs, p)", '''
def top_p(probs, p):
    order = sorted(range(len(probs)), key=lambda i: (-probs[i], i))
    keep = []
    cum = 0.0
    for i in order:
        keep.append(i)
        cum = cum + probs[i]
        if cum >= p - 1e-12:
            break
    ks = set(keep)
    s = sum([probs[i] for i in ks])
    return [round(probs[i] / s, 4) if i in ks else 0 for i in range(len(probs))]
''', [[[0.5, 0.3, 0.2], 0.7], [[0.5, 0.3, 0.2], 0.5], [[0.4, 0.3, 0.2, 0.1], 0.95]], "Smallest set reaching p."),
  PL("Token F1 (QA)", "Write token_f1(pred, gold): the F1 score between two token lists, counting overlapping tokens with multiplicity (common = sum of min counts); rounded to 3 decimals; 0 if no overlap.", "token_f1(pred, gold)", '''
def token_f1(pred, gold):
    common = 0
    used = list(gold)
    for t in pred:
        if t in used:
            common = common + 1
            used.remove(t)
    if common == 0:
        return 0
    p = common / float(len(pred))
    r = common / float(len(gold))
    return round(2 * p * r / (p + r), 3)
''', [[['the', 'big', 'cat'], ['a', 'big', 'cat']], [['x'], ['y']], [['a', 'a', 'b'], ['a', 'b', 'b']]], "Precision and recall of tokens.", approx=0.002),
  PL("Few-shot prompt", "Write build_prompt(instruction, examples, query): examples is a list of [input, output]; return the string instruction + newline, then for each example 'Input: x' newline 'Output: y' newline, then 'Input: query' newline 'Output:' (exact format).", "build_prompt(instruction, examples, query)", '''
def build_prompt(instruction, examples, query):
    s = instruction + '\\n'
    for x, y in examples:
        s = s + 'Input: ' + x + '\\n' + 'Output: ' + y + '\\n'
    s = s + 'Input: ' + query + '\\n' + 'Output:'
    return s
''', [['Classify the sentiment.', [['great film', 'positive'], ['awful', 'negative']], 'quite nice'], ['Translate.', [], 'hello']], "Join the pieces with newlines.")]
))

CHS.append(CH(
 "Applications: search, QA, translation and responsible NLP",
 ("Applications", [
  "BM25 | ranks | Documents for a query",
  "Inverted index | maps | Words to documents",
  "RAG | grounds | Generation in documents",
  "BLEU ROUGE | score | Text overlap",
  "Machine translation | maps | Language to language",
  "Hallucination | is | Unsupported output",
  "Bias | needs | Evaluation"]),
 ["Search engines use an inverted index to find documents containing query words and rank them with BM25, a refined TF-IDF. Modern systems add embedding-based dense retrieval and neural rerankers.",
  "Retrieval-augmented generation (RAG) retrieves relevant passages and puts them in the prompt of a language model so its answer is grounded in sources. Machine translation, summarisation and question answering are evaluated with overlap metrics such as BLEU and ROUGE, and increasingly by human or model judges.",
  "Responsible NLP means checking for hallucination, bias, privacy leaks and misuse, and testing on the people the system will serve."],
 [("Inverted index", "A map from each word to the list of documents containing it."),
  ("BM25", "A ranking function combining term frequency with saturation, length normalisation and IDF."),
  ("RAG", "Retrieval-augmented generation: fetching documents and giving them to a model to ground its answer."),
  ("BLEU", "A translation metric measuring n-gram overlap between output and reference translations."),
  ("Hallucination", "Fluent output that is not supported by the input or facts.")],
 ["Inverted index: word -> document ids.",
  "BM25 saturates term frequency.",
  "RAG: retrieve, then generate.",
  "Chunk long documents with overlap.",
  "Check facts, bias and privacy."],
 [T("When you search a million pages you do not scan them. A search engine builds an inverted index in advance: for each word, the list of documents that contain it. A query is answered by looking up its words and intersecting or merging the lists. Then the candidates are ranked. BM25 is the classic ranking function: like TF-IDF, but extra occurrences of a word count for less and less, and long documents are penalised gently."),
  T("Embeddings add meaning. Encode documents and queries as dense vectors with an encoder model and retrieve the nearest, so 'cheap flights' also finds 'low-cost airfare'. Production search often combines the two, lexical and dense, and finishes with a reranker, a model that reads the query and each candidate together and scores them accurately. Quality is measured by precision at k, recall at k and mean reciprocal rank."),
  C("from rank_bm25 import BM25Okapi\ncorpus = [d.lower().split() for d in docs]\nbm25 = BM25Okapi(corpus)\nscores = bm25.get_scores('refund policy'.split())\n\n# RAG skeleton\nhits = retrieve(query, k=4)\ncontext = '\\n\\n'.join(h.text for h in hits)\nprompt = f'Answer using only the context.\\n\\nContext:\\n{context}\\n\\nQuestion: {query}'\nanswer = llm(prompt)", "python"),
  T("Large language models know a lot but can make things up and cannot know your private or recent documents. Retrieval-augmented generation fixes both: retrieve the relevant passages, paste them into the prompt, and instruct the model to answer from them and cite them. Long documents are cut into overlapping chunks so that no answer is split across a boundary. Retrieval quality is usually the limit of such systems."),
  T("Other tasks have their own metrics. Machine translation systems are scored by BLEU, the overlap of n-grams with human reference translations, and summaries by ROUGE, which stresses recall. Overlap scores are crude, so human review and carefully validated model judges are used too. Finally, responsibility: language models learn from human text and inherit its stereotypes, may leak private data, may state falsehoods with confidence and can be misused. Test on the groups and languages your users speak, measure rather than assume, keep humans in the loop for high-stakes uses, and be open about limits.")],
 [("What does an inverted index map?", ["Words to documents", "Documents to words", "Letters to words", "Sentences to labels"], 0, "Look up fast."),
  ("What does BM25 improve on TF-IDF?", ["Saturating term frequency and length normalisation", "Colours", "Spelling", "Speed of typing"], 0, "Diminishing returns."),
  ("What is RAG?", ["Retrieve documents then generate with them", "A tokenizer", "A metric", "A stemmer"], 0, "Grounded answers."),
  ("What does BLEU measure?", ["N-gram overlap with references", "Sentiment", "Speed", "Vocabulary size"], 0, "Translation."),
  ("What is a hallucination?", ["Fluent but unsupported output", "A slow reply", "A short answer", "A rare word"], 0, "Made-up claims."),
  ("Why chunk with overlap?", ["Answers may span a boundary", "To save memory", "To remove stopwords", "To stem"], 0, "Avoid splits.")],
 [("BM25", "lexical ranking"), ("precision@k, MRR", "retrieval metrics"), ("retrieve then generate", "RAG")],
 [MATCH("Match the term", "Pair each application idea with its meaning.", [("Inverted index", "word to documents"), ("BM25", "lexical ranking function"), ("RAG", "ground generation in documents"), ("BLEU", "translation overlap score"), ("Reranker", "accurate second-stage scorer")]),
  PL("Build an inverted index", "Write inverted_index(docs): docs is a list of token lists; return [word, sorted list of document ids containing it] pairs sorted by word.", "inverted_index(docs)", '''
def inverted_index(docs):
    d = {}
    for i, doc in enumerate(docs):
        for w in set(doc):
            d.setdefault(w, []).append(i)
    return [[w, sorted(d[w])] for w in sorted(d.keys())]
''', [[[['a', 'b'], ['b', 'c'], ['a']]], [[[]]], [[['x', 'x']]]], "Add each document to each word's list once."),
  PL("Boolean AND query", "Write search_and(docs, words): the sorted ids of documents containing all the words.", "search_and(docs, words)", '''
def search_and(docs, words):
    return [i for i in range(len(docs)) if all([w in docs[i] for w in words])]
''', [[[['a', 'b'], ['b', 'c'], ['a', 'b', 'c']], ['b', 'c']], [[['a']], ['z']], [[['a']], []]], "Intersect the conditions."),
  PL("BM25 score", "Write bm25(query, doc, docs, k1, b): the BM25 score of a token-list doc for the query tokens, using idf = ln((N - df + 0.5) / (df + 0.5) + 1), the term-frequency part tf (k1 + 1) / (tf + k1 (1 - b + b len(doc) / avgdl)), summed over query terms. Round to 4 decimals.", "bm25(query, doc, docs, k1, b)", '''
import math
def bm25(query, doc, docs, k1, b):
    N = len(docs)
    avgdl = sum([len(d) for d in docs]) / float(N)
    s = 0.0
    for q in query:
        df = len([d for d in docs if q in d])
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
        tf = doc.count(q)
        s = s + idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(doc) / avgdl))
    return round(s, 4)
''', [[['cat'], ['the', 'cat', 'sat'], [['the', 'cat', 'sat'], ['a', 'dog'], ['the', 'dog']], 1.5, 0.75], [['dog', 'the'], ['a', 'dog'], [['the', 'cat', 'sat'], ['a', 'dog'], ['the', 'dog']], 1.2, 0.75], [['zzz'], ['a'], [['a'], ['b']], 1.5, 0.75]], "Sum over query terms.", approx=0.0005),
  PL("Precision and recall at k", "Write pr_at_k(ranked, relevant, k): [precision@k, recall@k] for a ranked list of ids and the set of relevant ids, each rounded to 3 decimals.", "pr_at_k(ranked, relevant, k)", '''
def pr_at_k(ranked, relevant, k):
    top = ranked[:k]
    hit = len([d for d in top if d in relevant])
    return [round(hit / float(k), 3), round(hit / float(len(relevant)), 3)]
''', [[[3, 1, 4, 2], [1, 2, 9], 3], [[1, 2], [1, 2], 2], [[5, 6, 7], [7], 1]], "Count relevant items in the top k.", approx=None),
  PL("Mean reciprocal rank", "Write mrr(rankings, relevants): for each query, 1 / rank of the first relevant id in its ranking (0 if none); return the mean rounded to 3 decimals. rankings is a list of id lists and relevants a list of id lists.", "mrr(rankings, relevants)", '''
def mrr(rankings, relevants):
    total = 0.0
    for r, rel in zip(rankings, relevants):
        score = 0.0
        for i, d in enumerate(r):
            if d in rel:
                score = 1.0 / (i + 1)
                break
        total = total + score
    return round(total / len(rankings), 3)
''', [[[[1, 2, 3], [4, 5, 6]], [[2], [4]]], [[[1, 2]], [[9]]], [[[7, 8]], [[8]]]], "Reciprocal of the first hit.", approx=0.002),
  PL("Chunk text", "Write chunk(tokens, size, overlap): split the token list into windows of size tokens, each starting size - overlap after the previous one; stop when a window reaches the end.", "chunk(tokens, size, overlap)", '''
def chunk(tokens, size, overlap):
    out = []
    i = 0
    step = size - overlap
    while True:
        out.append(tokens[i:i + size])
        if i + size >= len(tokens):
            break
        i = i + step
    return out
''', [[[1, 2, 3, 4, 5, 6, 7], 3, 1], [[1, 2], 5, 2], [[1, 2, 3, 4], 2, 0]], "Slide with overlap."),
  PL("Unigram BLEU precision", "Write unigram_precision(candidate, reference): the fraction of candidate tokens that appear in the reference, clipped by how many times each appears there, rounded to 3 decimals.", "unigram_precision(candidate, reference)", '''
def unigram_precision(candidate, reference):
    ref = list(reference)
    hit = 0
    for t in candidate:
        if t in ref:
            hit = hit + 1
            ref.remove(t)
    return round(hit / float(len(candidate)), 3)
''', [[['the', 'the', 'the', 'cat'], ['the', 'cat', 'sat']], [['a', 'b'], ['a', 'b']], [['x'], ['y']]], "Clip repeated words.", approx=0.002)]
))
