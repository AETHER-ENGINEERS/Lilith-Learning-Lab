"""Commodore 64 course, chapters 9-16."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clib import *
from cb1 import EMU, BAS, TOOL

B = []

B.append(CH(
 "VIC-II graphics and sprites",
 ("VIC-II", ["Sprite | is | 24 by 21 pixels", "Pointer $07F8 | picks | Sprite data", "$D015 | enables | Sprites", "$D000 | sets | X and Y", "VIC bank | is | 16 KB window", "Raster | counts | Screen lines"]),
 ["The VIC-II reads memory by itself and builds the picture. Programs change it by writing to registers at $D000.",
  "A sprite is a movable image, 24 pixels wide and 21 high, stored as 63 bytes. There are eight of them.",
  "The chip sees only 16 KB at a time, chosen by two bits on CIA 2."],
 [("Sprite", "A hardware-moved image of 24 by 21 pixels."), ("Sprite pointer", "A byte at $07F8 to $07FF: data address divided by 64."), ("Register", "A chip memory location that controls something: $D000 to $D02E for VIC-II."), ("VIC bank", "The 16 KB part of memory the VIC-II can see, picked by $DD00."), ("Multicolour", "A mode where pixels are twice as wide but have more colours.")],
 ["Sprite data: 3 bytes per row, 21 rows = 63 bytes.", "Pointer value = data address / 64 (at $07F8-$07FF).", "$D015 turns sprites on, one bit each.", "$D000/$D001 are sprite 0 X and Y; $D027 its colour.", "VIC bank = 3 minus the low two bits of $DD00."],
 [T("The VIC-II is the C64's video chip. Its registers start at $D000 and span 47 bytes. It reads the screen, the characters and the sprites straight from memory, so your program only changes the numbers it reads. The chip can display eight sprites over the picture at once."),
  T("A sprite is 24 pixels wide and 21 high. Each row is three bytes, and each bit is a pixel, so the shape takes 63 bytes. You store it in RAM, in a 64-byte block. A pointer byte at $07F8 for sprite 0 says which block: the block number is the data address divided by 64, so data at $0340 gives pointer 13."),
  M(r"\text{pointer}=\frac{\text{data address}}{64}"),
  T("Position comes from registers $D000 and $D001 for sprite 0, then $D002 and $D003 for sprite 1, and so on. Bit 0 of $D015 enables sprite 0, and $D027 holds its colour. Bits in $D010 supply the ninth bit of X for the right of the screen. Other registers expand sprites and detect collisions."),
  T("The VIC-II sees only 16 KB at a time. Two bits at $DD00 choose which quarter: the bank number is 3 minus those two bits, so the default, bits both on, is bank 0 at $0000. Moving the bank is how programs fit extra graphics beside the ROMs."),
  T("The lab below draws a box sprite. Change the pattern, the colour or the position. Then try turning on a second sprite.")],
 [("How many bytes is one sprite?", ["63", "24", "21", "256"], 0, "3 bytes by 21 rows."), ("What goes at $07F8?", ["Sprite 0 pointer", "Screen text", "Border colour", "SID volume"], 0, "Data address / 64."), ("What does $D015 do?", ["Enables sprites", "Moves sprites", "Colours sprites", "Stops sound"], 0, "One bit per sprite.")],
 [("Sprite size?", "24 by 21 pixels."), ("How many sprites?", "Eight."), ("Pointer for data at $0340?", "13."), ("VIC bank for $DD00 low bits = 3?", "Bank 0.")],
 [MATCH("Registers", "Match each register with its job.", [("$D015", "Sprite enable"), ("$D020", "Border colour"), ("$D000", "Sprite 0 X position"), ("$07F8", "Sprite 0 pointer")]),
  PL("Sprite bytes", "Write sprite_bytes(rows): rows is a list of 21 strings, each 24 characters long with '#' for a set pixel and '.' for a clear one. Return the 63 bytes (3 per row, leftmost pixel is the top bit).", "sprite_bytes(rows)", """
def sprite_bytes(rows):
    out = []
    for r in rows:
        for k in range(3):
            v = 0
            for b in range(8):
                v = v * 2
                if r[k * 8 + b] == '#':
                    v += 1
            out.append(v)
    return out
