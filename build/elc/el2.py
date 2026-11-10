"""Electronics course, chapters 8-13. Original text."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

B = []

B.append(CH(
 "Thyristors and light",
 ("Switches and light", ["SCR | latches | On", "Triac | switches | AC both ways", "UJT | makes | Pulses", "LED | emits | Light", "Photoresistor | changes | With light", "Photodiode | makes | Current from light", "Solar cell | gives | Power"]),
 ["A thyristor, such as an SCR or a triac, is a switch that a small pulse turns on and that then stays on until the current drops. Triacs work with AC in both directions.",
  "Light is a wave, and LEDs, photoresistors, photodiodes and solar cells all turn electricity into light or light into electricity.",
  "A lens bends light; a convex lens can focus it onto a detector."],
 [("SCR", "A silicon controlled rectifier; a one-way latching switch."), ("Triac", "A thyristor that conducts in both AC directions."), ("Latching", "Staying on after the trigger has gone."),
  ("Photoresistor", "A resistor whose value falls in bright light."), ("Photodiode", "A diode that makes current when lit."), ("Solar cell", "A large photodiode that produces power.")],
 ["An SCR turns on with a gate pulse and off when its current falls to zero.", "Triacs control AC power, for example in light dimmers.", "Mains circuits are dangerous: only experiment with low voltage.", "Light's frequency is the speed of light divided by wavelength.", "A photoresistor in a divider gives a voltage that follows the light.", "A convex lens brings parallel rays to a focus."],
 [T("A thyristor is a switch with memory. A short pulse on the gate turns an SCR on, and it stays on even after the pulse ends. It switches off only when the current through it falls to zero. That makes it useful with AC, where the current drops to zero every cycle."),
  T("A triac is like two SCRs back to back, so it handles both halves of an AC wave. By turning it on later in each half-cycle, a dimmer cuts the average power. This is how a lamp is dimmed without wasting heat in a resistor."),
  T("Light is a wave. Red light has a long wavelength and violet a short one, and frequency equals the speed of light divided by wavelength. An LED gives off light when current crosses its junction, and different materials give different colors."),
  M(r"f=\frac{c}{\lambda}"),
  T("Light detectors come in several types. A photoresistor changes its resistance with light, is cheap and slow. A photodiode makes a small current when lit and is fast. A phototransistor amplifies that current. A solar cell is a big photodiode that delivers useful power. Put a detector in a divider to turn light into a voltage.")],
 [("What turns off an SCR?", ["Current falling to zero", "A gate pulse", "More light", "A capacitor"], 0, "It latches."),
  ("Which switches AC both ways?", ["Triac", "SCR", "LED", "Photodiode"], 0, "Two SCRs back to back."),
  ("What does red light have?", ["A longer wavelength than violet", "A shorter wavelength", "No frequency", "Mass"], 0, "Violet is shorter.")],
 [("What is latching?", "Staying on."), ("What is a photodiode?", "A diode that makes current from light."), ("What is a triac for?", "AC power control."), ("What gives a solar cell power?", "Light on a PN junction.")],
 [MATCH("Light parts", "Match each part with its job.", [("Photoresistor", "Resistance falls in light"), ("Photodiode", "Makes current from light"), ("Phototransistor", "Amplifies photocurrent"), ("Solar cell", "Produces power from light")]),
  PL("SCR simulation", "Write scr(steps): steps is a list of [gate, current_flowing] pairs (1 or 0). The SCR is off at the start. It turns on when gate is 1 and current is 1. Once on, it stays on while current is 1 and turns off when current is 0. Return the list of states after each step (1 on, 0 off).", "scr(steps)", """
def scr(steps):
    on = 0
    out = []
    for gate, cur in steps:
        if on:
            if not cur:
                on = 0
        elif gate and cur:
            on = 1
        out.append(on)
    return out
