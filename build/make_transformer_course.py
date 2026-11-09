#!/usr/bin/env python3
"""Build the Transformer course. Usage: python3 make_transformer_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "trf"))
import cmk, trf  # noqa: E402

PRONOUNCE = {
    "Vaswani": "vah swah nee", "BERT": "bert", "GPT": "G P T", "BLEU": "bloo", "WMT": "W M T", "P100": "P one hundred",
    "ReLU": "rel you", "NeurIPS": "neur ips", "LayerNorm": "layer norm", "softmax": "soft max", "Softmax": "Soft max",
    "d_model": "d model", "d_ff": "d f f", "d_k": "d k", "d_v": "d v", "Adam": "adam", "BPE": "B P E", "FFN": "F F N",
    "GPUs": "G P Us", "GPU": "G P U", "Transformers": "Transformers", "argmax": "arg max", "arg-max": "arg max",
    "EN-DE": "English German", "EN-FR": "English French", "sqrt": "square root", "W^O": "W O",
}

SANDBOX = cmk.terminal("Transformer lookup", "tf>", "A scripted lookup, not a real model. Try: base, attn, lr, bleu", [
    ("base", ["N = 6 layers each side, d_model = 512, d_ff = 2048, h = 8, d_k = d_v = 64", "dropout 0.1, label smoothing 0.1, about 65M parameters"]),
    ("attn", ["Attention(Q,K,V) = softmax(Q K^T / sqrt(d_k)) V"]),
    ("lr", ["lrate = d_model^-0.5 * min(step^-0.5, step * warmup^-1.5)", "warmup = 4000, Adam beta1 0.9, beta2 0.98, eps 1e-9"]),
    ("bleu", ["big model: EN-DE 28.4, EN-FR 41.8", "base model: EN-DE 27.3, EN-FR 38.1"]),
    ("decode", ["beam size 4, length penalty 0.6"]),
])

EXAM = [
 ("Who introduced the Transformer?", ["Vaswani and colleagues at Google", "Hochreiter and Schmidhuber", "LeCun et al.", "Radford et al."], 0, "Attention Is All You Need, 2017."),
 ("What did the Transformer drop?", ["Recurrence and convolution", "Attention", "Embeddings", "Softmax"], 0, "Only attention and feed-forward layers remain."),
 ("How many layers does the base encoder have?", ["6", "2", "12", "24"], 0, "N = 6."),
 ("What is d_model in the base model?", ["512", "64", "2048", "8"], 0, "Vector width."),
 ("What is d_ff in the base model?", ["2048", "512", "64", "4096"], 0, "The big model uses 4096."),
 ("How many heads does the base model have?", ["8", "1", "16", "64"], 0, "16 in the big model."),
 ("What is d_k per head in the base model?", ["64", "512", "8", "2048"], 0, "512 / 8."),
 ("Why does attention need positional encoding?", ["It ignores order by itself", "Embeddings are small", "To save memory", "To add labels"], 0, "Shuffled input gives shuffled output."),
 ("Which functions form the positional encoding?", ["Sine and cosine", "ReLU", "Tanh", "Sigmoid"], 0, "Of different frequencies."),
 ("How is the positional encoding combined with embeddings?", ["Added", "Multiplied", "Concatenated", "Ignored"], 0, "Same width d_model."),
 ("What does the softmax in attention produce?", ["Weights that sum to one", "Integers", "Gradients", "Masks"], 0, "One row per query."),
 ("Why divide by sqrt(d_k)?", ["To stop large dot products saturating the softmax", "To save time", "To mask padding", "To normalize values"], 0, "Variance of dot products grows with d_k."),
 ("What are the three attention inputs?", ["Queries, keys and values", "Inputs, outputs, labels", "Weights, biases, masks", "Tokens, positions, heads"], 0, "Q, K and V."),
 ("What does multi-head attention do?", ["Runs several attentions in subspaces and concatenates", "Averages the sequence", "Adds a decoder", "Doubles the vocabulary"], 0, "Then a W^O projection."),
 ("How does cost grow with sequence length n in attention?", ["Quadratically", "Linearly", "Logarithmically", "Constantly"], 0, "n by n scores."),
 ("What does the causal mask forbid?", ["Attending to later positions", "Attending to earlier positions", "Using embeddings", "Using dropout"], 0, "Decoder self-attention."),
 ("What are masked scores set to before softmax?", ["A very negative number", "Zero", "One", "Their average"], 0, "Minus infinity in the paper."),
 ("What is teacher forcing?", ["Feeding the true previous tokens in training", "Forcing a teacher model", "Using no labels", "Skipping the mask"], 0, "Enables parallel training."),
 ("What is the form of a wrapped sublayer?", ["LayerNorm(x + Sublayer(x))", "Sublayer(LayerNorm(x))", "x * Sublayer(x)", "ReLU(x)"], 0, "Residual then norm."),
 ("What does layer normalization normalize over?", ["Features of one position", "The batch", "The vocabulary", "The sentence"], 0, "Independent of the batch."),
 ("What is inside the feed-forward network?", ["Linear, ReLU, linear", "Attention", "Convolution", "Softmax only"], 0, "Applied per position."),
 ("Is encoder self-attention causal?", ["No, it is bidirectional", "Yes", "Only at test time", "Only in layer 6"], 0, "A padding mask only."),
 ("What is the encoder's final output called here?", ["Memory", "Logits", "Mask", "Query"], 0, "Read by cross-attention."),
 ("How many sublayers does a decoder layer have?", ["3", "2", "1", "4"], 0, "Masked self, cross, feed-forward."),
 ("Where do cross-attention queries come from?", ["The decoder", "The encoder", "The embedding table", "The loss"], 0, "Keys and values come from the encoder."),
 ("What is the decoder input at training time?", ["The target shifted right", "The source", "Random noise", "The logits"], 0, "Starting with a start symbol."),
 ("What does the final linear plus softmax produce?", ["Next-token probabilities", "Positions", "Heads", "Masks"], 0, "Over the vocabulary."),
 ("What label smoothing value did the paper use?", ["0.1", "0.9", "0", "0.5"], 0, "It hurts perplexity but helps BLEU."),
 ("Which optimizer did the paper use?", ["Adam", "SGD", "RMSProp", "Adagrad"], 0, "beta2 = 0.98."),
 ("How long is the warmup?", ["4000 steps", "100 steps", "100,000 steps", "40 steps"], 0, "Then inverse square root decay."),
 ("Where is the learning rate highest?", ["At the end of warmup", "At step 1", "At the end", "It is constant"], 0, "The two terms in the min are equal."),
 ("What beam size did the paper use?", ["4", "1", "20", "100"], 0, "With length penalty 0.6."),
 ("What BLEU did the big model get on English to German?", ["28.4", "41.8", "10.0", "99.0"], 0, "41.8 was English to French."),
 ("What BLEU did the big model get on English to French?", ["41.8", "28.4", "27.3", "38.1"], 0, "Reported in the paper."),
 ("Which model family is built from encoder-style layers (background)?", ["BERT", "GPT", "WaveNet", "PixelCNN"], 0, "Trained on masked words."),
 ("Which model family is built from decoder-style layers (background)?", ["GPT", "BERT", "ResNet", "VGG"], 0, "Trained on next-word prediction."),
 ("Why does beam search need a length penalty?", ["Log probabilities favour short outputs", "The beam is too large", "The vocabulary is small", "Masks fail"], 0, "Longer sequences have lower total log probability."),
 ("What does weight tying share?", ["Embedding and output projection matrices", "Heads", "Layers", "Masks"], 0, "The paper does this to save parameters."),
]

CFG = dict(id="transformer", title="The Transformer: Encoder and Decoder", subtitle="Attention, heads, masks, layers and training, with Python labs",
    description="Attention Is All You Need (Vaswani et al., 2017): positional encoding, scaled dot-product and multi-head attention, masks, feed-forward layers with residuals and layer norm, the encoder stack, the decoder stack with cross-attention, training schedule and label smoothing, and beam search. Theory plus Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="trf", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "transformer.course.json")
    cmk.main(CFG, trf.CHS, [sys.argv[0], out])
