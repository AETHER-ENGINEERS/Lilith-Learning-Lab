"""Commodore 64 course, chapters 1-8. Original text. Facts checked against the Programmer's Reference Guide and Mapping the C64."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *


def EMU(key, title, intro, h=930):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__EMU_%s__" % key}


def BAS(key, title, intro, h=930):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__BAS_%s__" % key}


def TOOL(key, title, intro, h=640):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__T_%s__" % key}


A = []

A.append(CH(
 "Meet the Commodore 64",
 ("C64", ["6510 | is the | CPU", "VIC-II | draws | Screen and sprites", "SID | makes | Sound", "CIA | handles | Timers and I/O", "RAM | holds | 64 kilobytes", "ROM | holds | BASIC and KERNAL"]),
 ["The Commodore 64 is an 8-bit home computer from 1982. It was cheap, it had real graphics and sound chips, and it sold in the millions.",
  "Its heart is a 6510 processor with 64 KB of RAM. Three custom chips do the rest: VIC-II for video, SID for sound and two CIAs for timers and ports.",
  "This course teaches the machine, from BASIC down to chips, tape, disk and the user port, and every lab runs on a real emulator inside the app."],
 [("6510", "The C64's CPU: a 6502 with an extra built-in 6-bit I/O port."), ("VIC-II", "The video chip: text, bitmaps, sprites and raster interrupts."), ("SID", "The sound chip: three voices, filters and envelopes."), ("CIA", "Complex Interface Adapter: timers, keyboard, joysticks, user port."), ("KERNAL", "The operating-system routines in ROM, reached through fixed jump addresses."), ("PAL and NTSC", "The two TV standards: 50 Hz and 60 Hz machines.")],
 ["8-bit CPU at about 1 MHz, 16-bit addresses.", "64 KB RAM plus 20 KB ROM (BASIC, KERNAL, characters).", "40 by 25 text, 320 by 200 pixels, 16 colours, 8 sprites.", "SID: three voices, four waveforms.", "PAL machines run at 985248 Hz, NTSC at 1022727 Hz."],
 [T("The Commodore 64 launched in 1982 with 64 kilobytes of memory, colour graphics and a real synthesiser chip, for a low price. It became one of the best-selling single computer models ever. Thousands of games, demos and music tracks were written for it, and people still write new ones."),
  T("The processor is the 6510. It is a 6502 with a small input-output port at addresses 0 and 1. It runs a little under one megahertz. It has three working registers, A, X and Y, and a stack. Addresses are 16 bits wide, so it can reach 65536 bytes."),
  T("Three custom chips make the machine special. The VIC-II draws the picture, with 40 by 25 text, 320 by 200 bitmap graphics and eight sprites. The SID plays three voices. Two CIA chips run timers and talk to the keyboard, joysticks, serial bus and user port."),
  T("A PAL machine draws 312 lines of 63 clock cycles each, so a frame is 19656 cycles. An NTSC machine draws 263 lines of 65 cycles, which is 17095. Knowing cycles per frame tells you how much code fits between two screen refreshes."),
  M(r"\text{cycles per frame}=\text{lines}\times\text{cycles per line}")],
 [("How much RAM has a C64?", ["64 KB", "16 KB", "640 KB", "1 MB"], 0, "Hence the name."), ("Which chip makes sound?", ["SID", "VIC-II", "CIA", "6510"], 0, "A three-voice synthesiser."), ("How many cycles are in a PAL frame?", ["19656", "17095", "50", "1000"], 0, "312 lines of 63.")],
 [("Who draws the picture?", "The VIC-II."), ("Which CPU?", "The 6510, a 6502 variant."), ("PAL frame rate?", "About 50 per second."), ("What are the CIAs for?", "Timers, keyboard, joysticks, user port.")],
 [MATCH("Chips", "Match each chip with its job.", [("6510", "Runs the programs"), ("VIC-II", "Video and sprites"), ("SID", "Sound"), ("CIA", "Timers and ports")]),
  PL("Frame cycles", "Write frame_info(system): system is 'PAL' or 'NTSC'. PAL has 312 lines of 63 cycles at a clock of 985248 Hz; NTSC has 263 lines of 65 cycles at 1022727 Hz. Return [cycles per frame, frames per second rounded to 2 places].", "frame_info(system)", """
