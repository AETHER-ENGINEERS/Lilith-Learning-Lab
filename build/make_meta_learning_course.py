#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Meta-Learning for Compositionality course (an educational retelling of Lake and Baroni, Nature 2023, CC BY 4.0).
Usage: python3 make_meta_learning_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mlc"))
import cmk, mlc_a, mlc_b, figs, maps as mmaps  # noqa: E402
from clib import T  # noqa: E402

CHS = mlc_a.CHS + mlc_b.CHS
KEEP_PY = {"Count the phrases", "Three rules", "Read a sentence", "Exact match rate", "A one-to-one guess", "A memoriser", "Rename the words", "Pack the input", "Pick the target", "Log-likelihood", "Tiny SCAN", "Error rate"}
for _c in CHS:
    _c["practice"] = [x for x in _c["practice"] if x["type"] != "python" or x["title"] in KEEP_PY]

def _app(name, title, intro, h):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": open(os.path.join(HERE, "mlc", "apps", name), encoding="utf-8").read()}
CHS[2]["practice"].insert(0, _app("mlc_game.html", "Learn the alien language", "A fresh made-up language each time. Study the examples, then answer the questions by tapping colours. Notice which habits you use when you are unsure.", 1500))
CHS[5]["practice"].insert(0, _app("mlc_episodes.html", "Episode stream and rule finder", "See how the meanings change in every episode, then watch a rule finder rule out the impossible meanings one example at a time.", 1200))

FIG = lambda name, cap: {"type": "figure", "image": name, "caption": cap}
INS = [
 ("Why systematicity", "The grid in the figure", "mlc-compose.svg", "Known parts in new combinations. Green boxes were seen, dashed boxes were not."),
 ("A tiny language", "The figure below lists", "mlc-language.svg", "Our tiny pseudolanguage: four colour words and three function words."),
 ("A tiny language", "Sentences are read in pieces", "mlc-parse.svg", "Reading lug fep kiki wif in pieces."),
 ("How people learn", "The figure shows the results", "mlc-experiment.svg", "The few-shot experiment: study 14, answer 10, and the two headline results."),
 ("Three habits", "The paper highlights three", "mlc-biases.svg", "The three habits: one-to-one, iconic order, mutual exclusivity."),
 ("Three habits", "The figure shows the result", "mlc-openended.svg", "How many people used each habit in the open-ended task."),
 ("Why standard", "The figure shows the setup", "mlc-seq2seq.svg", "The encoder-decoder transformer that reads study examples and the query together."),
 ("Meta-learning", "The figure compares", "mlc-streams.svg", "Standard training sees one world. Meta-training sees a new world each episode."),
 ("The MLC recipe", "All of it goes into", "mlc-episode.svg", "Anatomy of one training episode and how its target is chosen."),
 ("Results", "The figure compares them", "mlc-results.svg", "People, MLC and a basic network on the few-shot task."),
 ("Benchmarks", "The results are striking", "mlc-scan.svg", "Exact-match error rates on SCAN and COGS: basic network against MLC."),
 ("Limits, lessons", "The figure sums it up", "mlc-limits.svg", "What MLC does and does not do yet."),
]
_fig_no = {}
for _t, _p, _f, _cap in INS:
    _ci = [i for i, c in enumerate(CHS) if c["title"].startswith(_t)][0]
    _ch = CHS[_ci]
    _k = [i for i, b in enumerate(_ch["lesson"]) if b["type"] == "text" and b["items"][0].startswith(_p)]
    assert _k, (_t, _p)
    _fig_no[_ci] = _fig_no.get(_ci, 0) + 1
    _num = "%d.%d" % (_ci + 1, _fig_no[_ci])
    _anchor = _ch["lesson"][_k[0]]
    _anchor["items"][-1] = _anchor["items"][-1].rstrip() + " (See Figure %s below.)" % _num
    _ch["lesson"].insert(_k[0] + 1, FIG(_f, "Figure %s. %s" % (_num, _cap)))

assert len(mmaps.MAPS) == len(CHS)
for _c, _ms in zip(CHS, mmaps.MAPS):
    _c["maps"] = [{"title": _t, "links": _l} for _t, _l in _ms]

for _i in range(1, len(CHS)):
    _prev = CHS[_i - 1]
    CHS[_i]["lesson"].insert(0, T("Quick recap of the last chapter, " + _prev["title"] + ":", *["• " + k for k in _prev["keyPoints"]]))

