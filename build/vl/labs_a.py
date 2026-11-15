# -*- coding: utf-8 -*-
"""Verilog labs for chapters 4-6: latches and flip-flops (watch), first modules, operators."""
from lib import *

# ---------------- Lab: watch latches and flip-flops (chapter 4); the student edits the testbench ----------------
SR = """module sr_latch(input s, input r, output q, output qn);
  nor (q, r, qn);
  nor (qn, s, q);
endmodule
"""
SR_TB = """`timescale 1ns/1ps
module tb;
  reg s, r; wire q, qn;
  sr_latch dut(.s(s), .r(r), .q(q), .qn(qn));
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    $monitor("t=%0t s=%b r=%b q=%b", $time, s, r, q);
    s = 0; r = 0;
    #10 s = 1;          // SET
    #10 $finish;
    // TODO: release s (set it back to 0) to see the latch HOLD, then pulse r to RESET
  end
endmodule
"""
SR_SOL = SR_TB.replace("    #10 $finish;\n", "    #10 s = 0;          // HOLD\n    #10 r = 1;          // RESET\n    #10 r = 0;\n    #10 $finish;\n")
DL = """module d_latch(input d, input en, output reg q);
  always @* if (en) q = d;      // transparent while en = 1, remembers while en = 0
endmodule
"""
DL_TB = """`timescale 1ns/1ps
module tb;
  reg d, en; wire q;
  d_latch dut(.d(d), .en(en), .q(q));
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    $monitor("t=%0t en=%b d=%b q=%b", $time, en, d, q);
    en = 1; d = 0;
    #10 d = 1;          // transparent: q follows d
    #10 $finish;
    // TODO: close the latch (en = 0) and change d: q must keep its old value
  end
endmodule
"""
DL_SOL = DL_TB.replace("    #10 $finish;\n", "    #10 en = 0;\n    #10 d = 0;          // q should still be 1\n    #10 en = 1;         // open again: q follows d\n    #10 $finish;\n")
FF = """module dff(input clk, input d, output reg q);
  initial q = 0;
  always @(posedge clk) q <= d;     // copies d only on the rising edge
endmodule
"""
FF_TB = """`timescale 1ns/1ps
module tb;
  reg clk = 0, d = 0; wire q;
  dff dut(.clk(clk), .d(d), .q(q));
  always #5 clk = ~clk;                // rising edges at 5, 15, 25, 35
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    $monitor("t=%0t clk=%b d=%b q=%b", $time, clk, d, q);
    // TODO: raise d while clk is low (t=12), then drop it while clk is high (t=27)
    #40 $finish;
  end
endmodule
"""
FF_SOL = FF_TB.replace("    // TODO: raise d while clk is low (t=12), then drop it while clk is high (t=27)\n", "    #12 d = 1;\n    #15 d = 0;\n").replace("#40 $finish", "#13 $finish")
TFF = """module tff(input clk, output reg q);
  initial q = 0;
  always @(posedge clk) q <= ~q;    // toggles on every rising edge
endmodule
"""
TFF_TB = """`timescale 1ns/1ps
module tb;
  reg clk = 0; wire q;
  tff dut(.clk(clk), .q(q));
  always #5 clk = ~clk;
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    $monitor("t=%0t clk=%b q=%b", $time, clk, q);
    #8 $finish;          // TODO: run long enough to see q go 0 -> 1 -> 0
  end
endmodule
"""
TFF_SOL = TFF_TB.replace("#8 $finish;          // TODO: run long enough to see q go 0 -> 1 -> 0", "#32 $finish;")

