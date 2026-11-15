# -*- coding: utf-8 -*-
"""Verilog labs for chapters 11-14: testbenches and timing, state machines, parameters and memories, the capstone CPU."""
from lib import *
from labs_a import gate_tb, vec_tb

# ---------------- chapter 11: testbenches and timing (student writes the testbench) ----------------
CNT = "module counter4(input clk, output reg [3:0] q);\n  initial q = 0;\n  always @(posedge clk) q <= q + 1;\nendmodule\n"
CNT_TB = """`timescale 1ns/1ps
module tb;
  reg clk = 0; wire [3:0] q;
  counter4 dut(.clk(clk), .q(q));
  // TODO: a clock generator with a 10 ns period (toggle every 5 ns)
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    #100 $display("count=%0d", q);
    $finish;
  end
endmodule
"""
FAD = "module full_adder(input a, input b, input cin, output sum, output cout);\n  assign sum = a ^ b ^ cin;\n  assign cout = (a & b) | (cin & (a ^ b));\nendmodule\n"
FAD_TB = """`timescale 1ns/1ps
module tb;
  reg a, b, cin; wire sum, cout;
  full_adder dut(.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));
  integer i, errs, cases;
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    errs = 0; cases = 0;
    // TODO: loop i from 0 to 7: put i on {a, b, cin}, wait 5 ns, compare {cout, sum} with a + b + cin,
    //       count a mismatch in errs, and count every case in cases
    $display("checked %0d cases, %0d errors", cases, errs);
    if (errs == 0 && cases == 8) $display("ALL PASS");
    $finish;
  end
endmodule
"""
FAD_SOL = FAD_TB.replace("""    // TODO: loop i from 0 to 7: put i on {a, b, cin}, wait 5 ns, compare {cout, sum} with a + b + cin,
    //       count a mismatch in errs, and count every case in cases
""", """    for (i = 0; i < 8; i = i + 1) begin
      {a, b, cin} = i[2:0];
      #5;
      if ({cout, sum} !== a + b + cin) errs = errs + 1;
      cases = cases + 1;
    end
""")
CMP = "module cmp4(input [3:0] a, input [3:0] b, output gt);\n  assign gt = (a >= b);   // is this right?\nendmodule\n"
CMP_TB = """`timescale 1ns/1ps
module tb;
  reg [3:0] a, b; wire gt; integer errs;
  cmp4 dut(.a(a), .b(b), .gt(gt));
  task check;
    begin
      #5;
      if (gt !== (a > b)) begin
        $display("MISMATCH a=%0d b=%0d gt=%b", a, b, gt);
        errs = errs + 1;
      end
    end
  endtask
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    errs = 0;
    a = 1; b = 2; check;
    a = 3; b = 1; check;
    // TODO: add test vectors that expose the bug (think about the boundary)
    if (errs == 0) $display("testbench found no bug"); else $display("BUG FOUND");
    $finish;
  end
endmodule
"""
CMP_SOL = CMP_TB.replace("    // TODO: add test vectors that expose the bug (think about the boundary)\n", "    a = 7; b = 7; check;\n")
ADD = "module add4(input [3:0] a, input [3:0] b, output [3:0] s, output co);\n  assign {co, s} = a + b;\nendmodule\n"
ADD_TB = """`timescale 1ns/1ps
module tb;
  reg [3:0] a, b; wire [3:0] s; wire co;
  add4 dut(.a(a), .b(b), .s(s), .co(co));
  integer i, n, errs;
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    n = 0; errs = 0;
    // TODO: 50 times: a = $random; b = $random; wait 5 ns; if {co, s} !== a + b count an error; count n
    $display("%0d random tests, %0d errors", n, errs);
    $finish;
  end
endmodule
"""
ADD_SOL = ADD_TB.replace("    // TODO: 50 times: a = $random; b = $random; wait 5 ns; if {co, s} !== a + b count an error; count n\n", """    for (i = 0; i < 50; i = i + 1) begin
      a = $random; b = $random;
      #5;
      if ({co, s} !== a + b) errs = errs + 1;
      n = n + 1;
    end
""")
INVD = "`timescale 1ns/1ps\nmodule inv_d(input a, output y);\n  assign y = ~a;      // TODO: give the inverter a 2 ns propagation delay\nendmodule\n"
INVD_TB = """`timescale 1ns/1ps
module tb;
  reg a = 0; wire y;
  inv_d dut(.a(a), .y(y));
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    $monitor("t=%0d a=%b y=%b", $time, a, y);
    #10 a = 1;
    #10 a = 0;
    #10 $finish;
  end
endmodule
"""
LAB_TB = ("Lab 9: Testbenches and timing", "Write the stimulus yourself: a clock generator, an exhaustive loop, a bug-hunting test and random tests. Then add a gate delay and watch the waveform shift.", 1500, [
    LV("Generate a clock", "Every sequential test needs a clock. Add one line that toggles clk every 5 ns (period 10 ns). Then the counter sees 10 rising edges in 100 ns.", "always #5 clk = ~clk;",
       CNT, CNT_TB.replace("  // TODO: a clock generator with a 10 ns period (toggle every 5 ns)\n", "  always #5 clk = ~clk;\n"), CNT_TB, edit="tb", goals=[{"t": "After 100 ns the counter shows 10", "re": r"count=10\b"}]),
    LV("Test every input with a loop", "A full adder has 3 inputs, so only 8 cases: test them all. Write the for loop described in the TODO.", "for (i = 0; i < 8; i = i + 1) begin {a, b, cin} = i[2:0]; #5; ... end",
       FAD, FAD_SOL, FAD_TB, edit="tb", goals=[{"t": "All 8 cases were checked", "re": r"checked 8 cases, 0 errors"}, {"t": "The testbench reports ALL PASS", "re": "ALL PASS"}]),
    LV("A testbench must be able to fail", "This comparator has a bug, but the testbench says nothing is wrong, because it never tries the case that breaks it. Add test vectors until the testbench prints MISMATCH. A test that cannot fail proves nothing.", "The bug is at the boundary: what does a >= b give when a equals b? Add a = 7; b = 7; check;",
       CMP, CMP_SOL, CMP_TB, edit="tb", goals=[{"t": "The testbench catches a wrong output (MISMATCH)", "re": "MISMATCH"}, {"t": "It reports BUG FOUND", "re": "BUG FOUND"}]),
    LV("Random tests against a reference", "For wide inputs you cannot try everything, so try many random values and compare with the Verilog operator as the reference. $random gives a random 32-bit number; assigning it to a 4-bit reg keeps the low bits.", "for (i = 0; i < 50; i = i + 1) begin a = $random; b = $random; #5; ...",
       ADD, ADD_SOL, ADD_TB, edit="tb", goals=[{"t": "50 random tests ran with no errors", "re": r"50 random tests, 0 errors"}]),
    LV("Add a propagation delay", "Real gates are not instant. Give the inverter a 2 ns delay with assign #2 y = ~a; and compare the printed times: y now changes 2 ns after a. (The timescale line must stay at the top.)", "assign #2 y = ~a;",
       INVD, "`timescale 1ns/1ps\nmodule inv_d(input a, output y);\n  assign #2 y = ~a;\nendmodule\n", INVD_TB, goals=[{"t": "y falls 2 ns after a rises (t=12)", "re": r"t=12 a=1 y=0"}, {"t": "y rises 2 ns after a falls (t=22)", "re": r"t=22 a=0 y=1"}], extra=[]),
])

