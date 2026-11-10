#!/usr/bin/env python3
"""Build the Commodore 64 course. Usage: python3 make_c64_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "c64c"))
import cmk, cb1, cb2, cb3, labs_c64, labs_more, app_emu, app_basic, app_tools  # noqa: E402
from clib import T, C  # noqa: E402

BAS = {
 "1": ("Make the border go through colours 0 to 15. Use a FOR loop with a POKE to register 53280 inside it, then run the program.",
       '10 PRINT "BORDER TEST"\n20 REM CYCLE THE BORDER COLOUR HERE (REGISTER 53280)\n30 END\n',
       [{"t": "program ends normally", "ran": True}, {"t": "border colour changed", "border": True}, {"t": "uses a FOR loop", "uses": "\\bFOR\\b"}]),
 "2": ("Type a number when asked. Then add a line that prints DOUBLE and twice that number.",
       '10 INPUT "YOUR NUMBER";N\n20 PRINT "YOU TYPED";N\n30 END\n',
       [{"t": "uses INPUT", "uses": "INPUT"}, {"t": "prints DOUBLE", "screen": "DOUBLE"}]),
 "3": ("POKE a letter A into the top-left screen cell (address 1024, screen code 1) and give it a colour with colour RAM (address 55296).",
       '10 REM A AT THE TOP LEFT\n20 POKE 1024,1\n30 END\n',
       [{"t": "a character is in the top-left cell with its own colour", "cell0": True}]),
}
for k, (d, src, goals) in BAS.items():
    app_basic.make_basic(d, src, goals, out="basic_%s.html" % k)
for k, (desc, src, goals) in labs_c64.LABS.items():
    tabs = ["c", "asm"] if k == "c" else ["asm"]
    app_emu.make_app(desc, tabs, src, goals, studio=(k == "c"), out="emu_%s.html" % k)

for k, (d, src, goals) in labs_more.BASIC.items():
    app_basic.make_basic(d, src, goals, out="basic_%s.html" % k)
for k, (d, src, goals) in labs_more.C.items():
    app_emu.make_app(d, ["c", "asm"], {"c": src, "asm": "*=$C000\n      rts\n"}, goals, studio=True, out="emu_%s.html" % k)
for k, (d, src, goals) in labs_more.ASM.items():
    app_emu.make_app(d, ["asm"], {"asm": src}, goals, out="emu_%s.html" % k)

APPS = {}
for k in list(labs_c64.LABS) + list(labs_more.C) + list(labs_more.ASM):
    APPS["__EMU_%s__" % k] = "emu_%s.html" % k
for k in labs_more.BASIC:
    APPS["__BAS_%s__" % k] = "basic_%s.html" % k
for k in labs_c64.LABS:
    APPS["__EMU_%s__" % k] = "emu_%s.html" % k
for k in BAS:
    APPS["__BAS_%s__" % k] = "basic_%s.html" % k
for k in ("mem", "uport", "tape", "disk"):
    APPS["__T_%s__" % k] = "%s.html" % k

PRONOUNCE = {
    "C64": "C sixty four", "6510": "sixty five ten", "6502": "sixty five oh two", "VIC-II": "vick two", "VIC": "vick", "SID": "sid", "CIA": "see eye ay", "CIAs": "see eye ays",
    "PETSCII": "pet ski", "KERNAL": "kernel", "PRG": "P R G", "D64": "D sixty four", "TAP": "tap", "CRT": "C R T", "BAM": "bam", "DDR": "D D R", "RAM": "ram", "ROM": "rom",
    "PAL": "pal", "NTSC": "N T S C", "IRQ": "I R Q", "NMI": "N M I", "SEI": "sey", "CLI": "C L I", "RTI": "R T I", "RTS": "R T S", "JSR": "J S R", "LDA": "load A", "STA": "store A",
    "LDX": "load X", "DEX": "decrement X", "INX": "increment X", "BNE": "B N E", "BEQ": "B E Q", "CLC": "C L C", "ADC": "A D C", "TTL": "T T L", "RS-232": "R S two thirty two",
    "ADSR": "A D S R", "CHROUT": "chr out", "GETIN": "get in", "CHRIN": "chr in", "cc65": "C C sixty five", "ca65": "C A sixty five", "ld65": "L D sixty five", "Datassette": "data set",
    "Commodore": "commodore", "BASIC": "basic", "PEEK": "peek", "POKE": "poke", "printf": "print F", "conio": "con I O", "int": "int", "ACME": "acme", "VICE": "vice", "SYS": "sis", "GOSUB": "go sub",
    "GOTO": "go to", "INPUT": "input", "XOR": "ex or", "TTL": "T T L", "1541": "fifteen forty one", "8bitworkshop": "eight bit workshop", "Open ROMs": "open roms", "ASCII": "ask ee",
}

SANDBOX = cmk.terminal("C64 cheat sheet", "c64>", "A scripted lookup, not a real machine. Try: map, vic, sid, cia, basic, joy, disk, tape", [
    ("map", ["$0000 zero page, $0100 stack, $0400 screen, $0801 BASIC", "$A000 BASIC ROM, $D000 I/O, $E000 KERNAL"]),
    ("vic", ["Border $D020, background $D021, sprites enable $D015", "Sprite 0: X $D000, Y $D001, colour $D027, pointer $07F8"]),
    ("sid", ["Voice 1 $D400-$D406, volume $D418", "Control: $10 tri, $20 saw, $40 pulse, $80 noise, $01 gate"]),
    ("cia", ["CIA 1 $DC00 (keyboard, joystick), CIA 2 $DD00 (serial, user port)", "Timer latch = clock / rate - 1"]),
    ("basic", ["PEEK(a) reads, POKE a,v writes", "POKE 53280,2 makes the border red"]),
    ("joy", ["Port 2 at $DC00, bits 0-4 are up, down, left, right, fire", "A bit reads 0 when pressed"]),
    ("disk", ["35 tracks, 683 blocks; directory at track 18", "254 data bytes per sector"]),
    ("tape", ["Pulses: short, medium, long", "Byte: LM marker, 8 bits low first, odd parity"]),
])

EXAM = [
 ("What CPU does the C64 use?", ["6510", "Z80", "68000", "8086"], 0, "A 6502 variant."),
 ("How much RAM does a C64 have?", ["64 KB", "16 KB", "128 KB", "1 MB"], 0, "Hence the name."),
 ("Which chip draws sprites?", ["VIC-II", "SID", "CIA", "6510"], 0, "The video chip."),
 ("Which chip makes sound?", ["SID", "VIC-II", "CIA", "PLA"], 0, "Three voices."),
 ("How many cycles in a PAL frame?", ["19656", "17095", "1000", "63"], 0, "312 by 63."),
 ("What do the first two bytes of a PRG hold?", ["Load address", "File size", "Checksum", "Name"], 0, "Low byte first."),
 ("Where does BASIC load?", ["$0801", "$0400", "$C000", "$D000"], 0, "Above the screen."),
 ("What does SYS 2061 do?", ["Starts machine code", "Prints 2061", "Loads a file", "Clears memory"], 0, "Used by BASIC stubs."),
 ("How many letters of a BASIC variable name count?", ["Two", "One", "Eight", "All"], 0, "A quirk of BASIC V2."),
 ("What does POKE 53280,2 do?", ["Border red", "Background red", "Plays a note", "Prints"], 0, "$D020."),
 ("What is at $D000 by default?", ["I/O chips", "RAM only", "BASIC", "Sprites"], 0, "VIC, SID, CIAs."),
 ("Which address holds the CPU port?", ["$0001", "$0400", "$D020", "$FFFF"], 0, "Bits control banking."),
 ("Where is screen RAM?", ["$0400", "$D800", "$A000", "$E000"], 0, "1000 bytes."),
 ("Where is colour RAM?", ["$D800", "$0400", "$0801", "$DC00"], 0, "One nibble per cell."),
 ("What is the screen code of the letter A?", ["1", "65", "193", "0"], 0, "A=1."),
 ("What does LDA #5 do?", ["Loads 5 into A", "Loads the byte at 5", "Stores A", "Jumps"], 0, "Immediate mode."),
 ("What does STA do?", ["Stores A in memory", "Loads A", "Adds", "Stops"], 0, "Store accumulator."),
 ("Which flag does BNE test?", ["Zero", "Carry", "Negative", "Decimal"], 0, "Branch if not equal."),
 ("What should you do before a plain ADC?", ["CLC", "SEC", "SEI", "RTS"], 0, "Clear the carry."),
 ("What does JSR push?", ["Return address minus one", "The flags", "A, X and Y", "Nothing"], 0, "RTS adds one."),
 ("Where is CHROUT?", ["$FFD2", "$FFE4", "$D020", "$0314"], 0, "Prints A."),
 ("What is an int in cc65?", ["16 bits", "8 bits", "32 bits", "64 bits"], 0, "Two bytes."),
 ("Which cc65 tool links?", ["ld65", "cc65", "ca65", "peekpoke"], 0, "Makes the PRG."),
 ("How many bytes is a sprite?", ["63", "24", "21", "256"], 0, "3 by 21."),
 ("What does $D015 do?", ["Enables sprites", "Sets volume", "Border", "Timer"], 0, "One bit per sprite."),
 ("Pointer value for sprite data at $0340?", ["13", "52", "64", "0"], 0, "Divide by 64."),
 ("Where is the SID?", ["$D400", "$D000", "$DC00", "$DD00"], 0, "Voice 1 first."),
 ("What starts a SID note?", ["Setting the gate", "Setting volume", "Writing the border", "RTS"], 0, "Bit 0."),
 ("What does ADSR stand for?", ["Attack decay sustain release", "Add data sum register", "Audio data stream rate", "None"], 0, "The envelope."),
 ("Which address is the IRQ vector?", ["$0314", "$D020", "$0400", "$FFD2"], 0, "System IRQ jumps through it."),
 ("What must a raster handler do?", ["Acknowledge in $D019", "Reset the VIC", "Clear the stack", "Turn off the SID"], 0, "Or it repeats."),
 ("What does a joystick bit read when pressed?", ["0", "1", "128", "255"], 0, "Active low."),
 ("Which bit is fire?", ["Bit 4", "Bit 0", "Bit 1", "Bit 7"], 0, "After four directions."),
 ("Which register sets user port directions?", ["$DD03", "$DD01", "$DC00", "$D418"], 0, "DDR."),
 ("What logic level does the user port use?", ["5 V TTL", "12 V", "3.3 V", "24 V"], 0, "Not RS-232 levels."),
 ("What encodes bits on tape?", ["Pulse lengths", "Frequencies of 1 kHz", "Voltage levels", "Light"], 0, "Short, medium, long."),
 ("How is parity chosen on tape?", ["Odd number of ones", "Even number of ones", "Always 0", "Random"], 0, "Per byte."),
 ("How many tracks has a 1541 disk?", ["35", "40", "17", "80"], 0, "Numbered from 1."),
 ("Where is the directory on a 1541 disk?", ["Track 18", "Track 1", "Track 35", "Track 0"], 0, "From sector 1."),
 ("How many data bytes does a disk sector hold?", ["254", "256", "128", "512"], 0, "Two bytes link on."),
]

CFG = dict(id="commodore-64-programming", title="Commodore 64 Programming: BASIC, Assembly, C and the Hardware",
    subtitle="From the memory map to sprites, sound, tape, disk and the user port, with a real C64 emulator in every lab",
    description="A condensed, original course on programming the Commodore 64. It covers the chips and memory map, BASIC V2, 6510 assembly, C with cc65, VIC-II sprites, SID sound, interrupts, joysticks and keyboard, the user port, tape and disk, with labs that run on an emulated C64 inside the app, so no real hardware is needed. "
    "Credits: the labs reuse the WebAssembly C64 emulator core from floooh/chips (zlib licence) as packaged by 8bitworkshop (GPL-3.0), the Open ROMs generic ROM image, and the cc65 toolchain (zlib licence). The course text and the BASIC interpreter are original.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="c64c", apps=APPS)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "commodore-64-programming.course.json")
    chs = cb1.A + cb2.B
    L = lambda kind, key, title, intro, h: {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s_%s__" % (kind, key)}
    EXTRA = {
     8: ([T("Sprites work from every language, because they are only registers and memory. In BASIC you POKE the 63 data bytes, the pointer at 2040, the position at 53248 and 53249, the colour at 53287 and the enable bit at 53269. The BASIC lab draws the sprite on its own screen. In C the lines are almost the same with peekpoke.h, and the emulator lab shows the real VIC-II.")],
         [L("BAS", "4", "BASIC lab: a sprite with POKE", "Switch the sprite on and slide it with a FOR loop.", 930), L("EMU", "c_sprite", "C lab: two sprites", "Set up sprite 0 in C, then add sprite 1.", 1250)]),
     9: ([T("Sound is the same story. The SID has no idea which language wrote to it. In BASIC the note is a handful of POKEs to 54272 and up. In C it is the same list with peekpoke.h. Only the speed differs, which matters when you want to play a melody in time.")],
         [L("BAS", "5", "BASIC lab: a note with POKE", "Complete the program so the SID plays a note.", 930), L("EMU", "c_sid", "C lab: change the waveform", "Run the note, then switch to a pulse wave.", 1250)]),
     11: ([T("BASIC reads the joystick with PEEK(56320), and the BASIC lab has arrow and fire buttons under the screen. In C the line is j = PEEK(56320U). The bit tests are the same everywhere: a pressed direction reads as 0 in its bit.")],
          [L("BAS", "6", "BASIC lab: read the joystick", "Print a message for each direction and for fire.", 930), L("EMU", "c_joy", "C lab: read the joystick", "Mirror port 2 and print the direction.", 1250)]),
    }
    for i, (blocks, labs) in EXTRA.items():
        chs[i]["lesson"] = chs[i]["lesson"] + blocks
        chs[i]["practice"] = chs[i]["practice"] + labs
    chs = chs + cb3.D
    cmk.main(CFG, chs, [sys.argv[0], out])
