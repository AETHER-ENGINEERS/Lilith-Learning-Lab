#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Signal Processing course. Usage: python3 make_signal_processing_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "dsp"))
import cmk, dsp_a, dsp_b, make_apps  # noqa: E402
make_apps.main()
CHS = dsp_a.CHS + dsp_b.CHS
PRONOUNCE = {"Nyquist": "nye kwist", "Shannon": "shan un", "Fourier": "foor ee ay", "Cooley": "koo lee", "Tukey": "too kee", "DFT": "D F T", "FFT": "F F T", "FIR": "F I R", "IIR": "I I R",
    "LTI": "L T I", "biquad": "bye kwod", "biquads": "bye kwods", "Hann": "han", "Hamming": "ham ing", "sinc": "sink", "quantisation": "kwon tih zay shun", "decimation": "dess ih may shun",
    "autocorrelation": "aw toe kor uh lay shun", "spectrogram": "spek truh gram", "JPEG": "jay peg", "DCT": "D C T", "hertz": "hurts", "Hz": "hertz", "kHz": "kilohertz", "dB": "decibels"}
SANDBOX = cmk.terminal("DSP cheat sheet", "dsp>", "A scripted lookup. Try: nyquist, alias, conv, dft, fir, iir, window, bins", [
    ("nyquist", ["Sample faster than twice the highest frequency. Nyquist frequency = fs / 2."]),
    ("alias", ["Fold f into 0..fs/2: r = f mod fs; if r > fs/2 use fs - r."]),
    ("conv", ["y[n] = sum of x[k] h[n-k]. Length = len(x) + len(h) - 1."]),
    ("dft", ["X[k] = sum x[n] e^(-2 pi i k n / N). Bin k is at k fs / N hertz."]),
    ("fir", ["Weighted sum of recent inputs. Symmetric taps give linear phase."]),
    ("iir", ["Uses past outputs. Stable when all poles are inside the unit circle."]),
    ("window", ["Taper the frame to cut leakage: Hann w[n] = 0.5 - 0.5 cos(2 pi n/(N-1))."]),
    ("bins", ["Resolution = fs / N. Zero padding does not improve it."]),
])
EXAM = [
 ("What is the Nyquist frequency?", ["Half the sample rate", "The sample rate", "Twice the sample rate", "The lowest frequency"], 0, "fs / 2."),
 ("What is aliasing?", ["A high frequency appearing as a lower one", "A gain change", "A delay", "Added noise"], 0, "Sampling too slowly."),
 ("A 30 Hz sine sampled at 40 Hz appears at what frequency?", ["10 Hz", "30 Hz", "70 Hz", "20 Hz"], 0, "40 - 30."),
 ("How many levels does 8-bit audio have?", ["256", "8", "128", "65536"], 0, "2 to the 8."),
 ("What does an anti-alias filter do?", ["Removes frequencies above fs / 2 before sampling", "Adds bits", "Speeds up sampling", "Removes DC"], 0, "Analog low-pass."),
 ("What is the period of a 50 Hz wave?", ["0.02 s", "0.5 s", "50 s", "0.2 s"], 0, "1 / f."),
 ("What is an impulse response?", ["Output for a single 1 input", "A sum of inputs", "A window", "A bin"], 0, "h[n]."),
 ("What operation gives an LTI system's output?", ["Convolution", "Division", "Squaring", "Sorting"], 0, "y = x * h."),
 ("Length of the full convolution of lists of lengths 5 and 3?", ["7", "8", "15", "5"], 0, "5 + 3 - 1."),
 ("What does the DFT reveal?", ["Frequency content", "Sample rate", "Bit depth", "Timing only"], 0, "Spectrum."),
 ("At what frequency is DFT bin k?", ["k fs / N", "k N / fs", "fs / k", "k"], 0, "Bin spacing fs / N."),
 ("What is the cost of the FFT?", ["About N log N", "About N squared", "About N", "About 1"], 0, "Cooley and Tukey."),
 ("What is H(0) of an FIR filter?", ["The sum of the taps", "Always 1", "Always 0", "The first tap"], 0, "DC gain."),
 ("Which FIR taps make a simple high-pass?", ["[1, -1]", "[1, 1]", "[1, 1, 1, 1]", "[0.5, 0.5]"], 0, "A difference."),
 ("What gives an FIR filter linear phase?", ["Symmetric taps", "Feedback", "Zero taps", "Large gain"], 0, "Equal delay."),
 ("What is a pole of a transfer function?", ["A root of the denominator", "A root of the numerator", "A sample", "A window"], 0, "Makes H infinite."),
 ("When is a causal IIR filter stable?", ["All poles inside the unit circle", "All poles outside it", "No zeros", "Taps sum to 1"], 0, "|z| < 1."),
 ("What does a smaller a do in y = a x + (1-a) y_prev?", ["Smooths more", "Smooths less", "Adds gain", "Makes it FIR"], 0, "Slower response."),
 ("What causes spectral leakage?", ["Cutting the wave mid-cycle", "Too many bits", "Silence", "A low gain"], 0, "Seam jump."),
 ("What does a window function do?", ["Tapers the frame edges", "Adds samples", "Raises the pitch", "Removes the DC"], 0, "Smooth hump."),
 ("Does zero padding improve resolution?", ["No, it only interpolates", "Yes", "Only for audio", "Only above Nyquist"], 0, "No new information."),
 ("What is a spectrogram?", ["Spectra over successive frames", "A single DFT", "A filter", "A window"], 0, "STFT."),
 ("Which filter best removes isolated spikes?", ["Median", "Mean", "Difference", "Sinc"], 0, "Ignores outliers."),
 ("What does autocorrelation help find?", ["The period or pitch", "The sample rate", "The bit depth", "The gain"], 0, "Peak at the period."),
 ("What must you do before decimating?", ["Low-pass filter", "High-pass filter", "Add noise", "Zero pad"], 0, "Avoid aliasing."),
 ("What does JPEG do to image blocks?", ["DCT and drop small coefficients", "Sort pixels", "Blur the whole image", "Double the size"], 0, "Lossy compression."),
]
CFG = dict(id="signal-processing", title="Signal Processing",
    subtitle="Sampling, convolution, the Fourier transform, filters and windows, with runnable Python labs and a spectrum lab",
    description="A hands-on introduction to digital signal processing: signals and systems, sampling, aliasing and quantisation, convolution and impulse responses, the discrete Fourier transform and FFT, FIR and IIR filters with frequency response and the z-transform, windows and spectral leakage, and applications in noise removal, pitch detection, decimation, image filtering and compression. Every chapter has Python labs verified in the built-in interpreter, and two interactive labs let you explore aliasing and filtering with live spectra.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="dsp", apps={"__ALIAS__": "alias.html", "__FILTER__": "filter.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "signal-processing.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