# ---------------- chapter 12: finite state machines ----------------
LAB_FSM = ("Lab 10: Finite state machines", "Draw the diagram in your head, then write the three parts of every state machine: the state register, the next-state logic and the outputs.", 1500, [
    LV("A toggle button (2 states)", "The led starts off. Each clock in which btn is 1 flips the state; otherwise it stays. Write the next-state logic. The state register and output are given.", "case (state) OFF: next = btn ? ON : OFF; ON: next = btn ? OFF : ON; default: next = OFF; endcase",
       "module toggler(input clk, input rst, input btn, output led);\n  localparam OFF = 1'b0, ON = 1'b1;\n  reg state, next;\n  always @(posedge clk) if (rst) state <= OFF; else state <= next;\n  always @* begin\n    next = state;\n    // TODO: next-state logic\n  end\n  assign led = (state == ON);\nendmodule\n",
       "module toggler(input clk, input rst, input btn, output led);\n  localparam OFF = 1'b0, ON = 1'b1;\n  reg state, next;\n  always @(posedge clk) if (rst) state <= OFF; else state <= next;\n  always @* begin\n    case (state)\n      OFF: next = btn ? ON : OFF;\n      ON:  next = btn ? OFF : ON;\n      default: next = OFF;\n    endcase\n  end\n  assign led = (state == ON);\nendmodule\n",
       seqtb("toggler", [("rst", 1), ("btn", 1)], [("led", 1)], [("in", {"rst": 1}), ("tick",), ("in", {"rst": 0}), ("exp", {"led": 0}, "starts off"), ("in", {"btn": 1}), ("tick",), ("exp", {"led": 1}, "on"), ("in", {"btn": 0}), ("tick",), ("exp", {"led": 1}, "stays on"), ("in", {"btn": 1}), ("tick",), ("exp", {"led": 0}, "off again")])),
    LV("A traffic light (Moore machine)", "Three states cycle on every clock: RED, GREEN, YELLOW, RED, ... In a Moore machine the outputs depend only on the state. Write the next-state case and one-hot outputs.", "RED -> GREEN -> YELLOW -> RED. assign red = (state == RED); and so on.",
       "module traffic(input clk, input rst, output red, output green, output yellow);\n  localparam RED = 2'd0, GREEN = 2'd1, YELLOW = 2'd2;\n  reg [1:0] state, next;\n  always @(posedge clk) if (rst) state <= RED; else state <= next;\n  always @* begin\n    // TODO: next-state logic\n    next = RED;\n  end\n  // TODO: outputs\n  assign red = 0;\n  assign green = 0;\n  assign yellow = 0;\nendmodule\n",
       "module traffic(input clk, input rst, output red, output green, output yellow);\n  localparam RED = 2'd0, GREEN = 2'd1, YELLOW = 2'd2;\n  reg [1:0] state, next;\n  always @(posedge clk) if (rst) state <= RED; else state <= next;\n  always @* begin\n    case (state)\n      RED: next = GREEN;\n      GREEN: next = YELLOW;\n      default: next = RED;\n    endcase\n  end\n  assign red = (state == RED);\n  assign green = (state == GREEN);\n  assign yellow = (state == YELLOW);\nendmodule\n",
       seqtb("traffic", [("rst", 1)], [("red", 1), ("green", 1), ("yellow", 1)], [("in", {"rst": 1}), ("tick",), ("in", {"rst": 0}), ("exp", {"red": 1, "green": 0, "yellow": 0}, "red"), ("tick",), ("exp", {"red": 0, "green": 1, "yellow": 0}, "green"), ("tick",), ("exp", {"red": 0, "green": 0, "yellow": 1}, "yellow"), ("tick",), ("exp", {"red": 1, "green": 0, "yellow": 0}, "red again")])),
    LV("Detect the sequence 101 (Mealy machine)", "x arrives one bit per clock. y must be 1 in the cycle when the last three bits were 1, 0 and now 1. Overlapping is allowed: 10101 gives two detections. S0 = nothing useful yet, S1 = saw 1, S2 = saw 10. In a Mealy machine y can use the input as well as the state.", "S1: next = x ? S1 : S2; S2: next = x ? S1 : S0; y = (state == S2) && x;",
       "module seq101(input clk, input rst, input x, output y);\n  localparam S0 = 2'd0, S1 = 2'd1, S2 = 2'd2;\n  reg [1:0] state, next;\n  always @(posedge clk) if (rst) state <= S0; else state <= next;\n  always @* begin\n    case (state)\n      S0: next = x ? S1 : S0;\n      // TODO: S1 and S2\n      default: next = S0;\n    endcase\n  end\n  assign y = 1'b0;   // TODO\nendmodule\n",
       "module seq101(input clk, input rst, input x, output y);\n  localparam S0 = 2'd0, S1 = 2'd1, S2 = 2'd2;\n  reg [1:0] state, next;\n  always @(posedge clk) if (rst) state <= S0; else state <= next;\n  always @* begin\n    case (state)\n      S0: next = x ? S1 : S0;\n      S1: next = x ? S1 : S2;\n      S2: next = x ? S1 : S0;\n      default: next = S0;\n    endcase\n  end\n  assign y = (state == S2) && x;\nendmodule\n",
       seqtb("seq101", [("rst", 1), ("x", 1)], [("y", 1)], [("in", {"rst": 1}), ("tick",), ("in", {"rst": 0, "x": 1}), ("tick",), ("in", {"x": 0}), ("tick",), ("in", {"x": 1}), ("exp", {"y": 1}, "101"), ("tick",), ("in", {"x": 0}), ("exp", {"y": 0}, "after"), ("tick",),
            ("in", {"x": 1}), ("exp", {"y": 1}, "overlap 10101"), ("tick",), ("in", {"x": 1}), ("exp", {"y": 0}, "11"), ("tick",), ("in", {"x": 0}), ("tick",), ("in", {"x": 0}), ("exp", {"y": 0}, "100"), ("tick",)])),
    LV("A vending machine", "A drink costs 15. The machine takes coins of 5 (n) or 10 (d), one per clock. It remembers the credit: S0 = 0, S5 = 5, S10 = 10. dispense is 1 in the cycle when the coin brings the credit to 15 or more, and then the machine returns to S0. (Mealy output.)", "dispense = (state == S5 && d) || (state == S10 && (n || d)); S0: n -> S5, d -> S10. S5: n -> S10, d -> S0. S10: n or d -> S0.",
       "module vend(input clk, input rst, input n, input d, output dispense);\n  localparam S0 = 2'd0, S5 = 2'd1, S10 = 2'd2;\n  reg [1:0] state, next;\n  always @(posedge clk) if (rst) state <= S0; else state <= next;\n  always @* begin\n    next = state;\n    // TODO: next-state logic for S0, S5 and S10\n  end\n  assign dispense = 1'b0;   // TODO\nendmodule\n",
       "module vend(input clk, input rst, input n, input d, output dispense);\n  localparam S0 = 2'd0, S5 = 2'd1, S10 = 2'd2;\n  reg [1:0] state, next;\n  always @(posedge clk) if (rst) state <= S0; else state <= next;\n  always @* begin\n    next = state;\n    case (state)\n      S0:  if (n) next = S5; else if (d) next = S10;\n      S5:  if (n) next = S10; else if (d) next = S0;\n      S10: if (n || d) next = S0;\n      default: next = S0;\n    endcase\n  end\n  assign dispense = (state == S5 && d) || (state == S10 && (n || d));\nendmodule\n",
       seqtb("vend", [("rst", 1), ("n", 1), ("d", 1)], [("dispense", 1)], [("in", {"rst": 1}), ("tick",), ("in", {"rst": 0, "n": 1}), ("exp", {"dispense": 0}, "5"), ("tick",), ("exp", {"dispense": 0}, "5+5"), ("tick",), ("exp", {"dispense": 1}, "5+5+5"), ("tick",),
            ("in", {"n": 0, "d": 1}), ("exp", {"dispense": 0}, "10"), ("tick",), ("exp", {"dispense": 1}, "10+10"), ("tick",), ("in", {"n": 1, "d": 0}), ("exp", {"dispense": 0}, "back at 0, 5"), ("tick",), ("in", {"n": 0, "d": 1}), ("exp", {"dispense": 1}, "5+10"), ("tick",)])),
])

