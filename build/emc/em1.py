"""Emulator course, chapters 1-7. Original text."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

# The toy machine used across the course ("TOY8"): an 8-bit accumulator CPU.
# 0 HLT(1) 1 LDI n(2) 2 ADD n(2) 3 SUB n(2) 4 STA a(2) 5 LDA a(2) 6 JMP a(2) 7 JNZ a(2) 8 OUT(1)
# Cycles: HLT 1, LDI/ADD/SUB 2, STA/LDA 3, JMP 3, JNZ 3 taken or 2, OUT 2. Z flag is set when A is 0 after LDI/ADD/SUB/LDA.
CORE = """
LEN = [1, 2, 2, 2, 2, 2, 2, 2, 1]
NAMES = ['HLT', 'LDI', 'ADD', 'SUB', 'STA', 'LDA', 'JMP', 'JNZ', 'OUT']
CYC = [1, 2, 2, 2, 3, 3, 3, 3, 2]

def run_toy(program, max_steps):
    mem = list(program) + [0] * (256 - len(program))
    pc = 0
    a = 0
    z = False
    out = []
    cycles = 0
    halted = 0
    for _ in range(max_steps):
        op = mem[pc & 255]
        n = mem[(pc + 1) & 255]
        pc = (pc + LEN[op]) & 255 if op < 9 else pc
        cycles += CYC[op]
        if op == 0:
            halted = 1
            break
        elif op == 1:
            a = n
            z = a == 0
        elif op == 2:
            a = (a + n) & 255
            z = a == 0
        elif op == 3:
            a = (a - n) & 255
            z = a == 0
        elif op == 4:
            mem[n] = a
        elif op == 5:
            a = mem[n]
            z = a == 0
        elif op == 6:
            pc = n
        elif op == 7:
            if not z:
                pc = n
            else:
                cycles -= 1
        elif op == 8:
            out.append(a)
    return [out, cycles, a, halted]
"""
COUNTDOWN = [1, 3, 8, 3, 1, 7, 2, 0]

A = []

A.append(CH(
 "What an emulator is",
 ("Emulators", ["Emulator | imitates | A guest machine", "Host | runs | The emulator", "Guest | is | The imitated system", "Simulator | models | Behavior", "Compatibility layer | translates | System calls", "Interpreter | runs | One instruction at a time", "ROM | holds | Guest software"]),
 ["An emulator is a program, or a device, that lets one system, the host, behave like another, the guest. The goal is to run the guest's software unchanged.",
  "A simulator models behavior in the abstract, while an emulator reproduces the machine well enough to run its real binaries. In everyday use the two words blur.",
  "Emulators exist for consoles, computers, terminals, printers and chips, and are used for play, preservation, homebrew and development."],
 [("Emulator", "Software or hardware that imitates another system."), ("Host", "The real machine the emulator runs on."), ("Guest", "The machine being imitated."),
  ("Simulation", "A model of behavior, not necessarily running real binaries."), ("Compatibility layer", "A translator of one system's calls into another's, without imitating its hardware."), ("ROM image", "A file copy of a program or chip's contents.")],
 ["IBM engineers coined the term emulator in the 1960s for hardware-assisted imitation.", "Types: console and arcade emulators, terminal emulators, in-circuit emulators, floating-point emulators and instruction-set simulators.", "A compatibility layer is lighter than an emulator but needs the same kind of programs.",
  "Interpreters are simple; recompilers are faster.", "Accuracy needs depend on the guest: some software relies on exact timing.", "You can write a small emulator in an afternoon and learn a great deal from it."],
 [T("Imagine a toy robot that only understands a special language. An emulator is a translator in the middle. It reads the robot's instructions one at a time and does what the robot would do, using your own computer. The program inside does not know the difference."),
  T("The guest is the system you imitate and the host is the one you run on. A classic example is running a game console's games on a laptop. Other examples include printers that imitate a popular model, so existing software works, and terminals on a modern desktop that act like old text terminals."),
  T("People often ask about emulation and simulation. Historically, emulation meant imitation helped by hardware or microcode, and simulation meant pure software. Today, emulation usually means reproducing a machine that runs real binary code, and simulation often means a model, such as a network or weather simulation."),
  T("A compatibility layer is a cousin. Instead of imitating the hardware, it translates the foreign program's requests, such as open a file, into calls the host understands. That works well when the programs rarely touch hardware directly, and it is much faster than full emulation."),
  C("# the smallest emulator: a stack calculator\ndef calc(tokens):\n    stack = []\n    for t in tokens:\n        if t == '+':\n            b = stack.pop(); a = stack.pop(); stack.append(a + b)\n        elif t == '*':\n            b = stack.pop(); a = stack.pop(); stack.append(a * b)\n        else:\n            stack.append(t)\n    return stack[-1]\n\nprint(calc([2, 3, '+', 4, '*']))   # 20", "python"),
  T("Through this course we build up a tiny imaginary computer called TOY8 and write pieces of its emulator as labs. You will meet the same ideas that real emulators use: a fetch-decode-execute loop, a memory map, cycle timing, interrupts, video and sound, and testing.")],
 [("What is the guest?", ["The system being imitated", "The real machine", "The compiler", "The ROM file only"], 0, "The host runs the emulator."),
  ("What does a compatibility layer translate?", ["System calls", "Pixels", "Voltages", "Clock speed"], 0, "It does not imitate hardware."),
  ("What does a simulator usually model?", ["Behavior", "A copper wire", "A keyboard", "A screen"], 0, "Often abstract.")],
 [("What is a host?", "The machine running the emulator."), ("What is a ROM image?", "A file copy of a program or chip."), ("What is a compatibility layer?", "A call translator."), ("When was emulator coined?", "In the 1960s at IBM.")],
 [MATCH("Terms", "Match each term with its meaning.", [("Host", "The real machine"), ("Guest", "The imitated machine"), ("Compatibility layer", "Translates system calls"), ("ROM image", "A file copy of software")]),
  PL("RPN calculator", "Write calc(tokens): tokens are numbers and the strings '+', '-', '*'. Evaluate them on a stack (reverse Polish notation) and return the last value.", "calc(tokens)", """
