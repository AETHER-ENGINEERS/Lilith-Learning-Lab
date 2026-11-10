"""Electronics course, chapters 1-7. Original text."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

A = []

A.append(CH(
 "Charge, current and voltage",
 ("Electricity", ["Charge | flows as | Current", "Voltage | pushes | Charge", "Conductor | lets | Current pass", "Insulator | blocks | Current", "DC | flows | One way", "AC | reverses | Direction", "Circuit | is | A closed loop"]),
 ["Everything is made of atoms, and atoms hold electrons that carry negative charge. Electricity is what happens when charge moves or builds up.",
  "Current is the flow of charge, measured in amperes. Voltage is the push behind it, measured in volts.",
  "Direct current flows one way, like from a battery. Alternating current keeps reversing, like from a wall outlet."],
 [("Charge", "A property of matter; electrons are negative."), ("Current", "The rate of flow of charge, in amperes (A)."), ("Voltage", "The push that moves charge, in volts (V)."),
  ("Conductor", "A material that lets current flow easily, like copper."), ("Insulator", "A material that blocks current, like rubber."), ("Circuit", "A closed path that current can follow.")],
 ["One ampere is one coulomb of charge per second.", "Voltage is measured between two points.", "Metals conduct; glass, plastic and dry air insulate.", "Static electricity is charge that sits still until it jumps.", "DC has a fixed direction; AC reverses many times a second.", "Current needs a complete loop to flow."],
 [T("Rub a balloon on your hair and it sticks to the wall. You moved electrons from one thing to another, and the extra charge stays put. That is static electricity. When it finds a path, it jumps as a spark."),
  T("Current is charge on the move. If one coulomb passes a point each second, the current is one ampere. Voltage is the push that makes it move. A battery has voltage between its two ends, and when you connect a path between them, the push drives current around."),
  M(r"I=\frac{Q}{t}"),
  T("Materials differ in how easily charge moves. Metals such as copper are conductors, because their outer electrons are free to wander. Plastic, rubber and glass are insulators. Semiconductors, such as silicon, sit in between, and they are the base of modern electronics."),
  T("A battery gives direct current, or DC, which flows one way. The outlet in a wall gives alternating current, or AC, which swings back and forth, often 50 or 60 times a second. Wall power can be dangerous. Learn on batteries, and treat mains with great respect.")],
 [("What does an ampere measure?", ["Current", "Voltage", "Resistance", "Power"], 0, "Charge per second."),
  ("Which is an insulator?", ["Rubber", "Copper", "Silver", "Iron"], 0, "It blocks current."),
  ("Which current changes direction?", ["AC", "DC", "Static", "None"], 0, "Alternating.")],
 [("What is voltage?", "The push on charge."), ("What is a circuit?", "A closed loop."), ("DC or AC from a battery?", "DC."), ("What is a semiconductor?", "Between conductor and insulator.")],
 [MATCH("Units", "Match each quantity with its unit.", [("Current", "ampere"), ("Voltage", "volt"), ("Resistance", "ohm"), ("Frequency", "hertz")]),
  PL("Current from charge", "Write current(charge, seconds): the current in amperes.", "current(charge, seconds)", """
def current(charge, seconds):
    return charge / seconds
""", [[10, 5], [1, 2], [0.5, 0.25]], "I = Q / t.", approx=1e-6),
  PL("Unit prefixes", "Write convert(value, src, dst): convert between the prefixes 'p' (1e-12), 'n' (1e-9), 'u' (1e-6), 'm' (1e-3), '' (1), 'k' (1e3) and 'M' (1e6). Round to 6 decimals.", "convert(value, src, dst)", """
