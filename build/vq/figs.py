# -*- coding: utf-8 -*-
"""Vectiq course figures: three generic layouts (flow, layers, columns) plus an XP bar chart."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from make_images import Svg, BG, PANEL, LINE, TX, DIM, VIO, PINK, BLUE, GRN, AMB, RED  # noqa: E402,F401
COL = {"v": VIO, "p": PINK, "b": BLUE, "g": GRN, "a": AMB, "r": RED}


def flow(title, desc, steps, note, per=3):
    rows = (len(steps) + per - 1) // per
    s = Svg(700, 70 + rows * 100 + 30, title, desc)
    s.text(350, 28, title, 15, VIO, weight="700")
    for i, (t, sub, c) in enumerate(steps):
        r, k = divmod(i, per)
        x = 20 + k * 230; y = 50 + r * 100
        s.box(x, y, 200, 62, t, sub, COL[c])
        if k < per - 1 and i + 1 < len(steps):
            s.arrow(x + 200, y + 31, x + 230, y + 31, DIM)
        elif k == per - 1 and i + 1 < len(steps):
            s.line(x + 100, y + 62, x + 100, y + 80, DIM, 1.6); s.line(x + 100, y + 80, 120, y + 80, DIM, 1.6); s.arrow(120, y + 80, 120, y + 100, DIM)
    s.text(350, 70 + rows * 100 + 14, note, 11.5, DIM)
    return s


def layers(title, desc, rows, note):
    s = Svg(700, 70 + len(rows) * 66 + 20, title, desc)
    s.text(350, 28, title, 15, VIO, weight="700")
    for i, (t, sub, c) in enumerate(rows):
        y = 48 + i * 66
        s.box(30, y, 640, 52, t, sub, COL[c])
        if i + 1 < len(rows):
            s.arrow(350, y + 52, 350, y + 66, DIM)
    s.text(350, 48 + len(rows) * 66 + 8, note, 11.5, DIM)
    return s


def columns(title, desc, left, right, lt, rt, note):
    n = max(len(left), len(right))
    s = Svg(700, 90 + n * 56 + 20, title, desc)
    s.text(350, 28, title, 15, VIO, weight="700")
    s.text(175, 56, lt, 13, BLUE, weight="700"); s.text(525, 56, rt, 13, GRN, weight="700")
    for i, (t, sub) in enumerate(left):
        s.box(20, 68 + i * 56, 320, 46, t, sub, BLUE)
    for i, (t, sub) in enumerate(right):
        s.box(360, 68 + i * 56, 320, 46, t, sub, GRN)
    s.text(350, 90 + n * 56 + 4, note, 11.5, DIM)
    return s


def xpbars():
    s = Svg(700, 330, "XP needed per level", "Bars showing the total XP needed to reach levels 1 to 10 on the MEE6 curve.")
    s.text(350, 28, "The level curve: total XP to reach each level", 15, VIO, weight="700")
    vals = [sum(5 * n * n + 50 * n + 100 for n in range(l)) for l in range(1, 11)]
    mx = vals[-1]
    for i, v in enumerate(vals):
        h = 220 * v / mx; x = 40 + i * 63
        s.rect(x, 280 - h, 44, h, PANEL, [BLUE, GRN, AMB][i % 3], 4, 1.5)
        s.text(x + 22, 274 - h, str(v), 11, TX)
        s.text(x + 22, 298, "L%d" % (i + 1), 11, DIM)
    s.text(350, 320, "Each level costs a little more than the one before. Level 10 needs 3720 XP in total.", 11.5, DIM)
    return s


ALL = {}


def reg(name, f):
    ALL[name] = f


def build_all():
    return {n: f().render() for n, f in ALL.items()}
