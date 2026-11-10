"""Electronics course additions: lumped circuits, visual simulator, Arduino. Original text.
The lumped-circuit chapter follows the ideas of MIT OpenCourseWare 6.002 lecture 1 (Agarwal and Lang), written in our own words."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *


def FIG(name, caption):
    return {"type": "figure", "image": name, "caption": caption}


LUMP = CH(
 "The lumped circuit abstraction",
 ("Lumped model", ["Abstraction | hides | Detail", "Lumped element | has | Two terminals", "Element | obeys | A v-i rule", "KCL | says | Currents at a node sum to zero", "KVL | says | Voltages round a loop sum to zero", "Small size | allows | Lumped model"]),
 ["Engineers do not model every electron. They squeeze a real part into a simple box with two ends and one rule.",
  "That box is a lumped element. Its rule links the voltage across it to the current through it.",
  "If the parts are small enough, two laws follow for free: currents at a node sum to zero, and voltages round a loop sum to zero."],
 [("Abstraction", "Hiding details so you can reason at a higher level."), ("Lumped element", "A part treated as one point with two terminals."), ("v-i relation", "The rule linking an element's voltage and current."),
  ("KCL", "Kirchhoff's current law: currents into a node sum to zero."), ("KVL", "Kirchhoff's voltage law: voltages around a loop sum to zero."), ("Node", "A point where element terminals join.")],
 ["A bulb can be replaced by a resistor if only V and I matter.", "Inside a lumped element, charge does not pile up.", "Outside, wires carry no changing magnetic flux.", "KCL and KVL come from those two rules.", "The model fails when a circuit is as big as the signal wavelength."],
 [T("Physics describes everything with fields and charges, and that is far too detailed to design a phone. So engineers build layers. Each layer keeps a few facts and throws the rest away. Software sits on processors, processors on logic gates, gates on circuits, and circuits on physics."),
  FIG("abstraction-tower.svg", "Each layer of design hides the details of the layer below it. This course sits between lumped circuits and logic."),
  T("Take a light bulb. It has a glass shell, a hot filament, heat and light. For circuit design you care about only two numbers: the voltage across its two ends and the current through it. So you replace it by a box with two terminals and a rule, such as I = V / R. That box is a lumped element, and a resistor is its simplest form."),
  FIG("lumped-bulb.svg", "A real bulb on the left; on the right the lumped model keeps only the voltage and the current."),
  T("This works only if you obey a discipline. Inside each element, electric charge may not pile up, so whatever current goes in one terminal comes out of the other. And outside the elements, in the wires, there may be no changing magnetic flux. When both hold, the world of fields collapses into plain algebra."),
  T("Two laws drop out. Kirchhoff's current law: at any node, the currents flowing in add up to zero, because charge cannot collect there. Kirchhoff's voltage law: going around any loop, the voltage rises and drops add up to zero, because you end up back at the same point."),
  FIG("kvl-kcl.svg", "Left: voltages around a loop sum to zero. Right: currents into a node sum to zero."),
  M(r"\sum i_{\text{in}}=0,\qquad \sum v_{\text{loop}}=0"),
  T("When is a part small enough? Signals travel at about the speed of light, so a wire is lumped only if a signal crosses it much faster than the signal changes. A common rule is that the circuit should be smaller than a tenth of the wavelength. At mains frequency that allows a huge circuit. At a few gigahertz it allows only a few millimetres.")],
 [("What does a lumped element keep?", ["Voltage and current", "Its color", "Its shape", "Its temperature"], 0, "Only the terminal behaviour."),
  ("What does KCL say?", ["Currents at a node sum to zero", "Voltages at a node sum to zero", "Power is constant", "Resistance adds"], 0, "Charge cannot pile up at a node."),
  ("When does the lumped model fail?", ["When circuits are as big as the wavelength", "When the battery is new", "When current is DC", "Never"], 0, "Signals then take time to cross.")],
 [("What is a lumped element?", "A two-terminal box with a v-i rule."), ("What is KVL?", "Loop voltages sum to zero."), ("Why abstract?", "To hide detail and reason simply."), ("Size limit for lumped?", "Under about a tenth of a wavelength.")],
 [MATCH("Laws", "Match each law with what it says.", [("KCL", "Currents at a node sum to zero"), ("KVL", "Voltages round a loop sum to zero"), ("Lumped element", "Two terminals and a v-i rule"), ("Abstraction", "Hiding detail")]),
  PL("The missing current", "Write missing(currents): the currents into a node are listed with into-the-node positive and out-of-the-node negative, with one current left out. Return the missing current so that the total is zero, rounded to 6 places.", "missing(currents)", """
