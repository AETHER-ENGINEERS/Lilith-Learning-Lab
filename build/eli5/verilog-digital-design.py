# -*- coding: utf-8 -*-
"""Expanded ELI5 blocks for the Verilog course (one per chapter)."""
import re


def _split(t, lim=380):
    if len(t) <= lim:
        return [t]
    cuts = [m.end() for m in re.finditer(r"[.!?] (?=[A-Z(])", t)]
    if not cuts:
        return [t]
    k = min(cuts, key=lambda c: abs(c - len(t) / 2))
    return _split(t[:k].rstrip(), lim) + _split(t[k:], lim)


def E(pic, words, tryit, keep):
    return ("\n\n".join(_split(pic) + _split("Now the real words. " + words) + ["Try it. " + tryit, "If you remember one thing: " + keep]), "")


FEY = [
 E("Imagine building a huge LEGO city with a billion bricks. You would never place each brick by hand. You would write a plan: a district, then streets, then houses, then bricks, and a machine would follow the plan and build it.",
   "A VLSI chip has a billion tiny switches called transistors. Engineers describe the chip in a language like Verilog, check the description by running it on a computer, and then special tools turn it into gates and finally into a layout for a factory. The steps are called the design flow. The big blocks are split into smaller ones, which is called hierarchy.",
   "Put the eight steps of the design flow in order in the practice section.",
   "you describe a chip in a language, test the description, and tools build it."),
 E("Imagine a tap in the kitchen. The handle does not carry the water. It just opens or closes the way. A very tiny tap with an electric handle is a transistor.",
   "A MOS transistor is a switch controlled by the voltage on its gate. The n-type closes when the gate is high, the p-type closes when the gate is low. Inside, a high gate voltage pulls electrons into a thin channel between the source and the drain, and current can flow. A wider channel lets more current through, and so does a higher gate voltage.",
   "In the lab flip the gate and watch the lamp: first for the nMOS, then for the pMOS.",
   "a transistor is a switch: n-type on for 1, p-type on for 0."),
 E("Imagine a seesaw with a rope on each end. One rope pulls the board up to the roof, the other pulls it down to the floor. You are only ever pulling one rope at a time. Whichever you pull, the board goes all the way to one end.",
   "A CMOS inverter has a p-type switch to the supply and an n-type switch to ground, both controlled by the input. Exactly one is on, so the output is pulled all the way up or all the way down, and it is always the opposite of the input. NAND puts the n-type switches in a row and the p-type switches side by side. NOR does the opposite. The rule is duality: swap series and parallel between the two networks.",
   "In the lab choose series or parallel for each network until the truth table is perfect and the checker says no short and no floating output.",
   "the pull-up network is the pull-down network with series and parallel swapped."),
 E("Imagine a light switch in your room. You flip it on, you leave, and when you come back it is still on. The switch remembers. A normal wire cannot do that: when you stop pushing, it forgets.",
   "Memory in a circuit comes from feedback: a gate whose output goes back to its own input can hold a state. Two NOR gates cross-connected make an SR latch with set, reset and hold. A D latch follows its input while it is open and freezes when it closes. Two latches back to back make a flip-flop that copies its input only when the clock rises. A clock is a regular tick that tells every flip-flop when to update.",
   "In the lab write the stimulus for the latch and the flip-flop and see on the waveform when q changes and when it does not.",
   "a flip-flop copies d at the clock edge and holds it until the next edge."),
 E("Imagine you are writing a recipe card for a machine that builds a toy. The card says: take two blocks, join them in this way, and call the result a sum. The machine does not follow the card one line at a time. All the parts exist at once on the table.",
   "A Verilog design is a set of modules. A module is a box with ports, and inside it you place gates or other modules and connect them with wires. Every statement describes hardware that exists all the time, not a step in a program. A testbench is a module with no ports that wiggles the inputs and lets a simulator show the waveform.",
   "In the lab build an AND gate, then a half adder, then use two half adders to build a full adder, and watch every input combination pass.",
   "Verilog describes hardware that all exists at once: modules, ports, wires."),
 E("Imagine a row of light bulbs that can show a number. Each bulb is on or off, and a row of eight is a byte. You can look at the left half, the right half, or the whole row. You can even swap the halves.",
   "Verilog writes a many-bit signal as a vector, like [7:0]. You can pick one bit, a part of it, or glue pieces together with braces. A number is written with its size and base, like 4'b1010. Signals have four values: 0, 1, x for unknown, and z for not being driven. The assign statement says a wire always equals an expression. The operators work on whole vectors at once.",
   "In the lab swap the two halves of a byte with one line of concatenation.",
   "vectors, sized numbers and operators let one line describe a lot of gates."),
 E("Imagine adding numbers on paper. You add the right column, write the carry above the next column, and so on. Each column waits for the carry from the one before it. A row of little adders passing a carry is a ripple-carry adder.",
   "A full adder adds three bits and gives a sum and a carry. Chain them and you can add numbers of any size, but the last carry has to wait for all the others. To subtract, you add the two's complement: flip every bit and add one. A multiplexer chooses one of several inputs, a decoder lights one line for each number, and a priority encoder tells you the highest line that is on.",
   "In the lab build a 4-bit adder from full adders and then a subtractor from one adder.",
   "every block is a few lines of assign, and subtraction is addition with inverted bits plus one."),
 E("Imagine a robot that is told: if the door is open, walk through, otherwise knock. The robot makes a decision. In hardware the decision is not made over time. Every branch exists as wires, and a switch picks the right one.",
   "Inside an always block you can use if, case and loops. A block that lists every input it reads, written always @*, becomes combinational logic. A block that waits for a clock edge becomes flip-flops. If you forget to say what an output does in some case, the circuit has to remember the old value, and you get an unwanted latch. The sign = updates now, the sign <= reads everything first and updates together.",
   "In the lab swap two registers with = and see that both end up equal, then fix it with <=.",
   "use = in logic, <= in clocked blocks, and always give every output a value."),
 E("Imagine a row of children passing a ball. Every time the teacher claps, each child passes the ball to the next one at the same moment. Nobody passes early. The clap is the clock.",
   "A flip-flop in Verilog is an always block that waits for the rising edge of the clock and then assigns with <=. Add an if for reset and one for enable. A counter adds one at every clap, and wraps around from the largest number to zero. A shift register moves bits one place along per clock. A reset puts every register in a known starting state.",
   "In the lab build a counter, then a ring counter where a single one runs around a circle.",
   "a clocked always block with <= is a register, and every register needs a reset."),
 E("Imagine a relay race. The first runner starts at the clap, runs to the next runner, and has to arrive in time to hand over the stick before the next clap. If the runner is too slow, the baton is dropped.",
   "Gates take time. Between two flip-flops, the clock period must be long enough for the first flip-flop's output to appear, for the logic to settle, and for the data to be stable a little before the next edge. That little time before the edge is the setup time, and after it the hold time. The slowest path decides how fast the clock can run. Delays written with # are only for simulation; the real chip has its own.",
   "In the practice section fill in the clock budget: 0.3 plus 2.2 plus 0.1.",
   "the clock period must cover clock-to-q, logic and setup time of the slowest path."),
 E("Imagine you built a toy car and want to know if it works. You would put it on a test track, push the start button, and watch. A good test track has steep hills and sharp corners, because easy tests do not find the problems.",
   "A testbench is a Verilog module with no ports. It contains the design under test, makes a clock, applies inputs, and compares the outputs to the right answers, then prints pass or fail. Loops can try every input. Random numbers can try many. The most important rule is that a test must be able to fail: include equal values, zero and the biggest values, where the bugs hide.",
   "In the lab a comparator has a bug and the testbench says it is fine. Add the one test that exposes it.",
   "a test that cannot fail proves nothing, so test the boundaries."),
 E("Imagine a vending machine. It does not remember everything that ever happened. It only remembers a small amount: how much money is in it. That amount is its state. Each coin moves it to a new state, and when it reaches the price it gives out a drink.",
   "A finite state machine is always in one of a few states, remembered by flip-flops. Next-state logic decides where to go on each clock, and output logic decides what to show. In a Moore machine the output depends only on the state. In a Mealy machine it also depends on the input. You draw circles and arrows first, then write the three parts in Verilog.",
   "In the lab finish the machine that detects the bits 1, 0, 1 in a stream, even when two patterns overlap.",
   "draw the states and arrows first, then the Verilog follows."),
 E("Imagine a cookie cutter. With one cutter you can make a hundred cookies, all the same. Now imagine you could turn a knob on the cutter and make the cookies bigger or smaller.",
   "A parameter is that knob: the same module can be made 3 bits wide or 12 bits wide. A generate loop places many copies of the same hardware, like a long adder. A function is a calculation you can reuse. A memory is an array of registers: you give it an address and it gives back a word, and a RAM also lets you write.",
   "In the lab turn a fixed 8-bit register into one of any width with a single parameter.",
   "write a module once, then reuse it with parameters, generate, functions and arrays."),
 E("Imagine you have drawn a house on paper and you want to build it for real. You need a builder to turn the drawing into bricks, an inspector to check it will stand, and a place to build. That is what happens to a chip design.",
   "Synthesis turns RTL into gates and flip-flops. Then either an FPGA tool places them into programmable blocks and makes a bitstream, or an ASIC flow builds a full layout for a factory. Timing tools check every path against the clock. To prove you can do it all, you build a tiny 8-bit processor: a program counter, a memory with the program, a control block that decodes instructions, and an ALU that calculates.",
   "In the lab write your own program in the ROM so the CPU prints 4, 3, 2, 1.",
   "you can build a real processor from the same simple parts: registers, logic and a state machine."),
]