def convert(value, src, dst):
    f = {'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, '': 1.0, 'k': 1e3, 'M': 1e6}
    return round(value * f[src] / f[dst], 6)
""", [[2200, "", "k"], [4.7, "u", "n"], [10, "k", ""], [500, "m", ""]], "Go through the base unit.", approx=1e-6),
  PL("Battery pack", "Write pack(volts, mah, series, parallel): cells in series add voltage; cells in parallel add capacity. Return [total_volts, total_mah].", "pack(volts, mah, series, parallel)", """
def pack(volts, mah, series, parallel):
    return [volts * series, mah * parallel]
""", [[1.5, 2000, 4, 1], [3.7, 3000, 1, 2], [1.2, 800, 2, 3]], "Series adds volts.", approx=1e-6)]))

A.append(CH(
 "Ohm's law, power and simple circuits",
 ("Ohm", ["Ohm's law | links | V, I and R", "Resistance | limits | Current", "Power | is | V times I", "Series | shares | Voltage", "Parallel | shares | Current", "Load | uses | Power", "Watt | measures | Power"]),
 ["Ohm's law says voltage equals current times resistance. If you know two, you can find the third.",
  "Electrical power is voltage times current, measured in watts. A part that gets too much power gets hot.",
  "Resistors in series add up. In parallel, the total is smaller than the smallest one."],
 [("Ohm's law", "V = I x R."), ("Resistance", "How strongly a part opposes current, in ohms."), ("Power", "Rate of energy use: P = V x I, in watts."),
  ("Series", "Parts joined end to end, with the same current."), ("Parallel", "Parts joined side by side, with the same voltage."), ("Load", "The part that uses the electrical power.")],
 ["V = I x R, so I = V / R and R = V / I.", "P = V x I = I squared x R = V squared / R.", "Series resistors add: R = R1 + R2 + ...", "Parallel: 1 / R = 1 / R1 + 1 / R2 + ...", "In series, voltages add up to the supply.", "In parallel, currents add up."],
 [T("Georg Ohm found that for many materials the current is proportional to the voltage. Double the voltage and the current doubles. The constant is the resistance. This one rule solves most beginner circuit problems."),
  M(r"V=I\,R\qquad P=V\,I=I^{2}R=\frac{V^{2}}{R}"),
  T("A 9 volt battery across a 900 ohm resistor gives 0.01 amperes, which is 10 milliamperes. The power is 9 times 0.01, which is 0.09 watts. A small resistor rated for a quarter watt can handle that."),
  T("In a series circuit, there is only one path. The same current runs through every part, and the voltages add up to the supply. In a parallel circuit, each branch gets the full voltage, and the branch currents add up. Home wiring is parallel so each device gets the full voltage."),
  M(r"R_{\text{series}}=R_1+R_2+\cdots\qquad \frac{1}{R_{\text{par}}}=\frac{1}{R_1}+\frac{1}{R_2}+\cdots"),
  T("Always check the power. A resistor that dissipates more than its rating overheats and may burn. A common habit is to choose a rating at least twice the power you calculate.")],
 [("What is the current for 9 V across 900 ohms?", ["10 mA", "1 A", "100 mA", "81 A"], 0, "9 / 900."),
  ("What happens to resistance in parallel?", ["Total is smaller", "Total is larger", "No change", "Zero"], 0, "More paths."),
  ("What is P with 2 A and 5 V?", ["10 W", "7 W", "2.5 W", "0.4 W"], 0, "P = V x I.")],
 [("What is Ohm's law?", "V = I R."), ("What is P?", "V times I."), ("Series resistors do what?", "Add."), ("Parallel voltage?", "The same on each branch.")],
 [FILL("Ohm", "Voltage equals current times {{resistance}}, and power is voltage times {{current}}."),
  PL("Ohm solver", "Write ohm(v, i, r): exactly one of the three is None. Return the missing one, rounded to 4 decimals.", "ohm(v, i, r)", """
def ohm(v, i, r):
    if v is None:
        return round(i * r, 4)
    if i is None:
        return round(v / r, 4)
    return round(v / i, 4)
""", [[9, None, 900], [None, 0.02, 100], [12, 0.5, None], [5, None, 220]], "Pick the right form.", approx=1e-4),
  PL("Series and parallel", "Write combine(values, mode): mode is 'series' or 'parallel'. Return the total resistance rounded to 4 decimals.", "combine(values, mode)", """
def combine(values, mode):
    if mode == 'series':
        return round(sum(values), 4)
    inv = 0.0
    for r in values:
        inv += 1.0 / r
    return round(1.0 / inv, 4)
""", [[[100, 200, 300], "series"], [[100, 100], "parallel"], [[10, 20, 40], "parallel"], [[47], "parallel"]], "Add inverses in parallel.", approx=1e-4),
  PL("Resistor power", "Write rating(v, r): return the power in watts across the resistor, rounded to 4 decimals, and the smallest standard rating from [0.125, 0.25, 0.5, 1, 2, 5] that is at least double that power (or 0 if none). Return [power, rating].", "rating(v, r)", """
def rating(v, r):
    p = v * v / r
    for s in [0.125, 0.25, 0.5, 1, 2, 5]:
        if s >= 2 * p:
            return [round(p, 4), s]
    return [round(p, 4), 0]
""", [[9, 900], [12, 100], [5, 1000], [50, 10]], "Compare double the power.", approx=1e-4)]))

A.append(CH(
 "Resistors",
 ("Resistors", ["Resistor | limits | Current", "Color code | tells | Value", "Tolerance | is | Accuracy", "Divider | makes | A smaller voltage", "Pot | varies | Resistance", "Wattage | is | Power rating", "Preferred values | are | Standard steps"]),
 ["A resistor limits current. Small ones carry colored bands that give their value, and a final band gives tolerance.",
  "Two resistors in series form a voltage divider, which outputs a fraction of the input voltage.",
  "A potentiometer is a resistor with a sliding contact, so you can adjust it."],
 [("Resistor", "A part that opposes current by a set amount."), ("Tolerance", "How far the real value may differ, such as 5 percent."), ("Voltage divider", "Two resistors in series that give a fraction of the voltage."),
  ("Potentiometer", "A variable resistor with a wiper."), ("Rating", "The most power a resistor can handle safely."), ("E12 series", "A set of 12 preferred values per decade.")],
 ["Bands: digit, digit, multiplier, tolerance.", "Colors: black 0, brown 1, red 2, orange 3, yellow 4, green 5, blue 6, violet 7, gray 8, white 9.", "Gold tolerance is 5 percent, silver 10 percent.", "Vout = Vin x R2 / (R1 + R2).", "A divider only holds when the load draws little current.", "Common ratings are 1/8, 1/4 and 1/2 watt."],
 [T("The simplest job for a resistor is to limit current. Put one in series with an LED so the LED does not burn out. Resistors also set bias for transistors, divide voltages and pull inputs up or down."),
  T("Small resistors are too tiny for printed numbers, so they use colored bands. Read from the end that has the bands closest together. The first two bands are digits. The third is how many zeros to add. The last shows tolerance."),
  C("# brown black red gold\ndigits = [1, 0]\nmultiplier = 10 ** 2\nvalue = (digits[0] * 10 + digits[1]) * multiplier\nprint(value)   # 1000 ohms, 5 percent", "python"),
  T("Two resistors in series from the supply to ground make a voltage divider. The voltage at the joint is a fraction of the supply set by their ratio. It is the base of many sensors, such as a light-dependent resistor in series with a fixed one."),
  M(r"V_{\text{out}}=V_{\text{in}}\,\frac{R_2}{R_1+R_2}"),
  T("A potentiometer, or pot, is a resistor with a third terminal that slides along it. Turn the knob and the divider ratio changes. Volume controls use this idea. Remember that a divider falls apart if you connect a heavy load to its output.")],
 [("What does the third band mean?", ["Multiplier", "Tolerance", "Power", "Voltage"], 0, "How many zeros."),
  ("What color is 2?", ["Red", "Brown", "Orange", "Green"], 0, "Brown 1, red 2."),
  ("What does a divider produce?", ["A fraction of the input voltage", "More current", "AC", "Heat only"], 0, "R2 over the sum.")],
 [("What does gold mean?", "5 percent tolerance."), ("What is a pot?", "A variable resistor."), ("What is a divider?", "Two resistors giving a fraction."), ("What is the E12 series?", "Preferred values.")],
 [MATCH("Colors", "Match each color with its digit.", [("brown", "1"), ("red", "2"), ("yellow", "4"), ("violet", "7")]),
  PL("Color code", "Write color_code(bands): bands is a list of four color names (digit, digit, multiplier, tolerance). Return [ohms, tolerance_percent]. Colors: black 0, brown 1, red 2, orange 3, yellow 4, green 5, blue 6, violet 7, gray 8, white 9. Tolerance: gold 5, silver 10.", "color_code(bands)", """
def color_code(bands):
    c = ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'gray', 'white']
    ohms = (c.index(bands[0]) * 10 + c.index(bands[1])) * 10 ** c.index(bands[2])
    tol = 5 if bands[3] == 'gold' else 10
    return [ohms, tol]
