"""Transformer course."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "Attention Is All You Need: the big picture",
 ("The Transformer", [
  "Transformer | introduced in | Attention Is All You Need",
  "Transformer | replaces | Recurrence and convolution",
  "Encoder | reads | Source sequence",
  "Decoder | writes | Target sequence",
  "Attention | connects | Any two positions",
  "Base model | has | 6 layers each side",
  "Authors | include | Vaswani and colleagues"]),
 ["The Transformer is a sequence model built from attention alone. It was introduced in the 2017 paper Attention Is All You Need by Vaswani and colleagues at Google.",
  "Earlier translation models read words one at a time with recurrent networks. The Transformer lets every position look at every other position in one step, which is easier to run in parallel and easier to train.",
  "It has two stacks. The encoder reads the source sentence. The decoder writes the target sentence one word at a time, looking at the encoder's output."],
 [("Transformer", "A neural network for sequences that uses attention instead of recurrence."),
  ("Encoder", "The stack that turns the source sequence into context vectors."),
  ("Decoder", "The stack that generates the target sequence using the encoder output."),
  ("Attention", "A weighted average of values, with weights from query-key similarity."),
  ("Recurrence", "Processing a sequence one step at a time, passing a hidden state."),
  ("Token", "One unit of text, such as a word or word piece.")],
 ["Published at NeurIPS 2017: Attention Is All You Need.",
  "The base model has 6 encoder layers, 6 decoder layers, model width 512 and 8 heads.",
  "It achieved 28.4 BLEU on English to German with the big model, and 41.8 on English to French.",
  "No recurrence and no convolution: only attention and feed-forward layers.",
  "Training is parallel over positions, unlike a recurrent network.",
  "The same blocks later became the basis of BERT, GPT and most large language models (background)."],
 [T("Before 2017 the best translation systems used recurrent networks. A recurrent network reads a sentence one word at a time, updating a hidden state. That is slow to train, since each step waits for the one before. Long-range links are also hard: information from the first word must survive many updates to reach the last."),
  T("The Transformer, by Ashish Vaswani and colleagues, removes the recurrence. It relies on attention: every position can look directly at every other position and take a weighted average of what it finds. Because all positions are processed at once, training uses modern hardware far better. The base model trained for 12 hours on 8 GPUs."),
  T("The architecture has an encoder and a decoder. The encoder is a stack of 6 identical layers. Each has two parts: a self-attention step, where the source words look at each other, and a small feed-forward network. The decoder is also a stack of 6 layers. It has the same two parts plus a third, in which the target words look at the encoder's output."),
  M(r"\text{source} \xrightarrow{\ \text{encoder}\ } \text{memory} \xrightarrow{\ \text{decoder}\ } \text{target, one token at a time}"),
  T("The results made the point. On the WMT 2014 English to German task, the big Transformer reached 28.4 BLEU, better than all earlier models including ensembles. On English to French it reached 41.8. It trained in a fraction of the cost of the competition. The authors also showed the model worked for parsing, so it was not only a translator."),
  T("This course follows the paper. We build each piece in small Python labs with plain lists: positional encoding, attention, heads, masks, layer normalization, the encoder and decoder layers, the learning rate schedule and decoding. Facts about later models such as BERT and GPT are marked as background knowledge.")],
 [("What did the Transformer remove?", ["Recurrence and convolution", "Attention", "The decoder", "Embeddings"], 0, "Only attention and feed-forward layers remain."),
  ("How many layers does the base encoder have?", ["6", "12", "2", "24"], 0, "N = 6."),
  ("Why is training faster than with recurrence?", ["All positions are processed in parallel", "Fewer words", "Smaller data", "No gradients"], 0, "No step waits for the previous one."),
  ("What does the decoder look at besides itself?", ["The encoder output", "The loss", "The dataset", "The optimizer"], 0, "Cross-attention.")],
 [("Who wrote the paper?", "Vaswani and colleagues at Google."), ("What replaced recurrence?", "Self-attention."), ("What were the two parts of each encoder layer?", "Self-attention and a feed-forward network."), ("What was the English to French BLEU?", "41.8 for the big model.")],
 [ORDER("Translation pipeline", "Put the steps in order.", ["Embed the source tokens", "Encoder layers build the memory", "Decoder embeds the target so far", "Decoder layers attend to the memory", "Predict the next target token"]),
  MATCH("Parts", "Match each part with its role.", [("Encoder", "Reads the source"), ("Decoder", "Writes the target"), ("Self-attention", "Positions look at each other"), ("Cross-attention", "Decoder looks at the memory"), ("Feed-forward", "Per-position network")]),
  FILL("Basics", "The Transformer uses {{attention}} instead of recurrence. The base model has {{6}} layers in each stack.")]))

CHS.append(CH(
 "Embeddings and positional encoding",
 ("Inputs", [
  "Embedding | maps | Token to vector",
  "Embedding | scaled by | Square root of d_model",
  "Attention | ignores | Order",
  "Positional encoding | adds | Order information",
  "Sinusoids | encode | Position",
  "Wavelengths | form | Geometric progression",
  "Sum | feeds | First layer"]),
 ["Attention treats its input as a set: it does not know which word came first. So the model adds a positional encoding to each embedding. The paper uses fixed sine and cosine waves of different wavelengths.",
  "Each token id is first mapped to a vector of size d_model by an embedding table. The paper multiplies the embeddings by the square root of d_model, then adds the positional encoding.",
  "The labs compute the encoding and look at how neighbouring positions relate."],
 [("Embedding", "A learned table that maps each token id to a vector."),
  ("d_model", "The width of the vectors flowing through the model; 512 in the base model."),
  ("Positional encoding", "A vector added to the embedding that depends on the position."),
  ("Sinusoid", "A sine or cosine wave."),
  ("Wavelength", "The distance over which a wave repeats."),
  ("Permutation invariance", "Giving the same answer when the input order is shuffled.")],
 ["PE(pos, 2i) = sin(pos / 10000^(2i/d_model)); PE(pos, 2i+1) = cos(same).",
  "Wavelengths run from 2 pi to 10000 times 2 pi.",
  "The authors chose sinusoids because they might let the model extrapolate to longer sequences.",
  "They also tried learned position embeddings and found nearly identical results.",
  "Embedding weights are multiplied by the square root of d_model.",
  "The encoding is added, not concatenated."],
 [T("Self-attention has a blind spot. If you shuffle the words of the input, the attention computation gives the same set of outputs, merely shuffled. It has no sense of order. But order matters: dog bites man is not man bites dog. The model must be told where each word sits."),
  T("The paper's answer is to add a position signal to each embedding. Position pos and dimension pair i give two numbers, a sine and a cosine, whose frequency depends on i. Low dimensions oscillate fast; high ones slowly."),
  M(r"PE_{(pos,\,2i)} = \sin\!\left(\frac{pos}{10000^{2i/d_{\mathrm{model}}}}\right), \qquad PE_{(pos,\,2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/d_{\mathrm{model}}}}\right)"),
  T("Why sines and cosines? Each dimension is a wave, and the wavelengths form a geometric progression from 2 pi up to 10000 times 2 pi. The authors hypothesised that this makes it easy to attend by relative position, because a shift by a fixed offset acts on each sine and cosine pair as a rotation. They also tried learned position vectors, and report nearly identical results. They kept sinusoids because these might extrapolate to sequences longer than those seen in training."),
  T("The input to the first layer is therefore the sum of two things: the token embedding, multiplied by the square root of d model, and the position vector. Summing keeps the width at d model. The multiplication brings the embedding to a scale comparable with the position signal."),
  T("In the labs, we build the encoding for a small model width, check its first values and add it to embeddings. Because the sine and cosine values are floating point, results are rounded to six decimals.")],
 [("Why is positional information needed?", ["Attention alone ignores word order", "Embeddings are too small", "To save memory", "To encode labels"], 0, "Shuffling the input only shuffles the output."),
  ("How is the positional encoding combined with the embedding?", ["Added", "Concatenated", "Multiplied", "Ignored"], 0, "The width stays d_model."),
  ("What functions does the paper use?", ["Sine and cosine", "ReLU", "Softmax", "Tanh"], 0, "At different frequencies."),
  ("By what are embeddings scaled?", ["Square root of d_model", "d_model", "1/d_model", "Nothing"], 0, "As in the paper.")],
 [("What is d_model in the base model?", "512."), ("Even dimensions use?", "Sine."), ("Odd dimensions use?", "Cosine."), ("Were learned positions tried?", "Yes, with nearly identical results.")],
 [PL("Positional encoding", "Write pos_encoding(pos, d): the list of d values of the sinusoidal encoding at position pos (d even): entry 2i is sin(pos / 10000^(2i/d)) and entry 2i+1 is cos of the same. Round each to 6 decimals. Use import math.",
     "pos_encoding(pos, d)", """
