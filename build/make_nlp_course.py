#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the NLP course. Usage: python3 make_nlp_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "nlp"))
import cmk, nlp_a, nlp_b, make_apps  # noqa: E402
make_apps.main()
CHS = nlp_a.CHS + nlp_b.CHS
PRONOUNCE = {"NLP": "N L P", "TF-IDF": "T F I D F", "BM25": "B M twenty five", "BERT": "bert", "GPT": "G P T", "LSTM": "L S T M", "RNN": "R N N", "GRU": "G R U", "BPE": "B P E",
    "word2vec": "word to vec", "GloVe": "glove", "Viterbi": "vih ter bee", "CKY": "C K Y", "BLEU": "blue", "ROUGE": "rooj", "RAG": "rag", "RLHF": "R L H F", "ModernBERT": "modern bert",
    "Naive": "nye eve", "Bayes": "bayz", "Zipf": "zif", "Levenshtein": "leh ven shtine", "Hochreiter": "hock rye ter", "Schmidhuber": "shmid hoo ber", "Bahdanau": "bah da now",
    "Mikolov": "mik oh lov", "seq2seq": "seq to seq", "softmax": "soft max", "tanh": "tan H", "Llama": "lah ma", "RoBERTa": "roberta", "n-gram": "en gram", "stemming": "stem ing", "lemma": "lem uh"}
SANDBOX = cmk.terminal("NLP cheat sheet", "nlp>", "A scripted lookup. Try: tokens, tfidf, cosine, ngram, bayes, viterbi, embed, attention, bert, gpt, bm25, rag", [
    ("tokens", ["Split text into tokens: words, subwords or characters. Normalise case and Unicode first."]),
    ("tfidf", ["tf-idf = tf x log(N / df). Frequent in this document, rare overall."]),
    ("cosine", ["cos(a, b) = a . b / (|a| |b|). Compares direction, not length."]),
    ("ngram", ["P(w | previous) = count(previous w) / count(previous). Smooth for unseen pairs. Perplexity measures fit."]),
    ("bayes", ["Pick the class maximising log P(class) + sum log P(word | class), with add-one smoothing."]),
    ("viterbi", ["Dynamic programming over tags: best[t][s] = max over previous of best + log transition + log emission."]),
    ("embed", ["Dense vectors where similar contexts mean similar words. king - man + woman is about queen."]),
    ("attention", ["softmax(Q K^T / sqrt(d)) V. Causal mask hides future tokens."]),
    ("bert", ["Encoder, bidirectional, pretrained by masked language modelling. Add a head and fine-tune."]),
    ("gpt", ["Decoder, causal, pretrained to predict the next token. Prompt it, or tune it to follow instructions."]),
    ("bm25", ["Lexical ranking: IDF times saturating, length-normalised term frequency."]),
    ("rag", ["Retrieve relevant chunks, put them in the prompt, answer from them, cite them."]),
])
EXAM = [
 ("What is tokenisation?", ["Splitting text into units", "Translating", "Tagging", "Ranking"], 0, "First step."),
 ("What does stemming do?", ["Chops words to a root form", "Adds suffixes", "Translates", "Sorts"], 0, "Crude normalisation."),
 ("What does Zipf's law say?", ["A few words are very frequent", "All words are equal", "Words are random", "Sentences are short"], 0, "Long tail."),
 ("What is a bag of words?", ["Word counts ignoring order", "A sequence", "A tree", "A grammar"], 0, "Order is lost."),
 ("What does TF-IDF down-weight?", ["Words common across documents", "Rare words", "Numbers", "Long words"], 0, "Inverse document frequency."),
 ("What does cosine similarity compare?", ["Direction of vectors", "Length only", "Spelling", "Counts only"], 0, "Angle."),
 ("What does an n-gram model predict?", ["The next word from the last n-1", "A topic", "A tag", "A translation"], 0, "Markov assumption."),
 ("What does perplexity measure?", ["How surprised a model is by text", "Word length", "Speed", "Accuracy of tags"], 0, "Lower is better."),
 ("Why smooth counts?", ["Unseen n-grams would get zero probability", "To speed up", "To stem", "To tag"], 0, "Add-one."),
 ("What does Naive Bayes assume?", ["Words are independent given the class", "Words are ordered", "Classes are equal", "No priors"], 0, "Naive."),
 ("Why use macro F1?", ["It weights classes equally", "It is faster", "It ignores errors", "It counts only the largest class"], 0, "Imbalance."),
 ("What does the Viterbi algorithm find?", ["The best tag sequence", "The shortest word", "A vector", "A topic"], 0, "Dynamic programming."),
 ("What does a CKY parser build?", ["A parse tree", "A vector", "An index", "A tag"], 0, "Chart parsing."),
 ("What is named-entity recognition?", ["Finding people, places and organisations", "Counting words", "Stemming", "Translating"], 0, "Spans with types."),
 ("What does word2vec skip-gram predict?", ["Context words from a centre word", "A label", "A sentence", "A tag"], 0, "Embeddings."),
 ("What does king - man + woman approximate?", ["queen", "man", "kings", "throne"], 0, "Analogy."),
 ("Why do plain RNNs forget?", ["Vanishing gradients", "Short words", "No weights", "Too few tags"], 0, "Long chains."),
 ("What does attention compute?", ["A relevance-weighted average", "A count", "A tag", "A stem"], 0, "Softmax weights."),
 ("What does a causal mask do?", ["Hides later tokens", "Hides earlier tokens", "Removes noise", "Shuffles"], 0, "Left to right."),
 ("What does BPE merge?", ["The most frequent adjacent pair", "Sentences", "Heads", "Layers"], 0, "Subwords."),
 ("How does BERT pretrain?", ["Masked language modelling", "Translation", "Parsing", "Sorting"], 0, "Fill the blank."),
 ("How does GPT pretrain?", ["Next-token prediction", "Masking", "Clustering", "Tagging"], 0, "Causal."),
 ("What does temperature control?", ["Randomness of sampling", "Model size", "Vocabulary", "Layers"], 0, "Sharper or flatter."),
 ("What is an inverted index?", ["Word to documents", "Document to words", "Tag to word", "Letter to word"], 0, "Search."),
 ("What does RAG do?", ["Retrieves documents to ground generation", "Stems words", "Tags parts of speech", "Compresses models"], 0, "Retrieve then generate."),
 ("What is a hallucination?", ["Fluent output not supported by facts", "A slow answer", "A rare word", "A typo"], 0, "Check claims."),
]
CFG = dict(id="nlp", title="Natural Language Processing",
    subtitle="From tokens and TF-IDF to n-grams, taggers, embeddings, transformers and large language models, classical and modern, with Python labs",
    description="A hands-on course in natural language processing covering classical and modern techniques: tokens, normalisation, stemming and Zipf's law; bag of words, TF-IDF, cosine similarity and edit distance; n-gram language models and perplexity; Naive Bayes text classification and evaluation; part-of-speech tagging with Viterbi, CKY parsing and entity extraction; word embeddings; recurrent networks, LSTMs, sequence-to-sequence models and attention; the transformer, positional encoding and subword tokenisers; BERT, GPT, prompting and sampling; and search with BM25, retrieval-augmented generation, evaluation metrics and responsible NLP. Every chapter has Python labs verified in the built-in interpreter, plus an n-gram text generator and a self-attention explorer.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="nlp", apps={"__NGRAM__": "ngram.html", "__ATTN__": "attn.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "nlp.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
