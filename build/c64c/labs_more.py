"""Extra BASIC and C labs for the C64 course (sprites, SID, joystick, raster, demo effects)."""

BASIC = {
 "4": ("A sprite from BASIC. The sprite data, pointer, position and colour are already set up, but the sprite is switched off. Switch it on with POKE 53269,1, then make it slide right: a FOR X loop from 60 to 250 that POKEs X into register 53248, with a short empty loop as a delay so you can watch it move.",
       '10 REM SPRITE 0 FROM BASIC\n20 FOR I=0 TO 62:POKE 832+I,255:NEXT I\n30 POKE 2040,13\n40 POKE 53248,60:POKE 53249,120\n50 POKE 53287,1\n60 REM 1) SWITCH THE SPRITE ON: POKE 53269,1\n70 REM 2) FOR X=60 TO 250 STEP 2 : POKE 53248,X\n80 REM    FOR D=1 TO 40:NEXT D : NEXT X\n90 END\n',
       [{"t": "sprite switched on with its pointer set", "spr": True}, {"t": "uses a FOR X loop to move it", "uses": "\\bFOR\\s+X\\b"}, {"t": "the sprite slid past x=160", "ramgt": [53248, 160]}]),
 "5": ("SID from BASIC. Set the volume, the envelope and a frequency, then start the note by setting the gate bit in the voice 1 control register 54276. Fill in the missing lines.",
       '10 REM A NOTE ON SID VOICE 1\n20 POKE 54296,15\n30 POKE 54277,9:POKE 54278,240\n40 POKE 54273,29:POKE 54272,69\n50 REM NOW START THE NOTE: TRIANGLE WAVE PLUS GATE IS 17\n60 END\n',
       [{"t": "SID is making a note", "sid": True}]),
 "6": ("The joystick from BASIC. Port 2 is PEEK(56320); a pressed direction reads 0 in its bit. Press the arrow buttons under the screen. Run the program, press UP, then add a line so that FIRE (bit 4, value 16) prints FIRE.",
       '10 J=PEEK(56320)\n20 IF (J AND 1)=0 THEN PRINT "UP"\n30 GOTO 10\n',
       [{"t": "UP was printed", "screen": "UP", "keep": True}, {"t": "FIRE was printed", "screen": "FIRE", "keep": True}]),
 "7": ("Colour cycling, the oldest demo trick. Cycle the border and the background through all 16 colours with a loop, in opposite directions. Then make it repeat forever with a GOTO.",
       '10 FOR I=0 TO 15\n20 POKE 53280,I\n30 NEXT I\n40 END\n',
       [{"t": "border changes", "border": True}, {"t": "background changes", "bg": True}, {"t": "uses GOTO to repeat", "uses": "GOTO"}]),
 "8": ("A text scroller in BASIC. MID$ takes a window out of a string, and CHR$(19) puts the cursor home. Run it, then change the text and make the window wider.",
       '10 T$="    HELLO DEMO WORLD    "\n20 PRINT CHR$(147)\n30 FOR S=1 TO LEN(T$)-12\n40 PRINT CHR$(19);MID$(T$,S,12)\n50 NEXT S\n60 END\n',
       [{"t": "the scroller ran", "ran": True}, {"t": "uses MID$", "uses": "MID\\$"}, {"t": "the end of the text is on screen", "screen": "WORLD"}]),
}

