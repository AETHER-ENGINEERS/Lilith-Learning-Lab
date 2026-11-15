#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Verilog course: VLSI basics, CMOS, sequential logic, Verilog and a tiny CPU.
14 chapters, 40 figures, 12 interactive labs (build/vl): two CMOS switch labs and ten that run Icarus Verilog (VeriSim, GPL-2.0) offline.
Usage: python3 make_verilog_course.py [out.json]"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vl"))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "cd"))
import cmk, vc_a, vc_b, vc_c, figs, maps as vmaps, build as vbuild, labs_all, labs_cmos  # noqa: E402
from clib import T  # noqa: E402

CHS = vc_a.CHS_A + vc_b.CHS_B + vc_c.CHS_C
assert len(CHS) == 14
# lab per chapter (None = no interactive lab): index in CHS -> (kind, lab tuple)
LV_ = labs_all.LABS     # watch, first, ops, comb, beh, seq, tb, fsm, hier, cpu
SW, GATES = labs_cmos.LABS_CMOS
LABMAP = {1: ("cmos", SW), 2: ("cmos", GATES), 3: ("vl", LV_[0]), 4: ("vl", LV_[1]), 5: ("vl", LV_[2]), 6: ("vl", LV_[3]), 7: ("vl", LV_[4]), 8: ("vl", LV_[5]),
          10: ("vl", LV_[6]), 11: ("vl", LV_[7]), 12: ("vl", LV_[8]), 13: ("vl", LV_[9])}
LAB_INTRO = {1: "Flip a gate voltage: an nMOS closes on 1, a pMOS on 0. Then join them into an inverter.",
             2: "Choose series or parallel for the pull-up and pull-down networks and build NAND, NOR and two complex gates.",
             3: "Write the stimulus yourself and watch latches and flip-flops hold, set, reset and ignore changes between clock edges.",
             4: "Compile and simulate real Verilog on your device: gate primitives, a half adder, a full adder from two half adders, and a mux.",
             5: "Write continuous assignments with operators: majority, nibble swap, reduction, comparison and arithmetic.",
             6: "Build a ripple adder, a subtractor, a 4-to-1 mux, a 3-to-8 decoder, a priority encoder and a parity checker.",
             7: "Use always, case, if, for and the = versus <= difference to build an ALU, arbiter, seven-segment decoder and popcount.",
             8: "Registers with reset and enable, counters, shift registers and a ring counter, checked by a clocked testbench.",
             10: "Write testbenches: a clock, an exhaustive loop, a bug-hunting test and random tests; then add a gate delay.",
             11: "Complete four state machines: a toggle, a traffic light, a 101 detector and a vending machine.",
             12: "Parameters, generate loops, a function, a ROM and a RAM.",
             13: "The capstone: build an 8-bit CPU block by block, then write your own program for it."}
HELP = "Each level lists goals that tick as you reach them. Hint explains and Show solution loads the answer; Run checks it. "
for _i, (_kind, _lab) in LABMAP.items():
    _title, _intro, _h, _levels = _lab
    _html = vbuild.cmos_html(_title, _intro, _levels) if _kind == "cmos" else vbuild.lab_html(_title, _intro, _levels)
    CHS[_i]["practice"].insert(0, {"type": "webxdc", "title": _title, "intro": HELP + LAB_INTRO[_i], "height": _h, "html": _html})

ANCHOR = re.compile(r"\s*\(See (Figure|Table) [\d.]+ below\.\)")
NFIG = NTAB = 0
for _ci, _ch in enumerate(CHS):
    _nf = _nt = 0
    _out = []
    for _b in _ch["lesson"]:
        if _b["type"] == "text":
            _b["items"] = [ANCHOR.sub("", it) for it in _b["items"]]
        if _b["type"] in ("figure", "table"):
            if _b["type"] == "figure":
                _nf += 1; _lab = "Figure %d.%d" % (_ci + 1, _nf); _b["caption"] = _lab + ". " + _b["caption"]
            else:
                _nt += 1; _lab = "Table %d.%d" % (_ci + 1, _nt); _b["title"] = _lab + ". " + _b["title"]
            for _p in reversed(_out):
                if _p["type"] == "text":
                    _p["items"][-1] = _p["items"][-1].rstrip() + " (See %s below.)" % _lab
                    break
        _out.append(_b)
    _ch["lesson"] = _out
    assert _nf >= 2 and _nt >= 2, (_ci + 1, _nf, _nt)
    NFIG += _nf; NTAB += _nt