import math
def pos_encoding(pos, d):
    out = []
    for i in range(d // 2):
        angle = pos / (10000 ** (2.0 * i / d))
        out.append(round(math.sin(angle), 6))
        out.append(round(math.cos(angle), 6))
    return out
""", [[0, 4], [1, 4], [5, 6], [10, 8], [3, 2]], "Loop over dimension pairs."),
  PL("Wavelength", "Write wavelength(i, d): the wavelength 2 pi * 10000^(2i/d) of the wave in dimension pair i. Use import math and round to 6 decimals.",
     "wavelength(i, d)", """
import math
def wavelength(i, d):
    return round(2 * math.pi * (10000 ** (2.0 * i / d)), 6)
""", [[0, 512], [1, 4], [127, 256], [0, 2]], "2 pi times the divisor.", approx=1e-9),
  PL("Input to layer one", "Write embed_input(emb, pos): emb is an embedding vector; return emb * sqrt(len(emb)) plus the positional encoding at pos, element by element, each rounded to 6 decimals. Use import math.",
     "embed_input(emb, pos)", """
import math
def embed_input(emb, pos):
    d = len(emb)
    out = []
    for i in range(d // 2):
        angle = pos / (10000 ** (2.0 * i / d))
        out.append(emb[2 * i] * math.sqrt(d) + math.sin(angle))
        out.append(emb[2 * i + 1] * math.sqrt(d) + math.cos(angle))
    return [round(x, 6) for x in out]
""", [[[0.1, 0.2, 0.3, 0.4], 0], [[0.1, 0.2, 0.3, 0.4], 2], [[1.0, 0.0], 3], [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 1]], "Scale, then add."),
  ORDER("Building the input", "Order the steps.", ["Look up the token embedding", "Multiply by the square root of d_model", "Compute the positional encoding", "Add the two vectors", "Feed the sum to the first layer"]),
  MATCH("Terms", "Match each term with its meaning.", [("d_model", "Vector width"), ("PE", "Position signal"), ("sin and cos", "Waves of different frequency"), ("Embedding", "Token to vector"), ("Permutation invariance", "Order is ignored")]),
  FILL("Position", "Attention ignores order, so a {{positional}} encoding built from sine and {{cosine}} waves is added.")]))

CHS.append(CH(
 "Scaled dot-product attention",
 ("Attention", [
  "Query | asks | What am I looking for",
  "Key | answers | What do I contain",
  "Value | carries | The content",
  "Dot product | scores | Query-key match",
  "Scaling | divides by | Square root of d_k",
  "Softmax | turns | Scores into weights",
  "Output | is | Weighted sum of values"]),
 ["Attention takes three sets of vectors: queries Q, keys K and values V. Each query is compared with every key by a dot product. The scores are scaled, turned into weights by a softmax, and used to average the values.",
  "The scaling by the square root of d_k keeps the dot products from growing large with the dimension, which would push the softmax into regions with tiny gradients.",
  "Everything in this chapter is a few lines of arithmetic, and the labs write each of them."],
 [("Query", "A vector that says what a position is looking for."),
  ("Key", "A vector that describes what a position offers."),
  ("Value", "The vector that is actually passed on."),
  ("Softmax", "Turns scores into positive weights that sum to one."),
  ("d_k", "The dimension of keys and queries; 64 in the base model."),
  ("Attention weights", "The softmax output: how much each position contributes.")],
 ["Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V.",
  "Weights in each row are positive and sum to 1.",
  "Without scaling, dot products grow with d_k and the softmax saturates.",
  "Dot-product attention is much faster and more space-efficient than additive attention in practice.",
  "Cost grows with the square of the sequence length.",
  "Each output is a convex combination of the value vectors."],
 [T("Imagine a library. You come with a query, a description of what you want. Each book has a key, a label saying what it is about, and a value, its contents. You compare your query with every key. The better the match, the more of that book's contents you take. The result is a blend of contents weighted by relevance. That is attention."),
  M(r"\mathrm{Attention}(Q,K,V) \;=\; \mathrm{softmax}\!\left(\frac{Q K^{\top}}{\sqrt{d_k}}\right) V"),
  T("Step by step. First, the matrix of scores: the dot product of every query with every key. Second, divide by the square root of d k. Third, apply softmax to each row, so each query gets weights that are positive and sum to one. Fourth, multiply the weights by the values: each output is the weighted average of the value vectors."),
  T("The scaling needs an argument. If the entries of q and k have mean zero and variance one, their dot product has variance d k. For d k of 64, the scores are typically around eight in size. The softmax of numbers that large is nearly a one-hot vector, and its gradient is almost zero. Dividing by the square root of d k brings the variance back to one. The authors observed that without the scaling, dot-product attention performed worse than additive attention for larger d k."),
  T("The paper compares two common attention functions. Additive attention computes compatibility with a small feed-forward network. Dot-product attention is the same except for the scaling factor. Theoretically they are similar in cost, but dot-product attention is much faster and more space-efficient in practice, as it can use highly optimised matrix multiplication."),
  T("The price is quadratic: for a sequence of n positions, the score matrix has n squared entries. Long sequences are expensive. Later work tried to reduce this, which is background knowledge beyond the paper."),
  T("In the labs we write softmax, the scaled scores for one query and the full attention output for lists of vectors.")],
 [("What is softmax of equal scores?", ["Equal weights", "All zero", "One-hot", "Undefined"], 0, "Each weight is 1/n."),
  ("Why divide by sqrt(d_k)?", ["To stop the softmax saturating", "To save memory", "To normalize values", "To add noise"], 0, "Dot products grow with d_k."),
  ("What is the output for one query?", ["A weighted average of the values", "The largest key", "The query itself", "The sum of keys"], 0, "Weights come from the softmax."),
  ("How does cost grow with sequence length n?", ["Like n squared", "Like n", "Like log n", "It is constant"], 0, "n by n scores.")],
 [("What are Q, K, V?", "Queries, keys and values."), ("What do softmax weights sum to?", "One."), ("What is d_k in the base model?", "64."), ("Why is dot-product attention used?", "Fast and space-efficient matrix multiplication.")],
 [PL("Softmax", "Write softmax(xs): the softmax of a list, subtracting the maximum first for stability, each result rounded to 9 decimals. Use import math.",
     "softmax(xs)", """
import math
def softmax(xs):
    m = max(xs)
    es = [math.exp(x - m) for x in xs]
    s = sum(es)
    return [round(e / s, 9) for e in es]
""", [[[0, 0]], [[1, 2, 3]], [[1000, 1000]], [[-1, 0, 1, 2]], [[5]]], "Subtract the max, exponentiate, normalize."),
  PL("Scaled scores", "Write scores(q, keys): for a query q (list) and a list of keys, return the list of dot(q, k) / sqrt(d_k) where d_k is len(q), each rounded to 9 decimals. Use import math.",
     "scores(q, keys)", """
import math
def scores(q, keys):
    d = len(q)
    out = []
    for k in keys:
        s = 0.0
        for a, b in zip(q, k):
            s += a * b
        out.append(round(s / math.sqrt(d), 9))
    return out
""", [[[1, 0], [[1, 0], [0, 1]]], [[1, 1, 1, 1], [[1, 1, 1, 1], [0, 0, 0, 0]]], [[2, 0], [[1, 1], [2, 2], [3, 0]]], [[0.5], [[2.0], [4.0]]]], "Dot product then divide."),
  PL("Attention for one query", "Write attend(q, keys, values): softmax of the scaled scores as weights, then the weighted sum of the value vectors. Return the output vector, each entry rounded to 6 decimals. Use import math.",
     "attend(q, keys, values)", """
import math
def attend(q, keys, values):
    d = len(q)
    sc = []
    for k in keys:
        s = 0.0
        for a, b in zip(q, k):
            s += a * b
        sc.append(s / math.sqrt(d))
    m = max(sc)
    es = [math.exp(x - m) for x in sc]
    t = sum(es)
    w = [e / t for e in es]
    out = [0.0] * len(values[0])
    for wi, v in zip(w, values):
        for j in range(len(v)):
            out[j] += wi * v[j]
    return [round(x, 6) for x in out]
""", [[[1, 0], [[1, 0], [0, 1]], [[10, 0], [0, 10]]], [[0, 0], [[1, 1], [2, 2]], [[1, 2], [3, 4]]], [[3, 0], [[1, 0], [0, 1], [1, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]]], [[1], [[1]], [[7, 8]]]], "Weights times values."),
  PL("Attention matrix", "Write attention_weights(Q, K): the matrix of softmax weights, one row per query, using scaled dot products. Round each entry to 6 decimals. Use import math.",
     "attention_weights(Q, K)", """
import math
def attention_weights(Q, K):
    d = len(Q[0])
    rows = []
    for q in Q:
        sc = []
        for k in K:
            s = 0.0
            for a, b in zip(q, k):
                s += a * b
            sc.append(s / math.sqrt(d))
        m = max(sc)
        es = [math.exp(x - m) for x in sc]
        t = sum(es)
        rows.append([round(e / t, 6) for e in es])
    return rows
""", [[[[1, 0], [0, 1]], [[1, 0], [0, 1]]], [[[0, 0]], [[1, 2], [3, 4], [5, 6]]], [[[2, 2], [1, 0]], [[1, 1], [1, -1]]]], "One softmax per query row."),
  ORDER("Attention", "Order the steps.", ["Dot each query with every key", "Divide by the square root of d_k", "Apply softmax along each row", "Multiply the weights by the values", "Read off the outputs"]),
  MATCH("Pieces", "Match each piece with its job.", [("Query", "What I look for"), ("Key", "What I offer"), ("Value", "What is passed on"), ("Softmax", "Weights that sum to one"), ("sqrt(d_k)", "Keeps scores in range")]),
  FILL("Formula", "Attention is softmax of Q K transposed over the square root of {{d_k|dk}}, times {{V}}.")]))

CHS.append(CH(
 "Multi-head attention",
 ("Heads", [
  "Head | runs | Attention in a subspace",
  "Projection | maps | d_model to d_k",
  "8 heads | each use | 64 dimensions",
  "Concatenation | joins | Head outputs",
  "Output projection | mixes | Heads",
  "Heads | attend to | Different patterns",
  "Total cost | similar to | One full-width head"]),
 ["Instead of one attention, the paper runs several in parallel, called heads. Each head applies its own learned projections to the queries, keys and values, shrinking them to a smaller size, and runs attention there.",
  "In the base model there are 8 heads, each with d_k = d_v = 64, so the total width is 8 times 64, or 512. The outputs of the heads are concatenated and mixed by a last projection.",
  "The reason is that a single attention averages over many things at once. Several heads can look at different relations at the same time."],
 [("Head", "One attention operation with its own projection matrices."),
  ("Projection", "Multiplying by a learned matrix to change dimension."),
  ("Concatenate", "Join vectors end to end."),
  ("W^O", "The final output projection after concatenation."),
  ("h", "The number of heads; 8 in the base model."),
  ("Subspace", "A lower-dimensional view of the vector.")],
 ["head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V).",
  "MultiHead = Concat(head_1 ... head_h) W^O.",
  "Base model: h = 8, d_k = d_v = d_model / h = 64.",
  "Because each head is smaller, the cost is similar to one full-width head.",
  "Heads can specialise; some look like they track syntax, per the paper's visualisations.",
  "Projection matrices are learned, one set per head."],
 [T("A single attention step produces one weighted average per position. That is limiting: the position may need to look at one word for its subject, another for the verb, and another for a nearby modifier. With a single average, those signals blur together."),
  T("The paper's remedy is multi-head attention. Instead of attending once with d model dimensional keys, values and queries, it projects them h times with different learned linear maps to the lower dimension d k, runs attention on each, concatenates the h results and projects once more."),
  M(r"\mathrm{MultiHead}(Q,K,V) = \mathrm{Concat}(\mathrm{head}_1,\dots,\mathrm{head}_h)\,W^{O}, \quad \mathrm{head}_i = \mathrm{Attention}(QW_i^{Q},\,KW_i^{K},\,VW_i^{V})"),
  T("With 8 heads of dimension 64, the concatenation has dimension 512, equal to d model. The cost is similar to a single head of full dimension, because each head works in a smaller space. The paper notes that averaging in a single head inhibits this kind of joint attention to different subspaces."),
  T("The paper's figures show attention heads that appear to do different jobs: some follow long-distance dependencies, such as a verb and its object far away. Others seem to be related to the sentence structure. This should be taken as an observation about the examples shown, not as a guarantee."),
  T("Transformers use multi-head attention in three places. In encoder self-attention, queries, keys and values all come from the previous encoder layer. In decoder self-attention they come from the previous decoder layer, with a mask. In encoder-decoder attention, queries come from the decoder and keys and values from the encoder output."),
  T("The labs split a vector into heads, merge heads again and run a tiny two-head attention with fixed projections.")],
 [("How many heads does the base model have?", ["8", "1", "64", "512"], 0, "h = 8."),
  ("What is d_k for each head in the base model?", ["64", "512", "8", "1"], 0, "512 divided by 8."),
  ("What happens to the head outputs?", ["Concatenated and projected", "Averaged only", "Summed with the input only", "Thrown away"], 0, "W^O mixes them."),
  ("Where do queries come from in cross-attention?", ["The decoder", "The encoder", "The embeddings only", "The loss"], 0, "Keys and values come from the encoder.")],
 [("Why several heads?", "To attend to different things jointly."), ("Is the cost much higher?", "No, each head is smaller."), ("How many uses of multi-head attention?", "Three: encoder self, decoder self, cross."), ("What mixes the heads?", "The output projection W^O.")],
 [PL("Split into heads", "Write split_heads(x, h): split the vector x into h equal consecutive parts and return the list of parts.",
     "split_heads(x, h)", """
def split_heads(x, h):
    n = len(x) // h
    return [x[i * n:(i + 1) * n] for i in range(h)]
""", [[[1, 2, 3, 4], 2], [[1, 2, 3, 4, 5, 6], 3], [[1, 2], 1], [[1, 2, 3, 4], 4]], "Slice into equal pieces."),
  PL("Merge heads", "Write merge_heads(parts): concatenate a list of lists into one list.",
     "merge_heads(parts)", """
def merge_heads(parts):
    out = []
    for p in parts:
        out = out + list(p)
    return out
""", [[[[1, 2], [3, 4]]], [[[1], [2], [3]]], [[[5, 6, 7]]]], "Join end to end."),
  PL("Matrix-vector product", "Write matvec(W, x): W is a list of rows; return the list of dot products of each row with x, rounded to 6 decimals.",
     "matvec(W, x)", """
def matvec(W, x):
    out = []
    for row in W:
        s = 0.0
        for a, b in zip(row, x):
            s += a * b
        out.append(round(s, 6))
    return out
""", [[[[1, 0], [0, 1]], [3, 4]], [[[1, 1], [1, -1]], [2, 5]], [[[2, 0, 1]], [1, 1, 1]], [[[0.5, 0.5]], [1.0, 3.0]]], "Row by row."),
  PL("Two-head attention", "Write two_head(q, keys, values): q, each key and each value are lists of even length d. Split every vector into two halves; for each half run attention (scaled by the square root of the half length, softmax, weighted sum of that half of the values) and concatenate the two outputs. Round to 6 decimals. Use import math.",
     "two_head(q, keys, values)", """
import math
def two_head(q, keys, values):
    d = len(q)
    hd = d // 2
    out = []
    for h in range(2):
        lo = h * hd
        hi = lo + hd
        sc = []
        for k in keys:
            s = 0.0
            for a, b in zip(q[lo:hi], k[lo:hi]):
                s += a * b
            sc.append(s / math.sqrt(hd))
        m = max(sc)
        es = [math.exp(x - m) for x in sc]
        t = sum(es)
        w = [e / t for e in es]
        o = [0.0] * hd
        for wi, v in zip(w, values):
            for j in range(hd):
                o[j] += wi * v[lo + j]
        out = out + o
    return [round(x, 6) for x in out]
""", [[[1, 0, 0, 1], [[1, 0, 0, 0], [0, 1, 0, 1]], [[1, 2, 3, 4], [5, 6, 7, 8]]], [[0, 0, 0, 0], [[1, 1, 1, 1], [2, 2, 2, 2]], [[1, 0, 1, 0], [0, 1, 0, 1]]], [[2, 2], [[1, 1], [1, -1]], [[1, 2], [3, 4]]]], "Each half has its own softmax."),
  ORDER("Multi-head", "Order the steps.", ["Project Q, K, V for each head", "Run attention in every head", "Concatenate the head outputs", "Apply the output projection", "Pass the result to the next sublayer"]),
  MATCH("Uses", "Match each attention with its inputs.", [("Encoder self-attention", "Q, K, V from the encoder layer below"), ("Decoder self-attention", "Q, K, V from the decoder below, masked"), ("Cross-attention", "Q from decoder, K and V from encoder"), ("Head", "One subspace attention"), ("W^O", "Mixes the heads")]),
  FILL("Heads", "The base model has {{8}} heads of dimension {{64}}; their outputs are concatenated.")]))

CHS.append(CH(
 "Masks: padding and causal",
 ("Masking", [
  "Padding mask | hides | Pad tokens",
  "Causal mask | hides | Future positions",
  "Masked score | set to | Minus infinity",
  "Softmax | gives | Zero weight to masked",
  "Decoder | needs | Causal mask",
  "Training | uses | Teacher forcing",
  "Parallel training | enabled by | Masks"]),
 ["Some positions must not be looked at. Padding tokens added to make a batch rectangular carry no meaning. In the decoder, the word at position t may not look at positions after t, otherwise it could copy the answer.",
  "A mask is applied to the scores before the softmax. Forbidden entries are set to a very negative number, minus infinity in the paper's description, so that their weights become zero.",
  "The causal mask is what lets the decoder train on a whole target sentence in one pass while still behaving as a left-to-right generator."],
 [("Padding", "Filler tokens added to make sequences the same length."),
  ("Causal mask", "A triangular mask that blocks attention to later positions."),
  ("Mask", "A pattern that decides which scores are allowed."),
  ("Teacher forcing", "Feeding the true previous tokens during training."),
  ("Autoregressive", "Generating one token at a time from earlier ones."),
  ("Minus infinity", "A value whose exponential is zero.")],
 ["Masked scores are set to minus infinity before the softmax, giving zero weight.",
  "The decoder's self-attention uses a causal mask: position t sees positions 0 to t.",
  "The decoder's outputs are also shifted right by one position.",
  "Padding masks keep real tokens from attending to pad tokens.",
  "Training with teacher forcing and a mask computes all positions in parallel.",
  "At generation time there is no future to mask, so tokens are produced one by one."],
 [T("When sentences are batched, short ones are padded with a special token to the length of the longest. The padding carries no information. If a real word attended to a pad, it would mix in a meaningless vector. So we mask: the scores for pad positions are replaced by a huge negative number before the softmax. The exponential of that is zero, so these positions get no weight."),
  T("The decoder has a second, deeper reason. It generates the target one word at a time, each word depending on the earlier ones. During training the full correct target is available, which tempts a shortcut: let each position attend to the position after it and just copy the answer. That must be prevented."),
  M(r"\mathrm{mask}_{ij} = \begin{cases} 0 & j \le i \\ -\infty & j > i \end{cases}, \qquad \mathrm{weights} = \mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}} + \mathrm{mask}\right)"),
  T("This is the causal mask: row i, the query position, may use columns up to and including i. Together with shifting the target one position to the right, it ensures that the prediction for position i depends only on the known outputs at positions before i. The paper states this in its description of the decoder."),
  T("The gain is parallelism. With a recurrent decoder, training goes step by step. With the causal mask, all positions are computed at once in one matrix operation, while each still sees only its past. This feeding of the true previous tokens is called teacher forcing."),
  T("At test time the situation changes. The future words do not exist yet, so the decoder runs once per generated token, appending each prediction to its input. The mask has the same shape of effect, but nothing remains to hide. Chapter 10 covers this decoding loop."),
  T("In the labs we build the causal mask, apply it to a score matrix, and compute weights that respect both masks.")],
 [("What does a causal mask prevent?", ["Looking at later positions", "Looking at earlier positions", "Embedding", "Dropout"], 0, "Position i sees only up to i."),
  ("Why mask padding?", ["Pad tokens carry no meaning", "To save memory", "To shorten sentences", "To add noise"], 0, "They should get zero weight."),
  ("What are masked scores set to?", ["A very negative number", "Zero", "One", "Their square"], 0, "Exponential then gives zero."),
  ("What does the mask enable in training?", ["Parallel computation over positions", "Larger vocabulary", "Smaller models", "Free labels"], 0, "No step-by-step loop.")],
 [("Which positions can position 2 see in the decoder?", "0, 1 and 2."), ("What is teacher forcing?", "Feeding true previous tokens in training."), ("How is the target offset?", "Shifted right by one position."), ("Is there a mask at generation time?", "Nothing is left to hide.")],
 [PL("Causal mask", "Write causal_mask(n): an n by n matrix with 1 where j <= i (allowed) and 0 elsewhere.",
     "causal_mask(n)", """
def causal_mask(n):
    return [[1 if j <= i else 0 for j in range(n)] for i in range(n)]
""", [[1], [3], [4], [0]], "Lower triangle of ones."),
  PL("Apply a mask", "Write apply_mask(scores, mask): replace score entries where the mask is 0 by -1e9, leaving others unchanged.",
     "apply_mask(scores, mask)", """
def apply_mask(scores, mask):
    out = []
    for srow, mrow in zip(scores, mask):
        out.append([s if m == 1 else -1e9 for s, m in zip(srow, mrow)])
    return out
""", [[[[1, 2], [3, 4]], [[1, 0], [1, 1]]], [[[5]], [[1]]], [[[1, 2, 3]], [[0, 1, 0]]]], "Keep or replace."),
  PL("Masked attention weights", "Write masked_weights(scores, mask): softmax of each row after masking, each result rounded to 6 decimals. Use import math.",
     "masked_weights(scores, mask)", """
import math
def masked_weights(scores, mask):
    out = []
    for srow, mrow in zip(scores, mask):
        r = [s if m == 1 else -1e9 for s, m in zip(srow, mrow)]
        mx = max(r)
        es = [math.exp(x - mx) for x in r]
        t = sum(es)
        out.append([round(e / t, 6) for e in es])
    return out
""", [[[[1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 0, 0], [1, 1, 0], [1, 1, 1]]], [[[0, 0]], [[1, 1]]], [[[2, 2, 2]], [[1, 0, 1]]]], "Masked entries get zero weight."),
  PL("Padding mask", "Write padding_mask(tokens, pad): a list with 1 for real tokens and 0 where the token equals pad.",
     "padding_mask(tokens, pad)", """
def padding_mask(tokens, pad):
    return [0 if t == pad else 1 for t in tokens]
""", [[[5, 6, 0, 0], 0], [[1, 2, 3], 0], [[0, 0], 0], [[7, 9, 9], 9]], "Compare with the pad id."),
  ORDER("Masked decoding step", "Order the steps for training.", ["Shift the target right by one", "Compute scores for all positions at once", "Apply the causal mask", "Softmax each row", "Predict every next token in parallel"]),
  MATCH("Masks", "Match each mask with its purpose.", [("Padding mask", "Ignore filler tokens"), ("Causal mask", "No peeking at the future"), ("Minus infinity", "Zero weight after softmax"), ("Teacher forcing", "Feed true previous tokens"), ("Shift right", "Align inputs and targets")]),
  FILL("Masks", "The decoder uses a {{causal}} mask so position i sees only positions up to {{i}}.")]))

CHS.append(CH(
 "Feed-forward layers, residuals and layer normalization",
 ("Sublayers", [
  "Feed-forward | applies | Two linear layers",
  "ReLU | sits between | The two layers",
  "d_ff | is | 2048",
  "Residual connection | adds | Input to output",
  "Layer norm | normalizes | Each position",
  "Dropout | regularizes | Sublayer outputs",
  "Sublayer output | is | LayerNorm(x + Sublayer(x))"]),
 ["Each layer has attention and a position-wise feed-forward network. Around each sublayer sits a residual connection and layer normalization: output = LayerNorm(x + Sublayer(x)).",
  "The feed-forward network is two linear maps with a ReLU between them, applied to each position separately: max(0, xW1 + b1)W2 + b2. In the base model the inner width d_ff is 2048.",
  "Residual connections help gradients flow through deep stacks. Layer normalization keeps activations in a stable range."],
 [("Feed-forward network", "Two linear maps with a ReLU; applied to each position independently."),
  ("ReLU", "max(0, x)."),
  ("Residual connection", "Adding a sublayer's input to its output."),
  ("Layer normalization", "Rescaling each vector to zero mean and unit variance, then a learned scale and shift."),
  ("d_ff", "The inner width of the feed-forward network; 2048 in the base model."),
  ("Dropout", "Randomly zeroing activations during training; rate 0.1 in the base model.")],
 ["FFN(x) = max(0, x W1 + b1) W2 + b2, d_model 512 to d_ff 2048 and back.",
  "Sublayer wrapper: LayerNorm(x + Dropout(Sublayer(x))).",
  "All sublayers and embeddings output vectors of size d_model so residuals can add.",
  "Layer norm statistics are computed over the features of one position.",
  "The big model uses d_model 1024, d_ff 4096, 16 heads.",
  "Parameter counts: about 65 million for the base model and 213 million for the big model."],
 [T("Attention mixes information between positions. The feed-forward network then processes each position by itself. The paper describes it as two linear transformations with a ReLU between. Think of it as a small two-layer perceptron applied identically at every position, with the same weights for all positions but different weights in each layer."),
  M(r"\mathrm{FFN}(x) = \max(0,\; xW_1 + b_1)\,W_2 + b_2"),
  T("In the base model d model is 512 and the inner dimension d ff is 2048, so the first map expands each vector fourfold and the second shrinks it back. Much of the parameter count of the Transformer lives in these layers."),
  T("Depth causes trouble for training. The paper wraps every sublayer, attention or feed-forward, in a residual connection followed by layer normalization. The input is added to the sublayer's output, so the layer only has to learn a correction. Gradients can travel along the shortcut. For the addition to be possible, all sublayers and embeddings produce outputs of the same dimension d model."),
  M(r"\mathrm{output} = \mathrm{LayerNorm}\bigl(x + \mathrm{Sublayer}(x)\bigr), \qquad \mathrm{LayerNorm}(v) = g \odot \frac{v - \mu}{\sqrt{\sigma^2 + \epsilon}} + b"),
  T("Layer normalization works on one position at a time. It computes the mean and variance across the features of that vector, subtracts the mean, divides by the standard deviation and applies a learned scale g and shift b. Unlike batch normalization it does not depend on the other examples in a batch."),
  T("The paper also applies dropout with rate 0.1 to the output of each sublayer before it is added and normalized, and to the sums of embeddings and positional encodings. Later work often moves the normalization before the sublayer, a variant known as pre-norm. This is background knowledge.")],
 [("What is the formula of a wrapped sublayer?", ["LayerNorm(x + Sublayer(x))", "Sublayer(x) only", "x * Sublayer(x)", "ReLU(x)"], 0, "Residual then normalize."),
  ("What is d_ff in the base model?", ["2048", "512", "64", "8"], 0, "Four times d_model."),
  ("Over what does layer norm compute statistics?", ["The features of one position", "The whole batch", "The vocabulary", "The positions of a sentence"], 0, "No dependence on the batch."),
  ("Why must all sublayers output d_model?", ["So residual additions work", "To save memory", "For dropout", "For the vocabulary"], 0, "x + Sublayer(x).")],
 [("What is in the FFN?", "Linear, ReLU, linear."), ("Is the FFN shared across positions?", "Yes, same weights at each position."), ("What dropout rate?", "0.1 in the base model."), ("Where do many parameters live?", "In the feed-forward layers.")],
 [PL("Feed-forward network", "Write ffn(x, W1, b1, W2, b2): W1 is a list of rows (d_ff rows, each of length len(x)), W2 has len(x) rows each of length d_ff. Return max(0, W1 x + b1) then W2 times that plus b2, each rounded to 6 decimals.",
     "ffn(x, W1, b1, W2, b2)", """
def ffn(x, W1, b1, W2, b2):
    h = []
    for row, b in zip(W1, b1):
        s = b
        for a, c in zip(row, x):
            s += a * c
        h.append(s if s > 0 else 0.0)
    out = []
    for row, b in zip(W2, b2):
        s = b
        for a, c in zip(row, h):
            s += a * c
        out.append(round(s, 6))
    return out
""", [[[1, 2], [[1, 0], [0, 1], [1, 1]], [0, 0, -2], [[1, 0, 0], [0, 1, 1]], [0, 0]], [[1], [[1], [-1]], [0, 0], [[1, 1]], [0.5]], [[0, 0], [[1, 1]], [1], [[2], [3]], [0, 0]]], "Expand, apply ReLU, project back."),
  PL("Layer normalization", "Write layer_norm(v, g, b, eps): subtract the mean, divide by sqrt(variance + eps) (population variance), multiply by g[i] and add b[i]. Round to 6 decimals. Use import math.",
     "layer_norm(v, g, b, eps)", """
import math
def layer_norm(v, g, b, eps):
    n = len(v)
    mu = sum(v) / n
    var = sum((x - mu) ** 2 for x in v) / n
    s = math.sqrt(var + eps)
    return [round(g[i] * (v[i] - mu) / s + b[i], 6) for i in range(n)]
""", [[[1, 2, 3], [1, 1, 1], [0, 0, 0], 1e-5], [[2, 2], [1, 1], [0, 0], 1e-5], [[0, 4], [2, 2], [1, 1], 0.0001], [[1, 2, 3, 4], [1, 1, 1, 1], [0, 0, 0, 0], 0.00001]], "Mean, variance, then scale and shift."),
  PL("Residual sublayer", "Write residual_ln(x, sub): given x and the sublayer output sub (same length), return LayerNorm(x + sub) with scale 1, shift 0 and eps 1e-5, rounded to 6 decimals. Use import math.",
     "residual_ln(x, sub)", """
import math
def residual_ln(x, sub):
    y = [a + b for a, b in zip(x, sub)]
    n = len(y)
    mu = sum(y) / n
    var = sum((t - mu) ** 2 for t in y) / n
    s = math.sqrt(var + 1e-5)
    return [round((t - mu) / s, 6) for t in y]
""", [[[1, 2, 3], [0, 0, 0]], [[1, 0], [0, 1]], [[5, 5, 5, 5], [1, 2, 3, 4]], [[0.5, -0.5], [0.25, 0.25]]], "Add first, then normalize."),
  PL("Parameter count of an FFN", "Write ffn_params(d_model, d_ff): the number of weights and biases in W1, b1, W2, b2.",
     "ffn_params(d_model, d_ff)", """
def ffn_params(d_model, d_ff):
    return d_model * d_ff + d_ff + d_ff * d_model + d_model
""", [[512, 2048], [1024, 4096], [4, 8], [2, 3]], "Count each matrix and bias."),
  ORDER("One sublayer", "Order the steps.", ["Compute the sublayer output", "Apply dropout", "Add the input", "Layer-normalize", "Pass to the next sublayer"]),
  MATCH("Pieces", "Match each piece with its job.", [("Residual", "Lets gradients bypass the sublayer"), ("Layer norm", "Stabilises activations"), ("ReLU", "max(0, x)"), ("d_ff", "Inner width, 2048"), ("Dropout", "Regularization")]),
  FILL("Layer", "Each sublayer is wrapped as LayerNorm(x + {{Sublayer|sublayer}}(x)). The inner width d_ff is {{2048}}.")]))

CHS.append(CH(
 "The encoder stack",
 ("Encoder", [
  "Encoder layer | has | Self-attention and FFN",
  "Encoder | stacks | N identical layers",
  "Self-attention | is | Bidirectional",
  "Memory | is | Final encoder output",
  "Padding mask | hides | Source pads",
  "Layers | do not share | Weights",
  "Output | has | Same shape as input"]),
 ["The encoder is a stack of N = 6 identical layers. Each layer applies multi-head self-attention, then a feed-forward network, each wrapped in a residual connection and layer norm.",
  "Encoder self-attention is bidirectional: every source position can look at every other, left and right. There is no causal mask, only a padding mask.",
  "The output of the last layer is the memory, one vector per source position, that the decoder will read."],
 [("Encoder layer", "Self-attention sublayer plus feed-forward sublayer."),
  ("Memory", "The encoder's final output, read by the decoder's cross-attention."),
  ("Bidirectional", "Each position sees both earlier and later positions."),
  ("Stack", "Layers applied one after another."),
  ("N", "The number of layers; 6 in the base model."),
  ("Source sequence", "The input sentence to be translated.")],
 ["Encoder layer: x1 = LN(x + SelfAttn(x)); x2 = LN(x1 + FFN(x1)).",
  "Six layers, each with its own parameters.",
  "Input and output have shape (source length, d_model).",
  "Self-attention uses a padding mask but no causal mask.",
  "BERT (background knowledge) is built from encoder-style layers.",
  "The encoder runs once per sentence, not once per output word."],
 [T("The encoder turns the source sentence into a set of context-rich vectors. Its input is the sum of embeddings and positional encodings, one vector of size d model for each source word."),
  T("Each of the six layers is the same in shape. The first sublayer is multi-head self-attention, in which queries, keys and values all come from the layer's own input. Every position looks at every position, to the left and right. The second sublayer is the position-wise feed-forward network. Each is wrapped by a residual connection and layer normalization."),
  M(r"x' = \mathrm{LN}\bigl(x + \mathrm{SelfAttn}(x)\bigr), \qquad x'' = \mathrm{LN}\bigl(x' + \mathrm{FFN}(x')\bigr)"),
  T("Stacking six layers lets information travel. After one layer, a word has mixed in information from its neighbours. After several, it has absorbed context from across the sentence and combined it in non-linear ways. Because all layers keep the same shape, the output has one d model vector per source word."),
  T("That output is the memory. It is computed once, and then the decoder looks at it again and again while it generates, one word at a time. The memory does not depend on what the decoder has written."),
  T("Many later models use the encoder alone. BERT, introduced in 2018, is a stack of encoder-style layers trained to fill in masked words. This is background knowledge beyond the paper."),
  T("In the labs we build a tiny encoder layer with fixed weights from the pieces of earlier chapters: self-attention with identity projections, a residual layer-normalization and a stack.")],
 [("Is encoder self-attention causal?", ["No, it is bidirectional", "Yes", "Only in the last layer", "Only at test time"], 0, "Every position sees all."),
  ("How many layers does the base encoder have?", ["6", "2", "12", "1"], 0, "N = 6."),
  ("What is the memory?", ["The encoder's final output", "The decoder's input", "The loss", "The embedding table"], 0, "Read by cross-attention."),
  ("How often does the encoder run per sentence?", ["Once", "Once per output word", "Twice", "Never"], 0, "The decoder reuses its output.")],
 [("What are the two sublayers?", "Self-attention and feed-forward."), ("Do layers share weights?", "No."), ("What shape is the output?", "One d_model vector per source position."), ("Which later model uses only encoders?", "BERT (background).")],
 [PL("Self-attention with identity projections", "Write self_attend(X): X is a list of vectors; for each position use X as queries, keys and values (scaled dot product, softmax, weighted sum), returning the list of output vectors rounded to 6 decimals. Use import math.",
     "self_attend(X)", """
import math
def self_attend(X):
    d = len(X[0])
    out = []
    for q in X:
        sc = []
        for k in X:
            s = 0.0
            for a, b in zip(q, k):
                s += a * b
            sc.append(s / math.sqrt(d))
        m = max(sc)
        es = [math.exp(t - m) for t in sc]
        tot = sum(es)
        o = [0.0] * d
        for e, v in zip(es, X):
            for j in range(d):
                o[j] += e / tot * v[j]
        out.append([round(t, 6) for t in o])
    return out
""", [[[[1, 0], [0, 1]]], [[[1, 1], [1, 1], [1, 1]]], [[[2, 0], [0, 2], [1, 1]]], [[[1, 0, 0]]]], "Every position queries all positions."),
  PL("Add and normalize all positions", "Write add_norm(X, Y): for each position add the vectors X[i] and Y[i], then layer-normalize with scale 1, shift 0 and eps 1e-5, rounded to 6 decimals. Use import math.",
     "add_norm(X, Y)", """
import math
def add_norm(X, Y):
    out = []
    for x, y in zip(X, Y):
        z = [a + b for a, b in zip(x, y)]
        n = len(z)
        mu = sum(z) / n
        var = sum((t - mu) ** 2 for t in z) / n
        s = math.sqrt(var + 1e-5)
        out.append([round((t - mu) / s, 6) for t in z])
    return out
""", [[[[1, 2], [3, 4]], [[0, 0], [0, 0]]], [[[1, 0, 0]], [[0, 1, 0]]], [[[5, 5, 5]], [[1, 2, 3]]]], "Residual add, then layer norm per position."),
  PL("Encoder layer (no FFN)", "Write enc_layer(X): return the add-and-normalize of X and its self-attention output (identity projections, scale 1, shift 0, eps 1e-5), rounded to 6 decimals. Use import math.",
     "enc_layer(X)", """
import math
def enc_layer(X):
    d = len(X[0])
    att = []
    for q in X:
        sc = []
        for k in X:
            s = 0.0
            for a, b in zip(q, k):
                s += a * b
            sc.append(s / math.sqrt(d))
        m = max(sc)
        es = [math.exp(t - m) for t in sc]
        tot = sum(es)
        o = [0.0] * d
        for e, v in zip(es, X):
            for j in range(d):
                o[j] += e / tot * v[j]
        att.append(o)
    out = []
    for x, y in zip(X, att):
        z = [a + b for a, b in zip(x, y)]
        n = len(z)
        mu = sum(z) / n
        var = sum((t - mu) ** 2 for t in z) / n
        s = math.sqrt(var + 1e-5)
        out.append([round((t - mu) / s, 6) for t in z])
    return out
""", [[[[1, 0], [0, 1]]], [[[1, 2, 3], [3, 2, 1]]], [[[2, 0], [0, 2], [1, 1]]]], "Attention, residual, normalize."),
  PL("Count positions per layer", "An encoder has n_layers layers; each layer has one attention (4 projection matrices of d_model by d_model, ignoring biases) and one FFN (2 matrices d_model by d_ff, ignoring biases). Write encoder_weights(n_layers, d_model, d_ff): the total number of weights.",
     "encoder_weights(n_layers, d_model, d_ff)", """
def encoder_weights(n_layers, d_model, d_ff):
    per = 4 * d_model * d_model + 2 * d_model * d_ff
    return n_layers * per
""", [[6, 512, 2048], [1, 4, 8], [2, 8, 16], [12, 768, 3072]], "Per-layer weights times layers."),
  ORDER("Encoder layer", "Order the steps in one encoder layer.", ["Self-attention over all source positions", "Add the input and layer-normalize", "Position-wise feed-forward network", "Add and layer-normalize again", "Hand the result to the next layer"]),
  MATCH("Encoder", "Match each item with its description.", [("Self-attention", "Positions look at each other"), ("Memory", "Final encoder output"), ("N = 6", "Number of layers"), ("Padding mask", "Hide source pads"), ("BERT", "Encoder-only model (background)")]),
  FILL("Encoder", "The encoder is a stack of {{6|six}} layers and its final output is called the {{memory}}.")]))

CHS.append(CH(
 "The decoder stack",
 ("Decoder", [
  "Decoder layer | has | Three sublayers",
  "Masked self-attention | sees | Earlier outputs",
  "Cross-attention | reads | Encoder memory",
  "Feed-forward | follows | Cross-attention",
  "Final linear | maps to | Vocabulary logits",
  "Softmax | gives | Next-token probabilities",
  "Embedding table | may be | Shared with output"]),
 ["The decoder has the same kind of layers as the encoder with one extra sublayer. In order: masked self-attention over the target so far, cross-attention to the encoder memory, then the feed-forward network. Each is wrapped by a residual connection and layer norm.",
  "In cross-attention the queries come from the decoder and the keys and values come from the encoder's output. That is how the decoder reads the source sentence.",
  "After the last layer, a linear map and a softmax turn each position's vector into probabilities over the vocabulary, for the next token."],
 [("Masked self-attention", "Self-attention with a causal mask, so a position sees only earlier ones."),
  ("Cross-attention", "Attention whose queries come from the decoder and whose keys and values come from the encoder."),
  ("Logits", "Raw scores over the vocabulary before the softmax."),
  ("Vocabulary", "The set of tokens the model can produce."),
  ("Weight tying", "Sharing the embedding matrix with the output projection."),
  ("Shifted right", "The decoder input is the target moved one step later.")],
 ["Decoder layer: masked self-attention, cross-attention, feed-forward; each with residual and layer norm.",
  "Cross-attention: Q from the decoder, K and V from the encoder memory.",
  "Output: softmax(linear(decoder output)) over the vocabulary.",
  "The paper shares the weights of the two embedding layers and the pre-softmax linear map.",
  "The decoder input is the target sequence shifted right, starting with a start symbol.",
  "Six decoder layers in the base model."],
 [T("The decoder writes the target sentence. It receives the target tokens produced so far, shifted right so that the first input is a start marker. These are embedded and given positional encodings, as in the encoder."),
  T("Each decoder layer has three sublayers. First comes masked self-attention, in which target positions look at earlier target positions and themselves, never later ones. Second, cross-attention: the queries come from the decoder's own state, while the keys and values come from the encoder memory. This is the step where the decoder consults the source sentence. Third is the usual feed-forward network."),
  M(r"y_1 = \mathrm{LN}(y + \mathrm{MaskedSelfAttn}(y)), \quad y_2 = \mathrm{LN}(y_1 + \mathrm{CrossAttn}(y_1, m, m)), \quad y_3 = \mathrm{LN}(y_2 + \mathrm{FFN}(y_2))"),
  T("In cross-attention every decoder position can look at every source position, as in the attention mechanisms of earlier recurrent translation models. The Transformer keeps this idea and applies it layer after layer."),
  T("At the top, a linear layer maps each decoder vector to one score per vocabulary token, and a softmax turns the scores into a probability distribution for the next token. The paper shares the weight matrix between the two embedding layers and this pre-softmax linear transformation, which saves parameters."),
  T("The paper used a shared vocabulary of about 37,000 word pieces for English to German, built with byte-pair encoding. For English to French it used a 32,000 word-piece vocabulary. This is reported in the training section. Word pieces let the model handle rare words by splitting them into familiar parts."),
  T("In the labs we compute the output distribution from a decoder vector, a cross-attention step and the greedy next token.")],
 [("What do cross-attention keys and values come from?", ["The encoder memory", "The decoder input", "The loss", "The vocabulary"], 0, "Queries come from the decoder."),
  ("What does the causal mask prevent in the decoder?", ["Seeing later target tokens", "Seeing the source", "Using the FFN", "Dropout"], 0, "Only earlier positions."),
  ("How many sublayers does a decoder layer have?", ["3", "2", "1", "4"], 0, "Masked self, cross, FFN."),
  ("What does the final softmax give?", ["Probabilities over the vocabulary", "Attention weights", "Positions", "Gradients"], 0, "For the next token.")],
 [("Why shift the target right?", "So position i predicts token i from tokens before it."), ("What is weight tying?", "Sharing the embedding and output matrices."), ("What is BPE?", "A word-piece vocabulary method."), ("Which sublayer reads the source?", "Cross-attention.")],
 [PL("Output distribution", "Write next_token_probs(h, W): W is a list of rows, one per vocabulary token; return the softmax of the dot products of h with each row, rounded to 6 decimals. Use import math.",
     "next_token_probs(h, W)", """
import math
def next_token_probs(h, W):
    sc = []
    for row in W:
        s = 0.0
        for a, b in zip(row, h):
            s += a * b
        sc.append(s)
    m = max(sc)
    es = [math.exp(x - m) for x in sc]
    t = sum(es)
    return [round(e / t, 6) for e in es]
""", [[[1, 0], [[1, 0], [0, 1], [1, 1]]], [[0, 0], [[1, 2], [3, 4]]], [[2], [[1], [-1], [0]]], [[1, 1], [[1, 1], [1, 1]]]], "Logits then softmax."),
  PL("Cross-attention", "Write cross_attend(q, memory): the queries q is one decoder vector; the keys and values are both the list memory. Scaled dot product, softmax, weighted sum of memory vectors, rounded to 6 decimals. Use import math.",
     "cross_attend(q, memory)", """
import math
def cross_attend(q, memory):
    d = len(q)
    sc = []
    for k in memory:
        s = 0.0
        for a, b in zip(q, k):
            s += a * b
        sc.append(s / math.sqrt(d))
    m = max(sc)
    es = [math.exp(x - m) for x in sc]
    t = sum(es)
    o = [0.0] * d
    for e, v in zip(es, memory):
        for j in range(d):
            o[j] += e / t * v[j]
    return [round(x, 6) for x in o]
""", [[[1, 0], [[1, 0], [0, 1]]], [[0, 0], [[2, 4], [4, 2]]], [[3, 3], [[1, 1], [-1, -1], [0, 0]]], [[1], [[5]]]], "Same as attend, but the keys and values are the memory."),
  PL("Greedy next token", "Write greedy_next(probs): the index of the largest probability (ties to the lowest index).",
     "greedy_next(probs)", """
def greedy_next(probs):
    best = 0
    for i in range(1, len(probs)):
        if probs[i] > probs[best]:
            best = i
    return best
""", [[[0.1, 0.7, 0.2]], [[0.5, 0.5]], [[1.0]], [[0.2, 0.3, 0.5, 0.0]]], "Arg-max."),
  PL("Shift right", "Write shift_right(tokens, start): the list tokens moved one place to the right with the start symbol first and the last token dropped.",
     "shift_right(tokens, start)", """
def shift_right(tokens, start):
    return [start] + list(tokens[:-1])
""", [[[5, 6, 7], 1], [[9], 1], [[2, 3], 0]], "Prepend the start symbol."),
  ORDER("Decoder layer", "Order the sublayers.", ["Masked self-attention over the target so far", "Add and layer-normalize", "Cross-attention to the encoder memory", "Add and layer-normalize again", "Feed-forward, add and normalize"]),
  MATCH("Decoder", "Match each item with its role.", [("Masked self-attention", "Looks at earlier outputs"), ("Cross-attention", "Reads the encoder"), ("Linear plus softmax", "Next-token probabilities"), ("Shifted right", "Decoder input"), ("Weight tying", "Share embeddings and output matrix")]),
  FILL("Decoder", "In cross-attention the queries come from the {{decoder}} and the keys and values from the {{encoder}}.")]))

CHS.append(CH(
 "Training: loss, optimizer and schedule",
 ("Training", [
  "Cross-entropy | trains | Next-token prediction",
  "Label smoothing | softens | One-hot targets",
  "Adam | optimizes | Parameters",
  "Warmup | raises | Learning rate first",
  "Inverse square root | decays | Learning rate",
  "Dropout | set to | 0.1",
  "Base model | trained | 100,000 steps"]),
 ["Training minimizes cross-entropy between the model's next-token probabilities and the true tokens. The paper adds label smoothing of 0.1, which makes targets slightly less certain and improves BLEU even though perplexity gets worse.",
  "The optimizer is Adam with beta1 0.9, beta2 0.98 and epsilon 1e-9. The learning rate rises linearly for 4000 warmup steps then falls with the inverse square root of the step number.",
  "The base model trained for 100,000 steps, about 12 hours on 8 P100 GPUs; the big model for 300,000 steps, 3.5 days."],
 [("Cross-entropy", "Minus the log probability assigned to the correct token."),
  ("Label smoothing", "Replacing the one-hot target by a slightly flattened distribution."),
  ("Adam", "An optimizer with per-parameter adaptive step sizes."),
  ("Warmup", "A period of increasing learning rate at the start."),
  ("BLEU", "A score comparing machine translations with references by n-gram overlap."),
  ("Perplexity", "Exponential of the average cross-entropy.")],
 ["lrate = d_model^(-0.5) * min(step^(-0.5), step * warmup^(-1.5)); warmup = 4000.",
  "Adam: beta1 = 0.9, beta2 = 0.98, epsilon = 1e-9.",
  "Label smoothing 0.1 hurts perplexity but improves accuracy and BLEU.",
  "Dropout 0.1 on sublayers and embeddings in the base model.",
  "Base: 100k steps, 12 hours, 8 P100 GPUs; big: 300k steps, 3.5 days.",
  "WMT 2014 English-German had about 4.5 million sentence pairs."],
 [T("The training objective is the standard one for sequence generation. For each target position, the model gives a probability to every token. The loss is the negative log of the probability of the correct token, averaged over positions. Because of the mask, all positions of a sentence are trained at the same time."),
  T("The paper uses label smoothing with a value of 0.1. Instead of demanding probability one for the correct token and zero for all others, the target gives the correct token 0.9 and spreads the rest across the vocabulary. The model is trained to be less sure of itself. The authors report that this hurts perplexity, as the model learns to be more unsure, but improves accuracy and BLEU score."),
  M(r"\text{target}_k = \begin{cases} 1-\varepsilon_{ls} + \varepsilon_{ls}/V & k = \text{correct} \\ \varepsilon_{ls}/V & \text{otherwise} \end{cases}"),
  T("The optimizer is Adam with beta one 0.9, beta two 0.98 and epsilon 1e-9. The paper varies the learning rate during training with a formula: increase it linearly for the first 4000 steps, then decrease it in proportion to the inverse square root of the step number. The scale is proportional to d model to the power minus one half."),
  M(r"\mathrm{lrate} = d_{\mathrm{model}}^{-0.5}\cdot\min\bigl(\mathrm{step}^{-0.5},\ \mathrm{step}\cdot \mathrm{warmup}^{-1.5}\bigr)"),
  T("Why warm up? At the start the weights are random and the gradients are noisy. Large steps then could make training unstable. Adam's estimates of the second moment are also poor at first. So the schedule starts small and ramps up. The peak is reached exactly at the warmup step, where the two terms in the minimum are equal."),
  T("The reported training costs were modest for the time. The base model took 100,000 steps, about 12 hours, on one machine with 8 P100 GPUs. The big model took 300,000 steps, about 3.5 days. Batches held roughly 25,000 source tokens and 25,000 target tokens. The English-German data had about 4.5 million sentence pairs."),
  T("The labs compute the schedule, the smoothed target and the loss with and without smoothing.")],
 [("What does label smoothing do?", ["Softens the one-hot target", "Increases the learning rate", "Adds layers", "Removes dropout"], 0, "Value 0.1 in the paper."),
  ("When is the learning rate highest?", ["At the end of warmup", "At step 1", "At the end of training", "Never"], 0, "Step 4000 in the paper."),
  ("What optimizer does the paper use?", ["Adam", "Plain SGD", "RMSProp", "LBFGS"], 0, "With beta2 = 0.98."),
  ("What does label smoothing improve?", ["Accuracy and BLEU", "Perplexity", "Memory use", "Training speed"], 0, "Perplexity gets worse.")],
 [("What is the warmup length?", "4000 steps."), ("How long did the base model train?", "About 12 hours on 8 GPUs."), ("What is the big model's d_model?", "1024."), ("What is the loss?", "Cross-entropy.")],
 [PL("Learning rate", "Write lrate(step, d_model, warmup): d_model^-0.5 * min(step^-0.5, step * warmup^-1.5). Use import math if needed.",
     "lrate(step, d_model, warmup)", """
def lrate(step, d_model, warmup):
    return (d_model ** -0.5) * min(step ** -0.5, step * warmup ** -1.5)
""", [[1, 512, 4000], [4000, 512, 4000], [8000, 512, 4000], [100, 1024, 4000], [100000, 512, 4000]], "Take the smaller of the two terms.", approx=1e-9),
  PL("Peak step", "Write peak_lr(d_model, warmup): the largest learning rate in the schedule, reached at step = warmup.",
     "peak_lr(d_model, warmup)", """
def peak_lr(d_model, warmup):
    return (d_model ** -0.5) * (warmup ** -0.5)
""", [[512, 4000], [1024, 4000], [512, 8000], [256, 100]], "Both terms are equal at the warmup step.", approx=1e-9),
  PL("Smoothed target", "Write smooth_target(correct, v, eps): the list of length v with 1 - eps + eps / v at the correct index and eps / v elsewhere, rounded to 9 decimals.",
     "smooth_target(correct, v, eps)", """
def smooth_target(correct, v, eps):
    out = []
    for k in range(v):
        if k == correct:
            out.append(round(1 - eps + eps / v, 9))
        else:
            out.append(round(eps / v, 9))
    return out
""", [[1, 4, 0.1], [0, 2, 0.0], [2, 5, 0.2], [0, 1, 0.1]], "Put most mass on the correct index."),
  PL("Cross-entropy with a target", "Write xent(probs, target): minus the sum of target[k] * ln(probs[k]) over k (skip terms where target is 0), rounded to 6 decimals. Use import math.",
     "xent(probs, target)", """
import math
def xent(probs, target):
    s = 0.0
    for p, t in zip(probs, target):
        if t > 0:
            s -= t * math.log(p)
    return round(s, 6)
""", [[[0.7, 0.2, 0.1], [1, 0, 0]], [[0.5, 0.5], [0.5, 0.5]], [[0.25, 0.75], [0.0, 1.0]], [[0.6, 0.2, 0.2], [0.8, 0.1, 0.1]]], "Skip zero targets."),
  ORDER("Training step", "Order the steps.", ["Embed the source and shifted target", "Run encoder and decoder with masks", "Compute the smoothed cross-entropy", "Compute gradients", "Update with Adam at the scheduled learning rate"]),
  MATCH("Settings", "Match each setting with its value.", [("Warmup", "4000 steps"), ("Label smoothing", "0.1"), ("Adam beta2", "0.98"), ("Base model steps", "100,000"), ("Dropout", "0.1")]),
  FILL("Training", "The learning rate rises for {{4000}} steps then decays with the inverse square {{root}} of the step.")]))

CHS.append(CH(
 "Decoding, results and what came next",
 ("Generation", [
  "Greedy decoding | picks | Most probable token",
  "Beam search | keeps | Several hypotheses",
  "Beam size | is | 4 in the paper",
  "Length penalty | is | 0.6",
  "BLEU | measures | Translation quality",
  "BERT | uses | Encoder stack",
  "GPT | uses | Decoder stack"]),
 ["To translate, the decoder is run repeatedly: feed the tokens so far, take the next-token distribution, choose a token, append, repeat until an end symbol. Greedy decoding always picks the most probable token. Beam search keeps several partial translations and extends the best ones.",
  "The paper used beam search with beam size 4 and a length penalty of 0.6 for translation. The big model scored 28.4 BLEU on English to German and 41.8 on English to French.",
  "Later models showed that the same blocks scale. Encoder-only models such as BERT and decoder-only models such as GPT are background knowledge in this course."],
 [("Greedy decoding", "Choose the highest-probability token at each step."),
  ("Beam search", "Keep the k best partial outputs at each step."),
  ("Beam size", "The number k of hypotheses kept."),
  ("Length penalty", "A correction so that longer outputs are not unfairly penalized by log probabilities."),
  ("End symbol", "A special token that stops generation."),
  ("BLEU", "An n-gram overlap score between output and references.")],
 ["Greedy decoding is fast but can miss better sequences.",
  "Beam search scores a hypothesis by the sum of log probabilities (with a length correction).",
  "The paper used beam size 4 and length penalty alpha = 0.6.",
  "Results: big model 28.4 BLEU (EN-DE) and 41.8 BLEU (EN-FR).",
  "Generation cost: each new token needs a decoder pass; caching keys and values avoids recomputation (background).",
  "Encoder-only (BERT) and decoder-only (GPT) models are descendants (background)."],
 [T("Training used the true previous tokens, but at test time the true target is unknown. So the decoder generates one token at a time. Start with a start symbol. Run the decoder on the tokens so far. Look at the distribution for the last position. Choose a token. Append it and repeat, until the end symbol appears or a length limit is reached."),
  T("The simplest rule is greedy: always take the most probable token. It is fast but short-sighted: a locally best word might lead to a poor sentence. Beam search is a compromise. Keep the k best partial outputs. Extend each by every possible next token. Score the extensions by total log probability. Keep the best k again. The paper used a beam size of four."),
  M(r"\mathrm{score}(y) = \frac{1}{lp(y)}\sum_{t}\log p(y_t \mid y_{<t}, x), \qquad lp(y) = \frac{(5+|y|)^{\alpha}}{(5+1)^{\alpha}}"),
  T("Long hypotheses collect more negative log probabilities, so unfiltered beam search prefers short outputs. A length penalty corrects this. The paper set alpha to 0.6, after tuning on a development set, as it reports in the training section. The formula above is one common form of the penalty from earlier translation work; I give it as background knowledge, not a quote from the paper."),
  T("The results speak for themselves. The big Transformer reached 28.4 BLEU on the WMT 2014 English to German test set, more than two BLEU above the previous best including ensembles. On English to French it reached 41.8 BLEU after 3.5 days of training on eight GPUs, a fraction of the training cost of earlier models."),
  T("What came next? Encoder-only models such as BERT, trained to predict masked words, set records on language understanding tasks. Decoder-only models such as the GPT family were trained to predict the next word and became the basis of modern chat assistants. Vision Transformers apply the same blocks to image patches. None of this is in the 2017 paper, but all of it uses the pieces you have just built."),
  T("The labs below implement a greedy decoding loop with a small table as the model, length-normalized beam scoring, and a final check of sizes. Where to go next: read the paper itself, then implement a small Transformer in your favourite library and train it on a toy copy task.")],
 [("What does greedy decoding choose?", ["The most probable token at each step", "A random token", "The longest word", "The rarest word"], 0, "Fast but short-sighted."),
  ("What beam size did the paper use?", ["4", "1", "100", "0"], 0, "With length penalty 0.6."),
  ("What does a length penalty correct?", ["Bias toward short outputs", "Bias toward long outputs", "The vocabulary", "The learning rate"], 0, "Log probabilities add up."),
  ("Which descendant uses only the encoder?", ["BERT", "GPT", "WaveNet", "PixelCNN"], 0, "Background knowledge.")],
 [("What stops generation?", "An end symbol or length limit."), ("What does beam search keep?", "The k best partial outputs."), ("Which BLEU on EN-FR?", "41.8 for the big model."), ("What is GPT built from?", "Decoder-style layers (background).")],
 [PL("Greedy decoding loop", "A model is a table T: T[token] is the list of next-token probabilities. Write greedy_decode(T, start, end, max_len): starting from start, repeatedly append the arg-max next token (ties to the lowest index) until the end token is produced or max_len tokens in total. Return the list including start and the end token if reached.",
     "greedy_decode(T, start, end, max_len)", """
def greedy_decode(T, start, end, max_len):
    seq = [start]
    while len(seq) < max_len:
        probs = T[seq[-1]]
        best = 0
        for i in range(1, len(probs)):
            if probs[i] > probs[best]:
                best = i
        seq.append(best)
        if best == end:
            break
    return seq
""", [[[[0.1, 0.8, 0.1], [0.1, 0.1, 0.8], [0.3, 0.3, 0.4]], 0, 2, 10], [[[0.1, 0.8, 0.1], [0.9, 0.05, 0.05], [1.0, 0.0, 0.0]], 0, 2, 5], [[[0.0, 1.0], [0.0, 1.0]], 0, 0, 3]], "Stop at the end token or the length limit."),
  PL("Sequence log probability", "Write seq_logprob(T, seq): the sum of ln T[a][b] over adjacent pairs of seq, rounded to 6 decimals. Use import math.",
     "seq_logprob(T, seq)", """
import math
def seq_logprob(T, seq):
    s = 0.0
    for a, b in zip(seq[:-1], seq[1:]):
        s += math.log(T[a][b])
    return round(s, 6)
""", [[[[0.5, 0.5], [0.25, 0.75]], [0, 1, 1]], [[[0.9, 0.1], [0.4, 0.6]], [0, 0, 0]], [[[1.0]], [0, 0]]], "Add logs of the transition probabilities."),
  PL("Length penalty", "Write length_penalty(n, alpha): ((5 + n) / 6) ** alpha.",
     "length_penalty(n, alpha)", """
def length_penalty(n, alpha):
    return ((5 + n) / 6) ** alpha
""", [[1, 0.6], [10, 0.6], [4, 1.0], [20, 0.0]], "The common form from translation systems.", approx=1e-9),
  PL("Beam score", "Write beam_score(logp, n, alpha): the sequence log probability divided by the length penalty ((5 + n)/6) ** alpha, rounded to 6 decimals.",
     "beam_score(logp, n, alpha)", """
def beam_score(logp, n, alpha):
    return round(logp / (((5 + n) / 6) ** alpha), 6)
""", [[-2.0, 4, 0.6], [-5.0, 10, 0.6], [-1.0, 1, 0.0], [-3.0, 7, 1.0]], "Divide the log probability by the penalty."),
  ORDER("Decoding loop", "Order the steps.", ["Start with the start symbol", "Run the decoder on the tokens so far", "Take the distribution for the last position", "Choose and append a token", "Stop at the end symbol"]),
  MATCH("Decoding", "Match each term with its meaning.", [("Greedy", "Best token each step"), ("Beam search", "Keeps k hypotheses"), ("Length penalty", "Corrects short bias"), ("BLEU", "Translation score"), ("End symbol", "Stops generation")]),
  FILL("Decoding", "Beam search keeps several {{hypotheses|candidates|partial outputs}}. The paper used beam size {{4|four}}.")]))