def frame_info(system):
    if system == 'PAL':
        cycles = 312 * 63
        clock = 985248
    else:
        cycles = 263 * 65
        clock = 1022727
    return [cycles, round(clock / cycles, 2)]
""", [["PAL"], ["NTSC"]], "Multiply lines by cycles per line, then divide the clock by that.", approx=0.01)]))

A.append(CH(
 "Tools, files and the Studio",
 ("Files", ["PRG | holds | A program", "PRG | starts with | Load address", "D64 | is | A disk image", "TAP | is | A tape image", "Emulator | runs | The C64 in software", "Cross-development | uses | A modern computer"]),
 ["You do not need real hardware. An emulator runs C64 programs on any device, and the labs in this course use one built into the app.",
  "Programs travel as files. A PRG file is two bytes of load address followed by the program. Disks and tapes have image formats too.",
  "This chapter ends with a first lab: assemble a tiny program and watch it change the screen colours."],
 [("PRG", "A program file: a 2-byte load address, then the bytes."), ("D64", "A disk image of a 1541 floppy: 174848 bytes."), ("TAP", "A tape image that stores pulse lengths."), ("Emulator", "Software that behaves like the hardware."), ("Cross-assembler", "An assembler that runs on one machine and produces code for another."), ("BASIC stub", "A tiny BASIC line, SYS 2061, that starts machine code.")],
 ["A PRG's first two bytes are the load address, low byte first.", "BASIC programs load at $0801.", "A SYS line at $0801 starts machine code.", "An emulator is the safest way to try things.", "A D64 holds 35 tracks of 256-byte sectors."],
 [T("A program on the Commodore 64 is usually a PRG file. The first two bytes give the address where it loads, low byte first, and the rest is the program. A BASIC program loads at hexadecimal 0801, so its file starts with 01 08."),
  T("Machine-code programs often begin with a one-line BASIC program: 10 SYS 2061. When you type RUN, BASIC reads the line and jumps to your code at address 2061, which is the first byte after the stub. This is the trick almost every commercial game used to start."),
  C("; the bytes of a BASIC stub: 10 SYS 2061\n0B 08       ; address of the next BASIC line\n0A 00       ; line number 10\n9E          ; token for SYS\n32 30 36 31 ; the characters 2 0 6 1\n00          ; end of line\n00 00       ; end of program"),
  T("Other files hold whole media. A D64 is an image of a 1541 floppy disk. A TAP file records the pulses from a cassette. Cartridges use CRT files. Programmers also use cross-development tools: you write code on a modern computer, build it, and test it in an emulator."),
  T("The labs in this course run a real C64 emulator. You write assembly, BASIC or C, press a button, and your program loads into the emulated machine. The first lab below assembles a few lines and colours the border and the background.")],
 [("What do the first two bytes of a PRG hold?", ["The load address", "The file size", "The name", "A checksum"], 0, "Low byte first."), ("What does SYS 2061 do?", ["Jumps to machine code at 2061", "Prints 2061", "Loads a disk", "Resets"], 0, "It runs code."), ("What is a D64?", ["A 1541 disk image", "A tape image", "A cartridge", "A sprite file"], 0, "35 tracks.")],
 [("Load address of BASIC?", "$0801."), ("What is a BASIC stub?", "A SYS line that starts machine code."), ("Which file is a disk image?", "D64."), ("Why use an emulator?", "No hardware needed.")],
 [MATCH("Files", "Match each file type with what it holds.", [("PRG", "One program"), ("D64", "A whole disk"), ("TAP", "A tape recording"), ("CRT", "A cartridge")]),
  PL("PRG bytes", "Write prg_bytes(addr, data): return the PRG file as a list of numbers: the load address low byte, high byte, then the data bytes.", "prg_bytes(addr, data)", """
def prg_bytes(addr, data):
    return [addr & 255, addr >> 8] + data
""", [[2049, [1, 2, 3]], [49152, []], [4096, [255]]], "Low byte first."),
  PL("BASIC stub", "Write basic_stub(sys_addr): the bytes of 'SYS <sys_addr>' as the only line, number 10, loaded at $0801. Layout: next-line pointer (2 bytes), line number 10 (2 bytes), token $9E, the address as ASCII digits, then 0, 0, 0. The pointer is $0801 + 2 + 2 + 1 + digits + 1.", "basic_stub(sys_addr)", """
