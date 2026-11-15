# -*- coding: utf-8 -*-
"""Verilog course figures, chapters 8-14."""
from fcommon import *
MONO = 'font-family="ui-monospace,Menlo,monospace"'


def always_map():
    s = Svg(640, 300, "What always blocks become", "always @* becomes combinational gates; always @(posedge clk) becomes flip-flops; a latch appears by accident when a path does not assign.")
    head(s, "Three always blocks, three kinds of hardware")
    cards = [("always @*", "if (s) y = b; else y = a;", "combinational logic", "a mux: no memory", GRN), ("always @(posedge clk)", "q <= d;", "flip-flops", "memory, updates on the edge", BLUE), ("always @* if (en) q = d;", "no else branch!", "a latch (usually a bug)", "q must remember when en = 0", RED)]
    for i, (a, b, c, d, col) in enumerate(cards):
        x = 20 + i * 205
        s.rect(x, 50, 195, 220, PANEL, col, 12, 2)
        s.text(x + 98, 76, a, 12, col, weight="700"); s.text(x + 98, 98, b, 11, TX, style=MONO)
        s.arrow(x + 98, 112, x + 98, 150, DIM)
        s.text(x + 98, 176, c, 13, TX, weight="700"); s.text(x + 98, 198, d, 10.5, DIM)
    s.text(320, 290, "Rule of thumb: assign a value on every path of a combinational block.", 11.5, DIM)
    return s


def blocking():
    s = Svg(660, 330, "Blocking and non-blocking assignment", "Swapping a and b with blocking assignments loses a value; with non-blocking assignments both right-hand sides are read first, so the swap works.")
    head(s, "a = b; b = a;   versus   a <= b; b <= a;")
    for i, (ttl, col, steps, res) in enumerate([("Blocking (=)", RED, ["start: a=3  b=5", "a = b;   a becomes 5 now", "b = a;   reads the NEW a: 5", "end: a=5  b=5"], "both 5: wrong"), ("Non-blocking (<=)", GRN, ["start: a=3  b=5", "read b (5) and a (3) first", "then update both together", "end: a=5  b=3"], "swapped: right")]):
        x = 20 + i * 325
        s.rect(x, 48, 305, 240, PANEL, col, 12, 2); s.text(x + 152, 74, ttl, 14, col, weight="700")
        for j, t in enumerate(steps):
            y = 100 + j * 44; s.rect(x + 18, y, 269, 34, BG, LINE, 8, 1.5); s.text(x + 152, y + 22, t, 12, TX, style=MONO)
            if j < 3: s.arrow(x + 152, y + 34, x + 152, y + 44, DIM, sw=1.4)
        s.text(x + 152, 282, res, 12.5, col, weight="700")
    s.text(330, 316, "Use <= in clocked blocks, = in combinational blocks. Never mix them in one block.", 11.5, DIM)
    return s


def scheduler():
    s = Svg(640, 300, "Simulator time step", "Within one time step the simulator evaluates active events and blocking assignments, then applies non-blocking updates, and repeats until nothing changes before time advances.")
    head(s, "Inside one simulation time step")
    steps = [("Active events", "run code, = now", BLUE), ("NBA updates", "<= land together", GRN), ("Re-evaluate", "changes wake blocks", AMB), ("Time advances", "nothing left to do", PINK)]
    for i, (t, sub, c) in enumerate(steps):
        x = 24 + i * 152; s.box(x, 70, 136, 80, t, sub, c)
        if i < 3: s.arrow(x + 136, 110, x + 152, 110, DIM)
    s.line(24 + 2 * 152 + 68, 70, 24 + 2 * 152 + 68, 48, AMB, 1.8); s.line(24 + 2 * 152 + 68, 48, 24 + 68, 48, AMB, 1.8); s.arrow(24 + 68, 48, 24 + 68, 70, AMB)
    s.text(200, 42, "repeat until stable (a delta cycle each time)", 11, AMB)
    s.rect(24, 190, 590, 80, "#0a0712", LINE, 10, 1.5)
    s.text(40, 214, "At posedge clk:  q1 <= d;   q2 <= q1;", 12.5, TX, anchor="start", style=MONO)
    s.text(40, 238, "Both read old values in the Active step; both update in the NBA step.", 11.5, DIM, anchor="start")
    s.text(40, 258, "So q2 gets the OLD q1: exactly like two real flip-flops in a chain.", 11.5, GRN, anchor="start")
    return s