def calc(tokens):
    stack = []
    for t in tokens:
        if t == '+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif t == '-':
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif t == '*':
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        else:
            stack.append(t)
    return stack[-1]
""", [[[2, 3, "+", 4, "*"]], [[5]], [[10, 4, "-", 3, "*"]], [[1, 2, 3, "*", "+"]]], "Push numbers, pop two for each operator.", approx=None),
  PL("Compatibility layer", "Write translate(calls, table): calls is a list of guest call names and table maps guest names to host names. Return the list of host names, using 'unsupported' for names not in the table.", "translate(calls, table)", """
def translate(calls, table):
    out = []
    for c in calls:
        out.append(table.get(c, 'unsupported'))
    return out
""", [[["open", "write", "fork"], {"open": "fopen", "write": "fwrite"}], [[], {}], [["x"], {"x": "y"}]], "A dictionary lookup with a default.", approx=None)]))

A.append(CH(
 "Anatomy of an emulator",
 ("Anatomy", ["CPU module | runs | Instructions", "Memory module | maps | Addresses", "Device module | imitates | A chip", "Bus | links | Parts", "Frontend | shows | Video and sound", "Scheduler | keeps | Time", "Module | can be | Reused"]),
 ["Split an emulator into modules that mirror the real machine: CPU, memory, video, sound, input and other chips. Each can be built and tested alone.",
  "A real bus connects the chips; emulators often skip it and give each device a direct link, or a central routing function.",
  "A frontend turns the emulated video and sound into a window and speakers on the host."],
 [("Module", "A separable part of the emulator, such as the CPU."), ("Bus", "The wires and rules that connect chips."), ("Address decoding", "Deciding which chip answers an address."),
  ("Open bus", "What a read returns when no chip answers."), ("Frontend", "The part that talks to the host's window, audio and input."), ("Core", "The emulation part, kept apart from the frontend.")],
 ["Keep the CPU core free of video and window code.", "A memory function routes each address to RAM, ROM or a device.", "Reads from nowhere return an open-bus value, often a leftover or 0xFF.", "Writing to ROM is usually ignored.", "Reusing a chip's module across machines saves work.", "Separating core from frontend lets one core run in many places."],
 [T("Look at a real computer and you see chips: a processor, some RAM, a ROM, a graphics chip and a sound chip. A good emulator has the same shape. Each chip becomes a module, with a clear job and a small interface. It is easier to find bugs when each piece is small."),
  T("In hardware, the CPU talks to the other chips over a bus. Every chip watches the address wires and answers only when the address belongs to it. The emulator copies this with a routing function. Given an address, it picks RAM, ROM or a device."),
  C("# a tiny address decoder\ndef route(addr):\n    if addr < 0x100:\n        return 'RAM'\n    if addr < 0x200:\n        return 'ROM'\n    return 'open bus'", "python"),
  T("What happens when the CPU reads an address where no chip lives? On real hardware, the wires keep whatever voltage was there last, or float. Software sometimes depends on this. Emulators return a fixed value, such as 0xFF, or the last value on the bus."),
  T("Keep the core of the emulator separate from the frontend, the part that opens windows and plays sound. The core only works on memory and numbers, so it can be tested without a screen and moved between platforms. The frontend asks the core to run one frame, then shows the picture and plays the sound.")],
 [("What is open bus?", ["A read where no chip answers", "A full bus", "A fast bus", "A bug"], 0, "Floating wires."),
  ("What is a frontend?", ["Window, audio and input code", "A CPU", "A ROM", "A compiler"], 0, "Kept apart from the core."),
  ("Why modules?", ["Easier to test and reuse", "Smaller screens", "Fewer pixels", "Free code"], 0, "Each is small.")],
 [("What does a bus connect?", "Chips."), ("What happens on ROM write?", "Usually ignored."), ("What is address decoding?", "Choosing the chip."), ("What is a core?", "The emulation logic.")],
 [MATCH("Modules", "Match each module with its job.", [("CPU", "Runs instructions"), ("Memory map", "Routes addresses"), ("Video chip", "Makes the picture"), ("Frontend", "Shows it on the host")]),
  PL("Address decoder", "Write route(addr, regions): regions is a list of [start, end, name] where end is exclusive. Return the name of the first region containing addr, or 'open bus'.", "route(addr, regions)", """