def basic_stub(sys_addr):
    digits = [ord(c) for c in str(sys_addr)]
    nxt = 0x0801 + 2 + 2 + 1 + len(digits) + 1
    return [nxt & 255, nxt >> 8, 10, 0, 0x9E] + digits + [0, 0, 0]
""", [[2061], [49152], [4096]], "The pointer is where the next line would start."),
  EMU("hello", "First program on the C64", "Press Build and run. The border should turn red and the background green.")]))

A.append(CH(
 "BASIC V2",
 ("BASIC", ["Line number | orders | Statements", "PRINT | shows | Values", "FOR NEXT | repeats | A block", "IF THEN | chooses | A path", "POKE | writes | A memory byte", "PEEK | reads | A memory byte"]),
 ["Turn the C64 on and you are in BASIC V2. It is slow but friendly, and its PEEK and POKE commands reach every chip.",
  "Programs are numbered lines. The computer runs them in order, jumping with GOTO and GOSUB.",
  "The lab below is a faithful BASIC V2 interpreter. Type a program, press RUN, and the output appears on a 40 by 25 screen."],
 [("Line number", "Orders the lines of a program."), ("Variable", "A named value; names use two significant letters; $ marks text."), ("FOR NEXT", "A loop with a counter."), ("GOSUB", "Jumps to a subroutine and RETURN comes back."), ("POKE", "Stores a value in a memory address."), ("PEEK", "Reads the value at a memory address.")],
 ["Lines run in number order.", "Variable names use only the first two letters.", "Text variables end with $, whole numbers with %.", "POKE 53280,0 makes the border black.", "BASIC V2 has no sound or graphics commands: use POKE."],
 [T("BASIC V2 was written for the C64 by Microsoft. Each line starts with a number, and the computer runs lines in order. PRINT shows text and numbers, and a semicolon keeps the cursor on the same line. FOR and NEXT repeat a block, and IF and THEN choose between two paths."),
  C('10 FOR I=1 TO 5\n20 PRINT "LINE";I\n30 NEXT I\n40 POKE 53280,2\n50 END'),
  T("Variable names count only the first two characters, so COUNT and COSTS are the same variable. A dollar sign makes a text variable and a percent sign a whole number. Numbers print with a leading space for the sign, which surprises people the first time."),
  T("BASIC V2 has no graphics or sound commands. You get them by POKEing numbers into chip registers, for example POKE 53280,2 sets the border colour to red. That is why the memory map in the next chapter matters so much."),
  T("Try the interpreter below. It runs on the screen above it with C64 colours. It covers PRINT, INPUT, GET, FOR, IF, GOTO, GOSUB, ON, DIM, DATA, READ, PEEK, POKE and the standard functions. Fix the program, add lines, and finish the goals.")],
 [("How many letters of a variable name count?", ["Two", "One", "Six", "All"], 0, "COUNT equals COSTS."), ("What does a $ at the end of a name mean?", ["Text", "Money", "Integer", "Array"], 0, "A string."), ("What does POKE 53280,2 do?", ["Border red", "Prints 2", "Clears the screen", "Plays a note"], 0, "A chip register.")],
 [("Which line runs first?", "The lowest number."), ("What ends a FOR loop?", "NEXT."), ("How to get colour in BASIC?", "POKE to the VIC-II."), ("What is GOSUB?", "A jump you can return from.")],
 [MATCH("Commands", "Match each command with its job.", [("PRINT", "Shows a value"), ("GOTO", "Jumps to a line"), ("POKE", "Writes memory"), ("DIM", "Makes an array")]),
  PL("FOR loop values", "Write loop_values(a, b, step): the values that I takes in FOR I=a TO b STEP step (include b if reached). step is never 0. Return a list.", "loop_values(a, b, step)", """
def loop_values(a, b, step):
    out = []
    i = a
    while (step > 0 and i <= b) or (step < 0 and i >= b):
        out.append(i)
        i += step
    return out