""", [[["brown", "black", "red", "gold"]], [["yellow", "violet", "orange", "silver"]], [["green", "blue", "brown", "gold"]], [["orange", "orange", "black", "gold"]]], "Use the index in the color list.", approx=None),
  PL("Divider", "Write divider(vin, r1, r2): the output voltage rounded to 4 decimals.", "divider(vin, r1, r2)", """
def divider(vin, r1, r2):
    return round(vin * r2 / (r1 + r2), 4)
""", [[9, 1000, 2000], [5, 10000, 10000], [12, 330, 470]], "R2 over the sum.", approx=1e-4),
  PL("Tolerance range", "Write limits(value, percent): the lowest and highest actual resistance as [low, high], rounded to 4 decimals.", "limits(value, percent)", """
def limits(value, percent):
    d = value * percent / 100.0
    return [round(value - d, 4), round(value + d, 4)]
""", [[1000, 5], [4700, 10], [220, 1]], "Add and subtract the tolerance.", approx=1e-4),
  PL("Nearest E12", "Write nearest_e12(value): the closest standard E12 value (use the table 1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2 times a power of ten). Compare ratios, and on a tie pick the lower. Return it rounded to 2 decimals.", "nearest_e12(value)", """
def nearest_e12(value):
    import math
    base = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
    p = math.floor(math.log10(value))
    best = None
    bd = None
    for q in [p - 1, p, p + 1]:
        for b in base + [10.0]:
            c = b * 10 ** q
            d = abs(math.log(c / value))
            if bd is None or d < bd - 1e-12:
                bd = d
                best = c
    return round(best, 2)
