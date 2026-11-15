# -*- coding: utf-8 -*-
"""Verilog labs for chapters 7-9: combinational blocks, behavioural modelling, sequential circuits."""
from lib import *
from labs_a import gate_tb, vec_tb

FA = "module full_adder(input a, input b, input cin, output sum, output cout);\n  assign sum = a ^ b ^ cin;\n  assign cout = (a & b) | (cin & (a ^ b));\nendmodule\n\n"
LAB_COMB = ("Lab 6: Combinational building blocks", "Adders, subtractors, multiplexers, decoders and encoders: the parts every datapath is made from.", 1500, [
    LV("A 4-bit ripple-carry adder", "Chain four full adders: the carry-out of each one feeds the carry-in of the next. The full_adder module is given. Use the wire vector c to carry the carries.", "full_adder f0(.a(a[0]), .b(b[0]), .cin(cin), .sum(sum[0]), .cout(c[1])); ... the last cout is c[4], and c[0] is cin.",
       FA + "module adder4(input [3:0] a, input [3:0] b, input cin, output [3:0] sum, output cout);\n  wire [4:0] c;\n  assign c[0] = cin;\n  // TODO: four full_adder instances, then assign cout = c[4];\nendmodule\n",
       FA + "module adder4(input [3:0] a, input [3:0] b, input cin, output [3:0] sum, output cout);\n  wire [4:0] c;\n  assign c[0] = cin;\n  full_adder f0(.a(a[0]), .b(b[0]), .cin(c[0]), .sum(sum[0]), .cout(c[1]));\n  full_adder f1(.a(a[1]), .b(b[1]), .cin(c[1]), .sum(sum[1]), .cout(c[2]));\n  full_adder f2(.a(a[2]), .b(b[2]), .cin(c[2]), .sum(sum[2]), .cout(c[3]));\n  full_adder f3(.a(a[3]), .b(b[3]), .cin(c[3]), .sum(sum[3]), .cout(c[4]));\n  assign cout = c[4];\nendmodule\n",
       vec_tb("adder4", [("a", 4), ("b", 4), ("cin", 1)], [("sum", 4), ("cout", 1)], lambda a, b, c: [(a + b + c) & 15, (a + b + c) >> 4], n=40)),
    LV("A subtractor from an adder", "a - b is a + (not b) + 1 in two's complement. Compute the 5-bit result {nb, diff} = {1'b0,a} + {1'b0,~b} + 5'd1 (widen every operand to 5 bits, or the ~b gets extended with ones!). The carry nb is 1 when no borrow was needed, so borrow = ~nb.", "wire nb; assign {nb, diff} = {1'b0, a} + {1'b0, ~b} + 5'd1; assign borrow = ~nb;",
       "module sub4(input [3:0] a, input [3:0] b, output [3:0] diff, output borrow);\n  // TODO\nendmodule\n",
       "module sub4(input [3:0] a, input [3:0] b, output [3:0] diff, output borrow);\n  wire nb;\n  assign {nb, diff} = {1'b0, a} + {1'b0, ~b} + 5'd1;\n  assign borrow = ~nb;\nendmodule\n",
       vec_tb("sub4", [("a", 4), ("b", 4)], [("diff", 4), ("borrow", 1)], lambda a, b: [(a - b) & 15, 1 if a < b else 0], n=40)),
    LV("A 4-to-1 multiplexer", "A 2-bit select picks one of four 4-bit inputs. Nest conditional operators, or compare s with each number.", "assign y = (s == 2'd0) ? a : (s == 2'd1) ? b : (s == 2'd2) ? c : d;",
       "module mux4(input [3:0] a, input [3:0] b, input [3:0] c, input [3:0] d, input [1:0] s, output [3:0] y);\n  // TODO\nendmodule\n",
       "module mux4(input [3:0] a, input [3:0] b, input [3:0] c, input [3:0] d, input [1:0] s, output [3:0] y);\n  assign y = (s == 2'd0) ? a : (s == 2'd1) ? b : (s == 2'd2) ? c : d;\nendmodule\n",
       vec_tb("mux4", [("a", 4), ("b", 4), ("c", 4), ("d", 4), ("s", 2)], [("y", 4)], lambda a, b, c, d, s: [[a, b, c, d][s]], n=40)),
    LV("A 3-to-8 decoder with enable", "Exactly one output line goes high: the one whose number is on a. If en = 0 all eight outputs are 0. Shifting helps: 8'b1 << a.", "assign y = en ? (8'b1 << a) : 8'b0;",
       "module dec38(input [2:0] a, input en, output [7:0] y);\n  // TODO\nendmodule\n", "module dec38(input [2:0] a, input en, output [7:0] y);\n  assign y = en ? (8'b1 << a) : 8'b0;\nendmodule\n",
       vec_tb("dec38", [("a", 3), ("en", 1)], [("y", 8)], lambda a, e: [(1 << a) if e else 0])),
    LV("A priority encoder", "Four request lines x[3:0]; code is the number of the highest line that is set, and valid says at least one is set. If x = 0 then valid = 0 and code = 0.", "valid = |x; code = x[3] ? 3 : x[2] ? 2 : x[1] ? 1 : 0;",
       "module penc4(input [3:0] x, output [1:0] code, output valid);\n  // TODO\nendmodule\n",
       "module penc4(input [3:0] x, output [1:0] code, output valid);\n  assign valid = |x;\n  assign code = x[3] ? 2'd3 : x[2] ? 2'd2 : x[1] ? 2'd1 : 2'd0;\nendmodule\n",
       vec_tb("penc4", [("x", 4)], [("code", 2), ("valid", 1)], lambda x: [(x.bit_length() - 1) if x else 0, 1 if x else 0])),
    LV("A parity checker", "A word of 8 bits is sent with even parity: the number of ones must be even. error is 1 when it is odd. One reduction operator does it.", "assign error = ^word;",
       "module pcheck(input [7:0] word, output error);\n  // TODO\nendmodule\n", "module pcheck(input [7:0] word, output error);\n  assign error = ^word;\nendmodule\n",
       vec_tb("pcheck", [("word", 8)], [("error", 1)], lambda w: [bin(w).count("1") & 1], n=30)),
])