""", [[1, 5, 1], [10, 0, -5], [1, 10, 4], [3, 1, 1]], "A positive step stops after passing b; a negative step stops before."),
  BAS("1", "BASIC lab: loops and the border", "Run the program, then change it so the border colour goes through all the colours. You need a FOR loop and a POKE inside it."),
  BAS("2", "BASIC lab: ask and answer", "This program asks a question with INPUT. Run it, answer, and then add a line that prints the double of the number you typed.")]))

A.append(CH(
 "Memory map and banking",
 ("Memory", ["RAM | fills | 64 KB", "ROM | hides | RAM", "Port $0001 | selects | The view", "BASIC ROM | lives at | $A000", "I/O | lives at | $D000", "KERNAL | lives at | $E000"]),
 ["The CPU can address only 64 KB, yet there is also 20 KB of ROM and a set of chips. They share addresses with RAM.",
  "Three bits in the processor port at address 1 choose what the CPU sees at $A000, $D000 and $E000.",
  "Reads see the ROM or chip, but writes always reach the RAM underneath."],
 [("Memory map", "The layout of what lives at each address."), ("Banking", "Switching what the CPU sees at an address."), ("LORAM, HIRAM, CHAREN", "The three bits of $0001 that control banking."), ("Zero page", "Addresses $00 to $FF: fast to access and used heavily by BASIC."), ("Colour RAM", "A separate 4-bit memory at $D800 for text colours.")],
 ["$0000-$00FF zero page; $0100-$01FF stack.", "$0400 screen; $0801 BASIC; $C000 free RAM.", "$A000 BASIC ROM; $D000 I/O or characters; $E000 KERNAL.", "Bit 0 LORAM, bit 1 HIRAM, bit 2 CHAREN.", "Writes to a ROM address go to the RAM below."],
 [T("Memory runs from address 0 to 65535, written $0000 to $FFFF. Zero page is $00 to $FF, and the stack is $0100 to $01FF. Screen memory starts at $0400, and BASIC programs at $0801. The block from $C000 to $CFFF is free RAM, handy for machine-code routines."),
  T("At the top of memory the picture gets crowded. BASIC ROM sits at $A000 to $BFFF, the chips sit at $D000 to $DFFF, and the KERNAL ROM sits at $E000 to $FFFF. Underneath each of them is RAM, so all 64 kilobytes of RAM remain usable."),
  T("Address $0001 holds the processor port. Its low three bits choose the view. LORAM and HIRAM together show BASIC ROM. HIRAM alone shows the KERNAL. If either of them is set, the $D000 block shows the chips when CHAREN is on and the character ROM when it is off. If neither is set, the block is plain RAM."),
  M(r"\text{visible at }\$D000=\begin{cases}\text{I/O}&(L\lor H)\land C\\\text{char ROM}&(L\lor H)\land\lnot C\\\text{RAM}&\text{otherwise}\end{cases}"),
  T("Use the lab to flip the three bits and see how the map changes. Notice that setting all three to zero leaves only RAM, which is how programs get the whole machine.")],
 [("Where does BASIC load?", ["$0801", "$0400", "$D000", "$C000"], 0, "Right after the screen and zero page."), ("What is at $D000 normally?", ["I/O chips", "RAM only", "BASIC", "KERNAL"], 0, "VIC, SID and CIAs."), ("What do writes to a ROM address do?", ["Reach the RAM underneath", "Nothing", "Crash", "Change ROM"], 0, "RAM sits below.")],
 [("Which address holds the CPU port?", "$0001."), ("Where is screen RAM?", "$0400."), ("Free RAM block?", "$C000-$CFFF."), ("What does CHAREN do?", "Chooses I/O or character ROM.")],
 [MATCH("Memory", "Match each address with what normally lives there.", [("$0400", "Screen RAM"), ("$A000", "BASIC ROM"), ("$D800", "Colour RAM"), ("$E000", "KERNAL ROM")]),
  PL("What does the CPU see?", "Write visible(port, addr): port is the value of $0001 (only the low 3 bits matter: bit0 LORAM, bit1 HIRAM, bit2 CHAREN). Return 'BASIC' for $A000-$BFFF when LORAM and HIRAM are set, 'IO' or 'CHAR' for $D000-$DFFF (see the lesson), 'KERNAL' for $E000-$FFFF when HIRAM is set, otherwise 'RAM'.", "visible(port, addr)", """
def visible(port, addr):
    lo = port & 1
    hi = (port >> 1) & 1
    ch = (port >> 2) & 1
    if 0xA000 <= addr < 0xC000 and lo and hi:
        return 'BASIC'
    if 0xD000 <= addr < 0xE000 and (lo or hi):
        return 'IO' if ch else 'CHAR'
    if addr >= 0xE000 and hi:
        return 'KERNAL'
    return 'RAM'