""", [[[[1, 1], [0, 1], [0, 0], [0, 1]]], [[]], [[[1, 0], [1, 1], [0, 1]]]], "Latch while the current continues.", approx=None),
  PL("Light frequency", "Write freq_thz(nm): the frequency in terahertz of light with wavelength nm nanometres (c = 3e8 m/s), rounded to 1 decimal.", "freq_thz(nm)", """
def freq_thz(nm):
    return round(3e8 / (nm * 1e-9) / 1e12, 1)
""", [[700], [550], [450], [850]], "f = c / wavelength.", approx=1e-1),
  PL("Light sensor", "Write ldr_out(vcc, r_fixed, r_ldr): the divider voltage across the fixed resistor, rounded to 3 decimals.", "ldr_out(vcc, r_fixed, r_ldr)", """
def ldr_out(vcc, r_fixed, r_ldr):
    return round(vcc * r_fixed / (r_fixed + r_ldr), 3)
""", [[5, 10000, 1000], [5, 10000, 100000], [9, 4700, 4700]], "Fixed over the sum.", approx=1e-3),
  PL("Dimmer power", "Write dimmer(angle): a triac turns on at firing angle (0 to 180 degrees) of each half cycle. The fraction of full power delivered to a resistive load is 1 - angle/180 + sin(2 x angle)/(2 pi). Return it rounded to 3 decimals.", "dimmer(angle)", """
def dimmer(angle):
    import math
    a = math.radians(angle)
    return round(1 - angle / 180.0 + math.sin(2 * a) / (2 * math.pi), 3)
""", [[0], [90], [180], [45]], "Use radians for sin.", approx=1e-3)]))

B.append(CH(
 "Waves, signals and noise",
 ("Signals", ["Wave | repeats | In time", "Frequency | counts | Cycles per second", "Period | is | One cycle's time", "Amplitude | is | Size", "RMS | is | Equivalent DC", "Duty cycle | is | Time on", "Noise | hides | Signal"]),
 ["A signal is a voltage that changes with time. A wave repeats: frequency counts how many cycles each second, and the period is the time of one cycle.",
  "The effective value of an AC wave is its RMS value. A sine wave's RMS is its peak divided by the square root of two.",
  "Noise is unwanted signal, and engineers compare size with decibels."],
 [("Frequency", "Cycles per second, in hertz."), ("Period", "Time for one cycle: T = 1 / f."), ("RMS", "The DC value that gives the same heating."),
  ("Duty cycle", "The fraction of the time a pulse is on."), ("Peak to peak", "From the lowest to the highest value."), ("Decibel", "A logarithmic way to compare sizes.")],
 ["f = 1 / T.", "RMS of a sine = peak / 1.414.", "Mains 120 V RMS has a peak of about 170 V.", "Duty cycle = on time / period.", "Pulses and square waves carry digital information.", "dB = 20 log10 of a voltage ratio."],
 [T("A battery gives a flat line. Most useful signals change. Sound from a microphone, a radio wave, a heartbeat from a sensor and the clock inside a computer are all voltages that vary with time. An oscilloscope draws them on a screen."),
  M(r"f=\frac{1}{T}\qquad V_{\text{rms}}=\frac{V_{\text{peak}}}{\sqrt 2}\qquad \text{dB}=20\log_{10}\frac{V_2}{V_1}"),
  T("A wave that repeats has a frequency, in hertz, and a period, the time for one cycle. A 1000 hertz tone has a period of one millisecond. The amplitude says how big it is. A single number is useful for AC, the RMS value, which gives the same heating as a DC of the same size."),
  T("Pulses change between low and high. How long the pulse stays high, compared with the full period, is the duty cycle. Changing the duty cycle controls average power to a motor or the brightness of an LED without wasting heat."),
  T("Noise is any unwanted signal. It comes from nearby motors, lights and radios, and from the random motion of electrons inside parts. The signal to noise ratio says how much bigger your signal is than the noise. Engineers give it in decibels, because it covers huge ranges.")],
 [("What is the period of 50 Hz?", ["20 ms", "50 ms", "2 ms", "5 ms"], 0, "1 / 50."),
  ("What is a 100% duty cycle?", ["Always on", "Always off", "Half on", "Noise"], 0, "On the whole time."),
  ("What is RMS?", ["The equivalent DC heating value", "The peak", "The period", "The noise"], 0, "Effective value.")],
 [("What is f in terms of T?", "1 over T."), ("What is duty cycle?", "Fraction of time on."), ("What does a scope show?", "Voltage against time."), ("What is noise?", "Unwanted signal.")],
 [MATCH("Terms", "Match each term with its meaning.", [("Frequency", "Cycles per second"), ("Period", "Time of one cycle"), ("Amplitude", "Size of the wave"), ("Duty cycle", "Fraction of time on")]),
  PL("RMS", "Write rms(samples): the root mean square of the list, rounded to 4 decimals.", "rms(samples)", """
