"""Emulator course, chapters 8-13. Original text."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "cd"))
sys.path.insert(0, HERE)
from clib import *
from em1 import CORE, COUNTDOWN

STEP = """
LEN = [1, 2, 2, 2, 2, 2, 2, 2, 1]
NAMES = ['HLT', 'LDI', 'ADD', 'SUB', 'STA', 'LDA', 'JMP', 'JNZ', 'OUT']

def toy_step(mem, st):
    pc = st[0]
    a = st[1]
    z = st[2]
    op = mem[pc & 255]
    n = mem[(pc + 1) & 255]
    out = None
    npc = (pc + LEN[op]) & 255
    if op == 0:
        st[3] = 1
        npc = pc
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
        npc = n
    elif op == 7:
        if not z:
            npc = n
    elif op == 8:
        out = a
    st[0] = npc
    st[1] = a
    st[2] = z
    return out
"""

B = []

B.append(CH(
 "Interrupts and event schedulers",
 ("Events", ["Interrupt | pauses | The CPU", "IRQ | can be | Masked", "NMI | cannot be | Masked", "Edge | triggers | An NMI", "Scheduler | orders | Events", "Next event | bounds | A run slice", "Raster IRQ | fires | On a line"]),
 ["An interrupt makes the CPU stop what it is doing and run a handler. Maskable interrupts (IRQ) can be disabled; non-maskable ones (NMI) cannot.",
  "Rather than checking every device after every instruction, an event scheduler finds when the next thing happens and runs the CPU exactly that long.",
  "Video and timers usually raise interrupts at set cycle counts, such as the start of the vertical blank."],
 [("Interrupt", "A signal that makes the CPU run a handler."), ("IRQ", "A maskable interrupt request."), ("NMI", "A non-maskable interrupt, often triggered by an edge."),
  ("Mask", "A flag that tells the CPU to ignore IRQs."), ("Scheduler", "A list of future events ordered by time."), ("Vertical blank", "The short gap between frames.")],
 ["Check interrupt lines between instructions, not in the middle.", "An IRQ is level-sensitive: it fires while the line is high and the mask allows it.", "An NMI is edge-sensitive: it fires when the line goes from low to high.", "A scheduler runs the CPU until the earliest event, then handles it.", "Keep events in time order; use insertion order for ties.", "A timer that wakes at cycle N is just an event."],
 [T("Sometimes a device needs the CPU right now: the screen has finished a frame, a timer ran out, a key was pressed. Instead of the CPU asking again and again, the device raises an interrupt line. At the next safe moment, the CPU saves where it was, jumps to a handler and comes back later."),
  T("There are two kinds. A maskable interrupt can be turned off by a flag in the CPU, so important code can run undisturbed. A non-maskable interrupt cannot, and is often wired to the start of the vertical blank so that games can update the screen safely. NMI usually reacts to the edge, the moment the line rises."),
  T("The old way to emulate this is to run a fixed number of cycles and then check everything. A cleaner way is a scheduler. Keep a list of events with their times: next scanline, timer expiry, sound sample. Ask for the nearest one, run the CPU until that time, and then handle the event."),
  C("events = [(120, 'timer'), (80, 'hblank'), (200, 'vblank')]\nnow = 0\nwhile events:\n    events.sort()\n    when, name = events.pop(0)\n    run_cpu(when - now)\n    now = when\n    handle(name)", "python"),
  T("This design handles odd cases well. If a timer is set for 37 cycles from now, the CPU runs exactly 37 cycles, with no slack. Event schedulers also make it easy to add new chips: each chip posts its next event. Many accurate modern emulators are built around such a scheduler.")],
 [("Which interrupt can be masked?", ["IRQ", "NMI", "Both", "Neither"], 0, "A flag disables it."),
  ("When does an NMI fire?", ["On a rising edge", "While high", "Never", "Only at reset"], 0, "Edge-sensitive."),
  ("What does a scheduler find?", ["The next event time", "The CPU model", "The ROM", "The frame rate"], 0, "Then runs until then.")],
 [("What is a handler?", "Code run on an interrupt."), ("What is masking?", "Ignoring an interrupt."), ("What is vblank?", "The gap between frames."), ("What is an event?", "Something at a future time.")],
 [MATCH("Interrupts", "Match each term with its meaning.", [("IRQ", "Maskable request"), ("NMI", "Cannot be masked"), ("Edge", "A change from low to high"), ("Scheduler", "Ordered list of events")]),
  PL("Interrupt service", "Write irq_service(steps): each step is [irq, nmi, i_flag] with 0 or 1 values. An NMI is serviced when nmi is 1 and was 0 at the step before (it is 0 before the first step). Otherwise an IRQ is serviced if irq is 1 and i_flag is 0. Return the list of 'NMI', 'IRQ' or 'none' for each step.", "irq_service(steps)", """
def irq_service(steps):
    prev = 0
    out = []
    for irq, nmi, iflag in steps:
        if nmi == 1 and prev == 0:
            out.append('NMI')
        elif irq == 1 and iflag == 0:
            out.append('IRQ')
        else:
            out.append('none')
        prev = nmi
    return out