""", [[["#" * 24] + ["." * 24] * 20], [["#.#.#.#." * 3] * 21], [["........" + "########" + "........"] * 21]], "Read eight characters at a time and build a byte."),
  PL("VIC bank", "Write vic_bank(dd00): the VIC-II bank number is 3 minus the low two bits of $DD00. Return [bank number, start address].", "vic_bank(dd00)", """
def vic_bank(dd00):
    bank = 3 - (dd00 & 3)
    return [bank, bank * 16384]
""", [[3], [0], [2], [151]], "Each bank is 16384 bytes."),
  EMU("sprite", "Assembly lab: a sprite", "Run the program. Then change the position, the colour or the shape.")]))

B.append(CH(
 "SID sound",
 ("SID", ["Voice | has | A waveform", "Frequency | sets | The pitch", "ADSR | shapes | Volume over time", "Gate | starts | The envelope", "$D418 | sets | Master volume", "Filter | cuts | Frequencies"]),
 ["The SID chip has three voices. Each has a waveform, a frequency and an envelope, and a master volume controls the whole chip.",
  "Registers start at $D400, seven per voice. A note starts when you set the gate bit and ends when you clear it.",
  "Pitch is a 16-bit number, and it depends on the clock, so PAL and NTSC machines differ slightly."],
 [("Voice", "One of three sound generators."), ("Waveform", "Triangle, sawtooth, pulse or noise."), ("ADSR", "Attack, decay, sustain, release: the volume shape of a note."), ("Gate", "Bit 0 of the control register: on starts a note, off releases it."), ("Filter", "A programmable high-pass, low-pass or band-pass filter.")],
 ["Voice 1 is $D400-$D406; add 7 for voice 2 and 14 for voice 3.", "Control bits: $10 triangle, $20 saw, $40 pulse, $80 noise, plus $01 gate.", "$D418 sets volume 0-15.", "freq register = Hz x 2^24 / clock.", "Clock: 985248 Hz (PAL), 1022727 Hz (NTSC)."],
 [T("The SID chip, the 6581, was designed to be a small synthesiser. It has three voices. Each voice has a 16-bit frequency, a pulse width, a control byte for the waveform, and two envelope bytes. The chip is mapped from $D400, and voice 1 uses seven bytes, voice 2 the next seven, and voice 3 the last."),
  T("The control byte picks the waveform with bit 4 triangle, bit 5 sawtooth, bit 6 pulse and bit 7 noise. Bit 0 is the gate. Setting it starts the attack phase of the envelope, and clearing it starts the release. Register $D418 holds the master volume in its low four bits."),
  M(r"F_n=\frac{F_{\text{out}}\times 2^{24}}{F_{\text{clock}}}"),
  T("The envelope has four steps. Attack is how fast the sound rises, decay how fast it falls to the sustain level, sustain is the level held while the gate stays on, and release is how fast it dies after the gate goes off. Attack and decay share one register byte, sustain and release the next."),
  T("The frequency number is Hz multiplied by 2 to the 24th and divided by the clock. For 440 Hz on a PAL machine that is 7493, or $1D45, so the high byte is $1D and the low byte $45. Click the picture in the lab, then run the program to hear a triangle note.")],
 [("How many voices does the SID have?", ["Three", "Two", "Eight", "One"], 0, "Each with its own envelope."), ("What starts a note?", ["Setting the gate bit", "Writing the volume", "Setting the border", "Resetting"], 0, "Bit 0 of the control byte."), ("Where is master volume?", ["$D418", "$D400", "$D020", "$DC00"], 0, "Low four bits.")],
 [("Waveforms?", "Triangle, saw, pulse, noise."), ("What is ADSR?", "Attack, decay, sustain, release."), ("Voice 2 starts at?", "$D407."), ("PAL clock?", "985248 Hz.")],
 [MATCH("Waveforms", "Match each control bit with its waveform.", [("$10", "Triangle"), ("$20", "Sawtooth"), ("$40", "Pulse"), ("$80", "Noise")]),
  PL("SID frequency", "Write sid_freq(hz, clock): the 16-bit register value is round(hz * 2^24 / clock). Return [low byte, high byte].", "sid_freq(hz, clock)", """
def sid_freq(hz, clock):
    f = int(round(hz * 16777216.0 / clock))
    return [f & 255, f >> 8]
""", [[440, 985248], [261.63, 985248], [440, 1022727]], "Split the 16-bit number into two bytes."),
  PL("ADSR bytes", "Write adsr(a, d, s, r): each is 0-15. Return the two register bytes [attack*16+decay, sustain*16+release].", "adsr(a, d, s, r)", """