""", [[1000], [2000], [470], [3000], [68]], "Compare on a log scale.", approx=1e-2)]))

A.append(CH(
 "Capacitors and timing",
 ("Capacitors", ["Capacitor | stores | Charge", "Farad | measures | Capacitance", "RC | sets | A time", "Charging | follows | A curve", "Series | lowers | Capacitance", "Parallel | adds | Capacitance", "Coupling | passes | AC, blocks DC"]),
 ["A capacitor stores charge on two plates separated by an insulator. Capacitance is measured in farads, though real parts are microfarads and smaller.",
  "With a resistor, a capacitor makes a timer. The time constant is R times C, in seconds.",
  "A capacitor blocks steady DC but lets changing signals through, which makes it useful for filtering and coupling."],
 [("Capacitor", "A part that stores energy in an electric field."), ("Farad", "The unit of capacitance."), ("Time constant", "R x C; the time to reach about 63 percent."),
  ("Electrolytic", "A large capacitor with a polarity; wrong way round can fail."), ("Coupling", "Passing AC while blocking DC."), ("Decoupling", "Smoothing the supply close to a chip.")],
 ["Q = C x V.", "Energy stored is one half C V squared.", "Parallel capacitors add; series capacitors combine like parallel resistors.", "Charging: V(t) = Vs x (1 - e to the minus t over RC).", "After 5 time constants it is about 99 percent charged.", "Electrolytic capacitors have a plus and a minus side."],
 [T("Two metal plates with a gap between them hold charge. Put a voltage across them and they charge up. Take the voltage away and they keep the charge for a while. More plate area and a smaller gap give more capacitance."),
  M(r"Q=C\,V\qquad E=\tfrac12 C V^{2}"),
  T("When you charge a capacitor through a resistor, it does not fill instantly. It starts fast and slows down. The product of R and C is the time constant. After one time constant it has reached about 63 percent of the supply, and after five it is nearly full."),
  M(r"V(t)=V_s\left(1-e^{-t/RC}\right)"),
  T("Capacitors do many jobs. They smooth the ripple in a power supply. They pass audio between stages while blocking the DC bias. They set delays and oscillator speeds. Electrolytic types have a polarity mark, so check it, or the part may fail.")],
 [("What is the unit of capacitance?", ["Farad", "Henry", "Ohm", "Volt"], 0, "Named after Faraday."),
  ("What does the time constant equal?", ["R x C", "R + C", "R / C", "V x I"], 0, "In seconds."),
  ("What do parallel capacitors do?", ["Add up", "Cancel", "Halve", "Block AC"], 0, "More plate area.")],
 [("What does a capacitor store?", "Charge."), ("When is it about 63 percent charged?", "After one time constant."), ("What do electrolytics need?", "Correct polarity."), ("What does coupling do?", "Passes AC, blocks DC.")],
 [MATCH("Roles", "Match each use with its job.", [("Smoothing", "Reduce ripple in a supply"), ("Coupling", "Pass AC, block DC"), ("Timing", "Set a delay with a resistor"), ("Decoupling", "Steady the supply near a chip")]),
  PL("Time constant", "Write tau(r, c): R times C in seconds, rounded to 6 decimals.", "tau(r, c)", """