def route(addr, regions):
    for start, end, name in regions:
        if start <= addr < end:
            return name
    return 'open bus'
""", [[5, [[0, 256, "RAM"], [256, 512, "ROM"]]], [300, [[0, 256, "RAM"], [256, 512, "ROM"]]], [900, [[0, 256, "RAM"]]], [0, []]], "Check each range in order.", approx=None),
  PL("A tiny bus", "Write bus_run(rom, ops): RAM is 256 bytes at 0x00-0xFF (starting at 0), ROM is the list rom at 0x100 onward and cannot be written. Each op is ['w', addr, value] or ['r', addr]. Reads of unmapped addresses return 255. Return the list of values read.", "bus_run(rom, ops)", """
def bus_run(rom, ops):
    ram = [0] * 256
    out = []
    for op in ops:
        addr = op[1]
        if op[0] == 'w':
            if addr < 256:
                ram[addr] = op[2] & 255
        else:
            if addr < 256:
                out.append(ram[addr])
            elif addr - 256 < len(rom):
                out.append(rom[addr - 256])
            else:
                out.append(255)
    return out
""", [[[7, 8, 9], [["w", 5, 42], ["r", 5], ["r", 257], ["w", 257, 1], ["r", 257], ["r", 999]]], [[], [["r", 0]]]], "RAM, then ROM, then open bus.", approx=None)]))

A.append(CH(
 "Bits, numbers and flags",
 ("Numbers", ["Byte | has | 8 bits", "Wraparound | keeps | 8 bits", "Carry | marks | Overflow out", "Zero flag | marks | A zero result", "Two's complement | makes | Negatives", "Endianness | orders | Bytes", "Mask | keeps | Some bits"]),
 ["Real CPUs work with fixed-size numbers that wrap around. An emulator must reproduce that exactly, using masks.",
  "After most operations the CPU sets flags, such as carry, zero, negative and overflow, that later instructions test.",
  "Multi-byte numbers can be stored low byte first, called little-endian, or high byte first, big-endian. Combine bytes with shifts, never by peeking at memory layout."],
 [("Wraparound", "A result is cut to the register size, so 255 plus 1 gives 0."), ("Flag", "A single bit recording something about the last result."), ("Carry", "Set when an addition overflows the register."),
  ("Two's complement", "The common way to store negative numbers."), ("Endianness", "Whether the low byte or the high byte comes first."), ("Mask", "A bit pattern used with AND to keep chosen bits.")],
 ["Mask with & 0xFF to keep 8 bits and & 0xFFFF for 16.", "Carry: the full sum is above 255.", "Overflow (signed): two numbers of the same sign give a result of the other sign.", "To read a signed byte: if it is 128 or more, subtract 256.", "Little-endian word = low + (high << 8).", "Use shifts and masks, not type punning; modern compilers and fixed-width types make that safe and portable."],
 [T("A byte holds 256 different values, from 0 to 255. If you add 1 to 255 a real 8-bit register does not become 256. It wraps to 0 and sets the carry flag. Your emulator has to copy that. In Python or C, you mask the result with 255."),
  M(r"r=(a+b)\bmod 256\qquad C=[a+b>255]"),
  T("Negative numbers use two's complement. The byte 255 is minus one, 254 is minus two, and so on. The top bit tells you the sign. The same bits mean different numbers depending on whether the instruction treats them as signed or unsigned."),
  C("def add8(a, b):\n    full = a + b\n    r = full & 0xFF\n    carry = 1 if full > 255 else 0\n    zero = 1 if r == 0 else 0\n    neg = r >> 7\n    # signed overflow: same input signs, different result sign\n    ov = 1 if ((a ^ r) & (b ^ r) & 0x80) else 0\n    return [r, carry, zero, neg, ov]", "python"),
  T("Endianness is the order of the bytes in a larger number. The 6502, Z80 and x86 store the low byte first. The 68000 stores the high byte first. The old HOWTO showed tricks with unions and pointer casts to handle this. Today, the clean way is shifts: build the word with low plus high shifted left by eight, which works on any host."),
  T("Another modern habit is fixed-width types. Instead of relying on how big an int is, use uint8_t, uint16_t and so on in C, or u8 and u16 in Rust. Then your masks and wraparound do exactly what you expect, on every compiler.")],
 [("What is 255 + 1 in an 8-bit register?", ["0 with carry", "256", "-1", "1"], 0, "It wraps."),
  ("What is byte 255 as signed?", ["-1", "255", "0", "127"], 0, "Two's complement."),
  ("How do you build a little-endian word?", ["low + (high << 8)", "high + low", "low << 8", "low & high"], 0, "Use shifts.")],
 [("What is carry?", "Overflow out of the top bit."), ("What is a mask?", "A pattern used with AND."), ("What does little-endian mean?", "Low byte first."), ("What sets zero flag?", "A zero result.")],
 [FILL("Wraparound", "To keep 8 bits you use & {{255}}, and a sum over 255 sets the {{carry}} flag."),
  PL("Signed byte", "Write to_signed(v, bits): interpret v (an unsigned number) as a two's complement number of that many bits.", "to_signed(v, bits)", """
def to_signed(v, bits):
    v = v & ((1 << bits) - 1)
    if v >= (1 << (bits - 1)):
        return v - (1 << bits)
    return v
