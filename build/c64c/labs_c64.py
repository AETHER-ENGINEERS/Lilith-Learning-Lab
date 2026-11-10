"""Lab definitions for the C64 course: (name, tabs, source, goals, description)."""
LABS = {}

LABS["hello"] = ("Assemble this small program and run it on the emulated C64. It colours the border red and the background green. The first line, *=$C000, says where it goes in memory.",
 {"asm": """; colour the border and the background
*=$C000
      lda #2        ; red
      sta $d020     ; border colour register
      lda #5        ; green
      sta $d021     ; background colour register
      rts
"""}, [{"t": "border colour changed", "border": True}, {"t": "background colour changed", "bg": True}])

LABS["screen"] = ("Screen RAM starts at $0400 and colour RAM at $D800. This program pokes the word HELLO into both. Run it, then change the row, the column or the colour.",
 {"asm": """; put HELLO on screen row 10, column 10 in white
*=$C000
      ldx #0
loop: lda msg,x
      sta $0400+410,x     ; 10*40+10 = 410
      lda #1               ; white
      sta $d800+410,x
      inx
      cpx #5
      bne loop
      rts
msg:  .byte 8,5,12,12,15   ; screen codes for H E L L O
"""}, [{"t": "HELLO appears on screen", "screen": "HELLO"}])

LABS["loop"] = ("A loop that never ends: it adds one to the border colour register over and over, so the border flickers through all 16 colours. Run it and watch. Then try dec instead of inc.",
 {"asm": """; flicker the border forever
*=$C000
loop: inc $d020
      jmp loop
"""}, [{"t": "program is running its loop", "pc": [49152, 49160]}, {"t": "border colour changed", "border": True}])

LABS["kernal"] = ("The KERNAL is a set of ready-made routines in ROM. CHROUT at $FFD2 prints the character in A. This program prints a string by calling it in a loop until it finds a zero byte.",
 {"asm": """; print a string with CHROUT
*=$C000
      ldx #0
loop: lda msg,x
      beq done
      jsr $ffd2
      inx
      bne loop
done: rts
msg:  .text "HELLO FROM ASM"
      .byte 13,0
"""}, [{"t": "text printed", "screen": "HELLO FROM ASM"}])

LABS["sprite"] = ("A sprite is a 24 by 21 picture you can move freely. Its 63 bytes live in RAM, a pointer at $07F8 says which 64-byte block, and VIC-II registers set position, colour and enable. This program draws a white box sprite.",
 {"asm": """; sprite 0: a box
*=$C000
      ldx #0
cp:   lda spr,x
      sta $0340,x          ; sprite data at $0340 = block 13
      inx
      cpx #63
      bne cp
      lda #13
      sta $07f8            ; sprite 0 pointer
      lda #120
      sta $d000            ; x position
      lda #120
      sta $d001            ; y position
      lda #1
      sta $d027            ; colour white
      sta $d015            ; enable sprite 0
      rts
spr:  .byte $ff,$ff,$ff
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $80,$00,$01
      .byte $ff,$ff,$ff
"""}, [{"t": "sprite pointer set", "ram": [2040, 13]}, {"t": "sprite visible on screen", "colors": 3}])

LABS["sid"] = ("The SID chip makes sound. Set the volume, the attack-decay and sustain-release envelope, a frequency, and then start a voice by turning its gate bit on. This plays A above middle C (440 Hz) as a triangle wave. Click the picture first to allow sound.",
 {"asm": """; one note on SID voice 1
*=$C000
      lda #15
      sta $d418      ; volume 15
      lda #$09
      sta $d405      ; attack 0, decay 9
      lda #$f0
      sta $d406      ; sustain 15, release 0
      lda #$1d
      sta $d401      ; frequency high byte
      lda #$45
      sta $d400      ; frequency low byte (0x1D45 = 440 Hz on PAL)
      lda #$11
      sta $d404      ; triangle wave + gate on
      rts
"""}, [{"t": "SID produces sound", "sound": True}])