def _split(t, lim=380):
    if len(t) <= lim:
        return [t]
    cuts = [m.end() for m in re.finditer(r"[.!?] (?=[A-Z(])", t) if t[:m.end()].count("$") % 2 == 0]
    if not cuts:
        return [t]
    k = min(cuts, key=lambda c: abs(c - len(t) / 2))
    return _split(t[:k].rstrip(), lim) + _split(t[k:], lim)


for _ch in CHS:
    for _b in _ch["lesson"]:
        if _b["type"] == "text":
            _b["items"] = [x for it in _b["items"] for x in _split(it)]

assert len(vmaps.MAPS) == len(CHS)
for _c, _ms in zip(CHS, vmaps.MAPS):
    _c["maps"] = [{"title": _t, "links": _l} for _t, _l in _ms]

for _i in range(1, len(CHS)):
    _prev = CHS[_i - 1]
    CHS[_i]["lesson"].insert(0, T("Quick recap of the last chapter, " + _prev["title"] + ":", *["• " + k for k in _prev["keyPoints"]]))

MNEM = [
 ("Describe, test, build", "VLSI flow: Describe, Test, Build. Spec, Architecture, RTL, Simulate, Synthesise, Place and route, Sign-off, Fab: 'Some Architects Really Seem Sleepy; Please Stay Focused.'"),
 ("N is one, P is zero", "nMOS conducts on one, pMOS on zero: 'N is oN for one, P is on for Plain zero.'"),
 ("Series down, parallel up (NAND)", "NAND: nMOS in Series, pMOS in Parallel. NOR is the Reverse. 'NAND stands Strong at the bottom.'"),
 ("A latch is a gate, a flop is a clock", "Latch follows the Level; Flip-flop samples at the Flank: 'Latch = Level, Flop = Flank.'"),
 ("Output first", "A gate primitive lists the Output first: and (OUT, in, in). 'Out first, then in.'"),
 ("Bitwise and, logical and", "One ampersand works bit by bit; two give one yes or no. 'One is Bits, Two is Truth.'"),
 ("Invert and add one", "Subtract by 'Invert and add one': a - b = a + ~b + 1."),
 ("Equals now, arrow later", "= happens Now; <= happens Later, together. 'Logic is equals, flops are arrows.'"),
 ("Reset first, enable next", "Order in a register: Reset, Load, Enable, Hold: 'Real Lions Eat Humans.'"),
 ("Tcq plus logic plus setup", "Clock period covers tcq + logic + setup: 'Clock, Logic, Setup: C-L-S.'"),
 ("A test must be able to fail", "Boundaries break things: Equal, Zero, Max, Wrap. 'Every Zebra Must Wander.'"),
 ("State, next, output", "Every FSM: State register, Next-state logic, Output logic: 'SNO': Snow. Moore = State only, Mealy = Mixed with input."),
 ("Knob, loop, array", "Reuse: parameter is a Knob, generate is a Loop, memory is an Array."),
 ("Fetch, decode, execute, write", "One CPU instruction: Fetch, Decode, Execute, Write back: 'FDEW'."),
]
assert len(MNEM) == len(CHS)
for _c, (_m, _d) in zip(CHS, MNEM):
    _full = _m + ". " + _d
    _c["lesson"].append(T("Memory trick: " + _full))
    _c["cards"].append({"q": "Memory trick for: " + _c["title"] + "?", "a": _full})
IMAGES = figs.build_all()

