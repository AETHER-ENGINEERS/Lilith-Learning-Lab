# -*- coding: utf-8 -*-
"""Signal processing course, part 2: filters, feedback, windows, applications."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "FIR filters and frequency response",
 ("FIR filters", [
  "Filter | keeps | Some frequencies",
  "Low-pass | passes | Low frequencies",
  "High-pass | passes | High frequencies",
  "Band-pass | passes | A band",
  "Frequency response | is | Gain per frequency",
  "Taps | are | Coefficients",
  "Cutoff | is | Edge of passband"]),
 ["A filter changes how strongly each frequency is passed. A low-pass filter keeps low frequencies and removes high ones; a high-pass does the opposite; a band-pass keeps a range.",
  "An FIR filter computes each output as a weighted sum of recent inputs, using a list of coefficients called taps. The moving average is the simplest low-pass.",
  "The frequency response shows the gain at each frequency. For taps b it is H(w) = sum of b[k] e^(-i w k), and its magnitude tells how much of frequency w gets through."],
 [("Low-pass filter", "A filter that passes low frequencies and attenuates high ones."),
  ("Frequency response", "How a system's gain and phase change with frequency."),
  ("Tap", "One coefficient of an FIR filter, multiplying one delayed sample."),
  ("Cutoff frequency", "The frequency where the gain starts to fall."),
  ("Linear phase", "A filter with symmetric taps delays all frequencies equally.")],
 ["y[n] = b0 x[n] + b1 x[n-1] + ... + bM x[n-M].",
  "H(w) = sum b[k] e^(-i w k).",
  "Symmetric taps give linear phase.",
  "Moving average: low-pass.",
  "Difference [1, -1]: high-pass."],
 [T("Imagine a smudge on a photograph that blends each pixel with its neighbours. A rapidly changing detail gets blurred away, while broad shapes remain. A low-pass filter does this to a signal along time."),
  T("The moving average over four samples is a low-pass FIR filter with taps one quarter, one quarter, one quarter, one quarter. A slow wave passes almost untouched because neighbouring samples are alike. A rapid wiggle averages to nearly zero because neighbours cancel."),
  T("The frequency response tells this precisely. Put the filter taps through the same sort of sum as the DFT: H of w equals the sum of b of k times e to the minus i w k. Its magnitude as a function of w is the gain curve. At w equal to zero it is just the sum of the taps."),
  T("Flip the sign of alternate taps and low-pass becomes high-pass. The two-tap filter one, minus one subtracts the previous sample, so it passes changes and removes steady levels. This is also a basic edge detector in images."),
  T("Designing a filter means choosing taps to approximate a desired gain curve. A classic method, the windowed sinc, takes the ideal low-pass impulse response, a sinc function, and tapers it with a window. Longer filters have sharper edges but cost more computation and delay.")],
 [("What does a low-pass filter do?", ["Passes low frequencies, removes high ones", "Passes only high ones", "Adds noise", "Samples faster"], 0, "Smooths."),
  ("What are the taps of an FIR filter?", ["Its coefficients", "Its inputs", "Its noise", "Its frequency"], 0, "Weights."),
  ("What is the gain of a filter at frequency zero?", ["The sum of its taps", "The first tap", "Always one", "Always zero"], 0, "H(0) = sum b."),
  ("Which taps make a simple high-pass?", ["[1, -1]", "[1, 1]", "[1, 1, 1]", "[0, 0]"], 0, "A difference."),
  ("Why use longer FIR filters?", ["Sharper cutoffs", "Less delay", "Less computing", "Fewer taps"], 0, "A trade-off."),
  ("What does symmetric taps give?", ["Linear phase", "Instability", "Aliasing", "No gain"], 0, "Equal delay.")],
 [("H(w)", "frequency response"), ("b[k]", "FIR taps"), ("H(0) = sum b", "DC gain"), ("[1, -1]", "difference filter")],
 [APP("FILTER", "Filter lab", "Pick a signal with low and high tones, then try the moving average, a difference and a windowed sinc low-pass. Watch the spectrum before and after. Try all three filters to complete this lab.", 760),
  MATCH("Match the filter", "Pair each filter with what it does.", [("Low-pass", "keeps low frequencies"), ("High-pass", "keeps high frequencies"), ("Band-pass", "keeps a band"), ("Moving average", "simple low-pass"), ("Difference", "simple high-pass")]),
  PL("FIR filter", "Write fir(x, b): filter the list x with taps b, y[n] = sum of b[k] x[n - k], using zero for x before the start. Return a list the same length as x, each value rounded to 4 decimals.", "fir(x, b)", '''
def fir(x, b):
    y = []
    for n in range(len(x)):
        s = 0.0
        for k in range(len(b)):
            if n - k >= 0:
                s = s + b[k] * x[n - k]
        y.append(round(s, 4))
    return y
''', [[[1, 2, 3, 4], [0.5, 0.5]], [[1, 0, 0, 0], [1, 2, 3]], [[1, 1, 1, 1], [1, -1]], [[2, 4, 6], [0.25, 0.5, 0.25]]], "Sum over taps, skipping indexes before the start."),
  PL("Gain at a frequency", "Write gain(b, w): the magnitude |H(w)| of the FIR filter with taps b at angular frequency w (radians per sample), where H(w) = sum of b[k] (cos(wk) - i sin(wk)). Round to 4 decimals.", "gain(b, w)", '''
import math
def gain(b, w):
    re = 0.0
    im = 0.0
    for k in range(len(b)):
        re = re + b[k] * math.cos(w * k)
        im = im - b[k] * math.sin(w * k)
    return round(math.sqrt(re * re + im * im), 4)
''', [[[0.5, 0.5], 0], [[0.5, 0.5], 3.14159265], [[1, -1], 0], [[1, -1], 3.14159265], [[0.25, 0.25, 0.25, 0.25], 1.5707963]], "Add real and imaginary parts then take the magnitude.", approx=0.001),
  PL("Windowed sinc taps", "Write lowpass_taps(cutoff, m): m taps (m odd) of a low-pass FIR filter with normalised cutoff between 0 and 0.5 (fraction of the sample rate), h[k] = 2 c sinc(2 c (k - centre)) where centre = (m - 1) / 2 and sinc(0) = 1, sinc(u) = sin(pi u) / (pi u). Return the taps divided by their sum, rounded to 4 decimals.", "lowpass_taps(cutoff, m)", '''
import math
def lowpass_taps(cutoff, m):
    c = (m - 1) / 2.0
    h = []
    for k in range(m):
        u = 2 * cutoff * (k - c)
        if u == 0:
            s = 1.0
        else:
            s = math.sin(math.pi * u) / (math.pi * u)
        h.append(2 * cutoff * s)
    t = sum(h)
    out = []
    for v in h:
        out.append(round(v / t, 4))
    return out
''', [[0.25, 5], [0.1, 7], [0.4, 3]], "Compute the sinc, then normalise so that taps add to one."),
  PL("Remove the mean", "Write remove_dc(x): subtract the average of x from every sample (a crude high-pass). Round each result to 4 decimals. An empty list returns an empty list.", "remove_dc(x)", '''
def remove_dc(x):
    if len(x) == 0:
        return []
    m = sum(x) / float(len(x))
    out = []
    for v in x:
        out.append(round(v - m, 4))
    return out
''', [[[1, 2, 3]], [[5, 5, 5, 5]], [[0, 10]], [[]]], "Average first, then subtract.")]
))

CHS.append(CH(
 "IIR filters, feedback and the z-transform",
 ("IIR filters", [
  "IIR | uses | Feedback",
  "z-transform | describes | Systems",
  "Pole | causes | Resonance",
  "Zero | causes | Cancellation",
  "Stability | needs | Poles inside the circle",
  "Transfer function | is | B over A",
  "One-pole | is | Exponential smoother"]),
 ["An IIR filter feeds past outputs back into the calculation, y[n] = b0 x[n] - a1 y[n-1] and so on. It can achieve a sharp response with very few coefficients but has an impulse response that never exactly ends.",
  "The z-transform turns a difference equation into algebra. The transfer function H(z) is a ratio of polynomials. Zeros are roots of the top, poles are roots of the bottom.",
  "A causal filter is stable when every pole lies inside the unit circle, meaning |z| < 1. A pole on or outside the circle makes the output grow without bound."],
 [("IIR filter", "A filter that feeds back its own past outputs, so its impulse response is infinite."),
  ("Transfer function", "The ratio H(z) = B(z) / A(z) describing a filter in the z domain."),
  ("Pole", "A value of z that makes the denominator of H(z) zero."),
  ("Zero", "A value of z that makes the numerator of H(z) zero."),
  ("Stable", "A system whose output stays bounded for bounded input.")],
 ["y[n] = a x[n] + (1 - a) y[n-1] smooths.",
  "Pole of 1 - p z^-1 is z = p.",
  "Stable if all |poles| < 1.",
  "Poles near the unit circle give sharp resonance.",
  "Zeros on the unit circle null a frequency."],
 [T("Think of a bath tap and drain. The water level this minute depends on the level a minute ago plus what the tap adds. That feedback is an IIR filter. It forgets the past gradually, never quite all at once."),
  T("The simplest one is a one-pole low-pass: each output is a blend of the new input and the previous output, y of n equals a times x of n plus one minus a times y of n minus one. Small a means heavy smoothing and slow response. It is used everywhere to calm noisy sensor readings, because it needs just one stored number."),
  T("The z-transform replaces delays by powers of z to the minus one. Then the filter becomes a fraction, H of z equals B of z over A of z. Roots of the denominator are the poles, and they decide the character of the filter: where they sit tells whether it rings, how fast it decays, and whether it is stable."),
  T("The stability rule is clean. A causal filter is stable when all poles are strictly inside the unit circle. The pole of the one-pole filter is at one minus a. With a between zero and one it lies inside. With a bigger than two it lies outside, and the output explodes."),
  T("Compared with FIR, IIR filters are cheaper for a given sharpness, but they are harder to make linear-phase and can be unstable or noisy in fixed-point arithmetic. A common safe design splits high-order filters into small second-order sections called biquads.")],
 [("What is feedback in an IIR filter?", ["Past outputs are used in the calculation", "The input is repeated", "The sample rate changes", "Noise is added"], 0, "y[n-1]."),
  ("What is a pole?", ["A root of the denominator", "A root of the numerator", "A sample", "A tap"], 0, "Makes H infinite."),
  ("When is a causal filter stable?", ["All poles inside the unit circle", "All poles outside", "Zeros inside", "No poles"], 0, "|z| < 1."),
  ("What does a small a do in a one-pole smoother?", ["Heavier smoothing", "Less smoothing", "Instability", "Nothing"], 0, "Slow response."),
  ("Why are biquads used?", ["Small sections are easier to keep stable", "They remove poles", "They are FIR", "They sample faster"], 0, "Second-order sections."),
  ("What does the z-transform turn a delay into?", ["Multiplication by z^-1", "Addition of 1", "A sine", "A pole"], 0, "Algebra.")],
 [("H(z) = B/A", "transfer function"), ("z^-1", "one-sample delay"), ("|p| < 1", "stable"), ("y = a x + (1-a) y_prev", "one-pole smoother")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Pole", "root of the denominator"), ("Zero", "root of the numerator"), ("IIR", "uses feedback"), ("Stable", "poles inside the unit circle"), ("Biquad", "second-order section")]),
  PL("One-pole smoother", "Write smooth(x, a): y[n] = a x[n] + (1 - a) y[n-1], with y[-1] = 0 (so y[0] = a x[0]). Return the list rounded to 4 decimals.", "smooth(x, a)", '''
def smooth(x, a):
    y = []
    prev = 0.0
    for v in x:
        prev = a * v + (1 - a) * prev
        y.append(round(prev, 4))
    return y
''', [[[1, 1, 1, 1], 0.5], [[10, 0, 0, 0], 0.25], [[1, 2, 3], 1], [[5, 5], 0.1]], "Keep the previous output in a variable."),
  PL("Step response", "Write iir_impulse(a1, n): the first n samples of the impulse response of y[k] = x[k] - a1 y[k-1] (input 1, 0, 0, ...). Round each to 4 decimals.", "iir_impulse(a1, n)", '''
def iir_impulse(a1, n):
    out = []
    prev = 0.0
    for k in range(n):
        xk = 1.0 if k == 0 else 0.0
        prev = xk - a1 * prev
        out.append(round(prev, 4))
    return out
''', [[-0.5, 5], [0.5, 5], [-1.0, 4], [-1.5, 5]], "Feed the previous output back with a minus sign."),
  PL("Is it stable?", "Write stable(a1): for the filter y[n] = x[n] - a1 y[n-1], return True if the pole z = -a1 lies strictly inside the unit circle, otherwise False.", "stable(a1)", '''
def stable(a1):
    return abs(-a1) < 1
''', [[0.5], [-0.9], [1], [-1], [1.5], [0]], "Compare the pole's magnitude with 1."),
  PL("Biquad run", "Write biquad(x, b0, b1, b2, a1, a2): the direct form I filter y[n] = b0 x[n] + b1 x[n-1] + b2 x[n-2] - a1 y[n-1] - a2 y[n-2], with zeros before the start. Return rounded to 4 decimals.", "biquad(x, b0, b1, b2, a1, a2)", '''
def biquad(x, b0, b1, b2, a1, a2):
    y = []
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0
    for v in x:
        out = b0 * v + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        y.append(round(out, 4))
        x2 = x1
        x1 = v
        y2 = y1
        y1 = out
    return y
''', [[[1, 0, 0, 0, 0], 1, 0, 0, -0.5, 0], [[1, 1, 1, 1], 0.5, 0.5, 0, 0, 0], [[1, 0, 0, 0, 0], 1, 0, 0, 0, -0.25]], "Remember two past inputs and two past outputs.")]
))

CHS.append(CH(
 "Windows, leakage and spectrum analysis",
 ("Windowing", [
  "Window | tapers | The edges",
  "Leakage | spreads | Energy",
  "Hann | reduces | Leakage",
  "Main lobe | is | Peak width",
  "Side lobes | are | Leakage ripples",
  "Zero padding | interpolates | The spectrum",
  "Spectrogram | shows | Time and frequency"]),
 ["The DFT assumes the N samples repeat forever. If a sine does not fit a whole number of cycles in the window, the repeat has a jump and energy leaks into many bins.",
  "A window function tapers the signal smoothly to zero at both edges, cutting the leakage at the price of a wider main peak. The Hann window is a popular compromise.",
  "To see how a spectrum changes in time, cut the signal into overlapping frames, window each one and take a DFT of each. The picture of those spectra is a spectrogram."],
 [("Spectral leakage", "Spreading of a frequency's energy into neighbouring bins because the window cuts the wave mid-cycle."),
  ("Window function", "A weighting that tapers a frame toward zero at its edges before the DFT."),
  ("Hann window", "The window w[n] = 0.5 - 0.5 cos(2 pi n / (N-1))."),
  ("Zero padding", "Appending zeros before the DFT to get a smoother-looking spectrum."),
  ("Spectrogram", "A plot of spectra over successive frames, showing frequency against time.")],
 ["Hann: w[n] = 0.5 - 0.5 cos(2 pi n / (N-1)).",
  "Whole cycles in the frame give no leakage.",
  "Better resolution needs a longer frame.",
  "Zero padding does not add information.",
  "Spectrogram = windowed DFTs over time."],
 [T("Cut a record of a pure tone at a random point and you almost certainly cut the wave mid-cycle. The DFT sees a signal that repeats the chunk end to end, with a sudden jump at the seam. A jump is rich in every frequency, so the clean peak gets skirts of leaked energy."),
  T("The remedy is to fade the chunk in and out. A window function multiplies the frame by a smooth hump that starts and ends at zero. The seam disappears and the skirts drop a lot. The cost is a slightly broader peak, because the effective signal is shorter."),
  T("Different windows make different trade-offs. The rectangular window, no tapering, has the narrowest peak and the worst leakage. Hann and Hamming reduce leakage a great deal. Blackman reduces it still more with a wider peak. There is no free lunch, only the right compromise for the job."),
  T("Resolution is set by the length of the observation. Two tones closer than fs over N cannot be told apart, however much you zero-pad. Padding with zeros only interpolates the same information on a finer grid and makes the plot look smoother."),
  T("Real sounds change with time, so we cut the signal into short overlapping frames, window each, take the DFT and stack the magnitudes. The result is the spectrogram: time along one axis, frequency along the other, brightness for strength. Speech, birdsong and music look like distinctive patterns on it.")],
 [("What causes spectral leakage?", ["The frame cuts the wave mid-cycle", "Low sample rate only", "Too many bits", "Silence"], 0, "A jump at the seam."),
  ("What does a Hann window do?", ["Tapers the frame to zero at the edges", "Doubles the frame", "Adds noise", "Samples faster"], 0, "Smooth hump."),
  ("What is the cost of a window?", ["A wider main peak", "More leakage", "A lower sample rate", "Aliasing"], 0, "Trade-off."),
  ("Does zero padding improve resolution?", ["No, it only interpolates", "Yes, fully", "Only for noise", "Only for audio"], 0, "No new information."),
  ("What is a spectrogram?", ["Spectra over time", "A filter", "A window", "A sample"], 0, "Frequency against time."),
  ("How do you resolve two close tones?", ["Observe for longer", "Pad with zeros", "Lower gain", "Sample slower"], 0, "Bigger N.")],
 [("Hann", "0.5 - 0.5 cos(2 pi n / (N-1))"), ("fs / N", "frequency resolution"), ("STFT", "short-time Fourier transform")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Leakage", "energy spread to other bins"), ("Window", "tapers the frame edges"), ("Zero padding", "finer grid, no new information"), ("Spectrogram", "spectra over time"), ("Resolution", "fs over N")]),
  PL("Hann window", "Write hann(n): the n-point Hann window w[k] = 0.5 - 0.5 cos(2 pi k / (n - 1)) for k = 0 to n-1, rounded to 4 decimals. For n = 1 return [1.0].", "hann(n)", '''
import math
def hann(n):
    if n == 1:
        return [1.0]
    out = []
    for k in range(n):
        out.append(round(0.5 - 0.5 * math.cos(2 * math.pi * k / (n - 1)), 4))
    return out
''', [[1], [2], [5], [8]], "Zero at both ends, one in the middle."),
  PL("Apply a window", "Write windowed(x, w): multiply each sample of x by the matching window value and round to 4 decimals. Assume equal lengths.", "windowed(x, w)", '''
def windowed(x, w):
    out = []
    for i in range(len(x)):
        out.append(round(x[i] * w[i], 4))
    return out
''', [[[1, 1, 1, 1], [0, 0.75, 0.75, 0]], [[2, 4, 6], [0, 1, 0]], [[3], [1]]], "Multiply element by element."),
  PL("Frames", "Write frames(x, size, hop): cut x into frames of the given size, starting every hop samples, keeping only complete frames. Return a list of lists.", "frames(x, size, hop)", '''
def frames(x, size, hop):
    out = []
    i = 0
    while i + size <= len(x):
        out.append(x[i:i + size])
        i = i + hop
    return out
''', [[[1, 2, 3, 4, 5, 6], 4, 2], [[1, 2, 3, 4, 5], 2, 2], [[1, 2, 3], 5, 1], [[1, 2, 3, 4], 3, 1]], "Move the start by hop each time."),
  PL("Frame energy", "Write energy(x): the sum of the squares of the samples, rounded to 4 decimals.", "energy(x)", '''
def energy(x):
    s = 0.0
    for v in x:
        s = s + v * v
    return round(s, 4)
''', [[[1, 2, 3]], [[0.5, 0.5]], [[]], [[-2, 2]]], "Squares are never negative.", approx=0.001)]
))

CHS.append(CH(
 "Applications: noise, pitch, images and compression",
 ("Applications", [
  "Median filter | removes | Spikes",
  "Autocorrelation | finds | Period",
  "Pitch | is | Fundamental frequency",
  "Decimation | lowers | Sample rate",
  "Image | is | 2D signal",
  "Compression | drops | Small parts",
  "Modulation | shifts | Frequency"]),
 ["The same tools serve many jobs. A median filter erases spikes without blurring edges. Autocorrelation finds the repeat period of a signal, which gives pitch. Decimation lowers the sample rate after low-pass filtering.",
  "An image is a two-dimensional signal; blurring, sharpening and edge detection are 2D convolutions with small kernels.",
  "Compression such as JPEG and MP3 transforms the signal to the frequency domain, discards small or inaudible parts, and stores the rest."],
 [("Median filter", "A nonlinear filter that replaces each sample by the median of its neighbourhood."),
  ("Autocorrelation", "The similarity of a signal with a delayed copy of itself, as a function of delay."),
  ("Decimation", "Lowering the sample rate by keeping every Mth sample after low-pass filtering."),
  ("Kernel", "A small grid of weights convolved with an image."),
  ("Modulation", "Shifting a signal's frequencies by multiplying it by a carrier wave.")],
 ["Autocorrelation peak at lag L: period L, pitch fs / L.",
  "Decimate by M: low-pass first, then keep every Mth.",
  "Median kills spikes, mean smears them.",
  "Blur kernel: all positive and sums to 1.",
  "Edge kernel: positive and negative parts."],
 [T("A sensor reading with an occasional wild spike is a headache for averaging, because the spike drags the mean. The median ignores outliers: sort the neighbourhood and take the middle. A three-point median filter removes isolated spikes and keeps sharp steps in place."),
  T("How do you find the pitch of a note? Compare the signal with delayed copies of itself. When the delay equals the period, the copy lines up with the original and the match is strong. The first strong peak of this autocorrelation gives the period in samples, and fs divided by that gives the frequency."),
  T("To store a signal at a lower rate, you cannot just throw samples away, or high frequencies alias. First low-pass filter to the new Nyquist limit, then keep every Mth sample. Raising the rate, interpolation, works by inserting zeros and then low-pass filtering."),
  T("Pictures are signals in two dimensions. Blurring slides a small kernel of positive weights over the image. A kernel with a positive side and a negative side picks out edges. A convolutional neural network is built from layers of such kernels, whose weights are learned rather than designed."),
  T("Compression exploits the frequency domain. JPEG cuts an image into small blocks, takes a discrete cosine transform and rounds away the small high-frequency coefficients that the eye barely notices. MP3 does similar things with a model of what the ear cannot hear. Radio uses modulation to place a message on a carrier frequency so many stations share the air.")],
 [("Which filter best removes isolated spikes?", ["Median", "Mean", "Difference", "Hann"], 0, "Ignores outliers."),
  ("What does autocorrelation help find?", ["The period of a signal", "The sample rate", "The bit depth", "The gain"], 0, "Pitch."),
  ("What must precede decimation?", ["A low-pass filter", "A high-pass filter", "More samples", "Zero padding"], 0, "Avoid aliasing."),
  ("What is an image in signal processing?", ["A 2D signal", "A filter", "A window", "A spectrum"], 0, "Rows and columns."),
  ("What does JPEG discard?", ["Small high-frequency coefficients", "All colours", "Half the pixels", "The header"], 0, "DCT blocks."),
  ("What does modulation do?", ["Places a message on a carrier frequency", "Removes noise", "Samples faster", "Counts bits"], 0, "Radio.")],
 [("fs / lag", "pitch from autocorrelation"), ("keep every Mth", "decimation"), ("DCT", "used by JPEG")],
 [MATCH("Match the tool to the job", "Pair each tool with its use.", [("Median filter", "remove spikes"), ("Autocorrelation", "find pitch"), ("Decimation", "lower the sample rate"), ("Blur kernel", "smooth an image"), ("DCT", "image compression")]),
  PL("Median filter", "Write median3(x): a 3-point median filter. The first and last samples are kept as they are; every interior sample becomes the median of itself and its two neighbours.", "median3(x)", '''
def median3(x):
    if len(x) < 3:
        return list(x)
    out = [x[0]]
    for i in range(1, len(x) - 1):
        t = sorted([x[i - 1], x[i], x[i + 1]])
        out.append(t[1])
    out.append(x[-1])
    return out
''', [[[1, 1, 9, 1, 1]], [[1, 2, 3, 4]], [[5, 0, 5, 0, 5]], [[7, 8]]], "Sort three values and take the middle."),
  PL("Autocorrelation", "Write autocorr(x, lag): the sum of x[i] x x[i + lag] for all valid i. Round to 4 decimals.", "autocorr(x, lag)", '''
def autocorr(x, lag):
    s = 0.0
    for i in range(len(x) - lag):
        s = s + x[i] * x[i + lag]
    return round(s, 4)
''', [[[1, 0, -1, 0, 1, 0, -1, 0], 0], [[1, 0, -1, 0, 1, 0, -1, 0], 2], [[1, 0, -1, 0, 1, 0, -1, 0], 4], [[1, 2, 3], 1]], "Multiply the signal with its shifted copy and add.", approx=0.001),
  PL("Pitch period", "Write pitch(x, fs, min_lag, max_lag): the frequency fs / L where L is the lag in min_lag..max_lag with the largest autocorrelation (the first such lag if tied). Return the frequency rounded to 2 decimals.", "pitch(x, fs, min_lag, max_lag)", '''
def pitch(x, fs, min_lag, max_lag):
    best = min_lag
    bv = None
    for lag in range(min_lag, max_lag + 1):
        s = 0.0
        for i in range(len(x) - lag):
            s = s + x[i] * x[i + lag]
        if bv is None or s > bv + 1e-9:
            bv = s
            best = lag
    return round(fs / float(best), 2)
''', [[[1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0], 8000, 2, 6], [[1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1], 1000, 2, 6]], "Try each lag and keep the best.", approx=0.01),
  PL("Decimate", "Write decimate(x, m): average each group of m consecutive samples (a crude low-pass) and keep one output per group, ignoring an incomplete final group. Round to 4 decimals.", "decimate(x, m)", '''
def decimate(x, m):
    out = []
    i = 0
    while i + m <= len(x):
        s = 0.0
        for j in range(m):
            s = s + x[i + j]
        out.append(round(s / m, 4))
        i = i + m
    return out
''', [[[1, 2, 3, 4, 5, 6], 2], [[1, 2, 3, 4, 5], 2], [[4, 4, 4], 3], [[1, 2], 3]], "Average before dropping samples."),
  PL("Image blur", "Write blur(img): replace each interior pixel of the 2D list img with the average of itself and its four neighbours (up, down, left, right), rounded to 3 decimals. Edge pixels stay as they are.", "blur(img)", '''
def blur(img):
    h = len(img)
    w = len(img[0]) if h else 0
    out = []
    for r in range(h):
        row = []
        for c in range(w):
            if r == 0 or c == 0 or r == h - 1 or c == w - 1:
                row.append(img[r][c])
            else:
                s = img[r][c] + img[r - 1][c] + img[r + 1][c] + img[r][c - 1] + img[r][c + 1]
                row.append(round(s / 5.0, 3))
        out.append(row)
    return out
''', [[[[0, 0, 0], [0, 5, 0], [0, 0, 0]]], [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[[1, 1], [1, 1]]]], "Leave the border pixels alone.")]
))