def missing(currents):
    return round(-sum(currents), 6)
""", [[[2, -0.5]], [[1, 1, -3]], [[0.25]]], "Use KCL: the total must be zero."),
  PL("The missing voltage", "Write loop_gap(drops): the voltages around a loop add to zero. Given all but one, return the last, rounded to 6 places.", "loop_gap(drops)", """
def loop_gap(drops):
    return round(-sum(drops), 6)
""", [[[9, -3, -2]], [[5, 5]], [[-1.5, 0.5, 0.5]]], "Use KVL."),
  PL("Is it lumped?", "Write lumped_ok(size_m, freq_hz): the signal travels at 3e8 m/s. Return True if the circuit is smaller than a tenth of the wavelength.", "lumped_ok(size_m, freq_hz)", """
def lumped_ok(size_m, freq_hz):
    wavelength = 3e8 / freq_hz
    return size_m < wavelength / 10
""", [[1, 50], [0.1, 1e9], [0.001, 1e9], [10, 1e7]], "wavelength = speed / frequency.")])


SIM = CH(
 "Visual circuit simulator",
 ("Simulation", ["Schematic | becomes | A netlist", "Nodes | hold | Voltages", "KCL | gives | One equation per node", "Solver | finds | All voltages", "Wire | joins | Two points into one node", "Ground | sets | Zero volts"]),
 ["A simulator turns your drawing into equations and solves them. It does what you would do with KCL and Ohm's law, only faster.",
  "You choose a ground, and every other point gets a voltage. Each part then gives a current from the voltage across it.",
  "The lab lets you place parts on a grid and press Solve. Build a divider that gives 3 V from 9 V."],
 [("Netlist", "A list of parts and the nodes they connect."), ("Ground", "The node chosen as zero volts."), ("Nodal analysis", "Writing KCL at each node and solving for voltages."), ("Ideal source", "A source whose voltage never sags."), ("Short circuit", "A path with no resistance, so very large current.")],
 ["Pick one ground node; all voltages are measured from it.", "Wires merge nodes.", "Each node gives one KCL equation.", "Solving the equations gives every voltage and current.", "An ideal battery across a wire is an error, not a circuit."],
 [T("A circuit drawing is also a graph. Points where parts meet are nodes, and parts are the links between them. A simulator reads that graph into a netlist: a list that says resistor R1 joins node 1 to node 2, battery B joins node 1 to ground, and so on."),
  T("It then picks a ground node as zero volts. For every other node it writes KCL: the currents leaving the node through each connected part add up to zero. For a resistor between nodes a and b, the current is (Va - Vb) / R. The result is a set of straight-line equations, one per node."),
  M(r"\sum_k \frac{V_n-V_k}{R_k}=0"),
  T("A battery fixes the voltage between two nodes, so it adds one equation and one unknown, its own current. Solving the whole set, usually by Gaussian elimination, gives every node voltage at once. Real tools such as SPICE use this idea with more part types and time steps."),
  T("The lab below has a grid. Choose a part, then tap two points. Wires join points into one node, and the ground part sets zero volts. Press Solve to see each voltage and the current in every part. Try the presets, then build a divider of your own that makes a 3 V node from the 9 V battery."),
  FIG("divider.svg", "The divider you are asked to build: two resistors in series, with the output taken between them.")],
 [("What does a simulator write at each node?", ["A KCL equation", "A color", "A time", "A fuse"], 0, "Currents sum to zero."),
  ("What does ground mean in a simulator?", ["The zero-volt reference", "The biggest voltage", "A wire to earth only", "A resistor"], 0, "All voltages are measured from it."),
  ("Why is a battery across a bare wire a problem?", ["Current would be unlimited", "It makes no light", "It is AC", "It is too cold"], 0, "An ideal source into zero ohms.")],
 [("What is a netlist?", "Parts and the nodes they join."), ("Which law gives the equations?", "KCL."), ("What does a wire do in the model?", "Merges two points into one node."), ("How to get 3 V from 9 V?", "Two resistors 2k over 1k.")],
 [MATCH("Terms", "Match each term with its meaning.", [("Netlist", "Parts and the nodes they join"), ("Ground", "Zero-volt reference"), ("Node", "A point where parts connect"), ("Ideal source", "Voltage that never sags")]),
  PL("Loaded divider", "Write loaded(vs, r1, r2, rl): a divider whose lower resistor r2 has a load rl in parallel. Return the output voltage rounded to 4 places.", "loaded(vs, r1, r2, rl)", """
