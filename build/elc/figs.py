"""Original SVG figures for the electronics course (no third-party artwork)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from make_images import Svg, BG, PANEL, LINE, TX, DIM, VIO, PINK, BLUE, GRN, AMB, RED  # noqa: E402

W = "#efe9ff"   # wire / part outline


def wire(s, pts, color=W, sw=2):
    s.add('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"/>' % (" ".join("%s,%s" % p for p in pts), color, sw))


def dot(s, x, y, color=W, r=3.5):
    s.add('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (x, y, r, color))


def zig(s, x1, x2, y, color=AMB, amp=8, n=6, sw=2.2):
    """Horizontal resistor between x1 and x2 with 8px lead wires."""
    a, b = x1 + 10, x2 - 10
    pts = [(x1, y), (a, y)]
    step = (b - a) / float(n)
    for i in range(n):
        pts.append((a + step * (i + 0.5), y + (amp if i % 2 == 0 else -amp)))
    pts += [(b, y), (x2, y)]
    wire(s, pts, color, sw)


def zig_v(s, y1, y2, x, color=AMB, amp=8, n=6, sw=2.2):
    a, b = y1 + 10, y2 - 10
    pts = [(x, y1), (x, a)]
    step = (b - a) / float(n)
    for i in range(n):
        pts.append((x + (amp if i % 2 == 0 else -amp), a + step * (i + 0.5)))
    pts += [(x, b), (x, y2)]
    wire(s, pts, color, sw)


def battery_v(s, x, y1, y2, label="", color=RED):
    """Vertical battery: + on top."""
    m = (y1 + y2) / 2.0
    wire(s, [(x, y1), (x, m - 8)], W)
    wire(s, [(x, m + 8), (x, y2)], W)
    s.line(x - 16, m - 8, x + 16, m - 8, color, 3)
    s.line(x - 9, m + 8, x + 9, m + 8, color, 3)
    s.text(x - 24, m - 12, "+", 14, color, weight="700")
    if label:
        s.text(x + 28, m + 4, label, 13, TX, anchor="start")


def cap_h(s, x, y, color=BLUE, gap=10, h=16):
    s.line(x - gap / 2.0, y - h, x - gap / 2.0, y + h, color, 3)
    s.line(x + gap / 2.0, y - h, x + gap / 2.0, y + h, color, 3)


def gnd(s, x, y):
    wire(s, [(x, y), (x, y + 8)], W)
    s.line(x - 14, y + 8, x + 14, y + 8, W, 2.2)
    s.line(x - 9, y + 13, x + 9, y + 13, W, 2.2)
    s.line(x - 4, y + 18, x + 4, y + 18, W, 2.2)


def diode_h(s, x, y, color=PINK, size=12):
    s.add('<polygon points="%s,%s %s,%s %s,%s" fill="none" stroke="%s" stroke-width="2.2"/>' % (x - size, y - size, x - size, y + size, x + size, y, color))
    s.line(x + size, y - size, x + size, y + size, color, 3)


def save(d, name, s):
    with open(os.path.join(d, name), "w", encoding="utf-8") as f:
        f.write(s.render())


def abstraction_tower(d):
    s = Svg(640, 372, "Layers of abstraction", "From physics up to software: each layer hides the details of the one below it.")
    s.text(320, 24, "Each layer hides the one below", 15, VIO, weight="700")
    names = [("Software and systems", "operating systems, apps", BLUE), ("Processors", "instruction set abstraction", BLUE), ("Digital logic", "gates, flip-flops, clocks", GRN),
             ("Amplifiers and gates", "op-amp and digital abstractions", AMB), ("Lumped circuits", "R, C, L, sources: just algebra", PINK), ("Physics", "Maxwell's equations, electrons", VIO)]
    y = 40
    for i, (a, b, c) in enumerate(names):
        w = 560 - i * 22
        s.box(320 - w / 2.0, y, w, 40, a, b, c)
        y += 47
    s.add('<text x="22" y="362" font-size="11" fill="%s">This course lives in the middle: from lumped circuits up to gates and amplifiers.</text>' % DIM)
    return s


def lumped_bulb(d):
    s = Svg(640, 250, "A bulb replaced by a resistor", "On the left a light bulb with a filament between terminals A and B; on the right the same bulb drawn as a resistor R with voltage V and current I.")
    s.text(160, 26, "The real object", 14, VIO, weight="700")
    s.text(480, 26, "The lumped abstraction", 14, VIO, weight="700")
    s.add('<circle cx="160" cy="110" r="52" fill="#2a1f45" stroke="%s" stroke-width="2.2"/>' % W)
    wire(s, [(135, 160), (135, 118), (148, 100), (160, 120), (172, 100), (185, 118), (185, 160)], AMB, 2.4)
    s.line(135, 160, 135, 190, W, 2.4)
    s.line(185, 160, 185, 190, W, 2.4)
    s.text(135, 208, "A", 13, TX)
    s.text(185, 208, "B", 13, TX)
    s.text(160, 236, "shape, heat, light, color...", 11, DIM)
    s.arrow(250, 120, 370, 120, VIO)
    s.text(310, 108, "ignore all but V and I", 11, DIM)
    wire(s, [(480, 70), (480, 80)], W)
    zig_v(s, 80, 180, 480)
    wire(s, [(480, 180), (480, 196)], W)
    dot(s, 480, 70)
    dot(s, 480, 196)
    s.text(462, 70, "A", 13, TX, anchor="end")
    s.text(462, 200, "B", 13, TX, anchor="end")
    s.text(500, 135, "R", 15, AMB, anchor="start", weight="700")
    s.text(540, 100, "I = V / R", 15, TX, anchor="start", weight="700")
    s.text(540, 124, "only the v-i", 11, DIM, anchor="start")
    s.text(540, 138, "relationship is kept", 11, DIM, anchor="start")
    return s


def kvl_kcl(d):
    s = Svg(640, 270, "Kirchhoff's laws", "Left: voltages around a loop add to zero. Right: currents into a node add to zero.")
    s.text(160, 24, "Loop: the voltages add to zero", 14, VIO, weight="700")
    s.text(480, 24, "Node: the currents add to zero", 14, VIO, weight="700")
    s.rect(60, 50, 200, 160, fill="none", stroke=W, r=4, sw=2)
    for (x, y, t) in [(160, 50, "v1"), (260, 130, "v2"), (160, 210, "v3"), (60, 130, "v4")]:
        s.add('<rect x="%s" y="%s" width="34" height="22" rx="6" fill="#2a1f45" stroke="%s"/>' % (x - 17, y - 11, VIO))
        s.text(x, y + 5, t, 13, TX)
    s.text(160, 240, "v1 + v2 + v3 + v4 = 0", 14, TX, weight="700")
    dot(s, 480, 120, AMB, 6)
    for (x2, y2, t, inward) in [(400, 70, "i1", True), (400, 170, "i2", True), (570, 120, "i3", False)]:
        if inward:
            s.arrow(x2, y2, 474, 120, W)
        else:
            s.arrow(486, 120, x2, y2, W)
        s.text(x2 + (-6 if inward else 6), y2 - 8, t, 13, TX, anchor="middle")
    s.text(480, 240, "i1 + i2 = i3", 14, TX, weight="700")
    s.text(480, 258, "(in = out)", 11, DIM)
    return s


def series_parallel(d):
    s = Svg(640, 250, "Series and parallel", "Two circuits with a battery: two resistors in series, and two resistors in parallel.")
    s.text(160, 22, "Series: one path, same current", 13, VIO, weight="700")
    s.text(480, 22, "Parallel: same voltage, two paths", 13, VIO, weight="700")
    # series
    battery_v(s, 50, 60, 200, "V")
    wire(s, [(50, 60), (130, 60)]); zig(s, 130, 200, 60); wire(s, [(200, 60), (240, 60), (240, 80)])
    zig_v(s, 80, 160, 240, color=GRN); wire(s, [(240, 160), (240, 200), (50, 200)])
    s.text(165, 48, "R1", 13, AMB); s.text(262, 125, "R2", 13, GRN, anchor="start")
    s.text(160, 232, "R = R1 + R2", 14, TX, weight="700")
    # parallel
    battery_v(s, 380, 60, 200, "V")
    wire(s, [(380, 60), (480, 60)]); wire(s, [(480, 60), (560, 60)])
    zig_v(s, 60, 200, 480, amp=8, n=8); zig_v(s, 60, 200, 560, color=GRN, amp=8, n=8)
    wire(s, [(480, 200), (560, 200)]); wire(s, [(380, 200), (480, 200)])
    dot(s, 480, 60); dot(s, 480, 200)
    s.text(500, 135, "R1", 13, AMB, anchor="start"); s.text(578, 135, "R2", 13, GRN, anchor="start")
    s.text(480, 232, "1/R = 1/R1 + 1/R2", 14, TX, weight="700")
    return s


def resistor_code(d):
    s = Svg(640, 280, "Resistor color code", "A resistor with brown, black, red and gold bands, which means 1000 ohms with 5 percent tolerance, and the digit table.")
    s.text(320, 24, "Brown, black, red, gold = 10 x 100 = 1000 ohms, 5 percent", 14, VIO, weight="700")
    wire(s, [(40, 80), (100, 80)], W, 3)
    wire(s, [(440, 80), (500, 80)], W, 3)
    s.add('<rect x="100" y="55" width="340" height="50" rx="22" fill="#c9a66b" stroke="#8d7040" stroke-width="2"/>')
    for x, c in [(140, "#6b3b12"), (190, "#111"), (240, "#d33"), (380, "#d4af37")]:
        s.add('<rect x="%s" y="55" width="16" height="50" fill="%s"/>' % (x, c))
    for x, t in [(148, "1"), (198, "0"), (248, "x100"), (388, "5%")]:
        s.text(x, 130, t, 12, TX)
    cols = [("black", "#111", 0), ("brown", "#6b3b12", 1), ("red", "#d33", 2), ("orange", "#f80", 3), ("yellow", "#ee3", 4), ("green", "#3a3", 5), ("blue", "#35e", 6), ("violet", "#93c", 7), ("gray", "#999", 8), ("white", "#fff", 9)]
    for i, (n, c, v) in enumerate(cols):
        x = 40 + i * 58
        s.add('<rect x="%s" y="170" width="46" height="34" rx="6" fill="%s" stroke="%s"/>' % (x, c, LINE))
        s.text(x + 23, 226, str(v), 15, TX, weight="700")
        s.text(x + 23, 244, n, 10.5, DIM)
    s.text(320, 268, "Gold = 5 percent, silver = 10 percent. The third band is the multiplier (number of zeros).", 11, DIM)
    return s


def divider(d):
    s = Svg(640, 270, "Voltage divider", "Two resistors in series from Vin to ground with Vout taken from the junction.")
    s.text(320, 24, "Two resistors share the voltage", 14, VIO, weight="700")
    s.text(130, 55, "Vin", 14, TX)
    wire(s, [(130, 70), (130, 80)]); dot(s, 130, 70, RED)
    zig_v(s, 80, 150, 130); s.text(152, 120, "R1", 14, AMB, anchor="start")
    wire(s, [(130, 150), (130, 160)]); dot(s, 130, 155)
    wire(s, [(130, 155), (240, 155)]); dot(s, 240, 155, GRN, 5)
    s.text(256, 159, "Vout", 14, GRN, anchor="start")
    zig_v(s, 160, 230, 130, color=GRN); s.text(152, 200, "R2", 14, GRN, anchor="start")
    gnd(s, 130, 230)
    s.add('<rect x="340" y="70" width="270" height="150" rx="12" fill="#1c1530" stroke="%s"/>' % LINE)
    s.text(475, 112, "Vout = Vin x R2 / (R1 + R2)", 14, TX, weight="700")
    s.text(475, 142, "9 V, R1 = 1k, R2 = 2k", 12, DIM)
    s.text(475, 164, "Vout = 9 x 2000 / 3000 = 6 V", 13, AMB, weight="600")
    s.text(475, 198, "Load the output and it sags.", 12, DIM)
    return s


def rc_curve(d):
    s = Svg(640, 290, "RC charging", "A resistor and capacitor circuit and the charging curve, reaching 63 percent of the supply after one time constant.")
    s.text(320, 22, "Charging a capacitor through a resistor", 14, VIO, weight="700")
    wire(s, [(40, 70), (80, 70)]); zig(s, 80, 150, 70); wire(s, [(150, 70), (190, 70), (190, 100)])
    cap_h(s, 190, 118, BLUE); s.line(190, 100, 190, 110, W, 2); s.line(190, 126, 190, 140, W, 2)
    # vertical cap
    s.add('<line x1="170" y1="110" x2="210" y2="110" stroke="%s" stroke-width="3"/><line x1="170" y1="126" x2="210" y2="126" stroke="%s" stroke-width="3"/>' % (BLUE, BLUE))
    wire(s, [(190, 140), (190, 200), (40, 200)]); battery_v(s, 40, 70, 200, "")
    s.text(115, 55, "R", 13, AMB); s.text(222, 122, "C", 13, BLUE, anchor="start"); s.text(14, 140, "Vs", 13, RED)
    x0, y0, w, h = 300, 50, 300, 170
    s.line(x0, y0 + h, x0 + w, y0 + h, DIM, 1.5); s.line(x0, y0, x0, y0 + h, DIM, 1.5)
    pts = []
    for i in range(0, 61):
        t = i / 60.0 * 5.0
        pts.append((x0 + t / 5.0 * w, y0 + h - h * (1 - math.exp(-t))))
    wire(s, pts, VIO, 2.6)
    s.line(x0, y0 + h * (1 - 0.63), x0 + w / 5.0, y0 + h * (1 - 0.63), AMB, 1.2, "4,3")
    s.line(x0 + w / 5.0, y0 + h * (1 - 0.63), x0 + w / 5.0, y0 + h, AMB, 1.2, "4,3")
    s.text(x0 - 6, y0 + 6, "Vs", 11, TX, anchor="end"); s.text(x0 - 6, y0 + h * 0.37 + 4, "63%", 11, AMB, anchor="end")
    s.text(x0 + w / 5.0, y0 + h + 16, "1 tau", 11, AMB); s.text(x0 + w, y0 + h + 16, "5 tau", 11, TX, anchor="end")
    s.text(x0 + w / 2.0, y0 + h + 34, "time", 11, DIM)
    s.text(130, 245, "tau = R x C", 14, TX, weight="700")
    return s


def transformer(d):
    s = Svg(640, 250, "Transformer", "Two coils on an iron core. The voltage ratio equals the turns ratio.")
    s.text(320, 22, "A transformer: Vs / Vp = Ns / Np", 14, VIO, weight="700")
    s.add('<rect x="250" y="60" width="140" height="130" rx="6" fill="none" stroke="%s" stroke-width="10" opacity="0.55"/>' % DIM)
    for (cx, c, label) in [(250, AMB, "Np"), (390, GRN, "Ns")]:
        for i in range(6):
            y = 80 + i * 18
            s.add('<path d="M%s,%s a10,9 0 1,1 0,18" fill="none" stroke="%s" stroke-width="2.6"/>' % (cx - 5 if cx == 250 else cx + 5, y, c))
        s.text(cx + (-36 if cx == 250 else 36), 135, label, 14, c)
    wire(s, [(100, 70), (245, 70)]); wire(s, [(100, 190), (245, 190)]); wire(s, [(100, 70), (100, 190)])
    wire(s, [(395, 70), (540, 70)]); wire(s, [(395, 190), (540, 190)]); wire(s, [(540, 70), (540, 190)])
    s.text(70, 135, "Vp", 14, AMB); s.text(570, 135, "Vs", 14, GRN)
    s.text(320, 228, "Few turns on the output: step down. More turns: step up. Only AC passes.", 11.5, DIM)
    return s


def diode_iv(d):
    s = Svg(640, 270, "Diode and its I-V curve", "A diode symbol and a current-voltage curve showing the knee near 0.7 volts.")
    s.text(320, 22, "A diode passes current one way", 14, VIO, weight="700")
    wire(s, [(30, 90), (95, 90)]); diode_h(s, 115, 90); wire(s, [(127, 90), (200, 90)])
    s.text(70, 76, "anode", 11, DIM); s.text(165, 76, "cathode", 11, DIM)
    s.arrow(60, 125, 190, 125, GRN); s.text(125, 145, "forward current", 11, GRN)
    x0, y0 = 400, 150
    s.line(250, y0, 620, y0, DIM, 1.5); s.line(x0, 45, x0, 245, DIM, 1.5)
    wire(s, [(250, y0), (x0 + 40, y0)], VIO, 2.6)
    pts = [(x0 + 40 + i * 4, y0 - (math.exp(i * 0.16) - 1) * 1.1) for i in range(0, 38)]
    pts = [p for p in pts if p[1] > 45]
    wire(s, pts, VIO, 2.6)
    s.line(x0 + 40, y0, x0 + 40, y0 + 14, AMB, 1.5, "3,3"); s.text(x0 + 40, y0 + 28, "0.7 V knee", 11, AMB)
    s.text(612, y0 + 16, "V", 12, TX); s.text(x0 + 10, 56, "I", 12, TX)
    s.text(300, 175, "reverse: almost no current", 11, DIM)
    return s


def rectify(d):
    s = Svg(640, 300, "Rectification", "An AC sine wave, the same wave after a half-wave rectifier and after a full-wave bridge.")
    s.text(320, 20, "Rectifying AC", 14, VIO, weight="700")
    for k, (label, kind) in enumerate([("AC in", "sine"), ("Half-wave (one diode)", "half"), ("Full-wave (bridge)", "full")]):
        y = 85 + k * 80
        s.line(40, y, 600, y, LINE, 1)
        pts = []
        for i in range(0, 121):
            t = i / 120.0 * 2 * 2 * math.pi
            v = math.sin(t)
            if kind == "half": v = max(0, v)
            if kind == "full": v = abs(v)
            pts.append((40 + i * 4.66, y - v * 30))
        wire(s, pts, [BLUE, AMB, GRN][k], 2.4)
        s.text(40, y - 40, label, 12, TX, anchor="start", weight="600")
    return s


def led_resistor(d):
    s = Svg(640, 250, "LED with a series resistor", "A battery, a resistor and an LED in a loop. The resistor value is (supply minus LED voltage) divided by the current.")
    s.text(320, 22, "An LED always needs a resistor", 14, VIO, weight="700")
    battery_v(s, 60, 50, 200, "9 V")
    wire(s, [(60, 50), (110, 50)]); zig(s, 110, 220, 50); wire(s, [(220, 50), (300, 50)])
    # LED pointing down
    s.add('<polygon points="288,70 312,70 300,95" fill="none" stroke="%s" stroke-width="2.4"/>' % PINK)
    s.line(288, 95, 312, 95, PINK, 3)
    wire(s, [(300, 50), (300, 70)]); wire(s, [(300, 95), (300, 200), (60, 200)])
    s.arrow(320, 60, 352, 42, AMB); s.arrow(328, 80, 360, 62, AMB)
    s.text(165, 36, "R", 14, AMB)
    s.text(430, 90, "R = (Vs - Vf) / I", 15, TX, weight="700", anchor="start")
    s.text(430, 116, "= (9 - 2) / 0.015", 13, DIM, anchor="start")
    s.text(430, 140, "= 467 ohms, use 470", 13, AMB, anchor="start", weight="600")
    return s


def npn_switch(d):
    s = Svg(640, 290, "Transistor as a switch", "An NPN transistor with a base resistor switching a lamp. A small base current turns on the larger collector current.")
    s.text(320, 22, "A small base current switches a bigger load", 14, VIO, weight="700")
    wire(s, [(300, 40), (300, 70)]); dot(s, 300, 40, RED); s.text(320, 44, "+V", 13, TX, anchor="start")
    s.add('<circle cx="300" cy="100" r="22" fill="#2a1f45" stroke="%s" stroke-width="2.2"/>' % AMB)
    s.line(286, 86, 314, 114, AMB, 2); s.line(314, 86, 286, 114, AMB, 2)
    s.text(334, 104, "lamp", 12, DIM, anchor="start")
    wire(s, [(300, 122), (300, 150), (300, 160)])
    s.line(280, 160, 280, 220, W, 4); wire(s, [(280, 175), (300, 160), (300, 150)]); wire(s, [(280, 205), (300, 220), (300, 245)])
    s.add('<polygon points="298,214 288,206 296,204" fill="%s"/>' % W)
    s.text(312, 160, "C", 12, DIM, anchor="start"); s.text(312, 232, "E", 12, DIM, anchor="start"); s.text(262, 195, "B", 12, DIM, anchor="end")
    wire(s, [(70, 190), (100, 190)]); zig(s, 100, 190, 190); wire(s, [(190, 190), (280, 190)])
    s.text(145, 172, "Rb", 13, AMB); s.text(70, 182, "input", 12, TX, anchor="end")
    gnd(s, 300, 245)
    s.add('<rect x="420" y="70" width="200" height="140" rx="12" fill="#1c1530" stroke="%s"/>' % LINE)
    for i, t in enumerate(["Ic = beta x Ib", "drive hard: Ib about Ic/(beta/10)", "Rb = (Vin - 0.7) / Ib", "Vce falls to a few tenths", "of a volt when saturated"]):
        s.text(520, 100 + i * 24, t, 11.5, TX if i < 3 else DIM)
    return s


def waveforms(d):
    s = Svg(640, 292, "Waves and pulses", "A sine wave with its period and amplitude marked, and a pulse train with the duty cycle marked.")
    s.text(160, 20, "Sine wave", 13, VIO, weight="700"); s.text(480, 20, "Pulse train", 13, VIO, weight="700")
    y = 130
    s.line(20, y, 300, y, LINE, 1)
    pts = [(20 + i * 2.8, y - 60 * math.sin(i / 100.0 * 2 * math.pi * 1.5)) for i in range(101)]
    wire(s, pts, BLUE, 2.6)
    s.line(20, y - 60, 300, y - 60, DIM, 1, "3,3"); s.text(300, y - 66, "peak", 11, DIM, anchor="end")
    s.arrow(20, 235, 113, 235, AMB); s.arrow(113, 235, 20, 235, AMB); s.text(66, 253, "period T = 1/f", 11.5, AMB)
    s.text(160, 272, "RMS = peak / 1.414", 11.5, TX)
    y2 = 190
    s.line(340, y2, 620, y2, LINE, 1)
    xs = 340
    pts = []
    for k in range(4):
        x = 340 + k * 70
        pts += [(x, y2), (x, y2 - 80), (x + 28, y2 - 80), (x + 28, y2)]
    pts.append((620, y2))
    wire(s, pts, GRN, 2.6)
    s.arrow(340, 75, 368, 75, AMB); s.arrow(368, 75, 340, 75, AMB); s.text(354, 66, "on", 11, AMB)
    s.arrow(340, 235, 410, 235, PINK); s.arrow(410, 235, 340, 235, PINK); s.text(375, 253, "period", 11.5, PINK)
    s.text(480, 276, "duty = on / period = 40%", 12, TX, weight="600")
    return s


def gate_symbols(d):
    s = Svg(640, 300, "Logic gate symbols", "Symbols and truth tables for AND, OR, NOT, NAND and XOR gates.")
    s.text(320, 20, "Logic gates", 14, VIO, weight="700")
    gates = [("AND", "0 0 0 1"), ("OR", "0 1 1 1"), ("NOT", "1 0"), ("NAND", "1 1 1 0"), ("XOR", "0 1 1 0")]
    for i, (n, tt) in enumerate(gates):
        x = 30 + i * 122
        y = 90
        if n in ("AND", "NAND"):
            s.add('<path d="M%s,%s h26 a26,26 0 0,1 0,52 h-26 z" fill="#2a1f45" stroke="%s" stroke-width="2.2"/>' % (x, y, VIO))
        elif n in ("OR", "XOR"):
            s.add('<path d="M%s,%s q12,26 0,52 q38,0 54,-26 q-16,-26 -54,-26 z" fill="#2a1f45" stroke="%s" stroke-width="2.2"/>' % (x, y, VIO))
            if n == "XOR":
                s.add('<path d="M%s,%s q12,26 0,52" fill="none" stroke="%s" stroke-width="2.2"/>' % (x - 7, y, VIO))
        else:
            s.add('<polygon points="%s,%s %s,%s %s,%s" fill="#2a1f45" stroke="%s" stroke-width="2.2"/>' % (x, y, x, y + 52, x + 44, y + 26, VIO))
        if n in ("NAND", "NOT"):
            s.add('<circle cx="%s" cy="%s" r="5" fill="%s" stroke="%s" stroke-width="2"/>' % (x + (54 if n == "NAND" else 49), y + 26, BG, VIO))
        s.text(x + 30, y - 12, n, 14, TX, weight="700")
        s.text(x + 30, y + 90, "out: " + tt if n != "NOT" else "in 0,1 -> " + tt, 11, AMB)
        s.text(x + 30, y + 110, "inputs 00 01 10 11" if n != "NOT" else "", 10, DIM)
    s.text(320, 270, "NAND is universal: every other gate can be built from NAND gates alone.", 12, DIM)
    return s


def opamp(d):
    s = Svg(640, 270, "Inverting op-amp", "An op-amp with a feedback resistor Rf and an input resistor Rin. The gain is minus Rf over Rin.")
    s.text(320, 22, "Feedback sets the gain", 14, VIO, weight="700")
    s.add('<polygon points="260,80 260,190 360,135" fill="#2a1f45" stroke="%s" stroke-width="2.4"/>' % VIO)
    s.text(272, 112, "-", 18, TX); s.text(272, 168, "+", 18, TX)
    wire(s, [(40, 108), (80, 108)]); zig(s, 80, 170, 108); wire(s, [(170, 108), (260, 108)])
    s.text(125, 92, "Rin", 13, AMB); s.text(30, 112, "Vin", 13, TX, anchor="end")
    wire(s, [(360, 135), (460, 135)]); s.text(470, 139, "Vout", 13, TX, anchor="start")
    wire(s, [(215, 108), (215, 50), (410, 50), (410, 135)]); dot(s, 215, 108); dot(s, 410, 135)
    zig(s, 270, 350, 50, color=GRN); s.text(310, 38, "Rf", 13, GRN)
    wire(s, [(260, 162), (230, 162), (230, 200)]); gnd(s, 230, 200)
    s.text(500, 100, "gain = -Rf / Rin", 14, TX, anchor="start", weight="700")
    s.text(500, 124, "Rf = 100k, Rin = 10k:", 11.5, DIM, anchor="start")
    s.text(500, 144, "gain = -10", 13, AMB, anchor="start", weight="600")
    return s


def timer555(d):
    s = Svg(640, 300, "555 astable circuit", "A 555 timer with resistors R1 and R2 and a capacitor C making a free-running oscillator.")
    s.text(320, 22, "555 astable oscillator", 14, VIO, weight="700")
    s.rect(230, 60, 140, 170, fill="#2a1f45", stroke=VIO, r=8, sw=2.2)
    s.text(300, 150, "555", 22, TX, weight="700")
    pins = [("1 GND", 230, 210, "L"), ("2 TRIG", 230, 180, "L"), ("3 OUT", 370, 150, "R"), ("4 RST", 230, 90, "L"), ("5 CTRL", 370, 200, "R"), ("6 THR", 230, 150, "L"), ("7 DIS", 230, 120, "L"), ("8 VCC", 370, 90, "R")]
    for (n, x, y, side) in pins:
        s.text(x + (10 if side == "L" else -10), y + 4, n, 9.5, DIM, anchor="start" if side == "L" else "end")
    wire(s, [(100, 60), (400, 60)], RED); s.text(80, 64, "+V", 12, RED, anchor="end")
    wire(s, [(300, 60), (300, 60)]); wire(s, [(370, 90), (400, 90), (400, 60)])
    zig_v(s, 60, 110, 150); wire(s, [(150, 110), (150, 120), (230, 120)]); s.text(172, 90, "R1", 12, AMB, anchor="start")
    zig_v(s, 120, 170, 150, color=GRN); s.text(172, 150, "R2", 12, GRN, anchor="start")
    wire(s, [(150, 170), (170, 170)]); wire(s, [(170, 170), (170, 150), (230, 150)]); wire(s, [(170, 170), (170, 180), (230, 180)])
    wire(s, [(150, 170), (150, 200)]); s.line(135, 200, 165, 200, BLUE, 3); s.line(135, 210, 165, 210, BLUE, 3); wire(s, [(150, 210), (150, 240)]); gnd(s, 150, 240)
    s.text(176, 208, "C", 12, BLUE, anchor="start")
    wire(s, [(230, 90), (200, 90), (200, 60)]); wire(s, [(230, 210), (210, 210), (210, 250)]); gnd(s, 210, 250)
    wire(s, [(370, 150), (440, 150)]); s.text(450, 154, "out", 12, TX, anchor="start")
    s.text(500, 210, "f = 1.44 / ((R1 + 2 R2) C)", 12, TX, anchor="middle", weight="600")
    s.text(500, 230, "duty = (R1 + R2) / (R1 + 2 R2)", 11, DIM)
    return s


def breadboard(d):
    s = Svg(640, 270, "Solderless breadboard", "A breadboard with power rails along the top and bottom and rows of five connected holes. An LED and resistor sit across the middle gap.")
    s.text(320, 20, "A solderless breadboard", 14, VIO, weight="700")
    s.rect(30, 36, 580, 200, fill="#d9d2c0", stroke="#9d957f", r=8)
    for r, (y, c) in enumerate([(50, RED), (62, "#2a58d9")]):
        s.line(40, y - 8, 600, y - 8, c, 1)
        for i in range(25):
            s.add('<rect x="%s" y="%s" width="7" height="7" fill="#444"/>' % (50 + i * 22, y - 3))
    for r, (y, c) in enumerate([(210, RED), (222, "#2a58d9")]):
        for i in range(25):
            s.add('<rect x="%s" y="%s" width="7" height="7" fill="#444"/>' % (50 + i * 22, y - 3))
    s.add('<rect x="40" y="124" width="560" height="10" fill="#bdb6a2"/>')
    for i in range(25):
        for j in range(5):
            s.add('<rect x="%s" y="%s" width="7" height="7" fill="#444"/>' % (50 + i * 22, 80 + j * 9 + (0 if j < 5 else 0)))
            s.add('<rect x="%s" y="%s" width="7" height="7" fill="#444"/>' % (50 + i * 22, 140 + j * 9))
    s.line(94, 76, 94, 188, "#e33", 1, "2,3")
    s.add('<rect x="70" y="105" width="44" height="12" rx="5" fill="#c9a66b" stroke="#8d7040"/>')
    s.add('<circle cx="160" cy="150" r="9" fill="#ff7777" stroke="#900"/>')
    s.text(320, 258, "Holes in a column of five are joined; the rails run along the whole length; the middle gap separates the two halves.", 10.5, DIM)
    return s


def arduino_uno(d):
    s = Svg(640, 340, "Arduino Uno layout", "A simplified Arduino Uno showing the USB socket, the power header, digital pins 0 to 13 with PWM pins marked, and analog pins A0 to A5.")
    s.text(320, 20, "Arduino Uno: where the pins are", 14, VIO, weight="700")
    s.rect(60, 40, 520, 270, fill="#0f6a6a", stroke="#064", r=14, sw=2)
    s.rect(60, 90, 60, 70, fill="#9aa", stroke="#566", r=4); s.text(90, 130, "USB", 11, "#123")
    s.rect(60, 210, 50, 60, fill="#111", stroke="#555", r=4); s.text(85, 245, "DC in", 10, TX)
    s.rect(300, 150, 100, 110, fill="#222", stroke="#555", r=4); s.text(350, 200, "ATmega328P", 11, TX); s.text(350, 216, "5 V, 16 MHz", 10, DIM)
    # digital header top
    s.text(320, 66, "Digital pins (~ = PWM)", 11, TX)
    labels = ["0", "1", "2", "~3", "4", "~5", "~6", "7", "8", "~9", "~10", "~11", "12", "13"]
    for i, l in enumerate(labels):
        x = 180 + i * 28
        s.add('<rect x="%s" y="72" width="16" height="20" fill="#111" stroke="#777"/>' % (x - 8))
        s.text(x, 106, l, 10.5, AMB if "~" in l else TX)
    s.text(150, 90, "GND AREF", 9, DIM, anchor="end")
    # power header bottom left
    pw = ["RESET", "3V3", "5V", "GND", "GND", "VIN"]
    s.text(230, 270, "Power", 11, TX)
    for i, l in enumerate(pw):
        x = 170 + i * 36
        s.add('<rect x="%s" y="276" width="16" height="20" fill="#111" stroke="#777"/>' % (x - 8))
        s.text(x, 308, l, 9.5, RED if l in ("5V", "3V3", "VIN") else TX)
    an = ["A0", "A1", "A2", "A3", "A4", "A5"]
    s.text(500, 270, "Analog in", 11, TX)
    for i, l in enumerate(an):
        x = 420 + i * 27
        s.add('<rect x="%s" y="276" width="16" height="20" fill="#111" stroke="#777"/>' % (x - 8))
        s.text(x, 308, l, 9.5, BLUE)
    s.add('<circle cx="540" cy="120" r="8" fill="#ff9d3c"/>'); s.text(540, 142, "pin 13 LED", 10, TX)
    s.text(160, 190, "Reset", 11, TX); s.add('<circle cx="190" cy="165" r="9" fill="#c33" stroke="#511"/>')
    return s


def arduino_led(d):
    s = Svg(640, 260, "LED on an Arduino pin", "Pin 13 connects through a 220 ohm resistor to an LED and then to ground.")
    s.text(320, 22, "Blink: pin 13 to resistor to LED to GND", 14, VIO, weight="700")
    s.rect(30, 60, 120, 140, fill="#0f6a6a", stroke="#064", r=10, sw=2)
    s.text(90, 120, "Arduino", 13, TX, weight="700"); s.text(90, 140, "Uno", 12, TX)
    wire(s, [(150, 90), (200, 90)]); s.text(150, 80, "pin 13", 10.5, TX, anchor="start")
    zig(s, 200, 300, 90); s.text(250, 72, "220 ohm", 11.5, AMB)
    wire(s, [(300, 90), (380, 90)])
    s.add('<polygon points="380,78 380,102 404,90" fill="none" stroke="%s" stroke-width="2.4"/>' % PINK); s.line(404, 78, 404, 102, PINK, 3)
    s.arrow(400, 68, 424, 50, AMB); s.arrow(412, 76, 436, 58, AMB)
    wire(s, [(404, 90), (470, 90), (470, 200), (150, 200)]); s.text(150, 216, "GND", 10.5, TX, anchor="start")
    s.text(330, 150, "digitalWrite(13, HIGH) puts 5 V on the pin", 11.5, TX)
    s.text(330, 170, "Current = (5 - 2) / 220 = about 14 mA", 11.5, AMB)
    s.text(330, 190, "(an Uno pin can give about 20 mA)", 10.5, DIM)
    return s


def arduino_ldr(d):
    s = Svg(640, 270, "Reading a light sensor", "A photoresistor and a fixed resistor form a voltage divider between 5 volts and ground, with the middle point wired to analog pin A0.")
    s.text(320, 22, "analogRead(A0) reads the divider", 14, VIO, weight="700")
    wire(s, [(160, 50), (160, 60)]); dot(s, 160, 50, RED); s.text(180, 54, "5V", 13, TX, anchor="start")
    zig_v(s, 60, 130, 160); s.text(184, 100, "LDR", 12, AMB, anchor="start")
    wire(s, [(160, 130), (160, 140)]); dot(s, 160, 140, GRN, 5); wire(s, [(160, 140), (260, 140)]); s.text(272, 144, "to A0", 12, GRN, anchor="start")
    zig_v(s, 140, 210, 160, color=GRN); s.text(184, 180, "10k", 12, GRN, anchor="start")
    gnd(s, 160, 210)
    s.arrow(110, 70, 140, 90, AMB); s.arrow(104, 90, 134, 108, AMB)
    s.add('<rect x="380" y="60" width="230" height="150" rx="12" fill="#1c1530" stroke="%s"/>' % LINE)
    for i, t in enumerate(["Bright: LDR small", "A0 voltage high, value near 1023", "Dark: LDR large", "A0 voltage low, value near 0", "value = volts / 5 x 1023"]):
        s.text(495, 90 + i * 28, t, 11.5, TX if i % 2 == 0 else AMB)
    return s


def pwm(d):
    s = Svg(640, 290, "PWM duty cycles", "Three pulse trains with 25, 50 and 75 percent duty and their average voltages of 1.25, 2.5 and 3.75 volts.")
    s.text(320, 20, "PWM: average voltage = duty x 5 V", 14, VIO, weight="700")
    for k, (duty, lab) in enumerate([(0.25, "analogWrite(9, 64)   25%  avg 1.25 V"), (0.5, "analogWrite(9, 128)  50%  avg 2.5 V"), (0.75, "analogWrite(9, 191)  75%  avg 3.75 V")]):
        y = 90 + k * 80
        pts = []
        for i in range(5):
            x = 40 + i * 80
            pts += [(x, y), (x, y - 40), (x + 80 * duty, y - 40), (x + 80 * duty, y)]
        pts.append((440, y))
        wire(s, pts, GRN, 2.4)
        s.line(40, y - 40 * duty, 440, y - 40 * duty, AMB, 1.2, "5,4")
        s.text(450, y - 14, lab, 11, TX, anchor="start")
    return s


def flipflop(d):
    s = Svg(640, 250, "D flip-flop timing", "A timing diagram of a D flip-flop: Q copies D only on rising clock edges.")
    s.text(320, 20, "D flip-flop: Q copies D on the rising clock edge", 14, VIO, weight="700")
    rows = [("CLK", [0, 1, 0, 1, 0, 1, 0, 1], BLUE), ("D", [1, 1, 0, 0, 1, 1, 0, 0], AMB), ("Q", [0, 1, 1, 0, 0, 1, 1, 0], GRN)]
    for k, (n, vals, c) in enumerate(rows):
        y = 90 + k * 60
        s.text(40, y - 6, n, 13, TX, anchor="end")
        pts = []
        for i, v in enumerate(vals):
            x = 60 + i * 70
            yy = y - 30 * v
            if i == 0:
                pts.append((x, yy))
            else:
                pts.append((x, y - 30 * vals[i - 1]))
                pts.append((x, yy))
            pts.append((x + 70, yy))
        wire(s, pts, c, 2.4)
    for i in range(1, 8, 2):
        s.line(60 + i * 70, 50, 60 + i * 70, 215, DIM, 1, "3,4")
    s.text(320, 238, "Dotted lines: rising edges, when the flip-flop looks at D.", 11, DIM)
    return s


ALL = dict(
    abstraction_tower=("abstraction-tower.svg", abstraction_tower), lumped_bulb=("lumped-bulb.svg", lumped_bulb), kvl_kcl=("kvl-kcl.svg", kvl_kcl),
    series_parallel=("series-parallel.svg", series_parallel), resistor_code=("resistor-code.svg", resistor_code), divider=("divider.svg", divider),
    rc_curve=("rc-curve.svg", rc_curve), transformer=("transformer.svg", transformer), diode_iv=("diode-iv.svg", diode_iv), rectify=("rectify.svg", rectify),
    led_resistor=("led-resistor.svg", led_resistor), npn_switch=("npn-switch.svg", npn_switch), waveforms=("waveforms.svg", waveforms), gate_symbols=("gate-symbols.svg", gate_symbols),
    flipflop=("flipflop.svg", flipflop), opamp=("opamp.svg", opamp), timer555=("timer555.svg", timer555), breadboard=("breadboard.svg", breadboard),
    arduino_uno=("arduino-uno.svg", arduino_uno), arduino_led=("arduino-led.svg", arduino_led), arduino_ldr=("arduino-ldr.svg", arduino_ldr), pwm=("pwm.svg", pwm),
)


def build_all(outdir=None):
    outdir = outdir or os.path.join(HERE, "img")
    os.makedirs(outdir, exist_ok=True)
    res = {}
    for key, (fn, f) in ALL.items():
        s = f(outdir)
        save(outdir, fn, s)
        res[fn] = open(os.path.join(outdir, fn), encoding="utf-8").read()
    return res


if __name__ == "__main__":
    r = build_all()
    print(len(r), "figures,", sum(len(v) for v in r.values()), "bytes")