""", [[255, 8], [127, 8], [128, 8], [65535, 16], [32768, 16], [0, 8]], "Subtract 2 to the bits when the top bit is set.", approx=None),
  PL("8-bit add", "Write add8(a, b): return [result, carry, zero, negative, overflow] for an 8-bit addition (all as 0 or 1 except the result).", "add8(a, b)", """
def add8(a, b):
    full = a + b
    r = full & 0xFF
    carry = 1 if full > 255 else 0
    zero = 1 if r == 0 else 0
    neg = r >> 7
    ov = 1 if ((a ^ r) & (b ^ r) & 0x80) else 0
    return [r, carry, zero, neg, ov]
""", [[1, 2], [255, 1], [127, 1], [128, 128], [100, 27], [0, 0]], "Overflow depends on signs.", approx=None),
  PL("Read a word", "Write read_word(mem, addr, endian): the 16-bit value from two bytes at addr and addr + 1; endian is 'little' or 'big'.", "read_word(mem, addr, endian)", """
def read_word(mem, addr, endian):
    a = mem[addr]
    b = mem[addr + 1]
    if endian == 'little':
        return a | (b << 8)
    return (a << 8) | b
""", [[[0x34, 0x12], 0, "little"], [[0x12, 0x34], 0, "big"], [[0, 255, 1], 1, "little"], [[0, 255, 1], 1, "big"]], "Shift the high byte by 8.", approx=None),
  PL("Swap bytes", "Write swap16(w): swap the two bytes of a 16-bit number.", "swap16(w)", """
def swap16(w):
    return ((w & 0xFF) << 8) | ((w >> 8) & 0xFF)
""", [[0x1234], [0x00FF], [0xABCD], [0]], "Shift and mask each half.", approx=None)]))

A.append(CH(
 "The fetch-decode-execute loop",
 ("The loop", ["PC | points to | The next opcode", "Fetch | reads | An opcode", "Decode | picks | An action", "Execute | changes | State", "Cycle count | tracks | Time", "Halt | stops | The loop", "Register | holds | A value"]),
 ["The heart of every CPU emulator is a loop: fetch the opcode at the program counter, decode it, execute it, and add its cycles to a counter.",
  "The CPU's state is just a few variables: registers, flags and the program counter. Each instruction changes them.",
  "We use TOY8, a tiny accumulator CPU with nine opcodes, as the running example."],
 [("Program counter (PC)", "The register holding the address of the next instruction."), ("Fetch", "Reading the opcode (and operands) from memory."), ("Decode", "Working out which instruction it is."),
  ("Execute", "Doing what the instruction says."), ("Accumulator", "A register that most arithmetic uses."), ("Opcode", "The number that names an instruction.")],
 ["Loop: opcode = mem[pc]; advance pc; decode; execute; cycles += cost.", "Jumps simply overwrite pc.", "Conditional jumps read a flag.", "Different opcodes take different numbers of cycles.", "Stop on a halt instruction or after a step limit.", "TOY8 opcodes: 0 HLT, 1 LDI, 2 ADD, 3 SUB, 4 STA, 5 LDA, 6 JMP, 7 JNZ, 8 OUT."],
 [T("A processor is a very fast reader. It looks at the address in its program counter, reads the number there, and treats that number as a command. When the command is done, the counter moves to the next one. An emulator does exactly that with a loop."),
  T("TOY8 has an accumulator A, a program counter and a zero flag. Memory is 256 bytes. LDI loads a number, ADD and SUB change A, STA and LDA store and load from memory, JMP and JNZ jump, OUT sends A to an output list, and HLT stops. Most instructions have one operand byte."),
  C("def run(program, max_steps):\n    mem = list(program) + [0] * (256 - len(program))\n    pc, a, z, out = 0, 0, False, []\n    for _ in range(max_steps):\n        op = mem[pc]\n        n = mem[(pc + 1) & 255]\n        if op == 0:            # HLT\n            break\n        elif op == 1:          # LDI\n            a = n; z = a == 0; pc += 2\n        elif op == 3:          # SUB\n            a = (a - n) & 255; z = a == 0; pc += 2\n        elif op == 7:          # JNZ\n            pc = n if not z else pc + 2\n        elif op == 8:          # OUT\n            out.append(a); pc += 1\n    return out", "python"),
  T("Each instruction costs a number of cycles, the ticks of the CPU's clock. LDI takes two, a load from memory takes three, and a taken jump takes one more than a jump that is not taken. We add up cycles so we can keep other chips in step. You will see why in the chapter about timing."),
  T("Here is a program that counts down: load 3, then loop: output A, subtract 1, and jump back while A is not zero. Running it on the emulator gives 3, 2, 1. Try it in the first lab below.")],
 [("What does the PC hold?", ["The address of the next instruction", "The last result", "A flag", "The clock"], 0, "Program counter."),
  ("What does a jump do?", ["Overwrites the PC", "Adds to A", "Stops the CPU", "Clears memory"], 0, "New address."),
  ("Why count cycles?", ["To keep other chips in step", "To save memory", "To draw pixels", "To read ROM"], 0, "Timing.")],
 [("What is fetch?", "Reading the opcode."), ("What is decode?", "Working out the instruction."), ("What does HLT do?", "Stops the loop."), ("What does JNZ test?", "The zero flag.")],
 [MATCH("TOY8", "Match each opcode with its job.", [("LDI", "Load a number into A"), ("STA", "Store A in memory"), ("JNZ", "Jump if not zero"), ("OUT", "Send A to the output")]),
  PL("Run TOY8", "Write run_toy(program, max_steps): run the TOY8 machine (opcodes 0 HLT, 1 LDI n, 2 ADD n, 3 SUB n, 4 STA a, 5 LDA a, 6 JMP a, 7 JNZ a, 8 OUT; instruction lengths 1,2,2,2,2,2,2,2,1; cycles 1,2,2,2,3,3,3,3(taken) or 2(not taken),2; memory 256 bytes, program at 0, addresses wrap at 256; A wraps at 256; the zero flag z is set when A is 0 after LDI, ADD, SUB or LDA and starts false; HLT stops and still costs its cycle). Stop after max_steps instructions. Return [outputs, cycles, a, halted] with halted 1 or 0.",
     "run_toy(program, max_steps)", CORE, [[COUNTDOWN, 100], [[1, 5, 2, 250, 8, 0], 100], [[1, 1, 6, 0], 5], [[1, 7, 4, 100, 1, 0, 5, 100, 8, 0], 50]], "Loop, decode with if-elif, add cycles.", approx=None),
  PL("Fetch and decode", "Write decode(program, pc): return [name, operand, length] for the instruction at pc, using the names HLT LDI ADD SUB STA LDA JMP JNZ OUT; operand is None for one-byte instructions; unknown opcodes give ['???', None, 1].", "decode(program, pc)", """
