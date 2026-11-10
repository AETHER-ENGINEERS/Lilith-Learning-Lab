"""Commodore 64 course, chapter 17: demo coding. Original text."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *
from cb1 import EMU, BAS

D = []

D.append(CH(
 "Demo coding",
 ("Demos", ["Demo | shows off | The machine", "Raster bar | changes | Colour per line", "Scroller | moves | Text", "Sine table | gives | Smooth motion", "Raster IRQ | times | Every effect", "Music | plays from | An IRQ"]),
 ["A demo is a program with no purpose except to impress: moving graphics, effects and music, squeezed out of old hardware by tricks its designers never planned for. Making them is called demo coding, and it grew into the demoscene.",
  "A few ideas build almost every C64 effect: change a register at an exact raster line, use a precomputed sine table for smooth motion, move text with the hardware scroll register, and drive everything from a raster interrupt that fires once per frame.",
  "This chapter walks through those ideas with working labs in BASIC, assembly and C, and ends with a plan for a small demo of your own."],
 [("Demoscene", "A computer-art subculture that makes demos, intros and music for the fun and the prestige."), ("Raster bar", "A band of colour made by changing the border or background colour on successive scan lines."), ("Scroller", "Text that slides across the screen, usually using the fine scroll register $D016."), ("Sine table", "A list of precomputed sine values, read by index so that no maths is needed at run time."), ("Badline", "A raster line where the VIC steals about 40 cycles from the CPU to fetch character data."), ("Cycle counting", "Planning code by the exact number of CPU cycles each instruction takes.")],
 ["A PAL frame is 19656 cycles; a raster line is 63.", "Do the heavy work in tables, not in the effect loop.", "Time effects to the raster beam, not to delay loops.", "Music is played by calling a player routine once per frame.", "Start simple: one effect, then another, then join them into parts."],
 [T("A demo is a showcase. It began with crackers who added a short animated screen, a cracktro, to the games they copied. Soon the screens mattered more than the games, and people began writing programs only for the effects. Groups formed, parties were held where groups competed, and the best Commodore 64 demos made the machine do things its designers said it could not: more than eight sprites, graphics in the border, and music with filters that sounded like a studio synthesiser."),
  T("Nearly everything rests on the raster beam. The video chip draws the picture one scan line at a time, 312 lines per PAL frame and 63 cycles per line, 50 times a second. The register at $D012 tells you which line is being drawn. If you change the border colour when the beam is on line 100 and again on line 108, you have drawn an eight-line coloured bar. A raster bar is the simplest demo effect and the first lesson in timing."),
  C("; one colour per raster line\nbar:  lda cols,x\n      ldy $d012\nw:    cpy $d012\n      beq w        ; wait until the line number changes\n      sta $d020    ; border\n      sta $d021    ; background\n      inx\n      cpx #8\n      bne bar"),
  T("Sine tables give smooth motion. Computing a sine on a one-megahertz 8-bit processor takes far too long, so demo coders compute 256 values once, on the host computer or when the program starts, and store them in a page of memory. Reading the next value is a single load instruction. A sprite that follows the table moves in a wave. Add the table to both its x and y positions and you get circles. Offset a second table and you get lissajous curves. The same trick drives bouncing scrollers and plasma."),
  M(r"y_i=\text{centre}+\text{amp}\times\sin\!\left(\frac{2\pi i}{n}\right)"),
  T("A scroller uses the fine scroll register. The low three bits of $D016 shift the whole screen by up to seven pixels to the left. When it wraps, you move every character on the row one cell to the left, add the next letter of your text on the right, and reset the register. That gives a smooth scroll at 50 frames per second without moving much data. In BASIC you cannot reach that speed, but the idea of a window sliding along a string is the same, and MID$ gives it to you."),
  T("Timing matters. A frame has 19656 cycles on a PAL machine, and the video chip steals about forty cycles on every eighth line, the badlines. A good demo plans its cycles: how much time the music player takes, how much each effect takes, and what is left. Effects that change registers mid-line need a stable raster, achieved by clever interrupt tricks, because an ordinary interrupt arrives a few cycles late and a different number each time, so the bar edges would wobble."),
  C("; the structure of most C64 demos\ninit:   set up screen, sprites, tables\n        install a raster interrupt\nmain:   (idle, or run the part-switch logic)\n\nirq:    play the music            ; once per frame\n        run the effect for this part\n        acknowledge the interrupt, return"),
  T("Beyond the basics there is a whole toolbox. Sprite multiplexing reuses the eight hardware sprites at different screen heights to show many more. Opening the border uses a timed write to $D011 to stop the video chip from drawing the border, so sprites and graphics can appear in what is normally empty space. Flexible line interpretation, FLI, forces a new colour fetch on every line for richer pictures. Cruncher programs such as Exomizer shrink the finished demo so that it loads fast. Tools like GoatTracker and SID-Wizard write the music. And CSDb, the C64 Scene Database, lists thousands of releases you can study.")
  ,
  T("The labs below start tiny. In BASIC you cycle colours and make a text scroller, in assembly you draw raster bars, and in C you make a sprite swing along a sine wave. Change the numbers, break them and fix them, and you are doing exactly what demo coders do.")],
 [("What is a raster bar?", ["Colour changes on successive scan lines", "A bar of text", "A loading bar", "A kind of sprite"], 0, "It comes from timing a register write to the beam."), ("Why use a sine table?", ["Reading beats calculating on a slow CPU", "SID requires it", "It saves disk space", "BASIC needs it"], 0, "Precomputed values make motion cheap."), ("Which register gives smooth horizontal scrolling?", ["$D016", "$D020", "$D418", "$DC00"], 0, "Its low three bits shift the screen."), ("How often is the music player usually called?", ["Once per frame", "Once per second", "Once per byte", "Only at the start"], 0, "From the raster interrupt."), ("What is a badline?", ["A line where the VIC steals CPU cycles", "An error in a program", "A broken sprite", "A bad tape block"], 0, "About forty cycles are taken.")],
 [("What is the demoscene?", "A subculture that makes demos and intros for fun and prestige."), ("Cycles in a PAL frame?", "19656, which is 312 lines of 63."), ("What does the music routine need?", "To be called once per frame."), ("Where do you find C64 demos?", "CSDb, the C64 Scene Database."), ("What shifts the screen by pixels?", "The scroll bits of $D016.")],
 [PL("Make a sine table", "Write sine_table(n, amp, centre): a list of n integers, where entry i is centre plus amp times the sine of 2 pi i / n, rounded to the nearest integer. For n = 8, amp = 10, centre = 100 the table swings between 90 and 110.", "sine_table(n, amp, centre)",
"""import math