def rms(samples):
    import math
    t = 0.0
    for s in samples:
        t += s * s
    return round(math.sqrt(t / len(samples)), 4)
""", [[[1, -1, 1, -1]], [[3, 4]], [[0, 5, 0, -5]]], "Square, average, square root.", approx=1e-3),
  PL("Duty cycle", "Write duty(samples, threshold): the fraction of the samples that are at least threshold, rounded to 3 decimals.", "duty(samples, threshold)", """
def duty(samples, threshold):
    n = 0
    for s in samples:
        if s >= threshold:
            n += 1
    return round(n / len(samples), 3)
""", [[[0, 5, 5, 0], 2.5], [[5, 5, 5, 5], 2.5], [[0, 0, 0, 5], 2.5]], "Count the high samples.", approx=1e-3),
  PL("Decibels", "Write db(v_out, v_in): 20 x log10(v_out / v_in), rounded to 2 decimals.", "db(v_out, v_in)", """
def db(v_out, v_in):
    import math
    return round(20 * math.log10(v_out / v_in), 2)
""", [[10, 1], [1, 10], [2, 1], [1, 1]], "A voltage ratio, so 20.", approx=1e-2),
  PL("Peak from mains", "Write peaks(vrms): return [peak, peak_to_peak] of a sine wave with that RMS voltage, rounded to 1 decimal.", "peaks(vrms)", """
def peaks(vrms):
    import math
    p = vrms * math.sqrt(2)
    return [round(p, 1), round(2 * p, 1)]
""", [[120], [230], [1]], "peak = rms x 1.414.", approx=1e-1)]))

B.append(CH(
 "Digital logic: gates",
 ("Gates", ["Bit | is | 0 or 1", "AND | needs | All inputs", "OR | needs | One input", "NOT | flips | A bit", "NAND | is | Universal", "Truth table | lists | All results", "Binary | counts | In twos"]),
 ["Digital circuits use only two voltage levels, called low and high, written 0 and 1. A bit is one such digit.",
  "Logic gates combine bits: AND is 1 only if all inputs are 1, OR is 1 if any input is 1, and NOT flips a bit.",
  "With NAND gates alone you can build every other gate, so digital chips can be made from one repeating cell."],
 [("Bit", "A binary digit, 0 or 1."), ("Gate", "A circuit that outputs a logic function of its inputs."), ("Truth table", "A list of outputs for every input combination."),
  ("Binary", "Counting with only 0 and 1, base two."), ("Adder", "A circuit that adds binary numbers."), ("TTL and CMOS", "Two families of digital chips.")],
 ["AND: 1 only if both are 1.", "OR: 1 if either is 1.", "NOT: 1 becomes 0 and 0 becomes 1.", "NAND is AND then NOT; NOR is OR then NOT.", "XOR is 1 when the inputs differ.", "A half adder is XOR for the sum and AND for the carry."],
 [T("Digital circuits are simple on purpose. A signal is either low or high, so small noise does not change the meaning. This makes computers reliable, and it lets us build huge systems from small parts."),
  T("Binary counts using only two digits. Each place is a power of two: 1, 2, 4, 8, 16. The number 1011 in binary is 8 plus 2 plus 1, which is 11. A group of eight bits is a byte."),
  C("# truth table of AND, OR, XOR\nfor a in (0, 1):\n    for b in (0, 1):\n        print(a, b, a & b, a | b, a ^ b)", "python"),
  T("A logic gate has one or more inputs and one output. NAND is special. Its output is 0 only when all inputs are 1. Any other gate can be built from NAND gates, so it is called universal. Real chips are made from a few transistors per gate."),
  T("Gates combine to do arithmetic. A half adder adds two bits: the sum is XOR and the carry is AND. Chain two of them and an OR to make a full adder, which also takes a carry in. A row of full adders adds binary numbers of any length.")],
 [("When is AND true?", ["All inputs 1", "Any input 1", "No inputs 1", "Never"], 0, "Both must be 1."),
  ("What is 1011 in binary?", ["11", "13", "9", "7"], 0, "8 + 2 + 1."),
  ("Which gate is universal?", ["NAND", "AND", "XOR", "Buffer"], 0, "All gates can be built from it.")],
 [("What is a bit?", "0 or 1."), ("What does XOR do?", "1 when inputs differ."), ("What is a truth table?", "All outputs listed."), ("What is a byte?", "Eight bits.")],
 [MATCH("Gates", "Match each gate with its rule.", [("AND", "1 only if all inputs are 1"), ("OR", "1 if any input is 1"), ("XOR", "1 if inputs differ"), ("NAND", "0 only if all inputs are 1")]),
  PL("Logic expression", "Write logic(expr, values): expr is nested lists like ['and', 'a', ['not', 'b']]; operators 'and', 'or', 'not', 'xor', 'nand'; variables are names looked up in the dict values. Return 0 or 1.", "logic(expr, values)", """