""", [[7, 0xA000], [7, 0xD400], [3, 0xD400], [1, 0xD000], [0, 0xD000], [6, 0xA000], [2, 0xE000], [0, 0xE000], [7, 0x4000]], "Check the three zones in turn."),
  TOOL("mem", "Banking lab", "Flip LORAM, HIRAM and CHAREN. Try at least four settings, including one with character ROM and one with only RAM.")]))

A.append(CH(
 "Screen, characters and colour",
 ("Screen", ["Screen RAM | holds | Character codes", "Colour RAM | holds | Colours", "Screen code | differs from | PETSCII", "Row and column | give | An address", "Border | is set by | $D020", "Background | is set by | $D021"]),
 ["The text screen is 40 columns by 25 rows. Each cell is one byte in screen RAM and one colour nibble in colour RAM.",
  "To put a letter on screen you store its screen code in memory. No drawing routine is needed.",
  "Screen codes are not the same as PETSCII, the numbers you use with PRINT and CHR$."],
 [("Screen RAM", "1000 bytes from $0400, one per character cell."), ("Colour RAM", "1000 nibbles from $D800, one per cell."), ("PETSCII", "The character set used by PRINT and CHR$."), ("Screen code", "The code stored in screen RAM to pick a glyph."), ("Border and background", "Colour registers $D020 and $D021.")],
 ["Cell address = $0400 + row*40 + column.", "Colour address = $D800 + row*40 + column.", "Screen code 1 is A; 32 is a space.", "Colours 0-15: black, white, red, cyan, purple, green, blue, yellow...", "Border $D020, background $D021."],
 [T("The screen is a grid of 40 columns and 25 rows, which is 1000 cells. Each cell has a byte in screen RAM starting at $0400 that says which character to draw, and a four-bit value in colour RAM starting at $D800 that says what colour to use."),
  M(r"\text{address}=\$0400+\text{row}\times40+\text{column}"),
  T("The codes in screen RAM are screen codes. In them, the letter A is 1, B is 2 and so on, a space is 32, and digits are 48 to 57. They differ from PETSCII, the codes you get from PRINT and CHR$, where A is 65. The system converts between them when it prints."),
  T("There are 16 colours, numbered 0 to 15: black, white, red, cyan, purple, green, blue, yellow, orange, brown, light red, dark grey, mid grey, light green, light blue and light grey. Register $D020 sets the border and $D021 the background."),
  T("Try both labs below. The BASIC lab writes characters with POKE. The assembly lab copies a message into screen and colour RAM. Change the row, the column and the colour to see them move.")],
 [("Where does screen RAM start?", ["$0400", "$D800", "$0801", "$C000"], 0, "1000 bytes."), ("What is screen code 1?", ["The letter A", "A space", "The digit 1", "Nothing"], 0, "A=1, B=2..."), ("Where is colour RAM?", ["$D800", "$0400", "$A000", "$0001"], 0, "One nibble per cell.")],
 [("Cells on the screen?", "1000."), ("Border register?", "$D020."), ("How to find a cell?", "$0400 + row*40 + column."), ("What is colour 1?", "White.")],
 [FILL("Screen facts", "Screen RAM starts at {{$0400}} and colour RAM at {{$D800}}. The border colour is held in {{$D020}}."),
  PL("Cell addresses", "Write cell(row, col): return [screen address, colour address] of the cell as numbers.", "cell(row, col)", """
def cell(row, col):
    off = row * 40 + col
    return [1024 + off, 55296 + off]
""", [[0, 0], [10, 10], [24, 39]], "Offset = row * 40 + col."),
  PL("PETSCII to screen code", "Write to_screen(p): convert a PETSCII code 32-255 to its screen code: 32-63 stay; 64-95 subtract 64; 96-127 subtract 32; 160-191 subtract 64; 192-254 subtract 128; 255 gives 94. Return -1 for anything below 32 or in 128-159.", "to_screen(p)", """
def to_screen(p):
    if p < 32 or 128 <= p < 160:
        return -1
    if p < 64:
        return p
    if p < 96:
        return p - 64
    if p < 128:
        return p - 32
    if p < 192:
        return p - 64
    if p < 255:
        return p - 128
    return 94