LAB_WATCH = ("Lab 3: Watch latches and flip-flops", "The circuit is given. You write the stimulus in the testbench, run it, and read the waveform to see what memory looks like.", 1500, [
    LV("SR latch: set, hold, reset", "Two cross-coupled NOR gates remember one bit. Right now the testbench only sets the latch. Edit tb.v so s goes back to 0 (the latch must HOLD q = 1) and then r pulses to 1 (RESET, q = 0).",
       "After #10 s = 1 add: #10 s = 0; then #10 r = 1; then #10 r = 0; and keep $finish last.", SR, SR_SOL, SR_TB, edit="tb",
       goals=[{"t": "Set: q becomes 1 when s = 1", "re": r"s=1 r=0 q=1"}, {"t": "Hold: q stays 1 after s is released", "re": r"s=0 r=0 q=1"}, {"t": "Reset: q becomes 0 when r = 1", "re": r"s=0 r=1 q=0"}]),
    LV("D latch: transparent or closed", "A D latch passes d to q while en = 1 and freezes q while en = 0. Close the latch, then change d, and check that q does not follow.",
       "After the transparent part add: #10 en = 0; then #10 d = 0; (q must still print 1).", DL, DL_SOL, DL_TB, edit="tb",
       goals=[{"t": "Transparent: en=1, d=1 gives q=1", "re": r"en=1 d=1 q=1"}, {"t": "Closed: en=0 and d=0 but q is still 1", "re": r"en=0 d=0 q=1"}, {"t": "Open again: en=1, d=0 gives q=0", "re": r"en=1 d=0 q=0"}]),
    LV("D flip-flop: only the edge counts", "A flip-flop copies d only at the rising edge of clk. Raise d while the clock is low, and see that q ignores it until the next edge. Then drop d while the clock is high and see that q ignores that too.",
       "Replace the TODO with: #12 d = 1; #15 d = 0; and shorten the run to #13 $finish after that.", FF, FF_SOL, FF_TB, edit="tb",
       goals=[{"t": "d is 1 while the clock is low, q is still 0", "re": r"clk=0 d=1 q=0"}, {"t": "At the rising edge q takes the value 1", "re": r"clk=1 d=1 q=1"}, {"t": "d falls while the clock is high, q keeps 1", "re": r"clk=1 d=0 q=1"}]),
    LV("Toggle flip-flop: divide by two", "Feeding q back inverted makes a flip-flop toggle on every rising edge, so q switches at half the clock rate. Let the simulation run long enough to see q rise and fall.",
       "Change the run time to #32 $finish: you need at least two rising edges after the first.", TFF, TFF_SOL, TFF_TB, edit="tb",
       goals=[{"t": "q goes to 1 on the first rising edge", "re": r"clk=1 q=1"}, {"t": "q returns to 0 on the second rising edge", "re": r"q=1[\s\S]*clk=1 q=0"}]),
])

# ---------------- Lab: first modules (chapter 5) ----------------
def gate_tb(top, ins, outs, fn):
    return combtb(top, [(n, 1) for n in ins], [(n, 1) for n in outs], rows_from(fn, ins, exhaustive([1] * len(ins))))

LAB_FIRST = ("Lab 4: Your first Verilog modules", "Write small circuits with the built-in gates and wire them together. Each level has a hidden-test testbench that checks every input combination.", 1500, [
    LV("The and gate", "Use the built-in primitive. A gate primitive lists the output first: and (y, a, b);", "Inside the module write: and (y, a, b);",
       "module and2(input a, input b, output y);\n  // TODO: one built-in and gate\nendmodule\n", "module and2(input a, input b, output y);\n  and (y, a, b);\nendmodule\n",
       gate_tb("and2", ["a", "b"], ["y"], lambda a, b: [a & b])),
    LV("XOR built from four NANDs", "NAND is a universal gate: any logic can be made from it. Wire four nand gates with three internal wires so that y = a XOR b. The first gate gets n1 = a NAND b.",
       "n1 = nand(a,b); n2 = nand(a,n1); n3 = nand(b,n1); y = nand(n2,n3).",
       "module xor_nand(input a, input b, output y);\n  wire n1, n2, n3;\n  // TODO: four nand gates\nendmodule\n",
       "module xor_nand(input a, input b, output y);\n  wire n1, n2, n3;\n  nand (n1, a, b);\n  nand (n2, a, n1);\n  nand (n3, b, n1);\n  nand (y, n2, n3);\nendmodule\n",
       gate_tb("xor_nand", ["a", "b"], ["y"], lambda a, b: [a ^ b])),
    LV("Half adder", "Add two bits: sum is a XOR b, carry is a AND b.", "xor (sum, a, b); and (carry, a, b);",
       "module half_adder(input a, input b, output sum, output carry);\n  // TODO\nendmodule\n",
       "module half_adder(input a, input b, output sum, output carry);\n  xor (sum, a, b);\n  and (carry, a, b);\nendmodule\n",
       gate_tb("half_adder", ["a", "b"], ["sum", "carry"], lambda a, b: [a ^ b, a & b])),
    LV("Full adder from two half adders", "Hierarchy: a module can contain other modules. The half adder is given. Build the full adder from two of them and one or gate. Instance syntax: half_adder h1(.a(x), .b(y), .sum(s), .carry(c));",
       "h1 adds a and b. h2 adds h1's sum and cin. cout = c1 OR c2.",
       "module half_adder(input a, input b, output sum, output carry);\n  xor (sum, a, b);\n  and (carry, a, b);\nendmodule\n\nmodule full_adder(input a, input b, input cin, output sum, output cout);\n  wire s1, c1, c2;\n  // TODO: two half adders and an or gate\nendmodule\n",
       "module half_adder(input a, input b, output sum, output carry);\n  xor (sum, a, b);\n  and (carry, a, b);\nendmodule\n\nmodule full_adder(input a, input b, input cin, output sum, output cout);\n  wire s1, c1, c2;\n  half_adder h1(.a(a), .b(b), .sum(s1), .carry(c1));\n  half_adder h2(.a(s1), .b(cin), .sum(sum), .carry(c2));\n  or (cout, c1, c2);\nendmodule\n",
       gate_tb("full_adder", ["a", "b", "cin"], ["sum", "cout"], lambda a, b, c: [(a + b + c) & 1, (a + b + c) >> 1])),
    LV("A 2-to-1 multiplexer from gates", "y = a when s = 0, y = b when s = 1. Build it from not, and, or gates: y = (a AND NOT s) OR (b AND s).", "not (ns, s); and (t1, a, ns); and (t2, b, s); or (y, t1, t2);",
       "module mux2(input a, input b, input s, output y);\n  wire ns, t1, t2;\n  // TODO\nendmodule\n",
       "module mux2(input a, input b, input s, output y);\n  wire ns, t1, t2;\n  not (ns, s);\n  and (t1, a, ns);\n  and (t2, b, s);\n  or (y, t1, t2);\nendmodule\n",
       gate_tb("mux2", ["a", "b", "s"], ["y"], lambda a, b, s: [b if s else a])),
])

