# -*- coding: utf-8 -*-
"""Verilog course figures, chapters 1-7."""
from fcommon import *


def flow():
    s = Svg(660, 330, "Digital design flow", "Specification, architecture, RTL in Verilog, simulation, synthesis, place and route, sign-off and fabrication, with a feedback loop from simulation back to RTL.")
    head(s, "From idea to chip: the design flow")
    steps = [("Specification", "what must it do?", BLUE), ("Architecture", "blocks and buses", BLUE), ("RTL in Verilog", "you write this", GRN), ("Simulation", "does it work?", GRN),
             ("Synthesis", "RTL to gates", AMB), ("Place and route", "gates to layout", AMB), ("Sign-off", "timing, power, rules", PINK), ("Fabrication", "silicon", PINK)]
    for i, (t, sub, c) in enumerate(steps):
        x = 24 + (i % 4) * 158; y = 52 + (i // 4) * 130
        s.box(x, y, 132, 62, t, sub, c)
        if i % 4 != 3:
            s.arrow(x + 132, y + 31, x + 158, y + 31, DIM)
    s.line(24 + 3 * 158 + 66, 114, 24 + 3 * 158 + 66, 150, DIM, 1.8); s.line(24 + 3 * 158 + 66, 150, 24 + 66, 150, DIM, 1.8); s.arrow(24 + 66, 150, 24 + 66, 180, DIM)
    s.line(24 + 2 * 158 + 66, 114 + 0, 24 + 2 * 158 + 66, 114, GRN)
    path(s, "M%d 114 L%d 128 L%d 128 L%d 114" % (24 + 3 * 158 + 66 - 160 * 0, 24 + 3 * 158 + 66 - 160 * 0, 24 + 2 * 158 + 66, 24 + 2 * 158 + 66), GRN, 1.5, dash="5 4", arrow=True)
    s.text(330, 312, "The green loop is where beginners live: write, simulate, fix, repeat. This course is the green boxes.", 11.5, DIM)
    return s


def ychart():
    s = Svg(560, 450, "Gajski-Kuhn Y-chart", "Three axes: behavioural, structural and physical domains, crossed by five rings of abstraction from system to circuit.")
    head(s, "The Y-chart: three views, five zoom levels")
    cx, cy = 280, 215; import math
    axes = [("Behavioural", -90 - 120 + 240 - 0, BLUE), ("Structural", 30, GRN), ("Physical", 150, AMB)]
    ang = {"Behavioural": 150 + 60 * 0, "Structural": 30, "Physical": 270}
    ang = {"Behavioural": 210, "Structural": 330, "Physical": 90}
    R = 150
    for k, (nm, a, c) in enumerate([("Behavioural", 150, BLUE), ("Structural", 30, GRN), ("Physical", 90, AMB)]):
        x2 = cx + R * math.cos(math.radians(a)); y2 = cy - R * math.sin(math.radians(a)) if a != 90 else cy + R
        if a == 90: x2, y2 = cx, cy + R
        s.line(cx, cy, x2, y2, c, 3)
        tx = cx + (R + 34) * math.cos(math.radians(a)); ty = (cy - (R + 24) * math.sin(math.radians(a))) if a != 90 else cy + R + 22
        s.text(tx, ty, nm, 13, c, weight="700")
    for i, nm in enumerate(["Circuit", "Logic", "Register transfer (RTL)", "Algorithm", "System"]):
        r = 30 + i * 24
        circ(s, cx, cy, r, "none", LINE, 1.2)
        s.text(cx + 4, cy - r + 11, "", 9, DIM)
    labs = [("Circuit", 30), ("Logic", 54), ("RTL", 78), ("Algorithm", 102), ("System", 126)]
    for nm, r in labs:
        s.text(cx + 8, cy - r - 2, nm, 10, DIM, anchor="start")
    ex = {"Behavioural": ["equations", "Verilog behaviour", "state diagram", "spec"], "Structural": ["transistors", "gates", "registers + ALU", "CPU + memory"], "Physical": ["polygons", "cell layout", "floorplan", "chip"]}
    s.text(30, 60, "Verilog lives here:", 12, GRN, anchor="start"); s.text(30, 78, "RTL ring, structural + behavioural axes", 11, DIM, anchor="start")
    s.text(280, 440, "Design = moving inward and between axes: behaviour to structure to geometry.", 11.5, DIM)
    return s


def styles():
    s = Svg(640, 300, "Design styles", "FPGA, gate array, standard cell and full custom compared by speed, density, cost per unit at low volume and design effort.")
    head(s, "Four ways to build the same logic")
    cols = [("FPGA", "reprogrammable tiles", GRN, [4, 2, 5, 1]), ("Gate array", "fixed transistors, wire it", BLUE, [3, 3, 3, 2]), ("Standard cell", "library of gates, auto layout", AMB, [4, 4, 2, 3]), ("Full custom", "every transistor drawn", PINK, [5, 5, 1, 5])]
    labels = ["speed", "density", "cheap at low volume", "design effort"]
    for i, (t, sub, c, v) in enumerate(cols):
        x = 24 + i * 152
        s.rect(x, 44, 140, 240, PANEL, c, 12, 2); s.text(x + 70, 68, t, 14, c, weight="700"); s.text(x + 70, 86, sub, 10, DIM)
        for j, lab in enumerate(labels):
            yy = 112 + j * 42
            s.text(x + 70, yy, lab, 10.5, TX)
            for k in range(5):
                s.rect(x + 16 + k * 22, yy + 6, 18, 10, c if k < v[j] else BG, c, 3, 1)
    return s


def mos_cross():
    s = Svg(620, 330, "nMOS transistor cross-section", "A p-type silicon substrate with two n+ regions, source and drain, a thin oxide and a gate on top; a channel forms between source and drain when the gate is positive.")
    head(s, "Inside an nMOS transistor")
    s.rect(40, 180, 540, 110, "#1a2a3a", BLUE, 6, 2); s.text(310, 270, "p-type silicon substrate (body)", 13, BLUE)
    s.rect(100, 180, 130, 50, "#2c4a2a", GRN, 6, 2); s.text(165, 210, "n+ source", 12, TX)
    s.rect(390, 180, 130, 50, "#2c4a2a", GRN, 6, 2); s.text(455, 210, "n+ drain", 12, TX)
    s.rect(230, 160, 160, 18, "#3a3a55", DIM, 3, 1.5); s.text(310, 154, "thin gate oxide (SiO2)", 11, DIM)
    s.rect(230, 112, 160, 46, "#4a3a22", AMB, 5, 2); s.text(310, 140, "gate (polysilicon)", 12, TX)
    s.rect(230, 180, 160, 10, "#7ab8ff55", BLUE, 2, 1, dash="4 3"); s.text(310, 204, "channel (forms when Vgs > Vt)", 10.5, BLUE)
    for nm, x, c in (("Source", 165, GRN), ("Gate", 310, AMB), ("Drain", 455, GRN)):
        s.line(x, 112 if nm == "Gate" else 180, x, 68, c, 2); s.text(x, 60, nm, 13, c, weight="700")
    s.arrow(210, 232, 400, 232, PINK, sw=2.2); s.text(310, 246, "electrons flow source to drain", 10.5, PINK)
    s.text(310, 312, "Length L = distance between source and drain; width W = how wide the channel is. Current grows with W / L.", 11, DIM)
    return s


def mos_regions():
    import math
    s = Svg(620, 360, "MOSFET I-V curves", "Drain current against drain-source voltage for several gate voltages, with the linear and saturation regions marked.")
    head(s, "Drain current Id against Vds")
    x0, y0, W, H = 70, 320, 500, 250
    s.line(x0, y0, x0 + W, y0, DIM, 2); s.line(x0, y0, x0, y0 - H, DIM, 2)
    s.text(x0 + W / 2, 346, "Vds  (drain-source voltage, volts)", 12, DIM); s.add('<text transform="rotate(-90 22 %d)" x="22" y="%d" font-size="12" fill="%s" text-anchor="middle">Id (drain current)</text>' % (y0 - H / 2, y0 - H / 2, DIM))
    Vt = 0.7; k = 1.0; cols = [BLUE, GRN, AMB, PINK]
    for j, vgs in enumerate([1.5, 2.0, 2.5, 3.0]):
        vov = vgs - Vt; pts = []
        for i in range(0, 101):
            v = i / 100 * 3.5
            idd = k * ((vov * v - v * v / 2)) if v < vov else k * vov * vov / 2
            pts.append((x0 + v / 3.5 * W, y0 - idd / 2.9 * H))
        path(s, "M" + " L".join("%.1f %.1f" % p for p in pts), cols[j], 2.4)
        s.text(x0 + W + 4, pts[-1][1] + 4, "Vgs=%.1f" % vgs, 10.5, cols[j], anchor="start")
        px = x0 + vov / 3.5 * W
        circ(s, px, y0 - k * vov * vov / 2 / 2.9 * H, 3.5, cols[j], cols[j])
    s.text(x0 + 70, y0 - 20, "LINEAR", 12, TX, weight="700"); s.text(x0 + 70, y0 - 6, "acts like a resistor", 10, DIM)
    s.text(x0 + 330, y0 - H + 22, "SATURATION", 12, TX, weight="700"); s.text(x0 + 330, y0 - H + 38, "acts like a current source", 10, DIM)
    s.text(x0 + 6, y0 + 16, "Below Vgs = Vt: cutoff (switch OFF, Id about 0)", 10.5, RED, anchor="start")
    return s


def switch_model():
    s = Svg(640, 290, "Transistors as switches", "nMOS conducts when the gate is 1 and passes a good 0; pMOS conducts when the gate is 0 and passes a good 1.")
    head(s, "The switch model: the only picture you need")
    for i, (kind, c, nm, rule, good) in enumerate([("n", BLUE, "nMOS", "gate = 1: ON   gate = 0: OFF", "passes a strong 0, weak 1"), ("p", PINK, "pMOS", "gate = 0: ON   gate = 1: OFF", "passes a strong 1, weak 0")]):
        x = 60 + i * 320
        t = mos(s, x + 40, 90, kind, c, 70)
        s.text(x + 80, 60, nm, 15, c, weight="700"); s.text(x + 80, 200, rule, 11.5, TX); s.text(x + 80, 218, good, 11.5, DIM)
        s.text(x + 10, 128, "gate", 10.5, DIM, anchor="middle"); s.text(x + 120, 84, "drain", 10.5, DIM, anchor="start"); s.text(x + 120, 178, "source", 10.5, DIM, anchor="start")
    s.text(320, 262, "Pull-down networks use nMOS (to ground). Pull-up networks use pMOS (to VDD).", 12, GRN)
    return s


def inverter():
    s = Svg(560, 340, "CMOS inverter", "A pMOS from VDD to the output and an nMOS from the output to ground, both gates tied to the input A.")
    head(s, "The CMOS inverter")
    vdd(s, 280, 50); s.line(280, 50, 280, 70, AMB, 2)
    p = mos(s, 262, 90, "p", PINK, 64); p2 = mos(s, 262, 190, "n", BLUE, 64)
    # sources/drains: for pMOS source at top, so redraw wires manually
    s.line(300, 84, 300, 70, AMB, 2); s.line(280, 70, 300, 70, AMB, 2)
    s.line(300, 160, 300, 184, DIM, 2); s.line(300, 254, 300, 280, DIM, 2); gnd(s, 300, 280)
    s.line(300, 172, 400, 172, GRN, 2); circ(s, 300, 172, 3.5, GRN, GRN); s.text(430, 177, "Y = NOT A", 13, GRN, weight="700")
    s.line(248, 122, 220, 122, TX, 2); s.line(248, 222, 220, 222, TX, 2); s.line(220, 122, 220, 222, TX, 2); s.line(150, 172, 220, 172, TX, 2); circ(s, 220, 172, 3.5, TX, TX); s.text(130, 177, "A", 14, TX, weight="700")
    s.text(380, 118, "pMOS: ON when A = 0", 11.5, PINK, anchor="start"); s.text(380, 222, "nMOS: ON when A = 1", 11.5, BLUE, anchor="start")
    s.text(280, 322, "Exactly one transistor conducts: no steady current, which is why CMOS saves power.", 11.5, DIM)
    return s


def vtc():
    import math
    s = Svg(600, 380, "Inverter voltage transfer curve", "Output voltage against input voltage for a CMOS inverter, computed from the long-channel model, with the five operating regions.")
    head(s, "Inverter transfer curve (computed)")
    VDD = 3.0; Vtn = 0.7; Vtp = 0.7; k = 1.0

    def In(vgs, vds):
        if vgs <= Vtn: return 0.0
        vov = vgs - Vtn
        return k * (vov * vds - vds * vds / 2) if vds < vov else k * vov * vov / 2

    def Ip(vsg, vsd):
        if vsg <= Vtp: return 0.0
        vov = vsg - Vtp
        return k * (vov * vsd - vsd * vsd / 2) if vsd < vov else k * vov * vov / 2

    def vout(vin):
        lo, hi = 0.0, VDD
        for _ in range(60):
            m = (lo + hi) / 2
            if In(vin, m) > Ip(VDD - vin, VDD - m): hi = m
            else: lo = m
        return (lo + hi) / 2
    x0, y0, W, H = 70, 330, 480, 250
    s.line(x0, y0, x0 + W, y0, DIM, 2); s.line(x0, y0, x0, y0 - H, DIM, 2)
    s.text(x0 + W / 2, 362, "Vin", 12, DIM); s.text(40, y0 - H / 2, "Vout", 12, DIM)
    pts = [(x0 + (i / 150 * VDD) / VDD * W, y0 - vout(i / 150 * VDD) / VDD * H) for i in range(151)]
    path(s, "M" + " L".join("%.1f %.1f" % p for p in pts), GRN, 3)
    s.line(x0, y0, x0 + W, y0 - H, LINE, 1.2, dash="4 4")
    for lab, vi in (("A: nMOS off, pMOS on", 0.15), ("B", 1.2), ("C: both on, Vm = VDD/2", 1.5), ("D", 1.8), ("E: pMOS off, nMOS on", 2.85)):
        px = x0 + vi / VDD * W; py = y0 - vout(vi) / VDD * H
        if lab[0] in "ACE":
            s.text(px + (70 if lab[0] == "A" else (0 if lab[0] == "C" else -80)), py + (-14 if lab[0] != "E" else -24), lab, 10.5, TX)
    s.text(x0 + W / 2 + 48, y0 - H / 2 - 40, "switching threshold", 10.5, AMB); circ(s, x0 + W / 2, y0 - H / 2, 4, AMB, AMB)
    s.text(300, 376, "The very steep middle gives CMOS its noise margins: tiny noise on a 0 or a 1 is cleaned away.", 11, DIM)
    return s


def nand_nor():
    s = Svg(700, 360, "CMOS NAND and NOR", "Two input NAND has series nMOS and parallel pMOS; NOR has parallel nMOS and series pMOS.")
    head(s, "NAND and NOR: series versus parallel")
    # NAND at left
    def stack(x, title, kind):
        s.text(x + 120, 54, title, 14, GRN, weight="700")
        vdd(s, x + 120, 76)
        # pull-up: two pMOS parallel (nand) or series (nor)
        if kind == "nand":
            a = mos(s, x + 50, 96, "p", PINK, 52); b = mos(s, x + 130, 96, "p", PINK, 52)
            s.line(a["d"][0], a["d"][1], a["d"][0], 80, AMB, 2); s.line(b["d"][0], b["d"][1], b["d"][0], 80, AMB, 2); s.line(a["d"][0], 80, b["d"][0], 80, AMB, 2); s.line(x + 120, 76, x + 120, 80, AMB, 2)
            ya = a["s"][1]; s.line(a["s"][0], ya, a["s"][0], 168, GRN, 2); s.line(b["s"][0], ya, b["s"][0], 168, GRN, 2); s.line(a["s"][0], 168, b["s"][0], 168, GRN, 2)
            s.text(x + 50 - 24, 126, "A", 12, TX); s.text(x + 130 - 24, 126, "B", 12, TX)
            yo = 168
            n1 = mos(s, x + 90, 184, "n", BLUE, 44); n2 = mos(s, x + 90, 252, "n", BLUE, 44)
            s.line(n1["d"][0], n1["d"][1], n1["d"][0], yo, GRN, 2); s.line(a["s"][0] + 0, yo, n1["d"][0], yo, GRN, 2)
            s.line(n1["s"][0], n1["s"][1], n2["d"][0], n2["d"][1], DIM, 2); s.line(n2["s"][0], n2["s"][1], n2["s"][0], 316, DIM, 2); gnd(s, n2["s"][0], 316)
            s.text(x + 90 - 24, 210, "A", 12, TX); s.text(x + 90 - 24, 278, "B", 12, TX)
        else:
            a = mos(s, x + 90, 92, "p", PINK, 44); b = mos(s, x + 90, 156, "p", PINK, 44)
            s.line(x + 120, 76, a["d"][0], 80, AMB, 2); s.line(a["d"][0], 80, a["d"][0], a["d"][1], AMB, 2)
            s.line(a["s"][0], a["s"][1], b["d"][0], b["d"][1], DIM, 2)
            s.text(x + 90 - 24, 118, "A", 12, TX); s.text(x + 90 - 24, 182, "B", 12, TX)
            yo = 226; s.line(b["s"][0], b["s"][1], b["s"][0], yo, GRN, 2)
            n1 = mos(s, x + 50, 244, "n", BLUE, 44); n2 = mos(s, x + 130, 244, "n", BLUE, 44)
            for nn in (n1, n2): s.line(nn["d"][0], nn["d"][1], nn["d"][0], yo, GRN, 2)
            s.line(n1["d"][0], yo, n2["d"][0], yo, GRN, 2)
            for nn in (n1, n2): s.line(nn["s"][0], nn["s"][1], nn["s"][0], 316, DIM, 2)
            s.line(n1["s"][0], 316, n2["s"][0], 316, DIM, 2); gnd(s, x + 120, 316)
            s.text(x + 50 - 24, 270, "A", 12, TX); s.text(x + 130 - 24, 270, "B", 12, TX)
        s.line(x + 180 if kind == "nand" else x + 130, yo, x + 220, yo, GRN, 2); s.text(x + 232, yo + 4, "Y", 13, GRN, weight="700", anchor="start")
    stack(10, "NAND: Y = NOT(A AND B)", "nand"); stack(360, "NOR: Y = NOT(A OR B)", "nor")
    s.text(350, 350, "Series nMOS = AND of the inputs pulling down. Parallel pMOS = the dual pull-up.", 11, DIM)
    return s


def dual():
    s = Svg(640, 280, "Pull-up and pull-down are duals", "For Y = NOT(A.B + C): pull-down has A and B in series, in parallel with C; the pull-up is the dual with A and B parallel, in series with C.")
    head(s, "Duality: swap series and parallel")
    s.rect(30, 50, 280, 200, PANEL, BLUE, 12, 2); s.text(170, 74, "Pull-down (nMOS)", 13, BLUE, weight="700")
    s.rect(330, 50, 280, 200, PANEL, PINK, 12, 2); s.text(470, 74, "Pull-up (pMOS)", 13, PINK, weight="700")
    # pull-down: (A series B) parallel C
    for (x, y, t) in ((90, 110, "A"), (90, 160, "B")): s.rect(x, y, 50, 34, BG, BLUE, 6, 2); s.text(x + 25, y + 22, t, 13, TX)
    s.line(115, 144, 115, 160, BLUE, 2); s.rect(190, 135, 50, 34, BG, BLUE, 6, 2); s.text(215, 157, "C", 13, TX)
    s.line(115, 100, 115, 110, BLUE, 2); s.line(215, 100, 215, 135, BLUE, 2); s.line(115, 100, 215, 100, BLUE, 2); s.line(115, 194, 115, 214, BLUE, 2); s.line(215, 169, 215, 214, BLUE, 2); s.line(115, 214, 215, 214, BLUE, 2)
    s.text(170, 236, "(A series B) parallel C", 11, DIM)
    # pull-up: (A parallel B) series C
    s.rect(390, 100, 50, 34, BG, PINK, 6, 2); s.text(415, 122, "A", 13, TX); s.rect(460, 100, 50, 34, BG, PINK, 6, 2); s.text(485, 122, "B", 13, TX)
    s.line(415, 134, 415, 150, PINK, 2); s.line(485, 134, 485, 150, PINK, 2); s.line(415, 150, 485, 150, PINK, 2); s.line(450, 150, 450, 164, PINK, 2)
    s.rect(425, 164, 50, 34, BG, PINK, 6, 2); s.text(450, 186, "C", 13, TX); s.line(415, 100, 415, 88, PINK, 2); s.line(485, 100, 485, 88, PINK, 2); s.line(415, 88, 485, 88, PINK, 2)
    s.text(470, 236, "(A parallel B) series C", 11, DIM)
    s.text(320, 270, "Rule: where one network has series, the other has parallel.", 12, GRN)
    return s


def srlatch():
    s = Svg(620, 300, "SR latch from NOR gates", "Two cross-coupled NOR gates with inputs R and S and outputs Q and Q-bar, plus its truth table.")
    head(s, "The SR latch: memory from feedback")
    a = gate(s, "nor", 90, 64, BLUE, 70, 44); b = gate(s, "nor", 90, 170, BLUE, 70, 44)
    s.text(40, 82, "R", 14, TX); s.text(40, 188, "S", 14, TX); s.line(48, 79, a[0][0], a[0][1], TX, 2); s.line(48, 205, b[1][0], b[1][1], TX, 2)
    s.line(a[2][0], a[2][1], 280, a[2][1], GRN, 2); s.text(296, a[2][1] + 4, "Q", 14, GRN, weight="700")
    s.line(b[2][0], b[2][1], 280, b[2][1], GRN, 2); s.text(296, b[2][1] + 4, "Q'", 14, GRN, weight="700")
    s.line(230, a[2][1], 230, b[1][1] - 6, DIM, 1.6); s.line(230, b[1][1] - 6, 70, b[1][1] - 6, DIM, 1.6); s.line(70, b[1][1] - 6, 70, b[0][1], DIM, 1.6)
    wire(s, [(230, 192 + 0), (230, 128)], DIM)
    s.line(60, 190, 60, 190, DIM)
    s.line(220, a[2][1], 220, 140, DIM, 1.6); s.line(220, 140, 70, 140, DIM, 1.6); s.line(70, 140, 70, b[0][1], DIM, 1.6)
    s.line(250, b[2][1], 250, 128, DIM, 1.6); s.line(250, 128, 72, 128, DIM, 1.6); s.line(72, 128, 72, a[1][1], DIM, 1.6)
    s.rect(380, 56, 210, 190, PANEL, LINE, 10, 1.5)
    rows = [("S", "R", "Q", "action"), ("0", "0", "Q", "hold"), ("1", "0", "1", "set"), ("0", "1", "0", "reset"), ("1", "1", "0 / 0", "forbidden")]
    for i, r in enumerate(rows):
        y = 84 + i * 32
        for j, (t, dx) in enumerate(zip(r, (402, 440, 484, 548))):
            s.text(dx, y, t, 12, (AMB if i == 0 else (RED if i == 4 else TX)), weight="700" if i == 0 else "400")
    s.text(310, 280, "While S = R = 0 the two gates hold each other in place: that is one stored bit.", 11, DIM)
    return s


def dff_timing():
    s = Svg(640, 310, "D flip-flop timing", "Waveforms of clock, d and q showing q taking the value of d only at rising clock edges.")
    head(s, "Edge triggering: q listens only at the edge")
    n = 16; w = 520; x0 = 90
    wave(s, x0, 56, w, "0101010101010101", "clk", AMB); wave(s, x0, 110, w, "0011110000111100", "d", BLUE)
    wave(s, x0, 164, w, "0000011111000000", "q", GRN)
    wave(s, x0, 164, w, "0000000000111111"[:0] or "0", "", GRN, lab=False) if False else None
    tw = w / n
    for e in (1, 3, 5, 7, 9, 11, 13, 15):
        xx = x0 + e * tw; s.line(xx, 44, xx, 200, LINE, 1, dash="3 4")
    s.text(x0 + 3 * tw, 224, "rising edges (dashed): sample d, update q", 11.5, DIM)
    s.text(x0 + 9 * tw, 244, "d changes between edges: q ignores it", 11.5, DIM)
    s.arrow(x0 + 5 * tw, 232, x0 + 5 * tw + 1, 190, PINK, sw=1.5)
    s.text(320, 290, "q takes d's old value just before the edge, then holds it until the next edge.", 11.5, DIM)
    return s


def master_slave():
    s = Svg(620, 260, "Master-slave flip-flop", "Two D latches in series with opposite enables: the master is open when the clock is low, the slave when it is high.")
    head(s, "A flip-flop is two latches back to back")
    s.box(110, 80, 120, 80, "Master latch", "open when clk = 0", BLUE); s.box(310, 80, 120, 80, "Slave latch", "open when clk = 1", PINK)
    s.arrow(40, 120, 110, 120, TX); s.text(36, 112, "D", 13, TX); s.arrow(230, 120, 310, 120, DIM); s.arrow(430, 120, 500, 120, GRN); s.text(512, 124, "Q", 13, GRN, anchor="start")
    s.line(170, 200, 170, 160, AMB, 2); s.line(370, 200, 370, 160, AMB, 2); s.line(170, 200, 370, 200, AMB, 2); s.line(270, 200, 270, 226, AMB, 2); s.text(270, 244, "clk", 13, AMB)
    circ(s, 170, 170, 4, PANEL, AMB, 2)
    s.text(270, 66, "Data passes the master while the clock is low, then the slave while it is high.", 11, DIM)
    return s


def module_box():
    s = Svg(620, 290, "A Verilog module", "A module drawn as a box with input ports on the left and output ports on the right, next to the Verilog that declares it.")
    head(s, "A module is a box with ports")
    s.rect(60, 60, 200, 170, PANEL, VIO, 12, 2.5); s.text(160, 84, "half_adder", 14, VIO, weight="700")
    for i, nm in enumerate(["a", "b"]):
        y = 124 + i * 50; s.arrow(10, y, 60, y, BLUE); s.text(30, y - 8, nm, 13, BLUE, weight="700")
    for i, nm in enumerate(["sum", "carry"]):
        y = 124 + i * 50; s.arrow(260, y, 310, y, GRN); s.text(300, y - 8, nm, 13, GRN, weight="700", anchor="end")
    s.text(160, 150, "inside: xor, and", 11, DIM); s.text(160, 168, "(the circuit)", 11, DIM)
    s.rect(340, 60, 260, 170, "#0a0712", LINE, 10, 1.5)
    code = ["module half_adder(", "  input  a, b,", "  output sum, carry);", "  xor (sum, a, b);", "  and (carry, a, b);", "endmodule"]
    for i, c in enumerate(code):
        s.text(356, 90 + i * 24, c, 12.5, TX if i in (0, 5) else (BLUE if i == 1 else (GRN if i == 2 else AMB)), anchor="start", style='font-family="ui-monospace,Menlo,monospace"')
    s.text(310, 268, "Ports are the only way in or out. Everything else inside is private.", 11.5, DIM)
    return s


def fa_hier():
    s = Svg(640, 300, "Full adder hierarchy", "A full adder built from two half adders and an or gate, showing the module hierarchy.")
    head(s, "Hierarchy: modules inside modules")
    s.rect(30, 46, 580, 220, "none", VIO, 14, 2, dash="6 4"); s.text(60, 66, "full_adder", 12, VIO, weight="700", anchor="start")
    s.box(110, 90, 120, 64, "half_adder h1", "a + b", BLUE); s.box(300, 128, 120, 64, "half_adder h2", "s1 + cin", BLUE)
    g = gate(s, "or", 480, 150, AMB, 60, 40, "or")
    s.arrow(40, 108, 110, 108, TX); s.text(44, 100, "a", 12, TX, anchor="start"); s.arrow(40, 138, 110, 138, TX); s.text(44, 130, "b", 12, TX, anchor="start")
    s.line(230, 108, 270, 108, DIM, 2); s.line(270, 108, 270, 146, DIM, 2); s.arrow(270, 146, 300, 146, DIM); s.text(262, 100, "s1", 11, DIM)
    s.arrow(40, 178, 300, 178, TX); s.text(44, 170, "cin", 12, TX, anchor="start")
    s.arrow(420, 146, 520 - 40, 146, GRN) if False else None
    s.line(420, 146, 450, 146, DIM, 2); s.line(450, 146, 450, 160, DIM, 2); s.arrow(450, 160, 480, 160, DIM)
    s.line(230, 138, 460, 138, DIM, 1.5, dash="3 3"); s.line(460, 138, 460, 172, DIM, 1.5, dash="3 3"); s.arrow(460, 172, 480, 172, DIM)
    s.text(240, 130, "c1", 11, DIM); s.text(430, 140, "c2", 11, DIM)
    s.arrow(420, 166, 440, 220, GRN, sw=0) if False else None
    s.line(420, 166, 440, 230, GRN, 1.8); s.line(440, 230, 600, 230, GRN, 1.8); s.text(604, 234, "sum", 12, GRN, anchor="start")
    s.arrow(540, 170, 600, 170, GRN); s.text(604, 174, "cout", 12, GRN, anchor="start")
    s.text(320, 288, "Instantiation: half_adder h1(.a(a), .b(b), .sum(s1), .carry(c1));", 11.5, DIM)
    return s


def levels():
    s = Svg(620, 330, "Levels of abstraction in Verilog", "Four ways to describe a 2-to-1 multiplexer: behavioural, dataflow, gate level and switch level, from most abstract to least.")
    head(s, "Same circuit, four levels of detail")
    rows = [("Behavioural", "always @* if (s) y = b; else y = a;", GRN), ("Dataflow (RTL)", "assign y = s ? b : a;", BLUE), ("Gate level", "and (t1,a,ns); and (t2,b,s); or (y,t1,t2);", AMB), ("Switch level", "nmos / pmos transistors (rare)", PINK)]
    for i, (t, code, c) in enumerate(rows):
        y = 50 + i * 66; w = 560 - i * 30
        s.rect(30 + i * 15, y, w, 54, PANEL, c, 10, 2); s.text(46 + i * 15, y + 22, t, 13, c, weight="700", anchor="start")
        s.text(46 + i * 15, y + 42, code, 11.5, TX, anchor="start", style='font-family="ui-monospace,Menlo,monospace"')
    s.arrow(600, 60, 600, 300, DIM); s.text(540, 318, "more detail, more control", 10.5, DIM)
    return s


def vectors():
    s = Svg(640, 300, "Vectors and part-selects", "An 8-bit vector with bit indices 7 down to 0, a part-select of the upper nibble, and a concatenation swapping the halves.")
    head(s, "reg [7:0] x  and what you can do with it")
    bits = "10110010"
    for i, b in enumerate(bits):
        x = 70 + i * 62; s.rect(x, 60, 54, 44, PANEL, AMB if i < 4 else BLUE, 6, 2); s.text(x + 27, 88, b, 17, TX, weight="700"); s.text(x + 27, 124, str(7 - i), 11, DIM)
    s.text(36, 88, "x", 14, TX, weight="700")
    s.line(70, 138, 70 + 4 * 62 - 8, 138, AMB, 3); s.text(70 + 124, 158, "x[7:4] = 4'b1011", 12, AMB)
    s.line(70 + 4 * 62, 138, 70 + 8 * 62 - 8, 138, BLUE, 3); s.text(70 + 372, 158, "x[3:0] = 4'b0010", 12, BLUE)
    s.text(70 + 3.5 * 62 + 27, 196, "{x[3:0], x[7:4]}", 13, TX, weight="700")
    for i, b in enumerate("00101011"):
        x = 70 + i * 62; s.rect(x, 208, 54, 36, PANEL, BLUE if i < 4 else AMB, 6, 2); s.text(x + 27, 232, b, 15, TX, weight="700")
    s.text(320, 280, "Single bit: x[5]. Replicate: {4{x[0]}}. Concatenate: {a, b}. All of these work on either side of an assignment.", 11, DIM)
    return s


def fourval():
    s = Svg(640, 310, "Four-valued logic and a tri-state bus", "The four Verilog values 0, 1, x, z with and-gate behaviour, and two tri-state drivers sharing one wire.")
    head(s, "Four values: 0, 1, x (unknown), z (high impedance)")
    heads = ["0", "1", "x", "z"]; tab = {"0": "0000", "1": "01xx", "x": "0xxx", "z": "0xxx"}
    s.text(100, 62, "a AND b", 12, DIM)
    for j, h in enumerate(heads): s.text(150 + j * 44, 62, "b=" + h, 11, BLUE)
    for i, h in enumerate(heads):
        s.text(110, 92 + i * 32, "a=" + h, 11, PINK, anchor="end")
        for j in range(4):
            v = tab[h][j]; s.rect(130 + j * 44, 76 + i * 32, 40, 26, PANEL, RED if v == "x" else LINE, 5, 1.5); s.text(150 + j * 44, 94 + i * 32, v, 13, RED if v == "x" else TX, weight="700")
    s.text(130, 224, "0 AND anything = 0, but 1 AND x = x.", 11, DIM, anchor="start")
    # tristate bus
    s.line(500, 150, 610, 150, GRN, 3); s.text(612, 154, "bus", 13, GRN, anchor="start")
    g1 = gate(s, "buf", 400, 60, BLUE, 52, 34); s.text(426, 54, "driver A: en_a = 1", 10.5, BLUE); s.text(380, 82, "a", 11, TX, anchor="end")
    s.line(452, 77, 500, 77, BLUE, 2); s.line(500, 77, 500, 150, GRN, 2); circ(s, 500, 150, 3.5, GRN, GRN)
    g2 = gate(s, "buf", 400, 200, DIM, 52, 34); s.text(426, 248, "driver B: en_b = 0, outputs z", 10.5, DIM); s.text(380, 222, "b", 11, TX, anchor="end")
    s.line(452, 217, 500, 217, DIM, 2, dash="4 3"); s.line(500, 217, 500, 150, GRN, 2)
    s.text(560, 120, "bus = a", 11, GRN, anchor="start"); s.text(560, 172, "(B lets go)", 11, DIM, anchor="start")
    s.text(420, 280, "assign bus = en_a ? a : 1'bz;", 11, TX, style='font-family="ui-monospace,Menlo,monospace"')
    s.text(320, 296, "Two drivers on at once with different values gives x: a bus fight.", 11, RED)
    return s


def ripple():
    s = Svg(680, 290, "Ripple-carry adder", "Four full adders in a row; each carry-out feeds the next carry-in, and the carry delay accumulates along the chain.")
    head(s, "4-bit ripple-carry adder: the carry ripples")
    for i in range(4):
        x = 500 - i * 150 + 0
        s.box(x - 20, 80, 110, 70, "FA%d" % i, "a%d b%d" % (i, i), BLUE)
        s.arrow(x + 35, 40, x + 35, 80, TX); s.text(x + 35, 36, "a%d b%d" % (i, i), 10.5, TX)
        s.arrow(x + 35, 150, x + 35, 190, GRN); s.text(x + 35, 204, "s%d" % i, 12, GRN, weight="700")
        if i < 3: s.arrow(x - 20, 115, x - 40, 115, AMB, sw=2.4); s.text(x - 30, 105, "c%d" % (i + 1), 11, AMB, weight="700")
    s.arrow(660, 115, 590, 115, AMB, sw=2.4); s.text(652, 105, "cin", 11, AMB, weight="700")
    s.arrow(20, 115, 10, 115, AMB) if False else None
    s.text(34, 119, "cout", 11, AMB, weight="700", anchor="start")
    s.text(340, 248, "Delay of the sum grows with the chain: t = 4 x (carry delay). Faster adders predict carries (carry-lookahead).", 11.5, DIM)
    s.text(340, 268, "In Verilog: four instances, or one line: assign {cout, sum} = a + b + cin;", 11.5, GRN)
    return s


def mux_dec():
    s = Svg(640, 300, "Multiplexer and decoder", "A 4-to-1 multiplexer with a 2-bit select and a 3-to-8 decoder with enable.")
    head(s, "Selecting and decoding")
    path(s, "M60 60 L190 90 L190 210 L60 240 Z", VIO, 2.2, PANEL)
    for i, nm in enumerate(["a", "b", "c", "d"]):
        y = 90 + i * 38; s.arrow(20, y, 60, y, BLUE); s.text(14, y - 4, nm, 12, BLUE)
    s.arrow(190, 150, 240, 150, GRN); s.text(244, 154, "y", 13, GRN, anchor="start")
    s.arrow(125, 268, 125, 222, AMB); s.text(125, 284, "s[1:0]", 11.5, AMB)
    s.text(125, 156, "MUX 4:1", 12, TX, weight="700")
    s.rect(340, 60, 120, 190, PANEL, VIO, 10, 2.2); s.text(400, 156, "DEC 3:8", 12, TX, weight="700")
    s.arrow(300, 110, 340, 110, BLUE); s.text(290, 104, "a[2:0]", 11, BLUE, anchor="end"); s.arrow(300, 200, 340, 200, AMB); s.text(290, 204, "en", 11, AMB, anchor="end")
    for i in range(8):
        y = 72 + i * 22; s.arrow(460, y, 500, y, GRN if i == 5 else DIM); s.text(506, y + 4, "y[%d]%s" % (i, "  = 1 when a = 5" if i == 5 else ""), 10.5, GRN if i == 5 else DIM, anchor="start")
    s.text(320, 296, "A multiplexer picks one of many; a decoder turns a number into one hot line.", 11.5, DIM)
    return s


def twos_wheel():
    import math
    s = Svg(560, 400, "Two's complement wheel", "The sixteen 4-bit patterns arranged on a circle, showing unsigned values 0 to 15 and signed values -8 to 7, with subtraction as walking backwards.")
    head(s, "4-bit numbers on a wheel: unsigned and signed")
    cx, cy, R = 280, 215, 140
    for i in range(16):
        a = math.radians(-90 + i * 22.5); x = cx + R * math.cos(a); y = cy + R * math.sin(a)
        signed = i if i < 8 else i - 16
        circ(s, x, y, 21, PANEL, GRN if signed >= 0 else PINK, 2)
        s.text(x, y - 2, format(i, "04b"), 10.5, TX, weight="700"); s.text(x, y + 11, "%d / %d" % (i, signed) if i >= 8 else str(i), 9.5, DIM)
    s.text(cx, cy - 6, "adding 1 = one step clockwise", 12, TX); s.text(cx, cy + 14, "subtracting = counter-clockwise", 12, TX)
    s.text(cx, cy + 40, "7 + 1 wraps to -8 (overflow)", 11.5, AMB)
    s.text(280, 392, "Same bits, two readings. Verilog stores bits; signed or unsigned is how you read them.", 11, DIM)
    return s


ALL_A = {"vl-flow.svg": flow, "vl-ychart.svg": ychart, "vl-styles.svg": styles, "vl-mos-cross.svg": mos_cross, "vl-mos-regions.svg": mos_regions, "vl-switch.svg": switch_model, "vl-inverter.svg": inverter, "vl-vtc.svg": vtc,
         "vl-nandnor.svg": nand_nor, "vl-dual.svg": dual, "vl-srlatch.svg": srlatch, "vl-dfftiming.svg": dff_timing, "vl-masterslave.svg": master_slave, "vl-module.svg": module_box, "vl-fahier.svg": fa_hier,
         "vl-levels.svg": levels, "vl-vectors.svg": vectors, "vl-fourval.svg": fourval, "vl-ripple.svg": ripple, "vl-muxdec.svg": mux_dec, "vl-twos.svg": twos_wheel}


if __name__ == "__main__":
    import os
    os.makedirs("/tmp/vl_figs", exist_ok=True)
    for fn, f in ALL_A.items(): open("/tmp/vl_figs/" + fn, "w").write(f().render())
    print(len(ALL_A))