""", [[65], [32], [97], [193], [255], [10], [130]], "Handle each range in turn."),
  BAS("3", "BASIC lab: POKE the screen", "Use POKE to put a letter on the screen at the top-left corner, in a colour of your choice. You need two POKEs: one to screen RAM and one to colour RAM."),
  EMU("screen", "Assembly lab: text in screen RAM", "Run the program, then change the row, the column or the colour.")]))

A.append(CH(
 "6510 assembly I: registers and flags",
 ("Assembly", ["A X Y | are | Registers", "LDA | loads | A", "STA | stores | A", "Flags | record | Results", "Branch | tests | Flags", "Labels | name | Addresses"]),
 ["Machine code runs thousands of times faster than BASIC. You write it as assembly: short names for each instruction.",
  "The 6510 has three working registers, A, X and Y, a stack pointer, a program counter and a status register of flags.",
  "The lab assembles your code, loads it into the emulated C64 and runs it."],
 [("Register", "A tiny fast storage cell inside the CPU: A, X, Y."), ("Immediate", "An operand written with #, meaning a number itself."), ("Flag", "A status bit: Zero, Carry, Negative, Overflow and others."), ("Branch", "A conditional jump with a one-byte offset."), ("Label", "A name for an address.")],
 ["LDA #5 loads the number 5; LDA $D020 loads the byte at that address.", "STA stores A. INX and DEX change X by one.", "Flags: Z zero, C carry, N negative, V overflow.", "BNE branches if the zero flag is clear.", "A branch reaches -128 to +127 bytes."],
 [T("The 6510 works on three registers. A is the accumulator, where arithmetic happens. X and Y are index registers, handy as loop counters. Each register holds one byte, a number from 0 to 255. The program counter points at the next instruction."),
  T("Instructions have addressing modes. With a hash sign the operand is the number itself: LDA #5 loads 5. Without it, the operand is an address: LDA $D020 loads the byte stored there. STA stores A back to memory. So LDA #2 followed by STA $D020 makes the border red."),
  T("After most instructions the CPU sets flags. Z is set when the result is zero, N when bit 7 is set, C is the carry out of an addition. Branch instructions such as BNE and BEQ test these flags. ADC adds with the carry flag, so you clear the carry with CLC before a plain addition."),
  M(r"\text{branch target}=\text{address of branch}+2+\text{signed offset}"),
  C("*=$C000\n      ldx #10      ; count 10 down to 0\nloop: dex\n      bne loop     ; repeat while X is not zero\n      rts"),
  T("The lab below runs a loop that adds one to the border colour forever. Edit it: use dec for the opposite direction, or change the register.")],
 [("What does LDA #5 do?", ["Loads the number 5 into A", "Loads the byte at address 5", "Stores 5", "Adds 5"], 0, "Immediate mode."), ("Which flag does BNE test?", ["Zero", "Carry", "Overflow", "Negative"], 0, "Not equal means Z is clear."), ("What should you do before a plain ADC?", ["CLC", "SEC", "SEI", "CLD"], 0, "Clear the carry.")],
 [("Registers?", "A, X and Y."), ("What does STA do?", "Stores A in memory."), ("What does CLC do?", "Clears the carry flag."), ("Reach of a branch?", "-128 to +127 bytes.")],
 [MATCH("Instructions", "Match each instruction with its meaning.", [("LDA", "Load the accumulator"), ("STA", "Store the accumulator"), ("DEX", "Subtract one from X"), ("BNE", "Branch if not zero")]),
  PL("Add with flags", "Write add_flags(a, b, carry): add two bytes plus carry as ADC does. Return [result (0-255), C, Z, N, V] where V is set if the signed result overflows.", "add_flags(a, b, carry)", """
def add_flags(a, b, carry):
    r = a + b + carry
    res = r & 255
    c = 1 if r > 255 else 0
    z = 1 if res == 0 else 0
    n = 1 if res & 128 else 0
    v = 1 if (~(a ^ b) & (a ^ res) & 128) else 0
    return [res, c, z, n, v]
""", [[1, 2, 0], [255, 1, 0], [127, 1, 0], [128, 128, 0], [10, 20, 1]], "Overflow is when two same-sign operands give a different-sign result."),
  PL("Branch target", "Write branch_target(pc, offset): pc is the address of a branch instruction, offset is its operand byte (0-255, signed). Return the address it jumps to, as a number from 0 to 65535.", "branch_target(pc, offset)", """
