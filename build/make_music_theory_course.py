#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Music Theory course. Usage: python3 make_music_theory_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mus"))
import cmk, mu1, mu2, make_apps  # noqa: E402
make_apps.main()
CHS = mu1.CHS + mu2.CHS
PRONOUNCE = {"semitone": "sem ee tone", "semitones": "sem ee tones", "enharmonic": "en har mon ik", "tritone": "try tone", "Aeolian": "ee oh lee an", "Ionian": "eye oh nee an", "Dorian": "door ee an",
    "Phrygian": "frij ee an", "Lydian": "lid ee an", "Mixolydian": "mix oh lid ee an", "Locrian": "low cree an", "pentatonic": "pen ta ton ik", "solfege": "sol fezh", "diatonic": "die uh ton ik",
    "subdominant": "sub dom in ant", "supertonic": "soo per ton ik", "mediant": "mee dee ant", "submediant": "sub mee dee ant", "cadence": "kay dens", "counterpoint": "count er point",
    "syncopation": "sin kuh pay shun", "rondo": "ron doh", "fugue": "fyoog", "motif": "mo teef", "Hz": "hertz", "MIDI": "middy", "Bach": "bock", "minuet": "min you et"}
SANDBOX = cmk.terminal("Music theory cheat sheet", "mus>", "A scripted lookup. Try: major, minor, triads, sevenths, intervals, fifths", [
    ("major", ["Major scale steps: W W H W W W H. C major: C D E F G A B"]),
    ("minor", ["Natural minor: W H W W H W W. A minor: A B C D E F G"]),
    ("triads", ["Major 0 4 7 | minor 0 3 7 | diminished 0 3 6 | augmented 0 4 8"]),
    ("sevenths", ["maj7 0 4 7 11 | 7 0 4 7 10 | m7 0 3 7 10 | m7b5 0 3 6 10"]),
    ("intervals", ["0 unison | 1 m2 | 2 M2 | 3 m3 | 4 M3 | 5 P4 | 6 TT | 7 P5 | 8 m6 | 9 M6 | 10 m7 | 11 M7 | 12 octave"]),
    ("fifths", ["Sharps: F C G D A E B. Flats: B E A D G C F. Up a fifth adds a sharp."]),
])
EXAM = [
 ("How many semitones in an octave?", ["12", "7", "8", "10"], 0, "Chromatic scale."),
 ("What is A4 in hertz?", ["440", "220", "880", "261"], 0, "Concert pitch."),
 ("Doubling the frequency gives...", ["An octave higher", "A fifth higher", "A semitone higher", "The same note"], 0, "Same letter name."),
 ("How many lines does a staff have?", ["5", "4", "6", "7"], 0, "Five."),
 ("In 4/4 time, a half note lasts...", ["2 beats", "1 beat", "4 beats", "3 beats"], 0, "Half a whole."),
 ("A dot after a note adds...", ["Half its value", "Its full value", "A quarter of it", "Nothing"], 0, "Dotted half = 3."),
 ("C up to E is...", ["A major third", "A minor third", "A perfect fourth", "A major second"], 0, "4 semitones."),
 ("A perfect fifth has how many semitones?", ["7", "5", "6", "8"], 0, "C to G."),
 ("The tritone is...", ["6 semitones", "5 semitones", "7 semitones", "4 semitones"], 0, "Half an octave."),
 ("The major scale pattern is...", ["W W H W W W H", "W H W W H W W", "H W W H W W W", "W W W H W W H"], 0, "Do re mi."),
 ("How many sharps does G major have?", ["1", "2", "0", "3"], 0, "F sharp."),
 ("The relative minor of C major is...", ["A minor", "D minor", "E minor", "G minor"], 0, "Sixth degree."),
 ("Which mode equals natural minor?", ["Aeolian", "Ionian", "Lydian", "Locrian"], 0, "6th degree."),
 ("Harmonic minor raises...", ["The 7th degree", "The 3rd degree", "The 2nd degree", "The 5th degree"], 0, "A leading tone."),
 ("A major triad has semitones...", ["0 4 7", "0 3 7", "0 3 6", "0 4 8"], 0, "Major third then minor."),
 ("A minor triad has semitones...", ["0 3 7", "0 4 7", "0 3 6", "0 4 8"], 0, "Minor third then major."),
 ("The triad on the 7th degree of a major scale is...", ["Diminished", "Major", "Minor", "Augmented"], 0, "B D F."),
 ("A dominant seventh chord has semitones...", ["0 4 7 10", "0 4 7 11", "0 3 7 10", "0 3 6 10"], 0, "G7."),
 ("E G C is...", ["C major, first inversion", "C major, root position", "C minor", "E minor"], 0, "Third in the bass."),
 ("V to I is a...", ["Authentic cadence", "Plagal cadence", "Half cadence", "Deceptive cadence"], 0, "Full stop."),
 ("IV to I is a...", ["Plagal cadence", "Authentic cadence", "Half cadence", "Deceptive cadence"], 0, "Amen."),
 ("I-V-vi-IV in C is...", ["C G Am F", "C F G C", "Am F C G", "C Dm G C"], 0, "Pop loop."),
 ("What is syncopation?", ["Stress on weak beats", "A very slow tempo", "A key change", "A rest"], 0, "Off-beat."),
 ("What does ABA describe?", ["Ternary form", "Binary form", "A rondo", "A fugue"], 0, "A returns."),
 ("Transposing a melody means...", ["Shifting every note by the same interval", "Changing the rhythm", "Removing notes", "Adding a bass"], 0, "Same tune, new pitch."),
 ("A B-flat clarinet sounds...", ["A whole tone lower than written", "A fifth higher", "As written", "An octave higher"], 0, "Transposing instrument."),
]
CFG = dict(id="music-theory", title="Music Theory",
    subtitle="Notes, scales, chords and harmony from the ground up, with Python labs, an ear trainer and a circle of fifths",
    description="A beginner-friendly course in Western music theory: pitch and notes, reading the staff and rhythm, intervals, major and minor scales and modes, key signatures, triads and seventh chords, inversions, Roman numeral harmony and cadences, melody, form, transposition and writing a simple song. Python labs build scales and chords from numbers; an interactive ear trainer and a circle of fifths let you hear and see the ideas.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="mus", apps={"__EAR__": "ear.html", "__FIFTHS__": "fifths.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "music-theory.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