def decode(program, pc):
    names = ['HLT', 'LDI', 'ADD', 'SUB', 'STA', 'LDA', 'JMP', 'JNZ', 'OUT']
    op = program[pc]
    if op > 8:
        return ['???', None, 1]
    if op == 0 or op == 8:
        return [names[op], None, 1]
    return [names[op], program[pc + 1], 2]
""", [[[1, 3, 8, 0], 0], [[1, 3, 8, 0], 2], [[1, 3, 8, 0], 3], [[99], 0], [[7, 2], 0]], "Look up the name; two-byte ones have an operand.", approx=None),
  PL("Count cycles", "Write cycles_for(program): run TOY8 until it halts (at most 1000 steps) and return only the number of cycles. Use the costs: HLT 1, LDI/ADD/SUB 2, STA/LDA 3, JMP 3, JNZ 3 taken or 2 not taken, OUT 2.", "cycles_for(program)", CORE + """
def cycles_for(program):
    return run_toy(program, 1000)[1]
""", [[COUNTDOWN], [[1, 0, 7, 9, 0]], [[1, 2, 8, 0]]], "Reuse the loop.", approx=None)]))

A.append(CH(
 "Decoding instructions",
 ("Decoding", ["Opcode | has | Bit fields", "Switch | picks | An action", "Table | maps | Opcode to handler", "Prefix | extends | The opcode space", "Addressing mode | says | Where data is", "Undocumented | opcodes | Do exist", "Decoder | can be | Generated"]),
 ["Opcodes are numbers with structure: some bits pick the operation, others pick registers or addressing modes. Decoding by bit fields is often shorter than listing every opcode.",
  "Common ways to dispatch are a big switch, a table of handlers, or code generated from a table. Modern compilers turn a dense switch into a fast jump table.",
  "Real CPUs have undocumented opcodes, and some software uses them."],
 [("Bit field", "A group of bits within an opcode that has one meaning."), ("Addressing mode", "How an instruction finds its operand: immediate, absolute, indexed and so on."), ("Dispatch", "Choosing which code to run for an opcode."),
  ("Jump table", "An array of addresses indexed by opcode."), ("Prefix byte", "An opcode that changes the meaning of the next one."), ("Undocumented opcode", "An instruction the maker never described but that works.")],
 ["Split opcodes with shifts and masks: (op >> 5) & 7.", "A switch on a dense range compiles to a jump table in modern compilers.", "A table of function pointers is clear, but each call has some cost.", "Generating decoder code from a table avoids typing mistakes.", "Write instruction handlers once and reuse them across addressing modes.", "Test undocumented opcodes against hardware-derived test suites."],
 [T("An opcode is a number, but it is not random. On the 6502, for example, many opcodes can be split into three fields, written aaabbbcc: a group in the low two bits, an addressing mode in the middle three and an operation in the top three. Learn the pattern and you can decode whole families at once."),
  C("def fields(op):\n    return [op >> 5, (op >> 2) & 7, op & 3]   # aaa, bbb, cc\n\nprint(fields(0xA9))   # [5, 2, 1]: LDA immediate on the 6502", "python"),
  T("The old HOWTO compared a switch with a table of function pointers and a table of labels. Today the choice is easier. Compilers make a dense switch into a jump table by themselves, and some compilers offer computed goto or guaranteed tail calls for the very hot path. Start with a plain switch and measure."),
  T("Addressing modes tell the instruction where its data is. Immediate means the operand is the next byte. Absolute means the next bytes name an address. Indexed adds a register. Write the address calculation as a small function for each mode, and let every instruction reuse it. That cuts the code size by a lot."),
  T("CHIP-8 is a friendly practice target. Its instructions are two bytes, and the first hex digit picks the family. For example, 6XNN means set register X to NN, and 7XNN means add NN to register X. Many people write a CHIP-8 emulator as their first project.")],
 [("What is an addressing mode?", ["How an instruction finds its operand", "A kind of flag", "A clock speed", "A bus"], 0, "Immediate, absolute and others."),
  ("What does a compiler do with a dense switch?", ["Often makes a jump table", "Deletes it", "Slows it down", "Splits the file"], 0, "Fast dispatch."),
  ("What is a prefix byte?", ["Changes the next opcode's meaning", "Ends a program", "Holds a flag", "Selects a bank"], 0, "Extends the opcode space.")],
 [("What is dispatch?", "Choosing the handler."), ("What is a bit field?", "A group of opcode bits."), ("What is CHIP-8?", "A friendly first target."), ("What is immediate mode?", "The operand follows the opcode.")],
 [MATCH("Modes", "Match each mode with its meaning.", [("Immediate", "The operand follows the opcode"), ("Absolute", "The operand is at a given address"), ("Indexed", "An address plus a register"), ("Implied", "No operand")]),
  PL("CHIP-8 decode", "Write chip8_decode(op): op is a 16-bit number. Return the text 'CLS' for 0x00E0, 'RET' for 0x00EE, 'JP nnn' for 1NNN (nnn as three lowercase hex digits), 'LD Vx,nn' for 6XNN, 'ADD Vx,nn' for 7XNN (x as one hex digit, nn as two hex digits), 'LD I,nnn' for ANNN, otherwise 'UNKNOWN'.", "chip8_decode(op)", """