def branch_target(pc, offset):
    if offset > 127:
        offset -= 256
    return (pc + 2 + offset) & 0xFFFF
""", [[49152, 3], [49152, 253], [49152, 254], [49152, 0]], "Add 2 for the instruction itself, then the signed offset."),
  EMU("loop", "Assembly lab: an endless loop", "Run the program. The border cycles through colours. Change inc to dec and run again.")]))

A.append(CH(
 "6510 assembly II: KERNAL, stack and patterns",
 ("Patterns", ["JSR | calls | A routine", "RTS | returns | To the caller", "Stack | stores | Return addresses", "KERNAL | provides | CHROUT and more", "Cycles | measure | Time", "Loop | uses | X and BNE"]),
 ["Real programs call subroutines. JSR jumps to one and RTS returns, with the return address kept on the stack.",
  "The KERNAL gives you ready-made routines at fixed addresses, such as CHROUT at $FFD2 to print a character.",
  "Every instruction takes a known number of clock cycles, so you can count how long a loop lasts."],
 [("JSR and RTS", "Call a subroutine and return from it."), ("Stack", "Last-in first-out memory at $0100 to $01FF."), ("CHROUT", "KERNAL routine at $FFD2 that prints the character in A."), ("GETIN", "KERNAL routine at $FFE4 that reads a key."), ("Cycle", "One tick of the CPU clock; instructions take 2 to 7.")],
 ["JSR pushes the return address minus one, high byte first.", "RTS pulls it and adds one.", "The stack grows downward from $01FF.", "CHROUT is at $FFD2, GETIN at $FFE4.", "DEX is 2 cycles; BNE is 3 if taken, 2 if not."],
 [T("A subroutine is a piece of code you call from many places. JSR pushes the address of the last byte of the JSR instruction onto the stack, high byte first, and jumps. RTS pulls that address, adds one, and continues after the call. The stack lives in page one, $0100 to $01FF, and grows downward."),
  T("The KERNAL is a set of routines in ROM at fixed addresses, so programs keep working whatever the ROM version. CHROUT at $FFD2 prints the character in A. GETIN at $FFE4 reads a key. SETLFS, SETNAM and LOAD handle files. Calling them saves a lot of code."),
  C("*=$C000\n      ldx #0\nloop: lda msg,x    ; get a character\n      beq done     ; zero marks the end\n      jsr $ffd2    ; print it\n      inx\n      bne loop\ndone: rts\nmsg:  .text \"HELLO\"\n      .byte 13,0"),
  T("Every instruction takes a fixed number of cycles. A countdown loop of DEX and BNE costs 2 cycles for DEX plus 3 for each taken branch, and 2 for the last branch that falls through. Multiply cycles by the clock period to get a delay: a million cycles is about one second."),
  M(r"t=\frac{\text{cycles}}{985248}\ \text{seconds (PAL)}"),
  T("The lab below prints a message through CHROUT. Change the text or add a second string.")],
 [("What does JSR push?", ["The return address minus one", "The registers", "The flags", "Nothing"], 0, "RTS adds one."), ("Where is CHROUT?", ["$FFD2", "$FFE4", "$0400", "$D020"], 0, "Prints the character in A."), ("Which direction does the stack grow?", ["Downward", "Upward", "Sideways", "It does not"], 0, "From $01FF.")],
 [("What ends a subroutine?", "RTS."), ("Page of the stack?", "Page one, $0100-$01FF."), ("Cycles for a taken BNE?", "Three."), ("What does GETIN do?", "Reads a key.")],
 [MATCH("KERNAL", "Match each routine with its job.", [("CHROUT $FFD2", "Print a character"), ("GETIN $FFE4", "Read a key"), ("CHRIN $FFCF", "Read input"), ("LOAD $FFD5", "Load a file")]),
  PL("Loop cycles", "Write loop_cycles(n): cycles of  LDX #n / loop: DEX / BNE loop  for n from 1 to 255 (LDX is 2, DEX is 2, a taken BNE is 3, a BNE that falls through is 2).", "loop_cycles(n)", """
def loop_cycles(n):
    return 2 + n * 2 + (n - 1) * 3 + 2