def tau(r, c):
    return round(r * c, 6)
""", [[10000, 0.0001], [1000, 1e-6], [4700, 0.00047]], "R x C.", approx=1e-6),
  PL("Capacitor voltage", "Write vcap(vs, r, c, t): the voltage on a capacitor t seconds after charging starts, rounded to 4 decimals.", "vcap(vs, r, c, t)", """
def vcap(vs, r, c, t):
    import math
    return round(vs * (1 - math.exp(-t / (r * c))), 4)
""", [[9, 10000, 0.0001, 1.0], [5, 1000, 1e-6, 0.001], [12, 1000, 0.001, 5.0], [9, 1000, 0.001, 0]], "Use exp.", approx=1e-3),
  PL("Combine capacitors", "Write cap_total(values, mode): 'parallel' adds; 'series' combines as 1 / sum(1 / c). Rounded to 6 decimals.", "cap_total(values, mode)", """
def cap_total(values, mode):
    if mode == 'parallel':
        return round(sum(values), 6)
    inv = 0.0
    for c in values:
        inv += 1.0 / c
    return round(1.0 / inv, 6)
""", [[[1e-6, 2e-6], "parallel"], [[1e-6, 1e-6], "series"], [[10, 40], "series"]], "Opposite to resistors.", approx=1e-6),
  PL("Time to reach", "Write time_to(vs, r, c, v): how many seconds a capacitor takes to charge to v (v is less than vs), rounded to 4 decimals.", "time_to(vs, r, c, v)", """
def time_to(vs, r, c, v):
    import math
    return round(-r * c * math.log(1 - v / vs), 4)
""", [[9, 10000, 0.0001, 5.7], [5, 1000, 1e-6, 2.5], [12, 1000, 0.001, 6]], "Solve for t with a log.", approx=1e-3)]))

A.append(CH(
 "Coils, transformers, switches and relays",
 ("Magnetic parts", ["Coil | stores | Magnetic energy", "Henry | measures | Inductance", "Reactance | resists | AC", "Resonance | picks | One frequency", "Transformer | changes | AC voltage", "Relay | switches | With a coil", "Switch | opens | A path"]),
 ["Current through a coil makes a magnetic field. A coil resists changes in current, and that property is called inductance.",
  "Capacitors and coils oppose AC in a way that depends on frequency, called reactance. A coil and capacitor together resonate at one frequency.",
  "A transformer changes AC voltage using two coils, and a relay lets a small current switch a bigger one."],
 [("Inductor", "A coil that stores energy in a magnetic field."), ("Henry", "The unit of inductance."), ("Reactance", "A coil's or capacitor's opposition to AC, in ohms."),
  ("Resonance", "The frequency where coil and capacitor reactances cancel."), ("Transformer", "Two coils on a core that change AC voltage."), ("Relay", "An electromagnetic switch.")],
 ["Coil reactance X_L = 2 pi f L; it grows with frequency.", "Capacitor reactance X_C = 1 / (2 pi f C); it shrinks with frequency.", "Resonance: f = 1 / (2 pi sqrt(L C)).", "Transformer: Vs / Vp = Ns / Np.", "A transformer works only with changing current, not DC.", "Put a diode across a relay coil to absorb the voltage spike."],
 [T("A wire carrying current makes a magnetic field. Wind the wire into a coil and the effect multiplies. A coil fights sudden changes of current, so it acts as a kind of electrical inertia. It is measured in henries, usually millihenries in electronics."),
  M(r"X_L=2\pi f L\qquad X_C=\frac{1}{2\pi f C}\qquad f_0=\frac{1}{2\pi\sqrt{LC}}"),
  T("Reactance is like resistance for AC. A coil passes low frequencies and resists high ones. A capacitor does the opposite. At one special frequency, the two cancel, and the circuit resonates. Radio tuners use this to pick one station."),
  T("A transformer has two coils on one core. AC in the first makes a changing magnetic field, which pushes AC in the second. The voltage ratio equals the turns ratio. A step-down transformer, with fewer turns on the output, gives a lower voltage and a higher current."),
  T("A relay is a switch operated by a coil. A small current in the coil pulls a contact, which switches a much bigger current. It also keeps the control side apart from the load. When the coil switches off, it kicks a voltage spike, so a diode across the coil protects the rest of the circuit.")],
 [("What does a transformer need?", ["Changing current", "Steady DC", "Light", "A battery only"], 0, "AC."),
  ("What does X_L do as frequency rises?", ["Grows", "Shrinks", "Stays", "Vanishes"], 0, "2 pi f L."),
  ("What protects a relay driver?", ["A diode across the coil", "A bigger coil", "More voltage", "Nothing"], 0, "Absorbs the spike.")],
 [("What is resonance?", "Reactances cancel."), ("What is a henry?", "Unit of inductance."), ("Step-down means?", "Lower voltage out."), ("Why isolate with a relay?", "Control and load stay apart.")],
 [MATCH("Parts", "Match each part with its job.", [("Inductor", "Stores energy in a magnetic field"), ("Transformer", "Changes AC voltage"), ("Relay", "Switches with a coil"), ("Capacitor", "Stores charge")]),
  PL("Reactance", "Write reactance(kind, f, value): kind is 'L' (henries) or 'C' (farads); return the reactance in ohms rounded to 3 decimals.", "reactance(kind, f, value)", """
