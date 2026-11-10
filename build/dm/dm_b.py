# -*- coding: utf-8 -*-
"""Decision models course, part 2: decoder-based models, calibration, evaluation, systems."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Decoder-based decision models (the Clef pattern)",
 ("Clef pattern", [
  "Decoder LLM | is | The base",
  "Prefill | reads | The whole prompt",
  "No generation | saves | Time",
  "Joint head | scores | Many fields",
  "Pointer head | picks | An input span",
  "KV cache | reuses | Shared prefix",
  "Multimodal | adds | Images"]),
 ["The other route builds a decision model on a decoder language model but never generates text. It runs only the prefill pass over the prompt, then reads the final hidden state with small heads. That keeps the language model's knowledge and instruction following while skipping slow token-by-token generation.",
  "Clef, from Cloudflare, is reported to use Qwen-based models of roughly 9 and 27 billion parameters with a joint schema head that fills several typed answers at once, and a pointer head that selects a span or item from the input. A related Kev design is described as a pointer head.",
  "Reported benefits are speed, typed outputs and shared computation through KV-cache reuse. Reports differ between sources, so verify specifics before relying on them."],
 [("Prefill", "The phase where a decoder processes the whole prompt in parallel before generating; a decision model stops here."),
  ("KV cache", "Stored attention keys and values from earlier tokens, reusable when the prompt shares a prefix."),
  ("Joint schema head", "A head that outputs several typed fields, such as a boolean, a choice and a score, from one pass."),
  ("Pointer head", "A head that picks a position or item in the input rather than a label from a fixed set."),
  ("Multimodal", "Handling more than text, for example images with text.")],
 ["Decoder + heads, no generation.",
  "Cost = one prefill.",
  "Pointer: choose among input items.",
  "Shared prefix: reuse the KV cache.",
  "Reported sizes: 9B and 27B (Clef)."],
 [T("A decoder language model like Llama or Qwen is built to generate: read the prompt, then emit one token at a time. The prompt phase, prefill, is a single parallel pass and is cheap per token. The generation phase is sequential and dominates latency, since each new token needs another pass. If you only need a decision, not an essay, you can stop after prefill, read the last hidden state, and feed it to a small head. That turns a language model into a decision model."),
  T("What do you gain over an encoder? A decoder with billions of parameters has more world knowledge, follows instructions and handles long, messy prompts, and can accept images if it is multimodal. What do you lose? It is bigger and slower than a 400-million-parameter encoder, though still far faster than a model that writes a chain of thought. Clef, announced by Cloudflare in 2026 and built on Qwen models reported at about 27 and 9 billion parameters, is the first well-known example of this pattern."),
  C("# prefill-only decision, in pseudocode\nhidden = decoder.prefill(prompt)[-1]        # last token state, no generation\nschema = {'urgent': 'boolean',\n          'team': ['billing', 'tech', 'sales'],\n          'priority': 'score'}\nout = {name: head[name](hidden) for name in schema}\n# one pass fills every field; none can be malformed", "python"),
  T("Two head ideas recur. A joint schema head answers several typed questions in one pass, so one prefill yields a boolean, a choice and a score together. A pointer head selects an item from the input itself, for example which of twenty tool descriptions or which retrieved passage best fits, which suits agent routing where the options are long and different each time. Both guarantee well-formed answers, unlike parsing generated text."),
  T("Because many requests share a long prefix, such as the same instructions, tool list or document, serving systems keep the attention keys and values of the shared part in a KV cache, so only the new suffix needs computing. For decision models that ask many questions about the same document this can make a large difference. You can run such models yourself: open weights and runtimes such as Unsloth and Ollama-style servers are mentioned in the project documentation. Remember the caveat that this category is only weeks old, and sources disagree on details.")],
 [("What does a prefill-only model skip?", ["Token-by-token generation", "Reading the prompt", "The head", "The weights"], 0, "No writing."),
  ("What does a pointer head choose?", ["An item or span from the input", "A random word", "A font", "A file"], 0, "Points into input."),
  ("What does a joint schema head provide?", ["Several typed answers in one pass", "A longer essay", "Image output", "Slower answers"], 0, "Multi-field."),
  ("What does a KV cache save?", ["Recomputing a shared prefix", "Disk space only", "Training", "Memory always"], 0, "Reuse."),
  ("What do decoders add over small encoders?", ["More knowledge and instruction following", "Smaller size", "Less cost", "Fewer parameters"], 0, "Scale."),
  ("What is the reliable way to treat reported model details?", ["Verify before relying", "Trust fully", "Ignore all", "Copy into papers"], 0, "Young field.")],
 [("prefill then head", "decision without generation"), ("KV cache reuse", "shared prefix")],
 [MATCH("Match the piece", "Pair each piece with its job.", [("Prefill", "process the prompt once"), ("Head", "read the final state into an answer"), ("Pointer head", "choose an input item"), ("KV cache", "reuse shared prefix work"), ("Joint head", "fill several fields at once")]),
  PL("Tokens to compute with cache", "Write tokens_needed(prefix_len, suffix_len, cached): total tokens to process: just the suffix if cached is True, else prefix plus suffix.", "tokens_needed(prefix_len, suffix_len, cached)", '''
def tokens_needed(prefix_len, suffix_len, cached):
    return suffix_len if cached else prefix_len + suffix_len
''', [[2000, 50, True], [2000, 50, False], [0, 10, True]], "Cache saves the prefix."),
  PL("Cache savings", "Write cache_savings(prefix_len, suffix_len, n_queries): the fraction of tokens saved over n_queries questions on the same prefix if the prefix is processed once (first query) and cached after; rounded to 3 decimals.", "cache_savings(prefix_len, suffix_len, n_queries)", '''
def cache_savings(prefix_len, suffix_len, n_queries):
    full = n_queries * (prefix_len + suffix_len)
    cached = prefix_len + n_queries * suffix_len
    return round(1 - cached / float(full), 3)
''', [[2000, 50, 10], [1000, 100, 1], [500, 50, 100]], "Amortise the prefix.", approx=0.002),
  PL("Pointer choice", "Write point(scores): the index of the highest score (first on ties).", "point(scores)", '''
def point(scores):
    b = 0
    for i in range(len(scores)):
        if scores[i] > scores[b]:
            b = i
    return b
''', [[[0.1, 0.9, 0.3]], [[1, 1]], [[5]]], "Pick an input item."),
  PL("Joint schema", "Write fill_schema(heads, hidden): heads is a list of [name, kind, weights] where kind is 'boolean' (sigmoid of weights dot hidden, rounded to 3 decimals) or 'score' (the plain dot product rounded to 3 decimals). Return a list of [name, value] pairs in order.", "fill_schema(heads, hidden)", '''
import math
def fill_schema(heads, hidden):
    out = []
    for name, kind, w in heads:
        z = sum([w[i] * hidden[i] for i in range(len(hidden))])
        if kind == 'boolean':
            out.append([name, round(1 / (1 + math.exp(-z)), 3)])
        else:
            out.append([name, round(z, 3)])
    return out
''', [[[['urgent', 'boolean', [1, 0]], ['size', 'score', [0, 2]]], [1, 1]], [[['a', 'boolean', [0, 0]]], [3, 4]], [[], [1]]], "Heads on one hidden state.", approx=None),
  PL("Latency estimate", "Write latency_ms(prefill_tokens, ms_per_prefill_token, gen_tokens, ms_per_gen_token): total milliseconds for prefill plus generation.", "latency_ms(prefill_tokens, ms_per_prefill_token, gen_tokens, ms_per_gen_token)", '''
def latency_ms(prefill_tokens, ms_per_prefill_token, gen_tokens, ms_per_gen_token):
    return round(prefill_tokens * ms_per_prefill_token + gen_tokens * ms_per_gen_token, 2)
''', [[500, 0.05, 0, 20], [500, 0.05, 300, 20], [100, 0.1, 5, 30]], "Generation dominates.", approx=0.02)]
))

CHS.append(CH(
 "Calibration: making probabilities trustworthy",
 ("Calibration", [
  "Confidence | should match | Accuracy",
  "Reliability diagram | plots | Bins",
  "ECE | averages | Gaps",
  "Brier score | squares | Errors",
  "Log loss | punishes | Confident mistakes",
  "Temperature | rescales | Logits",
  "Threshold | sets | Policy"]),
 ["A decision model is only useful if its probabilities mean something: of the cases where it says 90 percent, about 90 percent should be right. Neural networks are often overconfident, so we measure and repair calibration.",
  "Expected calibration error bins predictions by confidence and averages the gap between confidence and accuracy. Brier score and log loss are proper scoring rules that reward honest probabilities. Temperature scaling fixes much overconfidence with a single parameter fitted on held-out data.",
  "Some vendors train for calibration directly, with reinforcement learning on calibration objectives; reports describe this as a selling point, which you should test yourself."],
 [("Calibration", "The match between predicted probabilities and observed frequencies."),
  ("Expected calibration error", "The weighted average gap between confidence and accuracy across confidence bins."),
  ("Brier score", "The mean squared difference between predicted probability and the 0 or 1 outcome."),
  ("Log loss", "The mean negative log probability assigned to the true outcome."),
  ("Temperature scaling", "Dividing logits by a fitted constant to repair over- or under-confidence.")],
 ["ECE = sum over bins of (n_bin / n) |acc - conf|.",
  "Brier = mean (p - y)^2.",
  "Log loss = -mean log p(true).",
  "Fit T on a validation set, not the test set.",
  "Calibrate after fine-tuning."],
 [T("Suppose a model says 'refund approved, 95 percent' a thousand times. If 95 percent of those were correct, it is calibrated at that level. If only 80 percent were, it is overconfident, and a threshold of 0.9 will let through many mistakes. Modern networks tend to be overconfident because they are trained to push the loss down on the training data, which rewards ever larger logits."),
  T("To measure calibration, sort predictions into bins by confidence, say 0.5 to 0.6, 0.6 to 0.7 and so on. In each bin compare the average confidence with the fraction correct. Plotting accuracy against confidence gives a reliability diagram: a perfect model lies on the diagonal. Expected calibration error is the average of the gaps, weighted by bin size. Two scoring rules summarise both sharpness and calibration. The Brier score is the mean squared error of the probability. Log loss is the mean negative log probability of the truth, and punishes confident mistakes harshly."),
  C("import numpy as np\ndef ece(conf, correct, bins=10):\n    conf, correct = np.asarray(conf), np.asarray(correct)\n    edges = np.linspace(0, 1, bins + 1)\n    total = 0.0\n    for lo, hi in zip(edges[:-1], edges[1:]):\n        m = (conf > lo) & (conf <= hi)\n        if m.any():\n            total += m.mean() * abs(correct[m].mean() - conf[m].mean())\n    return total", "python"),
  T("The repair that works surprisingly often is temperature scaling. Keep the model fixed, hold out a validation set, and find the single number T that minimises log loss when logits are divided by T. When the model is overconfident T comes out above one, which flattens the probabilities without changing which option is top. Accuracy stays the same; only confidence changes. For richer problems there are other methods, such as isotonic regression, but start simple."),
  T("Some decision-model vendors describe training with a calibration-aware reinforcement objective, reported under the name RLCD, to make confidence honest from the start. Whether that works for your data is an empirical question, and the answer depends on the shift between their training data and your inputs. Always check calibration on your own held-out cases, re-check after fine-tuning or changing the question wording, and monitor it in production, because the world changes.")],
 [("What does a calibrated 90 percent mean?", ["About 90 percent of such answers are right", "The model is 90 percent big", "Ninety tokens", "Ninety labels"], 0, "Frequency matches."),
  ("What does temperature above 1 do to probabilities?", ["Flattens them", "Sharpens them", "Reorders options", "Removes options"], 0, "Less confident."),
  ("Does temperature scaling change accuracy?", ["No, only confidence", "Yes, raises it", "Yes, lowers it", "Only for text"], 0, "Same argmax."),
  ("What does log loss punish most?", ["Confident wrong answers", "Short answers", "Rare labels", "Slow answers"], 0, "Heavy penalty."),
  ("What does ECE average?", ["Confidence versus accuracy gaps over bins", "Latencies", "Token counts", "Losses only"], 0, "Per-bin gaps."),
  ("Where should T be fitted?", ["On a validation set", "On the test set", "On training data only", "Never"], 0, "Held-out.")],
 [("ECE", "calibration error"), ("T = argmin log loss", "temperature scaling")],
 [APP("CALIB", "Calibration lab", "A model's confidences and outcomes are plotted as a reliability diagram. Drag the temperature slider to repair the overconfident model and watch ECE fall. Reach an ECE below 0.04 to complete the lab.", 820),
  MATCH("Match the metric", "Pair each metric with its idea.", [("ECE", "average confidence-accuracy gap"), ("Brier score", "mean squared probability error"), ("Log loss", "punishes confident mistakes"), ("Reliability diagram", "accuracy against confidence"), ("Temperature scaling", "one-parameter repair")]),
  PL("Brier score", "Write brier(probs, outcomes): the mean of (p - y)^2 where outcomes are 0 or 1; rounded to 4 decimals.", "brier(probs, outcomes)", '''
def brier(probs, outcomes):
    return round(sum([(p - y) ** 2 for p, y in zip(probs, outcomes)]) / len(probs), 4)
''', [[[0.9, 0.2, 0.8], [1, 0, 0]], [[1.0, 0.0], [1, 0]], [[0.5, 0.5], [1, 0]]], "Squared error of probabilities.", approx=0.0003),
  PL("Log loss", "Write log_loss(probs, outcomes): the mean of -log(p) when the outcome is 1 and -log(1-p) when it is 0; rounded to 4 decimals.", "log_loss(probs, outcomes)", '''
import math
def log_loss(probs, outcomes):
    t = 0.0
    for p, y in zip(probs, outcomes):
        t = t - math.log(p if y == 1 else 1 - p)
    return round(t / len(probs), 4)
''', [[[0.9, 0.2], [1, 0]], [[0.5, 0.5], [1, 0]], [[0.99, 0.01], [1, 0]]], "Confident mistakes cost a lot.", approx=0.0005),
  PL("Expected calibration error", "Write ece(conf, correct, bins): split [0, 1] into equal bins (a value belongs to bin min(int(c * bins), bins - 1)); the sum over non-empty bins of (n_bin / n) |mean(correct) - mean(conf)|, rounded to 4 decimals.", "ece(conf, correct, bins)", '''
def ece(conf, correct, bins):
    n = len(conf)
    total = 0.0
    for b in range(bins):
        idx = [i for i in range(n) if min(int(conf[i] * bins), bins - 1) == b]
        if idx:
            c = sum([conf[i] for i in idx]) / float(len(idx))
            a = sum([correct[i] for i in idx]) / float(len(idx))
            total = total + len(idx) / float(n) * abs(a - c)
    return round(total, 4)
''', [[[0.9, 0.9, 0.9, 0.9], [1, 1, 1, 0], 10], [[0.6, 0.6, 0.95, 0.95], [1, 0, 1, 1], 5], [[0.5], [1], 2]], "Gap per bin.", approx=0.0005),
  PL("Reliability bins", "Write reliability(conf, correct, bins): for each non-empty bin (bin of c is min(int(c * bins), bins - 1)) return [bin index, count, mean confidence, accuracy], with the last two rounded to 3 decimals.", "reliability(conf, correct, bins)", '''
def reliability(conf, correct, bins):
    out = []
    for b in range(bins):
        idx = [i for i in range(len(conf)) if min(int(conf[i] * bins), bins - 1) == b]
        if idx:
            out.append([b, len(idx), round(sum([conf[i] for i in idx]) / float(len(idx)), 3), round(sum([correct[i] for i in idx]) / float(len(idx)), 3)])
    return out
''', [[[0.9, 0.95, 0.2], [1, 0, 0], 5], [[0.5, 0.5], [1, 1], 2], [[0.1], [0], 10]], "Data for the diagram.", approx=None),
  PL("Apply temperature to a pair", "Write calibrate(logit, T): the sigmoid of logit / T rounded to 4 decimals.", "calibrate(logit, T)", '''
import math
def calibrate(logit, T):
    return round(1 / (1 + math.exp(-logit / T)), 4)
''', [[3, 1], [3, 2], [-2, 1.5], [0, 3]], "Softens overconfident logits.", approx=None),
  PL("Best temperature", "Write fit_temperature(logits, outcomes, candidates): the candidate T with the lowest log loss of sigmoid(logit / T) against 0 or 1 outcomes (first on ties).", "fit_temperature(logits, outcomes, candidates)", '''
import math
def fit_temperature(logits, outcomes, candidates):
    best = None
    bl = None
    for T in candidates:
        loss = 0.0
        for z, y in zip(logits, outcomes):
            p = 1 / (1 + math.exp(-z / T))
            loss = loss - math.log(p if y == 1 else 1 - p)
        loss = round(loss, 9)
        if bl is None or loss < bl:
            bl = loss
            best = T
    return best
''', [[[4, 4, 4, 4], [1, 1, 0, 0], [0.5, 1, 2, 4, 8]], [[3, -3], [1, 0], [0.5, 1, 2]], [[2, 2, -2], [1, 0, 0], [1, 2, 3]]], "Minimise validation log loss."),
  PL("Threshold for target precision", "Write threshold_for_precision(conf, correct, target): the smallest confidence value present in conf such that the precision of all predictions with confidence at or above it is at least target; return None if none.", "threshold_for_precision(conf, correct, target)", '''
def threshold_for_precision(conf, correct, target):
    for t in sorted(set(conf)):
        idx = [i for i in range(len(conf)) if conf[i] >= t]
        if sum([correct[i] for i in idx]) / float(len(idx)) >= target:
            return t
    return None
''', [[[0.6, 0.7, 0.8, 0.9, 0.95], [0, 1, 0, 1, 1], 0.9], [[0.5, 0.6], [0, 0], 0.5], [[0.9, 0.8], [1, 1], 1.0]], "Pick an operating point.")]
))

CHS.append(CH(
 "Evaluating decision models",
 ("Evaluation", [
  "Test set | measures | Your task",
  "Accuracy | counts | Right answers",
  "Cost matrix | prices | Mistakes",
  "Latency | measures | Speed",
  "Benchmarks | compare | Vendors",
  "Contamination | inflates | Scores",
  "Fine-tuning gain | shows | Headroom"]),
 ["Do not rely on a vendor's headline numbers. Reports in this field include a Decision Index and results on public tasks such as BANKING77 intent classification, but they are self-reported and may not match your data.",
  "Build a labelled test set from your own traffic, measure accuracy, calibration, per-class errors, cost-weighted loss and latency at your batch size, and compare against a simple baseline and against a large LLM.",
  "Check the effect of fine-tuning: a few hundred of your own examples often add the most. Keep a separate untouched test set and watch for leakage."],
 [("Test set", "Labelled examples held out from all training and tuning, used to estimate real performance."),
  ("Cost matrix", "A table giving the cost of each kind of mistake, used to choose thresholds."),
  ("Baseline", "A simple reference such as the majority class or keyword rules, to show the added value."),
  ("Contamination", "Test data leaking into training, which inflates scores."),
  ("Decision Index", "A reported composite benchmark for decision models; treat as a vendor measure until independently checked.")],
 ["Own data first.",
  "Report accuracy, calibration, latency and cost.",
  "Compare with a baseline and with an LLM.",
  "Per-class precision and recall.",
  "Re-test on every model update."],
 [T("When a new model claims to beat everything, your first move is not to read the leaderboard but to build a test. Collect a few hundred real inputs, label them carefully (ideally by two people so you measure disagreement), and set them aside. This is the only number that predicts how the system will behave for you."),
  T("Public results are context. For the decision models in this chapter's sources, vendors report scores on a composite they call the Decision Index and on well-known tasks like BANKING77, a set of seventy-seven banking intents. Such numbers come with the usual caveats: they are self-reported, the prompts and options may be favourable, training data may overlap with test data, and the field changes monthly, with different articles giving different figures. Quote them as 'reported by the vendor, as of date' and verify."),
  C("from collections import Counter\ndef report(y_true, y_pred):\n    acc = sum(a == b for a, b in zip(y_true, y_pred)) / len(y_true)\n    errors = Counter((a, b) for a, b in zip(y_true, y_pred) if a != b)\n    return acc, errors.most_common(5)   # which confusions matter most", "python"),
  T("Accuracy is not enough. Look at per-class precision and recall, since rare but costly classes can hide behind a good average. Use a cost matrix: wrongly auto-approving a fraud costs far more than sending a good case to review. Check calibration, as in the last chapter, and measure latency and throughput on your own hardware with your own batch size, since a vendor's milliseconds assume their setup."),
  T("Finally compare options fairly. A keyword baseline tells you what the model adds. A large LLM given the same question is the quality ceiling and the cost reference. Fine-tune the decision model on part of your data to see headroom; if a few hundred examples lift accuracy a lot, the base model was not enough alone. Re-run the test whenever the model, the options wording or the input mix changes, and keep sampling live traffic for new labels.")],
 [("What is the first step when evaluating a model?", ["Build a test set from your data", "Read the leaderboard", "Buy hardware", "Rename classes"], 0, "Own data."),
  ("Why use a baseline?", ["To show what the model adds", "To slow things", "To hide errors", "To skip tests"], 0, "Reference."),
  ("What is contamination?", ["Test data leaking into training", "Dirty hardware", "Noise in audio", "Slow code"], 0, "Inflated score."),
  ("Why a cost matrix?", ["Mistakes cost different amounts", "To save time", "To shorten labels", "To tokenise"], 0, "Set thresholds."),
  ("How should vendor figures be quoted?", ["As reported with a date", "As facts", "Not at all, ever", "As official standards"], 0, "Self-reported."),
  ("What does a big fine-tuning gain suggest?", ["The base model alone was not enough", "The test is wrong", "Latency is low", "Costs are zero"], 0, "Headroom.")],
 [("classification_report", "per-class metrics"), ("confusion matrix", "which errors happen")],
 [MATCH("Match the term", "Pair each evaluation idea with its meaning.", [("Baseline", "simple reference method"), ("Cost matrix", "price of each mistake"), ("Contamination", "test data leaked into training"), ("Per-class recall", "found share of each class"), ("Latency", "time per request")]),
  PL("Accuracy", "Write accuracy(y_true, y_pred): the fraction correct, rounded to 3 decimals.", "accuracy(y_true, y_pred)", '''
def accuracy(y_true, y_pred):
    return round(sum([1 for a, b in zip(y_true, y_pred) if a == b]) / float(len(y_true)), 3)
''', [[['a', 'b', 'a'], ['a', 'a', 'a']], [['x'], ['x']], [['p', 'q'], ['q', 'p']]], "Fraction right.", approx=0.002),
  PL("Per-class precision and recall", "Write prf(y_true, y_pred, label): [precision, recall] for the label, each rounded to 3 decimals (0 when undefined).", "prf(y_true, y_pred, label)", '''
def prf(y_true, y_pred, label):
    tp = len([1 for a, b in zip(y_true, y_pred) if a == label and b == label])
    pp = len([b for b in y_pred if b == label])
    ap = len([a for a in y_true if a == label])
    p = tp / float(pp) if pp else 0
    r = tp / float(ap) if ap else 0
    return [round(p, 3), round(r, 3)]
''', [[['a', 'b', 'a', 'b'], ['a', 'a', 'a', 'b'], 'a'], [['x', 'y'], ['y', 'y'], 'x'], [['p'], ['p'], 'q']], "Rare classes matter.", approx=None),
  PL("Confusion pairs", "Write confusions(y_true, y_pred): [true, predicted, count] triples for every wrong prediction, sorted by count descending then alphabetically.", "confusions(y_true, y_pred)", '''
def confusions(y_true, y_pred):
    d = {}
    for a, b in zip(y_true, y_pred):
        if a != b:
            d[(a, b)] = d.get((a, b), 0) + 1
    keys = sorted(d.keys(), key=lambda k: (-d[k], k))
    return [[k[0], k[1], d[k]] for k in keys]
''', [[['a', 'a', 'b', 'c'], ['b', 'b', 'a', 'c']], [['x'], ['x']], [['p', 'q'], ['q', 'p']]], "Find the costly confusions."),
  PL("Cost-weighted error", "Write total_cost(y_true, y_pred, cost): cost is a list of [true, predicted, price] triples; wrong predictions not listed cost 1; correct ones cost 0. Return the total.", "total_cost(y_true, y_pred, cost)", '''
def total_cost(y_true, y_pred, cost):
    table = {}
    for a, b, c in cost:
        table[(a, b)] = c
    t = 0
    for a, b in zip(y_true, y_pred):
        if a != b:
            t = t + table.get((a, b), 1)
    return t
''', [[['fraud', 'ok', 'ok'], ['ok', 'fraud', 'ok'], [['fraud', 'ok', 100]]], [['a'], ['a'], []], [['a', 'b'], ['b', 'a'], [['a', 'b', 5]]]], "Not all errors are equal."),
  PL("Best threshold by cost", "Write best_threshold(conf, correct, candidates, c_wrong, c_review): for each candidate t, answered cases (conf >= t) cost c_wrong if wrong; the rest cost c_review each. Return the candidate with the lowest total cost (first on ties).", "best_threshold(conf, correct, candidates, c_wrong, c_review)", '''
def best_threshold(conf, correct, candidates, c_wrong, c_review):
    best = None
    bc = None
    for t in candidates:
        cost = 0
        for c, ok in zip(conf, correct):
            if c >= t:
                if not ok:
                    cost = cost + c_wrong
            else:
                cost = cost + c_review
        if bc is None or cost < bc:
            bc = cost
            best = t
    return best
''', [[[0.6, 0.7, 0.9, 0.95], [0, 0, 1, 1], [0.5, 0.8, 0.99], 10, 1], [[0.9, 0.9], [1, 1], [0.5, 0.95], 10, 1], [[0.55, 0.6], [0, 0], [0.5, 0.7], 2, 1]], "Trade review cost against error cost."),
  PL("Percentile latency", "Write percentile(values, q): the nearest-rank percentile: sort values and return the element at rank ceil(q / 100 x n) (1-based).", "percentile(values, q)", '''
import math
def percentile(values, q):
    s = sorted(values)
    k = int(math.ceil(q / 100.0 * len(s)))
    return s[max(k, 1) - 1]
''', [[[10, 20, 30, 40, 50], 50], [[5, 1, 9, 3], 95], [[7], 50]], "Tail latency matters more than the mean.")]
))

CHS.append(CH(
 "Decision models in real systems",
 ("Systems", [
  "Router | picks | The path",
  "Cascade | tries | Cheap first",
  "Guardrail | checks | Outputs",
  "Escalation | calls | Big model or human",
  "Logging | feeds | Evaluation",
  "Local serving | protects | Privacy",
  "Failure modes | need | Planning"]),
 ["The usual home for a decision model is a cascade: the fast model decides most cases, the uncertain ones escalate to a large LLM or a human, and the outcomes feed back into the evaluation data. Cost and latency fall while quality is kept by the thresholds.",
  "Typical uses are routing support tickets and agent tool calls, content and policy guardrails, verifying that an answer matches its sources, relevance filtering, and workflow gates. Open models can be run locally for privacy.",
  "Plan for failure: distribution shift, adversarial inputs, over-trust in confidence and silent changes in vendor models. Humans stay responsible for high-stakes decisions."],
 [("Cascade", "A chain of models from cheap and fast to expensive and accurate, with each stage answering only when confident."),
  ("Guardrail", "A check placed before or after a model to enforce policy, safety or format."),
  ("Router", "A component that sends each request to the best model or tool."),
  ("Distribution shift", "A change in the inputs over time, so past accuracy no longer holds."),
  ("Human in the loop", "A person reviews or decides cases the system is unsure about or that carry high risk.")],
 ["Fast model first, escalate when unsure.",
  "Log every decision and outcome.",
  "Re-calibrate when inputs drift.",
  "Local serving for private data.",
  "Humans own high-stakes calls."],
 [T("Put the pieces together. A request arrives. A decision model reads it and answers the typed question in a few milliseconds. If its confidence clears the threshold, the system acts. If not, it escalates: to a large reasoning model that thinks step by step, or to a person. Suppose eighty percent of traffic clears the bar. Then the expensive path serves a fifth of requests, and average cost and latency drop several-fold, while accuracy on the escalated cases comes from the strong model."),
  C("def handle(request):\n    p = decision_model.ask(request.text, question=request.question)\n    if max(p.values()) >= THRESHOLD:\n        result = ('auto', max(p, key=p.get))\n    else:\n        result = ('escalated', big_llm(request))\n    log(request, p, result)          # becomes tomorrow's test data\n    return result", "python"),
  T("Decision models fit several jobs. Routing: which team, which tool, which model. Guardrails: is this input safe, is this output on topic, does it follow the policy. Verification: does the answer follow from the retrieved sources. Gating in agents: should the agent continue, ask the user, or stop. Filtering: which of a hundred retrieved passages is relevant, using a pointer head. In all of them the decision is small and frequent, which is where a fast model beats a big one."),
  T("Where it runs matters. Open weights can be served on your own hardware with common tools, which keeps sensitive text in your own network and removes per-call fees, at the price of operating the system yourself. Hosted APIs are easier to start with but send data out and can change under you. Pin the model version, and re-run your evaluation when it updates."),
  T("Plan for failure. Inputs drift, so watch accuracy and calibration on a sample of live traffic. Adversarial users will write inputs that fool a classifier, so guardrails need layers and monitoring. Confidence can be misleading outside the training distribution. Keep a human path for high-stakes cases, record why decisions were made, and be open with users about automation. This is a young technology: use it where mistakes are cheap and reversible first, measure, and expand carefully.")],
 [("What is a cascade?", ["Cheap model first, escalate when unsure", "A river", "Two equal models", "A tokenizer"], 0, "Staged."),
  ("Why log every decision?", ["It becomes evaluation data", "It wastes space", "It is required to run", "It speeds things"], 0, "Feedback."),
  ("Why serve locally?", ["Keep private text in your network", "It is always cheaper", "It needs no maintenance", "It is more accurate"], 0, "Privacy."),
  ("What is distribution shift?", ["Inputs change over time", "Models shrink", "Labels vanish", "Temperature rises"], 0, "Monitor."),
  ("When should humans decide?", ["High-stakes or uncertain cases", "Never", "Every case always", "Only trivia"], 0, "Responsibility."),
  ("What does a guardrail do?", ["Enforce policy on inputs or outputs", "Train models", "Compress files", "Index words"], 0, "Checks.")],
 [("THRESHOLD", "escalation bar"), ("log(request, p, result)", "feedback loop")],
 [MATCH("Match the system part", "Pair each part with its job.", [("Router", "send requests to the right path"), ("Guardrail", "enforce policy"), ("Cascade", "cheap model first"), ("Escalation", "hand uncertain cases up"), ("Monitoring", "catch drift")]),
  PL("Cascade outcome", "Write cascade(confidence, threshold, small_cost, big_cost): return [path, cost]: path is 'small' with cost small_cost if confidence >= threshold, else 'big' with cost small_cost + big_cost.", "cascade(confidence, threshold, small_cost, big_cost)", '''
def cascade(confidence, threshold, small_cost, big_cost):
    if confidence >= threshold:
        return ['small', small_cost]
    return ['big', round(small_cost + big_cost, 6)]
''', [[0.95, 0.9, 0.0001, 0.01], [0.5, 0.9, 0.0001, 0.01], [0.9, 0.9, 1, 2]], "Escalation still paid for the first try.", approx=0.0001),
  PL("Average cascade cost", "Write avg_cost(confidences, threshold, small_cost, big_cost): the mean cost over all requests using the cascade rule; rounded to 5 decimals.", "avg_cost(confidences, threshold, small_cost, big_cost)", '''
def avg_cost(confidences, threshold, small_cost, big_cost):
    t = 0.0
    for c in confidences:
        t = t + small_cost + (0 if c >= threshold else big_cost)
    return round(t / len(confidences), 5)
''', [[[0.95, 0.99, 0.5, 0.97], 0.9, 0.0001, 0.01], [[0.1], 0.5, 1, 3], [[1.0, 1.0], 0.5, 0.5, 9]], "Mix the paths.", approx=0.00002),
  PL("Route a ticket", "Write route_ticket(probs, options, threshold, human_option): return the top option if its probability is at least threshold, else human_option.", "route_ticket(probs, options, threshold, human_option)", '''
def route_ticket(probs, options, threshold, human_option):
    b = 0
    for i in range(len(probs)):
        if probs[i] > probs[b]:
            b = i
    return options[b] if probs[b] >= threshold else human_option
''', [[[0.7, 0.2, 0.1], ['billing', 'tech', 'sales'], 0.6, 'human'], [[0.4, 0.35, 0.25], ['billing', 'tech', 'sales'], 0.6, 'human'], [[1.0], ['x'], 0.9, 'h']], "Fallback to a person."),
  PL("Guardrail check", "Write allowed(label, p, blocked, threshold): False if label is in the blocked list and p is at least threshold, else True.", "allowed(label, p, blocked, threshold)", '''
def allowed(label, p, blocked, threshold):
    return not (label in blocked and p >= threshold)
''', [['spam', 0.9, ['spam', 'abuse'], 0.8], ['spam', 0.5, ['spam'], 0.8], ['news', 0.99, ['spam'], 0.5]], "Block only when sure."),
  PL("Drift check", "Write drifted(old_acc, new_acc, tolerance): True if new_acc is lower than old_acc by more than tolerance.", "drifted(old_acc, new_acc, tolerance)", '''
def drifted(old_acc, new_acc, tolerance):
    return (old_acc - new_acc) > tolerance + 1e-12
''', [[0.95, 0.85, 0.05], [0.95, 0.93, 0.05], [0.9, 0.85, 0.05]], "Monitor live accuracy."),
  PL("Break-even share", "Write break_even(small_cost, big_cost): the minimum share of requests the small model must handle alone for a cascade to cost no more than always calling the big model; share = small_cost / big_cost, rounded to 4 decimals, capped at 1.", "break_even(small_cost, big_cost)", '''
def break_even(small_cost, big_cost):
    return round(min(1.0, small_cost / float(big_cost)), 4)
''', [[0.0001, 0.01], [0.5, 0.25], [0.002, 0.01]], "Everyone pays for the small model, so the savings must exceed it.", approx=0.0002)]
))