def adsr(a, d, s, r):
    return [a * 16 + d, s * 16 + r]
""", [[0, 9, 15, 0], [2, 4, 8, 6], [15, 15, 15, 15]], "Attack is the high nibble."),
  EMU("sid", "Assembly lab: play a note", "Click the screen to allow sound, press Build and run, and listen. Then change the pitch or the waveform.")]))

B.append(CH(
 "Interrupts and the CIA chips",
 ("Interrupts", ["IRQ | interrupts | The CPU", "Vector $0314 | points to | The handler", "Raster IRQ | fires on | A screen line", "CIA timer | counts | Clock cycles", "Handler | must | Acknowledge", "RTI | returns from | An interrupt"]),
 ["An interrupt stops the program, runs a handler, and then carries on. The C64 uses them for the keyboard, the clock and your own timing.",
  "The VIC-II can raise an interrupt at any screen line, so you can change colours or sprites mid-frame.",
  "The CIA chips have timers and handle ports, the keyboard and joysticks."],
 [("Interrupt", "A request that makes the CPU run a handler, then resume."), ("IRQ vector", "The address at $0314 that the system calls on each IRQ."), ("Raster interrupt", "A VIC-II interrupt at a chosen scan line."), ("CIA", "The 6526 timer and I/O chip; there are two."), ("Acknowledge", "Clear the chip's flag so the interrupt does not repeat.")],
 ["The system IRQ runs 60 or 50 times a second from a CIA timer.", "Change $0314/$0315 to hook the IRQ.", "Raster line goes in $D012 and bit 7 of $D011.", "Enable the raster IRQ with $D01A; acknowledge with $D019.", "CIA 1 is at $DC00, CIA 2 at $DD00."],
 [T("Normally a timer in CIA 1 interrupts the processor about sixty times a second, and the system uses that to scan the keyboard and update the clock. Each interrupt calls the routine whose address is stored at $0314 and $0315. If you change that address, your code runs instead, once per tick."),
  T("The VIC-II can also interrupt at a raster line. You choose the line by writing $D012, and enable the interrupt with $D01A. When it fires, your handler changes something, and then must acknowledge by writing to $D019. Changing the border colour at two lines is how rasters bars are made."),
  T("To start a handler safely, disable interrupts with SEI, set the vector, set up the chip, and enable interrupts again with CLI. The handler ends with RTI. Because the system pushed A, X and Y before calling the vector, a handler that does not call the system routine pulls them back itself, as the lab does."),
  T("Each CIA has two timers and two 8-bit ports. Timers count system clock cycles from a latch value you load, and they can interrupt when they reach zero. Timer values are one less than the number of cycles, so a latch of 19655 gives one PAL frame."),
  M(r"\text{latch}=\frac{\text{clock}}{\text{rate}}-1"),
  T("Run the lab. The handler adds one to the border register and counts in memory each time it runs. Change the raster line to see where the border stripe changes.")],
 [("Which address holds the IRQ vector?", ["$0314", "$0400", "$D020", "$FFFE only"], 0, "The system IRQ jumps through it."), ("What must a raster handler do?", ["Acknowledge in $D019", "Stop the VIC", "Clear the screen", "Reset"], 0, "Otherwise it fires again."), ("What does SEI do?", ["Disables interrupts", "Enables them", "Sets carry", "Stops the CPU"], 0, "Until CLI.")],
 [("Where is CIA 1?", "$DC00."), ("How to pick a raster line?", "Write $D012."), ("What ends a handler?", "RTI."), ("What does CLI do?", "Enables interrupts.")],
 [MATCH("Interrupts", "Match each register with its job.", [("$D012", "Raster line"), ("$D019", "Acknowledge"), ("$D01A", "Enable raster IRQ"), ("$0314", "IRQ vector")]),
  PL("Timer latch", "Write cia_latch(rate_hz, clock): the CIA timer needs round(clock / rate) - 1. Return [low byte, high byte] of that latch value.", "cia_latch(rate_hz, clock)", """
def cia_latch(rate_hz, clock):
    v = int(round(clock / float(rate_hz))) - 1
    return [v & 255, v >> 8]
""", [[50, 985248], [60, 1022727], [100, 985248]], "Counting from n down to 0 takes n + 1 cycles."),
  PL("Lines and time", "Write line_time_us(clock, cycles_per_line): microseconds a raster line takes, rounded to 2 places.", "line_time_us(clock, cycles_per_line)", """