C = {
 "c_sprite": ("A sprite from C. This sets up sprite 0 as a box. Run it, then add a second sprite: copy the pointer, position and colour lines for sprite 1 (pointer at 2041, X at 53250, Y at 53251, colour at 53288) and enable both with 3 (change the mask at 49408 too).",
   '#include <stdio.h>\n#include <peekpoke.h>\n\nint main(void) {\n    unsigned char i;\n    printf("SPRITES\\n");\n    for (i = 0; i < 63; i++) POKE(832U + i, 255);\n    POKE(2040U, 13);\n    POKE(53248U, 120);\n    POKE(53249U, 120);\n    POKE(53287U, 1);\n    POKE(53269U, 1);   /* enable sprite 0 */\n    POKE(49408U, 1);   /* note for the checker: sprite mask */\n    return 0;\n}\n',
   [{"t": "sprite 0 points at block 13", "ram": [2040, 13]}, {"t": "both sprites are enabled", "ram": [49408, 3]}, {"t": "sprites are visible", "colors": 3}]),
 "c_sid": ("A note from C. Run it, then change the waveform to a pulse wave (64) plus the gate (1) = 65 in the control register 54276 (and in the note at 49409), so you hear a different timbre.",
   '#include <stdio.h>\n#include <peekpoke.h>\n\nint main(void) {\n    printf("SID\\n");\n    POKE(54296U, 15);   /* volume */\n    POKE(54277U, 9);    /* attack/decay */\n    POKE(54278U, 240);  /* sustain/release */\n    POKE(54273U, 29);   /* frequency high */\n    POKE(54272U, 69);   /* frequency low */\n    POKE(54276U, 17);   /* triangle + gate */\n    POKE(49409U, 17);   /* note for the checker: control value */\n    return 0;\n}\n',
   [{"t": "SID produces sound", "sound": True}, {"t": "pulse wave plus gate is set", "ram": [49409, 65]}]),
 "c_joy": ("The joystick from C. The loop mirrors port 2 into $C100 (49408) and prints UP when bit 0 is 0. Press UP, then add a test for LEFT (bit 2, value 4) that prints LEFT.",
   '#include <stdio.h>\n#include <peekpoke.h>\n\nint main(void) {\n    unsigned char j;\n    for (;;) {\n        j = PEEK(56320U);\n        POKE(49408U, j);\n        if ((j & 1) == 0) printf("UP\\n");\n    }\n    return 0;\n}\n',
   [{"t": "UP was printed", "screen": "UP"}, {"t": "LEFT was printed", "screen": "LEFT"}]),
 "c_sine": ("A sine wave in C. A table of 16 precomputed values moves sprite 0 left and right, once per frame. Run it, then double the amplitude by changing the table.",
   '#include <stdio.h>\n#include <peekpoke.h>\n\nstatic const signed char sine[16] = {0, 24, 45, 59, 64, 59, 45, 24, 0, -24, -45, -59, -64, -59, -45, -24};\n\nint main(void) {\n    unsigned char i, k = 0;\n    printf("SINE\\n");\n    for (i = 0; i < 63; i++) POKE(832U + i, 255);\n    POKE(2040U, 13);\n    POKE(53249U, 140);\n    POKE(53287U, 1);\n    POKE(53269U, 1);\n    for (;;) {\n        POKE(53248U, 150 + sine[k]);\n        POKE(49408U, 150 + sine[k]);\n        k = (k + 1) & 15;\n        while (PEEK(53266U) != 255) ;\n        while (PEEK(53266U) == 255) ;\n    }\n    return 0;\n}\n',
   [{"t": "sprite is set up", "ram": [2040, 13]}, {"t": "the sprite swings right past x=170", "ramgt": [49408, 170]}]),
}

ASM = {
 "bars": ("Raster bars, assembly style. The program waits for raster line 100, then sets the border and background to a new colour on each of the next 8 lines. Change the colour table to make a different bar.",
   '; raster bars: one colour per raster line\n*=$C000\nloop: lda $d012\n      cmp #100\n      bne loop\n      ldx #0\nbar:  lda cols,x\n      ldy $d012\nw:    cpy $d012\n      beq w          ; wait for the next line\n      sta $d020\n      sta $d021\n      inx\n      cpx #8\n      bne bar\n      lda #14\n      sta $d020\n      lda #6\n      sta $d021\n      inc $c100\n      jmp loop\ncols: .byte 2,10,7,1,7,10,2,0\n',
   [{"t": "the effect loop is running", "ramnz": 49408}, {"t": "colour bars are on screen", "colors": 3}]),
}