def logic(expr, values):
    if isinstance(expr, str):
        return values[expr]
    op = expr[0]
    args = [logic(e, values) for e in expr[1:]]
    if op == 'not':
        return 1 - args[0]
    if op == 'and':
        return 1 if all(args) else 0
    if op == 'or':
        return 1 if any(args) else 0
    if op == 'xor':
        return args[0] ^ args[1]
    if op == 'nand':
        return 0 if all(args) else 1
    return 0
""", [[["and", "a", ["not", "b"]], {"a": 1, "b": 0}], [["or", "a", "b"], {"a": 0, "b": 0}], [["xor", "a", "b"], {"a": 1, "b": 0}], [["nand", "a", "b"], {"a": 1, "b": 1}]], "Evaluate arguments recursively.", approx=None),
  PL("Binary conversion", "Write to_binary(n, width): n as binary text, padded with zeros to at least width digits.", "to_binary(n, width)", """
def to_binary(n, width):
    s = ''
    while n > 0:
        s = str(n % 2) + s
        n = n // 2
    while len(s) < width:
        s = '0' + s
    return s
""", [[11, 4], [5, 8], [0, 3], [255, 8]], "Repeated division by two.", approx=None),
  PL("Ripple adder", "Write add_bits(a, b): a and b are equal-length lists of bits, least significant bit first. Add them with a chain of full adders and return the sum bits, least significant first, with one extra bit for the final carry.", "add_bits(a, b)", """
def add_bits(a, b):
    out = []
    carry = 0
    for x, y in zip(a, b):
        s = x ^ y ^ carry
        carry = (x & y) | (carry & (x ^ y))
        out.append(s)
    out.append(carry)
    return out