LABS["irq"] = ("An interrupt runs your code at the right moment without a polling loop. This program asks the VIC-II for a raster interrupt every frame. The handler adds to the border colour and counts in $C100.",
 {"asm": """; raster interrupt
*=$C000
      sei
      lda #<irq
      sta $0314        ; KERNAL IRQ vector
      lda #>irq
      sta $0315
      lda #$7f
      sta $dc0d        ; stop CIA 1 interrupts
      lda #$01
      sta $d01a        ; enable the raster interrupt
      lda #$80
      sta $d012        ; at raster line 128
      lda $d011
      and #$7f
      sta $d011
      cli
      rts
irq:  inc $d020
      inc $c100         ; count interrupts
      lda #$ff
      sta $d019         ; acknowledge
      pla
      tay
      pla
      tax
      pla
      rti
"""}, [{"t": "the handler has run", "ramnz": 49408}, {"t": "border colour changed", "border": True}])

LABS["joy"] = ("Joystick port 2 appears at $DC00. Five bits are active low: a pressed direction reads 0. This program keeps copying $DC00 to $C100. Use the pad (or arrow keys with the checkbox) to press UP, then FIRE.",
 {"asm": """; mirror joystick port 2 into $C100
*=$C000
loop: lda $dc00
      sta $c100
      jmp loop
"""}, [{"t": "UP pressed (bit 0 is 0)", "ramlow": [49408, 31, 30]}, {"t": "FIRE pressed (bit 4 is 0)", "ramlow": [49408, 31, 15]}])

LABS["project"] = ("Final project: move a sprite with the joystick. The program loops forever, adds to the x position for RIGHT and subtracts for LEFT. Press RIGHT a few times, then change it to move up and down as well.",
 {"asm": """; joystick-controlled sprite
*=$C000
      ldx #0
cp:   lda spr,x
      sta $0340,x
      inx
      cpx #63
      bne cp
      lda #13
      sta $07f8
      lda #100
      sta $c101
      sta $d001
      lda #7
      sta $d027
      lda #1
      sta $d015
loop: lda $dc00
      and #$08          ; bit 3 = right
      bne chkl
      inc $c101
chkl: lda $dc00
      and #$04          ; bit 2 = left
      bne show
      dec $c101
show: lda $c101
      sta $d000
      ldx #200
dl:   dex
      bne dl
      jmp loop
spr:  .byte $00,$7e,$00
      .byte $01,$ff,$80
      .byte $03,$ff,$c0
      .byte $07,$ff,$e0
      .byte $0f,$ff,$f0
      .byte $0f,$ff,$f0
      .byte $0f,$ff,$f0
      .byte $0f,$ff,$f0
      .byte $07,$ff,$e0
      .byte $03,$ff,$c0
      .byte $01,$ff,$80
      .byte $00,$7e,$00
      .byte $00,$00,$00
      .byte $00,$00,$00
      .byte $00,$00,$00
      .byte $00,$00,$00
      .byte $00,$00,$00
      .byte $00,$00,$00
      .byte $00,$00,$00
      .byte $00,$00,$00
      .byte $00,$00,$00
"""}, [{"t": "sprite is on screen", "ram": [2040, 13]}, {"t": "you moved it right", "ramgt": [49409, 110]}])

LABS["c"] = ("Real C on a real C64: this uses the cc65 compiler, assembler and linker running inside the app. Press Build and run. The first time it unpacks the toolchain. Change the message, the border colour, or add a loop.",
 {"c": """#include <stdio.h>
#include <peekpoke.h>

int main(void) {
    int i;
    printf("HELLO FROM C\\n");
    for (i = 0; i < 3; i++) {
        printf("LINE %d\\n", i);
    }
    POKE(53280U, 5);   /* border green */
    return 0;
}
""", "asm": """*=$C000
      lda #2
      sta $d020
      rts
"""}, [{"t": "program printed text", "screen": "HELLO FROM C"}, {"t": "border colour changed", "border": True}])