PRONOUNCE = {"VLSI": "V L S I", "Verilog": "VAIR i log", "VHDL": "V H D L", "HDL": "H D L", "RTL": "R T L", "FPGA": "F P G A", "ASIC": "A sick", "CMOS": "sea moss", "nMOS": "N moss", "pMOS": "P moss", "MOSFET": "moss fet", "MOS": "moss",
    "NAND": "nand", "NOR": "nor", "XOR": "ex or", "XNOR": "ex nor", "ALU": "A L U", "FSM": "F S M", "VCD": "V C D", "ROM": "rom", "RAM": "ram", "GDSII": "G D S two", "DUT": "D U T", "VDD": "V D D", "GND": "ground", "Vgs": "V G S", "Vds": "V D S",
    "Vt": "V T", "tcq": "T C Q", "tsu": "T setup", "mux": "mucks", "SSI": "S S I", "MSI": "M S I", "LSI": "L S I", "JNZ": "J N Z", "LDI": "L D I", "ISA": "I S A", "pc": "P C", "acc": "A C C", "Icarus": "ICK a russ", "VeriSim": "VAIR i sim",
    "WebAssembly": "web assembly", "Yosys": "YO sis", "SystemVerilog": "system VAIR i log", "UVM": "U V M", "SR": "S R", "JK": "J K", "IEEE": "I triple E", "Gajski": "GUY ski", "localparam": "local param", "genvar": "gen var", "posedge": "pos edge", "negedge": "neg edge",
    "iverilog": "I VAIR i log", "timescale": "time scale", "reg": "reg", "wire": "wire", "bitstream": "bit stream", "netlist": "net list", "testbench": "test bench", "VeriSim's": "VAIR i sim's"}

SANDBOX = cmk.terminal("Verilog cheat sheet", "verilog>", "A scripted lookup, not a simulator. Try: module, gates, numbers, operators, assign, always, ff, reset, case, fsm, clock, tb, delay, param, memory, flow", [
    ("module", ["module name(input a, input b, output y);", "  // contents", "endmodule", "instance: name inst(.a(x), .b(z), .y(w));"]),
    ("gates", ["and (y,a,b); or (y,a,b); nand nor xor xnor", "not (y,a); buf (y,a);", "the OUTPUT comes first"]),
    ("numbers", ["4'b1010  size 4, binary", "8'hFF  size 8, hex   12'd100  size 12, decimal", "values: 0 1 x (unknown) z (not driven)"]),
    ("operators", ["bitwise & | ^ ~   reduction &x |x ^x", "logical && || !   relational < > <= >=", "equality == != (=== !== exact)   shift << >>", "conditional s ? b : a   concat {a,b} {4{a}}"]),
    ("assign", ["assign y = a & b;", "a continuous connection: y always follows the expression", "left side must be a wire"]),
    ("always", ["always @*  { ... }       combinational, use =", "always @(posedge clk) sequential, use <=", "assign every output on every path, or a latch appears"]),
    ("ff", ["always @(posedge clk) q <= d;", "with enable: if (en) q <= d;", "with reset: if (rst) q <= 0; else ..."]),
    ("reset", ["sync:  always @(posedge clk)", "async: always @(posedge clk or negedge rst_n)", "reset first in the if chain"]),
    ("case", ["case (op)", "  2'd0: y = a + b;", "  default: y = 0;", "endcase"]),
    ("fsm", ["state register (clocked, <=)", "next-state logic (always @*, case)", "output logic (assign)", "Moore: from state; Mealy: state and input"]),
    ("clock", ["reg clk = 0;", "always #5 clk = ~clk;   // period 10"]),
    ("tb", ["no ports; reg inputs, wire outputs, DUT instance, initial begin ... end", "dumpfile and dumpvars record a waveform; finish ends the run", "check with !== and count errors"]),
    ("delay", ["`timescale 1ns/1ps", "#10 wait 10 units    assign #2 y = ~a;", "ignored by synthesis"]),
    ("param", ["module m #(parameter N = 8)(input [N-1:0] d, ...);", "m #(.N(12)) u1(...);", "genvar i; generate for (i=0;i<N;i=i+1) begin ... end endgenerate"]),
    ("memory", ["reg [7:0] mem [0:15];   16 words of 8 bits", "write: always @(posedge clk) if (we) mem[addr] <= din;", "read:  assign dout = mem[addr];"]),
    ("flow", ["spec, architecture, RTL, simulate, synthesise, place and route, sign-off, fab", "clock period >= tcq + tlogic + tsu"]),
])