MNEM = [
 ("Known parts, new plans", "Systematic means Known parts in New combinations, like Lego."),
 ("Fep Fills, Blicket Bread, Kiki Kicks", "Fep Fills three copies, Blicket makes a sandwich (bread, filling, bread), Kiki Kicks the order around."),
 ("Fourteen to study, ten to test", "Fourteen to study, ten to test, and about eighty percent right."),
 ("OOO: One, Order, Other", "One piece per word, Order kept, Other words get other answers."),
 ("Encoder Eats, Decoder Dishes", "The Encoder Eats the input and the Decoder Dishes out the answer. Memorisers only know the menu."),
 ("Shuffle, Show, Solve", "Shuffle the meanings, Show a few examples, Solve the query."),
 ("Random, Pack, 80-20", "Draw a Random grammar, Pack the input into one string, then 80 exact and 20 human-like targets."),
 ("Less negative is more human", "Log-likelihood closer to zero means the model finds human answers more likely."),
 ("Words yes, lengths no", "New uses of known Words: yes. New Lengths and shapes: not yet."),
 ("Three S for the future", "Structures, Symbols and Sentences-in-full are still to do."),
]
assert len(MNEM) == len(CHS)
for _c, (_m, _d) in zip(CHS, MNEM):
    _full = _d if _d.startswith(_m) else _m + ". " + _d
    _c["lesson"].append(T("Memory trick: " + _full))
    _c["cards"].append({"q": "Memory trick for: " + _c["title"] + "?", "a": _full})
IMAGES = figs.build_all()

PRONOUNCE = {"Fodor": "foe door", "Pylyshyn": "pie lish in", "Baroni": "ba row nee", "dax": "dacks", "wif": "wiff", "lug": "lug", "zup": "zup", "fep": "fep", "blicket": "blick it", "kiki": "key key",
    "SCAN": "scan", "COGS": "cogs", "seq2seq": "sequence to sequence", "MLC": "M L C", "systematicity": "sis tem at iss ity", "compositionality": "com poz ish on al ity", "Hadamard": "had a mard",
    "transformer": "trans former", "ELI5": "E L I five", "GPT-4": "G P T four", "COGS.": "cogs", "log-likelihood": "log like lee hood", "Adam": "adam", "Nature": "nature", "Zenon": "zee non"}