def line_time_us(clock, cycles_per_line):
    return round(cycles_per_line * 1000000.0 / clock, 2)
""", [[985248, 63], [1022727, 65]], "Cycles divided by the clock, in microseconds.", approx=0.01),
  EMU("irq", "Assembly lab: a raster interrupt", "Run the program. The handler runs every frame.")]))

B.append(CH(
 "Controllers: joysticks, paddles and keys",
 ("Input", ["Joystick | reads | $DC00 and $DC01", "Bits | are | Active low", "Paddles | use | The SID", "Keyboard | is | A matrix", "CIA 1 | scans | Rows and columns", "Fire | is | Bit 4"]),
 ["A joystick has five switches. Each is a bit in a CIA register, and a bit reads 0 when the switch is pressed.",
  "The keyboard is a grid of 8 rows by 8 columns that the CIA scans.",
  "Paddles are knobs read as voltages through the SID's analogue inputs."],
 [("Active low", "A signal that reads 0 when on."), ("Joystick port 2", "Reads at $DC00: bits 0-3 are up, down, left, right, bit 4 is fire."), ("Joystick port 1", "Reads at $DC01, shared with the keyboard."), ("Key matrix", "Eight lines by eight lines; a key joins one row to one column."), ("Paddle", "A variable resistor read through $D419 and $D41A.")],
 ["Port 2 at $DC00; port 1 at $DC01.", "Bit 0 up, 1 down, 2 left, 3 right, 4 fire; 0 means pressed.", "Keyboard: write a column pattern to $DC00, read the rows at $DC01.", "Paddle values come from $D419 and $D41A.", "Port 1 can confuse the keyboard scan."],
 [T("A joystick for the C64 has five switches: up, down, left, right and fire. Port 2 is read at $DC00 and port 1 at $DC01. Bits 0 to 3 are the four directions and bit 4 is fire. A bit is 0 when the switch is pressed, so a resting joystick reads all ones."),
  M(r"\text{pressed}=\lnot\,\text{bit}"),
  C("      lda $dc00     ; read port 2\n      and #$01     ; test bit 0 (up)\n      bne notup     ; non-zero = not pressed\n      ; the stick is pushed up here\nnotup:"),
  T("The keyboard is a matrix of eight columns by eight rows. To read it, you write a byte to $DC00 with exactly one column bit cleared, and then read $DC01. Any cleared bit in the result means a key is down in that row, in the column you selected. The system does this scan for you during every interrupt."),
  T("Because port 1 shares $DC01 with the keyboard rows, a joystick on port 1 can look like key presses. That is why most games use port 2. Paddles are different: each is a knob, read as a voltage through the SID's analogue inputs at $D419 and $D41A."),
  T("Press the pad buttons below the emulator in the lab. The program copies $DC00 to memory, and the goals check that you pressed up and fire.")],
 [("What does a joystick bit read when pressed?", ["0", "1", "255", "It varies"], 0, "Active low."), ("Which bit is fire?", ["Bit 4", "Bit 0", "Bit 7", "Bit 2"], 0, "Above the four directions."), ("Which port is shared with the keyboard?", ["Port 1", "Port 2", "The user port", "The tape port"], 0, "That is why games use port 2.")],
 [("Joystick port 2 address?", "$DC00."), ("How is the keyboard laid out?", "An 8 by 8 matrix."), ("What reads paddles?", "The SID, at $D419/$D41A."), ("Resting joystick value?", "All ones in the low bits.")],
 [MATCH("Bits", "Match each joystick bit with its switch.", [("Bit 0", "Up"), ("Bit 1", "Down"), ("Bit 2", "Left"), ("Bit 4", "Fire")]),
  PL("Decode joystick", "Write decode_joy(v): v is the byte read from $DC00 (only the low five bits matter, a 0 means pressed). Return the list of pressed names in this order: 'up', 'down', 'left', 'right', 'fire'.", "decode_joy(v)", """
def decode_joy(v):
    names = ['up', 'down', 'left', 'right', 'fire']
    out = []
    for i in range(5):
        if not (v >> i) & 1:
            out.append(names[i])
    return out
""", [[127], [126], [111], [118], [96]], "Test each bit; a zero means pressed."),
  PL("Scan the keyboard", "Write scan(matrix, sel): matrix is a list of 8 numbers, one per column; bit r set means the key at row r of that column is down. sel is the byte written to $DC00; a column is selected when its bit is 0. Return the byte read from $DC01: bit r is 0 if some selected column has a key down in row r, otherwise 1.", "scan(matrix, sel)", """