def counter_wave():
    s = Svg(660, 280, "Counter waveform", "A 4-bit counter with a synchronous reset: count goes 0 1 2 3 then wraps after 15, shown against the clock.")
    head(s, "A 4-bit counter, clock by clock")
    n = 18; w = 540; x0 = 100; tw = w / n
    wave(s, x0, 50, w, "0" + "10" * 8 + "1", "clk", AMB, 22)
    wave(s, x0, 96, w, "1100000000000000000", "rst", PINK, 22)
    vals = ["0", "0", "1", "2", "3", "4", "5", "6", "7"]
    segs = []
    xs = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    for k in range(9):
        segs.append((x0 + xs[k] * tw, x0 + xs[k + 1] * tw, vals[k]))
    s.text(x0 - 8, 154, "count", 12, TX, anchor="end")
    for (xa, xb, t) in segs:
        path(s, "M%.1f 160 L%.1f 146 L%.1f 146 L%.1f 160 L%.1f 174 L%.1f 174 Z" % (xa + 3, xa + 7, xb - 7, xb - 3, xb - 7, xa + 7), AMB, 1.8); s.text((xa + xb) / 2, 164, t, 11, TX)
    for e in range(1, n, 2):
        s.line(x0 + e * tw, 44, x0 + e * tw, 180, LINE, 1, dash="3 4")
    s.text(x0 + 2 * tw, 206, "reset released", 11, PINK); s.text(x0 + 11 * tw, 206, "+1 at every rising edge (dashed)", 11, DIM)
    s.text(330, 256, "After 15 comes 0 again: 4 bits wrap around.", 11.5, GRN)
    return s


def shift_reg():
    s = Svg(660, 280, "Shift register", "Four flip-flops in a chain sharing one clock; din enters at the right and each bit moves one place left per clock; the sequence 1 0 1 1 is shown filling the register.")
    head(s, "A shift register: a conveyor belt of bits")
    xs = [110, 215, 320, 425]
    for i, x in enumerate(xs):
        f = dff(s, x, 70, 70, 64, VIO, "q[%d]" % (3 - i))
        if i < 3: s.arrow(x + 70, 88, xs[i + 1], 88, DIM)
    s.arrow(40, 88, 110, 88, BLUE) if False else None
    s.text(66, 92, "", 10, TX)
    s.arrow(530, 88, 560, 88, DIM) if False else None
    s.text(560, 92, "din", 12, BLUE, anchor="start"); s.arrow(556, 88, 495, 88, BLUE) if False else None
    s.add('<path d="M555 88 L540 88 L540 54 L100 54 L100 88 L110 88" fill="none" stroke="%s" stroke-width="1.6" stroke-dasharray="4 3"/>' % BLUE) if False else None
    s.line(495, 88, 540, 88, BLUE, 2); s.text(560, 92, "din (new bit)", 12, BLUE, anchor="start")
    s.text(280, 46, "bits move left", 11, DIM); s.arrow(440, 54, 120, 54, DIM)
    for i, x in enumerate(xs): s.line(x, 120, x - 10, 150, AMB, 1.2) if False else None
    s.line(110, 200, 495, 200, AMB, 2); s.text(300, 218, "clk drives all four at once", 11, AMB)
    for x in xs: s.line(x + 35, 200, x + 35, 148, AMB, 1.5)
    s.rect(40, 230, 580, 36, "#0a0712", LINE, 8, 1.5); s.text(330, 253, "q <= {q[2:0], din};    after din = 1, 0, 1, 1 :  q = 1011", 12, TX, style=MONO)
    return s


