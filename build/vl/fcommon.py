# -*- coding: utf-8 -*-
"""Drawing helpers for the Verilog course figures: gates, waveforms, flip-flops, transistors."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from make_images import Svg, BG, PANEL, LINE, TX, DIM, VIO, PINK, BLUE, GRN, AMB, RED  # noqa: E402,F401


def head(s, t):
    s.text(s.w / 2, 26, t, 15, VIO, weight="700")


def circ(s, x, y, r, fill="none", stroke=LINE, sw=1.5):
    s.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (x, y, r, fill, stroke, sw))


def path(s, d, stroke=LINE, sw=1.5, fill="none", dash=None, arrow=False):
    s.add('<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"%s%s/>' % (d, fill, stroke, sw, ' stroke-dasharray="%s"' % dash if dash else "", ' marker-end="url(#ah)"' if arrow else ""))


def gate(s, kind, x, y, color=BLUE, w=56, h=40, label=None):
    """draw a logic gate with its input side at x. kind: and or xor not buf nand nor xnor. returns ((x_in, y1), (x_in, y2), (x_out, y_mid))"""
    m = y + h / 2; bub = kind in ("nand", "nor", "xnor", "not")
    k = kind.replace("n", "", 1) if kind in ("nand", "nor") else kind
    xe = x + w - (8 if bub else 0)
    if kind in ("and", "nand"):
        path(s, "M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f L%.1f %.1f Z" % (x, y, x + w * 0.45, y, h / 2, h / 2, x + w * 0.45, y + h, x, y + h), color, 2, PANEL)
    elif kind in ("or", "nor", "xor", "xnor"):
        d = "M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" % (x, y, x + w * 0.55, y, xe, m, x + w * 0.55, y + h, x, y + h, x + w * 0.22, m, x, y)
        path(s, d, color, 2, PANEL)
        if kind in ("xor", "xnor"):
            path(s, "M%.1f %.1f Q%.1f %.1f %.1f %.1f" % (x - 7, y, x + w * 0.15, m, x - 7, y + h), color, 2)
    elif kind in ("not", "buf"):
        path(s, "M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (x, y, xe, m, x, y + h), color, 2, PANEL)
    if bub:
        circ(s, xe + 4, m, 4, PANEL, color, 2)
    if label:
        s.text(x + w * 0.4, m + 4, label, 11, TX)
    ins = [(x - (7 if kind in ("xor", "xnor") else 0), y + h * 0.3), (x - (7 if kind in ("xor", "xnor") else 0), y + h * 0.7)] if kind not in ("not", "buf") else [(x, m), (x, m)]
    return ins[0], ins[1], (x + w, m)


def wire(s, pts, color=DIM, sw=1.6, dot=None):
    path(s, "M" + " L".join("%.1f %.1f" % p for p in pts), color, sw)
    for d in (dot or []):
        circ(s, d[0], d[1], 3, color, color)


def wave(s, x0, y0, w, bits, name, color=GRN, h=22, lab=True, labx=None):
    """digital waveform: bits is a string like '0011' (one char per slot) or list; x/z allowed"""
    n = len(bits); tw = w / n
    if lab:
        s.text(x0 - 8 if labx is None else labx, y0 + h / 2 + 4, name, 12, TX, anchor="end")
    pts = []
    prev = None
    for i, b in enumerate(bits):
        xa, xb = x0 + i * tw, x0 + (i + 1) * tw
        yv = y0 if b == "1" else (y0 + h if b == "0" else y0 + h / 2)
        col = color if b in "01" else RED
        if prev is not None and prev != yv:
            s.line(xa, prev, xa, yv, col, 2)
        s.line(xa, yv, xb, yv, col, 2)
        prev = yv


def busw(s, x0, y0, w, vals, name, color=AMB, h=22, edges=None):
    """bus waveform: vals is list of (start_fraction_slot_index, text) segments across n slots; edges: list of slot indices where value changes"""
    s.text(x0 - 8, y0 + h / 2 + 4, name, 12, TX, anchor="end")
    for (xa, xb, t) in vals:
        path(s, "M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (xa + 3, y0 + h / 2, xa + 7, y0, xb - 7, y0, xb - 3, y0 + h / 2, xb - 7, y0 + h, xa + 7, y0 + h), color, 1.8)
        s.text((xa + xb) / 2, y0 + h / 2 + 4, t, 11, TX)


def dff(s, x, y, w=70, h=64, color=VIO, label="D flip-flop", clk=True):
    s.rect(x, y, w, h, PANEL, color, 8, 2)
    s.text(x + 14, y + 22, "D", 12, TX); s.text(x + w - 12, y + 22, "Q", 12, TX)
    if clk:
        path(s, "M%.1f %.1f L%.1f %.1f L%.1f %.1f" % (x, y + h - 22, x + 11, y + h - 14, x, y + h - 6), color, 1.8)
    if label:
        s.text(x + w / 2, y + h + 14, label, 10.5, DIM)
    return {"d": (x, y + 18), "q": (x + w, y + 18), "clk": (x, y + h - 14)}


def mos(s, x, y, kind="n", color=BLUE, h=56, label=None, on=None):
    """a transistor symbol: drain at top, source at bottom, gate on the left. x,y: top-left of gate bar. kind n or p"""
    s.line(x + 14, y + 6, x + 14, y + h - 6, color, 3)           # channel bar
    s.line(x + 14, y + 10, x + 38, y + 10, color, 2); s.line(x + 38, y + 10, x + 38, y - 6, color, 2)       # drain
    s.line(x + 14, y + h - 10, x + 38, y + h - 10, color, 2); s.line(x + 38, y + h - 10, x + 38, y + h + 6, color, 2)  # source
    s.line(x + 7, y + 6, x + 7, y + h - 6, color, 2); s.line(x - 14, y + h / 2, x + 7, y + h / 2, color, 2)   # gate plate + lead
    if kind == "p":
        circ(s, x + 1, y + h / 2, 4, PANEL, color, 2)
    if label:
        s.text(x + 52, y + h / 2 + 4, label, 11, DIM, anchor="start")
    return {"g": (x - 14, y + h / 2), "d": (x + 38, y - 6), "s": (x + 38, y + h + 6)}


def vdd(s, x, y, w=40, label="VDD"):
    s.line(x - w / 2, y, x + w / 2, y, AMB, 3); s.text(x, y - 6, label, 11, AMB)


def gnd(s, x, y, w=40):
    s.line(x - w / 2, y, x + w / 2, y, DIM, 3); s.line(x - w / 3, y + 5, x + w / 3, y + 5, DIM, 2); s.line(x - w / 6, y + 10, x + w / 6, y + 10, DIM, 2)