# ---------------- chapter 13: hierarchy, parameters, generate, functions, memories ----------------
PTB = """`timescale 1ns/1ps
module tb;
  reg clk = 0; reg [11:0] d12 = 0; wire [11:0] q12; reg [2:0] d3 = 0; wire [2:0] q3;
  reg_n #(.N(12)) u12(.clk(clk), .d(d12), .q(q12));
  reg_n #(.N(3)) u3(.clk(clk), .d(d3), .q(q3));
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    d12 = 12'hABC; d3 = 3'd5;
    #1 clk = 1; #1 clk = 0; #1;
    if (q12 === 12'hABC && q3 === 3'd5) $display("ALL PASS"); else $display("q12=%h q3=%h: widths are not right", q12, q3);
    $finish;
  end
endmodule
"""
LAB_HIER = ("Lab 11: Parameters, generate, functions and memories", "Make designs reusable: a register of any width, a ripple adder of any length, a function, a ROM and a RAM.", 1500, [
    LV("A register of any width", "The same module is used twice: 12 bits wide and 3 bits wide. Add a parameter N with default 8 and use it for the widths: module reg_n #(parameter N = 8)(...)", "input [N-1:0] d, output reg [N-1:0] q",
       "module reg_n(input clk, input [7:0] d, output reg [7:0] q);\n  always @(posedge clk) q <= d;\nendmodule\n",
       "module reg_n #(parameter N = 8)(input clk, input [N-1:0] d, output reg [N-1:0] q);\n  always @(posedge clk) q <= d;\nendmodule\n", PTB),
    LV("An N-bit ripple adder with generate", "Write the chain once and let a generate loop repeat it N times. The full adder is given; c[0] is cin and c[N] is cout. Inside the loop use the loop variable i for the bit.", "genvar i; generate for (i = 0; i < N; i = i + 1) begin : fa full_adder f(.a(a[i]), .b(b[i]), .cin(c[i]), .sum(sum[i]), .cout(c[i+1])); end endgenerate",
       FAD + "\nmodule addn #(parameter N = 6)(input [N-1:0] a, input [N-1:0] b, input cin, output [N-1:0] sum, output cout);\n  wire [N:0] c;\n  assign c[0] = cin;\n  // TODO: genvar and generate for loop\n  assign cout = c[N];\nendmodule\n",
       FAD + "\nmodule addn #(parameter N = 6)(input [N-1:0] a, input [N-1:0] b, input cin, output [N-1:0] sum, output cout);\n  wire [N:0] c;\n  assign c[0] = cin;\n  genvar i;\n  generate\n    for (i = 0; i < N; i = i + 1) begin : fa\n      full_adder f(.a(a[i]), .b(b[i]), .cin(c[i]), .sum(sum[i]), .cout(c[i+1]));\n    end\n  endgenerate\n  assign cout = c[N];\nendmodule\n",
       vec_tb("addn #(.N(6))", [("a", 6), ("b", 6), ("cin", 1)], [("sum", 6), ("cout", 1)], lambda a, b, c: [(a + b + c) & 63, (a + b + c) >> 6], n=40)),
    LV("Binary to Gray code with a function", "In Gray code only one bit changes between neighbours. The rule is g = x ^ (x >> 1). Write it inside a function so it can be reused.", "function [3:0] to_gray; input [3:0] x; begin to_gray = x ^ (x >> 1); end endfunction",
       "module bin2gray(input [3:0] b, output [3:0] g);\n  function [3:0] to_gray;\n    input [3:0] x;\n    begin\n      // TODO: assign the result to the function name\n    end\n  endfunction\n  assign g = to_gray(b);\nendmodule\n",
       "module bin2gray(input [3:0] b, output [3:0] g);\n  function [3:0] to_gray;\n    input [3:0] x;\n    begin\n      to_gray = x ^ (x >> 1);\n    end\n  endfunction\n  assign g = to_gray(b);\nendmodule\n",
       vec_tb("bin2gray", [("b", 4)], [("g", 4)], lambda b: [b ^ (b >> 1)])),
    LV("A ROM of squares", "A memory is an array of registers: reg [7:0] mem [0:15]. Fill it once at time 0 with an initial block, mem[i] = i*i, and read it with a continuous assign.", "reg [7:0] mem [0:15]; integer i; initial for (i = 0; i < 16; i = i + 1) mem[i] = i * i; assign dout = mem[addr];",
       "module rom16(input [3:0] addr, output [7:0] dout);\n  // TODO: memory array, initial fill, read\n  assign dout = 8'd0;\nendmodule\n",
       "module rom16(input [3:0] addr, output [7:0] dout);\n  reg [7:0] mem [0:15];\n  integer i;\n  initial begin\n    for (i = 0; i < 16; i = i + 1) mem[i] = i * i;\n  end\n  assign dout = mem[addr];\nendmodule\n",
       vec_tb("rom16", [("addr", 4)], [("dout", 8)], lambda a: [(a * a) & 255])),
    LV("A RAM that you can write", "Same array, but now the clock writes it: when we = 1 the word at addr takes din on the rising edge. Reading is still immediate.", "always @(posedge clk) if (we) mem[addr] <= din; assign dout = mem[addr];",
       "module ram16(input clk, input we, input [3:0] addr, input [7:0] din, output [7:0] dout);\n  // TODO\n  assign dout = 8'd0;\nendmodule\n",
       "module ram16(input clk, input we, input [3:0] addr, input [7:0] din, output [7:0] dout);\n  reg [7:0] mem [0:15];\n  always @(posedge clk) begin\n    if (we) mem[addr] <= din;\n  end\n  assign dout = mem[addr];\nendmodule\n",
       seqtb("ram16", [("we", 1), ("addr", 4), ("din", 8)], [("dout", 8)], [("in", {"we": 1, "addr": 3, "din": 77}), ("tick",), ("in", {"addr": 9, "din": 200}), ("tick",), ("in", {"we": 0, "addr": 3}), ("exp", {"dout": 77}, "read 3"), ("in", {"addr": 9}), ("exp", {"dout": 200}, "read 9"),
            ("in", {"addr": 3, "din": 5}), ("tick",), ("exp", {"dout": 77}, "no write when we=0")])),
])