def resets():
    s = Svg(660, 330, "Asynchronous and synchronous reset", "With asynchronous reset q clears immediately when reset falls; with synchronous reset q clears only at the next clock edge.")
    head(s, "Two kinds of reset")
    n = 16; w = 460; x0 = 150; tw = w / n
    for k, (ttl, bits, col) in enumerate([("Asynchronous", "0000000011111111", GRN), ("Synchronous", "0000000000111111", BLUE)]):
        y = 50 + k * 140
        s.text(20, y + 14, ttl, 13, col, weight="700", anchor="start")
        wave(s, x0, y + 8, w, "0101010101010101", "clk", AMB, 18)
        wave(s, x0, y + 40, w, "0011111111111111" if k == 0 else "0011111111111111", "rst_n", PINK, 18) if False else None
        wave(s, x0, y + 40, w, "1111000011111111", "rst_n", PINK, 18)
        wave(s, x0, y + 72, w, "1111000000000000" if k == 0 else "1111100000000000", "q", col, 18)
        s.line(x0 + 4 * tw, y + 4, x0 + 4 * tw, y + 96, PINK, 1, dash="3 3")
    s.text(x0 + 5 * tw + 6, 160, "", 10, TX)
    s.text(500, 150, "q clears the moment rst_n falls", 11, GRN); s.text(500, 290, "q clears at the next rising edge", 11, BLUE)
    s.text(330, 318, "async:  always @(posedge clk or negedge rst_n)      sync:  always @(posedge clk)", 11, DIM, style=MONO)
    return s


def setup_hold():
    s = Svg(640, 300, "Setup and hold time", "Data must be stable for the setup time before and the hold time after the rising clock edge; a change inside this window can make the flip-flop go metastable.")
    head(s, "The forbidden window around the clock edge")
    x0 = 100; w = 480
    wave(s, x0, 60, w, "00000111111111", "clk", AMB, 24)
    wave(s, x0, 130, w, "01111111110000", "d", BLUE, 24)
    tw = w / 14; xe = x0 + 5 * tw
    s.add('<rect x="%.1f" y="54" width="%.1f" height="142" fill="%s" fill-opacity="0.18" stroke="%s" stroke-dasharray="4 3"/>' % (xe - 60, 100, RED, RED))
    s.line(xe, 54, xe, 200, AMB, 1.5, dash="3 3")
    s.text(xe - 30, 214, "setup", 12, RED); s.text(xe + 20, 214, "hold", 12, RED); s.text(xe, 50, "clock edge", 11, AMB)
    s.text(330, 244, "tsu: d must arrive this long BEFORE the edge.   th: d must stay this long AFTER it.", 11.5, TX)
    s.text(330, 268, "Break the window and q may be wrong or hover between 0 and 1 (metastability).", 11.5, DIM)
    return s


def delays():
    s = Svg(660, 330, "Inertial and transport delay", "An input pulse shorter than the gate delay vanishes with inertial delay but passes through with transport delay.")
    head(s, "Delay models: does a short pulse survive?")
    x0 = 120; w = 500; n = 20; tw = w / n
    wave(s, x0, 56, w, "00001100000000000000", "in", BLUE, 22)
    wave(s, x0, 112, w, "00000000000000000000", "inertial #4", GRN, 22)
    wave(s, x0, 168, w, "00000011000000000000", "transport #4", AMB, 22)
    s.text(x0 + 5 * tw, 50, "2-unit pulse", 11, BLUE); s.text(x0 + 11 * tw, 106, "pulse swallowed (too short)", 11, GRN); s.text(x0 + 14 * tw, 162, "pulse delayed", 11, AMB)
    s.text(330, 270, "assign #4 y = a;      is inertial: real gates filter glitches shorter than their delay.", 11.5, DIM, style=MONO)
    s.text(330, 292, "Transport delay (y <= #4 a;) models a wire: everything is just shifted.", 11.5, DIM)
    return s


def critpath():
    s = Svg(660, 280, "Clock period and critical path", "Between two flip-flops the clock period must cover the clock-to-q delay, the logic delay and the setup time.")
    head(s, "Why a chip has a maximum clock speed")
    dff(s, 40, 80, 80, 70, VIO, "launch flop"); dff(s, 520, 80, 80, 70, VIO, "capture flop")
    s.box(220, 84, 200, 62, "combinational logic", "tlogic (the slow path)", AMB)
    s.arrow(120, 98, 220, 98, DIM); s.arrow(420, 98, 520, 98, DIM)
    s.line(80, 178, 560, 178, AMB, 2); s.line(80, 150, 80, 178, AMB, 1.5); s.line(560, 150, 560, 178, AMB, 1.5)
    s.text(320, 198, "clock", 11, AMB)
    s.rect(60, 212, 520, 40, "#0a0712", LINE, 8, 1.5)
    s.text(320, 238, "Tclk  >=  tclk-to-q  +  tlogic  +  tsetup        fmax = 1 / Tclk", 13, TX, style=MONO)
    return s