def sine_table(n, amp, centre):
    out = []
    for i in range(n):
        out.append(int(round(centre + amp * math.sin(2 * math.pi * i / n))))
    return out
""", [[8, 10, 100], [16, 64, 150], [4, 1, 0], [32, 100, 128]], "Use math.sin and round each value."),
  PL("A scroller window", "Write window(text, width, step): the characters a scroller shows after step moves. The text is treated as a ring, so it wraps around. Return width characters starting at position step modulo the length of the text.", "window(text, width, step)",
"""def window(text, width, step):
    n = len(text)
    start = step % n
    out = ''
    for i in range(width):
        out += text[(start + i) % n]
    return out
""", [["HELLO DEMO ", 5, 0], ["HELLO DEMO ", 5, 8], ["AB", 5, 1], ["ABC", 3, 300]], "Index with the remainder after dividing by the length."),
  PL("Raster bar colours", "Write bar_colours(colours, start, height): the colour for each raster line in a screen of height lines, where the bar uses the colours in order, one per line, starting at line start. Other lines have colour -1. Return a list of height numbers.", "bar_colours(colours, start, height)",
"""def bar_colours(colours, start, height):
    out = []
    for line in range(height):
        k = line - start
        if 0 <= k < len(colours):
            out.append(colours[k])
        else:
            out.append(-1)
    return out
""", [[[2, 10, 7], 2, 8], [[1], 0, 3], [[2, 10], 5, 6], [[], 0, 2]], "Subtract the start line and check that the offset is inside the list."),
  BAS("7", "BASIC lab: colour cycling", "Cycle the border and background through the colours, then repeat forever.", 930),
  BAS("8", "BASIC lab: a text scroller", "Slide a window along a string with MID$.", 930),
  EMU("bars", "Assembly lab: raster bars", "One colour per raster line, timed to the beam.", 930),
  EMU("c_sine", "C lab: sprite on a sine wave", "A precomputed sine table moves a sprite smoothly.", 1250)]))
