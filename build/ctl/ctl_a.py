# -*- coding: utf-8 -*-
"""Control theory course, part 1: feedback, modelling, response, transfer functions."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Feedback and the control problem",
 ("Control", [
  "Plant | is | The thing controlled",
  "Controller | computes | The input",
  "Sensor | measures | The output",
  "Setpoint | is | The target",
  "Error | is | Setpoint minus output",
  "Open loop | ignores | The output",
  "Closed loop | uses | Feedback"]),
 ["Control theory is the study of making systems behave as we want. A plant (a motor, a room, a rocket) is driven by an input, and we want its output to follow a target called the setpoint.",
  "An open-loop controller sends a fixed command and hopes. A closed-loop (feedback) controller measures the output, forms the error between setpoint and measurement, and corrects it continuously.",
  "Feedback fights disturbances and uncertainty, but a badly designed loop can oscillate or go unstable."],
 [("Plant", "The system being controlled."),
  ("Setpoint", "The desired value of the output, also called the reference."),
  ("Error", "The setpoint minus the measured output."),
  ("Feedback", "Using the measured output to adjust the input."),
  ("Disturbance", "An unwanted outside influence on the plant.")],
 ["e = r - y.",
  "Closed loop: sense, compare, act, repeat.",
  "Feedback rejects disturbances.",
  "Too much gain can destabilise a loop.",
  "Goals: stability, accuracy, speed, robustness."],
 [T("A thermostat is the classic example. You set 21 degrees. A sensor reads the room, the controller compares, and the heater switches on if the room is too cold. The heater is the actuator, the room is the plant, and the loop of measuring and correcting is feedback."),
  T("Compare an oven timer. It heats for a fixed time and ignores the temperature. That is open loop. It works only if nothing changes: the same oven, the same food, the same door never opened. As soon as a disturbance enters, the result drifts, and the open-loop controller never knows."),
  T("In a closed loop the error is the setpoint minus the measurement, written e equals r minus y. The controller turns the error into a command u. If the error is large and positive the command pushes the output up. As the error shrinks, the push shrinks."),
  T("Feedback can be too eager. If you push hard when the error is small, the output overshoots, you push back, it overshoots the other way, and the loop oscillates. Everyone has felt this when adjusting a shower tap with a delay. The art of control is to be firm but not reckless."),
  T("Designers judge a loop by four things: stability, meaning it settles; accuracy, meaning it ends near the target; speed, meaning how quickly; and robustness, meaning it still works when the plant differs from the model. This course builds the maths and the code to reason about all four.")],
 [("What is the plant?", ["The system being controlled", "The sensor", "The setpoint", "The error"], 0, "Motor, room, rocket."),
  ("How is the error defined?", ["Setpoint minus output", "Output minus input", "Input plus output", "Sensor noise"], 0, "e = r - y."),
  ("What is an open-loop controller?", ["One that ignores the output", "One that measures the output", "A fast one", "An unstable one"], 0, "Oven timer."),
  ("What can too much gain cause?", ["Oscillation or instability", "Perfect tracking", "Lower cost", "Sampling"], 0, "Overshoot."),
  ("What does feedback help against?", ["Disturbances", "Gravity only", "Colour", "Heat only"], 0, "Corrects drift."),
  ("Name one design goal.", ["Stability", "Beauty", "Loudness", "Size of the code"], 0, "Settles down.")],
 [("e = r - y", "error"), ("u", "control input"), ("y", "plant output"), ("r", "reference")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Plant", "system being controlled"), ("Setpoint", "desired output"), ("Error", "setpoint minus output"), ("Open loop", "ignores the output"), ("Feedback", "uses the measured output")]),
  PL("Error", "Write error(r, y): setpoint r minus measured output y, rounded to 4 decimals.", "error(r, y)", '''
def error(r, y):
    return round(r - y, 4)
''', [[21, 18.5], [10, 10], [0, 3], [5, -2]], "Subtract.", approx=0.0001),
  PL("On-off thermostat", "Write thermostat(temps, setpoint, band): simulate a heater that turns ON when the temperature drops below setpoint - band, turns OFF when it rises above setpoint + band, and otherwise keeps its previous state (initially OFF). Return the list of states (1 for ON, 0 for OFF) for each temperature in temps.", "thermostat(temps, setpoint, band)", '''
def thermostat(temps, setpoint, band):
    state = 0
    out = []
    for t in temps:
        if t < setpoint - band:
            state = 1
        elif t > setpoint + band:
            state = 0
        out.append(state)
    return out
''', [[[18, 19, 20, 21, 22, 23, 22, 21, 19], 21, 1], [[25, 25], 21, 1], [[10, 20, 21, 22], 21, 0.5]], "Keep the previous state inside the band."),
  PL("Proportional loop", "Simulate a room: temp[k+1] = temp[k] + 0.1 x u[k] - 0.05 x (temp[k] - 10) where the outside temperature is 10 and u = kp x (setpoint - temp[k]), starting from temp[0] = start. Write p_room(start, setpoint, kp, steps) returning the temperatures after each of the steps steps (not including the start), rounded to 2 decimals.", "p_room(start, setpoint, kp, steps)", '''
def p_room(start, setpoint, kp, steps):
    t = float(start)
    out = []
    for k in range(steps):
        u = kp * (setpoint - t)
        t = t + 0.1 * u - 0.05 * (t - 10)
        out.append(round(t, 2))
    return out
''', [[10, 20, 2, 5], [10, 20, 5, 5], [15, 20, 0, 4], [30, 20, 3, 4]], "Compute u each step from the current error.")]
))

CHS.append(CH(
 "Modelling dynamic systems",
 ("Modelling", [
  "Differential equation | describes | Dynamics",
  "State | summarises | The system now",
  "First-order | has | A time constant",
  "Time constant | is | Speed of response",
  "Steady state | is | Final value",
  "Euler method | steps | Through time",
  "Linearisation | approximates | Near a point"]),
 ["To control a system we need a model: equations for how it changes. Most are differential equations such as dx/dt = f(x, u).",
  "A first-order system, like a cooling cup or a charging capacitor, moves toward its final value exponentially. Its time constant tau is the time to cover about 63 percent of the gap.",
  "We can simulate any model on a computer by stepping through time: Euler's method updates x by the rate times a small time step."],
 [("State", "The smallest set of numbers that fully describes the system at a moment."),
  ("Time constant", "For a first-order system, tau, the time to complete 63.2 percent of a step change."),
  ("Steady state", "The value the output settles to."),
  ("Euler method", "A simple simulation rule: x_next = x + dt times dx/dt."),
  ("Linearisation", "Approximating a nonlinear model by a straight-line model near an operating point.")],
 ["tau dy/dt + y = K u.",
  "Step response: y(t) = K (1 - e^(-t/tau)).",
  "After 3 tau: 95 percent. After 5 tau: 99 percent.",
  "Euler: x[k+1] = x[k] + dt f(x[k], u[k]).",
  "Smaller dt means better accuracy."],
 [T("A cup of coffee cools quickly at first, then more and more slowly toward room temperature. The rate of cooling is proportional to the gap. That one sentence is a differential equation, and its solution is an exponential curve."),
  T("The standard first-order model is tau times dy dt plus y equals K times u. K is the steady-state gain: the final output per unit input. Tau is the time constant. After one tau the output has covered 63 percent of the way, after three tau 95 percent, after five tau 99 percent."),
  T("A model describes how the state changes. For a car, the state may be position and velocity. For a circuit, it is the voltages across capacitors and currents in inductors. The state is the minimum memory needed to predict the future given the inputs."),
  T("Most useful models cannot be solved with pencil and paper, so we simulate. Euler's method takes small steps: new state equals old state plus the time step times the rate of change. It is crude but easy, and with a small step it is good enough for control studies. Better methods such as Runge-Kutta take more samples per step."),
  T("Real systems are nonlinear: friction, saturation, trigonometry. Near an operating point, though, a straight-line approximation works, and linear theory is rich and powerful. This is linearisation, and it is why linear control theory is so widely useful.")],
 [("What does the time constant measure?", ["How fast a first-order system responds", "The final value", "The noise", "The gain"], 0, "63 percent."),
  ("How much of a step is done after 3 tau?", ["About 95 percent", "About 63 percent", "About 50 percent", "100 percent"], 0, "1 - e^-3."),
  ("What is the state of a system?", ["The minimum info to predict its future", "The final value", "The controller", "The sensor"], 0, "Its memory."),
  ("What does Euler's method do?", ["Steps the state forward by rate times dt", "Solves exactly", "Filters noise", "Finds poles"], 0, "Simple simulation."),
  ("Why linearise?", ["To use linear theory near an operating point", "To make it nonlinear", "To add noise", "To slow it"], 0, "Straight-line approx."),
  ("What is K in a first-order model?", ["Steady-state gain", "Time constant", "Error", "Sampling time"], 0, "Output per input.")],
 [("tau", "time constant"), ("K", "steady-state gain"), ("dt", "time step"), ("1 - e^(-t/tau)", "first-order step")],
 [APP("POLES", "Poles and step response", "Move the poles of a second-order system (real part and imaginary part) and watch the step response and the stability verdict. Try a stable, an oscillating and an unstable pole position to complete this lab.", 760),
  MATCH("Match the term", "Pair each term with its meaning.", [("State", "memory of the system"), ("Time constant", "63 percent response time"), ("Steady state", "final value"), ("Euler", "step forward by rate times dt"), ("Linearisation", "straight-line approximation")]),
  PL("First-order step response", "Write step1(K, tau, t): the output at time t of a first-order system with gain K and time constant tau after a unit step, K x (1 - e^(-t / tau)), rounded to 4 decimals.", "step1(K, tau, t)", '''
import math
def step1(K, tau, t):
    return round(K * (1 - math.exp(-t / tau)), 4)
''', [[1, 2, 2], [2, 1, 3], [1, 5, 0], [3, 0.5, 5]], "Use the exponential.", approx=0.0002),
  PL("Euler simulation", "Simulate tau dy/dt = K u - y with Euler's method: y[k+1] = y[k] + dt x (K u - y[k]) / tau, starting at y = 0, with constant input u. Write euler1(K, tau, u, dt, steps) returning the list of y after each step, rounded to 3 decimals.", "euler1(K, tau, u, dt, steps)", '''
def euler1(K, tau, u, dt, steps):
    y = 0.0
    out = []
    for k in range(steps):
        y = y + dt * (K * u - y) / tau
        out.append(round(y, 3))
    return out
''', [[1, 1, 1, 0.5, 5], [2, 2, 1, 0.1, 5], [1, 1, 0, 0.1, 3], [5, 1, 1, 1, 4]], "Update y each step."),
  PL("Time to settle", "Write settle_time(tau, pct): the time a first-order system takes to get within pct percent of its final value, -tau x ln(pct / 100), rounded to 4 decimals.", "settle_time(tau, pct)", '''
import math
def settle_time(tau, pct):
    return round(-tau * math.log(pct / 100.0), 4)
''', [[1, 2], [2, 5], [0.5, 1], [10, 36.8]], "Solve e^(-t/tau) = pct/100.", approx=0.0002),
  PL("Cooling cup", "A cup cools by dT/dt = -k (T - room). Write cooling(T0, room, k, dt, steps): the Euler simulation giving the list of temperatures after each step, rounded to 3 decimals.", "cooling(T0, room, k, dt, steps)", '''
def cooling(T0, room, k, dt, steps):
    T = float(T0)
    out = []
    for i in range(steps):
        T = T + dt * (-k * (T - room))
        out.append(round(T, 3))
    return out
''', [[90, 20, 0.1, 1, 4], [20, 20, 0.5, 1, 3], [10, 30, 0.2, 0.5, 4]], "Rate is minus k times the gap.")]
))

CHS.append(CH(
 "Second-order systems: damping and overshoot",
 ("Second order", [
  "Natural frequency | sets | Speed",
  "Damping ratio | sets | Oscillation",
  "Underdamped | overshoots | And rings",
  "Critically damped | is | Fastest no overshoot",
  "Overdamped | is | Slow",
  "Overshoot | is | Peak above target",
  "Settling time | is | Time to stay close"]),
 ["Many systems, such as a mass on a spring, a pendulum or a motor with inertia, behave as second-order systems, described by a natural frequency wn and a damping ratio zeta.",
  "With little damping (zeta below 1) the response overshoots and rings. At zeta equal to 1 it is critically damped. Above 1 it is overdamped and slow.",
  "Specifications such as percent overshoot and settling time translate directly into zeta and wn."],
 [("Natural frequency", "wn, the frequency at which an undamped system would oscillate."),
  ("Damping ratio", "zeta, how strongly oscillations are suppressed."),
  ("Percent overshoot", "How far the peak goes beyond the final value, as a percentage of it."),
  ("Settling time", "The time after which the response stays within a small band, often 2 percent, of the final value."),
  ("Rise time", "The time to go from 10 percent to 90 percent of the final value.")],
 ["y'' + 2 zeta wn y' + wn^2 y = wn^2 u.",
  "Overshoot = exp(-pi zeta / sqrt(1 - zeta^2)).",
  "Settling (2 percent) is about 4 / (zeta wn).",
  "zeta < 1 underdamped; = 1 critical; > 1 over.",
  "Poles: -zeta wn plus or minus i wn sqrt(1 - zeta^2)."],
 [T("Picture a car's suspension. A worn shock absorber lets the car bounce many times after a bump. A good one lets it settle in one smooth motion. A stiff one makes it feel sluggish. These three cases are underdamped, near critically damped, and overdamped."),
  T("The standard form has two numbers. The natural frequency wn says how fast things want to move. The damping ratio zeta says how much friction fights the oscillation. Zeta of zero never stops ringing, zeta of one is the fastest response without overshoot, and larger values are slower and smoother."),
  T("For a step input the underdamped response overshoots the target by a predictable amount: exp of minus pi zeta over the square root of one minus zeta squared. At zeta of 0.5 that is about 16 percent. At 0.7 it is about 5 percent, a popular design target."),
  T("The settling time to within two percent is roughly four divided by zeta times wn. The product zeta wn is the decay rate, set by the real part of the poles. So the shape of the response is read from where the poles are: far left means fast decay, high up means fast ringing."),
  T("These formulas let designers work backwards. If the specification says less than ten percent overshoot and settle in two seconds, we compute the needed zeta and wn, and then choose controller gains that place the closed-loop poles accordingly. The poles lab lets you see the connection yourself.")],
 [("What does zeta below 1 mean?", ["Underdamped with overshoot", "Overdamped", "Unstable", "No response"], 0, "Rings."),
  ("What is the fastest response without overshoot?", ["Critical damping", "Underdamping", "Zero damping", "Negative damping"], 0, "zeta = 1."),
  ("Roughly how much overshoot at zeta 0.7?", ["About 5 percent", "About 50 percent", "About 0", "About 100"], 0, "A popular target."),
  ("What does the real part of a pole set?", ["How fast the response decays", "The final value", "The noise", "The gain"], 0, "Decay rate."),
  ("What does the imaginary part of a pole set?", ["The ringing frequency", "The decay", "The gain", "The delay"], 0, "Oscillation."),
  ("Settling time to 2 percent is about:", ["4 / (zeta wn)", "1 / wn", "zeta wn", "wn / 4"], 0, "Four time constants.")],
 [("zeta", "damping ratio"), ("wn", "natural frequency"), ("exp(-pi zeta / sqrt(1 - zeta^2))", "overshoot"), ("4 / (zeta wn)", "settling time")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Underdamped", "overshoots and rings"), ("Critically damped", "fastest without overshoot"), ("Overdamped", "slow, no overshoot"), ("Damping ratio", "zeta"), ("Settling time", "time to stay near the target")]),
  PL("Overshoot", "Write overshoot(zeta): the fractional overshoot exp(-pi zeta / sqrt(1 - zeta^2)) for 0 < zeta < 1, as a percentage rounded to 2 decimals. For zeta of 1 or more return 0.", "overshoot(zeta)", '''
import math
def overshoot(zeta):
    if zeta >= 1:
        return 0
    return round(100 * math.exp(-math.pi * zeta / math.sqrt(1 - zeta * zeta)), 2)
''', [[0.5], [0.7], [0.2], [1], [1.5], [0.9]], "Use the formula.", approx=0.02),
  PL("Settling time", "Write settle2(zeta, wn): the approximate 2 percent settling time 4 / (zeta x wn), rounded to 3 decimals.", "settle2(zeta, wn)", '''
def settle2(zeta, wn):
    return round(4.0 / (zeta * wn), 3)
''', [[0.7, 4], [0.5, 2], [1, 10], [0.3, 1]], "Divide four by the decay rate.", approx=0.002),
  PL("Poles of a second-order system", "Write poles(zeta, wn): the poles of s^2 + 2 zeta wn s + wn^2 = 0 as the list [real, imag] of the pole with positive imaginary part, if zeta < 1: real = -zeta wn, imag = wn sqrt(1 - zeta^2). If zeta >= 1 return the two real poles as [slow, fast] sorted from largest (closest to zero) to smallest. Round to 4 decimals.", "poles(zeta, wn)", '''
import math
def poles(zeta, wn):
    if zeta < 1:
        return [round(-zeta * wn, 4), round(wn * math.sqrt(1 - zeta * zeta), 4)]
    d = wn * math.sqrt(zeta * zeta - 1)
    return [round(-zeta * wn + d, 4), round(-zeta * wn - d, 4)]
''', [[0.5, 2], [0.7, 4], [1, 3], [2, 1]], "Choose the formula by the case.", approx=0.001),
  PL("Simulate a second-order step", "Euler-simulate y'' = wn^2 (u - y) - 2 zeta wn y' with u = 1 and zero start. Use v = y' : v += dt x acceleration, then y += dt x v (update v first). Write sim2(zeta, wn, dt, steps) returning y after each step, rounded to 3 decimals.", "sim2(zeta, wn, dt, steps)", '''
def sim2(zeta, wn, dt, steps):
    y = 0.0
    v = 0.0
    out = []
    for k in range(steps):
        a = wn * wn * (1.0 - y) - 2 * zeta * wn * v
        v = v + dt * a
        y = y + dt * v
        out.append(round(y, 3))
    return out
''', [[0.5, 2, 0.1, 8], [1, 2, 0.1, 6], [0.1, 3, 0.05, 8]], "Update the velocity, then the position.")]
))

CHS.append(CH(
 "Transfer functions and stability",
 ("Stability", [
  "Laplace transform | turns | Calculus into algebra",
  "Transfer function | is | Output over input",
  "Pole | sets | Behaviour",
  "Zero | shapes | Response",
  "Stable | means | Poles in left half-plane",
  "Routh-Hurwitz | tests | Without solving",
  "Final value | is | Gain at s = 0"]),
 ["The Laplace transform replaces differentiation by multiplication by s. A linear system then becomes a transfer function G(s) = Y(s) / U(s), a ratio of polynomials in s.",
  "The roots of the denominator are the poles. A continuous-time system is stable when all poles have negative real parts, lying in the left half of the s-plane.",
  "Routh-Hurwitz checks stability from the coefficients alone, without finding the roots. Closing a loop changes the poles, which is how feedback reshapes behaviour."],
 [("Transfer function", "G(s) = Y(s) / U(s), the ratio of output to input in the Laplace domain."),
  ("Left half-plane", "The region of the s-plane where the real part is negative; poles there mean decay."),
  ("Characteristic equation", "The denominator of the closed-loop transfer function set to zero; its roots are the closed-loop poles."),
  ("Routh-Hurwitz criterion", "A table test of stability using only polynomial coefficients."),
  ("Final value theorem", "A steady-state output equals G(0) times the input for a stable system and a unit step.")],
 ["G(s) = K / (tau s + 1).",
  "Closed loop: T = L / (1 + L).",
  "Characteristic equation: 1 + L(s) = 0.",
  "Stable iff all poles have Re < 0.",
  "Second order: stable iff all coefficients positive."],
 [T("The Laplace transform is a trick. Differentiation in time becomes multiplication by s, so differential equations become polynomials. A transfer function G of s is the output over the input for a system starting at rest. It captures everything about a linear time-invariant system."),
  T("A pole is a value of s where G blows up, a root of the denominator. A pole at minus two gives a decaying exponential e to the minus two t. A pole at plus two gives a growing one, e to the plus two t, so the system is unstable. Complex pole pairs give oscillations whose envelope decays when the real part is negative."),
  T("So stability has a clear picture: draw the s-plane and put a cross at each pole. All crosses in the left half means the system is stable. Any cross in the right half means it is unstable. Crosses on the imaginary axis give sustained oscillation, which is marginal stability."),
  T("Feedback changes the poles. With a controller C and plant P, the loop transfer function is L equals C times P, and the closed loop is L over one plus L. The closed-loop poles solve one plus L equals zero. Raising a gain moves the poles; the root locus is the picture of their paths."),
  T("Finding roots of a high-order polynomial is hard by hand, so Routh and Hurwitz found a way to tell whether any root lies in the right half-plane directly from the coefficients. For a second-order polynomial the rule is easy: all coefficients must be positive. For third order, a2 a1 must exceed a3 a0 as well.")],
 [("What is a transfer function?", ["Output over input in the Laplace domain", "A file format", "A gain only", "A noise model"], 0, "Y(s)/U(s)."),
  ("Where must poles lie for stability?", ["Left half-plane", "Right half-plane", "On the real axis only", "At zero"], 0, "Re < 0."),
  ("What does a pole at +2 give?", ["A growing exponential", "A decay", "A constant", "A delay"], 0, "e^(2t)."),
  ("What is the closed-loop transfer function?", ["L / (1 + L)", "L x (1 + L)", "1 / L", "L - 1"], 0, "Unity feedback."),
  ("Poles on the imaginary axis give:", ["Sustained oscillation", "Fast decay", "Growth", "Nothing"], 0, "Marginal."),
  ("Why use Routh-Hurwitz?", ["Test stability without finding roots", "Find noise", "Sample signals", "Compile code"], 0, "From coefficients.")],
 [("G(s)", "transfer function"), ("1 + L(s) = 0", "characteristic equation"), ("Re(p) < 0", "stability"), ("G(0)", "DC gain")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Pole", "root of the denominator"), ("Zero", "root of the numerator"), ("Left half-plane", "stable region"), ("Characteristic equation", "1 + L = 0"), ("Marginal stability", "poles on the imaginary axis")]),
  PL("Closed-loop gain", "For a plant with DC gain G0 and proportional gain kp in a unity feedback loop, the closed-loop DC gain is kp G0 / (1 + kp G0). Write closed_gain(kp, G0), rounded to 4 decimals.", "closed_gain(kp, G0)", '''
def closed_gain(kp, G0):
    return round(kp * G0 / (1 + kp * G0), 4)
''', [[1, 1], [10, 1], [5, 2], [0, 3]], "L over one plus L.", approx=0.0002),
  PL("Stable second-order?", "A polynomial a2 s^2 + a1 s + a0 has all roots in the left half-plane exactly when all three coefficients have the same sign (and are non-zero). Write stable2(a2, a1, a0) returning True or False.", "stable2(a2, a1, a0)", '''
def stable2(a2, a1, a0):
    if a2 > 0 and a1 > 0 and a0 > 0:
        return True
    if a2 < 0 and a1 < 0 and a0 < 0:
        return True
    return False
''', [[1, 3, 2], [1, -3, 2], [1, 0, 4], [-1, -2, -3], [2, 1, 0]], "All three must share a sign."),
  PL("Stable third-order?", "For a3 s^3 + a2 s^2 + a1 s + a0 with a3 > 0, the Routh-Hurwitz condition is: a2 > 0, a1 > 0, a0 > 0 and a2 x a1 > a3 x a0. Write stable3(a3, a2, a1, a0) returning True or False.", "stable3(a3, a2, a1, a0)", '''
def stable3(a3, a2, a1, a0):
    return a2 > 0 and a1 > 0 and a0 > 0 and a2 * a1 > a3 * a0
''', [[1, 6, 11, 6], [1, 1, 1, 10], [1, 2, 3, 6], [1, 2, 3, 7], [1, -1, 2, 1]], "Check all four inequalities."),
  PL("Gain margin from kp", "For the plant G(s) = 1 / (s + 1)^3 under proportional gain k, the closed-loop characteristic polynomial is s^3 + 3 s^2 + 3 s + (1 + k). Using the Routh-Hurwitz test (a2 a1 > a3 a0), write max_gain() returning the largest k for which the loop is stable (the limit, 8).", "max_gain()", '''
def max_gain():
    a2 = 3
    a1 = 3
    return a2 * a1 - 1
''', [[]], "Solve 9 > 1 + k.")]
))