EXAM = [
 ("What does VLSI stand for?", ["Very large scale integration", "Very low supply integration", "Variable logic signal interface", "Verified layout simulation inspection"], 0, "Chips with huge numbers of transistors."),
 ("Which step turns RTL into gates?", ["Synthesis", "Simulation", "Specification", "Fabrication"], 0, "A synthesis tool maps RTL to a netlist."),
 ("The three axes of the Y-chart are...", ["behavioural, structural, physical", "input, output, clock", "analogue, digital, mixed", "spec, design, test"], 0, "What it does, what it is made of, where it sits."),
 ("Which design style is reprogrammable after manufacture?", ["FPGA", "standard cell", "full custom", "gate array"], 0, "It loads a bitstream."),
 ("An nMOS transistor conducts when its gate is...", ["1", "0", "floating", "negative"], 0, "pMOS is the opposite."),
 ("Which MOSFET region acts like a resistor?", ["linear", "cutoff", "saturation", "breakdown"], 0, "At small Vds."),
 ("Increasing W/L of a transistor...", ["raises its current", "lowers its current", "has no effect", "sets its threshold"], 0, "k is proportional to W/L."),
 ("In a CMOS NAND gate the nMOS transistors are...", ["in series", "in parallel", "absent", "all tied to VDD"], 0, "Both must be on to pull down."),
 ("The CMOS pull-up network is...", ["the dual of the pull-down", "identical to it", "made of nMOS", "optional"], 0, "Swap series and parallel."),
 ("Why is idle CMOS power so small?", ["no steady path from VDD to ground", "it has no transistors", "it is off", "it is analogue"], 0, "One network is always off."),
 ("Dynamic power scales as...", ["C V squared f", "V f only", "C only", "1/f"], 0, "P = alpha C V squared f."),
 ("Which input of an SR latch (NOR) is forbidden?", ["S = 1 and R = 1", "S = 0 and R = 0", "S = 1, R = 0", "S = 0, R = 1"], 0, "Both outputs go low."),
 ("A flip-flop samples its input...", ["at the clock edge", "continuously", "only at reset", "never"], 0, "Edge triggered."),
 ("A D flip-flop is made from...", ["two latches with opposite enables", "one NAND gate", "a resistor", "a counter"], 0, "Master and slave."),
 ("In and (y, a, b), the output is...", ["y", "a", "b", "all three"], 0, "Output first."),
 ("A wire in Verilog...", ["carries but cannot store a value", "stores a value", "must be 8 bits", "is only an input"], 0, "A named connection."),
 ("The ordering of gate statements in a module...", ["does not matter: all exist at once", "sets the execution order", "only matters for xor", "matters for nand"], 0, "Hardware, not a program."),
 ("What does 8'hA5 denote?", ["an 8-bit hexadecimal number", "decimal 8", "a 5-bit number", "an unsized number"], 0, "Size, base, digits."),
 ("Which operator gives the parity of a vector?", ["^x", "&x", "||", "~x"], 0, "Reduction xor."),
 ("The Verilog value z means...", ["not driven (high impedance)", "zero", "unknown", "one"], 0, "x is unknown."),
 ("In a full adder the carry out is...", ["the majority of a, b, cin", "a xor b", "a and b only", "always 1"], 0, "At least two are 1."),
 ("a - b in two's complement is...", ["a + ~b + 1", "a + b", "~a + b", "a - ~b"], 0, "Invert and add one."),
 ("Why is a ripple-carry adder slow?", ["the carry passes through every stage", "it has no gates", "it needs a clock", "it is analogue"], 0, "Delay grows with width."),
 ("What does always @* make?", ["combinational logic", "a flip-flop", "a clock", "memory"], 0, "Sensitive to everything it reads."),
 ("An accidental latch appears when...", ["a path in a combinational block assigns nothing", "a clock is used", "a case has a default", "a reset is async"], 0, "It must remember."),
 ("In a clocked block you should use...", ["<=", "=", "assign", "force"], 0, "Non-blocking."),
 ("Swapping a and b with a = b; b = a; gives...", ["both equal to the old b", "a swap", "an error", "both zero"], 0, "The second line sees the new a."),
 ("Which line is a D flip-flop?", ["always @(posedge clk) q <= d;", "assign q = d;", "always @* q = d;", "initial q = d;"], 0, "Clock edge and <=."),
 ("Asynchronous reset needs...", ["negedge rst_n in the sensitivity list", "no clock", "a second reset", "an initial block"], 0, "It reacts to the reset edge."),
 ("A 4-bit counter after 15 goes to...", ["0", "16", "x", "stops"], 0, "Wraps."),
 ("A delay such as assign #2 y = ~a; in synthesis is...", ["ignored", "implemented", "an error", "a latch"], 0, "Only for simulation."),
 ("Setup time is...", ["stability required before the clock edge", "after the edge", "the period", "a gate delay"], 0, "Hold is after."),
 ("The clock period must be at least...", ["tcq + tlogic + tsu", "tcq only", "tsu only", "tlogic - tcq"], 0, "Launch, logic, capture."),
 ("A testbench has...", ["no ports", "only inputs", "only outputs", "an enable"], 0, "It is the outer world."),
 ("To compare with x counted as a mismatch use...", ["!==", "!=", "<>", "~="], 0, "Case inequality."),
 ("A clock with period 10 is made by...", ["always #5 clk = ~clk;", "always #10 clk = 1;", "assign clk = 10;", "initial clk = 10;"], 0, "Toggle every half period."),
 ("A Moore machine's outputs depend on...", ["the state only", "state and inputs", "inputs only", "the clock only"], 0, "Mealy uses inputs too."),
 ("Which three parts does every FSM have?", ["state register, next-state logic, output logic", "ALU, pc, rom", "mux, decoder, encoder", "clock, reset, enable"], 0, "Register plus two combinational blocks."),
 ("A parameter N is overridden with...", ["m #(.N(12)) u1(...);", "m u1(N = 12);", "defparam only", "it cannot be"], 0, "Use the #( ) list."),
 ("reg [7:0] mem [0:15]; declares...", ["16 words of 8 bits", "8 words of 16 bits", "a 128-bit register", "one byte"], 0, "Width first, depth after."),
 ("In the tiny CPU the opcode is in...", ["instruction bits 7 to 4", "bits 3 to 0", "the pc", "the ROM address"], 0, "The operand is in the lower four."),
]
print("exam", len(EXAM))