def loaded(vs, r1, r2, rl):
    rp = r2 * rl / (r2 + rl)
    return round(vs * rp / (r1 + rp), 4)
""", [[9, 2000, 1000, 1e9], [9, 2000, 1000, 1000], [5, 1000, 1000, 1000]], "Combine r2 and rl in parallel first.", approx=1e-3),
  PL("Series current and drops", "Write drops(vs, resistors): return the voltage across each resistor in a series chain, each rounded to 4 places.", "drops(vs, resistors)", """
def drops(vs, resistors):
    i = vs / sum(resistors)
    return [round(i * r, 4) for r in resistors]
""", [[9, [2000, 1000]], [12, [100, 200, 300]], [5, [470]]], "The same current flows through every part.", approx=1e-3),
  {"type": "webxdc", "title": "Circuit simulator", "intro": "Place parts and solve. Build a divider that makes a 3 V node from the 9 V battery.", "height": 760, "html": "__SIM__"}])


ARD1 = CH(
 "Arduino: pins and sketches",
 ("Arduino", ["Sketch | has | setup and loop", "Pin | is | Input or output", "digitalWrite | sets | High or low", "LED | needs | A resistor", "Uno | runs at | 5 volts", "delay | waits | Milliseconds"]),
 ["An Arduino is a small computer board with pins you can set high or low or read. It is the bridge between code and the circuits you have learned.",
  "A program, called a sketch, has two parts. Setup runs once. Loop runs again and again.",
  "The lab below is a virtual Uno, so you can try each idea without any wiring."],
 [("Sketch", "An Arduino program."), ("Pin", "A connection point the program can drive or read."), ("Digital", "Only two values: high (5 V) or low (0 V)."), ("Analog input", "A pin that measures a voltage from 0 to 5 V as a number 0 to 1023."), ("PWM", "Pulse width modulation: fast on-off switching that acts like a partial voltage.")],
 ["Uno: 5 V logic, 14 digital pins, 6 analog inputs, 16 MHz.", "setup() runs once; loop() repeats.", "pinMode chooses input or output.", "An LED pin needs about 220 ohms in series.", "INPUT_PULLUP reads low when a button joins the pin to ground."],
 [T("The Arduino Uno has a small chip, the ATmega328P, running at 16 megahertz with 32 kilobytes of program memory and 2 kilobytes of working memory. Its logic runs at 5 volts. It has 14 digital pins numbered 0 to 13, six analog inputs named A0 to A5, and power pins for 5 volts, 3.3 volts and ground."),
  FIG("arduino-uno.svg", "The Uno: digital pins along the top (the ones marked with a tilde can do PWM), power and analog pins along the bottom."),
  T("Every sketch has two functions. Setup runs once at power-up, where you call pinMode to say whether each pin is an output or an input. Loop runs forever. A blink is just: set pin 13 high, delay 500 milliseconds, set it low, delay 500 milliseconds."),
  C("void setup() {\n  pinMode(13, OUTPUT);\n}\n\nvoid loop() {\n  digitalWrite(13, HIGH);\n  delay(500);\n  digitalWrite(13, LOW);\n  delay(500);\n}"),
  T("An output pin that is high is a 5 volt source with a limited current, about 20 milliamps for comfort. An LED needs a series resistor, exactly the rule from the diode chapter: R = (5 - Vf) / I. A red LED at 15 milliamps needs about 200 ohms, so 220 ohms is a common choice."),
  FIG("arduino-led.svg", "Pin 13 drives an LED through a 220 ohm resistor to ground."),
  T("To read a button, wire it between the pin and ground and use INPUT_PULLUP. A small internal resistor pulls the pin high. Pressing the button joins it to ground, so digitalRead returns LOW when pressed. This needs no outside resistor."),
  T("Try it below. Press Upload to run Blink, then change the delays. Pin 13 is the LED you toggle, and the goal is met when it has blinked four times and the sketch has used analogWrite.")],
 [("What does setup() do?", ["Runs once at start", "Runs forever", "Never runs", "Resets the chip"], 0, "Then loop() repeats."),
  ("What does INPUT_PULLUP read when the button is pressed?", ["LOW", "HIGH", "512", "Nothing"], 0, "The button joins the pin to ground."),
  ("Why put a resistor with an LED on a pin?", ["To limit current", "To make it blink", "To raise voltage", "To save memory"], 0, "Or the pin and LED may burn out.")],
 [("Logic voltage of an Uno?", "5 volts."), ("How many analog inputs?", "Six, A0 to A5."), ("What does delay(500) do?", "Waits half a second."), ("What is pinMode for?", "Setting a pin as input or output.")],
 [MATCH("Functions", "Match each call with its job.", [("pinMode", "Chooses input or output"), ("digitalWrite", "Sets a pin high or low"), ("digitalRead", "Reads a pin"), ("delay", "Waits in milliseconds")]),
  FILL("Blink recipe", "The function that runs once is {{setup}} and the one that repeats is {{loop}}. To make a pin drive an LED you call {{pinMode}} with OUTPUT."),
  PL("LED resistor on a pin", "Write pin_resistor(vf, ma): the LED forward voltage vf, the wanted current in milliamps. The pin gives 5 V. Return the resistor in ohms, rounded to the nearest whole ohm.", "pin_resistor(vf, ma)", """