# ---------------- chapter 14: capstone, a tiny CPU ----------------
ALU = "module alu(input [7:0] a, input [7:0] b, input [1:0] op, output reg [7:0] y);\n  always @* begin\n    case (op)\n      2'd0: y = a + b;\n      2'd1: y = a - b;\n      2'd2: y = a & b;\n      default: y = a | b;\n    endcase\n  end\nendmodule\n\n"
PCM = "module pc(input clk, input rst, input en, input load, input [3:0] addr, output reg [3:0] pc);\n  always @(posedge clk) begin\n    if (rst) pc <= 4'd0;\n    else if (en) begin\n      if (load) pc <= addr;\n      else pc <= pc + 4'd1;\n    end\n  end\nendmodule\n\n"
CTL = "module control(input [3:0] op, output reg ld_imm, output reg use_alu, output reg [1:0] alu_op, output reg jnz, output reg out_en, output reg halt);\n  always @* begin\n    ld_imm = 0; use_alu = 0; alu_op = 2'd0; jnz = 0; out_en = 0; halt = 0;\n    case (op)\n      4'd0: ld_imm = 1;\n      4'd1: begin use_alu = 1; alu_op = 2'd0; end\n      4'd2: begin use_alu = 1; alu_op = 2'd1; end\n      4'd3: begin use_alu = 1; alu_op = 2'd2; end\n      4'd4: jnz = 1;\n      4'd5: out_en = 1;\n      4'd6: halt = 1;\n      default: ;\n    endcase\n  end\nendmodule\n\n"