def tb_arch():
    s = Svg(660, 320, "Testbench architecture", "A testbench contains a stimulus generator, the design under test, a reference model and a checker, and writes a waveform file.")
    head(s, "A testbench is a lab bench in code")
    s.rect(20, 46, 620, 230, "none", VIO, 14, 2, dash="6 4"); s.text(40, 66, "module tb;  (no ports: it is the whole world)", 12, VIO, weight="700", anchor="start")
    s.box(50, 100, 130, 64, "Stimulus", "clock, reset, inputs", BLUE); s.box(260, 100, 130, 64, "DUT", "design under test", GRN)
    s.box(260, 200, 130, 56, "Reference model", "the expected answer", AMB); s.box(470, 150, 130, 64, "Checker", "compare, count errors", PINK)
    s.arrow(180, 132, 260, 132, DIM); s.arrow(115, 164, 115, 228, DIM); s.line(115, 228, 260, 228, DIM, 1.8); s.arrow(255, 228, 260, 228, DIM)
    s.arrow(390, 132, 470, 170, DIM); s.arrow(390, 228, 470, 200, DIM)
    s.text(530, 240, "$display PASS / FAIL", 11.5, PINK); s.text(530, 94, "dump.vcd (waveform)", 11, DIM)
    s.arrow(390, 112, 500, 100, DIM, dash="4 3")
    s.text(330, 304, "Stimulus + checker + reference = a self-checking testbench: it tells you pass or fail on its own.", 11.5, DIM)
    return s


def clkgen():
    s = Svg(640, 270, "Clock generation", "initial clk = 0 and always #5 clk = ~clk gives a clock with period 10 time units, rising at 5, 15, 25.")
    head(s, "always #5 clk = ~clk;   (period = 10)")
    x0 = 90; w = 520; n = 12; tw = w / n
    wave(s, x0, 70, w, "000011110000111100001111"[:12] if False else "001100110011", "clk", AMB, 28) if False else None
    wave(s, x0, 70, w, "010101", "clk", AMB, 28)
    for i in range(0, 13, 2):
        pass
    for k, t in enumerate([0, 5, 10, 15, 20, 25, 30]):
        x = x0 + k * tw * 12 / 6 / 1
    for k in range(7):
        x = x0 + k * w / 6; s.line(x, 62, x, 112, LINE, 1, dash="3 3"); s.text(x, 128, "%d" % (k * 5), 11, DIM)
    s.text(330, 160, "time in ns (with `timescale 1ns/1ps)", 11, DIM)
    s.rect(60, 180, 520, 60, "#0a0712", LINE, 8, 1.5)
    s.text(320, 204, "reg clk = 0;  always #5 clk = ~clk;", 12.5, TX, style=MONO); s.text(320, 226, "half period 5 ns, period 10 ns, frequency 100 MHz", 11.5, GRN)
    return s


def fsm_struct():
    s = Svg(660, 300, "FSM structure", "A finite state machine has next-state logic, a state register and output logic; Moore outputs depend only on the state and Mealy outputs also on the inputs.")
    head(s, "Every state machine has the same three parts")
    s.box(160, 80, 150, 70, "Next-state logic", "combinational", BLUE); s.box(380, 80, 110, 70, "State", "register (clk)", VIO); s.box(380, 190, 150, 56, "Output logic", "combinational", GRN)
    s.arrow(30, 100, 160, 100, TX); s.text(26, 92, "inputs", 11, TX, anchor="start")
    s.arrow(310, 115, 380, 115, DIM); s.text(345, 108, "next", 10.5, DIM)
    s.arrow(490, 115, 560, 115, DIM) if False else None
    s.line(490, 115, 530, 115, DIM, 1.8); s.line(530, 115, 530, 60, DIM, 1.8); s.line(530, 60, 235, 60, DIM, 1.8); s.arrow(235, 60, 235, 80, DIM); s.text(380, 54, "current state fed back", 10.5, DIM)
    s.line(530, 115, 530, 218, DIM, 1.8); s.arrow(530, 218, 530, 218, DIM) if False else None
    s.arrow(530, 218, 531, 218, DIM) if False else None
    s.line(530, 218, 530, 218, DIM)
    s.arrow(380, 218, 380, 218, DIM) if False else None
    s.arrow(530, 218, 535, 218, DIM) if False else None
    s.arrow(150, 218, 380, 218, PINK, dash="5 4"); s.text(250, 238, "Mealy: inputs also reach the outputs", 11, PINK)
    s.arrow(530, 218, 610, 218, GRN); s.text(618, 222, "outputs", 11, GRN, anchor="start")
    s.line(40, 100, 40, 218, TX, 1.2, dash="3 3"); s.line(40, 218, 150, 218, PINK, 1.2, dash="5 4")
    s.text(330, 280, "Moore: output = f(state).    Mealy: output = f(state, input).    Write them as three pieces of Verilog.", 11.5, DIM)
    return s