""", [[[[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 1, 0], [0, 1, 0], [1, 1, 0]]], [[]], [[[1, 1, 1], [1, 1, 0]]]], "Remember the previous NMI level.", approx=None),
  PL("Event scheduler", "Write scheduler(events, until): events is a list of [time, name]. Return the names of the events with time at most until, ordered by time (ties keep the original order).", "scheduler(events, until)", """
def scheduler(events, until):
    items = []
    for i, e in enumerate(events):
        if e[0] <= until:
            items.append([e[0], i, e[1]])
    items.sort()
    return [x[2] for x in items]
""", [[[[120, "timer"], [80, "hblank"], [200, "vblank"]], 150], [[[5, "a"], [5, "b"], [1, "c"]], 5], [[], 10], [[[9, "x"]], 3]], "Sort by time, then position.", approx=None),
  PL("Next event", "Write next_event(timers, now): timers is a list of [period, due] pairs with due the cycle count of the next firing. Return [cycles_to_run, index] for the earliest due (on a tie, the lowest index); cycles_to_run is never below 0.", "next_event(timers, now)", """
def next_event(timers, now):
    best = 0
    for i in range(1, len(timers)):
        if timers[i][1] < timers[best][1]:
            best = i
    return [max(0, timers[best][1] - now), best]
""", [[[[100, 120], [50, 80], [10, 80]], 50], [[[10, 5]], 9], [[[3, 7], [3, 4]], 0]], "Find the minimum due time.", approx=None),
  PL("Raster position", "Write raster(cycle, per_line, lines): return [frame, line, cycle_in_line] for an absolute CPU cycle count.", "raster(cycle, per_line, lines)", """
def raster(cycle, per_line, lines):
    frame_len = per_line * lines
    return [cycle // frame_len, (cycle % frame_len) // per_line, cycle % per_line]
""", [[0, 100, 10], [250, 100, 10], [1005, 100, 10], [999, 100, 10]], "Divide twice.", approx=None)]))

B.append(CH(
 "Video and sound",
 ("Video", ["Framebuffer | holds | The picture", "Tile | repeats | A small image", "Sprite | moves | Over the background", "Palette | maps | Numbers to colors", "Scanline | is | Drawn in turn", "Sample | is | One sound value", "Mixer | adds | Channels"]),
 ["Many old machines draw the picture from tiles, sprites and palettes rather than a full bitmap. An emulator reads those tables and writes pixels into a framebuffer.",
  "Rendering a whole frame at once is simple; rendering line by line is needed when games change settings between lines.",
  "Sound is a stream of samples, often square waves mixed together. The emulator must make samples at the audio rate, in step with the cycles."],
 [("Framebuffer", "A block of memory holding the pixels of the picture."), ("Tile", "A small block of pixels reused many times."), ("Sprite", "A movable object drawn over the background."),
  ("Palette", "A table that turns small numbers into colors."), ("Sample", "One measurement of a sound wave."), ("Mixer", "Code that adds several sound channels together.")],
 ["Tile maps store which tile goes where; the tiles store the pixels.", "A scanline renderer draws one line at a time using the settings in force at that moment.", "RGB565 packs a color in 16 bits: 5 red, 6 green, 5 blue.", "A square wave toggles between high and low at a fixed frequency.", "Mix by adding samples and clamping to the valid range.", "Accuracy matters: games change registers mid-frame to get effects."],
 [T("Early consoles had very little memory, so their graphics chips were clever. They kept a small set of 8 by 8 pixel tiles and a map saying which tile goes at each place on the screen. A background of a whole level was just a table of numbers. Sprites, which are the moving characters, were drawn over it."),
  T("An emulator must turn those tables into pixels. A simple method draws the entire frame once the frame is over. A better method draws each scanline at the right time, because games often change the scroll or palette part way down the screen to make effects, such as a wavy water or a split screen."),
  C("def tile_row(tile_ids, tiles, y):\n    # tiles[id] is a list of 8 strings of 8 pixels\n    return ''.join(tiles[t][y] for t in tile_ids)", "python"),
  T("Colors are often packed. In the common RGB565 format a 16-bit number holds 5 bits of red, 6 of green and 5 of blue. To show it on a modern screen you spread each part out to 8 bits. Palettes add another step, because a pixel value is just an index into a table of colors."),
  T("Sound is simpler than it sounds. The hardware makes tones, often square waves, and noise. The emulator creates a sample for each tick of the audio clock, say 44,100 a second, adds the channels and sends the result to the sound card. If the samples arrive late, you hear clicks, so timing matters again.")],
 [("What does a palette do?", ["Maps numbers to colors", "Draws sprites", "Plays sound", "Stores ROM"], 0, "An index into colors."),
  ("Why draw by scanline?", ["Games change settings mid-frame", "It uses less memory", "It looks darker", "It is required by Python"], 0, "Raster effects."),
  ("What is a square wave?", ["A signal toggling between two levels", "A sine", "A noise", "A sprite"], 0, "High, low, high, low.")],
 [("What is a tile?", "A small reusable block of pixels."), ("What is a sprite?", "A movable object."), ("What is RGB565?", "16-bit color."), ("What is a sample?", "One sound value.")],
 [MATCH("Graphics", "Match each term with its meaning.", [("Tile", "A reusable block of pixels"), ("Sprite", "A movable object"), ("Palette", "Index to color table"), ("Framebuffer", "Memory holding the picture")]),
  PL("Draw a scanline", "Write render_row(tile_ids, tiles, y): tiles is a list of tiles, each a list of 8 strings of 8 characters. Return the string for pixel row y built by joining that row of each tile in tile_ids.", "render_row(tile_ids, tiles, y)", """
def render_row(tile_ids, tiles, y):
    out = ''
    for t in tile_ids:
        out += tiles[t][y]
    return out
""", [[[0, 1, 0], [["........", "........", "........", "........", "........", "........", "........", "........"], ["########", "#......#", "#......#", "#......#", "#......#", "#......#", "#......#", "########"]], 0], [[1], [["........"] * 8, ["#.#.#.#."] * 8], 3], [[], [], 0]], "Join one row of each tile.", approx=None),
  PL("Sprite collision", "Write overlap(a, b): a and b are rectangles [x, y, w, h]. Return True if they overlap (touching edges do not count).", "overlap(a, b)", """
def overlap(a, b):
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]
""", [[[0, 0, 4, 4], [2, 2, 4, 4]], [[0, 0, 4, 4], [4, 0, 4, 4]], [[0, 0, 2, 2], [5, 5, 1, 1]], [[1, 1, 3, 3], [2, 2, 1, 1]]], "Compare ranges on both axes.", approx=None),
  PL("RGB565 to RGB888", "Write rgb565(v): return [r, g, b] with each 0 to 255, scaling r and b (5 bits) as r x 255 // 31 and g (6 bits) as g x 255 // 63.", "rgb565(v)", """