def scan(matrix, sel):
    down = 0
    for c in range(8):
        if not (sel >> c) & 1:
            down |= matrix[c]
    return 255 & ~down
""", [[[0, 0, 0, 0, 0, 0, 0, 0], 255], [[1, 0, 0, 0, 0, 0, 0, 0], 254], [[1, 2, 0, 0, 0, 0, 0, 0], 252], [[0, 4, 0, 0, 0, 0, 0, 0], 253]], "OR the rows of every selected column, then invert."),
  EMU("joy", "Joystick lab", "Press UP and then FIRE on the pad (or turn on the keyboard joystick: arrows and Z).")]))

B.append(CH(
 "The user port",
 ("User port", ["Port B | is | $DD01", "DDR | sets | Direction", "Pin | is | Input or output", "RS-232 | uses | Serial pins", "PA2 | transmits | Data", "Flag | signals | Handshakes"]),
 ["The user port is the edge connector at the back. It gives you eight data pins you can drive or read yourself, plus power and control lines.",
  "Each data pin is an input or an output, chosen by a bit in the data direction register.",
  "Hobbyists used it for modems, printers, sensors and home-made hardware."],
 [("User port", "A 24-pin connector with the CIA 2 port B pins PB0-PB7 and some control lines."), ("DDR", "Data direction register: 1 makes a pin an output, 0 an input."), ("Port B", "CIA 2 data register at $DD01; DDR at $DD03."), ("RS-232", "A serial standard; the user port carries its signals at TTL levels."), ("Handshake", "Signals that tell two devices when data is ready.")],
 ["PB0-PB7 are read and written at $DD01.", "$DD03 is the direction register: bit 1 = output.", "Reading gives output bits for output pins and the outside voltage for input pins.", "The pins are 5 V TTL, not RS-232 voltages.", "A pin can drive only a few milliamps."],
 [T("The user port is the long edge connector on the back of the C64. Its eight data pins, PB0 to PB7, belong to CIA 2 port B. Others carry power, ground, handshake lines and the serial signals used for RS-232 communication. It is the easiest way to connect your own electronics."),
  T("Each of the eight pins is either an output or an input. The direction register at $DD03 decides: a one makes the pin an output, a zero an input. You write bits to $DD01 to drive the output pins, and you read $DD01 to see the input pins. After a reset all of them are inputs."),
  M(r"\text{read}=(\text{out}\ \&\ \text{DDR})\ |\ (\text{pins}\ \&\ \lnot\text{DDR})"),
  C("      lda #$0f\n      sta $dd03    ; PB0-PB3 outputs, PB4-PB7 inputs\n      lda #$05\n      sta $dd01    ; drive 0101 on the outputs\n      lda $dd01    ; read: outputs as written, inputs from outside"),
  T("The voltages are 5 volt logic, not true RS-232 voltage swings, so a level-shifter chip is needed to talk to a real serial device. The pins can only supply a few milliamps, so drive an LED through a resistor and use a transistor for anything bigger, just as with an Arduino pin."),
  T("The lab below shows the three things that matter for each pin: its direction, what you wrote, and what the outside world holds. Set the direction to $0F, write $05, and flip two of the input switches.")],
 [("Which register sets pin direction?", ["$DD03", "$DD01", "$DC00", "$D020"], 0, "Bit 1 = output."), ("What does an input pin read?", ["The outside voltage", "Your last write", "Always 0", "Always 1"], 0, "Not the output latch."), ("What logic level do the pins use?", ["5 V TTL", "12 V", "RS-232 +-12 V", "3.3 V"], 0, "Add a level shifter for RS-232.")],
 [("Where is user port B?", "$DD01."), ("How to make PB0 an output?", "Set bit 0 of $DD03."), ("What does DDR stand for?", "Data direction register."), ("What do you need for RS-232 levels?", "A level shifter.")],
 [MATCH("Registers", "Match each address with its role.", [("$DD01", "Port B data"), ("$DD03", "Port B direction"), ("$DD00", "Port A data"), ("$DD02", "Port A direction")]),
  PL("Read the port", "Write port_read(ddr, out, pins): return the byte read from $DD01. Output pins give the written bits, input pins give the outside levels.", "port_read(ddr, out, pins)", """
