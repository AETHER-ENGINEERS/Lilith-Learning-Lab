# -*- coding: utf-8 -*-
"""One hierarchical concept map per chapter of the Verilog course."""


def M(title, text):
    return (title, [ln.strip() for ln in text.strip().split("\n") if ln.strip()])


STRUCT = [
M("VLSI", """
VLSI | needs | Design flow
VLSI | viewed as | Y-chart
VLSI | built as | Four styles
Design flow | starts with | Specification
Design flow | then | RTL in Verilog
Design flow | then | Synthesis
Design flow | ends in | Fabrication
Y-chart | axis | Behavioural
Y-chart | axis | Structural
Y-chart | axis | Physical
Four styles | include | FPGA
Four styles | include | Standard cell
Four styles | include | Full custom
"""),
M("MOS transistor", """
MOS transistor | has | Gate
MOS transistor | has | Source and drain
MOS transistor | comes as | nMOS
MOS transistor | comes as | pMOS
MOS transistor | works in | Three regions
nMOS | conducts when | Gate is 1
pMOS | conducts when | Gate is 0
Three regions | is | Cutoff
Three regions | is | Linear
Three regions | is | Saturation
Current | grows with | W over L
"""),
M("CMOS logic", """
CMOS logic | has | Pull-up network
CMOS logic | has | Pull-down network
CMOS logic | example | Inverter
CMOS logic | example | NAND
CMOS logic | example | NOR
Pull-up network | uses | pMOS
Pull-down network | uses | nMOS
Pull-up network | is the dual of | Pull-down network
NAND | pull-down | Series
NOR | pull-down | Parallel
CMOS logic | spends | Dynamic power
"""),
M("Sequential logic", """
Sequential logic | needs | Memory
Memory | comes from | Feedback
Feedback | gives | Bistable circuit
Bistable circuit | made into | SR latch
Bistable circuit | made into | D latch
D latch | pair makes | Flip-flop
Flip-flop | triggered by | Clock edge
Flip-flop | kind | D
Flip-flop | kind | T
Flip-flop | kind | JK
SR latch | forbids | S and R both 1
"""),
M("Verilog basics", """
Verilog | describes | Hardware
Verilog | built from | Modules
Modules | have | Ports
Modules | contain | Gate primitives
Modules | contain | Instances
Ports | are | Input
Ports | are | Output
Instances | give | Hierarchy
Verilog | checked by | Testbench
Testbench | produces | Waveform
"""),
M("Data and operators", """
Data | held in | wire
Data | held in | reg
Data | has | Four values
Four values | include | x unknown
Four values | include | z undriven
Data | grouped into | Vectors
Vectors | use | Bit select
Vectors | use | Concatenation
Operators | include | Bitwise
Operators | include | Reduction
Operators | include | Conditional
assign | makes | Continuous connection
"""),
M("Combinational blocks", """
Combinational blocks | include | Adders
Combinational blocks | include | Multiplexers
Combinational blocks | include | Decoders
Combinational blocks | include | Encoders
Adders | include | Half adder
Adders | include | Full adder
Adders | chain into | Ripple carry
Ripple carry | limited by | Carry delay
Subtraction | uses | Two's complement
Subtraction | reuses | Adder
"""),
M("Behavioural Verilog", """
Behavioural Verilog | uses | always block
always block | with | Sensitivity list
Sensitivity list | is | always at star
Sensitivity list | is | posedge clk
Behavioural Verilog | uses | if and case
Behavioural Verilog | uses | Loops
always at star | makes | Combinational logic
posedge clk | makes | Flip-flops
Assignment | is | Blocking
Assignment | is | Non-blocking
Missing branch | causes | Latch
"""),
M("Sequential Verilog", """
Sequential Verilog | builds | Registers
Sequential Verilog | builds | Counters
Sequential Verilog | builds | Shift registers
Registers | have | Reset
Registers | have | Enable
Reset | is | Synchronous
Reset | is | Asynchronous
Counters | include | Up
Counters | include | Up-down
Counters | include | Ring
Shift registers | convert | Serial to parallel
"""),
M("Timing", """
Timing | concerns | Delays
Timing | concerns | Clock period
Timing | concerns | Setup and hold
Delays | are | Inertial
Delays | are | Transport
Delays | ignored by | Synthesis
Clock period | covers | Clock-to-q
Clock period | covers | Logic delay
Clock period | covers | Setup time
Critical path | sets | Maximum frequency
Setup and hold | broken gives | Metastability
"""),
M("Testbenches", """
Testbench | contains | DUT
Testbench | contains | Stimulus
Testbench | contains | Checker
Stimulus | includes | Clock
Stimulus | includes | Directed tests
Stimulus | includes | Random tests
Checker | uses | Reference model
Checker | reports | Pass or fail
Testbench | records | Waveform
Test | must be able to | Fail
"""),
M("State machines", """
FSM | has | State register
FSM | has | Next-state logic
FSM | has | Output logic
FSM | style | Moore
FSM | style | Mealy
Moore | output from | State only
Mealy | output from | State and input
FSM | example | Traffic light
FSM | example | Sequence detector
FSM | example | Vending machine
State register | holds | Encoding
"""),
M("Reuse and structure", """
Reuse | uses | Parameters
Reuse | uses | Generate
Reuse | uses | Functions
Reuse | uses | Memories
Parameters | set | Width
Generate | repeats | Hardware
Functions | compute | Values
Memories | include | ROM
Memories | include | RAM
Memories | are | Arrays of registers
"""),
M("RTL to chip", """
RTL | goes through | Synthesis
Synthesis | makes | Netlist
Netlist | goes to | FPGA flow
Netlist | goes to | ASIC flow
FPGA flow | gives | Bitstream
ASIC flow | gives | GDSII
Timing | checked by | Static analysis
RTL | builds | Tiny CPU
Tiny CPU | has | Datapath
Tiny CPU | has | Control
Datapath | contains | ALU
Datapath | contains | Program counter
"""),
]
MAPS = [[a] for a in STRUCT]