SANDBOX = cmk.terminal("MLC cheat sheet", "mlc>", "A scripted lookup. Try: paper, systematicity, language, experiment, bias, seq2seq, episode, recipe, results, scan, cogs, limits", [
    ("paper", ["Lake and Baroni, Nature 623, 115-121 (2023). Open access, CC BY 4.0. This course retells it in our own words."]),
    ("systematicity", ["Using known parts in new combinations. Fodor and Pylyshyn (1988) doubted networks could."]),
    ("language", ["Our pseudolanguage: dax R, wif G, lug B, zup Y. fep repeats 3 times. blicket: x y x. kiki swaps."]),
    ("experiment", ["14 study examples, 10 queries. 80.7 percent matched the rule. 72.5 percent right on longer outputs."]),
    ("bias", ["One-to-one, iconic concatenation, mutual exclusivity. 58.6 percent of people used all three."]),
    ("seq2seq", ["A basic sequence-to-sequence network scored 0 percent on the few-shot task. MLC uses a plain transformer."]),
    ("episode", ["Study examples plus a query, from a random grammar. Word meanings change every episode."]),
    ("recipe", ["Random grammars, one packed input, 80 percent algebraic and 20 percent human-like targets, plain transformer."]),
    ("results", ["MLC sampled: 82.4 percent systematic (people 80.7). Longer outputs: 77.8 (people 72.5). Basic seq2seq: 0."]),
    ("scan", ["Commands to actions. Add jump error: 99.27 percent basic, 0.22 percent MLC."]),
    ("cogs", ["Sentences to logical forms. Lexical error: 6.08 percent basic, 0.87 percent MLC."]),
    ("limits", ["Fails SCAN length and three COGS structure splits. Cannot emit new symbols without a pointer mechanism."]),
])
EXAM = [
 ("Systematic generalization means:", ["Using known parts in new combinations", "Memorising phrases", "Typing quickly", "Random guessing"], 0, "Lego pieces."),
 ("Who argued in 1988 that networks lack systematicity?", ["Fodor and Pylyshyn", "Lake and Baroni", "Turing", "Hinton"], 0, "The old challenge."),
 ("What is MLC?", ["Meta-learning for compositionality", "A memory chip", "A language", "A game"], 0, "The paper's method."),
 ("In our language, what does fep do?", ["Repeats three times", "Swaps order", "Sandwiches", "Deletes"], 0, "x x x."),
 ("What does blicket do?", ["Makes x then y then x", "Swaps order", "Repeats", "Deletes"], 0, "A sandwich."),
 ("What does kiki do?", ["Swaps the order", "Repeats", "Sandwiches", "Ends the sentence"], 0, "Second part first."),
 ("What is an interpretation grammar?", ["Rules that give each sentence its answer", "A dictionary of colours", "A neural network", "A score"], 0, "A recipe for meaning."),
 ("How many study examples did people get?", ["14", "2", "100", "1"], 0, "Few-shot."),
 ("How often did people match the rule in the few-shot task?", ["80.7 percent", "10 percent", "50 percent", "100 percent"], 0, "Strong, not perfect."),
 ("What is an inductive bias?", ["A built-in guessing preference", "A bug", "A dataset", "A chip"], 0, "From inside the learner."),
 ("What is mutual exclusivity?", ["Different instructions get different answers", "All answers equal", "One word only", "No guessing"], 0, "Different words, different meanings."),
 ("What did a basic seq2seq network score on the few-shot task?", ["0 percent", "80 percent", "100 percent", "50 percent"], 0, "It never sees new meanings."),
 ("What does an encoder do?", ["Reads the input", "Writes the output", "Stores weights", "Draws"], 0, "Reads everything first."),
 ("What is an episode?", ["A small task with study examples and a query", "A TV show", "A weight", "A file"], 0, "A mini task."),
 ("Why shuffle word meanings per episode?", ["So the network must infer them", "To save memory", "To confuse people", "No reason"], 0, "No memorising."),
 ("What happens to the weights at test time?", ["They are frozen", "They are retrained", "They are deleted", "They double"], 0, "No task-specific updates."),
 ("How often is the target the exact algebraic answer?", ["80 percent", "20 percent", "100 percent", "0 percent"], 0, "The rest are human-like."),
 ("Is rule machinery added to the MLC network?", ["No, it is a plain transformer", "Yes, a grammar engine", "Yes, a database", "Yes, a calculator"], 0, "The training does the work."),
 ("How did sampled MLC compare with people on rule following?", ["82.4 against 80.7 percent", "20 against 80 percent", "Far worse", "Identical to a coin"], 0, "Close match."),
 ("What does a higher log-likelihood mean?", ["The model finds the human answers more likely", "A slower model", "More noise", "A worse model"], 0, "Closer to zero."),
 ("What does SCAN translate?", ["Commands into actions", "Pictures into text", "Music into notes", "Code into binary"], 0, "jump twice to JUMP JUMP."),
 ("What was MLC's error on SCAN add jump?", ["0.22 percent", "99.27 percent", "50 percent", "100 percent"], 0, "Basic was 99.27."),
 ("Which tests does MLC still fail?", ["SCAN length and some COGS structure splits", "All tests", "No tests", "Only spelling"], 0, "100 percent error remains."),
 ("What would new symbols need?", ["A pointer mechanism", "More layers", "A bigger screen", "Nothing"], 0, "Copying unseen words."),
 ("What is the big lesson?", ["A new kind of practice can change what a network understands", "Networks are magic", "Rules never help", "People are slow"], 0, "Training matters."),
]
CFG = dict(id="meta-learning-compositionality", title="Meta-Learning for Compositionality",
    subtitle="An intuitive walk through Lake and Baroni's Nature paper on how a plain neural network can learn to combine known parts in new ways",
    description="An intuitive, step-by-step retelling of the open-access Nature paper Human-like systematic generalization through a meta-learning neural network by Brenden Lake and Marco Baroni (Nature 623, 115-121, 2023, CC BY 4.0). Learn what systematic generalization is, play a made-up colour language, meet the three human habits the paper measures, see why ordinary networks stumble, and follow the meta-learning for compositionality (MLC) recipe, its results and its limits, with numbered figures, recaps, memory tricks, concept maps and short Python labs. The examples and words in this course are our own illustrations in the spirit of the paper, and this course is not affiliated with or endorsed by the authors or the journal.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, images=IMAGES)
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "meta-learning-compositionality.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