# ---------------- chapter 8 ----------------
LAB_BEH = ("Lab 7: Behavioural modelling", "always blocks, if and case, loops, and the difference between = and <=.", 1500, [
    LV("A four-function ALU with case", "op chooses: 0 add, 1 subtract, 2 and, 3 or. In an always @* block every path must assign y, so give y a value in each case.", "always @* case (op) 2'd0: y = a + b; 2'd1: y = a - b; 2'd2: y = a & b; default: y = a | b; endcase",
       "module alu4(input [3:0] a, input [3:0] b, input [1:0] op, output reg [3:0] y);\n  always @* begin\n    // TODO: case (op) ... endcase\n  end\nendmodule\n",
       "module alu4(input [3:0] a, input [3:0] b, input [1:0] op, output reg [3:0] y);\n  always @* begin\n    case (op)\n      2'd0: y = a + b;\n      2'd1: y = a - b;\n      2'd2: y = a & b;\n      default: y = a | b;\n    endcase\n  end\nendmodule\n",
       vec_tb("alu4", [("a", 4), ("b", 4), ("op", 2)], [("y", 4)], lambda a, b, o: [[(a + b) & 15, (a - b) & 15, a & b, a | b][o]], n=48)),
    LV("A priority arbiter with if / else if", "Four requesters; req[0] has the highest priority. grant is one-hot: only the highest-priority active request gets its bit. If nobody asks, grant is 0.", "if (req[0]) grant = 4'b0001; else if (req[1]) grant = 4'b0010; ... else grant = 4'b0000;",
       "module arbiter(input [3:0] req, output reg [3:0] grant);\n  always @* begin\n    // TODO\n  end\nendmodule\n",
       "module arbiter(input [3:0] req, output reg [3:0] grant);\n  always @* begin\n    if (req[0]) grant = 4'b0001;\n    else if (req[1]) grant = 4'b0010;\n    else if (req[2]) grant = 4'b0100;\n    else if (req[3]) grant = 4'b1000;\n    else grant = 4'b0000;\n  end\nendmodule\n",
       vec_tb("arbiter", [("req", 4)], [("grant", 4)], lambda r: [(r & -r) if r else 0])),
    LV("A seven-segment decoder", "Segments are g f e d c b a, bit 6 down to bit 0, and 1 means lit. Digits 0 to 3 are done. Add 4 to 9 (0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F) and make everything else blank.", "4: seg = 7'h66; 5: seg = 7'h6D; 6: seg = 7'h7D; 7: seg = 7'h07; 8: seg = 7'h7F; 9: seg = 7'h6F; default: seg = 7'h00;",
       "module seg7(input [3:0] digit, output reg [6:0] seg);\n  always @* begin\n    case (digit)\n      4'd0: seg = 7'h3F;\n      4'd1: seg = 7'h06;\n      4'd2: seg = 7'h5B;\n      4'd3: seg = 7'h4F;\n      // TODO: 4 to 9 and default\n    endcase\n  end\nendmodule\n",
       "module seg7(input [3:0] digit, output reg [6:0] seg);\n  always @* begin\n    case (digit)\n      4'd0: seg = 7'h3F;\n      4'd1: seg = 7'h06;\n      4'd2: seg = 7'h5B;\n      4'd3: seg = 7'h4F;\n      4'd4: seg = 7'h66;\n      4'd5: seg = 7'h6D;\n      4'd6: seg = 7'h7D;\n      4'd7: seg = 7'h07;\n      4'd8: seg = 7'h7F;\n      4'd9: seg = 7'h6F;\n      default: seg = 7'h00;\n    endcase\n  end\nendmodule\n",
       vec_tb("seg7", [("digit", 4)], [("seg", 7)], lambda d: [[0x3F, 6, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 7, 0x7F, 0x6F][d] if d < 10 else 0])),
    LV("Count the ones with a for loop", "A for loop inside always @* is unrolled into hardware. Count the ones in an 8-bit word: start n at 0, then add x[i] for i from 0 to 7.", "n = 0; for (i = 0; i < 8; i = i + 1) n = n + x[i];",
       "module popcount(input [7:0] x, output reg [3:0] n);\n  integer i;\n  always @* begin\n    // TODO\n  end\nendmodule\n",
       "module popcount(input [7:0] x, output reg [3:0] n);\n  integer i;\n  always @* begin\n    n = 0;\n    for (i = 0; i < 8; i = i + 1)\n      n = n + x[i];\n  end\nendmodule\n",
       vec_tb("popcount", [("x", 8)], [("n", 4)], lambda x: [bin(x).count("1")], n=40)),
    LV("Swap two registers: blocking or not?", "On every clock edge a and b should swap. With blocking = the first line changes a at once and the second line then copies the new a, so both end up equal. Fix it with the non-blocking assignment <=.", "Use a <= b; b <= a; so both right-hand sides are read before either register changes.",
       "module swapper(input clk, output reg [3:0] a, output reg [3:0] b);\n  initial begin a = 3; b = 5; end\n  always @(posedge clk) begin\n    a = b;\n    b = a;\n  end\nendmodule\n",
       "module swapper(input clk, output reg [3:0] a, output reg [3:0] b);\n  initial begin a = 3; b = 5; end\n  always @(posedge clk) begin\n    a <= b;\n    b <= a;\n  end\nendmodule\n",
       """`timescale 1ns/1ps
module tb;
  reg clk = 0; wire [3:0] a, b;
  swapper dut(.clk(clk), .a(a), .b(b));
  initial begin
    $dumpfile("dump.vcd"); $dumpvars(0, tb);
    #1 clk = 1; #1 clk = 0; #1;
    if (a === 4'd5 && b === 4'd3) $display("ALL PASS: swapped once"); else $display("a=%0d b=%0d: not swapped", a, b);
    #1 clk = 1; #1 clk = 0; #1;
    if (a === 4'd3 && b === 4'd5) $display("swapped back"); else $display("second swap wrong: a=%0d b=%0d", a, b);
    #2 $finish;
  end
endmodule
""", extra=[{"t": "A second clock swaps them back", "re": "swapped back"}]),
])