def pin_resistor(vf, ma):
    return round((5 - vf) / (ma / 1000.0))
""", [[2.0, 15], [3.2, 10], [1.8, 20]], "R = (5 - Vf) / I."),
  PL("Blink count", "Write blinks(total_ms, on_ms, off_ms): a blink sketch turns the LED on for on_ms then off for off_ms, repeating. How many times does it turn on within total_ms (starting at time 0)? Each turn-on counts if it starts before total_ms.", "blinks(total_ms, on_ms, off_ms)", """
def blinks(total_ms, on_ms, off_ms):
    period = on_ms + off_ms
    return (total_ms + period - 1) // period
""", [[1000, 500, 500], [2500, 500, 500], [300, 100, 100], [0, 10, 10]], "A turn-on starts every period."),
  {"type": "webxdc", "title": "Virtual Arduino Uno", "intro": "Upload a sketch and watch the pins. Blink pin 13 four times and use analogWrite.", "height": 860, "html": "__ARD__"}])


ARD2 = CH(
 "Arduino: sensors, PWM and loads",
 ("Arduino I/O", ["analogRead | returns | 0 to 1023", "PWM | fakes | Partial voltage", "LDR | forms | A divider", "Transistor | drives | Big loads", "Diode | protects | From coil spikes", "millis | tells | Time since start"]),
 ["Analog input turns a voltage into a number. PWM turns a number into an average voltage.",
  "A light sensor and a fixed resistor make a divider, and the Arduino reads the middle point.",
  "Pins are weak, so motors and relays need a transistor and a flyback diode."],
 [("ADC", "Analog to digital converter: 10 bits on the Uno, so 0 to 1023."), ("PWM duty", "The fraction of each cycle that the pin is high."), ("analogWrite", "Sets PWM duty from 0 to 255."), ("Debounce", "Ignoring the tiny bounces of a switch contact."), ("Servo pulse", "A pulse of 1 to 2 ms, repeated every 20 ms, that sets a hobby servo angle.")],
 ["Volts = reading / 1023 x 5.", "Average PWM voltage = duty / 255 x 5.", "A pin gives about 20 mA; use a transistor for more.", "Put a diode across any coil.", "Use millis() instead of delay() to do two things at once."],
 [T("The Uno's analog converter measures a voltage between 0 and 5 volts and returns a number from 0 to 1023. Because 5 volts splits into 1023 steps, each step is about 4.9 millivolts. So analogRead(A0) of 512 means about 2.5 volts."),
  M(r"V=\frac{\text{reading}}{1023}\times 5"),
  T("A light-dependent resistor, or LDR, is a resistor that gets smaller in the light. Put it in series with a fixed resistor between 5 volts and ground, and the middle point is a voltage divider. The brighter the light, the higher that voltage, and the bigger the number analogRead gives."),
  FIG("arduino-ldr.svg", "An LDR and a 10k resistor form a divider; the middle point goes to A0."),
  T("There is no true analog output on the Uno. Instead analogWrite switches a pin on and off about 490 times a second, and the fraction of time it is high is the duty. An LED sees the average, so duty 128 out of 255 looks half bright and averages 2.5 volts."),
  FIG("pwm.svg", "Three duty cycles and the average voltage each one gives."),
  C("int raw = analogRead(A0);   // 0 to 1023\nint duty = raw / 4;           // 0 to 255\nanalogWrite(9, duty);         // dim the LED with the knob"),
  T("A pin can give only about 20 milliamps, so it cannot run a motor or a relay directly. Use a transistor as a switch: the pin drives the base through a resistor, and the load sits in the collector path. A motor or relay coil also needs a diode across it, to catch the voltage spike when it switches off. That is the flyback diode from the coil chapter."),
  T("The delay function stops everything. To read a button while something blinks, record millis() when the last change happened and compare it on each pass of loop. Switch contacts also bounce for a few milliseconds, so accept a press only after the pin has stayed the same for a short time. Hobby servos take a pulse of 1 to 2 milliseconds every 20 milliseconds, and the pulse length sets the angle.")],
 [("What does analogRead return at 5 V?", ["1023", "255", "5", "1"], 0, "The top of the 10-bit range."),
  ("What does analogWrite(9, 128) give?", ["About half duty", "Full on", "Off", "5 V steady"], 0, "128 of 255."),
  ("Why a diode across a relay coil?", ["To absorb the turn-off spike", "To make it click", "To save power", "To make it AC"], 0, "The coil keeps pushing current when switched off.")],
 [("Range of analogRead?", "0 to 1023."), ("Range of analogWrite?", "0 to 255."), ("Why use millis()?", "To keep time without blocking."), ("What is debounce?", "Ignoring contact bounce.")],
 [MATCH("I/O", "Match each need with the tool.", [("Read a knob", "analogRead"), ("Dim an LED", "analogWrite"), ("Drive a motor", "Transistor and diode"), ("Keep time", "millis")]),
  PL("ADC to volts", "Write adc_to_volts(raw): convert a 10-bit reading to volts on a 5 V reference, rounded to 3 places.", "adc_to_volts(raw)", """