def reactance(kind, f, value):
    import math
    if kind == 'L':
        return round(2 * math.pi * f * value, 3)
    return round(1 / (2 * math.pi * f * value), 3)
""", [["L", 1000, 0.01], ["C", 1000, 1e-6], ["C", 50, 0.0001], ["L", 60, 1]], "Two formulas.", approx=1e-3),
  PL("Resonant frequency", "Write resonance(l, c): the resonant frequency in hertz, rounded to 2 decimals.", "resonance(l, c)", """
def resonance(l, c):
    import math
    return round(1 / (2 * math.pi * math.sqrt(l * c)), 2)
""", [[0.01, 1e-6], [1e-3, 1e-9], [0.1, 0.0001]], "1 / (2 pi sqrt LC).", approx=1e-3),
  PL("Transformer", "Write transformer(vp, np, ns): the secondary voltage, rounded to 3 decimals.", "transformer(vp, np, ns)", """
def transformer(vp, np, ns):
    return round(vp * ns / np, 3)
""", [[120, 1000, 100], [230, 1000, 52], [12, 50, 500]], "Voltage follows the turns ratio.", approx=1e-3),
  PL("Relay logic", "Write relay_state(events, hold): events is a list of coil currents in mA per time step. The relay closes when the current is at least 20 and stays closed until the current falls below hold. Return the list of states (1 closed, 0 open).", "relay_state(events, hold)", """
def relay_state(events, hold):
    out = []
    closed = 0
    for i in events:
        if closed:
            if i < hold:
                closed = 0
        elif i >= 20:
            closed = 1
        out.append(closed)
    return out