# ---------------- Lab: operators and assign (chapter 6) ----------------
def vec_tb(top, ins, outs, fn, n=24):
    ws = [w for _, w in ins]
    return combtb(top, ins, outs, rows_from(fn, ins, sample(ws, n) if sum(ws) > 6 else exhaustive(ws)))

LAB_OPS = ("Lab 5: Operators and continuous assignment", "Describe circuits with assign and operators instead of gates: bits, vectors, reduction, comparison and arithmetic.", 1500, [
    LV("Majority with assign", "y is 1 when at least two of the three inputs are 1. One line: y = (a & b) | (b & c) | (a & c).", "assign y = (a & b) | (b & c) | (a & c);",
       "module majority(input a, input b, input c, output y);\n  // TODO: assign y = ...\nendmodule\n", "module majority(input a, input b, input c, output y);\n  assign y = (a & b) | (b & c) | (a & c);\nendmodule\n",
       gate_tb("majority", ["a", "b", "c"], ["y"], lambda a, b, c: [1 if a + b + c >= 2 else 0])),
    LV("Swap the nibbles", "x is 8 bits. y has the same bits with the upper and lower 4-bit halves swapped. Use part-selects x[7:4] and x[3:0] and concatenation { , }.", "assign y = {x[3:0], x[7:4]};",
       "module swapnib(input [7:0] x, output [7:0] y);\n  // TODO\nendmodule\n", "module swapnib(input [7:0] x, output [7:0] y);\n  assign y = {x[3:0], x[7:4]};\nendmodule\n",
       vec_tb("swapnib", [("x", 8)], [("y", 8)], lambda x: [((x & 15) << 4) | (x >> 4)])),
    LV("Reduction operators", "A reduction operator squeezes a vector into one bit. parity must be 1 when x has an odd number of ones (^x). all_ones is 1 only when every bit is 1 (&x). any_one is 1 when some bit is 1 (|x).", "assign parity = ^x; assign all_ones = &x; assign any_one = |x;",
       "module reduce4(input [3:0] x, output parity, output all_ones, output any_one);\n  // TODO\nendmodule\n",
       "module reduce4(input [3:0] x, output parity, output all_ones, output any_one);\n  assign parity = ^x;\n  assign all_ones = &x;\n  assign any_one = |x;\nendmodule\n",
       vec_tb("reduce4", [("x", 4)], [("parity", 1), ("all_ones", 1), ("any_one", 1)], lambda x: [bin(x).count("1") & 1, 1 if x == 15 else 0, 1 if x else 0])),
    LV("Max of two numbers", "The conditional operator is a multiplexer: cond ? when_true : when_false. Output the larger of two 4-bit numbers.", "assign y = (a > b) ? a : b;",
       "module max4(input [3:0] a, input [3:0] b, output [3:0] y);\n  // TODO\nendmodule\n", "module max4(input [3:0] a, input [3:0] b, output [3:0] y);\n  assign y = (a > b) ? a : b;\nendmodule\n",
       vec_tb("max4", [("a", 4), ("b", 4)], [("y", 4)], lambda a, b: [max(a, b)], n=30)),
    LV("Adder with carry out", "Add two 4-bit numbers and keep the fifth bit. Put a 5-bit result on the left side: {cout, sum} = a + b. Then make sub = a - b with a borrow flag lt = (a < b).", "assign {cout, sum} = a + b; assign sub = a - b; assign lt = a < b;",
       "module arith4(input [3:0] a, input [3:0] b, output [3:0] sum, output cout, output [3:0] sub, output lt);\n  // TODO\nendmodule\n",
       "module arith4(input [3:0] a, input [3:0] b, output [3:0] sum, output cout, output [3:0] sub, output lt);\n  assign {cout, sum} = a + b;\n  assign sub = a - b;\n  assign lt = a < b;\nendmodule\n",
       vec_tb("arith4", [("a", 4), ("b", 4)], [("sum", 4), ("cout", 1), ("sub", 4), ("lt", 1)], lambda a, b: [(a + b) & 15, (a + b) >> 4, (a - b) & 15, 1 if a < b else 0], n=40)),
])
LABS_A = [LAB_WATCH, LAB_FIRST, LAB_OPS]