CFG = dict(id="verilog-digital-design", title="Verilog and Digital Design: From Transistors to a Working CPU",
    subtitle="A hands-on beginner course on VLSI, CMOS logic, sequential circuits and Verilog, with labs that compile and simulate real Verilog on your device",
    description="This course takes you from a single transistor to a working 8-bit processor, in 14 chapters. It starts with the VLSI design flow, the Y-chart and the four design styles, then the MOS transistor as a switch, CMOS gates and duality, latches and flip-flops. "
    "Then it teaches Verilog step by step: modules and gate primitives, data types and operators, adders, multiplexers and decoders, behavioural modelling with always, if and case, registers, counters and shift registers, delays and timing, testbenches, finite state machines, parameters, generate and memories, "
    "and finally the road from RTL to silicon, ending in a capstone where you build a tiny CPU block by block and write a program for it. "
    "There are 40 numbered figures (waveforms, schematics and timing diagrams drawn from the same ideas you code), numbered tables, a recap, a memory trick, an expanded ELI5 and a concept map in every chapter. "
    "12 interactive labs: two CMOS switch labs, and ten labs that compile and simulate Verilog fully offline using the Icarus Verilog engine from the VeriSim project, with a console, a waveform viewer and self-checking testbenches. "
    "Every level starts unsolved, tells you what to build, gives a hint, and ticks its goals when the simulation passes. "
    "Sources and credits: the outline of the first chapters follows the TutorialsPoint VLSI Design quick guide (text, figures and labs here are original). The simulator is VeriSim by senolgulgonul, which packages Icarus Verilog (GPL v2 or later) compiled to WebAssembly; the unmodified engine files are included in the labs under their GPL-2.0 licence.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, images=IMAGES)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "verilog-digital-design.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
    print("figures", NFIG, "tables", NTAB)
