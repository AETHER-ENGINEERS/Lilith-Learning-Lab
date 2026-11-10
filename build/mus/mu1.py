# -*- coding: utf-8 -*-
"""Music theory course, part 1: sound, notation, rhythm, intervals, scales, keys."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=680):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


NOTE_HELPER = '''
NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def note_to_midi(name):
    pc = NAMES[name[0]]
    i = 1
    while i < len(name) - 1:
        if name[i] == "#":
            pc = pc + 1
        elif name[i] == "b":
            pc = pc - 1
        i = i + 1
    octave = int(name[len(name) - 1])
    return 12 * (octave + 1) + pc
'''

CHS.append(CH(
 "Sound, pitch and the notes",
 ("Sound and notes", [
  "Sound | is | A vibration",
  "Pitch | follows | Frequency",
  "Octave | doubles | Frequency",
  "Note | names | A pitch",
  "Semitone | is | Smallest step",
  "Sharp | raises | A semitone",
  "Flat | lowers | A semitone"]),
 ["Sound is vibration. How fast something vibrates, its frequency in hertz (Hz), sets the pitch. A faster vibration sounds higher.",
  "Western music divides the octave, a doubling of frequency, into twelve equal steps called semitones. The seven white keys on a piano are the notes A to G, and the black keys are sharps or flats.",
  "Each note has a letter name and an octave number, such as C4 for middle C. Concert A, A4, is 440 Hz."],
 [("Frequency", "The number of vibrations per second, measured in hertz."),
  ("Pitch", "How high or low a note sounds, set mostly by its frequency."),
  ("Octave", "The interval between a note and the one with double its frequency."),
  ("Semitone", "The smallest step in Western music; twelve of them make an octave."),
  ("Accidental", "A sign that changes a note by a semitone: sharp (♯), flat (♭) or natural (♮).")],
 ["Pitch goes up with frequency.",
  "An octave doubles the frequency: A4 = 440 Hz, A5 = 880 Hz.",
  "12 semitones make an octave.",
  "Letter names A B C D E F G, then repeat.",
  "Sharp (♯) raises by one semitone; flat (♭) lowers by one."],
 [T("Pluck a guitar string and watch it blur. The blur is the string vibrating, many times a second. The more times, the higher the sound. A string that vibrates 440 times a second gives the note A above middle C, the pitch orchestras tune to."),
  T("Double the frequency and your ear hears the same note again, only higher. That is the octave. It is why a man and a woman can sing the same tune an octave apart, and why notes in different octaves share a letter name."),
  T("Western music cuts the octave into twelve equal steps. Each step is a semitone, and each step multiplies the frequency by the twelfth root of two, about 1.0595. On a piano, neighbouring keys, white or black, are one semitone apart."),
  T("The white keys are named A, B, C, D, E, F and G. Between most pairs of white keys sits a black key. It can be named by the note below with a sharp, as in C♯, or by the note above with a flat, as in D♭. The two names mean the same key and are called enharmonic."),
  T("There is no black key between B and C, and none between E and F. So B to C and E to F are semitones, while C to D and the other white pairs are two semitones, called a whole tone. This uneven pattern is the key to all scales."),
  T("A pitch is named by a letter and an octave number. Middle C is C4. The C above it is C5. Computers number the keys from 0 to 127 in MIDI, where middle C is 60 and A4 is 69. A frequency follows from the MIDI number with one formula: 440 times two to the power of (number minus 69) over twelve.")],
 [("How many semitones are in an octave?", ["12", "7", "8", "10"], 0, "Chromatic scale."),
  ("What is the frequency of A4?", ["440 Hz", "220 Hz", "880 Hz", "261 Hz"], 0, "Concert pitch."),
  ("Doubling the frequency gives...", ["An octave higher", "A fifth higher", "A semitone higher", "The same pitch"], 0, "Same letter name."),
  ("Which two white-key pairs are only a semitone apart?", ["E-F and B-C", "C-D and D-E", "F-G and A-B", "G-A and C-D"], 0, "No black key between them."),
  ("What does a flat do?", ["Lowers a note by a semitone", "Raises a note", "Doubles a note", "Cancels a sharp only"], 0, "♭."),
  ("What is the MIDI number of middle C?", ["60", "48", "69", "72"], 0, "C4.")],
 [("A4", "440 Hz, MIDI 69"), ("C4", "middle C, MIDI 60"), ("Semitone", "one piano key step"), ("Octave", "12 semitones, double frequency"), ("Enharmonic", "same pitch, two names, like C♯ and D♭")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Semitone", "smallest step"), ("Octave", "12 semitones"), ("Hertz", "vibrations per second"), ("♯", "raise by a semitone"), ("♭", "lower by a semitone")]),
  FILL("Pitch facts", "A higher frequency gives a higher {{pitch}}. An octave has {{12}} semitones. The note A4 is {{440}} Hz."),
  PL("Note to MIDI", "Write note_to_midi(name) for names like 'C4', 'F#3' or 'Bb2' (letter, optional # or b, octave). MIDI number = 12 x (octave + 1) + pitch class, where C=0 D=2 E=4 F=5 G=7 A=9 B=11, # adds 1 and b subtracts 1.", "note_to_midi(name)", NOTE_HELPER, [["C4"], ["A4"], ["F#3"], ["Bb2"], ["C-1" if False else "C0"], ["B5"], ["Eb4"]], "Use the table, then adjust for the accidental."),
  PL("MIDI to frequency", "Write midi_to_hz(n): 440 x 2 to the power ((n - 69) / 12), rounded to 2 decimals. Use 2 ** x with floats and round(value, 2).", "midi_to_hz(n)", '''
def midi_to_hz(n):
    return round(440.0 * (2 ** ((n - 69) / 12.0)), 2)
''', [[69], [60], [81], [57], [72], [0]], "Use the formula directly.", approx=0.01)]
))

CHS.append(CH(
 "Reading music: staff, clefs and rhythm",
 ("Notation", [
  "Staff | has | Five lines",
  "Clef | fixes | Pitches",
  "Note head | shows | Pitch",
  "Note shape | shows | Duration",
  "Time signature | sets | The beat",
  "Bar line | divides | Measures",
  "Rest | marks | Silence"]),
 ["Music is written on a staff of five lines and four spaces. A clef at the start says which pitches the lines stand for. The treble clef fixes the second line as G4, and the bass clef fixes the fourth line as F3.",
  "The shape of a note shows how long it lasts. A whole note lasts four beats in 4/4 time, a half note two, a quarter one, an eighth half a beat. Each next shape halves the value before it.",
  "The time signature at the start tells how many beats are in each measure and which note gets the beat. In 3/4 there are three quarter-note beats per measure."],
 [("Staff", "Five horizontal lines on which notes are written."),
  ("Clef", "A sign at the start of the staff that fixes the pitch of the lines."),
  ("Measure", "A group of beats between two bar lines."),
  ("Time signature", "Two numbers: beats per measure over the note value that gets one beat."),
  ("Rest", "A sign for a silence of a given length.")],
 ["Treble clef: lines E G B D F; spaces F A C E.",
  "Bass clef: lines G B D F A; spaces A C E G.",
  "Whole = 4 beats, half = 2, quarter = 1, eighth = 1/2 (in 4/4).",
  "A dot adds half the note's value.",
  "Time signature 4/4: four quarter beats per measure."],
 [T("The staff is a ladder. Every line and space is one step of the ladder. A note high on the ladder sounds high. A clef is a key to the ladder: it tells you which pitch a certain line means, and the rest follow in order."),
  T("In the treble clef, the line curled by the clef is G4. The lines from bottom to top are E, G, B, D, F, and the spaces are F, A, C, E. A rhyme helps: every good boy does fine for the lines, and FACE for the spaces. Notes above and below the staff sit on short ledger lines."),
  T("Duration is shown by shape. A hollow oval with no stem is a whole note. Add a stem and it is a half note. Fill the oval and it is a quarter note. Add a flag and it is an eighth note. Each shape lasts half as long as the one before. A dot after a note adds half its length."),
  T("Beats are grouped into measures. The time signature 4/4 says four quarter notes in each measure, and 3/4 says three. In 6/8 there are six eighth notes, usually felt as two groups of three. The top number counts beats and the bottom shows the unit."),
  T("A rest is silence with a length. It has a shape for every note value, so a whole rest, half rest and so on. In 4/4, a quarter note, a quarter rest and a half note add up to four beats, filling exactly one measure.")],
 [("How many lines does a staff have?", ["5", "4", "6", "7"], 0, "Five lines."),
  ("In 4/4 time, how many beats is a half note?", ["2", "1", "4", "3"], 0, "Half of a whole."),
  ("What does a dot after a note do?", ["Adds half its value", "Doubles it", "Halves it", "Makes it a rest"], 0, "Dotted half = 3 beats."),
  ("What does the top number of a time signature give?", ["Beats per measure", "The note value", "The tempo", "The key"], 0, "3 in 3/4."),
  ("The treble clef lines are E G B D F. What are the spaces?", ["F A C E", "G B D F", "A C E G", "E G B D"], 0, "FACE."),
  ("How many eighth notes fit in one 4/4 measure?", ["8", "4", "2", "16"], 0, "Two per beat.")],
 [("Whole note", "4 beats in 4/4"), ("Half note", "2 beats"), ("Quarter note", "1 beat"), ("Eighth note", "half a beat"), ("Dotted note", "value times one and a half")],
 [MATCH("Match the value", "Pair each note with its length in 4/4 time.", [("Whole note", "4 beats"), ("Half note", "2 beats"), ("Quarter note", "1 beat"), ("Eighth note", "1/2 beat"), ("Dotted half note", "3 beats")]),
  PL("Measure length", "Notes are given as strings: 'w' whole (4 beats), 'h' half (2), 'q' quarter (1), 'e' eighth (0.5), 's' sixteenth (0.25). A trailing '.' adds half again ('h.' is 3). Write measure_beats(notes): the total beats of the list.", "measure_beats(notes)", '''
def measure_beats(notes):
    vals = {"w": 4.0, "h": 2.0, "q": 1.0, "e": 0.5, "s": 0.25}
    total = 0.0
    for n in notes:
        v = vals[n[0]]
        if len(n) > 1 and n[1] == ".":
            v = v * 1.5
        total = total + v
    return total
''', [[["q", "q", "h"]], [["w"]], [["h.", "q"]], [["e", "e", "e", "e", "q", "h"]], [["s", "s", "e", "q", "h."]]], "Look up the base value, then handle the dot."),
  PL("Does the measure fill?", "Write fills(notes, top, bottom): True if the total beats of the notes (same codes as before) equals top x 4 / bottom, which is the measure length in quarter-note beats. For 3/4 that is 3, for 6/8 it is 3, for 4/4 it is 4.", "fills(notes, top, bottom)", '''
def fills(notes, top, bottom):
    vals = {"w": 4.0, "h": 2.0, "q": 1.0, "e": 0.5, "s": 0.25}
    total = 0.0
    for n in notes:
        v = vals[n[0]]
        if len(n) > 1 and n[1] == ".":
            v = v * 1.5
        total = total + v
    return total == top * 4.0 / bottom
''', [[["q", "q", "q"], 3, 4], [["h.", "q"], 4, 4], [["e", "e", "e", "e", "e", "e"], 6, 8], [["h", "h", "q"], 4, 4], [["q", "q"], 3, 4]], "Compare the total with top times four over bottom.")]
))

CHS.append(CH(
 "Intervals",
 ("Intervals", [
  "Interval | measures | Distance between notes",
  "Number | counts | Letter names",
  "Quality | counts | Semitones",
  "Perfect | marks | Unison fourth fifth octave",
  "Major | is | One semitone above minor",
  "Tritone | spans | Six semitones",
  "Inversion | flips | An interval"]),
 ["An interval is the distance between two notes. It has a number, counted in letter names (C up to E is a third), and a quality, found from the semitones (major, minor, perfect, augmented or diminished).",
  "Unisons, fourths, fifths and octaves come in a perfect quality. Seconds, thirds, sixths and sevenths come in major and minor.",
  "Learn the intervals by their semitone count and by a familiar song to hear them."],
 [("Interval", "The distance between two notes."),
  ("Perfect interval", "Unison, fourth, fifth or octave in their normal size."),
  ("Major and minor", "The two normal sizes of seconds, thirds, sixths and sevenths; minor is a semitone smaller."),
  ("Tritone", "An interval of six semitones, halfway through the octave."),
  ("Inversion", "Moving the lower note up an octave; intervals of n and 9 - n then swap.")],
 ["0 unison, 1 minor 2nd, 2 major 2nd, 3 minor 3rd, 4 major 3rd.",
  "5 perfect 4th, 6 tritone, 7 perfect 5th.",
  "8 minor 6th, 9 major 6th, 10 minor 7th, 11 major 7th, 12 octave.",
  "Invert: 2nd and 7th, 3rd and 6th, 4th and 5th swap.",
  "Perfect inverts to perfect; major to minor."],
 [T("To find an interval, count letter names from the lower note to the upper one, counting both ends. C to E is C, D, E, which is a third. C to G is a fifth. Then count semitones to find the quality. C to E is 4 semitones, which is a major third. C to E-flat is 3, which is a minor third."),
  T("Fourths, fifths and octaves are called perfect because they sound pure and stable. A perfect fifth is 7 semitones, a perfect fourth is 5, and an octave is 12. Make one a semitone bigger and it is augmented, a semitone smaller and it is diminished."),
  T("Seconds, thirds, sixths and sevenths are major or minor. The minor is one semitone smaller than the major. A major second is 2 semitones, a minor second 1. A major third is 4, a minor third 3. A major sixth is 9, a minor sixth 8. A major seventh is 11, a minor seventh 10."),
  T("Six semitones, halfway through the octave, is the tritone. It is either an augmented fourth or a diminished fifth. It sounds tense and wants to resolve, and was nicknamed the devil in music by medieval writers."),
  T("Turn an interval upside down by moving the lower note up an octave. The inversion of a third is a sixth, and of a fourth is a fifth. The numbers always add to nine, and the semitones to twelve. Perfect stays perfect, while major becomes minor."),
  T("Songs make useful anchors. The first two notes of the Star Wars theme is a perfect fifth. A major third is the start of 'When the Saints Go Marching In'. A minor second is the shark theme from Jaws. Pick your own song for each interval.")],
 [("What is C up to E?", ["A major third", "A minor third", "A perfect fourth", "A major second"], 0, "4 semitones."),
  ("How many semitones in a perfect fifth?", ["7", "5", "6", "8"], 0, "C to G."),
  ("What is the tritone?", ["6 semitones", "5 semitones", "7 semitones", "4 semitones"], 0, "Half an octave."),
  ("The inversion of a major third is a...", ["Minor sixth", "Major sixth", "Perfect fifth", "Minor third"], 0, "4 + 8 = 12."),
  ("Which intervals are perfect?", ["Unison, 4th, 5th, octave", "2nd, 3rd, 6th, 7th", "Only the octave", "3rd and 5th"], 0, "Pure intervals."),
  ("How many semitones in a minor third?", ["3", "4", "2", "5"], 0, "One less than a major third.")],
 [("m2", "1 semitone"), ("M3", "4 semitones"), ("P4", "5 semitones"), ("P5", "7 semitones"), ("TT", "6 semitones")],
 [APP("EAR", "Ear trainer: name the interval", "Press Play to hear two notes, then choose the interval. Get 5 right to complete this lab.", 640),
  MATCH("Match the interval", "Pair each interval with its size in semitones.", [("Minor second", "1"), ("Major third", "4"), ("Perfect fourth", "5"), ("Tritone", "6"), ("Perfect fifth", "7"), ("Octave", "12")]),
  PL("Name the interval", "Write interval_name(semitones) for 0 to 12. Return the standard name from this list: 0 'unison', 1 'minor 2nd', 2 'major 2nd', 3 'minor 3rd', 4 'major 3rd', 5 'perfect 4th', 6 'tritone', 7 'perfect 5th', 8 'minor 6th', 9 'major 6th', 10 'minor 7th', 11 'major 7th', 12 'octave'.", "interval_name(semitones)", '''
def interval_name(semitones):
    names = ["unison", "minor 2nd", "major 2nd", "minor 3rd", "major 3rd", "perfect 4th", "tritone", "perfect 5th", "minor 6th", "major 6th", "minor 7th", "major 7th", "octave"]
    return names[semitones]
''', [[0], [4], [7], [6], [11], [12], [3]], "A list lookup is enough."),
  PL("Interval between two notes", "Write semitones_between(a, b): the number of semitones from note a up to note b, where each is a name like 'C4' or 'F#3' or 'Bb2'. Use the same note numbering as MIDI: C=0 D=2 E=4 F=5 G=7 A=9 B=11, # +1, b -1, number = 12 x (octave + 1) + pitch class. Return b minus a.", "semitones_between(a, b)", NOTE_HELPER + '''
def semitones_between(a, b):
    return note_to_midi(b) - note_to_midi(a)
''', [["C4", "E4"], ["C4", "G4"], ["A3", "C5"], ["E4", "C4"], ["F#3", "C4"], ["Bb3", "D4"]], "Convert both notes, then subtract."),
  PL("Invert an interval", "Write invert(number, semitones): given an interval's number (1 to 8) and semitones (0 to 12), return [9 - number, 12 - semitones]. For a major third [3, 4] the inversion is [6, 8], a minor sixth. If the number is 1, treat it as 8.", "invert(number, semitones)", '''
def invert(number, semitones):
    if number == 1:
        number = 8
        if semitones == 0:
            semitones = 12
    return [9 - number, 12 - semitones]
''', [[3, 4], [5, 7], [2, 2], [6, 9], [4, 5], [1, 0]], "The numbers add to nine and the semitones to twelve.")]
))

CHS.append(CH(
 "Major scales and key signatures",
 ("Major scales", [
  "Scale | is | Ordered notes",
  "Major scale | follows | W W H W W W H",
  "Key | names | The tonic",
  "Key signature | lists | Sharps or flats",
  "Circle of fifths | orders | The keys",
  "Relative minor | shares | The signature",
  "Degree | has | A name"]),
 ["A scale is a ladder of notes. The major scale follows the step pattern whole, whole, half, whole, whole, whole, half. Starting on C and playing only white keys gives C major.",
  "The first note of a scale is the tonic, the home note that gives the key its name. Each scale degree has a name: tonic, supertonic, mediant, subdominant, dominant, submediant and leading tone.",
  "To play a major scale from any note, apply the same pattern. This forces some notes to be sharp or flat, and these are listed in the key signature."],
 [("Scale", "A set of notes arranged by pitch, such as the major scale."),
  ("Tonic", "The first and most important note of a key."),
  ("Key signature", "The sharps or flats at the start of the staff that apply to the whole piece."),
  ("Circle of fifths", "A diagram of the keys ordered by fifths, showing how many sharps or flats each has."),
  ("Relative minor", "The minor key that shares a key signature with a major key, starting on its sixth degree.")],
 ["Major scale pattern: W W H W W W H.",
  "Sharps in order: F C G D A E B.",
  "Flats in order: B E A D G C F.",
  "Up a fifth: add one sharp; down a fifth: add one flat.",
  "Relative minor starts on the sixth degree."],
 [T("A major scale sounds like do re mi fa so la ti do. The gaps between its notes follow a pattern of whole tones (W, two semitones) and half tones (H, one semitone): W W H W W W H. Start on C and you get all white keys, because the half steps fall at E to F and B to C."),
  T("Start on G and apply the same pattern. The step from E to F would be wrong. The pattern needs a whole tone from E up to F-sharp, so F must be raised. G major has one sharp, F-sharp. This is how key signatures arise: they fix the pattern for each starting note."),
  T("The sharps appear in a fixed order: F, C, G, D, A, E, B. Each new sharp key is a fifth above the last: C, G, D, A, E, B, F-sharp. The flats come in the reverse order: B, E, A, D, G, C, F. Each new flat key is a fifth below: F, B-flat, E-flat, A-flat and so on."),
  T("Arrange the keys in a circle by fifths and you get the circle of fifths. Going clockwise adds a sharp, going anticlockwise adds a flat. At the bottom the sharp and flat keys meet, since F-sharp major and G-flat major sound the same."),
  T("To read a key signature of sharps, take the last sharp and go up a half step: that is the major tonic. With one sharp (F-sharp) the key is G. For flats, the second last flat is the key, and with one flat the key is F. Each major key shares its signature with a relative minor, a minor third below.")],
 [("What is the major scale step pattern?", ["W W H W W W H", "W H W W H W W", "H W W H W W W", "W W W H W W H"], 0, "Do re mi fa so la ti."),
  ("How many sharps does G major have?", ["1", "2", "0", "3"], 0, "F-sharp."),
  ("Which sharp comes first in a key signature?", ["F-sharp", "C-sharp", "B-sharp", "G-sharp"], 0, "Father Charles."),
  ("What is the tonic?", ["The first note of the scale", "The fifth note", "The last note", "A rest"], 0, "Home note."),
  ("What is the relative minor of C major?", ["A minor", "E minor", "D minor", "G minor"], 0, "Sixth degree."),
  ("Which key has one flat?", ["F major", "G major", "D major", "B-flat major"], 0, "B-flat.")],
 [("C major", "no sharps or flats"), ("G major", "1 sharp: F#"), ("D major", "2 sharps: F# C#"), ("F major", "1 flat: Bb"), ("Relative minor", "6th degree of the major")],
 [APP("FIFTHS", "Circle of fifths", "Tap keys on the circle to see the scale, the sharps or flats and the relative minor. Visit 4 different keys to complete this lab.", 680),
  MATCH("Match the key", "Pair each major key with its key signature.", [("C major", "no sharps or flats"), ("G major", "F#"), ("D major", "F# C#"), ("F major", "Bb"), ("Bb major", "Bb Eb")]),
  PL("Build a major scale", "Write major_scale(tonic): given a tonic as a pitch class number 0 to 11 (C = 0), return the list of 7 pitch classes of the major scale, in order, each 0 to 11. Use the steps 2, 2, 1, 2, 2, 2 and take each note modulo 12.", "major_scale(tonic)", '''
def major_scale(tonic):
    steps = [2, 2, 1, 2, 2, 2]
    scale = [tonic % 12]
    n = tonic
    for s in steps:
        n = n + s
        scale.append(n % 12)
    return scale
''', [[0], [7], [2], [5], [10], [11]], "Add each step and wrap with modulo 12."),
  PL("How many sharps?", "Write sharps_in_key(tonic): given a major tonic as pitch class 0 to 11, return the number of sharps (positive) or flats (negative) in its key signature using the circle of fifths: go up in fifths (7 semitones) from C. Positions: C 0, G 1, D 2, A 3, E 4, B 5, F# 6, C# 7 (or Db -5), Ab -4, Eb -3, Bb -2, F -1. Use the table 0:0, 7:1, 2:2, 9:3, 4:4, 11:5, 6:6, 1:-5, 8:-4, 3:-3, 10:-2, 5:-1.", "sharps_in_key(tonic)", '''
def sharps_in_key(tonic):
    table = {"0": 0, "7": 1, "2": 2, "9": 3, "4": 4, "11": 5, "6": 6, "1": -5, "8": -4, "3": -3, "10": -2, "5": -1}
    return table[str(tonic % 12)]
''', [[0], [7], [2], [5], [10], [3], [6]], "A table lookup works; the keys are just a fifth apart."),
  PL("Relative minor", "Write relative_minor(tonic): the pitch class of the relative minor tonic, which is the sixth degree of the major scale: tonic + 9, modulo 12.", "relative_minor(tonic)", '''
def relative_minor(tonic):
    return (tonic + 9) % 12
''', [[0], [7], [5], [2], [10]], "A minor third below the major tonic is nine semitones above it.")]
))