def chip8_decode(op):
    h = '0123456789abcdef'
    x = (op >> 8) & 15
    nn = op & 255
    nnn = op & 4095
    def hx(v, n):
        s = ''
        for i in range(n):
            s = h[v & 15] + s
            v = v >> 4
        return s
    if op == 0x00E0:
        return 'CLS'
    if op == 0x00EE:
        return 'RET'
    t = op >> 12
    if t == 1:
        return 'JP ' + hx(nnn, 3)
    if t == 6:
        return 'LD V' + hx(x, 1) + ',' + hx(nn, 2)
    if t == 7:
        return 'ADD V' + hx(x, 1) + ',' + hx(nn, 2)
    if t == 0xA:
        return 'LD I,' + hx(nnn, 3)
    return 'UNKNOWN'
""", [[0x00E0], [0x1234], [0x6A05], [0x7B10], [0xA2F0], [0xFFFF], [0x00EE]], "Use the first nibble.", approx=None),
  PL("Opcode fields", "Write fields(op): split an 8-bit opcode into [aaa, bbb, cc] where aaa is the top 3 bits, bbb the middle 3 and cc the low 2 bits.", "fields(op)", """
def fields(op):
    return [(op >> 5) & 7, (op >> 2) & 7, op & 3]
""", [[0xA9], [0x00], [0xFF], [0x4C]], "Shifts and masks.", approx=None),
  PL("CHIP-8 execute", "Write chip8_exec(ops): V is a list of 16 registers, all 0. For each op: 6XNN sets V[x] = nn; 7XNN adds nn to V[x] (wrapping at 256, no flag); 8XY4 adds V[y] to V[x], wraps at 256 and sets V[15] to 1 if there was a carry otherwise 0. Ignore other ops. Return V.", "chip8_exec(ops)", """
def chip8_exec(ops):
    v = [0] * 16
    for op in ops:
        t = op >> 12
        x = (op >> 8) & 15
        y = (op >> 4) & 15
        nn = op & 255
        if t == 6:
            v[x] = nn
        elif t == 7:
            v[x] = (v[x] + nn) & 255
        elif t == 8 and (op & 15) == 4:
            s = v[x] + v[y]
            v[x] = s & 255
            v[15] = 1 if s > 255 else 0
    return v