""", [[1], [10], [255]], "Add LDX, every DEX, every taken branch and the last branch."),
  PL("What JSR pushes", "Write jsr_push(addr): a JSR instruction is 3 bytes long and sits at address addr. Return the two bytes it pushes, in push order [high, low]: the address of the last byte of the instruction.", "jsr_push(addr)", """
def jsr_push(addr):
    r = addr + 2
    return [r >> 8, r & 255]
""", [[49152], [2049], [65000]], "The last byte is at addr + 2."),
  EMU("kernal", "Assembly lab: print with CHROUT", "Run it. Then change the text or print it twice.")]))

A.append(CH(
 "C on the C64 with cc65",
 ("C", ["cc65 | compiles | C to 6502", "ca65 | assembles | The result", "ld65 | links | A PRG", "POKE | is | A macro in C", "int | is | 16 bits", "printf | prints | Text"]),
 ["You can write C for the 6502. The cc65 toolchain compiles it to assembly, assembles it and links a PRG file that starts with a BASIC stub.",
  "The code is small and sometimes surprising: an int is 16 bits and floating point is not built in.",
  "The lab runs cc65 inside the app, so you can build C with no installation."],
 [("cc65", "A C compiler for 6502 machines."), ("ca65 and ld65", "The assembler and linker that finish the job."), ("peekpoke.h", "Header with PEEK and POKE macros."), ("conio", "Console routines for text, colour and keys."), ("Static allocation", "On this CPU, local variables are kept in fixed places for speed.")],
 ["cc65 turns C into 6502 assembly.", "int is 16 bits, char is 8 bits, long is 32.", "POKE(addr, value) writes memory.", "Programs start at $0801 with a SYS stub.", "Avoid deep recursion and big stack arrays."],
 [T("The cc65 toolchain has three programs. The compiler turns C into assembly, the assembler turns that into an object file, and the linker joins it with the C64 library into one PRG. The PRG starts with the BASIC stub from chapter two, so you start it with RUN."),
  C('#include <stdio.h>\n#include <peekpoke.h>\n\nint main(void) {\n    printf("HELLO FROM C\\n");\n    POKE(53280U, 5);   /* green border */\n    return 0;\n}'),
  T("C on an 8-bit machine has quirks. An int is 16 bits, so it holds -32768 to 32767. A char is one byte. There is no floating point unless you add a library, and code is bigger and slower than hand-written assembly. You can mix the two: inline assembly lets you drop into 6510 code where speed matters."),
  T("The header peekpoke.h gives you PEEK and POKE as macros, so you reach the chips just as in BASIC. Other headers handle text, colour and joysticks. Using unsigned constants such as 53280U avoids sign trouble with 16-bit ints."),
  T("Run the lab below. It starts the whole toolchain in the page the first time, which takes a moment, then compiles and runs your program on the emulated machine.")],
 [("How many bits is an int in cc65?", ["16", "8", "32", "64"], 0, "A 6502 is 8 bits, but int is wider."), ("What does cc65 produce first?", ["Assembly", "A PRG", "A disk", "A sprite"], 0, "Then ca65 and ld65 finish."), ("What does POKE(addr, v) do in C?", ["Writes memory", "Prints", "Reads memory", "Waits"], 0, "A macro.")],
 [("Which tool links?", "ld65."), ("Header for POKE?", "peekpoke.h."), ("Size of char?", "One byte."), ("How is a C PRG started?", "RUN, through a SYS stub.")],
 [MATCH("Toolchain", "Match each program with its job.", [("cc65", "C to assembly"), ("ca65", "Assembly to object"), ("ld65", "Link to a PRG"), ("peekpoke.h", "PEEK and POKE macros")]),
  PL("int range", "Write int_range(bits, signed): the smallest and largest value of an integer with the given number of bits. Return [min, max]; signed is 1 for two's complement, 0 for unsigned.", "int_range(bits, signed)", """
def int_range(bits, signed):
    if signed:
        return [-(2 ** (bits - 1)), 2 ** (bits - 1) - 1]
    return [0, 2 ** bits - 1]
""", [[16, 1], [16, 0], [8, 0], [8, 1]], "Two's complement halves the range."),
  EMU("c", "C lab: build and run", "Build and run the C program with cc65.", 1250)]))