def fsm101():
    s = Svg(660, 300, "Sequence detector state diagram", "Mealy state diagram with states S0, S1, S2 detecting the bit pattern 1 0 1, output 1 on the arc from S2 labelled input 1.")
    head(s, "Detect 1 0 1  (Mealy, overlapping)")
    pos = {"S0": (110, 150), "S1": (330, 150), "S2": (550, 150)}
    for nm, (x, y) in pos.items():
        circ(s, x, y, 36, PANEL, VIO, 2.5); s.text(x, y + 5, nm, 14, TX, weight="700")
    s.text(110, 206, "nothing yet", 10.5, DIM); s.text(330, 206, "saw 1", 10.5, DIM); s.text(550, 206, "saw 10", 10.5, DIM)
    s.arrow(146, 140, 294, 140, GRN, sw=2.2); s.text(220, 130, "x=1 / y=0", 11, GRN)
    s.arrow(366, 140, 514, 140, GRN, sw=2.2); s.text(440, 130, "x=0 / y=0", 11, GRN)
    path(s, "M520 172 Q440 230 360 176", PINK, 2.2, arrow=True); s.text(440, 234, "x=1 / y=1  (detected!)", 11, PINK)
    path(s, "M560 116 Q620 40 330 60 Q300 62 320 112", AMB, 2, arrow=True) if False else None
    path(s, "M575 118 Q420 20 285 118", DIM, 2, arrow=True); s.text(430, 64, "x=0 / y=0  back to S0", 11, DIM)
    path(s, "M80 128 Q60 80 110 90 Q140 94 130 116", GRN, 2, arrow=True); s.text(60, 70, "x=0 / y=0", 11, GRN)
    path(s, "M312 118 Q330 60 348 118", GRN, 2, arrow=True); s.text(330, 56, "x=1 / y=0", 11, GRN)
    s.text(330, 282, "Arc labels: input / output. The detected arc returns to S1 because the last 1 can start the next 101.", 11, DIM)
    return s


def traffic():
    s = Svg(560, 260, "Traffic light FSM", "Three states in a loop: red, green, yellow, each with one lit output.")
    head(s, "Moore machine: the state is the output")
    for i, (nm, c, x) in enumerate((("RED", RED, 90), ("GREEN", GRN, 280), ("YELLOW", AMB, 470))):
        circ(s, x, 120, 42, PANEL, c, 3); s.text(x, 125, nm, 13, c, weight="700"); s.text(x, 188, "red=%d green=%d yellow=%d" % (nm == "RED", nm == "GREEN", nm == "YELLOW"), 10.5, DIM)
    s.arrow(132, 120, 238, 120, DIM, sw=2); s.arrow(322, 120, 428, 120, DIM, sw=2)
    path(s, "M470 80 Q280 28 90 80", DIM, 2, arrow=True); s.text(280, 58, "every clock", 11, DIM)
    s.text(280, 238, "Outputs are decoded from the state alone: assign red = (state == RED);", 11.5, GRN)
    return s


