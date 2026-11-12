# -*- coding: utf-8 -*-
"""Original SVG figures for the meta-learning for compositionality course. Numbers on the results figures come from Lake and Baroni (2023)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from make_images import Svg, BG, PANEL, LINE, TX, DIM, VIO, PINK, BLUE, GRN, AMB, RED  # noqa: E402

COL = {"R": "#ff6b6b", "G": "#76b900", "B": "#4fa8ff", "Y": "#e3b341"}


def dots(s, x, y, letters, r=11, gap=6):
    for i, c in enumerate(letters):
        s.add('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (x + i * (2 * r + gap) + r, y, r, COL[c]))
    return x + len(letters) * (2 * r + gap)


def f_compose():
    s = Svg(640, 300, "Known parts, new combinations", "Words like skip, walk and jump combine with modifiers like twice and backwards. A person who knows the parts can understand every combination, even ones never seen.")
    s.text(320, 24, "Systematic generalization: known parts, new combinations", 14.5, VIO, weight="700")
    rows = ["skip", "walk", "jump"]; cols = ["", "twice", "backwards", "twice backwards"]
    s.text(40, 62, "", 12, DIM)
    for j, c in enumerate(cols):
        s.text(150 + j * 135, 62, c or "(alone)", 12.5, DIM, weight="600")
    seen = {(0, 0), (1, 0), (2, 0), (1, 1), (1, 2), (2, 0), (2, 1)}
    for i, r in enumerate(rows):
        s.text(38, 104 + i * 62, r, 14, TX, anchor="start", weight="700")
        for j in range(4):
            x = 92 + j * 135; y = 80 + i * 62
            was = (i, j) in {(0, 0), (1, 0), (2, 0), (1, 1), (1, 2), (2, 1)}
            s.rect(x, y, 116, 46, fill=PANEL, stroke=GRN if was else PINK, r=9, dash=None if was else "5 4")
            s.text(x + 58, y + 28, (r + (" " + cols[j] if cols[j] else "")), 10.5, TX)
    s.rect(70, 270, 14, 14, fill=PANEL, stroke=GRN, r=3); s.text(92, 282, "seen while learning", 12, DIM, anchor="start")
    s.rect(300, 270, 14, 14, fill=PANEL, stroke=PINK, r=3, dash="4 3"); s.text(322, 282, "never seen: can you still use it?", 12, DIM, anchor="start")
    return s


def f_language():
    s = Svg(640, 330, "The pseudolanguage", "Four made-up words stand for coloured circles. Three function words transform them: fep repeats three times, blicket sandwiches, kiki swaps the order.")
    s.text(320, 24, "A tiny made-up language", 15, VIO, weight="700")
    s.text(24, 56, "Words for colours", 13, DIM, anchor="start", weight="700")
    for i, (w, c) in enumerate([("dax", "R"), ("wif", "G"), ("lug", "B"), ("zup", "Y")]):
        x = 24 + i * 150
        s.rect(x, 66, 130, 42, fill=PANEL, stroke=LINE, r=9); s.text(x + 40, 93, w, 14, TX, weight="700")
        s.add('<circle cx="%s" cy="87" r="12" fill="%s"/>' % (x + 100, COL[c]))
    s.text(24, 142, "Words that act on other words", 13, DIM, anchor="start", weight="700")
    rows = [("x fep", "repeat three times", "R", "RRR"), ("x blicket y", "x, then y, then x", "RG", "RGR"), ("x kiki y", "swap: y first, then x", "RG", "GR")]
    for i, (a, b, inp, out) in enumerate(rows):
        y = 154 + i * 52
        s.rect(24, y, 150, 40, fill=PANEL, stroke=VIO, r=9); s.text(99, y + 25, a, 14, TX, weight="700")
        s.text(190, y + 25, b, 12.5, DIM, anchor="start")
        s.text(372, y + 25, "e.g.", 12, DIM)
        dots(s, 392, y + 20, inp, r=9, gap=4); s.arrow(442, y + 20, 476, y + 20, DIM, sw=1.4)
        dots(s, 486, y + 20, out, r=9, gap=4)
    s.text(320, 322, "These words and meanings are our own illustration in the spirit of the paper's task.", 11, DIM)
    return s


def f_parse():
    s = Svg(640, 300, "Reading a sentence", "The sentence lug fep kiki wif is read in parts: lug fep gives three blue circles, wif gives one green, and kiki puts the second part first.")
    s.text(320, 24, "Read it in pieces: lug fep kiki wif", 15, VIO, weight="700")
    toks = [("lug", 70), ("fep", 150), ("kiki", 250), ("wif", 350)]
    for w, x in toks:
        s.rect(x - 32, 50, 64, 34, fill=PANEL, stroke=LINE, r=8); s.text(x, 73, w, 14, TX, weight="700")
    s.line(70, 92, 150, 92, BLUE, 2); s.text(110, 108, "part A", 11.5, BLUE)
    s.line(318, 92, 382, 92, GRN, 2); s.text(350, 108, "part B", 11.5, GRN)
    s.rect(50, 128, 120, 40, fill=PANEL, stroke=BLUE, r=9); dots(s, 66, 148, "BBB", r=9, gap=4); s.text(110, 184, "lug fep = three blue", 11, DIM)
    s.rect(330, 128, 60, 40, fill=PANEL, stroke=GRN, r=9); dots(s, 349, 148, "G", r=9, gap=4); s.text(360, 184, "wif = green", 11, DIM)
    s.arrow(110, 192, 250, 224, VIO); s.arrow(360, 192, 280, 224, VIO)
    s.rect(200, 226, 200, 48, fill=PANEL, stroke=VIO, r=10); dots(s, 222, 250, "GBBB", r=9, gap=5)
    s.text(300, 292, "kiki: the second part comes first", 12, AMB)
    return s


def f_experiment():
    s = Svg(640, 300, "The few-shot experiment", "People study 14 instructions with answers, then answer 10 new ones. 80.7 percent of their answers matched the rule, and 72.5 percent were right on answers longer than any studied.")
    s.text(320, 24, "Study 14, then answer 10", 15, VIO, weight="700")
    s.rect(30, 44, 250, 118, fill=PANEL, stroke=BLUE, r=10); s.text(155, 66, "Study (answers shown)", 13, TX, weight="700")
    for i, (a, o) in enumerate([("dax", "R"), ("lug fep", "BBB"), ("wif blicket zup", "GYG")]):
        s.text(48, 94 + i * 20, a, 12, DIM, anchor="start"); dots(s, 190, 90 + i * 20, o, r=6, gap=3)
    s.text(155, 146, "... 14 in all", 11.5, DIM)
    s.arrow(284, 100, 340, 100, DIM)
    s.rect(344, 44, 266, 110, fill=PANEL, stroke=PINK, r=10); s.text(477, 66, "Query (you answer)", 13, TX, weight="700")
    for i, a in enumerate(["zup fep kiki dax", "lug blicket wif fep", "... 10 in all"]):
        s.text(362, 94 + i * 20, a, 12, DIM, anchor="start")
    for j, (lab, v, c) in enumerate([("matched the rule", 80.7, VIO), ("right on longer outputs", 72.5, PINK)]):
        y = 190 + j * 46
        s.text(30, y + 18, lab, 12.5, TX, anchor="start"); s.rect(220, y, 380, 26, fill=PANEL, stroke=LINE, r=6)
        s.rect(220, y, 380 * v / 100.0, 26, fill=c, stroke=c, r=6); s.text(220 + 380 * v / 100.0 - 8, y + 18, "%.1f%%" % v, 12.5, BG, anchor="end", weight="700")
    return s


def f_biases():
    s = Svg(640, 300, "Three habits of the mind", "People guess unseen words in three ways: one word to one output item, items written in the order heard, and a different answer for every different word.")
    s.text(320, 24, "Three built-in habits when guessing", 15, VIO, weight="700")
    cards = [("One to one", "each word makes its own piece", "wif zup", "GY", PINK), ("Iconic order", "pieces in the order heard", "a F b", "a b", BLUE), ("Mutual exclusivity", "different words, different answers", "F1 vs F2", "≠", GRN)]
    for i, (t, sub, ex, res, c) in enumerate(cards):
        x = 20 + i * 205
        s.rect(x, 44, 190, 230, fill=PANEL, stroke=c, r=12)
        s.text(x + 95, 72, t, 14, TX, weight="700"); s.text(x + 95, 94, sub, 11.5, DIM)
        s.text(x + 95, 150, ex, 15, TX, weight="600"); s.arrow(x + 95, 160, x + 95, 196, c)
        if i == 0:
            dots(s, x + 70, 222, "GY", r=11, gap=4)
        elif i == 1:
            s.text(x + 95, 228, "a  b", 17, TX, weight="700")
        else:
            s.text(x + 95, 228, "different outputs", 13, TX, weight="700")
    return s


def f_openended():
    s = Svg(640, 280, "Open-ended results", "In the open-ended task 93.1 percent of people gave a unique answer to each instruction, 79.3 percent used iconic concatenation, 62.1 percent used one-to-one mappings and 58.6 percent used all three.")
    s.text(320, 24, "Guessing with no examples: how many people used each habit", 14.5, VIO, weight="700")
    for j, (lab, v, c) in enumerate([("Mutual exclusivity", 93.1, GRN), ("Iconic concatenation", 79.3, BLUE), ("One to one", 62.1, PINK), ("All three at once", 58.6, VIO)]):
        y = 48 + j * 54
        s.text(30, y + 20, lab, 13, TX, anchor="start"); s.rect(220, y, 380, 30, fill=PANEL, stroke=LINE, r=6)
        s.rect(220, y, 380 * v / 100.0, 30, fill=c, stroke=c, r=6); s.text(220 + 380 * v / 100.0 - 8, y + 21, "%.1f%%" % v, 13, BG, anchor="end", weight="700")
    return s


def f_seq2seq():
    s = Svg(640, 300, "Encoder-decoder network", "A transformer encoder reads the study examples together with the query. The decoder then writes the answer one symbol at a time. Weights are frozen at test time.")
    s.text(320, 24, "A standard encoder-decoder transformer", 15, VIO, weight="700")
    s.rect(20, 50, 210, 190, fill=PANEL, stroke=BLUE, r=12); s.text(125, 72, "Encoder", 14, BLUE, weight="700")
    s.rect(34, 86, 182, 34, fill=BG, stroke=LINE, r=7); s.text(125, 108, "study examples", 12, DIM)
    s.rect(34, 126, 182, 34, fill=BG, stroke=PINK, r=7); s.text(125, 148, "query to answer", 12, TX)
    s.text(125, 186, "all in one input", 11.5, DIM); s.text(125, 206, "3 layers, about 1.4M weights", 11, DIM)
    s.arrow(232, 145, 300, 145, DIM)
    s.rect(304, 50, 150, 190, fill=PANEL, stroke=VIO, r=12); s.text(379, 72, "Decoder", 14, VIO, weight="700")
    s.text(379, 130, "writes the", 12, DIM); s.text(379, 148, "answer one", 12, DIM); s.text(379, 166, "symbol at a time", 12, DIM)
    s.arrow(456, 145, 500, 145, DIM)
    s.rect(504, 100, 116, 90, fill=PANEL, stroke=GRN, r=12); s.text(562, 128, "output", 13, TX, weight="700"); dots(s, 520, 160, "GBB", r=8, gap=3)
    s.text(320, 270, "No special symbolic parts. The magic is in how it is trained.", 12.5, AMB)
    return s


def f_streams():
    s = Svg(640, 300, "Standard and meta training", "Standard training shows one fixed task many times. Meta training shows a stream of episodes where the meanings of the words keep changing.")
    s.text(320, 24, "Standard training vs a stream of episodes", 15, VIO, weight="700")
    s.rect(20, 44, 290, 220, fill=PANEL, stroke=LINE, r=12); s.text(165, 66, "Standard: one fixed world", 13, TX, weight="700")
    for i in range(3):
        y = 84 + i * 56
        s.rect(40, y, 250, 42, fill=BG, stroke=LINE, r=8); s.text(56, y + 26, "dax fep", 12.5, DIM, anchor="start"); s.text(138, y + 26, "→", 14, DIM); dots(s, 164, y + 21, "RRR", r=8, gap=3)
    s.text(165, 256, "same meaning every time", 11.5, DIM)
    s.rect(330, 44, 290, 220, fill=PANEL, stroke=VIO, r=12); s.text(475, 66, "Meta: a new world each episode", 13, TX, weight="700")
    for i, (w, o) in enumerate([("dax fep", "RRR"), ("dax fep", "GGG"), ("dax fep", "BBB")]):
        y = 84 + i * 56
        s.rect(350, y, 250, 42, fill=BG, stroke=VIO, r=8); s.text(362, y + 18, "episode %d" % (i + 1), 10.5, DIM, anchor="start")
        s.text(366, y + 36, w, 12.5, TX, anchor="start"); s.text(448, y + 36, "→", 14, DIM); dots(s, 474, y + 29, o, r=8, gap=3)
    s.text(475, 256, "the network must work it out from the examples", 11.5, DIM)
    return s


def f_episode():
    s = Svg(640, 320, "Anatomy of an episode", "Each episode has a few study examples and a query. The target answer follows the rule 80 percent of the time and a human-like guess 20 percent of the time.")
    s.text(320, 24, "One training episode", 15, VIO, weight="700")
    s.rect(20, 44, 380, 150, fill=PANEL, stroke=BLUE, r=12); s.text(210, 66, "Study examples (a fresh meaning for each word)", 12.5, TX, weight="700")
    for i, (a, o) in enumerate([("zup", "B"), ("lug", "Y"), ("lug fep", "YYY"), ("zup blicket lug", "BYB")]):
        s.text(40, 94 + i * 22, a, 12.5, DIM, anchor="start"); s.text(190, 94 + i * 22, "→", 13, DIM); dots(s, 210, 89 + i * 22, o, r=7, gap=3)
    s.arrow(404, 120, 440, 120, DIM)
    s.rect(444, 44, 176, 150, fill=PANEL, stroke=PINK, r=12); s.text(532, 66, "Query", 13, TX, weight="700"); s.text(532, 98, "zup fep kiki lug", 12.5, DIM)
    s.text(532, 130, "target answer:", 11.5, DIM); dots(s, 484, 156, "YBBB", r=7, gap=3)
    s.rect(20, 214, 600, 80, fill=PANEL, stroke=VIO, r=12)
    s.text(320, 238, "How the target is chosen", 12.5, TX, weight="700")
    s.rect(40, 252, 360, 24, fill=VIO, stroke=VIO, r=6); s.text(220, 269, "80%: strict algebraic answer", 12, BG, weight="700")
    s.rect(400, 252, 180, 24, fill=PINK, stroke=PINK, r=6); s.text(490, 269, "20%: human-like guess", 12, BG, weight="700")
    return s


def f_results():
    s = Svg(640, 300, "People and MLC compared", "On exact rule following, people scored 80.7 percent and MLC 82.4. On longer outputs, people 72.5 and MLC 77.8. A basic sequence-to-sequence model scored zero on the few-shot task.")
    s.text(320, 24, "People and the MLC network behave alike", 15, VIO, weight="700")
    groups = [("Follows the rule", [("People", 80.7, BLUE), ("MLC", 82.4, VIO), ("Basic seq2seq", 0, RED)]), ("Right on longer outputs", [("People", 72.5, BLUE), ("MLC", 77.8, VIO)])]
    x0 = 40
    for g, (title, bars_) in enumerate(groups):
        base = 250; gx = x0 + g * 310
        s.text(gx + 110, 54, title, 12.5, TX, weight="700")
        for i, (n, v, c) in enumerate(bars_):
            bx = gx + i * 76; h = v * 1.6
            s.rect(bx, base - max(h, 2), 56, max(h, 2), fill=c, stroke=c, r=5, sw=1)
            s.text(bx + 28, base - h - 8, "%.1f" % v, 12, TX, weight="700"); s.text(bx + 28, base + 16, n, 11, DIM)
    s.line(30, 250, 620, 250, LINE, 1.2)
    return s


def f_scan():
    s = Svg(640, 320, "SCAN and COGS errors", "On SCAN add jump the error rate fell from 99.27 percent for a basic model to 0.22 percent for MLC. On COGS lexical generalization it fell from 6.08 to 0.87 percent. Failures remain on length and structure splits.")
    s.text(320, 24, "Benchmarks: lower error is better (exact match)", 14.5, VIO, weight="700")
    s.text(30, 52, "SCAN: \"jump twice\" → JUMP JUMP", 12.5, DIM, anchor="start")
    rows = [("SCAN add jump", 99.27, 0.22), ("SCAN around right", 51.13, 0.04), ("SCAN opposite right", 100.0, 0.06), ("COGS lexical", 6.08, 0.87)]
    for i, (n, a, b) in enumerate(rows):
        y = 70 + i * 54
        s.text(30, y + 20, n, 12.5, TX, anchor="start")
        s.rect(200, y, 330, 16, fill=PANEL, stroke=LINE, r=4); s.rect(200, y, max(4, 330 * a / 100.0), 16, fill=RED, stroke=RED, r=4); s.text(536, y + 13, "%.2f%% basic" % a, 10.5, DIM, anchor="start")
        s.rect(200, y + 20, 330, 16, fill=PANEL, stroke=LINE, r=4); s.rect(200, y + 20, max(3, 330 * b / 100.0), 16, fill=VIO, stroke=VIO, r=4); s.text(536, y + 33, "%.2f%% MLC" % b, 10.5, DIM, anchor="start")
    s.text(320, 300, "Still unsolved: the SCAN length split and three COGS structure splits (100% error).", 11.5, AMB)
    return s


def f_limits():
    s = Svg(640, 260, "What MLC does and does not do", "MLC handles new combinations of known words in the kinds of episodes it trained on. It does not yet handle entirely new structures, new symbols, or full natural language.")
    s.text(320, 24, "Strengths and limits", 15, VIO, weight="700")
    s.rect(20, 44, 290, 190, fill=PANEL, stroke=GRN, r=12); s.text(165, 68, "Does", 14, GRN, weight="700")
    for i, t in enumerate(["New combinations of known words", "Learns human-like habits from data", "Works with a plain transformer", "Strong on lexical benchmarks"]):
        s.text(36, 100 + i * 30, "✓ " + t, 12.5, TX, anchor="start")
    s.rect(330, 44, 290, 190, fill=PANEL, stroke=RED, r=12); s.text(475, 68, "Does not yet", 14, RED, weight="700")
    for i, t in enumerate(["Entirely new structures", "Emit new symbols (needs pointers)", "Beat length and productivity splits", "Prove it works on full language"]):
        s.text(346, 100 + i * 30, "✗ " + t, 12.5, TX, anchor="start")
    return s


ALL = {
 "mlc-compose.svg": f_compose, "mlc-language.svg": f_language, "mlc-parse.svg": f_parse, "mlc-experiment.svg": f_experiment, "mlc-biases.svg": f_biases,
 "mlc-openended.svg": f_openended, "mlc-seq2seq.svg": f_seq2seq, "mlc-streams.svg": f_streams, "mlc-episode.svg": f_episode, "mlc-results.svg": f_results,
 "mlc-scan.svg": f_scan, "mlc-limits.svg": f_limits,
}


def build_all(outdir="/tmp/mlc_figs"):
    os.makedirs(outdir, exist_ok=True)
    res = {}
    for fn, f in ALL.items():
        svg = f().render()
        open(os.path.join(outdir, fn), "w", encoding="utf-8").write(svg)
        res[fn] = svg
    return res


if __name__ == "__main__":
    print(len(build_all()), "figures")
