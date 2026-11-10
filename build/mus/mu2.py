# -*- coding: utf-8 -*-
"""Music theory course, part 2: minor and modes, chords, harmony, form, practice."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "Minor scales and modes",
 ("Minor and modes", [
  "Natural minor | follows | W H W W H W W",
  "Harmonic minor | raises | The seventh",
  "Melodic minor | raises | Sixth and seventh going up",
  "Mode | starts | On another degree",
  "Dorian | has | Raised sixth",
  "Mixolydian | has | Flat seventh",
  "Pentatonic | has | Five notes"]),
 ["The natural minor scale follows the step pattern whole, half, whole, whole, half, whole, whole. It sounds darker than major because of its lowered third, sixth and seventh.",
  "The harmonic minor raises the seventh degree to make a stronger pull to the tonic. The melodic minor raises the sixth and seventh going up and uses natural minor coming down.",
  "A mode is a scale built by starting the major scale on a different degree. The seven modes are Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian and Locrian."],
 [("Natural minor", "A scale with the pattern W H W W H W W; also called the Aeolian mode."),
  ("Harmonic minor", "Natural minor with a raised seventh degree."),
  ("Melodic minor", "A scale that raises the sixth and seventh when ascending."),
  ("Mode", "A scale made by starting a parent scale on a different note."),
  ("Pentatonic scale", "A five-note scale found in folk, blues and rock music.")],
 ["Natural minor: W H W W H W W.",
  "Harmonic minor: raise the 7th.",
  "Modes start on degrees 1 to 7 of the major scale: Ionian Dorian Phrygian Lydian Mixolydian Aeolian Locrian.",
  "Major pentatonic: 1 2 3 5 6.",
  "Minor pentatonic: 1 b3 4 5 b7."],
 [T("Play the white keys from A to A. That is A natural minor. It uses the same notes as C major but starts on the sixth degree, so A minor is the relative minor of C major. Its third degree is C, a minor third above the tonic, and that minor third gives the scale its sad colour."),
  T("Natural minor has no half step leading up to the tonic. That makes the end feel weak. The harmonic minor raises the seventh degree by a semitone, giving a leading tone. In A harmonic minor the G becomes G-sharp. This leaves an awkward gap, an augmented second, between the sixth and seventh degrees."),
  T("The melodic minor smooths the gap by raising both the sixth and seventh degrees when going up, F-sharp and G-sharp in A minor. Coming down, it returns to natural minor. Jazz musicians often use the ascending form in both directions."),
  T("Every major scale gives seven modes, one for each starting degree. Starting on the 2nd gives Dorian, the 3rd Phrygian, the 4th Lydian, the 5th Mixolydian, the 6th Aeolian and the 7th Locrian. Dorian is minor with a bright sixth. Mixolydian is major with a flat seventh, the sound of a lot of rock."),
  T("A pentatonic scale leaves out the notes that clash. Major pentatonic is 1 2 3 5 6, as in C D E G A. Minor pentatonic is 1 flat3 4 5 flat7. With only five notes, every combination sounds good together, which is why guitarists start there.")],
 [("What is the relative minor of C major?", ["A minor", "D minor", "E minor", "G minor"], 0, "Sixth degree."),
  ("What does harmonic minor change?", ["Raises the 7th", "Lowers the 3rd", "Raises the 2nd", "Lowers the 5th"], 0, "A leading tone."),
  ("Which mode starts on the 2nd degree of the major scale?", ["Dorian", "Lydian", "Phrygian", "Aeolian"], 0, "D to D on white keys."),
  ("How many notes are in a pentatonic scale?", ["5", "7", "6", "8"], 0, "Penta means five."),
  ("Which mode is the same as natural minor?", ["Aeolian", "Ionian", "Lydian", "Locrian"], 0, "6th degree."),
  ("Which mode is the same as major?", ["Ionian", "Dorian", "Aeolian", "Phrygian"], 0, "1st degree.")],
 [("Aeolian", "natural minor"), ("Ionian", "major"), ("Dorian", "minor with raised 6th"), ("Mixolydian", "major with flat 7th"), ("Lydian", "major with raised 4th")],
 [MATCH("Match the mode", "Pair each mode with the degree of the major scale where it starts.", [("Ionian", "1st"), ("Dorian", "2nd"), ("Phrygian", "3rd"), ("Lydian", "4th"), ("Mixolydian", "5th"), ("Aeolian", "6th"), ("Locrian", "7th")]),
  PL("Build a minor scale", "Write minor_scale(tonic, kind): tonic is a pitch class 0 to 11, kind is 'natural' or 'harmonic'. Return the 7 pitch classes. Natural minor steps are 2, 1, 2, 2, 1, 2 from the tonic. Harmonic minor is natural with the seventh note raised by one semitone (mod 12).", "minor_scale(tonic, kind)", '''
def minor_scale(tonic, kind):
    steps = [2, 1, 2, 2, 1, 2]
    scale = [tonic % 12]
    n = tonic
    for s in steps:
        n = n + s
        scale.append(n % 12)
    if kind == "harmonic":
        scale[6] = (scale[6] + 1) % 12
    return scale
''', [[9, "natural"], [9, "harmonic"], [0, "natural"], [4, "harmonic"], [2, "natural"]], "Build natural minor first, then adjust the last note."),
  PL("Build a mode", "Write mode(tonic, degree): the 7 pitch classes of the mode that starts on the given degree (1 to 7) of the MAJOR scale of the given tonic (pitch class 0 to 11). First build the major scale with steps 2, 2, 1, 2, 2, 2, then rotate it to start from the chosen degree. Return the list.", "mode(tonic, degree)", '''
def mode(tonic, degree):
    steps = [2, 2, 1, 2, 2, 2]
    scale = [tonic % 12]
    n = tonic
    for s in steps:
        n = n + s
        scale.append(n % 12)
    out = []
    for i in range(7):
        out.append(scale[(degree - 1 + i) % 7])
    return out
''', [[0, 1], [0, 2], [0, 6], [2, 5], [7, 4], [0, 7]], "Rotate the list by degree minus one."),
  PL("Pentatonic", "Write pentatonic(tonic, kind): pitch classes of the pentatonic scale. 'major' uses semitone offsets [0, 2, 4, 7, 9] from the tonic and 'minor' uses [0, 3, 5, 7, 10]. Return each as (tonic + offset) % 12.", "pentatonic(tonic, kind)", '''
def pentatonic(tonic, kind):
    if kind == "major":
        offs = [0, 2, 4, 7, 9]
    else:
        offs = [0, 3, 5, 7, 10]
    return [(tonic + o) % 12 for o in offs]
''', [[0, "major"], [9, "minor"], [7, "major"], [4, "minor"]], "Pick the offsets, then add the tonic.")]
))

CHS.append(CH(
 "Chords: triads",
 ("Triads", [
  "Chord | has | Three or more notes",
  "Triad | stacks | Two thirds",
  "Major triad | is | Major third plus minor third",
  "Minor triad | is | Minor third plus major third",
  "Diminished | stacks | Two minor thirds",
  "Augmented | stacks | Two major thirds",
  "Root | names | The chord"]),
 ["A chord is three or more notes sounded together. The simplest is the triad, made by stacking two thirds on a root: the root, the third and the fifth.",
  "The quality depends on the thirds. A major triad is a major third then a minor third, 4 + 3 semitones. A minor triad is 3 + 4. A diminished triad is 3 + 3, and an augmented triad is 4 + 4.",
  "Building a triad on each degree of a major scale gives three major, three minor and one diminished triad."],
 [("Chord", "Three or more notes played together."),
  ("Triad", "A three-note chord of root, third and fifth."),
  ("Root", "The note a chord is built on and named after."),
  ("Chord quality", "Whether a triad is major, minor, diminished or augmented."),
  ("Diatonic", "Using only the notes of the key.")],
 ["Major triad: 0 4 7. Minor: 0 3 7.",
  "Diminished: 0 3 6. Augmented: 0 4 8.",
  "In a major key: I ii iii IV V vi vii-dim.",
  "Major chords sound bright; minor chords sound sad.",
  "Chord symbols: C, Cm, Cdim, Caug."],
 [T("Build a chord by skipping notes. Take C, skip D, take E, skip F, take G. That gives C, E and G, a C major triad. The bottom note is the root, the next the third, the top the fifth. Stacking in thirds is the heart of Western harmony."),
  T("The sizes of the two thirds set the colour. Major triad: a major third (4 semitones) below a minor third (3). C E G. Minor triad: swap them, a minor third below a major third. C E-flat G. That single lowered note turns bright to sad."),
  T("Two odd triads complete the set. Stack two minor thirds, C E-flat G-flat, and you have a diminished triad, tense and unstable. Stack two major thirds, C E G-sharp, and you have an augmented triad, dreamlike and unsettled."),
  T("Now build a triad on every degree of C major using only its own notes. C E G is major. D F A is minor. E G B is minor. F A C is major. G B D is major. A C E is minor. B D F is diminished. The pattern is I, ii, iii, IV, V, vi, vii-diminished. Big letters mean major."),
  T("Chord symbols write all this down. C means C major, Cm or C-minus is minor, Cdim is diminished, Caug or C+ is augmented. Guitarists read symbols above the lyrics, and pianists often see them above a melody. In the Nashville system the numbers stand in for any key.")],
 [("What are the semitones of a major triad?", ["0 4 7", "0 3 7", "0 3 6", "0 4 8"], 0, "Root, major third, fifth."),
  ("What is a minor triad?", ["Minor third then major third", "Two major thirds", "Two minor thirds", "A fourth and a fifth"], 0, "3 + 4."),
  ("Which triad is on the 7th degree of a major scale?", ["Diminished", "Major", "Minor", "Augmented"], 0, "B D F in C."),
  ("What is C E G?", ["C major", "C minor", "C diminished", "C augmented"], 0, "Major triad."),
  ("What is C E-flat G?", ["C minor", "C major", "C diminished", "C augmented"], 0, "Lowered third."),
  ("Which chord has two major thirds?", ["Augmented", "Diminished", "Minor", "Major"], 0, "C E G-sharp.")],
 [("Major", "0 4 7"), ("Minor", "0 3 7"), ("Diminished", "0 3 6"), ("Augmented", "0 4 8"), ("Root", "the note the chord is named for")],
 [MATCH("Match the triad", "Pair each triad quality with its semitone pattern.", [("Major", "0 4 7"), ("Minor", "0 3 7"), ("Diminished", "0 3 6"), ("Augmented", "0 4 8")]),
  PL("Build a triad", "Write triad(root, quality): root is a pitch class 0 to 11 and quality is 'major', 'minor', 'dim' or 'aug'. Return the three pitch classes [root, third, fifth] mod 12, using the offsets 0 4 7 for major, 0 3 7 minor, 0 3 6 dim, 0 4 8 aug.", "triad(root, quality)", '''
def triad(root, quality):
    offs = {"major": [0, 4, 7], "minor": [0, 3, 7], "dim": [0, 3, 6], "aug": [0, 4, 8]}
    return [(root + o) % 12 for o in offs[quality]]
''', [[0, "major"], [0, "minor"], [7, "major"], [11, "dim"], [4, "aug"], [9, "minor"]], "Look up the offsets, then add the root."),
  PL("Name the triad", "Write triad_quality(a, b, c): given three pitch classes of a triad in root position (root, third, fifth, each 0 to 11), compute the two intervals (b - a) mod 12 and (c - b) mod 12 and return 'major' for 4 and 3, 'minor' for 3 and 4, 'dim' for 3 and 3, 'aug' for 4 and 4, otherwise 'other'.", "triad_quality(a, b, c)", '''
def triad_quality(a, b, c):
    x = (b - a) % 12
    y = (c - b) % 12
    if x == 4 and y == 3:
        return "major"
    if x == 3 and y == 4:
        return "minor"
    if x == 3 and y == 3:
        return "dim"
    if x == 4 and y == 4:
        return "aug"
    return "other"
''', [[0, 4, 7], [9, 0, 4], [11, 2, 5], [0, 4, 8], [0, 2, 7], [7, 11, 2]], "Two intervals decide the quality."),
  PL("Diatonic triads", "Write diatonic_triads(tonic): the qualities of the seven triads built on the degrees of the major scale. The answer does not depend on the tonic: return ['major', 'minor', 'minor', 'major', 'major', 'minor', 'dim']. Compute it yourself by building the scale, stacking thirds from the scale, and naming each triad, then return the list of names.", "diatonic_triads(tonic)", '''
def diatonic_triads(tonic):
    steps = [2, 2, 1, 2, 2, 2]
    scale = [tonic % 12]
    n = tonic
    for s in steps:
        n = n + s
        scale.append(n % 12)
    out = []
    for i in range(7):
        a = scale[i]
        b = scale[(i + 2) % 7]
        c = scale[(i + 4) % 7]
        x = (b - a) % 12
        y = (c - b) % 12
        if x == 4 and y == 3:
            out.append("major")
        elif x == 3 and y == 4:
            out.append("minor")
        else:
            out.append("dim")
    return out
''', [[0], [7], [5], [2]], "Take every other scale note, wrapping around the list.")]
))

CHS.append(CH(
 "Seventh chords and inversions",
 ("Seventh chords", [
  "Seventh chord | adds | A fourth note",
  "Dominant seventh | has | Flat seventh",
  "Major seventh | has | Major seventh",
  "Minor seventh | has | Minor third and 7th",
  "Inversion | changes | The bass note",
  "First inversion | has | Third in the bass",
  "Slash chord | names | The bass note"]),
 ["A seventh chord adds a note a third above the fifth. Stack three thirds on a root and you have four notes: root, third, fifth and seventh.",
  "The main types are major seventh (0 4 7 11), dominant seventh (0 4 7 10), minor seventh (0 3 7 10) and half-diminished (0 3 6 10). The dominant seventh is the engine of classical and jazz harmony.",
  "An inversion puts a note other than the root in the bass. The chord is the same, only the lowest note changes."],
 [("Seventh chord", "A four-note chord made by stacking three thirds."),
  ("Dominant seventh", "A major triad with a minor seventh; the V7 chord."),
  ("Inversion", "A voicing of a chord with a note other than the root on the bottom."),
  ("Figured bass", "Numbers such as 6 and 6/4 that show the inversion of a chord."),
  ("Slash chord", "A chord symbol like C/E, showing the bass note after a slash.")],
 ["maj7: 0 4 7 11. 7: 0 4 7 10. m7: 0 3 7 10. m7b5: 0 3 6 10.",
  "V7 is a dominant seventh built on the 5th degree.",
  "Root position, first inversion (6), second inversion (6/4).",
  "A triad has 3 positions; a seventh chord has 4.",
  "C/E means a C chord with E in the bass."],
 [T("A triad has three notes, and a seventh chord has four. Take C E G and add the next third above, B, and you have C major seventh. Take the B down to B-flat and you have C7, a dominant seventh. A small change in the top note makes a big change in feel."),
  T("The dominant seventh is the most important. Built on the fifth degree of the key, it contains a tritone between its third and seventh. In C, G7 contains B and F, a tritone, and the tension resolves when B moves up to C and F moves down to E. That pull is why V7 leads strongly to I."),
  T("Four seventh-chord types cover most music. Major seventh is a major triad with a major seventh, 0 4 7 11, smooth and dreamy. Dominant seventh is a major triad with a minor seventh, 0 4 7 10. Minor seventh is a minor triad with a minor seventh, 0 3 7 10. Half-diminished is 0 3 6 10."),
  T("An inversion changes which note is lowest. For C major, C E G is root position, E G C is the first inversion, and G C E is the second inversion. The notes are the same, only the lowest changes. The sound differs a little, and moving the bass smoothly is a main reason to invert."),
  T("Inversions are named by the interval above the bass. In figured bass, the first inversion of a triad is 6 and the second is 6/4. Pop music writes a slash chord instead: C/E means C major over an E in the bass. Walking basslines often use slash chords.")],
 [("How many notes in a seventh chord?", ["4", "3", "5", "6"], 0, "Root, third, fifth, seventh."),
  ("What are the semitones of a dominant seventh?", ["0 4 7 10", "0 4 7 11", "0 3 7 10", "0 3 6 9"], 0, "G7 = G B D F."),
  ("What is E G C?", ["C major, first inversion", "C major, root position", "C minor", "E minor"], 0, "Third in the bass."),
  ("What does C/E mean?", ["C major with E in the bass", "C and E together", "C minor", "E major"], 0, "Slash chord."),
  ("Which degree carries the dominant seventh in a key?", ["5th", "1st", "4th", "7th"], 0, "V7."),
  ("How many positions does a seventh chord have?", ["4", "3", "2", "5"], 0, "Root and three inversions.")],
 [("maj7", "0 4 7 11"), ("7", "0 4 7 10"), ("m7", "0 3 7 10"), ("m7b5", "0 3 6 10"), ("6/4", "second inversion")],
 [MATCH("Match the seventh chord", "Pair each chord with its semitone pattern.", [("maj7", "0 4 7 11"), ("7", "0 4 7 10"), ("m7", "0 3 7 10"), ("m7b5", "0 3 6 10")]),
  PL("Build a seventh chord", "Write seventh(root, kind): root is a pitch class 0 to 11, kind is 'maj7', '7', 'm7' or 'm7b5'. Return the four pitch classes (root + offset) % 12 using offsets maj7 [0,4,7,11], 7 [0,4,7,10], m7 [0,3,7,10], m7b5 [0,3,6,10].", "seventh(root, kind)", '''
def seventh(root, kind):
    offs = {"maj7": [0, 4, 7, 11], "7": [0, 4, 7, 10], "m7": [0, 3, 7, 10], "m7b5": [0, 3, 6, 10]}
    return [(root + o) % 12 for o in offs[kind]]
''', [[0, "maj7"], [7, "7"], [2, "m7"], [11, "m7b5"], [5, "maj7"]], "Use a dictionary of offsets."),
  PL("Invert a chord", "Write invert_chord(notes, n): rotate the chord so that it is in its n-th inversion. For a list of pitch classes in root position, the n-th inversion starts n places later, with the earlier notes moved to the end. n = 0 returns the list unchanged.", "invert_chord(notes, n)", '''
def invert_chord(notes, n):
    out = []
    for i in range(len(notes)):
        out.append(notes[(i + n) % len(notes)])
    return out
''', [[[0, 4, 7], 0], [[0, 4, 7], 1], [[0, 4, 7], 2], [[7, 11, 2, 5], 1], [[7, 11, 2, 5], 3]], "Rotate the list."),
  PL("Which inversion?", "Write inversion_of(notes, bass): notes are the pitch classes of a chord in root position, bass is the lowest pitch class. Return the index of bass in the notes (0 root position, 1 first inversion, 2 second, 3 third), or -1 if bass is not in the chord.", "inversion_of(notes, bass)", '''
def inversion_of(notes, bass):
    for i in range(len(notes)):
        if notes[i] == bass:
            return i
    return -1
''', [[[0, 4, 7], 0], [[0, 4, 7], 4], [[0, 4, 7], 7], [[7, 11, 2, 5], 5], [[0, 4, 7], 2]], "Find the position of the bass note.")]
))

CHS.append(CH(
 "Harmony: progressions and cadences",
 ("Harmony", [
  "Roman numeral | names | A chord in a key",
  "Tonic | feels | At rest",
  "Dominant | creates | Tension",
  "Subdominant | moves | Away from home",
  "Cadence | ends | A phrase",
  "Authentic cadence | is | V to I",
  "Progression | is | A chord sequence"]),
 ["Roman numerals name chords by the scale degree of their root: I, ii, iii, IV, V, vi and vii-dim in a major key. Big numerals are major chords and small ones are minor, so the same pattern works in every key.",
  "Chords have jobs. The tonic (I) is home. The subdominant (IV, ii) moves away. The dominant (V, vii-dim) creates tension that wants to return home. Common progressions combine these jobs.",
  "A cadence is a chord pair that ends a phrase, like a full stop or a comma. The authentic cadence V to I is a full stop, and the half cadence ending on V is a comma."],
 [("Roman numeral analysis", "Naming chords by the scale degree of their root."),
  ("Tonic function", "Chords that feel stable and at rest, such as I and vi."),
  ("Dominant function", "Chords that create tension needing resolution, such as V and vii-dim."),
  ("Cadence", "A closing chord pair at the end of a phrase."),
  ("Progression", "A sequence of chords.")],
 ["I ii iii IV V vi vii-dim.",
  "Tonic: I vi. Subdominant: IV ii. Dominant: V vii.",
  "Authentic cadence V-I, plagal IV-I, half cadence ends on V, deceptive V-vi.",
  "Pop loop: I-V-vi-IV.",
  "Jazz turnaround: ii-V-I."],
 [T("Say we are in the key of C major. The chords are C, Dm, Em, F, G, Am and B-dim. Roman numerals replace those names with degrees, I ii iii IV V vi vii-dim. If the key changes to G, the chords change, but the numerals stay the same. A progression I-IV-V is the same shape in any key."),
  T("Chords play roles, like characters in a story. The tonic chord is home: the story starts and ends here. The subdominant steps away, a little restless. The dominant builds tension that wants to go home. Moving through these roles in the order tonic, subdominant, dominant, tonic is the base of classical and pop harmony."),
  T("A cadence is the ending of a phrase. The authentic cadence goes V to I, strong and final, like a full stop. The plagal cadence goes IV to I, the amen at the end of hymns. The half cadence stops on V and feels like a comma. The deceptive cadence goes V to vi, a surprise that dodges the expected ending."),
  T("Some progressions turn up everywhere. I-V-vi-IV drives countless pop songs. I-vi-IV-V is the 1950s doo-wop loop. The twelve-bar blues uses I, IV and V in a fixed pattern. In jazz, ii-V-I is the standard turnaround, resolving down by fifths."),
  T("Minor keys work the same way with different chords. In A minor, the harmonic minor scale gives i, ii-dim, III, iv, V, VI and vii-dim. The raised seventh makes V major, so minor keys can still end with a strong V to i cadence. Writing the progression in numerals lets you move it to any key.")],
 [("What does V to I form?", ["An authentic cadence", "A plagal cadence", "A half cadence", "A deceptive cadence"], 0, "Full stop."),
  ("Which chord is the tonic in C major?", ["C", "G", "F", "Am"], 0, "I."),
  ("What does the dominant chord do?", ["Creates tension that resolves to I", "Plays the melody", "Marks the tempo", "Cancels the key"], 0, "V wants I."),
  ("What is I-V-vi-IV in C?", ["C G Am F", "C F G C", "Am F C G", "C Dm G C"], 0, "The pop loop."),
  ("Which cadence is IV to I?", ["Plagal", "Authentic", "Half", "Deceptive"], 0, "The amen."),
  ("What is a deceptive cadence?", ["V to vi", "V to I", "IV to I", "I to V"], 0, "A surprise ending.")],
 [("I", "tonic, home"), ("IV", "subdominant"), ("V", "dominant"), ("V-I", "authentic cadence"), ("I-V-vi-IV", "pop progression")],
 [MATCH("Match the cadence", "Pair each cadence with its chords.", [("Authentic", "V to I"), ("Plagal", "IV to I"), ("Half", "ends on V"), ("Deceptive", "V to vi")]),
  PL("Roman numeral to chord", "Write chord_in_key(tonic, numeral): tonic is a pitch class 0 to 11 for a MAJOR key, numeral is one of 'I','ii','iii','IV','V','vi','vii'. Return the three pitch classes of that diatonic triad. Build the major scale, take the degree (I=0 ... vii=6), and stack scale notes at +0, +2 and +4 degrees (wrapping around).", "chord_in_key(tonic, numeral)", '''
def chord_in_key(tonic, numeral):
    steps = [2, 2, 1, 2, 2, 2]
    scale = [tonic % 12]
    n = tonic
    for s in steps:
        n = n + s
        scale.append(n % 12)
    names = ["I", "ii", "iii", "IV", "V", "vi", "vii"]
    d = names.index(numeral)
    return [scale[d], scale[(d + 2) % 7], scale[(d + 4) % 7]]
''', [[0, "I"], [0, "V"], [0, "vi"], [7, "IV"], [2, "ii"], [5, "vii"]], "Index into the scale list with wrap-around."),
  PL("A progression", "Write progression(tonic, numerals): for a list of numerals return a list of the root pitch classes of each chord in the major key tonic (I=degree 0 ... vii=degree 6). For tonic 0 and ['I','V','vi','IV'] the roots are [0, 7, 9, 5].", "progression(tonic, numerals)", '''
def progression(tonic, numerals):
    steps = [2, 2, 1, 2, 2, 2]
    scale = [tonic % 12]
    n = tonic
    for s in steps:
        n = n + s
        scale.append(n % 12)
    names = ["I", "ii", "iii", "IV", "V", "vi", "vii"]
    return [scale[names.index(x)] for x in numerals]
''', [[0, ["I", "V", "vi", "IV"]], [7, ["I", "IV", "V", "I"]], [2, ["ii", "V", "I"]], [5, ["I", "vi", "IV", "V"]]], "Reuse the scale and look up each numeral."),
  PL("Classify a cadence", "Write cadence(a, b): given two numerals ('I','ii','IV','V','vi'), return 'authentic' for V then I, 'plagal' for IV then I, 'deceptive' for V then vi, 'half' if b is V and a is not V, otherwise 'none'.", "cadence(a, b)", '''
def cadence(a, b):
    if a == "V" and b == "I":
        return "authentic"
    if a == "IV" and b == "I":
        return "plagal"
    if a == "V" and b == "vi":
        return "deceptive"
    if b == "V" and a != "V":
        return "half"
    return "none"
''', [["V", "I"], ["IV", "I"], ["V", "vi"], ["I", "V"], ["ii", "V"], ["I", "IV"], ["vi", "ii"]], "Check the specific pairs in order.")]
))

CHS.append(CH(
 "Melody, rhythm and form",
 ("Melody and form", [
  "Melody | is | A line of notes",
  "Motif | is | A short idea",
  "Phrase | ends | With a cadence",
  "Period | pairs | Two phrases",
  "Syncopation | stresses | Off-beats",
  "Form | arranges | Sections",
  "Counterpoint | combines | Melodies"]),
 ["A melody is a line of notes that makes sense as a tune. It is built from motifs, short ideas that are repeated, varied and developed into phrases.",
  "Rhythm gives melody its shape in time. Syncopation puts stress on weak beats, and a groove repeats a pattern.",
  "Form is the large-scale plan. Common forms use letters for sections: AB, ABA, verse and chorus, rondo, theme and variations."],
 [("Motif", "A short musical idea that is repeated and developed."),
  ("Phrase", "A musical sentence, usually ending in a cadence."),
  ("Syncopation", "Stress on a normally weak beat or between beats."),
  ("Binary and ternary form", "Two-part AB and three-part ABA structures."),
  ("Counterpoint", "Combining independent melodies that fit together.")],
 ["Motif, phrase, period, section.",
  "A period = antecedent (question) + consequent (answer).",
  "Forms: AB, ABA, rondo ABACA, verse-chorus.",
  "Syncopation: accents off the beat.",
  "Counterpoint: independent lines that make good harmony."],
 [T("Hum Happy Birthday. The first four notes are a motif. The song repeats it, changes it a little and builds a complete phrase. Most tunes work like that: take a small idea, repeat it, change it, and give it a clear ending."),
  T("Phrases pair up like questions and answers. The first phrase, the antecedent, ends on an open chord like V. The second phrase, the consequent, answers with a closed ending on I. Together they form a period, the basic sentence of tonal music."),
  T("Rhythm decides whether a tune dances. In 4/4, the strong beats are one and three. Place accents on the weaker two and four, or between beats, and you get syncopation, the heart of jazz, funk and Latin music. A pattern that repeats makes a groove."),
  T("Form is the architecture. A song with verse and chorus alternates sections, say A B A B. A classical minuet uses ternary form ABA. A rondo returns to its main theme between episodes, ABACA. Theme and variations keep the harmony and change the surface."),
  T("Counterpoint means point against point. Two melodies played together, each good by itself, make good harmony together. Bach's fugues are the classic example, where a subject enters in one voice after another. The basic rules are to move mostly in contrary motion and treat parallel fifths with care.")],
 [("What is a motif?", ["A short repeated idea", "A time signature", "A cadence", "A chord"], 0, "The seed of a melody."),
  ("What does an antecedent phrase do?", ["Asks, ending open", "Answers, ending closed", "Plays a drone", "Marks a rest"], 0, "A question."),
  ("What is syncopation?", ["Stress on weak beats", "A very slow tempo", "A key change", "A rest"], 0, "Off-beat accents."),
  ("What does ABA describe?", ["Ternary form", "Binary form", "A rondo", "A fugue"], 0, "Return of A."),
  ("What is counterpoint?", ["Combining independent melodies", "A chord type", "A scale", "A tempo mark"], 0, "Point against point."),
  ("What is a rondo's pattern?", ["ABACA", "ABAB", "AABB", "ABCD"], 0, "A keeps returning.")],
 [("Motif", "short idea"), ("Period", "question and answer phrase"), ("ABA", "ternary form"), ("Syncopation", "off-beat stress"), ("Fugue", "contrapuntal form")],
 [MATCH("Match the form", "Pair each form with its pattern.", [("Binary", "AB"), ("Ternary", "ABA"), ("Rondo", "ABACA"), ("Verse and chorus", "ABAB")]),
  PL("Contour", "Write contour(pitches): for a list of MIDI note numbers return a list of 'u' (up), 'd' (down) or 's' (same) for each step between neighbouring notes. The result has one fewer item than the input.", "contour(pitches)", '''
def contour(pitches):
    out = []
    for i in range(1, len(pitches)):
        if pitches[i] > pitches[i - 1]:
            out.append("u")
        elif pitches[i] < pitches[i - 1]:
            out.append("d")
        else:
            out.append("s")
    return out
''', [[[60, 62, 64, 62]], [[60, 60, 67]], [[72]], [[64, 62, 60, 60, 62]]], "Compare each note with the one before it."),
  PL("Form string", "Write count_sections(form): given a form string like 'ABACA', return a dict-like list: [number of distinct letters, number of times the first letter appears]. For 'ABACA' this is [3, 3].", "count_sections(form)", '''
def count_sections(form):
    seen = {}
    for ch in form:
        seen[ch] = 1
    first = form[0]
    n = 0
    for ch in form:
        if ch == first:
            n = n + 1
    return [len(seen), n]
''', [["ABACA"], ["ABA"], ["AB"], ["ABAB"], ["AABBA"]], "Collect the letters you see and count the first one."),
  PL("Syncopation count", "Write syncopated(onsets): onsets is a list of positions in eighth-note units within a 4/4 measure (0 to 7); strong beats are the even positions (0, 2, 4, 6 are on the beat). Return how many onsets fall on an odd position (off the beat).", "syncopated(onsets)", '''
def syncopated(onsets):
    n = 0
    for o in onsets:
        if o % 2 == 1:
            n = n + 1
    return n
''', [[[0, 2, 4, 6]], [[1, 3, 5]], [[0, 1, 4, 7]], [[]]], "Odd positions are the off-beats.")]
))

CHS.append(CH(
 "Transposition, ear training and putting it together",
 ("Putting it together", [
  "Transposition | shifts | A melody",
  "Interval | is | Preserved",
  "Ear training | learns | Intervals and chords",
  "Solfege | names | Scale degrees",
  "Songwriting | uses | Progression and melody",
  "Practice | builds | Skill",
  "Theory | explains | What you hear"]),
 ["To transpose a piece, shift every note by the same interval. The pattern of intervals, and therefore the tune, is unchanged, only the pitch level moves.",
  "Ear training links sounds to names. Learn the intervals from songs, sing scale degrees with solfege (do re mi), and hear chord qualities as colours.",
  "Writing a short song uses everything you have learned: pick a key, choose a progression, write a melody that uses chord tones on strong beats, and shape the form."],
 [("Transposition", "Moving music up or down by a fixed interval."),
  ("Solfege", "Syllables do re mi fa sol la ti used to name scale degrees."),
  ("Ear training", "Practice that links sounds with their names."),
  ("Chord tone", "A note that belongs to the chord sounding at that moment."),
  ("Lead sheet", "A melody with chord symbols above it.")],
 ["Transpose: add the same number of semitones to each note.",
  "Solfege: do re mi fa sol la ti do.",
  "Hear intervals through songs.",
  "Strong beats: chord tones; weak beats: passing notes.",
  "A lead sheet = melody + chords."],
 [T("Singers who find a song too high ask to transpose it. Every note moves down by the same number of semitones. The shape and the intervals are the same, so it is still recognisably the same song. Transposing up a whole tone adds two semitones to every note."),
  T("Musicians who play in different instruments also transpose. A B-flat clarinet sounds a whole tone lower than written, so its part is written two semitones higher. A key change in a pop song, up a semitone or a tone for the last chorus, is a transposition."),
  T("Ear training makes the symbols audible. Sing the scale with solfege: do re mi fa sol la ti do. Learn each interval by a song. Play triads and learn to hear whether they are major or minor. A few minutes a day for a month changes how you hear music."),
  T("Now try writing a small song. Pick a key such as C major. Choose a four-chord loop such as I V vi IV. Write a melody where the notes on strong beats are notes of the chord that is sounding, and let notes on weak beats move by step between them. End the phrase on the tonic."),
  T("Theory describes what music does. It does not decide what is good. Use it to understand what you like, to find what a piece is doing, and to get ideas when you are stuck. The best next step is to play and listen to music with a theory ear, and to keep notes of what you find.")],
 [("What does transposing do?", ["Shifts all notes by the same interval", "Changes the rhythm", "Changes the form", "Removes accidentals"], 0, "Same tune, new pitch."),
  ("What are the syllables for the major scale degrees?", ["Do re mi fa sol la ti", "A B C D E F G", "I II III IV V", "Alpha beta gamma"], 0, "Solfege."),
  ("If a melody in C is transposed up 2 semitones, what key is it in?", ["D major", "B-flat major", "E major", "C major"], 0, "C plus 2."),
  ("Which notes should fall on strong beats?", ["Chord tones", "Any non-key notes", "Rests only", "Dissonant notes"], 0, "They sound stable."),
  ("What is a lead sheet?", ["Melody with chord symbols", "A full orchestra score", "A drum chart", "A tuning chart"], 0, "Simple and portable."),
  ("A B-flat clarinet sounds...", ["A whole tone lower than written", "A fifth higher", "As written", "An octave higher"], 0, "Transposing instrument.")],
 [("Transpose", "add the same semitones to every note"), ("Solfege", "do re mi fa sol la ti"), ("Lead sheet", "melody plus chord symbols"), ("Chord tone", "note in the current chord")],
 [MATCH("Match the step", "Pair each step of songwriting with its job.", [("Choose a key", "sets the notes"), ("Choose a progression", "sets the harmony"), ("Write a melody", "uses chord tones on strong beats"), ("Shape the form", "decides the sections")]),
  FILL("Transposition", "To transpose, add the same number of {{semitones}} to every note. The intervals stay the {{same}}, so the tune is recognisable."),
  PL("Transpose a melody", "Write transpose(notes, n): add n semitones to every MIDI note number in the list and return the new list.", "transpose(notes, n)", '''
def transpose(notes, n):
    return [x + n for x in notes]
''', [[[60, 62, 64], 2], [[60, 67, 72], -5], [[69], 12], [[], 3]], "Add n to each note."),
  PL("Which note is a chord tone?", "Write chord_tones(melody, chord): melody is a list of pitch classes 0 to 11, chord is a list of pitch classes. Return how many of the melody notes belong to the chord.", "chord_tones(melody, chord)", '''
def chord_tones(melody, chord):
    n = 0
    for m in melody:
        if m in chord:
            n = n + 1
    return n
''', [[[0, 2, 4, 7], [0, 4, 7]], [[1, 3, 5], [0, 4, 7]], [[7, 11, 2], [7, 11, 2]], [[], [0, 4, 7]]], "Count the melody notes found in the chord."),
  PL("Frequency ratio of an interval", "Write ratio(semitones): the equal-tempered frequency ratio for an interval, 2 to the power (semitones / 12), rounded to 4 decimals. An octave gives 2.0 and a fifth gives about 1.4983.", "ratio(semitones)", '''
def ratio(semitones):
    return round(2 ** (semitones / 12.0), 4)
''', [[12], [7], [0], [4], [5], [6]], "Use 2 ** (x / 12.0).", approx=0.0001)]
))