def port_read(ddr, out, pins):
    return (out & ddr) | (pins & (~ddr & 255))
""", [[15, 5, 240], [0, 255, 170], [255, 90, 255], [240, 160, 15]], "Combine the two halves with a mask."),
  PL("Direction mask", "Write ddr_mask(outputs): outputs is a list of pin numbers (0-7) that should be outputs. Return the byte to write to $DD03.", "ddr_mask(outputs)", """
def ddr_mask(outputs):
    m = 0
    for p in outputs:
        m |= 1 << p
    return m
""", [[[0, 1, 2, 3]], [[7]], [[]], [[0, 7]]], "Set a bit for each output pin."),
  PL("Serial time", "Write serial_time(nbytes, baud): each byte is sent as 10 bits (start, 8 data, stop). Return the seconds needed, rounded to 3 places.", "serial_time(nbytes, baud)", """
def serial_time(nbytes, baud):
    return round(nbytes * 10.0 / baud, 3)
""", [[100, 300], [1000, 1200], [1, 300]], "Ten bits per byte.", approx=0.001),
  TOOL("uport", "User port lab", "Set DDR to $0F, write $05 to the output register and flip two of the input switches.")]))

B.append(CH(
 "The tape drive",
 ("Tape", ["Datassette | stores | Pulses", "Short medium long | encode | Bits", "Marker | starts | A byte", "Parity | checks | Each byte", "Checksum | checks | A block", "Motor | is | Port bit 5"]),
 ["The Datassette stores programs on an ordinary cassette. Data is written as pulses of three lengths.",
  "Each bit is a pair of pulses. A long and a medium pulse mark the start of every byte, and an odd-parity bit follows the eight data bits.",
  "The processor port controls the motor, the sense switch and the write line."],
 [("Datassette", "The C64's cassette recorder, plugged into the cassette port."), ("Pulse", "A half-wave on tape; its length carries the data."), ("Parity", "An extra bit that makes the count of ones odd, to detect errors."), ("Checksum", "An XOR of all bytes in a block, stored after it."), ("Motor control", "Bit 5 of $0001: 0 turns the motor on.")],
 ["Pulses: short, medium, long.", "Bit 0 = short then medium; bit 1 = medium then short.", "Byte marker = long then medium; end-of-data = long then short.", "Data bits go lowest bit first, then odd parity.", "Checksum = XOR of the data bytes."],
 [T("The Datassette stores sound-like pulses on tape. The computer does not record bytes directly. It records three pulse lengths, called short, medium and long, and the information is in which pulse follows which. The recorder's motor is switched on and off by bit 5 of the processor port at $0001, where zero means on."),
  T("Each byte starts with a marker made of a long pulse and a medium pulse. Then come eight data bits, lowest bit first. A zero bit is a short pulse followed by a medium one, and a one bit is a medium followed by a short. After the data comes a parity bit chosen so that the total number of ones, parity included, is odd."),
  T("A block ends with a long and a short pulse. The last byte of the block is a checksum: the XOR of all the data bytes. When loading, the computer recomputes the parity of each byte and the checksum of the block. If either does not match, you see a load error. Programs are saved twice so that the second copy can repair the first."),
  M(r"\text{checksum}=b_0\oplus b_1\oplus\cdots\oplus b_n"),
  T("Type a few letters into the lab below and look at the pulse train. Count the pulses per byte: two for the marker, sixteen for the data bits, and two for the parity bit, twenty in all.")],
 [("What does a long then medium pulse mean?", ["Start of a byte", "A zero bit", "End of data", "A one bit"], 0, "The byte marker."), ("How is parity chosen?", ["Total ones is odd", "Total ones is even", "Always 1", "Always 0"], 0, "Odd parity."), ("What is the checksum?", ["XOR of the data bytes", "Sum of the bytes", "The first byte", "The length"], 0, "Detects load errors.")],
 [("How many pulses per bit?", "Two."), ("Which bit order?", "Lowest bit first."), ("Which port bit runs the motor?", "Bit 5 of $0001."), ("How is a block ended?", "Long then short pulse.")],
 [MATCH("Pulses", "Match each pattern with its meaning.", [("Long, medium", "Byte marker"), ("Short, medium", "Zero bit"), ("Medium, short", "One bit"), ("Long, short", "End of data")]),
  PL("Tape pulses", "Write tape_pulses(b): return the pulses for one byte as a string of letters S, M and L: the marker 'LM', then eight bits lowest first ('SM' for 0, 'MS' for 1), then the parity bit chosen so the count of ones (data plus parity) is odd.", "tape_pulses(b)", """
