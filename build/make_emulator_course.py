#!/usr/bin/env python3
"""Build the emulator programming course. Usage: python3 make_emulator_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "emc"))
import cmk, em1, em2  # noqa: E402

PRONOUNCE = {
    "emulator": "em you lay ter", "emulators": "em you lay ters", "Emulator": "em you lay ter", "emulation": "em you lay shun", "Emulation": "em you lay shun", "emulate": "em you late", "emulated": "em you lay ted",
    "6502": "sixty five oh two", "Z80": "zee eighty", "8088": "eighty eighty eight", "68000": "sixty eight thousand", "x86": "x eighty six", "CHIP-8": "chip eight", "TOY8": "toy eight", "NES": "ness", "NESdev": "ness dev",
    "ROM": "rom", "ROMs": "roms", "RAM": "ram", "CPU": "C P U", "JIT": "jit", "IRQ": "I R Q", "NMI": "N M I", "DMA": "D M A", "MMIO": "M M I O", "RGB565": "R G B five six five", "RGB888": "R G B eight eight eight",
    "HLT": "halt", "LDI": "L D I", "ADD": "add", "SUB": "sub", "STA": "S T A", "LDA": "L D A", "JMP": "jump", "JNZ": "J N Z", "OUT": "out", "PC": "P C", "ISA": "I S A", "HOWTO": "how to", "FPGA": "F P G A",
    "endianness": "end ee an ness", "Endianness": "end ee an ness", "little-endian": "little endian", "big-endian": "big endian", "uint8_t": "u int eight", "uint16_t": "u int sixteen", "u8": "U eight", "u16": "U sixteen",
    "IBM": "I B M", "Fayzullin": "fay zoo lin", "Marat": "mah rat", "Commodore": "commodore", "Nintendo": "nin ten doe", "Dolphin": "dolphin", "libretro": "libre retro", "MiSTer": "mister", "perf": "perf",
    "Rust": "rust", "Zig": "zig", "Python": "pie thon", "ELI5": "E L I five", "JSON": "jason", "Fletcher-16": "fletcher sixteen", "LCG": "L C G", "lcg": "L C G", "hex": "hex", "HLE": "H L E", "pixel": "pixel",
    "scanline": "scan line", "scanlines": "scan lines", "vblank": "V blank", "hblank": "H blank", "framebuffer": "frame buffer", "Pan": "pan", "NESdev": "ness dev", "AAAA": "four hex digits", "nnn": "N N N", "VF": "V F", "Vx": "V X",
}

SANDBOX = cmk.terminal("Emulator cheat sheet", "emu>", "A scripted lookup, not a real emulator. Try: loop, flags, memory, timing, irq, jit, test, debug, endian", [
    ("loop", ["fetch opcode at PC, advance PC, decode, execute, add cycles", "when the cycle counter runs out: run events, add the period back"]),
    ("flags", ["carry = sum above 255; zero = result 0; negative = top bit", "overflow: same input signs, different result sign"]),
    ("memory", ["route each address to RAM, ROM or a device; mirror with a mask", "bank = window into a larger memory; MMIO reads can have side effects"]),
    ("timing", ["cycles per frame = clock / fps", "tick = greatest common divisor of the periods"]),
    ("irq", ["IRQ: level, can be masked; NMI: rising edge, cannot", "check lines between instructions"]),
    ("jit", ["translate a basic block once, cache it by address", "invalidate when the guest writes to code"]),
    ("test", ["load state, run one instruction, compare", "hardware-derived JSON suites exist for the 6502, Z80, 8088, 68000 and more"]),
    ("debug", ["breakpoints, single step, trace log, disassembler", "peek memory without side effects"]),
    ("endian", ["little: low byte first (6502, Z80, x86); big: high first (68000)", "word = low | (high << 8) works on any host"]),
])

EXAM = [
 ("What is the guest in emulation?", ["The system being imitated", "The real machine", "The compiler", "The window"], 0, "The host runs the emulator."),
 ("What does a compatibility layer translate?", ["System calls", "Pixels", "Voltages", "Clock rate"], 0, "It does not imitate hardware."),
 ("Who coined the term emulator?", ["IBM engineers in the 1960s", "Nintendo", "A game studio", "A university in 2000"], 0, "Hardware and microcode assisted."),
 ("What is open bus?", ["A read where no chip answers", "A fast bus", "A bug in Python", "A cache"], 0, "Floating wires."),
 ("Why separate the core from the frontend?", ["Testing and portability", "Smaller screens", "Fewer colors", "Faster ROMs"], 0, "The core needs no window."),
 ("What is 255 + 1 in an 8-bit register?", ["0 with carry", "256", "-1", "1"], 0, "Wraparound."),
 ("What is byte 255 as a signed number?", ["-1", "255", "0", "127"], 0, "Two's complement."),
 ("How do you build a little-endian word portably?", ["low | (high << 8)", "high + low", "A pointer cast", "A union only"], 0, "Shifts."),
 ("What does the program counter hold?", ["The next instruction's address", "The last result", "A flag", "The clock"], 0, "PC."),
 ("What does a jump instruction do?", ["Overwrites the PC", "Adds to A", "Halts", "Clears memory"], 0, "New address."),
 ("What does the loop add after each instruction?", ["Its cycle cost", "A pixel", "A sound sample", "Nothing"], 0, "Timing."),
 ("What is an addressing mode?", ["How an instruction finds its operand", "A kind of flag", "A clock", "A bus"], 0, "Immediate, absolute..."),
 ("What does a modern compiler do with a dense switch?", ["Often makes a jump table", "Rejects it", "Slows it down", "Splits it"], 0, "No hand tables needed."),
 ("What first digit of a CHIP-8 opcode means 'set register'?", ["6", "1", "A", "F"], 0, "6XNN."),
 ("What is mirroring?", ["The same memory at several addresses", "A CPU copy", "A fast bus", "A bug"], 0, "Partial decoding."),
 ("What does bank switching do?", ["Changes which block is visible", "Makes memory faster", "Erases ROM", "Slows the CPU"], 0, "A window."),
 ("What is special about MMIO reads?", ["They may change device state", "They are slower", "They are illegal", "They are free"], 0, "Side effects."),
 ("How many cycles per frame at 2.5 MHz and 50 fps?", ["50,000", "125,000", "5,000", "2,500"], 0, "Clock over fps."),
 ("Why add the period instead of resetting the counter?", ["To keep leftover cycles", "To save memory", "To hide bugs", "To go faster"], 0, "Avoid drift."),
 ("What is a spiral of death?", ["Catching up makes you fall further behind", "A graphics effect", "A ROM bug", "A key matrix"], 0, "Cap catch-up frames."),
 ("Which interrupt cannot be masked?", ["NMI", "IRQ", "Both", "Neither"], 0, "Non-maskable."),
 ("When does an NMI fire?", ["On a rising edge", "While high", "Never", "At reset only"], 0, "Edge-sensitive."),
 ("What does an event scheduler find?", ["The next event time", "The CPU model", "The ROM", "The frame rate"], 0, "Run until then."),
 ("What does a palette do?", ["Maps numbers to colors", "Draws sprites", "Plays sound", "Stores ROM"], 0, "Index to color."),
 ("Why render by scanline?", ["Games change settings mid-frame", "Less memory", "Darker picture", "A Python rule"], 0, "Raster effects."),
 ("How are sound samples mixed?", ["Add and clamp", "Multiply", "Pick the loudest", "Concatenate"], 0, "Sum within range."),
 ("What does a joypad register hold?", ["One bit per button", "A picture", "A score", "Sound"], 0, "Bits."),
 ("What does DMA do?", ["Copies memory without the CPU", "Draws sprites", "Reads keys", "Plays sound"], 0, "May steal cycles."),
 ("What is a basic block?", ["Straight code with one entry and one exit", "A byte", "A memory bank", "A frame"], 0, "Ends in a jump."),
 ("What invalidates a JIT cache entry?", ["The guest writing to translated code", "A new frame", "A key press", "Sound output"], 0, "Self-modifying code."),
 ("What should you do before optimizing?", ["Profile", "Write assembly", "Remove tests", "Add threads"], 0, "Measure first."),
 ("Which old advice has aged?", ["Hand-written label tables for dispatch", "Keep CPU and video modular", "Charge DMA cycles", "Test instructions"], 0, "Compilers do it."),
 ("What is cycle accurate?", ["Matches timing cycle by cycle", "Fast", "Small", "High level"], 0, "Some software needs it."),
 ("What is a single-step test?", ["State before and after one instruction", "A full game", "A backup", "A sound test"], 0, "Exact."),
 ("What does determinism allow?", ["Replay and save states", "More colors", "Smaller ROMs", "Faster clocks"], 0, "Same inputs same results."),
 ("What does a breakpoint do?", ["Stops at an address", "Speeds up code", "Deletes a ROM", "Plays sound"], 0, "Pauses."),
 ("Why must a debugger peek without side effects?", ["Reads can change device state", "It is faster", "It saves memory", "A Python rule"], 0, "MMIO."),
 ("What is digital preservation?", ["Keeping old software usable", "Compressing files", "Encrypting ROMs", "Selling games"], 0, "Emulation helps."),
 ("What is a sensible first emulator target?", ["CHIP-8", "A modern console", "A server farm", "A phone OS"], 0, "Small and friendly."),
]

CFG = dict(id="emulator-programming", title="Emulator Programming: From Fetch-Decode-Execute to JIT", subtitle="Build the ideas of a computer emulator step by step, with a tiny CPU, a memory map, timing, interrupts, video, sound and testing",
    description="Learn how to write a computer emulator. Starting from what an emulator is and how it differs from a simulator or a compatibility layer, you build a tiny 8-bit CPU and study the fetch-decode-execute loop, instruction decoding, bit tricks, flags and endianness, memory maps, mirroring, banking and memory-mapped devices, cycle timing, interrupts and event schedulers, video and sound, input and DMA, caches and just-in-time compilation, accuracy and hardware-derived test suites, and debuggers. The course updates the classic 1990s how-to advice for modern compilers, languages, tools and test suites. Each chapter has an ELI5 block, a quiz and Python labs that run on the built-in interpreter.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="emc", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "emulator-programming.course.json")
    cmk.main(CFG, em1.A + em2.B, [sys.argv[0], out])
