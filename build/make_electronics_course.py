#!/usr/bin/env python3
"""Build the electronics course. Usage: python3 make_electronics_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "elc"))
import cmk, el1, el2, el3, figs  # noqa: E402

PRONOUNCE = {
    "Ohm": "ohm", "ohm": "ohm", "ohms": "ohms", "Ohm's": "ohms", "ampere": "am pair", "amperes": "am pairs", "milliamperes": "mil ee am pairs", "hertz": "hurts", "henry": "hen ree", "henries": "hen reez", "farad": "far ad", "farads": "far ads",
    "microfarads": "my kro far ads", "microfarad": "my kro far ad", "millihenries": "mil ee hen reez", "kilohm": "kill ohm", "hFE": "H F E", "hfe": "H F E", "NPN": "N P N", "PNP": "P N P", "MOSFET": "moss fet", "FET": "F E T",
    "SCR": "S C R", "LED": "L E D", "LEDs": "L E Ds", "IC": "I C", "ICs": "I Cs", "TTL": "T T L", "CMOS": "sea moss", "AC": "A C", "DC": "D C", "RMS": "R M S", "NAND": "nand", "NOR": "nor", "XOR": "ex or", "UJT": "U J T",
    "triac": "try ack", "Triac": "try ack", "triacs": "try acks", "thyristor": "thigh ris tor", "Thyristor": "thigh ris tor", "thyristors": "thigh ris tors", "Zener": "zee ner", "zener": "zee ner", "photodiode": "foto die ode", "photodiodes": "foto die odes",
    "phototransistor": "foto transistor", "photoresistor": "foto resistor", "photoresistors": "foto resistors", "photonic": "foh ton ik", "oscilloscope": "oss ill oh scope", "multimeter": "multi meter", "datasheet": "data sheet", "datasheets": "data sheets",
    "op-amp": "op amp", "Op-amp": "op amp", "op-amps": "op amps", "astable": "ay stable", "monostable": "mono stable", "decibels": "dess ih bels", "decibel": "dess ih bel", "dB": "decibel", "dBs": "decibels", "7805": "seventy eight oh five",
    "555": "five five five", "hFE": "H F E", "pF": "pico farad", "uF": "micro farad", "kHz": "kilohertz", "MHz": "megahertz", "mA": "milliamps", "mAh": "milliamp hours", "ELI5": "E L I five", "Vbe": "V B E", "Ic": "I C", "Ib": "I B",
    "silicon": "silicon", "bipolar": "by polar", "unijunction": "you nee junction", "ripple": "ripple", "solder": "sodder", "soldering": "sodder ing", "Georg": "gay org", "Faraday": "fair uh day", "sqrt": "square root", "log10": "log ten",
    "Arduino": "ar dwee no", "Uno": "oo no", "PWM": "P W M", "ADC": "A D C", "LDR": "L D R", "KCL": "K C L", "KVL": "K V L", "Kirchhoff": "keer koff", "Kirchhoff's": "keer koffs", "pinMode": "pin mode", "digitalWrite": "digital write", "digitalRead": "digital read", "analogRead": "analog read", "analogWrite": "analog write", "millis": "millis", "ATmega328P": "A T mega three two eight P", "SPICE": "spice", "netlist": "net list", "lumped": "lumped", "flyback": "fly back", "coulomb": "coo lomb", "coulombs": "coo lombs", "hertz": "hurts", "kHz": "kilohertz", "Vs": "V S", "E12": "E twelve", "PN": "P N", "NTC": "N T C",
}

SANDBOX = cmk.terminal("Electronics cheat sheet", "volt>", "A scripted lookup, not a real simulator. Try: ohm, power, divider, rc, led, transistor, gates, opamp, 555, solder", [
    ("ohm", ["V = I x R, so I = V / R and R = V / I", "9 V across 900 ohms is 10 mA"]),
    ("power", ["P = V x I = I squared x R", "Pick a resistor rated for at least twice the power"]),
    ("divider", ["Vout = Vin x R2 / (R1 + R2)", "A heavy load pulls the output down"]),
    ("rc", ["Time constant = R x C seconds", "63 percent after one, 99 percent after five"]),
    ("led", ["R = (Vsupply - Vled) / I", "A red LED drops about 2 V"]),
    ("transistor", ["Ic = beta x Ib until saturation", "Drive a switch with about a tenth of the stated beta"]),
    ("gates", ["AND all, OR any, XOR differ, NAND is universal", "Half adder: sum = XOR, carry = AND"]),
    ("opamp", ["Inverting gain = -Rf / Rin", "Non-inverting gain = 1 + Rf / Rg"]),
    ("555", ["Astable f = 1.44 / ((R1 + 2 R2) C)", "Duty = (R1 + R2) / (R1 + 2 R2)"]),
    ("arduino", ["setup() runs once, loop() repeats", "analogRead is 0-1023, analogWrite is 0-255"]),
    ("kirchhoff", ["KCL: currents at a node sum to zero", "KVL: voltages round a loop sum to zero"]),
    ("solder", ["Heat the pad and the lead, then feed the solder", "A good joint is smooth and shiny"]),
])

EXAM = [
 ("What is the unit of current?", ["Ampere", "Volt", "Ohm", "Watt"], 0, "Charge per second."),
 ("Which material is an insulator?", ["Rubber", "Copper", "Gold", "Iron"], 0, "It blocks current."),
 ("Which current changes direction?", ["AC", "DC", "Static", "Leakage"], 0, "Alternating."),
 ("What does Ohm's law say?", ["V = I x R", "P = I + V", "V = I / R", "R = V x I"], 0, "The basic rule."),
 ("What is the power with 12 V and 0.5 A?", ["6 W", "24 W", "12 W", "0.04 W"], 0, "V x I."),
 ("What happens to total resistance in parallel?", ["It gets smaller", "It gets larger", "It stays", "It doubles"], 0, "More paths."),
 ("What does a series circuit share?", ["The same current", "The same voltage", "Nothing", "The same resistance"], 0, "One path."),
 ("What does the third color band mean?", ["Multiplier", "Tolerance", "Wattage", "First digit"], 0, "Number of zeros."),
 ("What is the output of a divider with equal resistors?", ["Half the input", "The whole input", "Zero", "Double"], 0, "R2 over the sum."),
 ("What does a capacitor store?", ["Charge", "Light", "Heat", "Current"], 0, "On two plates."),
 ("What is the time constant?", ["R x C", "R + C", "R / C", "C / R"], 0, "In seconds."),
 ("How charged is a capacitor after one time constant?", ["About 63 percent", "50 percent", "100 percent", "10 percent"], 0, "1 minus 1/e."),
 ("What does a transformer need?", ["Changing current", "Steady DC", "Light", "A diode"], 0, "AC."),
 ("What does a step-down transformer do?", ["Lowers the AC voltage", "Raises it", "Makes DC", "Stores charge"], 0, "Fewer turns on the output."),
 ("What does X_L do as frequency rises?", ["Grows", "Shrinks", "Stays", "Vanishes"], 0, "2 pi f L."),
 ("What protects against a relay's coil spike?", ["A diode across the coil", "A bigger relay", "More voltage", "Nothing"], 0, "A flyback diode."),
 ("What is a silicon diode's forward drop?", ["About 0.7 V", "About 5 V", "0 V", "About 12 V"], 0, "Typical."),
 ("What does a rectifier do?", ["AC to DC", "DC to AC", "Amplifies", "Stores"], 0, "Using diodes."),
 ("Why does an LED need a resistor?", ["To limit current", "To make light", "To add voltage", "To cool"], 0, "Or it burns."),
 ("What does a Zener diode do?", ["Holds a voltage", "Makes light", "Amplifies", "Switches AC"], 0, "Used in reverse."),
 ("Which terminal controls a bipolar transistor?", ["The base", "The collector", "The emitter", "The case"], 0, "A small current."),
 ("What is Ic with beta 100 and Ib 0.1 mA?", ["10 mA", "0.1 mA", "100 mA", "1 mA"], 0, "Beta x Ib."),
 ("What does a MOSFET gate need?", ["A voltage, almost no current", "A big current", "Light", "A coil"], 0, "Voltage controlled."),
 ("What turns an SCR off?", ["Current falling to zero", "A gate pulse", "Light", "A resistor"], 0, "It latches."),
 ("Which switches AC both ways?", ["A triac", "An SCR", "An LED", "A diode"], 0, "Two SCRs back to back."),
 ("What does a photoresistor do in light?", ["Resistance falls", "Resistance rises", "Makes light", "Stores charge"], 0, "Brighter, lower R."),
 ("What is the period of a 100 Hz wave?", ["10 ms", "100 ms", "1 ms", "1 s"], 0, "1 / f."),
 ("What is the RMS of a sine with peak 10?", ["About 7.07", "10", "5", "14.1"], 0, "Peak over root two."),
 ("What does duty cycle mean?", ["Fraction of time on", "Frequency", "Amplitude", "Noise"], 0, "On over period."),
 ("When is an AND gate output 1?", ["All inputs 1", "Any input 1", "No inputs 1", "Never"], 0, "All of them."),
 ("What is 101 in binary?", ["5", "3", "6", "7"], 0, "4 + 1."),
 ("Which gate is universal?", ["NAND", "AND", "OR", "XOR"], 0, "All others can be built from it."),
 ("What does a flip-flop store?", ["One bit", "One byte", "A voltage", "A current"], 0, "On a clock edge."),
 ("What gives memory in a latch?", ["Feedback", "A battery", "A lens", "A fuse"], 0, "Output to input."),
 ("What sets an op-amp's gain?", ["Feedback resistors", "The case", "The battery", "The clock"], 0, "Rf and Rin."),
 ("What does a 555 timer make?", ["Pulses and delays", "Light", "AC power", "Heat"], 0, "With R and C."),
 ("What heats a linear regulator?", ["Voltage drop times current", "The clock", "Light", "Noise"], 0, "Wasted power."),
 ("How do you measure voltage with a meter?", ["Across the part", "In series", "With power off", "With a fuse"], 0, "In parallel."),
 ("What does a good solder joint look like?", ["Smooth and shiny", "Dull and lumpy", "Black", "Wet"], 0, "A small cone."),
 ("What is a lumped element?", ["A two-terminal part with a v-i rule", "A lump of coal", "A wire only", "A battery only"], 0, "A point-like model."),
 ("What does KVL say?", ["Voltages round a loop sum to zero", "Currents at a node sum to zero", "Power is constant", "Resistance adds"], 0, "Same start and end point."),
 ("What does KCL say?", ["Currents at a node sum to zero", "Voltages round a loop sum to zero", "Voltage is constant", "Current is lost"], 0, "No charge piles up."),
 ("What does a circuit simulator solve?", ["Node voltage equations", "Color codes", "Fuse ratings", "Battery life only"], 0, "One KCL equation per node."),
 ("What range does analogRead give on an Uno?", ["0 to 1023", "0 to 255", "0 to 5", "0 to 100"], 0, "A 10-bit converter."),
 ("What does analogWrite use to fake a voltage?", ["PWM", "A battery", "A coil", "A fuse"], 0, "Fast on-off switching."),
 ("What does INPUT_PULLUP read when a button is pressed?", ["LOW", "HIGH", "1023", "255"], 0, "It joins the pin to ground."),
 ("Why put a flyback diode across a relay coil?", ["To absorb the turn-off spike", "To make it louder", "To speed it up", "To save power"], 0, "The coil keeps pushing current."),
]

IMAGES = figs.build_all()
FIGS = {1: [("series-parallel.svg", "Resistors in series share one current; resistors in parallel share one voltage.")],
        2: [("resistor-code.svg", "The color bands of a resistor and the digit each color stands for."), ("divider.svg", "A voltage divider: two resistors in series share the supply.")],
        3: [("rc-curve.svg", "Charging a capacitor through a resistor follows a rising curve; one time constant reaches 63 percent.")],
        4: [("transformer.svg", "A transformer: the output voltage follows the turns ratio.")],
        5: [("diode-iv.svg", "A diode passes current one way, with a knee near 0.7 volts."), ("rectify.svg", "Half-wave and full-wave rectifying of an AC wave."), ("led-resistor.svg", "Sizing the series resistor for an LED.")],
        6: [("npn-switch.svg", "An NPN transistor switching a lamp from a small base current.")],
        8: [("waveforms.svg", "A sine wave with its period and peak, and a pulse train with its duty cycle.")],
        9: [("gate-symbols.svg", "Symbols and truth tables for the basic gates.")],
        10: [("flipflop.svg", "A D flip-flop copies D to Q on each rising clock edge.")],
        11: [("opamp.svg", "An inverting op-amp stage: the gain is minus Rf over Rin."), ("timer555.svg", "A 555 timer wired as a free-running oscillator.")],
        12: [("breadboard.svg", "How a solderless breadboard joins its holes.")]}


def build_chapters():
    base = el1.A + el2.B
    for i, figlist in FIGS.items():
        les = base[i]["lesson"]
        for k, (img, cap) in enumerate(figlist):
            les.insert(2 + k, el3.FIG(img, cap))
    # order: charge, lumped, ohm, resistors, simulator, rest, arduino x2
    return [base[0], el3.LUMP, base[1], base[2], el3.SIM] + base[3:] + [el3.ARD1, el3.ARD2]


CFG = dict(id="electronics-from-scratch", title="Electronics from Scratch: Components, Circuits and Logic", subtitle="From electric charge to op-amps and logic gates, with small Python models of each idea",
    description="An original beginner course in electronics, covering the same ground as a classic introductory handbook. You will learn electricity and Ohm's law, resistors, capacitors, coils and transformers, diodes and LEDs, transistors, thyristors and light detectors, waves and signals, digital logic and memory, linear ICs such as the op-amp and the 555 timer, and how to build, solder and measure real circuits safely. Each chapter has an ELI5 block, a quiz and Python labs that calculate the circuits.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="elc", apps={"__SIM__": "sim.html", "__ARD__": "ard.html"}, images=IMAGES)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "electronics-from-scratch.course.json")
    cmk.main(CFG, build_chapters(), [sys.argv[0], out])