def param():
    s = Svg(620, 280, "Parameterised module", "One module reg_n with a parameter N instantiated twice, as 12 bits wide and as 3 bits wide.")
    head(s, "Write once, use at any width")
    s.rect(20, 50, 190, 190, PANEL, VIO, 12, 2.5); s.text(115, 76, "module reg_n #(N = 8)", 12, VIO, weight="700"); s.text(115, 110, "input  [N-1:0] d", 11, BLUE, style=MONO); s.text(115, 132, "output [N-1:0] q", 11, GRN, style=MONO); s.text(115, 170, "N is a knob", 12, TX)
    s.arrow(210, 110, 290, 90, DIM); s.arrow(210, 170, 290, 190, DIM)
    for i, (n, y, c) in enumerate(((12, 60, GRN), (3, 160, AMB))):
        s.rect(290, y, 310, 70, PANEL, c, 10, 2); s.text(300, y + 22, "reg_n #(.N(%d)) u%d(...);" % (n, n), 12, TX, anchor="start", style=MONO)
        for b in range(n):
            s.rect(300 + b * (290 / max(n, 3) if n == 3 else 24), y + 36, (60 if n == 3 else 21), 20, c, c, 3, 1) if False else None
        wbit = 290 / 12
        for b in range(n):
            s.rect(300 + b * (wbit if n == 12 else 90), y + 38, (wbit - 3 if n == 12 else 84), 20, "none", c, 3, 1.5)
        s.text(595, y + 22, "%d bits" % n, 10.5, c, anchor="end")
    s.text(310, 268, "Override with #(.N(12)); the default applies when you say nothing.", 11.5, DIM)
    return s


def memory():
    s = Svg(620, 330, "Memory array", "A 16 by 8 memory: an address decoder selects one of sixteen 8-bit words; writes happen on the clock when write enable is 1.")
    head(s, "reg [7:0] mem [0:15]  a 16-word memory")
    for i in range(16):
        y = 54 + i * 15; col = AMB if i == 5 else LINE
        s.rect(200, y, 180, 13, "#3a2a10" if i == 5 else PANEL, col, 2, 1.2); s.text(194, y + 10, str(i), 9.5, DIM, anchor="end")
        s.text(290, y + 10, "8 bits" if i != 5 else "word 5 selected", 9.5, TX if i == 5 else DIM)
    s.arrow(60, 160, 180, 130, BLUE); s.text(60, 150, "addr[3:0]", 11, BLUE, anchor="middle"); s.text(60, 176, "= 5", 11, BLUE)
    s.arrow(60, 230, 200, 230, PINK); s.text(60, 224, "din[7:0]", 11, PINK); s.arrow(60, 270, 200, 255, AMB); s.text(60, 264, "we, clk", 11, AMB)
    s.arrow(380, 125, 470, 125, GRN); s.text(480, 129, "dout[7:0]", 11, GRN, anchor="start")
    s.rect(60, 296, 500, 26, "#0a0712", LINE, 6, 1.2); s.text(310, 313, "always @(posedge clk) if (we) mem[addr] <= din;   assign dout = mem[addr];", 11, TX, style=MONO)
    return s


def synth():
    s = Svg(680, 340, "From RTL to silicon", "RTL is synthesised to a gate netlist, which goes either to an FPGA bitstream or to an ASIC layout, with timing checks at each stage.")
    head(s, "Where your Verilog goes next")
    s.box(20, 140, 120, 64, "RTL", "your Verilog", GRN); s.box(180, 140, 130, 64, "Synthesis", "to gates + flops", AMB)
    s.arrow(140, 172, 180, 172, DIM); s.box(350, 140, 130, 64, "Netlist", "AND OR NOT DFF", BLUE); s.arrow(310, 172, 350, 172, DIM)
    s.arrow(480, 160, 530, 90, DIM); s.arrow(480, 184, 530, 256, DIM)
    s.box(530, 50, 130, 70, "FPGA", "LUTs + bitstream", PINK); s.box(530, 216, 130, 80, "ASIC", "layout (GDSII)", VIO)
    s.text(100, 120, "simulate first", 11, GRN); s.text(245, 120, "constraints: clock, pins", 10.5, AMB)
    s.text(340, 326, "Both paths check timing (static timing analysis): does the slowest path fit in one clock period?", 11.5, DIM)
    return s