""", [[[0x6005, 0x6103, 0x8014]], [[0x60FF, 0x6102, 0x8014]], [[0x6001, 0x70FF]], [[]]], "Handle the carry in VF.", approx=None)]))

A.append(CH(
 "Memory maps",
 ("Memory", ["Flat memory | is | A byte array", "Mirroring | repeats | A region", "Banking | swaps | Memory pages", "ROM | cannot be | Written", "MMIO | reaches | A device", "Side effect | follows | A read or write", "Paging | extends | The address space"]),
 ["The simplest memory is an array of bytes, but real machines add mirroring, bank switching, ROM and memory-mapped I/O.",
  "Wrap every access in read and write functions that apply those rules in one place.",
  "Some addresses are devices: reading or writing them does something, such as clearing a flag or advancing a counter."],
 [("Mirroring", "The same memory appearing at several addresses."), ("Bank switching", "Swapping which block of memory appears in a window."), ("Memory-mapped I/O", "Device registers placed in the address space."),
  ("Side effect", "An action caused by a memory access, beyond the data."), ("Address window", "A range of addresses showing a selected bank."), ("Paged lookup", "Using high address bits to pick a block.")],
 ["Mirroring: addr & (size - 1) when size is a power of two.", "Bank window: physical = bank x window_size + (addr - window_start).", "Reads happen far more often than writes, so keep the read path short.", "ROM writes may be ignored, or used to switch banks.", "A device read may change state, so never read a device just to look at it in a debugger.", "Fast emulators use a table of page pointers for the common case."],
 [T("A CPU thinks it sees one long row of bytes. Behind that row, the real machine may have many different chips. The memory map says which address goes where. Your emulator wraps all of this in two functions, one for reads and one for writes."),
  T("Mirroring happens because the address decoder ignores some wires. If a machine has 2 kilobytes of RAM but decodes 8 kilobytes of space, the same RAM appears four times. The fix is a mask: keep only the low bits of the address."),
  T("Bank switching gets more memory than the address space allows. A window of addresses shows one of several blocks, and writing a number to a special address changes which one. Many cartridge games used this to fit large programs on a small processor."),
  C("def read(addr, banks, bank):\n    # window 0x8000-0xBFFF shows one 16 KB bank\n    if 0x8000 <= addr < 0xC000:\n        return banks[bank][addr - 0x8000]\n    return 0xFF", "python"),
  T("Memory-mapped I/O means a device register lives at an address. Reading a status register might clear a flag. Writing a control register might start a sound. So your read function can have side effects. Remember that when you add a debugger, since peeking must not trigger them.")],
 [("What is mirroring?", ["The same memory at several addresses", "A copy of the CPU", "A fast bus", "A bug"], 0, "From partial decoding."),
  ("What does bank switching do?", ["Changes which block is visible", "Makes memory faster", "Erases ROM", "Slows the CPU"], 0, "A window of addresses."),
  ("What is MMIO?", ["Device registers in the address space", "A kind of ROM", "A cache", "A screen"], 0, "Reads can have side effects.")],
 [("What is a window?", "A range showing a bank."), ("How to mirror?", "Mask the address."), ("What is a side effect?", "An action from an access."), ("Which is hotter, reads or writes?", "Reads.")],
 [MATCH("Memory ideas", "Match each idea with its meaning.", [("Mirroring", "Same data at several addresses"), ("Banking", "Swap blocks in a window"), ("MMIO", "Registers of a device"), ("ROM", "Not writable")]),
  PL("Mirror", "Write mirror(addr, size): size is a power of two; return the address folded into the memory of that size.", "mirror(addr, size)", """
def mirror(addr, size):
    return addr & (size - 1)
""", [[0x2000, 0x800], [0x7FF, 0x800], [0x1234, 0x400], [5, 16]], "Mask with size minus one.", approx=None),
  PL("Banked read", "Write banked_read(banks, bank, addr, win_start, win_size): banks is a list of lists. If addr is inside the window (win_start to win_start + win_size, end exclusive) return the byte from the selected bank at the offset; otherwise return 255.", "banked_read(banks, bank, addr, win_start, win_size)", """
def banked_read(banks, bank, addr, win_start, win_size):
    if win_start <= addr < win_start + win_size:
        return banks[bank][addr - win_start]
    return 255
""", [[[[1, 2], [3, 4]], 1, 0x8001, 0x8000, 2], [[[1, 2], [3, 4]], 0, 0x8000, 0x8000, 2], [[[1, 2]], 0, 5, 0x8000, 2]], "Offset into the selected bank.", approx=None),
  PL("MMIO counter", "Write mmio(ops): memory has 16 bytes of RAM at addresses 0 to 15, all 0. Address 255 is a counter register: every read returns the current counter and then increments it (starting at 0); writes to 255 reset the counter to 0. Each op is ['r', addr] or ['w', addr, value]. Return the list of values read. Reads from any other address return 0.", "mmio(ops)", """
def mmio(ops):
    ram = [0] * 16
    counter = 0
    out = []
    for op in ops:
        a = op[1]
        if op[0] == 'r':
            if a == 255:
                out.append(counter)
                counter += 1
            elif a < 16:
                out.append(ram[a])
            else:
                out.append(0)
        else:
            if a == 255:
                counter = 0
            elif a < 16:
                ram[a] = op[2] & 255
    return out
""", [[[["r", 255], ["r", 255], ["r", 255], ["w", 255, 9], ["r", 255]]], [[["w", 3, 7], ["r", 3], ["r", 99]]], [[]]], "A read can change state.", approx=None),
  PL("Page table", "Write page_lookup(page_map, addr): page_map is a list of region names, one for each 256-byte page starting at address 0. Return the name for addr, or 'open bus' if addr is past the end.", "page_lookup(page_map, addr)", """
def page_lookup(page_map, addr):
    p = addr >> 8
    if p >= len(page_map):
        return 'open bus'
    return page_map[p]