""", [[[1, 1, 0], [1, 0, 1]], [[1], [1]], [[0, 0], [0, 0]], [[1, 1, 1], [1, 1, 1]]], "sum = x xor y xor carry.", approx=None)]))

B.append(CH(
 "Sequential logic: memory and counting",
 ("Memory", ["Latch | holds | A bit", "Flip-flop | stores | One bit", "Clock | steps | Time", "Counter | counts | Pulses", "Register | holds | Many bits", "Shift register | moves | Bits", "Feedback | makes | Memory"]),
 ["Combinational logic only reacts to its current inputs. Sequential logic also remembers the past, because its outputs feed back into its inputs.",
  "A flip-flop stores one bit, and changes only on the edge of a clock. Several flip-flops make a counter, a register or a shift register.",
  "A clock is a steady stream of pulses that keeps a digital system in step."],
 [("Latch", "A circuit that holds one bit using feedback."), ("Flip-flop", "A clocked latch that changes only on a clock edge."), ("Clock", "A regular pulse that steps a digital circuit."),
  ("Counter", "A set of flip-flops that counts pulses."), ("Register", "A group of flip-flops holding a number."), ("Shift register", "A chain that moves bits one place per clock.")],
 ["A D flip-flop copies D to Q on the rising clock edge.", "A toggle flip-flop flips on each clock edge, so it halves the frequency.", "An n-bit counter counts from 0 to 2 to the n minus 1.", "A shift register turns serial data to parallel and back.", "Cross-coupled NOR or NAND gates form an SR latch.", "Count the bits: 4 flip-flops give 16 states."],
 [T("The gates in the last chapter forget. Change the input and the output follows at once. To make memory, feed the output back into the input. Two cross-coupled NAND gates make a latch with two stable states. It holds a bit as long as it has power."),
  T("A flip-flop is a latch that waits for a clock. A D flip-flop looks at its input only on the rising edge of the clock and copies it to the output. In between edges it ignores the input, so the circuit changes in neat steps."),
  T("Connect a flip-flop so that its output feeds its input inverted, and it flips at each clock pulse. Its output is half the clock frequency. Chain four such stages and you get a counter that counts in binary from zero to fifteen, then repeats."),
  C("# a 3-bit counter, in Python\ncount = 0\nfor tick in range(10):\n    count = (count + 1) % 8\n    print(tick, format(count, '03b') if False else count)", "python"),
  T("A shift register moves bits along a chain, one place per clock. Feed bits in one at a time and they come out in parallel, or the other way. Registers hold a number between operations. Together with gates, these parts make up the processor inside a computer.")],
 [("What does a D flip-flop copy?", ["D on the clock edge", "Q always", "The clock", "Ground"], 0, "Rising edge."),
  ("How many states have 4 flip-flops?", ["16", "4", "8", "32"], 0, "2 to the 4."),
  ("What makes a latch remember?", ["Feedback", "A battery", "A fuse", "A lens"], 0, "Output to input.")],
 [("What is a clock?", "A stream of pulses."), ("What is a register?", "Flip-flops holding a number."), ("What does a toggle do?", "Halves the frequency."), ("What is a shift register?", "A chain that moves bits.")],
 [MATCH("Memory parts", "Match each part with its job.", [("Latch", "Holds a bit using feedback"), ("Flip-flop", "Stores a bit on a clock edge"), ("Counter", "Counts pulses"), ("Shift register", "Moves bits along")]),
  PL("D flip-flop", "Write dff(d_values, clocks): both lists have the same length. The output starts at 0; whenever the clock list has a 1 after a 0 (a rising edge; the clock before the first sample is 0), the output copies the D value at that moment. Return the list of outputs.", "dff(d_values, clocks)", """
def dff(d_values, clocks):
    q = 0
    prev = 0
    out = []
    for d, c in zip(d_values, clocks):
        if c == 1 and prev == 0:
            q = d
        prev = c
        out.append(q)
    return out
""", [[[1, 0, 1, 1, 0], [0, 1, 0, 1, 1]], [[1, 1, 1], [1, 1, 1]], [[], []]], "Only change on a rising edge.", approx=None),
  PL("Binary counter", "Write counter(bits, pulses): an n-bit counter starts at 0. Return the list of its values after each of the pulses (it wraps around).", "counter(bits, pulses)", """
def counter(bits, pulses):
    out = []
    v = 0
    for _ in range(pulses):
        v = (v + 1) % (2 ** bits)
        out.append(v)
    return out
""", [[2, 6], [3, 3], [1, 4]], "Wrap with a remainder.", approx=None),
  PL("Shift register", "Write shift(bits, data): a shift register of the given length starts at all zeros. For each bit in data, shift everything one place to the right and insert the new bit at the left. Return the final contents as a list (left first).", "shift(bits, data)", """