def adc_to_volts(raw):
    return round(raw / 1023.0 * 5, 3)
""", [[0], [512], [1023], [205]], "Divide by 1023 and multiply by 5.", approx=1e-3),
  PL("PWM average", "Write pwm_average(value): analogWrite value 0 to 255. Return the average pin voltage on 5 V, rounded to 3 places.", "pwm_average(value)", """
def pwm_average(value):
    return round(value / 255.0 * 5, 3)
""", [[0], [64], [128], [255]], "Duty is value over 255.", approx=1e-3),
  PL("LDR reading", "Write ldr_reading(r_ldr, r_fixed): the LDR is on the 5 V side and r_fixed to ground, with A0 in the middle. Return the integer reading from 0 to 1023 (round to nearest).", "ldr_reading(r_ldr, r_fixed)", """
def ldr_reading(r_ldr, r_fixed):
    return round(1023.0 * r_fixed / (r_ldr + r_fixed))
""", [[1000, 10000], [10000, 10000], [100000, 10000]], "Divider first, then scale to 1023."),
  PL("Debounce", "Write pressed_at(samples, need): samples is a list of 0 and 1 readings taken once per millisecond. A press is accepted when the pin has read 1 for need readings in a row. Return the index of the sample that completes this, or -1 if never.", "pressed_at(samples, need)", """
def pressed_at(samples, need):
    run = 0
    for i in range(len(samples)):
        if samples[i] == 1:
            run += 1
        else:
            run = 0
        if run >= need:
            return i
    return -1
""", [[[0, 1, 0, 1, 1, 1, 1], 3], [[1, 0, 1, 0], 2], [[1, 1, 1], 3]], "Count a run of ones; reset on a zero."),
  PL("Servo pulse", "Write servo_pulse(angle): a servo gets 1000 microseconds at 0 degrees and 2000 at 180, linearly. Return the pulse in microseconds, rounded to a whole number.", "servo_pulse(angle)", """
def servo_pulse(angle):
    return round(1000 + angle / 180.0 * 1000)
""", [[0], [90], [180], [45]], "A straight line between the two ends.")])

NEW = dict(lump=LUMP, sim=SIM, ard1=ARD1, ard2=ARD2)