def ROM(prog):
    lines = "".join("      4'd%d: instr = 8'h%02X;   // %s\n" % (i, v, c) for i, (v, c) in enumerate(prog))
    return "module rom(input [3:0] addr, output reg [7:0] instr);\n  always @* begin\n    case (addr)\n%s      default: instr = 8'h60;   // HALT\n    endcase\n  end\nendmodule\n\n" % lines


PROG_A = [(0x03, "LDI 3"), (0x14, "ADD 4"), (0x15, "ADD 5"), (0x50, "OUT"), (0x60, "HALT")]
PROG_B = [(0x04, "LDI 4"), (0x50, "OUT"), (0x21, "SUB 1"), (0x41, "JNZ 1"), (0x60, "HALT")]
CPU_TOP = "module cpu(input clk, input rst, output reg [7:0] out, output halted);\n  reg [7:0] acc;\n  wire [3:0] pc_val;\n  wire [7:0] instr, alu_y;\n  wire ld_imm, use_alu, jnz, out_en, halt;\n  wire [1:0] alu_op;\n%s  assign halted = halt;\nendmodule\n"
CPU_SOL = """  rom r(.addr(pc_val), .instr(instr));
  control c(.op(instr[7:4]), .ld_imm(ld_imm), .use_alu(use_alu), .alu_op(alu_op), .jnz(jnz), .out_en(out_en), .halt(halt));
  alu a(.a(acc), .b({4'b0000, instr[3:0]}), .op(alu_op), .y(alu_y));
  pc p(.clk(clk), .rst(rst), .en(~halt), .load(jnz && (acc != 8'd0)), .addr(instr[3:0]), .pc(pc_val));
  always @(posedge clk) begin
    if (rst) begin acc <= 8'd0; out <= 8'd0; end
    else begin
      if (ld_imm) acc <= {4'b0000, instr[3:0]};
      if (use_alu) acc <= alu_y;
      if (out_en) out <= acc;
    end
  end
"""
CPU_TB = """`timescale 1ns/1ps
module tb;
  reg clk = 0, rst = 1; wire [7:0] out; wire halted;
  cpu dut(.clk(clk), .rst(rst), .out(out), .halted(halted));
  always #5 clk = ~clk;
  integer n = 0, k = 0; reg [7:0] seq [0:15];
  always @(out) if (!rst) begin seq[k] = out; k = k + 1; end
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    #12 rst = 0;
    while (halted !== 1'b1 && n < 60) begin @(posedge clk); n = n + 1; end
    #1;
    $display("halted=%%b after %%0d clocks, last out=%%0d, %%0d outputs", halted, n, out, k);
    %s
    $finish;
  end
endmodule
"""
TB_A = CPU_TB % '    if (halted === 1\'b1 && out === 8\'d12) $display("ALL PASS"); else $display("wrong result (expected out=12 and halted)");'
TB_B = CPU_TB % '    if (halted === 1\'b1 && k == 4 && seq[0] == 4 && seq[1] == 3 && seq[2] == 2 && seq[3] == 1) $display("ALL PASS"); else $display("wrong output sequence");'
LAB_CPU = ("Lab 12: Capstone: build a tiny CPU", "A complete 8-bit accumulator processor, one block at a time: the ALU, the program counter, the control decoder, the top level, and finally your own program running on it.", 1700, [
    LV("The ALU", "The arithmetic unit: op 0 add, 1 subtract, 2 and, 3 or. It is combinational: an always @* block with a case.", "case (op) 2'd0: y = a + b; 2'd1: y = a - b; 2'd2: y = a & b; default: y = a | b; endcase",
       "module alu(input [7:0] a, input [7:0] b, input [1:0] op, output reg [7:0] y);\n  always @* begin\n    // TODO\n    y = 8'd0;\n  end\nendmodule\n", ALU.strip() + "\n",
       vec_tb("alu", [("a", 8), ("b", 8), ("op", 2)], [("y", 8)], lambda a, b, o: [[(a + b) & 255, (a - b) & 255, a & b, a | b][o]], n=48)),
    LV("The program counter", "pc says which instruction to fetch. On each clock: reset sets it to 0; if en is 0 it holds; if load is 1 it jumps to addr; otherwise it adds 1. It is 4 bits, so it wraps at 16.", "if (rst) pc <= 0; else if (en) begin if (load) pc <= addr; else pc <= pc + 1; end",
       "module pc(input clk, input rst, input en, input load, input [3:0] addr, output reg [3:0] pc);\n  // TODO\nendmodule\n", PCM.strip() + "\n",
       seqtb("pc", [("rst", 1), ("en", 1), ("load", 1), ("addr", 4)], [("pc", 4)], [("in", {"rst": 1}), ("tick",), ("exp", {"pc": 0}, "reset"), ("in", {"rst": 0, "en": 1}), ("tick", 3), ("exp", {"pc": 3}, "counts"), ("in", {"load": 1, "addr": 9}), ("tick",), ("exp", {"pc": 9}, "jump"),
            ("in", {"load": 0, "en": 0}), ("tick",), ("exp", {"pc": 9}, "hold"), ("in", {"en": 1}), ("tick", 7), ("exp", {"pc": 0}, "wraps")])),
    LV("The control decoder", "The top 4 bits of an instruction are the opcode. Decode them into control signals: 0 LDI (ld_imm), 1 ADD, 2 SUB, 3 AND (use_alu with alu_op 0, 1, 2), 4 JNZ (jnz), 5 OUT (out_en), 6 HALT (halt). Every other opcode does nothing. All signals must default to 0.", "Start the block by setting every output to 0, then override in a case.",
       "module control(input [3:0] op, output reg ld_imm, output reg use_alu, output reg [1:0] alu_op, output reg jnz, output reg out_en, output reg halt);\n  always @* begin\n    ld_imm = 0; use_alu = 0; alu_op = 2'd0; jnz = 0; out_en = 0; halt = 0;\n    // TODO: case (op)\n  end\nendmodule\n", CTL.strip() + "\n",
       combtb("control", [("op", 4)], [("ld_imm", 1), ("use_alu", 1), ("alu_op", 2), ("jnz", 1), ("out_en", 1), ("halt", 1)],
              [([o], [1 if o == 0 else 0, 1 if o in (1, 2, 3) else 0, {1: 0, 2: 1, 3: 2}.get(o, 0), 1 if o == 4 else 0, 1 if o == 5 else 0, 1 if o == 6 else 0]) for o in range(16)])),
    LV("Wire the processor", "All the parts are given. Write the top level: instantiate rom, control, alu and pc, and write the register block that updates acc (LDI loads the immediate, ALU instructions store the ALU result) and out (OUT copies acc). The program adds 3 + 4 + 5 and shows 12.", "pc stops when halt is 1 (en = ~halt). pc loads when jnz && acc != 0. The ALU's b input is {4'b0000, instr[3:0]} and its a input is acc.",
       ROM(PROG_A) + ALU + PCM + CTL + CPU_TOP % "  // TODO: instances and the register block\n", ROM(PROG_A) + ALU + PCM + CTL + CPU_TOP % CPU_SOL, TB_A,
       goals=[{"t": "The program halts", "re": r"halted=1"}, {"t": "out shows 12 (3 + 4 + 5)", "re": "ALL PASS"}]),
    LV("Write your own program", "Everything is built. Now you are the programmer: edit the ROM so the machine prints 4, 3, 2, 1 and halts. Instructions are 8 bits: the opcode on the left, the operand on the right. 0n LDI n, 1n ADD n, 2n SUB n, 3n AND n, 4a JNZ a (jump to address a if acc is not 0), 50 OUT, 60 HALT. Use a loop.", "LDI 4; OUT; SUB 1; JNZ 1; HALT is 04, 50, 21, 41, 60 at addresses 0 to 4.",
       ROM([(0x60, "HALT")]) + ALU + PCM + CTL + CPU_TOP % CPU_SOL, ROM(PROG_B) + ALU + PCM + CTL + CPU_TOP % CPU_SOL, TB_B,
       goals=[{"t": "It prints four values and halts", "re": r"halted=1 after \d+ clocks, last out=1, 4 outputs"}, {"t": "The values are 4, 3, 2, 1 in order", "re": "ALL PASS"}]),
])
LABS_C = [LAB_TB, LAB_FSM, LAB_HIER, LAB_CPU]