def shift(bits, data):
    reg = [0] * bits
    for d in data:
        reg = [d] + reg[:-1]
    return reg
""", [[4, [1, 0, 1, 1]], [3, [1]], [2, []], [3, [1, 1, 1, 0]]], "Drop the last, add at the left.", approx=None),
  PL("SR latch", "Write sr_latch(events): events is a list of [s, r] pairs. Q starts at 0. [1, 0] sets Q to 1; [0, 1] resets it to 0; [0, 0] holds; [1, 1] is forbidden: treat it as hold. Return the list of Q values.", "sr_latch(events)", """
def sr_latch(events):
    q = 0
    out = []
    for s, r in events:
        if s == 1 and r == 0:
            q = 1
        elif s == 0 and r == 1:
            q = 0
        out.append(q)
    return out
""", [[[[1, 0], [0, 0], [0, 1], [0, 0]]], [[]], [[[1, 1], [1, 0], [1, 1]]]], "Hold when not set or reset.", approx=None)]))

B.append(CH(
 "Linear ICs: op-amps, timers and regulators",
 ("Linear ICs", ["Op-amp | amplifies | A difference", "Feedback | sets | Gain", "555 | makes | Pulses", "Regulator | holds | A voltage", "Comparator | decides | Higher or lower", "Linear | means | Continuous", "IC | packs | Many parts"]),
 ["An integrated circuit, or IC, packs many transistors and resistors onto one chip. Linear ICs handle continuous signals, while digital ones handle bits.",
  "An operational amplifier has huge gain, and feedback resistors set the exact gain. A 555 timer makes pulses and delays with two resistors and a capacitor.",
  "A voltage regulator holds a steady output voltage, whatever the input or load does."],
 [("IC", "Integrated circuit: a whole circuit on one chip."), ("Op-amp", "A high-gain differential amplifier."), ("Feedback", "Sending some output back to the input to control gain."),
  ("Comparator", "A circuit that tells which of two voltages is higher."), ("555 timer", "A popular chip for pulses and delays."), ("Regulator", "A chip that holds a fixed output voltage.")],
 ["Inverting gain = minus Rf / Rin.", "Non-inverting gain = 1 + Rf / Rg.", "A comparator's output swings to one supply rail or the other.", "555 astable: f = 1.44 / ((R1 + 2 R2) C).", "Linear regulator waste: (Vin - Vout) x I as heat.", "Add capacitors near the chip's supply pins."],
 [T("An integrated circuit puts a whole circuit on a tiny piece of silicon. You do not have to know every transistor inside. You just need to know what it does and how to connect it. Chips come in packages with numbered pins, counted from a notch or dot."),
  T("The operational amplifier, or op-amp, boosts the small difference between its two inputs. Its gain on its own is enormous, so you use feedback. A resistor from output back to input fixes the gain at a precise, predictable value, set only by resistors."),
  M(r"A_{\text{inv}}=-\frac{R_f}{R_{in}}\qquad A_{\text{non}}=1+\frac{R_f}{R_g}"),
  T("The 555 timer is one of the most popular chips ever made. With two resistors and one capacitor it runs as a free-running oscillator, called astable, making a steady train of pulses. With one resistor and one capacitor it makes a single timed pulse, called monostable."),
  M(r"f\approx\frac{1.44}{(R_1+2R_2)\,C}"),
  T("A linear voltage regulator, such as the 7805, turns an uneven input into a steady 5 volts. The extra voltage is burned off as heat, equal to the voltage drop times the current. For heavy loads, that heat needs a heat sink.")],
 [("What sets an op-amp's gain?", ["Feedback resistors", "The battery", "The case", "The clock"], 0, "Rf and Rin."),
  ("What does a comparator say?", ["Which input is higher", "The frequency", "The power", "The color"], 0, "A yes or no."),
  ("What heats a linear regulator?", ["The voltage drop times current", "The clock", "Light", "Noise"], 0, "Wasted power.")],
 [("What is feedback?", "Output sent back to input."), ("What is astable?", "Free-running."), ("Which regulator gives 5 V?", "The 7805."), ("Where does pin 1 go?", "Next to the notch or dot.")],
 [MATCH("Chips", "Match each chip with its job.", [("Op-amp", "Amplify a difference"), ("555", "Make pulses and delays"), ("Regulator", "Hold a steady voltage"), ("Comparator", "Decide which is higher")]),
  PL("Op-amp gain", "Write opamp_gain(mode, rf, r): mode is 'inverting' (r is Rin) or 'non' (r is Rg). Return the gain, rounded to 3 decimals.", "opamp_gain(mode, rf, r)", """