""", [[[0, 25, 15, 8, 25], 10], [[], 10], [[30, 12, 12], 15]], "Pull in at 20, drop out below the hold value.", approx=None)]))

A.append(CH(
 "Diodes and LEDs",
 ("Diodes", ["Semiconductor | sits between | Metal and insulator", "Diode | passes | One direction", "Forward drop | is | About 0.7 V", "Rectifier | makes | AC into DC", "Zener | holds | A voltage", "LED | emits | Light", "Resistor | limits | LED current"]),
 ["A diode lets current go one way and blocks it the other. A silicon diode drops about 0.6 to 0.7 volts when it conducts.",
  "Rectifiers use diodes to change AC into pulsing DC. A Zener diode is used backwards to hold a steady voltage.",
  "An LED is a diode that gives off light, and it always needs a resistor to limit its current."],
 [("Diode", "A part that conducts mainly one way."), ("Forward voltage", "The drop across a conducting diode."), ("Rectifier", "A circuit that turns AC into DC."),
  ("Zener diode", "A diode that conducts backwards at a set voltage."), ("LED", "A light-emitting diode."), ("Anode and cathode", "The positive and negative ends of a diode.")],
 ["Silicon diode forward drop is about 0.7 V; a red LED is about 2 V.", "The stripe on a diode marks the cathode.", "A half-wave rectifier uses one diode, a full-wave one uses four in a bridge.", "A bridge loses about 1.4 V (two drops).", "LED resistor: R = (Vsupply - Vled) / I.", "Add a capacitor after the rectifier to smooth the ripple."],
 [T("Silicon is the base of electronics. In its pure state it conducts poorly. Adding tiny amounts of other atoms makes either an N type, with extra electrons, or a P type, with missing ones, called holes. Join an N and a P piece and you get a PN junction, which is a diode."),
  T("A diode is like a one-way valve. Forward-biased, with the positive on the anode, it conducts after about 0.7 volts. Reversed, it blocks. Real diodes break down if the reverse voltage is too high."),
  T("AC swings positive and negative. One diode passes only the positive half, which makes a half-wave rectifier. Four diodes in a bridge turn both halves the same way, giving full-wave. A capacitor across the output fills the gaps and smooths the result."),
  C("# an LED on a 9 V battery\nv_supply = 9\nv_led = 2.0\ni = 0.015          # 15 mA\nr = (v_supply - v_led) / i\nprint(round(r))    # 467 ohms, use 470", "python"),
  T("An LED makes light when current flows, but it has almost no resistance by itself. Without a resistor it draws too much and burns out. Use the formula with the LED's forward voltage. A Zener diode has a different trick: used in reverse, it conducts at a set voltage and holds it steady.")],
 [("Which end does the stripe mark?", ["Cathode", "Anode", "Gate", "Base"], 0, "Negative side."),
  ("Why does an LED need a resistor?", ["To limit current", "To make light", "To add voltage", "To cool it"], 0, "Or it burns out."),
  ("What does a bridge use?", ["Four diodes", "One diode", "Two coils", "A relay"], 0, "Full-wave.")],
 [("Silicon drop?", "About 0.7 V."), ("What is a Zener for?", "Holding a voltage."), ("What does a rectifier do?", "AC to DC."), ("What is a hole?", "A missing electron.")],
 [MATCH("Diodes", "Match each part with its use.", [("Rectifier diode", "AC to DC"), ("Zener diode", "Voltage reference"), ("LED", "Light"), ("Photodiode", "Light detector")]),
  PL("LED resistor", "Write led_resistor(vs, vf, i): the resistor in ohms for current i amperes, rounded to 2 decimals, and the next higher E12 value (1.0 1.2 1.5 1.8 2.2 2.7 3.3 3.9 4.7 5.6 6.8 8.2 times a power of ten). Return [exact, standard].", "led_resistor(vs, vf, i)", """
def led_resistor(vs, vf, i):
    import math
    r = (vs - vf) / i
    base = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2, 10.0]
    p = math.floor(math.log10(r))
    best = None
    for b in base:
        c = b * 10 ** p
        if c >= r - 1e-9:
            best = c
            break
    return [round(r, 2), round(best, 2)]
""", [[9, 2.0, 0.015], [5, 2.0, 0.02], [12, 3.2, 0.01], [3.3, 2.0, 0.005]], "Round up to a standard value.", approx=1e-2),
  PL("Rectify", "Write rectify(samples, mode): samples is a list of voltages. 'half' keeps the positive ones and sets negatives to 0; 'full' gives the absolute value. Ignore diode drops.", "rectify(samples, mode)", """
def rectify(samples, mode):
    out = []
    for s in samples:
        if mode == 'half':
            out.append(s if s > 0 else 0)
        else:
            out.append(abs(s))
    return out
""", [[[1, -1, 2, -2], "half"], [[1, -1, 2, -2], "full"], [[], "half"]], "Think of the diode as a valve.", approx=None),
  PL("Zener regulator", "Write zener_r(vin, vz, i_load, i_zener): the series resistor, rounded to 2 decimals, and its power in watts, rounded to 3. Return [r, p].", "zener_r(vin, vz, i_load, i_zener)", """
def zener_r(vin, vz, i_load, i_zener):
    i = i_load + i_zener
    r = (vin - vz) / i
    p = (vin - vz) * i
    return [round(r, 2), round(p, 3)]
