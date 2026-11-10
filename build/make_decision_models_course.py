#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Decision Models course. Usage: python3 make_decision_models_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "dm"))
import cmk, dm_a, dm_b, make_apps  # noqa: E402
make_apps.main()
CHS = dm_a.CHS + dm_b.CHS
PRONOUNCE = {"ModernBERT": "modern bert", "BERT": "bert", "Laya": "lie uh", "Clef": "clef", "Jev": "jev", "Kev": "kev", "TypeSafe": "type safe", "Qwen": "chwen", "BANKING77": "banking seventy seven",
    "RLCD": "R L C D", "NLI": "N L I", "ECE": "E C E", "Brier": "bry er", "Kahneman": "kah nuh man", "FlashAttention": "flash attention", "Unsloth": "un sloth", "Ollama": "oh lah ma",
    "softmax": "soft max", "logits": "low jits", "prefill": "pre fill", "KV": "K V", "LLM": "L L M", "calibration": "cal ih bray shun", "cascade": "cass kade"}
SANDBOX = cmk.terminal("Decision model cheat sheet", "dm>", "A scripted lookup. Try: types, laya, clef, softmax, temperature, ece, brier, threshold, cascade, eval", [
    ("types", ["Boolean: P(yes). Choice: distribution over options. Score: number on a scale."]),
    ("laya", ["Reported: ModernBERT-based, about 421M parameters. Input, then each option followed by a mask token. Head scores each mask, softmax across options. Verify details."]),
    ("clef", ["Reported: Qwen-based decoder, about 9B and 27B. Prefill only, no generation. Joint schema head. Verify details."]),
    ("softmax", ["p_i = exp(z_i) / sum exp(z_j). Subtract the maximum for stability."]),
    ("temperature", ["p = softmax(z / T). T above 1 flattens, below 1 sharpens. Fit T on a validation set."]),
    ("ece", ["Bin by confidence. ECE = sum (n_bin/n) |accuracy - confidence|."]),
    ("brier", ["Mean (p - y)^2."]),
    ("threshold", ["Act above the high bar, review in the middle, reject below. Choose from your cost matrix."]),
    ("cascade", ["Small model first. Escalate if confidence is below the threshold. Everyone pays the small cost."]),
    ("eval", ["Own labelled test set, baseline, big-LLM reference, per-class errors, calibration, latency, cost."]),
])
EXAM = [
 ("What is a decision model?", ["A small model answering typed questions with probabilities", "A text generator", "An image model", "A database"], 0, "One pass."),
 ("What is System One?", ["Fast one-pass judgement", "Slow reasoning", "A language", "A cache"], 0, "Intuition."),
 ("What are the three typed question kinds?", ["Boolean, choice, score", "Text, image, sound", "Read, write, run", "Short, long, medium"], 0, "Answer shapes."),
 ("What does a classification head do?", ["Maps a vector to label scores", "Generates text", "Tokenises", "Stores memory"], 0, "Linear layer."),
 ("How does zero-shot NLI classification work?", ["Tests each label as a hypothesis", "Retrains each time", "Counts words", "Sorts labels"], 0, "Entailment."),
 ("What does ModernBERT add over BERT?", ["Long context and modern components", "Fewer layers", "Image input", "Text generation"], 0, "8,192 tokens."),
 ("What follows each option in a Laya-style prompt?", ["A mask token", "A comma", "A number", "Nothing"], 0, "One slot per option."),
 ("What turns mask scores into probabilities?", ["Softmax across options", "Sorting", "Sampling text", "Hashing"], 0, "Normalise."),
 ("What does temperature above 1 do?", ["Flattens probabilities", "Sharpens them", "Adds options", "Removes options"], 0, "Less confident."),
 ("What does a prefill-only decision model skip?", ["Token generation", "Reading the prompt", "Heads", "Weights"], 0, "No writing."),
 ("What does a pointer head choose?", ["An item from the input", "A word from nowhere", "A colour", "A file"], 0, "Points."),
 ("What does a KV cache reuse?", ["Work on a shared prefix", "The answers", "The labels", "The files"], 0, "Prefix."),
 ("What does a calibrated 80 percent mean?", ["About 80 percent are right", "80 tokens", "80 options", "80 ms"], 0, "Frequency."),
 ("What does ECE measure?", ["Gaps between confidence and accuracy", "Latency", "Size", "Loss only"], 0, "Binned."),
 ("What does log loss punish?", ["Confident mistakes", "Short answers", "Slow answers", "Rare words"], 0, "Heavy penalty."),
 ("Does temperature scaling change which option is top?", ["No", "Yes", "Only for scores", "Only for text"], 0, "Same argmax."),
 ("Where should the temperature be fitted?", ["On validation data", "On the test set", "Nowhere", "On the training set only"], 0, "Held out."),
 ("What is the first step in evaluating a vendor model?", ["Build your own test set", "Read the leaderboard", "Buy a license", "Rename labels"], 0, "Own data."),
 ("What is contamination?", ["Test data in training", "Dirty input", "A slow model", "A long prompt"], 0, "Inflated scores."),
 ("Why a cost matrix?", ["Errors cost different amounts", "Faster training", "Smaller models", "Better tokens"], 0, "Thresholds."),
 ("What is a cascade?", ["Fast model first, escalate if unsure", "Two equal models", "A tokenizer", "A cache"], 0, "Staged."),
 ("Why log every decision?", ["It becomes test data", "To waste space", "To slow serving", "No reason"], 0, "Feedback."),
 ("Why serve an open model locally?", ["Keep private text in your network", "It is always cheaper", "It never needs upkeep", "It is always better"], 0, "Privacy."),
 ("What is distribution shift?", ["Inputs change over time", "The model grows", "Labels vanish", "The GPU heats"], 0, "Monitor."),
 ("Who decides high-stakes cases?", ["Humans, with model help", "Nobody", "Only the model", "A random draw"], 0, "Responsibility."),
 ("How should vendor numbers be quoted?", ["As reported, with a date", "As proof", "Never", "As laws"], 0, "Self-reported."),
]
CFG = dict(id="decision-models", title="Decision Models and Generalised Classifiers",
    subtitle="From BERT-style classifiers to the new System One decision models: typed questions, calibration, evaluation and routing, with Python labs",
    description="A hands-on introduction to generalised classifiers and the new category of decision models, also called System One models. Learn how classifiers, encoders and ModernBERT work; zero-shot and embedding classification; the typed-question interface of boolean, choice and score answers; the masked-option encoder design reported for Laya; the prefill-only decoder design reported for Clef, with joint and pointer heads and KV-cache reuse; calibration with temperature scaling, ECE, Brier score and log loss; evaluation on your own data; and routing, cascades, guardrails and escalation in real systems. The field is only weeks old, so vendor figures are marked as reported and the course stresses durable concepts. Every chapter has Python labs verified in the built-in interpreter, plus a decision playground and a calibration lab.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="dm", apps={"__DECIDE__": "decide.html", "__CALIB__": "calib.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "decision-models.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