def opamp_gain(mode, rf, r):
    if mode == 'inverting':
        return round(-rf / r, 3)
    return round(1 + rf / r, 3)
""", [["inverting", 100000, 10000], ["non", 90000, 10000], ["inverting", 10000, 10000], ["non", 0, 1000]], "Two formulas.", approx=1e-3),
  PL("555 astable", "Write timer555(r1, r2, c): return [frequency_hz, duty] with f = 1.44 / ((r1 + 2 r2) c) and duty = (r1 + r2) / (r1 + 2 r2); round f to 2 decimals and duty to 3.", "timer555(r1, r2, c)", """
def timer555(r1, r2, c):
    f = 1.44 / ((r1 + 2 * r2) * c)
    d = (r1 + r2) / (r1 + 2.0 * r2)
    return [round(f, 2), round(d, 3)]
""", [[1000, 10000, 1e-6], [10000, 10000, 1e-7], [4700, 47000, 1e-5]], "Plug into the formulas.", approx=1e-2),
  PL("Regulator heat", "Write reg_heat(vin, vout, i): the power burned off in watts, rounded to 3 decimals, and the efficiency (vout / vin), rounded to 3. Return [watts, efficiency].", "reg_heat(vin, vout, i)", """
def reg_heat(vin, vout, i):
    return [round((vin - vout) * i, 3), round(vout / vin, 3)]
""", [[12, 5, 0.5], [9, 5, 1], [7, 5, 0.1]], "Drop times current.", approx=1e-3),
  PL("Comparator", "Write comparator(samples, ref, high, low): for each sample output high if it is above ref, otherwise low. Return the list.", "comparator(samples, ref, high, low)", """
def comparator(samples, ref, high, low):
    return [high if s > ref else low for s in samples]
