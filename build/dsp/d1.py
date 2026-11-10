# -*- coding: utf-8 -*-
"""Signal processing course, part 1: signals, sampling, systems, convolution, DFT."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Signals and systems: what we are processing",
 ("Signals", [
  "Signal | carries | Information",
  "Analog signal | is | Continuous in time",
  "Digital signal | is | Sampled and quantised",
  "System | transforms | Signals",
  "Amplitude | is | Height",
  "Frequency | is | Cycles per second",
  "Phase | is | Shift in time"]),
 ["A signal is a quantity that varies, usually with time, and carries information: sound pressure, a heartbeat voltage, a stock price, the brightness along a row of pixels. A system takes a signal in and produces a signal out.",
  "Analog signals are continuous. Digital signal processing (DSP) works on lists of numbers that were sampled at regular steps, which computers can handle exactly.",
  "The simplest signal is the sine wave, described by amplitude, frequency and phase. Almost every other signal can be built from sines."],
 [("Signal", "A function that carries information, such as a value that changes with time."),
  ("System", "Anything that turns an input signal into an output signal."),
  ("Amplitude", "The size of a signal's swing."),
  ("Frequency", "How many cycles happen per second, measured in hertz (Hz)."),
  ("Phase", "How far a wave is shifted along the time axis.")],
 ["A sine: A sin(2 pi f t + phase).",
  "Period T = 1 / f.",
  "Digital signals are lists of numbers.",
  "A system maps input signals to output signals.",
  "Every real signal can be built from sines."],
 [T("Look at a voice recorded on a phone. Behind the file is a list of numbers, thousands per second, each one the air pressure at a moment. That list is a digital signal. Signal processing is the art of changing, cleaning and understanding such lists."),
  T("The sine wave is the building block. Its three numbers are amplitude, how tall it is; frequency, how many times it repeats per second; and phase, where in its cycle it starts. A 440 hertz sine with amplitude one sounds as the note A above middle C."),
  T("The period is the time for one cycle, and equals one divided by the frequency. A 100 hertz wave repeats every 0.01 seconds. Signals made of several sines add up, and the sum can look complicated while each part is simple."),
  T("A system is anything that acts on signals: an amplifier, an echo, a filter, a microphone. Some systems are linear and time-invariant, called LTI systems. They have a beautiful theory built on convolution and Fourier analysis, which is the core of this course."),
  T("Along the way we will use Python to build signals, sample them, filter them and look at their spectra. The same ideas run inside phones, radios, medical scanners, music software and radar.")],
 [("What is a signal?", ["A function carrying information", "A kind of cable", "A battery", "A code editor"], 0, "Often varies with time."),
  ("What is the period of a 100 Hz sine?", ["0.01 s", "100 s", "0.1 s", "1 s"], 0, "1 / f."),
  ("What does frequency measure?", ["Cycles per second", "Height of the wave", "Position of the wave", "Noise"], 0, "Hertz."),
  ("What does a system do?", ["Turns an input signal into an output signal", "Stores a file", "Draws a graph", "Prints a number"], 0, "Input to output."),
  ("What is a digital signal?", ["A list of sampled numbers", "A continuous voltage", "A radio tower", "A cable"], 0, "Discrete."),
  ("What is phase?", ["A shift along the time axis", "The height", "The speed of sound", "The noise level"], 0, "Where the cycle starts.")],
 [("Hz", "cycles per second"), ("T = 1/f", "period from frequency"), ("A sin(2 pi f t)", "a sine wave"), ("LTI", "linear time-invariant system")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Amplitude", "size of the swing"), ("Frequency", "cycles per second"), ("Phase", "shift along time"), ("Period", "time for one cycle"), ("System", "turns a signal into another signal")]),
  PL("Period from frequency", "Write period(f): the period in seconds of a sine of frequency f hertz, 1 / f, rounded to 6 decimals.", "period(f)", '''
def period(f):
    return round(1.0 / f, 6)
''', [[100], [440], [1], [50], [0.5]], "One divided by f.", approx=0.000002),
  PL("Generate a sine", "Write sine(amp, freq, phase, fs, n): the first n samples of amp x sin(2 pi freq t + phase) sampled at fs samples per second (t = k / fs). Return the list of samples multiplied by 1000 and rounded to integers, so that the values are exact to compare.", "sine(amp, freq, phase, fs, n)", '''
import math
def sine(amp, freq, phase, fs, n):
    out = []
    for k in range(n):
        v = amp * math.sin(2 * math.pi * freq * k / fs + phase)
        out.append(int(round(v * 1000)))
    return out
''', [[1, 1, 0, 8, 8], [2, 2, 0, 16, 8], [1, 1, 1.5707963, 8, 4], [0.5, 10, 0, 40, 4]], "Loop over sample numbers k and compute the time k over fs."),
  PL("Sum of two sines", "Write mix(f1, f2, fs, n): the first n samples of sin(2 pi f1 t) + sin(2 pi f2 t) at sample rate fs, multiplied by 1000 and rounded to integers.", "mix(f1, f2, fs, n)", '''
import math
def mix(f1, f2, fs, n):
    out = []
    for k in range(n):
        t = k / float(fs)
        v = math.sin(2 * math.pi * f1 * t) + math.sin(2 * math.pi * f2 * t)
        out.append(int(round(v * 1000)))
    return out
''', [[1, 2, 16, 8], [5, 5, 40, 4], [3, 7, 32, 6]], "Add the two sines at each time.")]
))

CHS.append(CH(
 "Sampling, aliasing and quantisation",
 ("Sampling", [
  "Sampling | measures | At regular times",
  "Sample rate | is | Samples per second",
  "Nyquist | needs | Twice the top frequency",
  "Aliasing | fakes | Lower frequencies",
  "Anti-alias filter | removes | High frequencies",
  "Quantisation | rounds | To levels",
  "Bit depth | sets | Number of levels"]),
 ["To store a continuous signal in a computer we sample it: measure it at regular instants. The sample rate fs is how many samples per second we take.",
  "The Nyquist-Shannon sampling theorem says that a signal containing no frequency above B can be captured perfectly if fs is more than 2B. Sampling too slowly causes aliasing: a high frequency masquerades as a lower one.",
  "Each sample is also rounded to one of a finite number of levels, called quantisation. With b bits there are 2^b levels, and the rounding error behaves like a faint noise."],
 [("Sample rate", "The number of samples taken per second."),
  ("Nyquist frequency", "Half the sample rate; the highest frequency that can be represented."),
  ("Aliasing", "The false appearance of a high frequency as a lower one when sampled too slowly."),
  ("Quantisation", "Rounding each sample to the nearest of a finite set of levels."),
  ("Bit depth", "The number of bits per sample; b bits give 2^b levels.")],
 ["Sample faster than 2 times the top frequency.",
  "Nyquist frequency = fs / 2.",
  "Alias of f: fold into 0..fs/2.",
  "CD audio: 44100 Hz, 16 bits.",
  "6 dB of range per bit."],
 [T("Imagine filming a spinning wheel. If the camera takes too few pictures per second, the wheel can seem to turn slowly, or even backwards. That is aliasing. The camera sampled too slowly to follow the true motion, and the samples fit a slower false story."),
  T("The rule is the sampling theorem. If the highest frequency in a signal is B, sample at more than twice B. Human hearing reaches about 20,000 hertz, so CD audio uses 44,100 samples per second. Half of that, 22,050 hertz, is the Nyquist frequency."),
  T("What if a frequency above the Nyquist frequency sneaks in? It folds back. A 30 hertz sine sampled at 40 hertz appears as a 10 hertz sine, because 40 minus 30 is 10. To prevent this, real systems put an analog anti-aliasing filter before the sampler to remove frequencies above the limit."),
  T("Sampling is only half of digitising. Each sample must be stored with a limited number of bits. This is quantisation. With 3 bits there are 8 levels. With 16 bits, as on a CD, there are 65,536 levels. The difference between the true value and the rounded one acts like a small noise, and each extra bit improves the signal-to-noise ratio by about 6 decibels."),
  T("Choosing rates and bit depths is an engineering trade-off. Speech needs only about 8,000 samples per second. Music needs 44,100 or more. Medical and scientific systems may need many more bits. The labs let you compute aliases and quantise signals yourself.")],
 [("What does the Nyquist theorem say about sample rate?", ["It must exceed twice the top frequency", "It must equal the top frequency", "It must be below half", "It does not matter"], 0, "fs > 2B."),
  ("What is aliasing?", ["A high frequency appearing as a lower one", "A louder sound", "A faster clock", "A gain change"], 0, "Folding."),
  ("What is the Nyquist frequency at 44100 Hz sampling?", ["22050 Hz", "44100 Hz", "88200 Hz", "11025 Hz"], 0, "fs / 2."),
  ("How many levels does 16-bit audio have?", ["65536", "256", "16", "1024"], 0, "2 to the 16."),
  ("What does an anti-alias filter remove?", ["Frequencies above the Nyquist limit", "Low frequencies", "All noise", "DC offset only"], 0, "Before sampling."),
  ("What does quantisation do?", ["Rounds samples to finite levels", "Samples faster", "Filters noise", "Adds echo"], 0, "Finite precision.")],
 [("fs > 2B", "Nyquist-Shannon rule"), ("fs / 2", "Nyquist frequency"), ("2^b", "levels in b bits"), ("6 dB per bit", "approximate SNR gain")],
 [APP("ALIAS", "Spectrum and aliasing explorer", "Set two tones and the sample rate, and watch the waveform and spectrum. Push a tone above half the sample rate to see it alias. Do this twice and change the sample rate once to complete this lab.", 760),
  MATCH("Match the idea", "Pair each term with its meaning.", [("Sample rate", "samples per second"), ("Nyquist frequency", "half the sample rate"), ("Aliasing", "false lower frequency"), ("Quantisation", "rounding to levels"), ("Anti-alias filter", "removes frequencies above fs / 2")]),
  PL("Alias frequency", "Write alias(f, fs): the apparent frequency in hertz (0 to fs/2) when a sine of frequency f is sampled at rate fs. Fold f into the range: take f modulo fs; if the result is more than fs / 2 return fs minus that result, otherwise the result.", "alias(f, fs)", '''
def alias(f, fs):
    r = f % fs
    if r > fs / 2.0:
        return fs - r
    return r
''', [[30, 40], [10, 40], [50, 40], [20, 40], [44100, 44100], [3000, 8000], [7000, 8000]], "Fold around fs over two.", approx=0.001),
  PL("Quantise", "Write quantise(x, bits): x is a value from -1 to 1. Quantise it to a signed grid with 2^bits levels spread evenly: levels = 2^bits; step = 2 / (levels - 1); return round((x + 1) / step) x step - 1, rounded to 4 decimals.", "quantise(x, bits)", '''
def quantise(x, bits):
    levels = 2 ** bits
    step = 2.0 / (levels - 1)
    return round(round((x + 1.0) / step) * step - 1.0, 4)
''', [[0.3, 2], [-1, 3], [0.5, 3], [0.9, 1], [0.0, 4]], "Round to the nearest grid point.", approx=0.001),
  PL("Levels and range", "Write levels(bits): the number of quantisation levels, 2 to the power bits, and the approximate dynamic range in decibels, 6.02 x bits rounded to 1 decimal. Return the list [levels, range].", "levels(bits)", '''
def levels(bits):
    return [2 ** bits, round(6.02 * bits, 1)]
''', [[8], [16], [1], [24]], "Two powers and six decibels per bit.", approx=0.05)]
))

CHS.append(CH(
 "Discrete systems and convolution",
 ("Systems", [
  "LTI system | is | Linear and time-invariant",
  "Impulse | is | A single 1",
  "Impulse response | defines | The system",
  "Convolution | gives | The output",
  "FIR | has | Finite response",
  "IIR | has | Feedback",
  "Delay | shifts | In time"]),
 ["A discrete system turns an input list x[n] into an output list y[n]. If it is linear (outputs add and scale with inputs) and time-invariant (shifting the input shifts the output), it is an LTI system.",
  "Feed an LTI system a single impulse, a 1 followed by zeros, and the output is its impulse response h[n]. Every other output is then the convolution of the input with h.",
  "Convolution slides a flipped copy of h along x, multiplying and adding, and it is the main operation of filtering."],
 [("Impulse", "A signal that is 1 at n = 0 and 0 elsewhere."),
  ("Impulse response", "The output of a system when the input is an impulse, written h[n]."),
  ("Convolution", "The operation y[n] = sum over k of x[k] h[n - k]."),
  ("Linear time-invariant (LTI)", "A system whose outputs add and scale with inputs and do not depend on when the input starts."),
  ("FIR filter", "A filter whose impulse response has finite length.")],
 ["y[n] = sum of x[k] h[n - k].",
  "Length of x * h = len(x) + len(h) - 1.",
  "Convolution is commutative and associative.",
  "Convolving with an impulse leaves a signal unchanged.",
  "A delay is convolution with a shifted impulse."],
 [T("Take a simple system: it outputs the average of the current input and the previous one. Give it a single 1 followed by zeros. The output is half, half, zero. That output is the impulse response, and it fully describes the system."),
  T("Why? Any input is a sum of scaled and shifted impulses. A linear time-invariant system turns each impulse into a scaled, shifted copy of the impulse response. Adding them up gives the output. That sum is the convolution of the input with the impulse response."),
  T("To compute it by hand, flip the impulse response, slide it along the input, and at each position multiply overlapping numbers and add. The output has length of x plus length of h minus one. In code it is a double loop: for each input sample and each tap, add the product to the right output position."),
  T("An FIR filter, finite impulse response, has an impulse response that ends. A moving average is a typical example. An IIR filter, infinite impulse response, uses feedback so that the response never quite stops, like the echo of a shout in a canyon. Chapters on filters will build both."),
  T("Convolution has handy properties. It is commutative and associative, so cascading two filters gives the same result in either order. Convolving with a single impulse changes nothing, and convolving with a delayed impulse delays the signal. Echo effects in audio are convolution with a few spikes.")],
 [("What is an impulse response?", ["The output when the input is a single 1", "The sum of the input", "A kind of filter", "The sample rate"], 0, "h[n]."),
  ("What does convolution compute for an LTI system?", ["The output from input and impulse response", "The Fourier transform", "The sample rate", "The noise"], 0, "y = x * h."),
  ("What is the length of x * h?", ["len(x) + len(h) - 1", "len(x)", "len(h)", "len(x) x len(h)"], 0, "Full convolution."),
  ("What does an FIR filter have?", ["Finite impulse response", "Feedback", "An infinite memory", "No taps"], 0, "It ends."),
  ("What does convolving with a delayed impulse do?", ["Delays the signal", "Doubles it", "Filters it", "Removes it"], 0, "Shift."),
  ("Does the order of cascaded LTI filters matter?", ["No", "Yes always", "Only for FIR", "Only for IIR"], 0, "Commutative.")],
 [("h[n]", "impulse response"), ("x * h", "convolution"), ("FIR", "finite impulse response"), ("IIR", "infinite impulse response")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Impulse", "a single 1 then zeros"), ("Impulse response", "output for an impulse"), ("Convolution", "slide, multiply, add"), ("FIR", "finite response"), ("IIR", "uses feedback")]),
  PL("Convolve", "Write convolve(x, h): the full convolution of two lists of numbers. The result has len(x) + len(h) - 1 entries, y[n] = sum of x[k] x h[n - k]. If either list is empty return an empty list.", "convolve(x, h)", '''
def convolve(x, h):
    if len(x) == 0 or len(h) == 0:
        return []
    y = []
    for i in range(len(x) + len(h) - 1):
        y.append(0)
    for i in range(len(x)):
        for j in range(len(h)):
            y[i + j] = y[i + j] + x[i] * h[j]
    return y
''', [[[1, 2, 3], [1, 1]], [[1, 0, 0], [5, 6, 7]], [[1, 2, 3, 4], [0.5, 0.5]], [[], [1]], [[2], [3]]], "Add each product x[i] h[j] into position i + j."),
  PL("Moving average", "Write moving_average(x, m): the average of each window of m consecutive samples (the 'valid' part only), so the result has len(x) - m + 1 entries, each rounded to 3 decimals. If m is larger than len(x) return an empty list.", "moving_average(x, m)", '''
def moving_average(x, m):
    out = []
    for i in range(len(x) - m + 1):
        s = 0
        for j in range(m):
            s = s + x[i + j]
        out.append(round(s / float(m), 3))
    return out
''', [[[1, 2, 3, 4, 5], 2], [[1, 2, 3, 4, 5], 3], [[10, 0, 10, 0], 2], [[1, 2], 5]], "Slide a window along the list."),
  PL("Impulse response", "Write impulse_response(b, n): the first n samples of the output of the FIR filter y[k] = sum of b[j] x[k - j] when the input is the impulse (1, 0, 0, ...). Samples beyond the filter length are zero.", "impulse_response(b, n)", '''
def impulse_response(b, n):
    out = []
    for k in range(n):
        if k < len(b):
            out.append(b[k])
        else:
            out.append(0)
    return out
''', [[[0.5, 0.5], 4], [[1, 2, 3], 3], [[1], 2], [[1, -1], 5]], "The output equals the coefficients, padded with zeros."),
  PL("Echo", "Write echo(x, delay, gain): add a delayed, scaled copy of x to itself. The output has len(x) + delay samples: y[n] = x[n] + gain x x[n - delay], where x outside its range is 0.", "echo(x, delay, gain)", '''
def echo(x, delay, gain):
    y = []
    for i in range(len(x) + delay):
        y.append(0)
    for i in range(len(x)):
        y[i] = y[i] + x[i]
        y[i + delay] = y[i + delay] + gain * x[i]
    return y
''', [[[1, 0, 0], 2, 0.5], [[1, 2], 1, 1], [[3], 3, 2], [[], 2, 1]], "Add the original and the delayed copy.")]
))

CHS.append(CH(
 "The Fourier idea and the DFT",
 ("Fourier analysis", [
  "Fourier | splits | Signals into sines",
  "Spectrum | shows | Frequency content",
  "DFT | transforms | N samples",
  "Bin | covers | A frequency band",
  "Magnitude | gives | Strength",
  "Phase | gives | Timing",
  "Resolution | is | fs over N"]),
 ["Fourier's idea is that any signal can be written as a sum of sine waves of different frequencies, amplitudes and phases. The spectrum shows how much of each frequency a signal contains.",
  "The discrete Fourier transform (DFT) turns N samples into N complex numbers, one for each frequency bin. Bin k corresponds to the frequency k fs / N. The magnitude of the bin tells how strong that frequency is.",
  "The fast Fourier transform (FFT) computes the same result in about N log N steps instead of N squared, which made digital spectrum analysis practical."],
 [("Spectrum", "A description of a signal's strength at each frequency."),
  ("DFT", "The discrete Fourier transform: X[k] = sum over n of x[n] e^(-2 pi i k n / N)."),
  ("Bin", "One output of the DFT, covering a narrow band of frequency."),
  ("Frequency resolution", "The spacing between bins, fs / N."),
  ("FFT", "A fast algorithm for the DFT, taking about N log N operations.")],
 ["X[k] = sum x[n] (cos - i sin)(2 pi k n / N).",
  "Bin k is at k fs / N hertz.",
  "Real signal: bins above N/2 mirror the lower ones.",
  "Magnitude = sqrt(re^2 + im^2).",
  "Resolution = fs / N."],
 [T("A musical chord sounds like one thing, but your ear can pick out the notes. The Fourier transform does the same for numbers. Give it a list of samples, and it says how much of each pure frequency the list contains."),
  T("The recipe for the DFT is simple. For each frequency bin k, multiply the signal by a cosine and a sine that complete k cycles over the N samples, and add up the results. If the signal contains that frequency, the products line up and the sum is large. If not, they cancel and the sum is small."),
  T("The cosine sum gives the real part and the minus sine sum gives the imaginary part. The magnitude, the square root of their squares, is the strength of the frequency. The angle gives its phase. To plot a spectrum, you usually plot the magnitude against frequency."),
  T("Bin k stands for the frequency k times fs divided by N. If you sample at 1000 hertz and take 100 samples, the bins are 10 hertz apart. A real signal has a mirror-image spectrum, so only bins up to N over two carry new information, up to the Nyquist frequency."),
  T("Computing the DFT directly takes N squared multiplications. The fast Fourier transform, popularised by Cooley and Tukey in 1965, splits the sum into even and odd samples and reuses work, getting N log N. For a million samples that is the difference between hours and a fraction of a second.")],
 [("What does the Fourier transform show?", ["How much of each frequency a signal has", "The sample rate", "The noise", "The bit depth"], 0, "Spectrum."),
  ("What frequency does bin k represent?", ["k x fs / N", "k x N / fs", "fs / k", "k"], 0, "Spacing fs / N."),
  ("With fs = 1000 and N = 100, how far apart are bins?", ["10 Hz", "100 Hz", "1 Hz", "1000 Hz"], 0, "fs / N."),
  ("What is the magnitude of a bin?", ["sqrt(re^2 + im^2)", "re + im", "re x im", "im"], 0, "Strength."),
  ("How many operations does a direct DFT need?", ["About N squared", "About N", "About log N", "About 2"], 0, "N times N."),
  ("What does the FFT achieve?", ["The same result in about N log N steps", "A different result", "Noise removal", "Resampling"], 0, "Cooley and Tukey.")],
 [("X[k]", "DFT output at bin k"), ("fs / N", "bin spacing"), ("N log N", "FFT cost"), ("|X[k]|", "magnitude")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Spectrum", "strength at each frequency"), ("Bin", "one DFT output"), ("Magnitude", "strength of a frequency"), ("Resolution", "fs divided by N"), ("FFT", "fast way to compute the DFT")]),
  PL("DFT magnitude", "Write dft_mag(x): the magnitude |X[k]| of the DFT of the real list x for k = 0 to N-1, each value rounded to 3 decimals. Use X[k] = sum over n of x[n] (cos(2 pi k n / N) - i sin(2 pi k n / N)), so |X[k]| = sqrt(re^2 + im^2).", "dft_mag(x)", '''
import math
def dft_mag(x):
    n = len(x)
    out = []
    for k in range(n):
        re = 0.0
        im = 0.0
        for t in range(n):
            ang = 2 * math.pi * k * t / n
            re = re + x[t] * math.cos(ang)
            im = im - x[t] * math.sin(ang)
        out.append(round(math.sqrt(re * re + im * im), 2))
    return out
''', [[[1, 1, 1, 1]], [[1, 0, -1, 0]], [[0, 1, 0, -1]], [[1, 2, 3, 4]]], "Two nested loops, summing cos and sin terms."),
  PL("Bin frequency", "Write bin_freq(k, fs, n): the centre frequency in hertz of DFT bin k for n samples at sample rate fs, k x fs / n, rounded to 3 decimals.", "bin_freq(k, fs, n)", '''
def bin_freq(k, fs, n):
    return round(k * fs / float(n), 3)
''', [[5, 1000, 100], [0, 44100, 1024], [1, 8000, 8], [3, 48000, 256]], "Multiply by fs and divide by n.", approx=0.001),
  PL("Peak frequency", "Write peak_freq(x, fs): the frequency in hertz of the strongest bin among bins 1 to n//2 of the DFT of the real list x (skip bin 0, the average), computed with the DFT magnitudes. Return the frequency k x fs / n for the first bin with the largest magnitude.", "peak_freq(x, fs)", '''
import math
def peak_freq(x, fs):
    n = len(x)
    best = 1
    bm = -1.0
    for k in range(1, n // 2 + 1):
        re = 0.0
        im = 0.0
        for t in range(n):
            ang = 2 * math.pi * k * t / n
            re = re + x[t] * math.cos(ang)
            im = im - x[t] * math.sin(ang)
        m = math.sqrt(re * re + im * im)
        if m > bm + 1e-9:
            bm = m
            best = k
    return best * fs / float(n)
''', [[[0, 1, 0, -1, 0, 1, 0, -1], 8], [[1, 1, -1, -1, 1, 1, -1, -1], 8], [[0.0, 0.7071, 1.0, 0.7071, 0.0, -0.7071, -1.0, -0.7071], 8]], "Compute the magnitude for each bin and keep the largest.", approx=0.001)]
))