def tape_pulses(b):
    s = 'LM'
    ones = 0
    for i in range(8):
        bit = (b >> i) & 1
        ones += bit
        s += 'MS' if bit else 'SM'
    parity = 0 if ones % 2 else 1
    s += 'MS' if parity else 'SM'
    return s
""", [[0], [1], [255], [65]], "Count the ones, then add the parity bit last."),
  PL("Block checksum", "Write checksum(data): the XOR of all the numbers in the list. Return 0 for an empty list.", "checksum(data)", """
def checksum(data):
    x = 0
    for b in data:
        x ^= b
    return x
""", [[[1, 2, 3]], [[255, 255]], [[]], [[72, 73, 54, 52]]], "XOR them one at a time."),
  TOOL("tape", "Tape pulse lab", "Encode at least four characters and read the pulse train.")]))

B.append(CH(
 "The 1541 disk drive",
 ("Disk", ["Track | holds | Sectors", "Sector | holds | 256 bytes", "BAM | tracks | Free blocks", "Directory | is at | Track 18", "Block | is | 254 data bytes", "D64 | is | A disk image"]),
 ["The 1541 floppy drive stores 35 tracks. Outer tracks are longer, so they hold more sectors.",
  "Each sector is 256 bytes: two bytes link to the next block and 254 hold data.",
  "Track 18 is special. It holds the block availability map and the directory."],
 [("Track", "A ring on the disk, numbered 1 to 35."), ("Sector", "A 256-byte block within a track."), ("BAM", "Block Availability Map at track 18 sector 0."), ("Directory", "The list of files, at track 18 from sector 1."), ("Block chain", "Each sector's first two bytes name the next track and sector.")],
 ["Sectors per track: 21 (1-17), 19 (18-24), 18 (25-30), 17 (31-35).", "683 blocks in total; 664 free on a new disk.", "A sector holds 254 data bytes after a 2-byte link.", "BAM at 18/0, directory from 18/1.", "A directory entry is 32 bytes."],
 [T("A 1541 disk has 35 tracks, numbered from 1 at the outside. Outer tracks are longer, so they hold more sectors: 21 sectors on tracks 1 to 17, 19 on tracks 18 to 24, 18 on tracks 25 to 30, and 17 on tracks 31 to 35. That makes 683 blocks, or 174848 bytes, for the whole disk."),
  T("A sector is 256 bytes. The first two bytes give the track and sector of the next block in the file. The remaining 254 bytes are data, so a file of n bytes needs the next whole number above n divided by 254 blocks. The last block has a track of zero and a second byte telling how much of it is used."),
  T("Track 18 holds the disk's housekeeping. Sector 0 is the BAM, a bit map of which blocks are free, together with the disk name. Sectors from 1 on hold the directory, where each 32-byte entry gives the file type, the first track and sector, a 16-character name padded with shifted spaces, and the number of blocks."),
  M(r"\text{blocks}=\lceil n/254\rceil"),
  T("A D64 image stores the sectors one after another, so you can find any sector by counting blocks. The lab below converts track and sector to a block number and a byte offset, and lets you add file names to the directory to see how many blocks stay free.")],
 [("How many tracks has a 1541 disk?", ["35", "40", "80", "17"], 0, "Numbered from 1."), ("Where is the directory?", ["Track 18", "Track 1", "Track 35", "Track 40"], 0, "Starting at sector 1."), ("How many data bytes per sector?", ["254", "256", "128", "512"], 0, "Two bytes are the link.")],
 [("Blocks on a disk?", "683."), ("Where is the BAM?", "Track 18, sector 0."), ("Size of a directory entry?", "32 bytes."), ("How is the end of a file marked?", "Track 0 in the link.")],
 [MATCH("Zones", "Match each track range with its sectors per track.", [("Tracks 1-17", "21"), ("Tracks 18-24", "19"), ("Tracks 25-30", "18"), ("Tracks 31-35", "17")]),
  PL("D64 byte offset", "Write d64_offset(track, sector): the byte offset in a .d64 file. Tracks have 21, 19, 18 or 17 sectors by zone (see the lesson), and every sector is 256 bytes.", "d64_offset(track, sector)", """