""", [[[0, 1, 2, 3, 2, 1], 1.5, 5, 0], [[], 1, 5, 0], [[1, 1], 1, 9, -9]], "Compare each sample.", approx=None)]))

B.append(CH(
 "Building real circuits",
 ("Building", ["Breadboard | holds | Temporary circuits", "Solder | joins | Permanently", "Meter | measures | V, I and R", "Supply | powers | The circuit", "Datasheet | lists | Part limits", "Fuse | protects | Against overload", "Safety | comes | First"]),
 ["Start on a solderless breadboard, which lets you build, test and change circuits without tools. Move to soldering once a design works.",
  "A multimeter measures voltage, current and resistance. Check your supply and wiring before power goes on.",
  "Always respect limits: part ratings, battery capacity and especially mains voltage."],
 [("Breadboard", "A reusable board for temporary circuits."), ("Solder", "A metal alloy that melts to join parts."), ("Multimeter", "A tool that measures volts, amps and ohms."),
  ("Datasheet", "A maker's document listing a part's limits."), ("Fuse", "A deliberate weak link that blows on overload."), ("Heat sink", "A metal piece that carries heat away from a part.")],
 ["Test circuits on a breadboard before soldering.", "Measure voltage in parallel, current in series, resistance with power off.", "Heat both the pad and the lead, then add solder.", "A good joint is shiny and shaped like a small cone.", "Read the datasheet for pinouts and maximum ratings.", "Never experiment with wall power. Use batteries or low-voltage supplies."],
 [T("A breadboard has rows of small spring clips. You push component leads in and the clips connect them in rows. There is nothing to heat or cut, so mistakes are cheap. Most designs in this course can be tried on one."),
  T("A multimeter is your eyes. To measure voltage, touch the probes across the part, in parallel. To measure current, break the circuit and put the meter in series. To measure resistance, switch the circuit off and take the part out of the circuit if you can."),
  T("When a design works, you can solder it. Heat the pad and the lead together for a second or two, then touch solder to the joint, not the iron. Let the solder flow, then remove the solder and the iron. A good joint is smooth and shiny. A dull, lumpy one is probably a cold joint."),
  T("Power comes from batteries or a regulated supply. Work out how long a battery will last: capacity in milliampere-hours divided by the current in milliamperes, and then be pessimistic. Fit a fuse when the supply could deliver a dangerous current."),
  T("Before you finish, check the basics. Is every polarity right? Do your parts stay under their ratings? Is each power pin decoupled? And remember: low voltage batteries are safe to learn on. Mains power can kill. If a project needs it, get proper training and use a tested, enclosed supply.")],
 [("How do you measure voltage?", ["Across the part", "In series", "With power off", "With a fuse"], 0, "In parallel."),
  ("What does a good solder joint look like?", ["Shiny", "Dull and lumpy", "Black", "Wet"], 0, "Smooth and shiny."),
  ("Where do you find a part's limits?", ["In the datasheet", "On the breadboard", "In the solder", "On the meter"], 0, "From the maker.")],
 [("Why use a breadboard?", "Cheap changes."), ("How to measure current?", "In series."), ("What is a datasheet?", "A part's limits and pins."), ("What blows to protect a circuit?", "A fuse.")],
 [MATCH("Tools", "Match each tool with its use.", [("Breadboard", "Build without soldering"), ("Multimeter", "Measure volts, amps, ohms"), ("Soldering iron", "Join parts permanently"), ("Fuse", "Protect against overload")]),
  PL("Battery life", "Write runtime(mah, load_ma, usable): the hours a battery of mah capacity lasts at load_ma, if only the fraction usable can be drawn. Round to 2 decimals.", "runtime(mah, load_ma, usable)", """
def runtime(mah, load_ma, usable):
    return round(mah * usable / load_ma, 2)
""", [[2000, 100, 0.8], [500, 25, 1.0], [9000, 300, 0.7]], "Capacity over load.", approx=1e-2),
  PL("Fuse choice", "Write fuse(load_a, margin): pick the smallest standard fuse from [0.1, 0.25, 0.5, 1, 2, 5, 10] amperes that is at least load_a x margin. Return 0 if none is big enough.", "fuse(load_a, margin)", """
def fuse(load_a, margin):
    need = load_a * margin
    for f in [0.1, 0.25, 0.5, 1, 2, 5, 10]:
        if f >= need - 1e-9:
            return f
    return 0
""", [[0.3, 1.25], [1.5, 1.25], [9, 1.5], [0.05, 2]], "The first one that fits.", approx=None),
  PL("Meter reading", "Write reading(kind, v, r): kind is 'volts' (return v), 'amps' (return v / r, rounded to 4 decimals) or 'ohms' (return r). Used to check a resistor in a simple circuit.", "reading(kind, v, r)", """
def reading(kind, v, r):
    if kind == 'volts':
        return v
    if kind == 'amps':
        return round(v / r, 4)
    return r
""", [["volts", 9, 100], ["amps", 9, 100], ["ohms", 9, 470]], "Ohm's law for amps.", approx=1e-4),
  PL("Wire resistance", "Write wire_r(length_m, area_mm2): the resistance of copper wire in ohms (resistivity 0.0172 ohm mm2 per metre), rounded to 4 decimals.", "wire_r(length_m, area_mm2)", """
def wire_r(length_m, area_mm2):
    return round(0.0172 * length_m / area_mm2, 4)
""", [[10, 0.5], [1, 1.5], [100, 2.5]], "Resistance grows with length.", approx=1e-4)]))
