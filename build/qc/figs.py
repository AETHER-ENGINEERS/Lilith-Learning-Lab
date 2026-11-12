# -*- coding: utf-8 -*-
"""Original SVG figures for the quantum computing course (drawn in code, no third-party artwork)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from make_images import Svg, BG, PANEL, LINE, TX, DIM, VIO, PINK, BLUE, GRN, AMB, RED  # noqa: E402

CY = "#8fd3ff"


def bars(s, x, base, vals, w=34, gap=14, scale=70, labels=None, colors=None, fmt=None, vmax=None, ly=None):
    """Signed vertical bars around a baseline. vals in -1..1 (times scale)."""
    for i, v in enumerate(vals):
        bx = x + i * (w + gap)
        h = abs(v) * scale
        col = (colors[i] if colors else (VIO if v >= 0 else PINK))
        if h > 0.5:
            s.rect(bx, base - h if v >= 0 else base, w, h, fill=col, stroke=col, r=4, sw=1)
        if fmt is not None:
            s.text(bx + w / 2, (base - h - 6) if v >= 0 else (base + h + 14), fmt(v), 11.5, TX, weight="600")
        if labels:
            s.text(bx + w / 2, base + (scale * 0.55 + 22 if ly is None else ly), labels[i], 12, DIM)
    s.line(x - 8, base, x + len(vals) * (w + gap) - gap + 8, base, LINE, 1.2)


def qm_filters():
    s = Svg(640, 340, "Polarizer filters", "Two crossed filters block all light. Adding a third filter at 45 degrees between them lets a quarter of the light through.")
    s.text(320, 26, "Sunglasses surprise: more filters, more light", 15, VIO, weight="700")

    def row(y, filters, outs, title):
        s.text(18, y - 22, title, 12.5, DIM, anchor="start", weight="600")
        s.add('<circle cx="40" cy="%s" r="14" fill="%s"/>' % (y + 20, AMB)); s.text(40, y + 52, "light", 11, DIM)
        x = 76
        s.arrow(x - 18, y + 20, x + 6, y + 20, AMB)
        for i, ang in enumerate(filters):
            fx = 96 + i * 130
            s.rect(fx, y - 6, 50, 52, fill=PANEL, stroke=BLUE, r=8)
            a = math.radians(ang)
            s.line(fx + 25 - 18 * math.sin(a), y + 20 + 18 * math.cos(a), fx + 25 + 18 * math.sin(a), y + 20 - 18 * math.cos(a), BLUE, 3)
            s.text(fx + 25, y + 62, "%d°" % ang, 11, DIM)
            nx = fx + 50
            s.arrow(nx, y + 20, nx + 60, y + 20, AMB if outs[i] > 0 else LINE)
            s.text(nx + 40, y + 10, "%d%%" % outs[i], 12.5, TX, weight="600")
    row(84, [0, 90], [100, 0], "Two filters: all blocked")
    row(214, [0, 45, 90], [100, 50, 25], "Add a middle filter: light comes back")
    return s


def qm_ball_vs_electron():
    s = Svg(640, 260, "Ball and electron", "A ball follows one path. An electron spreads out like a cloud of possibilities until we look.")
    s.text(160, 26, "A ball: one path", 14, VIO, weight="700"); s.text(480, 26, "An electron: a cloud", 14, VIO, weight="700")
    s.line(40, 190, 280, 190, LINE)
    pts = [(40 + 24 * i, 190 - 4 * i * (10 - i) / 1.0) for i in range(11)]
    s.add('<polyline points="%s" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="4 5"/>' % (" ".join("%s,%s" % (x, y) for x, y in pts), DIM))
    for x, y in pts[::5]:
        s.add('<circle cx="%s" cy="%s" r="11" fill="%s"/>' % (x, y, AMB))
    s.text(160, 228, "You know where it is, always", 12, DIM)
    for i in range(70):
        a = i * 2.399
        r = 8 + 5.5 * math.sqrt(i)
        s.add('<circle cx="%.1f" cy="%.1f" r="4" fill="%s" opacity="0.5"/>' % (480 + r * math.cos(a), 118 + 0.75 * r * math.sin(a), VIO))
    s.add('<circle cx="548" cy="82" r="7" fill="%s"/>' % PINK); s.text(560, 62, "looked: one spot", 11, PINK)
    s.text(480, 228, "Spread out until you look, then it picks one place", 12, DIM)
    return s


def bits_vs_qubits():
    s = Svg(640, 230, "Bit, coin and qubit", "A bit is 0 or 1. A coin has chances. A qubit has two amplitudes that make the chances.")
    for i, (t, sub, col) in enumerate([("Bit", "definitely 0 or 1", BLUE), ("Coin (chance)", "heads 50%, tails 50%", AMB), ("Qubit", "two amplitudes a and b", VIO)]):
        x = 20 + i * 205
        s.rect(x, 30, 190, 170, fill=PANEL, stroke=col)
        s.text(x + 95, 56, t, 14, TX, weight="700")
    s.rect(60, 80, 44, 44, fill=BLUE, stroke=BLUE, r=6); s.text(82, 110, "0", 22, BG, weight="700")
    s.rect(112, 80, 44, 44, fill=PANEL, stroke=BLUE, r=6); s.text(134, 110, "1", 22, BLUE, weight="700")
    s.text(115, 160, "a switch: off or on", 12, DIM); s.text(115, 180, "definitely one", 12, DIM)
    s.add('<circle cx="325" cy="102" r="30" fill="%s" stroke="%s" stroke-width="2"/>' % (PANEL, AMB)); s.text(325, 108, "?", 24, AMB, weight="700")
    s.text(320, 160, "hidden until it lands", 12, DIM); s.text(320, 180, "chances add to 100%", 12, DIM)
    s.add('<ellipse cx="530" cy="102" rx="34" ry="14" fill="%s" opacity="0.55"/><ellipse cx="530" cy="102" rx="14" ry="34" fill="%s" opacity="0.45"/>' % (VIO, PINK)); s.text(530, 108, "a, b", 14, TX, weight="700")
    s.text(530, 160, "square them for chances", 12, DIM); s.text(530, 180, "then it picks one", 12, DIM)
    return s


def bits_double():
    s = Svg(640, 250, "Doubling", "Each extra qubit doubles the number of amplitudes: 2, 4, 8, 16, 32.")
    s.text(320, 24, "Every extra qubit doubles the list", 15, VIO, weight="700")
    for i in range(5):
        n = 2 ** (i + 1); h = 12 + n * 4.6; x = 60 + i * 110
        s.rect(x, 200 - h, 70, h, fill=VIO, stroke=VIO, r=6, sw=1)
        s.text(x + 35, 192 - h, str(n), 15, TX, weight="700"); s.text(x + 35, 222, "%d qubit%s" % (i + 1, "" if i == 0 else "s"), 12, DIM)
    return s


def qubit_squares():
    s = Svg(640, 260, "Amplitude squared", "Amplitudes 0.6 and 0.8 become chances 36 percent and 64 percent, which add to 100 percent.")
    s.text(320, 24, "Square the amplitude to get the chance", 15, VIO, weight="700")
    s.text(150, 52, "amplitudes", 12.5, DIM); s.text(490, 52, "chances", 12.5, DIM)
    bars(s, 90, 190, [0.6, 0.8], w=50, gap=34, scale=110, labels=["|0⟩", "|1⟩"], fmt=lambda v: "%.1f" % v)
    s.arrow(250, 130, 390, 130, PINK); s.text(320, 118, "square", 12, PINK, weight="600")
    bars(s, 430, 190, [0.36, 0.64], w=50, gap=34, scale=110, labels=["|0⟩", "|1⟩"], colors=[BLUE, BLUE], fmt=lambda v: "%d%%" % round(v * 100))
    return s


def gates_effect():
    s = Svg(640, 300, "X, H and Z", "X swaps the amplitudes. H makes an even blend. Z flips the sign of the one amplitude.")
    s.text(320, 24, "What the gates do to a plain 0", 15, VIO, weight="700")
    for i, (t, a, b, sub) in enumerate([("X", [0, 1], None, "swaps: 0 becomes 1"), ("H", [0.707, 0.707], None, "even blend"), ("Z on a blend", [0.707, -0.707], None, "flips a sign")]):
        x = 20 + i * 210
        s.rect(x, 40, 195, 240, fill=PANEL, stroke=VIO)
        s.text(x + 97, 66, t, 14, TX, weight="700")
        bars(s, x + 36, 150, a, w=44, gap=24, scale=70, labels=["|0⟩", "|1⟩"], fmt=lambda v: "%.2f" % v if v else "", ly=92)
        s.text(x + 97, 264, sub, 12, DIM)
    return s


def interference_waves():
    s = Svg(640, 270, "Waves add or cancel", "Two waves in step make a bigger wave. Two waves out of step cancel to nothing.")
    s.text(320, 24, "Interference: add the waves", 15, VIO, weight="700")
    for k, (title, ph, ym) in enumerate([("In step: bigger", 0, 90), ("Opposite: they cancel", math.pi, 205)]):
        s.text(18, ym - 56, title, 12.5, DIM, anchor="start", weight="600")
        for col, p, dy in [(BLUE, 0, -6), (PINK, ph, 6)]:
            pts = ["%.1f,%.1f" % (40 + x * 3.6, ym + dy + 22 * math.sin(x / 20.0 * 6.283 + p)) for x in range(0, 101)]
            s.add('<polyline points="%s" fill="none" stroke="%s" stroke-width="2" opacity="0.8"/>' % (" ".join(pts), col))
        s.arrow(412, ym, 452, ym, DIM)
        amp = 44 if k == 0 else 0
        pts = ["%.1f,%.1f" % (462 + x * 1.6, ym + amp * math.sin(x / 20.0 * 6.283) * 0.9) for x in range(0, 101)]
        s.add('<polyline points="%s" fill="none" stroke="%s" stroke-width="3"/>' % (" ".join(pts), GRN))
        s.text(540, ym + 50, "sum", 11, DIM)
    return s


def interference_paths():
    s = Svg(640, 300, "H then Z then H", "After H the amplitudes are 0.7 and 0.7. Z makes the second negative. The last H cancels the paths to 0 and adds the paths to 1.")
    s.text(320, 24, "H, Z, H: paths cancel and add", 15, VIO, weight="700")
    cols = [60, 220, 380, 540]
    heads = ["start", "after H", "after Z", "after H"]
    vals = [("1", "0"), ("0.7", "0.7"), ("0.7", "-0.7"), ("0", "1")]
    for c, h in zip(cols, heads):
        s.text(c + 20, 50, h, 12, DIM)
    for i, c in enumerate(cols):
        s.rect(c - 12, 70, 64, 40, fill=PANEL, stroke=BLUE, r=8); s.text(c + 20, 86, "|0⟩", 10.5, DIM); s.text(c + 20, 102, vals[i][0], 14, TX, weight="700")
        s.rect(c - 12, 160, 64, 40, fill=PANEL, stroke=PINK, r=8); s.text(c + 20, 176, "|1⟩", 10.5, DIM); s.text(c + 20, 192, vals[i][1], 14, TX, weight="700")
    for c, g in zip([140, 300, 460], ["H", "Z", "H"]):
        s.rect(c - 14, 120, 28, 28, fill=VIO, stroke=VIO, r=6); s.text(c, 140, g, 14, BG, weight="700")
    s.text(320, 250, "At the end the two routes to |0⟩ have opposite signs and cancel.", 12.5, TX)
    s.text(320, 272, "The two routes to |1⟩ have the same sign and add up to a sure 1.", 12.5, TX)
    return s


def bloch_sphere():
    s = Svg(640, 410, "Bloch sphere", "A globe with north pole 0, south pole 1, and the plus, minus, plus i and minus i points on the equator. An arrow shows a qubit state.")
    cx, cy, R = 225, 215, 130
    s.text(320, 26, "The Bloch sphere: a globe for one qubit", 15, VIO, weight="700")
    s.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="2"/>' % (cx, cy, R, PANEL, LINE))
    s.add('<ellipse cx="%d" cy="%d" rx="%d" ry="40" fill="none" stroke="%s" stroke-width="1.5"/>' % (cx, cy, R, LINE))
    s.add('<ellipse cx="%d" cy="%d" rx="48" ry="%d" fill="none" stroke="%s" stroke-width="1" stroke-dasharray="3 4"/>' % (cx, cy, R, LINE))
    s.line(cx, cy - R - 14, cx, cy + R + 14, DIM, 1.2, "3 4"); s.line(cx - R - 14, cy + 18, cx + R + 14, cy - 18, DIM, 1.2, "3 4")
    for (x, y, t, c) in [(cx, cy - R - 12, "|0⟩ north pole", TX), (cx, cy + R + 22, "|1⟩ south pole", TX), (cx + R + 22, cy - 22, "|+⟩", DIM), (cx - R - 22, cy + 28, "|−⟩", DIM), (cx + 62, cy + 62, "|+i⟩", DIM)]:
        s.text(x, y, t, 12.5, c)
    ex, ey = cx + 60, cy - 70
    s.line(cx, cy, ex, ey, PINK, 3.5)
    s.add('<circle cx="%d" cy="%d" r="7" fill="%s"/>' % (ex, ey, PINK))
    s.add('<path d="M %d %d A 40 40 0 0 1 %d %d" fill="none" stroke="%s" stroke-width="2"/>' % (cx, cy - 40, cx + 24, cy - 33, AMB)); s.text(cx + 34, cy - 46, "θ", 14, AMB, weight="700")
    s.rect(430, 90, 190, 230, fill=PANEL, stroke=VIO)
    for i, t in enumerate(["Height = chance", "top: always 0", "middle: 50 50", "bottom: always 1", "", "Round = phase", "turn around the", "vertical axis", "", "Gates = turns", "of the globe"]):
        s.text(450, 118 + i * 18, t, 12.5, TX if i in (0, 5, 9) else DIM, anchor="start", weight="700" if i in (0, 5, 9) else "400")
    return s


def bloch_gates():
    s = Svg(640, 300, "Gates as turns", "X, Y and Z are half turns about the x, y and z axes. H is a half turn about a slanted axis. S is a quarter turn and T an eighth turn about the vertical axis.")
    s.text(320, 24, "Every gate is a turn of the globe", 15, VIO, weight="700")
    rows = [("X", "half turn about x", "swaps the poles", PINK), ("Y", "half turn about y", "swaps the poles, shifts phase", PINK), ("Z", "half turn about vertical", "flips the phase", BLUE), ("H", "half turn about the slant between x and z", "pole ↔ equator", VIO), ("S", "quarter turn about vertical", "equator point moves 90°", CY), ("T", "eighth turn about vertical", "equator point moves 45°", CY)]
    for i, (g, a, b, c) in enumerate(rows):
        y = 44 + i * 40
        s.rect(20, y, 40, 32, fill=c, stroke=c, r=6); s.text(40, y + 22, g, 16, BG, weight="700")
        s.text(76, y + 14, a, 13, TX, anchor="start", weight="600"); s.text(76, y + 29, b, 11.5, DIM, anchor="start")
    return s


def circuit_read():
    s = Svg(640, 250, "Reading a circuit", "Two wires, qubit 0 on top and qubit 1 below. An H gate on the top wire, then a CNOT with a dot on the top wire and a plus in a circle on the bottom wire. Read left to right.")
    s.text(320, 24, "A circuit is a music sheet: read left to right", 15, VIO, weight="700")
    for y, t in [(90, "qubit 0"), (170, "qubit 1")]:
        s.text(24, y + 5, t, 12.5, DIM, anchor="start"); s.line(90, y, 600, y, LINE, 2.5)
        s.text(80, y + 5, "0", 14, TX, anchor="end", weight="700")
    s.rect(150, 70, 40, 40, fill=PINK, stroke=PINK, r=8); s.text(170, 96, "H", 17, BG, weight="700")
    s.add('<circle cx="300" cy="90" r="7" fill="%s"/>' % VIO); s.line(300, 90, 300, 170, VIO, 2.5)
    s.add('<circle cx="300" cy="170" r="16" fill="none" stroke="%s" stroke-width="2.5"/>' % VIO); s.line(300, 154, 300, 186, VIO, 2.5); s.line(284, 170, 316, 170, VIO, 2.5)
    for y in (90, 170):
        s.rect(440, y - 18, 42, 36, fill=PANEL, stroke=DIM, r=6); s.text(461, y + 5, "M", 14, TX, weight="700")
    s.arrow(150, 218, 560, 218, AMB); s.text(355, 240, "time goes this way", 12, AMB)
    s.text(170, 50, "1. blend", 12, DIM); s.text(300, 50, "2. link (CNOT)", 12, DIM); s.text(461, 50, "3. look", 12, DIM)
    return s


def cnot_table():
    s = Svg(640, 260, "CNOT table", "CNOT flips the second qubit only when the first qubit is 1: 00 stays 00, 01 stays 01, 10 becomes 11 and 11 becomes 10.")
    s.text(320, 24, "CNOT: flip the target only if the control is 1", 15, VIO, weight="700")
    s.text(150, 52, "before", 12.5, DIM); s.text(490, 52, "after", 12.5, DIM)
    rows = [("00", "00", False), ("01", "01", False), ("10", "11", True), ("11", "10", True)]
    for i, (a, b, ch) in enumerate(rows):
        y = 64 + i * 48
        s.rect(100, y, 100, 36, fill=PANEL, stroke=BLUE, r=8); s.text(150, y + 24, a, 17, TX, weight="700")
        s.arrow(210, y + 18, 420, y + 18, PINK if ch else LINE)
        s.text(315, y + 10, "flips qubit 1" if ch else "no change", 11.5, PINK if ch else DIM)
        s.rect(440, y, 100, 36, fill=PANEL, stroke=PINK if ch else BLUE, r=8); s.text(490, y + 24, b, 17, TX, weight="700")
    return s


def bell_pair():
    s = Svg(640, 280, "Bell pair", "Two linked coins always agree. Measuring gives 00 half the time and 11 half the time, never 01 or 10.")
    s.text(320, 24, "Entanglement: two coins that always agree", 15, VIO, weight="700")
    for x in (100, 260):
        s.add('<circle cx="%d" cy="100" r="34" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x, PANEL, AMB)); s.text(x, 108, "?", 26, AMB, weight="700")
    pts = ["%.1f,%.1f" % (136 + i * 2.2, 100 + 9 * math.sin(i * 0.9)) for i in range(0, 41)]
    s.add('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.5"/>' % (" ".join(pts), PINK))
    s.text(180, 160, "linked", 12.5, PINK, weight="600"); s.text(180, 180, "each alone is random", 11.5, DIM)
    s.text(500, 60, "what you see", 12.5, DIM)
    bars(s, 410, 220, [0.5, 0, 0, 0.5], w=34, gap=14, scale=140, labels=["00", "01", "10", "11"], colors=[VIO, VIO, VIO, VIO], fmt=lambda v: "%d%%" % round(v * 100))
    return s


def grover_bars():
    s = Svg(640, 270, "Grover steps", "Start with equal amplitudes. The marked item gets a negative sign. Reflecting about the average raises the marked item to 1 and removes the rest.")
    s.text(320, 24, "Grover: mark it, then reflect", 15, VIO, weight="700")
    for i, (t, v) in enumerate([("1. even blend", [0.5, 0.5, 0.5, 0.5]), ("2. mark 11 (flip sign)", [0.5, 0.5, 0.5, -0.5]), ("3. reflect about the average", [0, 0, 0, 1])]):
        x = 20 + i * 210
        s.rect(x, 40, 195, 215, fill=PANEL, stroke=VIO)
        s.text(x + 97, 62, t, 12, TX, weight="600")
        cols = [PINK if (j == 3) else BLUE for j in range(4)]
        bars(s, x + 22, 170, v, w=26, gap=10, scale=95, labels=["00", "01", "10", "11"], colors=cols, ly=62)
    return s


def shots_wobble():
    s = Svg(640, 250, "More shots", "With 10 shots the counts are far from 50 50. With 100 they are closer. With 1000 they are very close.")
    s.text(320, 24, "More shots, steadier counts", 15, VIO, weight="700")
    for i, (n, a) in enumerate([(10, 7), (100, 56), (1000, 507)]):
        x = 30 + i * 205
        s.rect(x, 40, 185, 190, fill=PANEL, stroke=VIO)
        s.text(x + 92, 62, "%d shots" % n, 13, TX, weight="700")
        fa = a / float(n)
        for j, (v, c) in enumerate([(fa, BLUE), (1 - fa, PINK)]):
            h = v * 100
            s.rect(x + 36 + j * 62, 175 - h, 44, h, fill=c, stroke=c, r=4, sw=1); s.text(x + 58 + j * 62, 168 - h, "%d%%" % round(v * 100), 12, TX, weight="600")
            s.text(x + 58 + j * 62, 196, ["00", "11"][j], 12, DIM)
        s.line(x + 20, 125, x + 165, 125, AMB, 1.2, "4 4")
    s.text(320, 244, "dashed line = the true 50%", 11.5, AMB)
    return s


def qasm_vs_circuit():
    s = Svg(640, 270, "OpenQASM and the circuit", "The same Bell circuit as a picture and as OpenQASM text: qubit declaration, h on q0, then cx from q0 to q1.")
    s.text(320, 24, "One circuit, two ways to write it", 15, VIO, weight="700")
    s.rect(20, 44, 290, 200, fill=PANEL, stroke=BLUE, r=10); s.text(165, 68, "picture", 12.5, DIM)
    for y in (110, 180):
        s.line(40, y, 290, y, LINE, 2.5)
    s.rect(80, 92, 36, 36, fill=PINK, stroke=PINK, r=7); s.text(98, 116, "H", 16, BG, weight="700")
    s.add('<circle cx="200" cy="110" r="6" fill="%s"/>' % VIO); s.line(200, 110, 200, 180, VIO, 2.5)
    s.add('<circle cx="200" cy="180" r="14" fill="none" stroke="%s" stroke-width="2.5"/>' % VIO); s.line(200, 166, 200, 194, VIO, 2.5); s.line(186, 180, 214, 180, VIO, 2.5)
    s.rect(330, 44, 290, 200, fill=PANEL, stroke=VIO, r=10); s.text(475, 68, "text", 12.5, DIM)
    for i, (t, c) in enumerate([("OPENQASM 3.0;", DIM), ("qubit[2] q;", TX), ("h q[0];", PINK), ("cx q[0], q[1];", VIO)]):
        s.text(352, 104 + i * 30, t, 15, c, anchor="start", weight="600", style='font-family="monospace"')
    s.arrow(312, 144, 328, 144, DIM)
    return s


def qiskit_pipeline():
    s = Svg(640, 220, "Qiskit steps", "Build the circuit, transpile it for the chip, run it with a sampler, then read the counts.")
    s.text(320, 24, "A Qiskit program in four steps", 15, VIO, weight="700")
    for i, (t, sub, c) in enumerate([("1 Build", "QuantumCircuit", BLUE), ("2 Transpile", "fit the chip", AMB), ("3 Run", "Sampler: shots", PINK), ("4 Read", "counts", GRN)]):
        x = 20 + i * 155
        s.box(x, 60, 125, 70, t, sub, c)
        if i < 3:
            s.arrow(x + 127, 95, x + 153, 95, DIM)
    s.text(320, 170, "Our lab's Python tab runs MicroQiskit: the same first and last steps, offline.", 12.5, DIM)
    return s


def endian():
    s = Svg(640, 250, "Qubit order", "Our composer writes qubit 0 on the left of a result. Qiskit writes qubit 0 on the right. The same state is written 10 in the composer and 01 in Qiskit.")
    s.text(320, 24, "The trap: which side is qubit 0?", 15, VIO, weight="700")
    for k, (t, d0, d1, x, c) in enumerate([("Our composer", "1", "0", 60, PINK), ("Qiskit", "0", "1", 360, BLUE)]):
        s.rect(x, 44, 220, 170, fill=PANEL, stroke=c)
        s.text(x + 110, 68, t, 13, TX, weight="700")
        left, right = (("q0", "q1") if k == 0 else ("q1", "q0"))
        vals = ("1", "0") if k == 0 else ("0", "1")
        for j, (nm, v) in enumerate(zip((left, right), vals)):
            bx = x + 40 + j * 80
            s.rect(bx, 90, 60, 60, fill=BG, stroke=c, r=10); s.text(bx + 30, 130, v, 30, TX, weight="700"); s.text(bx + 30, 168, nm, 12, DIM)
        s.text(x + 110, 200, "the state is written %s" % ("10" if k == 0 else "01"), 11.5, DIM)
    return s


def uses_map():
    s = Svg(640, 260, "What quantum is for", "Promising: chemistry, search speedups, factoring and optimisation ideas. Not for: games, email, web browsing.")
    s.text(320, 24, "A special tool, not a faster everything", 15, VIO, weight="700")
    s.rect(20, 44, 300, 190, fill=PANEL, stroke=GRN); s.text(170, 68, "Promising jobs", 14, GRN, weight="700")
    for i, t in enumerate(["Simulating molecules", "Searching without a map (Grover)", "Factoring big numbers (Shor)", "Some optimisation ideas"]):
        s.text(40, 104 + i * 30, "✓ " + t, 13, TX, anchor="start")
    s.rect(340, 44, 280, 190, fill=PANEL, stroke=RED); s.text(480, 68, "Not what it is for", 14, RED, weight="700")
    for i, t in enumerate(["Playing games faster", "Email and web pages", "Everyday apps", "Trying every answer at once"]):
        s.text(360, 104 + i * 30, "✗ " + t, 13, TX, anchor="start")
    return s


ALL = {
    "qm-filters.svg": qm_filters, "qm-ball-electron.svg": qm_ball_vs_electron, "bits-vs-qubits.svg": bits_vs_qubits, "bits-double.svg": bits_double,
    "qubit-squares.svg": qubit_squares, "gates-effect.svg": gates_effect, "interference-waves.svg": interference_waves, "interference-paths.svg": interference_paths,
    "bloch-sphere.svg": bloch_sphere, "bloch-gates.svg": bloch_gates, "circuit-read.svg": circuit_read, "cnot-table.svg": cnot_table, "bell-pair.svg": bell_pair,
    "grover-bars.svg": grover_bars, "shots-wobble.svg": shots_wobble, "qasm-vs-circuit.svg": qasm_vs_circuit, "qiskit-pipeline.svg": qiskit_pipeline,
    "endian.svg": endian, "uses-map.svg": uses_map,
}


def build_all(outdir="/tmp/qc_figs"):
    os.makedirs(outdir, exist_ok=True)
    res = {}
    for fn, f in ALL.items():
        svg = f().render()
        open(os.path.join(outdir, fn), "w", encoding="utf-8").write(svg)
        res[fn] = svg
    return res


if __name__ == "__main__":
    print(len(build_all()), "figures")