def d64_offset(track, sector):
    blocks = 0
    for t in range(1, track):
        if t <= 17:
            blocks += 21
        elif t <= 24:
            blocks += 19
        elif t <= 30:
            blocks += 18
        else:
            blocks += 17
    return (blocks + sector) * 256
""", [[1, 0], [18, 0], [18, 1], [35, 16]], "Count the blocks on all earlier tracks first."),
  PL("Blocks for a file", "Write blocks_for(size): the number of disk blocks a file of size bytes needs (254 data bytes per block, at least 1).", "blocks_for(size)", """
def blocks_for(size):
    n = (size + 253) // 254
    if n < 1:
        n = 1
    return n
""", [[0], [254], [255], [1000]], "Round up."),
  PL("Directory name", "Write dir_name(name): a directory entry stores the name as 16 bytes: the ASCII codes of the name, padded with 160 ($A0) up to 16. Return the list of 16 numbers.", "dir_name(name)", """
def dir_name(name):
    out = [ord(c) for c in name[:16]]
    while len(out) < 16:
        out.append(160)
    return out
""", [["HELLO"], ["ABCDEFGHIJKLMNOPQ"], [""]], "Pad on the right."),
  TOOL("disk", "Disk image lab", "Look up track 18 sector 1 and one more sector, then add a file to the directory.")]))

B.append(CH(
 "Projects and next steps",
 ("Next", ["Joystick | moves | A sprite", "Raster | colours | Bars", "SID | plays | Music", "Disk | stores | Your game", "Emulator | tests | Everything", "Community | shares | Demos"]),
 ["You now know the memory map, the screen, assembly, C, graphics, sound, interrupts, input and storage.",
  "The best way forward is to build something small: a sprite you move, a tune you play, a raster effect.",
  "The lab below starts you off with a joystick-controlled sprite."],
 [("Game loop", "Read input, update, draw, wait for the frame; repeat."), ("Vertical blank", "The gap between frames, a safe time to change graphics."), ("Cartridge", "A ROM plugged into the expansion port."), ("Demo", "A program that shows off what the machine can do."), ("Emulator", "Software for running old machines; the safest way to share work.")],
 ["Game loop: input, update, draw, wait.", "Keep your code in $C000 or after BASIC's stub.", "Test small steps in the emulator.", "Use frames, not delays, to time things.", "Share D64 or PRG files."],
 [T("Almost every C64 game is a loop. Each pass reads the joystick, updates positions and state, draws the sprites, and waits for the next screen refresh. The wait is usually done with a raster interrupt or by polling the raster line, so that the game runs at the display rate, fifty or sixty times a second."),
  T("Start small and grow. First get one sprite on the screen. Then move it with the joystick. Then add a second sprite and test for a collision with a hardware register. Then add sound with the SID and a title screen. Each step is a few lines, and you can test it right away in the emulator."),
  M(r"\text{frames}=\frac{\text{milliseconds}\times\text{frame rate}}{1000}"),
  T("When you outgrow the labs, try a full toolchain on your own computer. cc65 for C, assemblers such as ca65 or ACME, and emulators such as VICE give you the same workflow with bigger projects. The 8bitworkshop site mentioned in the credits offers a complete browser IDE for the C64 as well."),
  T("The final lab is a sprite that follows the joystick. Press right a few times. Then change the program: make up and down work too, add a second sprite, or give it a sound when the fire button is pressed.")],
 [("What does a game loop do?", ["Input, update, draw, wait", "Only draw", "Only wait", "Load a disk"], 0, "Every frame."), ("How do you time things well?", ["Use frames or interrupts", "Use random loops", "Use BASIC", "Use the border"], 0, "They stay steady."), ("Why test in an emulator?", ["Quick and safe", "It is required", "It is faster than a real C64 always", "It is cheaper than code"], 0, "No hardware wear.")],
 [("First step of a game?", "Get a sprite on screen."), ("What is a demo?", "A show-off program."), ("How to time a game?", "By frames."), ("Where do you share work?", "As PRG or D64 files.")],
 [PL("Frames for time", "Write frames_for(ms, fps): how many whole frames fit in ms milliseconds at fps frames per second (round down).", "frames_for(ms, fps)", """
def frames_for(ms, fps):
    return int(ms * fps // 1000)
""", [[1000, 50], [250, 60], [20, 50], [0, 50]], "Multiply and divide by 1000."),
  EMU("project", "Project: move a sprite", "Press RIGHT on the pad a few times. Then extend the program.")]))
