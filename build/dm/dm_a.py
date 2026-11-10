# -*- coding: utf-8 -*-
"""Decision models course, part 1: classifiers, encoders, typed questions, Laya-style heads."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "From classifiers to decision models",
 ("Decision models", [
  "Classifier | maps | Text to label",
  "Decision model | answers | A typed question",
  "System one | is | Fast and one pass",
  "System two | is | Slow reasoning",
  "Probabilities | express | Confidence",
  "Router | picks | Cheap or costly path",
  "Escalation | handles | Uncertain cases"]),
 ["A classifier reads input and picks a label. A decision model is the newer idea of a small model that answers a typed question about some input, such as yes or no, one of these options, or a score from 0 to 1, in a single forward pass and with calibrated probabilities.",
  "The pitch is a split of labour. Fast System One models make the many routine decisions cheaply, and slow System Two models, the large reasoning LLMs, handle what is hard or uncertain. The idea is new, so products and numbers change quickly and vendor claims need checking.",
  "This course starts with the durable concepts: encoders, calibration, evaluation and routing. Vendor details are marked as reported as of late 2026."],
 [("Classifier", "A model mapping an input to one of a fixed set of labels."),
  ("Decision model", "A compact model that answers a typed question about an input in one pass and returns a calibrated probability or score."),
  ("System one", "Fast, automatic judgement, borrowed from psychology to describe one-pass models."),
  ("System two", "Slow, deliberate reasoning, here meaning large reasoning models that think step by step."),
  ("Calibration", "Agreement between stated confidence and how often the answer is right.")],
 ["Typed answer: yes/no, choice, score.",
  "One forward pass, no chain of thought.",
  "Probabilities must be calibrated.",
  "Route easy cases here, hard cases to an LLM.",
  "Treat vendor numbers as claims to verify."],
 [T("Many software decisions are small. Is this message spam? Is this ticket about billing or shipping? Does this answer follow the policy? Which of five tools should the agent call? Asking a large language model each time works, but it is slow, costs money, and its text answers must be parsed and can wander. For years, teams trained small classifiers for each such question, which are fast but rigid: every new question needed new labelled data."),
  T("Decision models try to combine the two. You pass the input and a typed question: a yes or no question, a choice among options, or a score. The model answers in one forward pass, producing probabilities rather than prose. The label comes from the math, not from generating text, so latency is a few milliseconds to tens of milliseconds, the answer type is guaranteed, and the confidence can be used to decide what to do next."),
  T("The framing comes from Kahneman's System One and System Two. System One is quick intuition. System Two is slow reasoning. In the architecture proposed, a System One decision model handles the high-volume routine calls and passes the uncertain ones up to a reasoning model. Vendors in this area, from late 2026, include Jev from TypeSafe, the open Laya built on ModernBERT, and Clef, built on a Qwen language model by a large infrastructure provider. These are weeks old; treat their reported figures as marketing until you test them on your data."),
  C("# the shape of the idea (pseudocode)\nanswer = decision_model.ask(\n    input='My card was charged twice',\n    question={'type': 'choice',\n              'options': ['billing', 'shipping', 'account']},\n)\nprint(answer.probs)   # e.g. {'billing': 0.93, 'shipping': 0.04, 'account': 0.03}\nif max(answer.probs.values()) < 0.8:\n    answer = big_llm(input)   # escalate the uncertain case", "python"),
  T("The course has four parts. First the building blocks: encoder models such as ModernBERT, and how a generalised classifier works. Then the typed-question interface and two architectures, a masked-token encoder design and a prefill-only decoder design. Then calibration, evaluation and how to build your own test. Last, putting decision models into systems with routing, thresholds, guardrails and cost maths. Each chapter has labs in plain Python that implement the key calculations.")],
 [("What does a decision model return?", ["A typed answer with probabilities", "Free-form essays", "Images", "Source code"], 0, "One pass."),
  ("What is System One here?", ["Fast one-pass judgement", "Slow reasoning", "A database", "A compiler"], 0, "Intuition."),
  ("Why avoid parsing text answers?", ["Output types are guaranteed by the model head", "Text is illegal", "It is too short", "It is encrypted"], 0, "Typed."),
  ("What should be escalated to a big LLM?", ["Uncertain or hard cases", "Every case", "Only easy cases", "Nothing"], 0, "Low confidence."),
  ("How should vendor benchmark figures be treated?", ["As claims to verify on your data", "As proven", "As secret", "As irrelevant forever"], 0, "Self-reported."),
  ("What is calibration?", ["Confidence matches accuracy", "Training speed", "Model size", "Token count"], 0, "Reliable probabilities.")],
 [("ask(input, question)", "typed query"), ("max(probs) < threshold", "escalate")],
 [MATCH("Match the term", "Pair each idea with its meaning.", [("System one", "fast one-pass judgement"), ("System two", "slow step-by-step reasoning"), ("Typed question", "yes/no, choice or score"), ("Calibration", "confidence matches accuracy"), ("Escalation", "send uncertain cases upward")]),
  PL("Softmax to answer", "Write decide(options, logits): softmax the logits and return [best option, its probability rounded to 3 decimals] (first option on ties).", "decide(options, logits)", '''
import math
def decide(options, logits):
    m = max(logits)
    e = [math.exp(v - m) for v in logits]
    t = sum(e)
    p = [v / t for v in e]
    b = 0
    for i in range(len(p)):
        if p[i] > p[b] + 1e-12:
            b = i
    return [options[b], round(p[b], 3)]
''', [[['billing', 'shipping', 'account'], [3, 1, 0]], [['yes', 'no'], [0, 0]], [['a', 'b'], [-1, 2]]], "Largest probability wins.", approx=None),
  PL("Escalate or answer", "Write route(probs, threshold): return 'answer' if the largest probability is at least threshold, else 'escalate'.", "route(probs, threshold)", '''
def route(probs, threshold):
    return 'answer' if max(probs) >= threshold else 'escalate'
''', [[[0.9, 0.1], 0.8], [[0.5, 0.5], 0.8], [[0.8, 0.2], 0.8]], "Compare confidence to the bar."),
  PL("Share handled cheaply", "Write handled_share(confidences, threshold): the fraction of confidences at or above threshold, rounded to 3 decimals.", "handled_share(confidences, threshold)", '''
def handled_share(confidences, threshold):
    n = len([c for c in confidences if c >= threshold])
    return round(n / float(len(confidences)), 3)
''', [[[0.9, 0.95, 0.6, 0.99], 0.9], [[0.5, 0.4], 0.9], [[1.0], 0.5]], "How many stay on the fast path?", approx=0.002),
  PL("Expected cost", "Write expected_cost(share_fast, cost_fast, cost_slow): the average cost per request when share_fast of requests cost cost_fast and the rest, plus the fast attempt, cost cost_slow in addition (every request first pays cost_fast). Round to 4 decimals.", "expected_cost(share_fast, cost_fast, cost_slow)", '''
def expected_cost(share_fast, cost_fast, cost_slow):
    return round(cost_fast + (1 - share_fast) * cost_slow, 4)
''', [[0.8, 0.0001, 0.01], [1.0, 0.0002, 0.05], [0.0, 0.001, 0.02]], "Everyone pays for the fast model.", approx=0.00005),
  PL("Argmax with abstain", "Write answer_or_none(options, probs, threshold): the option with the highest probability if that probability is at least threshold, else None.", "answer_or_none(options, probs, threshold)", '''
def answer_or_none(options, probs, threshold):
    b = 0
    for i in range(len(probs)):
        if probs[i] > probs[b]:
            b = i
    return options[b] if probs[b] >= threshold else None
''', [[['a', 'b'], [0.7, 0.3], 0.6], [['a', 'b'], [0.55, 0.45], 0.6], [['x'], [1.0], 0.9]], "Abstain when unsure.")]
))

CHS.append(CH(
 "Encoders and generalised classifiers: from BERT to ModernBERT",
 ("Encoders", [
  "Encoder | reads | Whole text both ways",
  "Classification head | maps | Vector to label",
  "NLI | frames | Entailment",
  "Zero-shot | uses | Label descriptions",
  "Embedding | feeds | Nearest neighbour",
  "Cross-encoder | scores | Pair together",
  "ModernBERT | modernises | The encoder"]),
 ["Encoders turn text into contextual vectors. A small head on top turns a vector into a label. Fine-tuned on a few thousand examples, this is the classic classifier and still the efficient choice for many tasks.",
  "Generalised classifiers avoid retraining per label set: zero-shot natural language inference frames each label as a hypothesis to test, embedding models match text to label descriptions, and cross-encoders score a text and a candidate together.",
  "ModernBERT, released at the end of 2024, updates the BERT encoder with rotary positions, alternating local and global attention, unpadding, FlashAttention and an eight-thousand-token context. It is the base on which Laya is reported to be built."],
 [("Encoder", "A transformer that reads the whole input with attention in both directions and outputs a vector for every token."),
  ("Classification head", "A small layer on top of an encoder that maps a vector to label scores."),
  ("Zero-shot classification", "Choosing among labels never seen in training, usually by testing each label as an entailment hypothesis."),
  ("Cross-encoder", "A model that reads a text and a candidate together and outputs a relevance or match score."),
  ("ModernBERT", "A 2024 update of BERT with longer context and faster, more modern components.")],
 ["Encoder + head = classifier.",
  "NLI zero-shot: premise = text, hypothesis = 'This is about X'.",
  "Bi-encoder is fast, cross-encoder is accurate.",
  "ModernBERT: long context, RoPE, FlashAttention.",
  "Fine-tuning needs hundreds to thousands of labels."],
 [T("An encoder reads all of a text at once. Every token can attend to every other, left and right, so the vector for each token is informed by the whole sentence. Put a head on the vector for the first token or on the average of all tokens, a linear layer producing one score per label, and train on labelled examples with cross-entropy loss. That is a fine-tuned classifier. At a few hundred million parameters it runs in milliseconds on a modest GPU or a CPU, and for fixed label sets it remains hard to beat on cost."),
  T("Its weakness is the fixed label set. Generalised classifiers address that. The zero-shot trick uses a model trained on natural language inference, which decides whether a premise entails a hypothesis. To classify 'My card was charged twice' you ask, for each candidate label, whether the text entails 'This message is about billing', 'about shipping' and so on, and compare the entailment scores. An embedding model offers another route: encode the text and the label descriptions separately and pick the nearest. A cross-encoder reads text and label together, slower but sharper."),
  C("from transformers import pipeline\nclf = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')\nout = clf('My card was charged twice',\n          candidate_labels=['billing', 'shipping', 'account'])\nprint(out['labels'], out['scores'])", "python"),
  T("BERT dates from 2018, and the field learned much since. ModernBERT, published by Answer.AI and LightOn at the end of 2024, brings the encoder up to date: rotary position embeddings, alternating local and global attention layers for efficiency, removal of padding tokens, FlashAttention kernels, a vocabulary trained on code as well as text, and a context of 8,192 tokens instead of 512."),
  T("It comes in a base size near 150 million parameters and a large size near 400 million. It is faster than older encoders, and its long context matters for classifying documents."),
  T("Why does this matter for decision models? A decision model needs to read an input, understand a question and options, and produce calibrated scores. An encoder reads everything both ways in one pass and is small, so it is a natural base. The next chapters show how option markers and typed heads turn an encoder into a general decision maker, and how the same idea carries over to decoder models.")],
 [("What does an encoder read?", ["The whole input in both directions", "Only the left side", "Only the last token", "Only labels"], 0, "Bidirectional."),
  ("What is added to make a classifier?", ["A head on the vector", "A decoder", "A new tokenizer", "Sound"], 0, "Linear layer."),
  ("How does NLI zero-shot work?", ["Test each label as a hypothesis", "Retrain on the fly", "Guess randomly", "Count words"], 0, "Entailment."),
  ("Why is a cross-encoder slower than a bi-encoder?", ["It reads each pair together", "It is bigger by law", "It cannot batch", "It uses images"], 0, "No precomputed vectors."),
  ("What context length does ModernBERT support?", ["8,192 tokens", "512 only", "50", "One sentence"], 0, "Long context."),
  ("When is a fine-tuned encoder a good choice?", ["Fixed labels, high volume, low latency", "Open-ended writing", "Image generation", "Long reasoning"], 0, "Cheap and fast.")],
 [("pipeline('zero-shot-classification')", "NLI zero-shot"), ("AutoModelForSequenceClassification", "encoder plus head")],
 [MATCH("Match the term", "Pair each classifier idea with its meaning.", [("Head", "maps a vector to labels"), ("NLI", "does the premise entail the hypothesis"), ("Bi-encoder", "embed separately then compare"), ("Cross-encoder", "read the pair together"), ("ModernBERT", "updated long-context encoder")]),
  PL("Hypotheses for zero-shot", "Write hypotheses(labels, template): replace '{}' in the template with each label; return the list of hypothesis strings.", "hypotheses(labels, template)", '''
def hypotheses(labels, template):
    return [template.replace('{}', l) for l in labels]
''', [[['billing', 'shipping'], 'This message is about {}.'], [['a'], '{} is true'], [[], 'x {}']], "One hypothesis per label."),
  PL("Pick by entailment", "Write zero_shot(labels, entail_scores): the label with the highest entailment score (first on ties); return [label, score].", "zero_shot(labels, entail_scores)", '''
def zero_shot(labels, entail_scores):
    b = 0
    for i in range(len(labels)):
        if entail_scores[i] > entail_scores[b]:
            b = i
    return [labels[b], entail_scores[b]]
''', [[['billing', 'shipping'], [0.8, 0.1]], [['a', 'b', 'c'], [0.2, 0.2, 0.1]], [['x'], [0.5]]], "Highest wins."),
  PL("Multi-label threshold", "Write multi_label(labels, scores, threshold): all labels whose score is at least threshold, in order.", "multi_label(labels, scores, threshold)", '''
def multi_label(labels, scores, threshold):
    return [labels[i] for i in range(len(labels)) if scores[i] >= threshold]
''', [[['a', 'b', 'c'], [0.9, 0.4, 0.7], 0.5], [['x'], [0.1], 0.5], [['p', 'q'], [0.5, 0.5], 0.5]], "Independent yes/no per label."),
  PL("Mean pooling", "Write mean_pool(vectors, mask): the average of the vectors where mask is 1, rounded to 3 decimals.", "mean_pool(vectors, mask)", '''
def mean_pool(vectors, mask):
    dim = len(vectors[0])
    acc = [0.0] * dim
    n = 0
    for v, m in zip(vectors, mask):
        if m == 1:
            n = n + 1
            for j in range(dim):
                acc[j] = acc[j] + v[j]
    return [round(a / n, 3) for a in acc]
''', [[[[1, 2], [3, 4], [9, 9]], [1, 1, 0]], [[[2, 2]], [1]], [[[0, 1], [2, 3]], [0, 1]]], "Ignore padding.", approx=None),
  PL("Linear head", "Write head(vector, W, b): scores for each class = W row dot vector + bias; return the list rounded to 3 decimals.", "head(vector, W, b)", '''
def head(vector, W, b):
    out = []
    for i in range(len(W)):
        out.append(round(sum([W[i][j] * vector[j] for j in range(len(vector))]) + b[i], 3))
    return out
''', [[[1, 2], [[1, 0], [0, 1], [1, 1]], [0, 0, 0.5]], [[0, 0], [[1, 1]], [2]], [[3], [[2], [-1]], [0, 1]]], "One row per class.", approx=None),
  PL("Cross-entropy loss", "Write cross_entropy(probs, target_index): negative natural log of the probability of the true class, rounded to 4 decimals.", "cross_entropy(probs, target_index)", '''
import math
def cross_entropy(probs, target_index):
    return round(-math.log(probs[target_index]), 4)
''', [[[0.7, 0.2, 0.1], 0], [[0.7, 0.2, 0.1], 2], [[0.5, 0.5], 1]], "Training loss for a classifier.", approx=0.0005)]
))

CHS.append(CH(
 "The typed-question interface",
 ("Typed questions", [
  "Question type | defines | Output shape",
  "Yes or no | gives | One probability",
  "Choice | gives | A distribution",
  "Score | gives | A number",
  "Criteria | state | What to judge",
  "State | adds | Context",
  "Schema | constrains | Valid answers"]),
 ["A decision model is queried with a structured request: the input, a context or state, optional criteria, and a typed question. The type fixes the output: a probability for yes or no, a distribution over options for a choice, or a bounded score.",
  "Because the answer comes from a head rather than generated text, it is always well formed. The caller sets the policy: thresholds, how to treat low confidence and when to escalate.",
  "Good questions are specific, mutually exclusive and checkable. Designing the question and options is the main job of the person using a decision model."],
 [("Typed question", "A request whose answer type is fixed in advance: boolean, one of several options, or a numeric score."),
  ("Criteria", "A short statement of the rules or standards the decision should follow."),
  ("State", "Extra context passed with the input, such as user history or the current step of a workflow."),
  ("Option set", "The list of allowed answers for a choice question."),
  ("Abstention", "Declining to answer, or flagging low confidence, instead of forcing a choice.")],
 ["Boolean: P(yes).",
  "Choice: probabilities sum to 1.",
  "Score: a value in a range, such as 0 to 1.",
  "Put hard rules in criteria, not in hope.",
  "Options should not overlap."],
 [T("Think of a decision model as a function with a strict signature. You give it an input, perhaps a state, perhaps criteria, and a question. Vendors differ in names. A reported API from this field uses three question types: a yes or no kind, a choice among options, and a score. Whatever the names, the pattern is the same, and it is worth learning because it determines what you can build."),
  T("A boolean question yields one probability that the answer is yes. Is this email a phishing attempt? Does this reply violate the refund policy? "),
  T("A choice question yields a distribution over listed options that sums to one: which department should handle this ticket? A score question yields a number in a range: how urgent is this, from zero to one? All three produce numbers, not prose, so your code can compare them with thresholds, log them, and plot them."),
  C("# a typed request, as plain data\nrequest = {\n    'input': 'The customer says the parcel never arrived and wants money back.',\n    'state': {'order_age_days': 12, 'tier': 'gold'},\n    'criteria': 'Refunds over 100 dollars need a human.',\n    'question': {'type': 'choice',\n                 'options': ['refund', 'reship', 'escalate', 'reply']},\n}\nvalid = request['question']['type'] in ('boolean', 'choice', 'score')", "python"),
  T("Question design matters more than people expect. Options should be mutually exclusive and cover the cases, with an 'other' or 'escalate' option for the rest. Criteria should state rules plainly. State, such as order age or earlier steps, lets the model use context it cannot see in the text. Ask one thing at a time: 'Is this urgent and about billing?' is two questions. A score needs an anchored scale, so say what 0 and 1 mean."),
  T("Then you decide what to do with the answer, and that policy belongs to you, not to the model. Typical policies: act automatically above a high threshold, escalate in a grey zone, and reject or defer below. Different mistakes cost different amounts, so thresholds should be set from your own data, as a later chapter shows. Keep a log of questions, probabilities and outcomes; it is your evaluation set for tomorrow.")],
 [("What shape does a choice answer have?", ["A distribution over options", "A paragraph", "A picture", "A file"], 0, "Sums to one."),
  ("What does a boolean question return?", ["P(yes)", "A list of words", "A table", "Nothing"], 0, "One probability."),
  ("What is state for?", ["Context outside the text", "Styling", "Speed", "Billing"], 0, "Extra facts."),
  ("Why should options be mutually exclusive?", ["Overlap makes probabilities ambiguous", "It saves money", "It shortens text", "It is a law"], 0, "Clean choices."),
  ("Who sets the thresholds?", ["The caller, from their own data", "The vendor only", "Nobody", "The user"], 0, "Policy."),
  ("What should a score question define?", ["What the ends of the scale mean", "The font", "The author", "The date"], 0, "Anchors.")],
 [("{'type':'choice','options':[...]}", "choice question"), ("P(yes) >= 0.9", "act automatically")],
 [APP("DECIDE", "Decision playground", "Type a message, pick a question and options, and see probabilities from a toy bag-of-words scorer. Change the temperature and the escalation threshold and watch which cases are answered, escalated or rejected. Try three different messages to complete the lab.", 820),
  MATCH("Match the question type", "Pair each type with its output.", [("Boolean", "one probability of yes"), ("Choice", "distribution over options"), ("Score", "number on a scale"), ("Criteria", "rules to follow"), ("State", "context besides the text")]),
  PL("Validate a request", "Write valid(question): True if question['type'] is 'boolean', or 'choice' with at least two distinct options, or 'score' with lo < hi; else False. Questions are dicts with keys type and options or lo and hi.", "valid(question)", '''
def valid(question):
    t = question.get('type')
    if t == 'boolean':
        return True
    if t == 'choice':
        o = question.get('options', [])
        return len(set(o)) >= 2 and len(set(o)) == len(o)
    if t == 'score':
        return question.get('lo', 0) < question.get('hi', 0)
    return False
''', [[{'type': 'boolean'}], [{'type': 'choice', 'options': ['a', 'b']}], [{'type': 'choice', 'options': ['a', 'a']}], [{'type': 'score', 'lo': 0, 'hi': 1}], [{'type': 'score', 'lo': 1, 'hi': 1}], [{'type': 'essay'}]], "Check each type's requirements."),
  PL("Normalise a choice", "Write normalise(scores): divide non-negative scores by their sum so they total 1, rounded to 3 decimals; if the sum is 0 return equal shares.", "normalise(scores)", '''
def normalise(scores):
    t = float(sum(scores))
    if t == 0:
        return [round(1.0 / len(scores), 3)] * len(scores)
    return [round(s / t, 3) for s in scores]
''', [[[2, 1, 1]], [[0, 0]], [[5]]], "Make a distribution.", approx=None),
  PL("Rescale a score", "Write rescale(p, lo, hi): map a probability p in [0, 1] to the range lo..hi, rounded to 3 decimals.", "rescale(p, lo, hi)", '''
def rescale(p, lo, hi):
    return round(lo + p * (hi - lo), 3)
''', [[0.5, 0, 10], [1.0, 1, 5], [0.25, -1, 1]], "Linear map.", approx=0.002),
  PL("Policy bands", "Write policy(p, act, reject): 'act' if p >= act, 'reject' if p <= reject, otherwise 'review'.", "policy(p, act, reject)", '''
def policy(p, act, reject):
    if p >= act:
        return 'act'
    if p <= reject:
        return 'reject'
    return 'review'
''', [[0.95, 0.9, 0.1], [0.05, 0.9, 0.1], [0.5, 0.9, 0.1], [0.9, 0.9, 0.1]], "Three outcomes, two thresholds."),
  PL("Entropy of an answer", "Write entropy(probs): the Shannon entropy in bits of a distribution, rounded to 3 decimals; ignore zero probabilities.", "entropy(probs)", '''
import math
def entropy(probs):
    return round(-sum([p * math.log(p, 2) for p in probs if p > 0]), 3)
''', [[[0.5, 0.5]], [[1.0, 0.0]], [[0.25, 0.25, 0.25, 0.25]], [[0.9, 0.1]]], "High entropy means unsure.", approx=0.002)]
))

CHS.append(CH(
 "Masked-option encoder designs (the Laya pattern)",
 ("Laya pattern", [
  "Input | holds | Text and options",
  "Option marker | is | A mask slot",
  "Encoder | reads | All together",
  "Head | scores | Each marker",
  "Softmax | normalises | Across options",
  "Temperature | softens | Probabilities",
  "Fine-tuning | adapts | To your domain"]),
 ["One design for a decision model puts the input and the options into a single encoder prompt, each option followed by a mask token. After one pass, the vector at each mask is scored by a small head, and a softmax across the masks gives the option probabilities.",
  "Laya is reported to follow this pattern on a ModernBERT base of about 421 million parameters, offered openly. Details come from vendor material and may change; the pattern is what matters.",
  "Such a design is fast and small but limited by the encoder's context, its pretraining and the amount of adaptation. Specialised domains usually need fine-tuning."],
 [("Option marker", "A mask token placed after each candidate option so the encoder produces one vector per option."),
  ("Joint encoding", "Reading the input and all options together so each option's vector is informed by the others."),
  ("Scoring head", "A small layer that turns each option vector into a score."),
  ("Temperature scaling", "Dividing logits by a constant before softmax to soften or sharpen probabilities."),
  ("Fine-tuning", "Further training on your own labelled decisions.")],
 ["[input] option A [MASK] option B [MASK] ...",
  "score_i = head(vector at mask i).",
  "p = softmax(scores / T).",
  "Reported: ModernBERT base, 421M parameters.",
  "Fine-tune for domain-specific decisions."],
 [T("Here is one way to build a decision model out of an encoder, described in material about Laya, an open decision model reported to be based on ModernBERT. Write the input, then each option, and after each option put a special mask token. Feed the whole string to the encoder. Because attention runs both ways, the vector at each mask token has seen the input and all the other options. A tiny head scores each of those vectors, and a softmax across the options gives probabilities."),
  C("# the idea, in pseudocode\ntext = 'Customer: my card was charged twice'\noptions = ['billing', 'shipping', 'account']\nprompt = text + ' [SEP] ' + ' '.join(o + ' [MASK]' for o in options)\nhidden = encoder(prompt)                 # one forward pass\nscores = [head(hidden[i]) for i in mask_positions]\nprobs = softmax([s / temperature for s in scores])", "python"),
  T("The attractions are plain. It is one forward pass over a few hundred tokens, so on suitable hardware it takes milliseconds. The model is small enough to run on your own machine, which helps with privacy and cost. The options are inputs, not fixed outputs, so you can change them per request without retraining. The training task, predicting which option is right, matches pretraining on masked tokens, so the encoder transfers well."),
  T("The limits are also plain. The encoder's context bounds the length of input plus options, so the 8,192 tokens of ModernBERT are a ceiling. Tasks needing multi-step reasoning, arithmetic, or deep world knowledge are not a good fit; the model is deciding, not thinking. Off-the-shelf quality on your domain is unknown until measured, and the reports say that fine-tuning on a few hundred or thousand of your own labelled examples is often what makes it strong. The reported figures from the vendors should be re-tested."),
  T("Temperature deserves a note. Raw softmax outputs from a neural network are often overconfident. A single number, the temperature, divides the logits before the softmax. Above one it flattens probabilities, below one it sharpens them. You choose it on held-out data to make confidence match accuracy. The calibration chapter makes this precise. Meanwhile, remember that a decision model's probabilities are only useful if they are trustworthy.")],
 [("What follows each option in the prompt?", ["A mask token", "A full stop only", "An image", "A password"], 0, "One slot per option."),
  ("What produces the option probabilities?", ["A softmax over mask scores", "Sampling text", "A parser", "A random draw"], 0, "Across options."),
  ("Why can options change per request?", ["They are inputs, not fixed outputs", "They are ignored", "Models are retrained each time", "They are secret"], 0, "No fixed label set."),
  ("What limits input plus options length?", ["The encoder context window", "The alphabet", "The temperature", "The head"], 0, "Context."),
  ("What does temperature above 1 do?", ["Flattens the probabilities", "Sharpens them", "Removes options", "Adds options"], 0, "Softer."),
  ("What usually makes such a model strong in a niche?", ["Fine-tuning on your own labels", "Bigger prompts", "Deleting options", "Randomness"], 0, "Domain data.")],
 [("text + options + [MASK]", "joint prompt"), ("softmax(scores / T)", "calibrated probabilities")],
 [MATCH("Match the part", "Pair each part of the masked-option design with its job.", [("Mask after option", "gives a vector per option"), ("Encoder", "reads input and options together"), ("Head", "scores each option vector"), ("Softmax", "turns scores into probabilities"), ("Temperature", "softens or sharpens")]),
  PL("Build the masked prompt", "Write build_prompt(text, options): text + ' [SEP] ' + each option followed by ' [MASK]' joined with a single space.", "build_prompt(text, options)", '''
def build_prompt(text, options):
    return text + ' [SEP] ' + ' '.join([o + ' [MASK]' for o in options])
''', [['hello', ['a', 'b']], ['x', ['only']], ['t', []]], "Concatenate with the marker."),
  PL("Mask positions", "Write mask_positions(tokens): the indexes where the token is '[MASK]'.", "mask_positions(tokens)", '''
def mask_positions(tokens):
    return [i for i in range(len(tokens)) if tokens[i] == '[MASK]']
''', [[['a', '[SEP]', 'x', '[MASK]', 'y', '[MASK]']], [['a']], [['[MASK]', '[MASK]']]], "Where to read the scores."),
  PL("Temperature softmax", "Write probs(scores, T): softmax of scores / T rounded to 4 decimals.", "probs(scores, T)", '''
import math
def probs(scores, T):
    s = [v / T for v in scores]
    m = max(s)
    e = [math.exp(v - m) for v in s]
    t = sum(e)
    return [round(v / t, 4) for v in e]
''', [[[2, 1, 0], 1], [[2, 1, 0], 2], [[2, 1, 0], 0.5], [[0, 0, 0], 1]], "The calibration knob.", approx=None),
  PL("Sequence budget", "Write fits(text_tokens, option_tokens, max_len, overhead): True if text_tokens + the sum of option token counts (option_tokens is a list) + 2 per option (separator and mask) + overhead is at most max_len.", "fits(text_tokens, option_tokens, max_len, overhead)", '''
def fits(text_tokens, option_tokens, max_len, overhead):
    total = text_tokens + sum(option_tokens) + 2 * len(option_tokens) + overhead
    return total <= max_len
''', [[500, [3, 4, 5], 8192, 10], [8000, [100, 100], 8192, 10], [10, [], 16, 6]], "Context budgeting."),
  PL("Rank options", "Write rank(options, scores): options sorted by score descending (ties by original order).", "rank(options, scores)", '''
def rank(options, scores):
    idx = sorted(range(len(options)), key=lambda i: (-scores[i], i))
    return [options[i] for i in idx]
''', [[['a', 'b', 'c'], [0.2, 0.7, 0.1]], [['x', 'y'], [1, 1]], [['z'], [0]]], "Sort by score."),
  PL("Margin", "Write margin(probs): the gap between the largest and second largest probability, rounded to 3 decimals (0 if one option).", "margin(probs)", '''
def margin(probs):
    if len(probs) < 2:
        return 0
    s = sorted(probs, reverse=True)
    return round(s[0] - s[1], 3)
''', [[[0.6, 0.3, 0.1]], [[0.5, 0.5]], [[1.0]]], "A close call has a small margin.", approx=0.002)]
))