""", [[12, 5.1, 0.02, 0.005], [9, 5.6, 0.01, 0.005], [15, 12, 0.05, 0.01]], "The resistor carries both currents.", approx=1e-3)]))

A.append(CH(
 "Transistors",
 ("Transistors", ["Transistor | controls | A big current", "Base | takes | A small current", "Collector | carries | The load current", "Gain | multiplies | Current", "Saturation | is | Fully on", "FET | uses | Voltage", "Switch | is | A key use"]),
 ["A transistor lets a small signal control a larger current. It can act as an amplifier or as an electronic switch.",
  "In a bipolar transistor, a small base current controls a collector current that is hundreds of times bigger.",
  "A field-effect transistor, or FET, is controlled by voltage on its gate and takes almost no current to do it."],
 [("Transistor", "A three-terminal part where one terminal controls current between the others."), ("Base", "The control terminal of a bipolar transistor."), ("Gain (hFE)", "Collector current divided by base current."),
  ("Saturation", "When the transistor is fully on as a switch."), ("MOSFET", "A field-effect transistor with an insulated gate."), ("Bias", "The steady setting that puts a transistor in the right range.")],
 ["NPN: current flows from collector to emitter when the base is driven above about 0.7 V.", "Ic = beta x Ib while not saturated.", "As a switch, drive the base hard: Ib about Ic / (beta / 10).", "Vbe is about 0.7 V for silicon.", "Use a resistor in series with the base.", "A MOSFET gate draws almost no current; mind static."],
 [T("The transistor is the building block of modern electronics. In an NPN transistor, a small current into the base lets a much bigger current flow from collector to emitter. The ratio is the gain, called beta or hFE, often 100 or more."),
  M(r"I_C=\beta\,I_B\qquad R_B=\frac{V_{in}-V_{BE}}{I_B}"),
  T("As a switch, you push the transistor into saturation. Choose a base current several times higher than the minimum, so the transistor is fully on and the voltage across it is a few tenths of a volt. A common rule is to assume a gain of only one tenth of the stated beta."),
  C("# switch a 100 mA lamp from a 5 V logic pin\nic = 0.1\nbeta = 100\nib = ic / (beta / 10)       # drive hard\nrb = (5 - 0.7) / ib\nprint(round(rb))            # 430 ohms", "python"),
  T("A field-effect transistor works differently. A voltage on the gate controls the current from drain to source, and the gate draws almost nothing. Power MOSFETs switch big currents with very little loss. Their gates are delicate, so handle them with care against static.")],
 [("What does the base do?", ["Controls the main current", "Supplies power", "Makes light", "Stores charge"], 0, "A small current controls a big one."),
  ("What is Ic with beta 100 and Ib 1 mA?", ["100 mA", "1 mA", "0.01 mA", "101 mA"], 0, "Beta x Ib."),
  ("Which draws almost no gate current?", ["A MOSFET", "A relay", "A diode", "A resistor"], 0, "Voltage controlled.")],
 [("What is hFE?", "Current gain."), ("What is saturation?", "Fully on."), ("Why a base resistor?", "To set base current."), ("What is a FET?", "A voltage controlled transistor.")],
 [MATCH("Terminals", "Match the terminal with its job.", [("Base", "Control input"), ("Collector", "Receives the load current"), ("Emitter", "Common return"), ("Gate", "Control input of a FET")]),
  PL("Base resistor", "Write base_r(vin, ic, beta): choose the base current as ic / (beta / 10) and return the base resistor in ohms (Vbe 0.7 V), rounded to 1 decimal.", "base_r(vin, ic, beta)", """
def base_r(vin, ic, beta):
    ib = ic / (beta / 10.0)
    return round((vin - 0.7) / ib, 1)
""", [[5, 0.1, 100], [3.3, 0.02, 200], [9, 0.5, 50]], "Drive the base hard.", approx=1e-2),
  PL("Collector current", "Write collector(vcc, rc, ib, beta): the collector current in amperes: beta x ib, but not more than the saturation limit (vcc - 0.2) / rc. Round to 5 decimals.", "collector(vcc, rc, ib, beta)", """
def collector(vcc, rc, ib, beta):
    ic = beta * ib
    lim = (vcc - 0.2) / rc
    return round(min(ic, lim), 5)
""", [[9, 1000, 0.00002, 100], [9, 1000, 0.001, 100], [5, 100, 0.0005, 200]], "Take the smaller.", approx=1e-4),
  PL("Switch state", "Write is_on(vin, vbe_on): return 1 if the input voltage is at least vbe_on (a transistor switch conducts), else 0, for each input in the list vin. Return the list.", "is_on(vin, vbe_on)", """
def is_on(vin, vbe_on):
    return [1 if v >= vbe_on else 0 for v in vin]
""", [[[0, 0.3, 0.7, 5], 0.7], [[], 0.6], [[1.0, 0.5], 0.8]], "A threshold.", approx=None),
  PL("Amplifier gain", "Write amp_gain(rc, re): the voltage gain of a common-emitter stage with emitter resistor, approximately rc / re, rounded to 2 decimals.", "amp_gain(rc, re)", """
def amp_gain(rc, re):
    return round(rc / re, 2)
""", [[4700, 470], [10000, 1000], [2200, 100]], "The ratio of resistors.", approx=1e-2)]))