# ---------------- chapter 9 ----------------
LAB_SEQ = ("Lab 8: Sequential circuits", "Flip-flops with reset and enable, counters and shift registers, checked by a clocked testbench.", 1500, [
    LV("A register with asynchronous reset and enable", "q is cleared the moment rst_n goes low, with no clock needed. Otherwise on each rising edge q takes d, but only if en is 1.", "always @(posedge clk or negedge rst_n) if (!rst_n) q <= 0; else if (en) q <= d;",
       "module reg4(input clk, input rst_n, input en, input [3:0] d, output reg [3:0] q);\n  // TODO: always @(posedge clk or negedge rst_n)\nendmodule\n",
       "module reg4(input clk, input rst_n, input en, input [3:0] d, output reg [3:0] q);\n  always @(posedge clk or negedge rst_n) begin\n    if (!rst_n) q <= 4'd0;\n    else if (en) q <= d;\n  end\nendmodule\n",
       seqtb("reg4", [("rst_n", 1), ("en", 1), ("d", 4)], [("q", 4)], [("in", {"rst_n": 0, "d": 9}), ("exp", {"q": 0}, "async reset"), ("in", {"rst_n": 1, "en": 0}), ("tick",), ("exp", {"q": 0}, "enable low holds"),
            ("in", {"en": 1}), ("tick",), ("exp", {"q": 9}, "load 9"), ("in", {"d": 4, "en": 0}), ("tick",), ("exp", {"q": 9}, "hold 9"), ("in", {"rst_n": 0}), ("exp", {"q": 0}, "reset without a clock")])),
    LV("A 4-bit counter", "Count up on every rising edge. A synchronous reset (checked inside the clocked block) sends it to 0. It must wrap from 15 back to 0 by itself.", "always @(posedge clk) if (rst) count <= 0; else count <= count + 1;",
       "module counter4(input clk, input rst, output reg [3:0] count);\n  // TODO\nendmodule\n",
       "module counter4(input clk, input rst, output reg [3:0] count);\n  always @(posedge clk) begin\n    if (rst) count <= 4'd0;\n    else count <= count + 4'd1;\n  end\nendmodule\n",
       seqtb("counter4", [("rst", 1)], [("count", 4)], [("in", {"rst": 1}), ("tick",), ("exp", {"count": 0}, "reset"), ("in", {"rst": 0}), ("tick", 5), ("exp", {"count": 5}, "five clocks"), ("tick", 10), ("exp", {"count": 15}, "fifteen"), ("tick",), ("exp", {"count": 0}, "wraps to 0")])),
    LV("An up/down counter with load", "up = 1 counts up, up = 0 counts down. When load = 1 the counter takes value d instead. Reset is synchronous and has priority.", "if (rst) ... else if (load) count <= d; else if (up) count <= count + 1; else count <= count - 1;",
       "module udcount(input clk, input rst, input load, input up, input [3:0] d, output reg [3:0] count);\n  // TODO\nendmodule\n",
       "module udcount(input clk, input rst, input load, input up, input [3:0] d, output reg [3:0] count);\n  always @(posedge clk) begin\n    if (rst) count <= 4'd0;\n    else if (load) count <= d;\n    else if (up) count <= count + 4'd1;\n    else count <= count - 4'd1;\n  end\nendmodule\n",
       seqtb("udcount", [("rst", 1), ("load", 1), ("up", 1), ("d", 4)], [("count", 4)], [("in", {"rst": 1}), ("tick",), ("in", {"rst": 0, "up": 1}), ("tick", 3), ("exp", {"count": 3}, "up 3"), ("in", {"up": 0}), ("tick", 5), ("exp", {"count": 14}, "down 5 wraps"),
            ("in", {"load": 1, "d": 7}), ("tick",), ("exp", {"count": 7}, "load 7"), ("in", {"load": 0, "up": 1}), ("tick",), ("exp", {"count": 8}, "up after load")])),
    LV("A shift register", "On each clock the bits move one place to the left and din enters at bit 0: q <= {q[2:0], din}. Reset clears it. Send 1, 0, 1, 1 and q reads 1011.", "always @(posedge clk) if (rst) q <= 0; else q <= {q[2:0], din};",
       "module shift4(input clk, input rst, input din, output reg [3:0] q);\n  // TODO\nendmodule\n",
       "module shift4(input clk, input rst, input din, output reg [3:0] q);\n  always @(posedge clk) begin\n    if (rst) q <= 4'd0;\n    else q <= {q[2:0], din};\n  end\nendmodule\n",
       seqtb("shift4", [("rst", 1), ("din", 1)], [("q", 4)], [("in", {"rst": 1}), ("tick",), ("in", {"rst": 0, "din": 1}), ("tick",), ("exp", {"q": 1}, "first bit"), ("in", {"din": 0}), ("tick",), ("exp", {"q": 2}, "second"), ("in", {"din": 1}), ("tick",), ("in", {"din": 1}), ("tick",), ("exp", {"q": 11}, "1011"), ("in", {"din": 0}), ("tick", 4), ("exp", {"q": 0}, "flushed")])),
    LV("A ring counter", "Reset puts a single 1 in the lowest bit (0001). On every clock the 1 rotates one place left and wraps from bit 3 to bit 0: it walks around the ring.", "if (rst) q <= 4'b0001; else q <= {q[2:0], q[3]};",
       "module ring4(input clk, input rst, output reg [3:0] q);\n  // TODO\nendmodule\n",
       "module ring4(input clk, input rst, output reg [3:0] q);\n  always @(posedge clk) begin\n    if (rst) q <= 4'b0001;\n    else q <= {q[2:0], q[3]};\n  end\nendmodule\n",
       seqtb("ring4", [("rst", 1)], [("q", 4)], [("in", {"rst": 1}), ("tick",), ("exp", {"q": 1}, "reset"), ("in", {"rst": 0}), ("tick",), ("exp", {"q": 2}, "2"), ("tick",), ("exp", {"q": 4}, "4"), ("tick",), ("exp", {"q": 8}, "8"), ("tick",), ("exp", {"q": 1}, "wraps")])),
])
LABS_B = [LAB_COMB, LAB_BEH, LAB_SEQ]