def rgb565(v):
    r = (v >> 11) & 31
    g = (v >> 5) & 63
    b = v & 31
    return [r * 255 // 31, g * 255 // 63, b * 255 // 31]
""", [[0xFFFF], [0x0000], [0xF800], [0x07E0], [0x001F], [0x8410]], "Mask and scale each field.", approx=None),
  PL("Square wave", "Write square(freq, rate, n): n samples of a square wave of frequency freq at sample rate rate. Sample i is 1 when (i x freq x 2 // rate) is even, otherwise -1.", "square(freq, rate, n)", """
def square(freq, rate, n):
    out = []
    for i in range(n):
        out.append(1 if (i * freq * 2 // rate) % 2 == 0 else -1)
    return out
""", [[1, 8, 8], [2, 8, 8], [440, 44100, 5], [1, 4, 8]], "Integer arithmetic keeps it exact.", approx=None),
  PL("Mix channels", "Write mix(a, b): add two lists of samples item by item (the shorter list is padded with zeros) and clamp each result to the range -32768 to 32767.", "mix(a, b)", """
def mix(a, b):
    n = max(len(a), len(b))
    out = []
    for i in range(n):
        x = a[i] if i < len(a) else 0
        y = b[i] if i < len(b) else 0
        s = x + y
        out.append(max(-32768, min(32767, s)))
    return out
""", [[[100, 200], [50, 50]], [[30000], [30000]], [[-30000, 1], [-30000]], [[], [5]]], "Add, then clamp.", approx=None)]))

B.append(CH(
 "Input, timers and devices",
 ("Devices", ["Joypad | reports | Button bits", "Matrix | scans | Keys", "Timer | counts | Down", "DMA | copies | Memory", "Polling | reads | Input", "Frontend | sends | Key events", "Device | has | Registers"]),
 ["Input devices appear to the guest as registers. A joypad is often a byte where each bit is a button; a keyboard may be a matrix that the program scans row by row.",
  "Timers count down at a fixed rate, and fire an interrupt at zero. DMA lets a device copy memory without the CPU, and the CPU may have to wait while it does.",
  "Treat every device as a small state machine with registers, and update it by cycles, not by wall-clock time."],
 [("Joypad register", "A byte whose bits show which buttons are down."), ("Key matrix", "Keys wired in rows and columns, read by selecting rows."), ("Timer", "A counter that decrements at a fixed rate."),
  ("DMA", "Direct memory access: copying without the CPU."), ("Polling", "Reading a device again and again."), ("Latch", "A register that holds a value until read.")],
 ["Map host keys to guest buttons in the frontend; the core just sees bits.", "Timers must count in cycles, keeping the leftover cycles between updates.", "DMA often steals cycles from the CPU: charge them.", "A read of the key matrix returns the OR of the selected rows.", "Fewer surprises: update devices only when their registers are accessed or their event fires.", "Record inputs per frame to make runs repeatable."],
 [T("The guest does not know about your keyboard. It knows its own hardware. A console pad might be a register where bit 0 means up, bit 1 means down and so on. Your frontend translates real key presses into that byte, and the core hands it to the program when it reads that address."),
  C("ORDER = ['up', 'down', 'left', 'right', 'a', 'b']\ndef joypad(pressed):\n    v = 0\n    for i, name in enumerate(ORDER):\n        if name in pressed:\n            v |= 1 << i\n    return v", "python"),
  T("Computer keyboards are often a matrix of rows and columns. The program drives one or more rows, then reads the columns. If it selects several rows, a pressed key in any of them shows up. In the emulator, you OR the bytes of the rows that are selected."),
  T("Timers are counters. A typical one counts down sixty times a second and sets a flag at zero. Because the emulator measures time in cycles, a timer must keep the leftover cycles between steps. Otherwise it drifts. This is the same rule as in the timing chapter."),
  T("DMA is a way to copy memory without running CPU instructions. On some machines the CPU is stopped for the duration, so a copy of 256 bytes costs hundreds of cycles. If you forget to charge them, timing-sensitive games break. When a device is the source of surprise, check the cost first.")],
 [("What does a joypad register hold?", ["One bit per button", "A picture", "The score", "Sound"], 0, "Bits for buttons."),
  ("What does DMA do?", ["Copies memory without the CPU", "Draws sprites", "Plays sound", "Reads keys"], 0, "May steal cycles."),
  ("Why keep leftover cycles in a timer?", ["To avoid drift", "To save memory", "To hide bugs", "To increase speed"], 0, "Counts must be exact.")],
 [("What is polling?", "Reading a device repeatedly."), ("What is a key matrix?", "Rows and columns of keys."), ("What does a timer do?", "Counts down."), ("What does DMA cost?", "CPU cycles.")],
 [MATCH("Devices", "Match each device with its job.", [("Joypad", "Button bits"), ("Timer", "Counts down at a rate"), ("DMA", "Copies memory"), ("Key matrix", "Rows and columns")]),
  PL("Joypad byte", "Write joypad(pressed, order): return a byte with bit i set when order[i] is in pressed.", "joypad(pressed, order)", """
def joypad(pressed, order):
    v = 0
    for i in range(len(order)):
        if order[i] in pressed:
            v |= 1 << i
    return v
""", [[["up", "a"], ["up", "down", "left", "right", "a", "b"]], [[], ["a", "b"]], [["b"], ["a", "b"]], [["left", "right"], ["up", "down", "left", "right"]]], "Set the bit for each pressed button.", approx=None),
  PL("Key matrix", "Write key_scan(rows, selected): rows is a list of ints, one per row, with a bit per key pressed. selected is a list of row indexes being driven. Return the OR of those rows (0 if none selected).", "key_scan(rows, selected)", """
def key_scan(rows, selected):
    v = 0
    for i in selected:
        v |= rows[i]
    return v
""", [[[1, 2, 4], [0, 2]], [[1, 2, 4], []], [[255], [0]], [[3, 12], [1]]], "OR the chosen rows.", approx=None),
  PL("Timer tick", "Write timer_tick(value, leftover, cycles, per_tick): total = leftover + cycles; ticks = total // per_tick; value drops by ticks but not below 0; new leftover = total % per_tick. Return [value, leftover].", "timer_tick(value, leftover, cycles, per_tick)", """
def timer_tick(value, leftover, cycles, per_tick):
    total = leftover + cycles
    ticks = total // per_tick
    return [max(0, value - ticks), total % per_tick]
""", [[10, 0, 25, 10], [10, 5, 5, 10], [1, 0, 100, 10], [0, 3, 3, 4]], "Keep the remainder.", approx=None),
  PL("DMA copy", "Write dma(mem, src, dst, length): copy length bytes from src to dst (read all the source bytes first, then write them). Return [new_mem, cycles] where cycles = 4 + 2 x length.", "dma(mem, src, dst, length)", """
def dma(mem, src, dst, length):
    m = list(mem)
    data = m[src:src + length]
    for i in range(length):
        m[dst + i] = data[i]
    return [m, 4 + 2 * length]
""", [[[1, 2, 3, 0, 0, 0], 0, 3, 3], [[1, 2, 3, 4], 0, 1, 3], [[9, 9], 0, 1, 0]], "Snapshot the source first.", approx=None)]))

B.append(CH(
 "Speed: caches, JITs and what has changed since the 1990s",
 ("Speed", ["Interpreter | runs | One by one", "Basic block | has | One way in", "JIT | translates | At run time", "Cache | stores | Translated code", "Static recompile | translates | Ahead of time", "Profile | finds | Hot code", "Hardware assist | runs | Same ISA fast"]),
 ["An interpreter is simple and portable but slow. A dynamic recompiler, or JIT, translates blocks of guest code into host code the first time they run and caches the result.",
  "Static recompilation translates a whole program ahead of time, but struggles with code that changes itself and with telling code from data.",
  "Much advice from the 1990s, written for assembly and early compilers, is out of date. Measure first, and let the compiler and the profiler help."],
 [("Basic block", "A run of instructions with one entry and one exit, ending in a jump."), ("JIT", "Just-in-time compilation: translating code while the program runs."), ("Code cache", "Storage for already translated blocks."),
  ("Static recompilation", "Translating the whole guest program before it runs."), ("Profiler", "A tool that shows where a program spends its time."), ("Hardware assist", "Using the host CPU's own features, such as virtualization, to run guest code.")],
 ["Interpret first; optimize only the hot paths found by a profiler.", "A JIT translates basic blocks and caches them by guest address.", "Self-modifying code means the cache must be invalidated when guest memory is written.", "Modern systems often forbid memory that is both writable and executable; JITs write first, then switch to executable.", "If the guest and host share an instruction set, virtualization can run guest code almost natively.", "Prefer clear code in a modern compiled language; the compiler outperforms hand tuning for most uses."],
 [T("An interpreter pays a toll on every instruction: fetch, decode, dispatch. If the guest runs a loop a million times, the toll is paid a million times. A dynamic recompiler pays once. It translates a block into host code, remembers it, and runs the stored version every time."),
  T("A basic block is a straight run of instructions that ends with a jump. It is the natural unit to translate, since control always enters at the start. To find blocks, mark the program start, every jump target and every instruction after a jump."),
  C("# leaders: where basic blocks start\nleaders = {0}\nfor pc, op, target in instructions:\n    if op in ('JMP', 'JNZ'):\n        leaders.add(target)\n        leaders.add(pc + length)", "python"),
  T("The old HOWTO said static translation cannot cope with self-modifying code, and that is still true. The dynamic approach has the same issue in a milder form: when the guest writes to memory that holds translated code, the cache entry must be thrown away. Many JITs track which pages hold code and watch writes to them."),
  T("Other advice has aged. Today, compilers turn a dense switch into a jump table by themselves, so hand-written label tables are rarely needed. The register keyword is ignored. Hand-unrolled loops often do worse than the compiler's choices. Use fixed-width integer types and shifts, not pointer tricks. Use a profiler such as perf or a flame graph before changing anything. Assembly is rarely needed, and languages such as Rust, C++ and Zig are all common choices."),
  T("New constraints have arrived too. Some platforms refuse to run memory that is both writable and executable, or forbid JITs altogether, so a fast interpreter is still valuable. Multi-core hosts rarely help a single emulated CPU, but a separate thread for audio or video can. And the best news is testing: hardware-derived test suites now exist for many classic CPUs, as the next chapter shows.")],
 [("What is a basic block?", ["Instructions with one entry and one exit", "A single byte", "A memory bank", "A frame"], 0, "Straight-line code."),
  ("What invalidates a JIT cache entry?", ["The guest writing to translated code", "A new frame", "A key press", "Sound output"], 0, "Self-modifying code."),
  ("What should you do before optimizing?", ["Profile", "Rewrite in assembly", "Remove tests", "Use more threads"], 0, "Measure first.")],
 [("What does a JIT do?", "Translates at run time."), ("What is hardware assist?", "Running guest code natively."), ("Why a code cache?", "Avoid retranslating."), ("What is a profiler for?", "Finding hot code.")],
 [MATCH("Then and now", "Match the old advice with the modern view.", [("Hand-written jump tables", "Compilers make them from a switch"), ("The register keyword", "Ignored by compilers"), ("Pointer tricks for byte order", "Use shifts and masks"), ("Guess where it is slow", "Profile it")]),
  PL("Basic blocks", "Write basic_blocks(program): decode TOY8 (instruction lengths 1,2,2,2,2,2,2,2,1 for opcodes 0..8) and return the sorted list of block start addresses: 0; every JMP (6) or JNZ (7) target that lies inside the program; and the address after every JMP, JNZ or HLT (0) if it lies inside the program.", "basic_blocks(program)", """
def basic_blocks(program):
    lens = [1, 2, 2, 2, 2, 2, 2, 2, 1]
    leaders = set([0])
    pc = 0
    while pc < len(program):
        op = program[pc]
        n = lens[op] if op < 9 else 1
        if op == 6 or op == 7:
            t = program[pc + 1]
            if t < len(program):
                leaders.add(t)
        if op in (0, 6, 7):
            if pc + n < len(program):
                leaders.add(pc + n)
        pc += n
    return sorted(leaders)
""", [[COUNTDOWN], [[1, 0, 7, 6, 0, 0, 8, 0]], [[8, 8, 0]], [[6, 0]]], "Walk the program and mark leaders.", approx=None),
  PL("Translate a block", "Write block_ops(program, start): decode TOY8 instructions from start up to and including the first JMP, JNZ or HLT (or the end of the program). Return a list of texts such as 'LDI 3' or 'OUT' (names HLT LDI ADD SUB STA LDA JMP JNZ OUT; one-byte instructions have no operand).", "block_ops(program, start)", """
def block_ops(program, start):
    names = ['HLT', 'LDI', 'ADD', 'SUB', 'STA', 'LDA', 'JMP', 'JNZ', 'OUT']
    out = []
    pc = start
    while pc < len(program):
        op = program[pc]
        if op == 0 or op == 8:
            out.append(names[op])
            pc += 1
        else:
            out.append(names[op] + ' ' + str(program[pc + 1]))
            pc += 2
        if op in (0, 6, 7):
            break
    return out
""", [[COUNTDOWN, 0], [COUNTDOWN, 2], [COUNTDOWN, 7], [[1, 1, 2, 2], 0]], "Stop at the first control instruction.", approx=None),
  PL("Code cache", "Write cache_sim(trace, cap): trace is a list of block addresses executed in order. The cache holds at most cap blocks and evicts the least recently used. Return [hits, misses].", "cache_sim(trace, cap)", """
def cache_sim(trace, cap):
    cache = []
    hits = 0
    misses = 0
    for b in trace:
        if b in cache:
            hits += 1
            cache.remove(b)
            cache.append(b)
        else:
            misses += 1
            if len(cache) >= cap:
                cache.pop(0)
            cache.append(b)
    return [hits, misses]
""", [[[0, 2, 2, 2, 7], 4], [[1, 2, 3, 1, 2, 3], 2], [[1, 2, 3, 1, 2, 3], 3], [[], 2]], "Move used blocks to the end.", approx=None),
  PL("Interpret or JIT", "Write jit_total(trace, sizes, interp_cost, compile_cost, run_cost): trace lists block ids; sizes maps id to the number of instructions in the block (a dict with string keys, ids are strings too). Interpreting costs interp_cost per instruction each time. The JIT pays compile_cost per instruction the first time a block runs, plus run_cost per instruction on every run. Return [interpreted_total, jit_total].", "jit_total(trace, sizes, interp_cost, compile_cost, run_cost)", """
def jit_total(trace, sizes, interp_cost, compile_cost, run_cost):
    seen = set()
    interp = 0
    jit = 0
    for b in trace:
        n = sizes[b]
        interp += n * interp_cost
        if b not in seen:
            seen.add(b)
            jit += n * compile_cost
        jit += n * run_cost
    return [interp, jit]
""", [[["a", "b", "a", "a"], {"a": 4, "b": 2}, 10, 50, 1], [["a"], {"a": 3}, 10, 50, 1], [["a"] * 100, {"a": 5}, 10, 50, 1], [[], {}, 1, 1, 1]], "A JIT pays once and runs cheaply.", approx=None)]))

B.append(CH(
 "Accuracy and testing",
 ("Accuracy", ["Accuracy | has | Levels", "Instruction accurate | matches | Results", "Cycle accurate | matches | Timing", "Test ROM | checks | Behavior", "Single-step test | checks | One instruction", "Save state | stores | Everything", "Determinism | allows | Replay"]),
 ["How accurate an emulator must be depends on the guest. Some software works with approximate timing, while some relies on exact cycles and undocumented behavior.",
  "Test your CPU with test ROMs and with hardware-derived single-instruction test suites, which give the exact registers, memory and sometimes bus activity before and after each instruction.",
  "A deterministic core lets you save state, replay input, and compare runs, which makes bugs reproducible."],
 [("Instruction accurate", "Gets the same results per instruction but not necessarily the same timing."), ("Cycle accurate", "Matches the guest's timing cycle by cycle."), ("High-level emulation", "Reproducing a chip's job instead of its inner workings."),
  ("Test ROM", "A program that checks parts of a machine and reports pass or fail."), ("Single-step test", "A record of a state before one instruction and the expected state after."), ("Save state", "A snapshot of the whole emulated machine.")],
 ["Pick the level of accuracy the software needs.", "High-level emulation can be faster but can break software that depends on details.", "Hardware-generated JSON suites exist for many CPUs, including the 6502 family, Z80, 8088 and 68000.", "Test ROMs exist for many machines and run inside the emulator.", "Keep the core deterministic: no clocks, no random numbers without a seed.", "A checksum on save states catches corrupted files."],
 [T("There are many levels of accuracy. An instruction-accurate core gets each instruction's result right, but may not match the timing. A cycle-accurate core matches the exact cycle of every bus access. Some systems, such as the Commodore 64, have software that depends on cycle-level behavior. Others do not, and a simpler emulator is enough."),
  T("High-level emulation reproduces what a chip does, not how. Some Game Boy Advance emulators can run without the real boot ROM by imitating its functions, at a small cost in accuracy. The Nintendo 64 used preprogrammed graphics routines, so emulators can handle those directly. The trade is speed against exactness."),
  T("How do you know your CPU is right? There are two good ways. First, test ROMs: programs that run in your emulator and print pass or fail. Second, and more recent, are test suites made from real hardware. Each test lists registers and memory before one instruction and the expected state after it. You load the state, run one instruction and compare."),
  C("def check(case):\n    cpu = load(case['initial'])\n    cpu.step()\n    return diff(case['final'], cpu.state())   # [] means pass", "python"),
  T("Save states copy the whole machine to a file: registers, memory, device state. They need the core to be a pure function of its state and inputs. A deterministic core also lets you record the buttons pressed each frame and replay the exact same run, which is a huge help when you hunt a bug that appears after twenty minutes.")],
 [("What is cycle accurate?", ["Matches timing cycle by cycle", "Fast", "Small", "High level"], 0, "Needed by some software."),
  ("What is a single-step test?", ["State before and after one instruction", "A full game", "A sound test", "A backup"], 0, "Exact checks."),
  ("What does determinism allow?", ["Replay and save states", "More colors", "Faster ROMs", "Smaller files"], 0, "Same inputs, same results.")],
 [("What is HLE?", "Imitating what a chip does."), ("What is a test ROM?", "A self-checking program."), ("What is a save state?", "A snapshot."), ("Why a checksum?", "To catch corruption.")],
 [MATCH("Accuracy", "Match each term with its meaning.", [("Cycle accurate", "Matches exact timing"), ("Instruction accurate", "Matches results of each instruction"), ("High-level emulation", "Imitates what a chip does"), ("Test ROM", "A self-checking program")]),
  PL("Compare states", "Write diff_state(expected, actual): both are dicts. Return the sorted list of keys whose values differ (a key missing from either side counts as different).", "diff_state(expected, actual)", """
def diff_state(expected, actual):
    keys = set(list(expected.keys()) + list(actual.keys()))
    bad = []
    for k in keys:
        if k not in expected or k not in actual or expected[k] != actual[k]:
            bad.append(k)
    return sorted(bad)
""", [[{"a": 1, "pc": 2}, {"a": 1, "pc": 2}], [{"a": 1, "pc": 2}, {"a": 5, "pc": 2}], [{"a": 1}, {"a": 1, "z": 0}], [{}, {}]], "Compare each key.", approx=None),
  PL("Single-step test", "Write check_case(case): case has 'initial' ({'a', 'pc', 'ram' as a list of [addr, value]}) and 'final' ({'a', 'pc'}). Run exactly one TOY8 instruction (LDI, ADD, SUB, JMP or OUT) from the initial state (memory is 256 bytes of zeros plus the ram entries; the instruction is at pc) and return the sorted list of keys among 'a' and 'pc' whose result differs from final (an empty list means the test passes).", "check_case(case)", STEP + """
def check_case(case):
    mem = [0] * 256
    for addr, v in case['initial']['ram']:
        mem[addr] = v
    st = [case['initial']['pc'], case['initial']['a'], False, 0]
    toy_step(mem, st)
    bad = []
    if st[1] != case['final']['a']:
        bad.append('a')
    if st[0] != case['final']['pc']:
        bad.append('pc')
    return sorted(bad)
""", [[{"initial": {"a": 0, "pc": 0, "ram": [[0, 1], [1, 5]]}, "final": {"a": 5, "pc": 2}}], [{"initial": {"a": 250, "pc": 4, "ram": [[4, 2], [5, 10]]}, "final": {"a": 4, "pc": 6}}], [{"initial": {"a": 3, "pc": 0, "ram": [[0, 3], [1, 5]]}, "final": {"a": 0, "pc": 2}}], [{"initial": {"a": 7, "pc": 9, "ram": [[9, 6], [10, 20]]}, "final": {"a": 7, "pc": 20}}], [{"initial": {"a": 1, "pc": 0, "ram": [[0, 8]]}, "final": {"a": 1, "pc": 2}}]], "The last two cases have wrong expectations on purpose.", approx=None),
  PL("Fletcher-16", "Write fletcher16(data): data is a list of bytes. sum1 and sum2 both start at 0; for each byte: sum1 = (sum1 + byte) % 255, sum2 = (sum2 + sum1) % 255. Return sum2 x 256 + sum1.", "fletcher16(data)", """
def fletcher16(data):
    s1 = 0
    s2 = 0
    for b in data:
        s1 = (s1 + b) % 255
        s2 = (s2 + s1) % 255
    return s2 * 256 + s1
""", [[[1, 2]], [[]], [[255, 255, 255]], [[0, 1, 2, 3, 4, 5, 6, 7]]], "Two running sums.", approx=None),
  PL("Save state", "Write save_state(a, pc, z, ram): return a list: [a, pc low byte, pc high byte, 1 or 0 for z] followed by the ram bytes, followed by the two checksum bytes [sum1, sum2] of Fletcher-16 over that body (sum1 = sum1 + byte mod 255, sum2 = sum2 + sum1 mod 255).", "save_state(a, pc, z, ram)", """
def save_state(a, pc, z, ram):
    body = [a, pc & 255, (pc >> 8) & 255, 1 if z else 0] + list(ram)
    s1 = 0
    s2 = 0
    for b in body:
        s1 = (s1 + b) % 255
        s2 = (s2 + s1) % 255
    return body + [s1, s2]
""", [[5, 0x1234, True, [1, 2, 3]], [0, 0, False, []], [255, 65535, True, [255]]], "Body then checksum.", approx=None),
  PL("Replayable randomness", "Write lcg(seed, n): a deterministic generator: x = seed; repeat n times: x = (x x 1103515245 + 12345) & 0x7FFFFFFF and output x % 256. Return the list of outputs.", "lcg(seed, n)", """
def lcg(seed, n):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        out.append(x % 256)
    return out
""", [[1, 5], [42, 3], [0, 0], [2147483647, 4]], "Same seed, same values.", approx=None)]))

B.append(CH(
 "Debuggers, preservation and next steps",
 ("Next steps", ["Debugger | steps | Code", "Breakpoint | stops | At an address", "Trace | logs | Instructions", "Disassembler | shows | Mnemonics", "Preservation | keeps | Old software alive", "Homebrew | makes | New software", "Community | shares | Documents"]),
 ["A debugger and a disassembler are the emulator author's best tools: they let you stop at an address, look at registers and memory, and read the program as text.",
  "Emulation is also how old software and documents stay usable, and how new software for old systems gets made.",
  "Legal and ethical rules differ by country. Emulators themselves are widely treated as lawful, but sharing copyrighted ROMs or system software without permission is not; this course is not legal advice."],
 [("Debugger", "A tool to run a program step by step and inspect its state."), ("Breakpoint", "An address where execution pauses."), ("Disassembler", "A tool turning bytes into instruction names."),
  ("Trace", "A log of executed instructions and states."), ("Preservation", "Keeping old software and data usable."), ("Homebrew", "New programs written for old systems.")],
 ["Build the debugger and disassembler early.", "Peeking at memory must not trigger device side effects.", "Trace logs let you compare your emulator against a known-good one line by line.", "Dump your own cartridges and discs; do not distribute copyrighted system software.", "The old HOWTO's links are mostly gone; use present-day wikis, test suites, forums and open-source cores instead.", "Good places to learn: platform wikis such as the NESdev Wiki, Pan Docs for the Game Boy, public test ROMs and open emulator source code."],
 [T("Writing an emulator without a debugger is like driving at night without headlights. The first thing to add after the CPU is a way to stop, step and look. A disassembler turns the bytes at an address into names such as LDI 3, so you can read the guest program, and a trace log prints each instruction as it runs."),
  C("pc = 0\nwhile pc < len(program):\n    name, operand, length = decode(program, pc)\n    print('%04x  %s %s' % (pc, name, operand if operand is not None else ''))\n    pc += length", "python"),
  T("A breakpoint is a list of addresses. Before each instruction, check whether the program counter is in the list, and if so, stop. Combine breakpoints with single stepping and a view of memory and you can find most bugs. When you read memory for display, use a side-effect-free peek."),
  T("Emulation has a wider purpose. It keeps software and documents alive when the original hardware is gone, which is called digital preservation. It lets developers write programs for old systems and test them, and lets engineers test new chips before they are built. It is a fine way to learn how computers really work."),
  T("Where next? Pick a small system, such as CHIP-8, the Game Boy or the NES. Read its public documentation, write the CPU, test it with the hardware-derived suites, then add video, sound and input. Look at open-source emulators for ideas, use the community wikis for details, and share your findings. The HOWTO you may have read years ago was a great start, and now you have the modern map.")],
 [("What does a breakpoint do?", ["Stops at an address", "Makes code faster", "Deletes a ROM", "Plays sound"], 0, "Pauses the run."),
  ("What does a disassembler show?", ["Instruction names from bytes", "The picture", "The sound", "The clock"], 0, "Readable code."),
  ("Why must a debugger peek without side effects?", ["Reads can change device state", "It is faster", "It saves memory", "It is a rule of Python"], 0, "MMIO.")],
 [("What is a trace?", "A log of executed instructions."), ("What is homebrew?", "New software for old systems."), ("What is preservation?", "Keeping software usable."), ("What system to start with?", "CHIP-8 or Game Boy.")],
 [MATCH("Tools", "Match each tool with its job.", [("Disassembler", "Shows instruction names"), ("Breakpoint", "Stops at an address"), ("Trace log", "Records what ran"), ("Test suite", "Checks the CPU against hardware")]),
  PL("Disassemble", "Write disassemble(program): return a list of lines for TOY8, one per instruction, of the form 'AAAA: NAME operand' with the address as four lowercase hex digits and no operand for one-byte instructions (names HLT LDI ADD SUB STA LDA JMP JNZ OUT; lengths 1,2,2,2,2,2,2,2,1; operands in decimal). Stop at the end of the program.", "disassemble(program)", """
def disassemble(program):
    names = ['HLT', 'LDI', 'ADD', 'SUB', 'STA', 'LDA', 'JMP', 'JNZ', 'OUT']
    h = '0123456789abcdef'
    out = []
    pc = 0
    while pc < len(program):
        op = program[pc]
        addr = h[(pc >> 12) & 15] + h[(pc >> 8) & 15] + h[(pc >> 4) & 15] + h[pc & 15]
        if op == 0 or op == 8:
            out.append(addr + ': ' + names[op])
            pc += 1
        else:
            out.append(addr + ': ' + names[op] + ' ' + str(program[pc + 1]))
            pc += 2
    return out
""", [[COUNTDOWN], [[8]], [[]], [[1, 255, 6, 0]]], "Format the address by hand.", approx=None),
  PL("Run to breakpoint", "Write run_until(program, breakpoints, max_steps): run TOY8 from address 0 (the machine as in the earlier labs, memory padded with zeros). Before executing each instruction, stop if its address is in breakpoints. Return [pc, steps, reason] where reason is 'breakpoint', 'halt' (after executing a HLT) or 'limit' (max_steps instructions done).", "run_until(program, breakpoints, max_steps)", STEP + """
def run_until(program, breakpoints, max_steps):
    mem = list(program) + [0] * (256 - len(program))
    st = [0, 0, False, 0]
    steps = 0
    while steps < max_steps:
        if st[0] in breakpoints:
            return [st[0], steps, 'breakpoint']
        toy_step(mem, st)
        steps += 1
        if st[3]:
            return [st[0], steps, 'halt']
    return [st[0], steps, 'limit']
""", [[COUNTDOWN, [5], 100], [COUNTDOWN, [], 100], [COUNTDOWN, [], 3], [COUNTDOWN, [0], 10]], "Check the breakpoint before each step.", approx=None),
  PL("Trace", "Write trace(program, n): run TOY8 and return a list of up to n entries [pc, name, a] describing each executed instruction (pc before it executes, and A after it executes). Stop after executing a HLT. Names: HLT LDI ADD SUB STA LDA JMP JNZ OUT.", "trace(program, n)", STEP + """
def trace(program, n):
    mem = list(program) + [0] * (256 - len(program))
    st = [0, 0, False, 0]
    out = []
    for _ in range(n):
        pc = st[0]
        op = mem[pc]
        toy_step(mem, st)
        out.append([pc, NAMES[op], st[1]])
        if st[3]:
            break
    return out
""", [[COUNTDOWN, 6], [COUNTDOWN, 100], [[1, 9, 2, 1, 0], 10], [[], 3]], "Record before and after.", approx=None)]))