""", [[["RAM", "RAM", "ROM"], 0x1FF], [["RAM", "RAM", "ROM"], 0x200], [["RAM"], 0x300], [[], 0]], "High bits pick the page.", approx=None)]))

A.append(CH(
 "Timing and cycles",
 ("Timing", ["Clock | ticks | Cycles", "Cycle count | tracks | Time", "Frame | is | A screen refresh", "Scanline | is | One screen line", "Period | sets | A task's rhythm", "Pacing | matches | Real time", "Drift | is | Lost cycles"]),
 ["Every chip in a machine runs from clocks, so an emulator needs a notion of time. The CPU's cycle count is the usual yardstick.",
  "A frame lasts clock rate divided by frame rate cycles, and a scanline is a fraction of that. Video, sound and timer events fire at those intervals.",
  "Add the period to the counter instead of resetting it, so leftover cycles are not lost."],
 [("Clock rate", "Cycles per second, such as 1.79 million for an old CPU."), ("Frame", "One complete picture, 50 or 60 times a second on many systems."), ("Scanline", "One horizontal line of the picture."),
  ("Cycle counter", "A number that counts down to the next event."), ("Pacing", "Slowing the emulator to match real time."), ("Drift", "Error that builds up when leftovers are dropped.")],
 ["Cycles per frame = clock / fps.", "Cycles per scanline = cycles per frame / lines.", "Use the greatest common divisor of all periods as the tick.", "When the counter reaches zero, handle events and add the period back.", "Run no more than a few frames at once to avoid a spiral of death.", "Use the host's monotonic clock to pace; never sleep in the middle of a frame."],
 [T("The CPU, the video chip and the sound chip all run at the same time in the real machine. In an emulator, they run one after another, so we cut time into slices. We run the CPU for a few cycles, then let the other chips catch up. Cycle counts are what keep them in step."),
  M(r"\text{cycles per frame}=\frac{f_{\text{clock}}}{\text{fps}}"),
  T("Suppose a CPU runs at 2.5 million cycles per second and the screen refreshes 50 times a second. Each frame is 50,000 cycles. If the screen has 256 lines, each line is about 195 cycles. Video events must happen at those points, because games often change things between lines."),
  C("counter = period\nfor cycles in instruction_costs:\n    counter -= cycles\n    while counter <= 0:\n        run_tick()\n        counter += period       # add, do not reset!", "python"),
  T("Notice the last line. If you set the counter back to the period, you lose the cycles by which you overshot. Add the period instead. After a million ticks, those lost cycles would add up to real drift. Timing errors like this cause audio crackle and missed raster effects."),
  T("To run at real speed, measure host time with a monotonic clock. Work out how many frames are due, run them, show the picture, and wait if you are early. Cap the number of frames you catch up in one go, or a slow moment will make the emulator run harder and fall further behind.")],
 [("What are cycles per frame?", ["Clock rate divided by fps", "Fps times two", "Lines times fps", "Clock plus fps"], 0, "Spread over the frame."),
  ("Why add the period instead of resetting?", ["Keeps leftover cycles", "Saves memory", "Looks nicer", "Is faster"], 0, "Avoids drift."),
  ("What is a spiral of death?", ["Catching up makes you slower and further behind", "A graphic effect", "A loop in ROM", "A CPU bug"], 0, "Cap the catch-up.")],
 [("What is a scanline?", "One screen line."), ("What is pacing?", "Matching real time."), ("What is drift?", "Accumulated lost cycles."), ("What is a good tick?", "The GCD of the periods.")],
 [MATCH("Timing", "Match each term with its meaning.", [("Frame", "One whole picture"), ("Scanline", "One line of it"), ("Tick", "A scheduled step"), ("Pacing", "Matching real time")]),
  PL("Cycles per frame", "Write frame_cycles(clock_hz, fps, lines): return [cycles_per_frame, cycles_per_scanline] with the first as a whole number (rounded) and the second rounded to 2 decimals.", "frame_cycles(clock_hz, fps, lines)", """
def frame_cycles(clock_hz, fps, lines):
    f = clock_hz / fps
    return [round(f), round(f / lines, 2)]
""", [[2500000, 50, 256], [1789773, 60, 262], [4194304, 60, 154]], "Divide.", approx=1e-2),
  PL("Event counter", "Write run_ticks(costs, period): a counter starts at period. For each instruction cost, subtract it; while the counter is 0 or less, count a tick and add period. Return [ticks, counter].", "run_ticks(costs, period)", """
def run_ticks(costs, period):
    counter = period
    ticks = 0
    for c in costs:
        counter -= c
        while counter <= 0:
            ticks += 1
            counter += period
    return [ticks, counter]
""", [[[3, 4, 5, 2, 6], 8], [[], 5], [[10], 4], [[1, 1, 1, 1], 2]], "Add the period back.", approx=None),
  PL("Common tick", "Write common_tick(periods): the greatest common divisor of all the task periods.", "common_tick(periods)", """
def common_tick(periods):
    g = 0
    for p in periods:
        a = g
        b = p
        while b:
            a, b = b, a % b
        g = a
    return g
""", [[[195, 39000, 50000]], [[12, 18]], [[7]], [[100, 250, 400]]], "Euclid's algorithm.", approx=None),
  PL("Frames due", "Write frames_due(elapsed_ms, fps, emulated, cap): how many frames should be run now: floor(elapsed_ms x fps / 1000) minus emulated, but never below 0 and never above cap.", "frames_due(elapsed_ms, fps, emulated, cap)", """
def frames_due(elapsed_ms, fps, emulated, cap):
    due = int(elapsed_ms * fps // 1000) - emulated
    return max(0, min(cap, due))
""", [[1000, 60, 0, 5], [1000, 60, 58, 5], [5000, 60, 0, 5], [10, 60, 3, 5]], "Clamp between 0 and the cap.", approx=None)]))