def cpu_block():
    s = Svg(680, 330, "Tiny CPU block diagram", "Program counter, instruction ROM, control decoder, ALU and accumulator connected into a single-cycle 8-bit processor.")
    head(s, "The capstone: an 8-bit accumulator CPU")
    s.box(20, 120, 100, 60, "pc", "4-bit counter", BLUE); s.box(160, 110, 100, 80, "rom", "16 x 8 program", AMB); s.box(300, 50, 110, 60, "control", "decode opcode", PINK)
    s.box(300, 200, 110, 60, "alu", "add sub and or", GRN); s.box(460, 200, 100, 60, "acc", "8-bit register", VIO); s.box(580, 120, 80, 60, "out", "register", VIO)
    s.arrow(120, 150, 160, 150, DIM); s.text(140, 140, "addr", 10, DIM)
    s.arrow(260, 140, 300, 90, DIM); s.text(280, 100, "op", 10, DIM)
    s.arrow(260, 165, 300, 225, DIM); s.text(268, 205, "imm", 10, DIM)
    s.arrow(410, 230, 460, 230, DIM); s.line(510, 260, 510, 290, DIM, 1.8); s.line(510, 290, 355, 290, DIM, 1.8); s.arrow(355, 290, 355, 260, DIM); s.text(430, 284, "acc feeds back to the ALU", 10, DIM)
    s.arrow(560, 215, 620, 180, DIM); s.text(600, 212, "OUT", 10, DIM)
    s.arrow(355, 110, 355, 200, PINK, dash="4 3"); s.text(372, 156, "alu_op, ld, use_alu", 10, PINK, anchor="start")
    s.line(355, 50, 355, 36, PINK, 1.5); s.line(355, 36, 70, 36, PINK, 1.5) if False else None
    s.line(300, 80, 70, 80, PINK, 1.4, dash="4 3"); s.arrow(70, 80, 70, 120, PINK); s.text(180, 74, "jump / halt to the pc", 10, PINK)
    s.text(340, 318, "One instruction per clock: fetch from the rom, decode, execute, write back.", 11.5, DIM)
    return s


def isa():
    s = Svg(620, 300, "Instruction format and opcodes", "An 8-bit instruction: opcode in the upper four bits and operand in the lower four, with the seven opcodes of the tiny CPU.")
    head(s, "One instruction = 8 bits")
    for i in range(8):
        c = AMB if i < 4 else BLUE; s.rect(80 + i * 56, 50, 50, 40, PANEL, c, 6, 2); s.text(105 + i * 56, 76, "b%d" % (7 - i), 12, TX)
    s.line(80, 104, 80 + 4 * 56 - 6, 104, AMB, 3); s.text(80 + 112, 124, "opcode [7:4]", 12, AMB); s.line(80 + 4 * 56, 104, 80 + 8 * 56 - 6, 104, BLUE, 3); s.text(80 + 336, 124, "operand [3:0]", 12, BLUE)
    rows = [("0", "LDI n", "acc = n"), ("1", "ADD n", "acc = acc + n"), ("2", "SUB n", "acc = acc - n"), ("3", "AND n", "acc = acc & n"), ("4", "JNZ a", "if acc != 0 pc = a"), ("5", "OUT", "out = acc"), ("6", "HALT", "stop")]
    for i, (op, nm, d) in enumerate(rows):
        y = 144 + i * 22
        s.text(120, y, op, 12, AMB, weight="700"); s.text(200, y, nm, 12, TX, weight="700", anchor="start") if False else None
        s.text(170, y, nm, 12, TX, weight="700", anchor="start"); s.text(290, y, d, 12, DIM, anchor="start", style=MONO)
    return s


ALL_B = {"vl-alwaysmap.svg": always_map, "vl-blocking.svg": blocking, "vl-scheduler.svg": scheduler, "vl-counterwave.svg": counter_wave, "vl-shift.svg": shift_reg, "vl-resets.svg": resets,
         "vl-setuphold.svg": setup_hold, "vl-delays.svg": delays, "vl-critpath.svg": critpath, "vl-tbarch.svg": tb_arch, "vl-clkgen.svg": clkgen, "vl-fsmstruct.svg": fsm_struct, "vl-fsm101.svg": fsm101,
         "vl-traffic.svg": traffic, "vl-param.svg": param, "vl-memory.svg": memory, "vl-synth.svg": synth, "vl-cpu.svg": cpu_block, "vl-isa.svg": isa}
