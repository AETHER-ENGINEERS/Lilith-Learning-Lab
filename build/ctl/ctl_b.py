# -*- coding: utf-8 -*-
"""Control theory course, part 2: PID, frequency methods, state space, digital control."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "PID control",
 ("PID", [
  "P | reacts to | Present error",
  "I | removes | Steady-state error",
  "D | predicts | Future error",
  "Kp | scales | Error",
  "Ki | scales | Accumulated error",
  "Kd | scales | Rate of change",
  "Windup | is | Integrator overshoot"]),
 ["The PID controller computes its command from three terms: proportional to the error now, integral of the error so far, and derivative of the error's rate of change.",
  "Proportional control alone often leaves a steady-state error. The integral term removes it by acting until the error is exactly zero. The derivative term damps oscillation by reacting to the trend.",
  "Practical PID needs care: limit the output, stop the integrator winding up when saturated, and filter the derivative to avoid amplifying noise."],
 [("Proportional term", "Kp times the current error."),
  ("Integral term", "Ki times the accumulated error over time; removes steady-state error."),
  ("Derivative term", "Kd times the rate of change of the error; adds damping."),
  ("Integrator windup", "Excessive growth of the integral term while the actuator is saturated."),
  ("Steady-state error", "The remaining error after transients have died.")],
 ["u = Kp e + Ki integral(e) + Kd de/dt.",
  "Discrete: I += e dt; D = (e - e_prev) / dt.",
  "Raise Kp: faster, more overshoot.",
  "Raise Ki: removes offset, more oscillation.",
  "Raise Kd: damps, amplifies noise."],
 [T("About nine out of ten industrial control loops use PID. Cruise control, drone stabilisers, ovens and chemical plants all run it. It is popular because three intuitive knobs often suffice and it needs only a rough idea of the plant."),
  T("Think of steering a car toward a lane centre. The proportional term is steering in proportion to how far off you are. The integral term is the gentle persistent nudge that cancels a steady crosswind you have noticed has been pushing you for a while. The derivative term is easing off because you are already closing in fast."),
  T("Proportional alone leaves an offset when the plant needs a constant effort to hold the target, since zero error would mean zero push. The integral term keeps growing while any error persists, so it finally supplies exactly the effort required and the error vanishes."),
  T("Too much integral causes slow oscillations. Too much proportional causes fast oscillation. The derivative term helps by opposing rapid motion, but because it differentiates, it magnifies measurement noise, so real controllers filter it. A tuner explores these trade-offs."),
  T("Two practical fixes matter. First, the actuator has limits; a heater cannot go below off. If the integrator keeps accumulating while saturated, it takes a long time to unwind afterwards. Anti-windup stops it from accumulating then. Second, derivative kick: use the derivative of the measurement, not the error, so a setpoint jump does not cause a spike.")],
 [("What does the integral term remove?", ["Steady-state error", "Noise", "Delay", "Gain"], 0, "Persistent offset."),
  ("What does the derivative term add?", ["Damping", "Offset", "Delay", "Gain error"], 0, "Reacts to the trend."),
  ("What does too much Kp cause?", ["Overshoot and oscillation", "Slower response", "No error", "Lower noise"], 0, "Eager."),
  ("What is windup?", ["Integral growth during saturation", "A noise source", "A sensor fault", "A filter"], 0, "Actuator limits."),
  ("Why filter the derivative?", ["It amplifies noise", "It is too slow", "It is too small", "It removes offset"], 0, "Differentiating noise."),
  ("Which loops use PID?", ["Most industrial loops", "Only rockets", "Only radios", "None"], 0, "About 90 percent.")],
 [("u = Kp e + Ki integral + Kd derivative", "PID law"), ("I += e dt", "discrete integral"), ("(e - e_prev) / dt", "discrete derivative")],
 [APP("PID", "PID tuner", "Tune Kp, Ki and Kd for a plant with a lag and a delay. Aim for small overshoot and quick settling. Get a response with less than 10 percent overshoot that settles to within 2 percent to complete this lab.", 800),
  MATCH("Match the term", "Pair each term with its job.", [("P", "responds to present error"), ("I", "removes steady-state error"), ("D", "damps using the trend"), ("Windup", "integrator growth when saturated"), ("Saturation", "actuator limit")]),
  PL("PID output", "Write pid_step(e, e_prev, integral, kp, ki, kd, dt): one PID step. New integral = integral + e x dt; derivative = (e - e_prev) / dt. Return the list [u, new_integral] with u = kp e + ki new_integral + kd derivative, rounded to 4 decimals.", "pid_step(e, e_prev, integral, kp, ki, kd, dt)", '''
def pid_step(e, e_prev, integral, kp, ki, kd, dt):
    integral = integral + e * dt
    d = (e - e_prev) / dt
    u = kp * e + ki * integral + kd * d
    return [round(u, 4), round(integral, 4)]
''', [[1, 0, 0, 2, 1, 0.5, 0.1], [0, 0, 5, 1, 1, 1, 0.5], [2, 3, 1, 0, 1, 0, 1], [-1, 1, 0, 1, 0, 1, 0.5]], "Update the integral first.", approx=0.0002),
  PL("Closed-loop PI simulation", "Plant: y[k+1] = y[k] + dt x (u - y[k]). Controller PI with output u = kp e + ki I where e = r - y, and I += e dt before computing u. Start y = 0, I = 0. Write pi_sim(r, kp, ki, dt, steps) returning y after each step, rounded to 3 decimals.", "pi_sim(r, kp, ki, dt, steps)", '''
def pi_sim(r, kp, ki, dt, steps):
    y = 0.0
    integ = 0.0
    out = []
    for k in range(steps):
        e = r - y
        integ = integ + e * dt
        u = kp * e + ki * integ
        y = y + dt * (u - y)
        out.append(round(y, 3))
    return out
''', [[1, 1, 0, 0.1, 6], [1, 1, 1, 0.1, 6], [2, 4, 2, 0.05, 6]], "Compute e, integrate, then drive the plant."),
  PL("Saturate", "Write clamp(u, lo, hi): limit u to the range lo..hi.", "clamp(u, lo, hi)", '''
def clamp(u, lo, hi):
    if u < lo:
        return lo
    if u > hi:
        return hi
    return u
''', [[5, 0, 3], [-1, 0, 3], [2, 0, 3], [3, 0, 3]], "Compare against both limits."),
  PL("Anti-windup", "Write pid_aw(errors, kp, ki, dt, lo, hi): for each error in errors (in order), update integral += e dt only if the unsaturated output kp e + ki (integral + e dt) lies within lo..hi; otherwise leave the integral unchanged. Output u is the clamped kp e + ki x integral (after the update). Return the list of u values rounded to 3 decimals.", "pid_aw(errors, kp, ki, dt, lo, hi)", '''
def pid_aw(errors, kp, ki, dt, lo, hi):
    integ = 0.0
    out = []
    for e in errors:
        trial = integ + e * dt
        raw = kp * e + ki * trial
        if lo <= raw <= hi:
            integ = trial
        u = kp * e + ki * integ
        if u < lo:
            u = lo
        if u > hi:
            u = hi
        out.append(round(u, 3))
    return out
''', [[[1, 1, 1, 1], 2, 1, 0.5, -1, 3], [[5, 5, 5], 1, 1, 1, 0, 4], [[0.5, -0.5, 0.5], 1, 2, 0.1, -2, 2]], "Skip the integral update when out of range.")]
))

CHS.append(CH(
 "Root locus and frequency response",
 ("Frequency methods", [
  "Root locus | shows | Pole paths",
  "Bode plot | shows | Gain and phase",
  "Gain margin | is | Spare gain",
  "Phase margin | is | Spare phase",
  "Crossover | is | Gain of one",
  "Nyquist | tests | Stability",
  "Bandwidth | is | Speed"]),
 ["Root locus shows how the closed-loop poles move as a gain k grows from zero to infinity, giving a picture of when the loop becomes unstable.",
  "Frequency response describes how a system treats sine inputs. A Bode plot draws gain and phase against frequency. Margins measure how close the loop is to instability.",
  "Gain margin and phase margin are safety distances. A phase margin of 45 to 60 degrees usually means a well-damped loop."],
 [("Root locus", "The set of closed-loop pole positions as a gain varies."),
  ("Bode plot", "A graph of a system's gain (in decibels) and phase against frequency."),
  ("Gain crossover", "The frequency where the loop gain magnitude equals 1 (0 dB)."),
  ("Phase margin", "How much extra phase lag at gain crossover would make the loop marginally stable."),
  ("Gain margin", "How much the gain could rise before instability, measured where the phase is minus 180 degrees.")],
 ["|G(iw)| and angle G(iw).",
  "dB = 20 log10 |G|.",
  "Phase margin = 180 + phase at crossover.",
  "Gain margin = 1 / |L| at phase -180.",
  "Bandwidth sets speed of response."],
 [T("Push a child on a swing. Pushes in time with the swing build it up; pushes against it cancel. Systems respond to sine inputs in a similar way: each frequency is amplified or reduced, and delayed by some amount. That is the frequency response."),
  T("For a transfer function G of s, put s equal to i w and you get the gain and phase at frequency w. A Bode plot draws the gain in decibels, twenty times the log of the magnitude, and the phase in degrees, both against frequency on a logarithmic axis. Simple systems give straight-line asymptotes that are easy to sketch."),
  T("Why care? Because a loop goes unstable when, at the frequency where the loop is turned around by 180 degrees, the gain is still one or more. Feedback then turns negative into positive and reinforces itself. The margins measure how far from that state you are."),
  T("Phase margin is the extra delay the loop can tolerate at the crossover frequency. Gain margin is how many times the gain could be multiplied. Rules of thumb: phase margin above 45 degrees and gain margin above 2, which is 6 decibels. These numbers protect against the plant being a little different from the model."),
  T("Root locus complements this view. Plot the poles as gain k rises. Branches start at the open-loop poles and head toward the zeros or to infinity. If a branch crosses into the right half-plane at some k, that k is the stability limit. Together, Bode and root locus are the classical design toolbox.")],
 [("What does a Bode plot show?", ["Gain and phase against frequency", "Poles only", "Time response", "Noise"], 0, "Frequency response."),
  ("What is phase margin?", ["Spare phase at gain crossover", "Spare gain", "The time constant", "The overshoot"], 0, "Safety distance."),
  ("What is 0 dB?", ["Gain of one", "Gain of zero", "Gain of ten", "Infinite gain"], 0, "20 log 1."),
  ("What does a root locus plot?", ["Closed-loop poles as gain varies", "Frequency response", "Noise", "Bits"], 0, "Pole paths."),
  ("A typical good phase margin is:", ["45 to 60 degrees", "0 degrees", "180 degrees", "5 degrees"], 0, "Rule of thumb."),
  ("Why do margins matter?", ["The real plant differs from the model", "They look nice", "They reduce cost", "They fix noise"], 0, "Robustness.")],
 [("dB = 20 log10 |G|", "decibels"), ("PM = 180 + phase", "phase margin"), ("GM = 1 / |L|", "gain margin")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Root locus", "poles as gain changes"), ("Bode plot", "gain and phase against frequency"), ("Phase margin", "spare phase at crossover"), ("Gain margin", "spare gain before instability"), ("Crossover", "gain equals one")]),
  PL("Decibels", "Write db(g): 20 x log10(g) rounded to 3 decimals, for positive g.", "db(g)", '''
import math
def db(g):
    return round(20 * math.log10(g), 3)
''', [[1], [10], [0.1], [2], [0.5]], "Twenty times the base-ten log.", approx=0.002),
  PL("First-order response", "For G(s) = K / (tau s + 1), write mag_phase(K, tau, w): the list [magnitude, phase in degrees] at frequency w, magnitude K / sqrt(1 + (w tau)^2) and phase = -atan(w tau) in degrees. Round both to 3 decimals.", "mag_phase(K, tau, w)", '''
import math
def mag_phase(K, tau, w):
    m = K / math.sqrt(1 + (w * tau) ** 2)
    p = -math.degrees(math.atan(w * tau))
    return [round(m, 3), round(p, 3)]
''', [[1, 1, 1], [2, 0.5, 2], [1, 1, 0], [5, 2, 10]], "Use the magnitude and angle formulas.", approx=0.003),
  PL("Phase margin", "Write phase_margin(phase_at_crossover_deg): 180 plus the phase (a negative number) in degrees at the gain crossover frequency, rounded to 2 decimals.", "phase_margin(phase_at_crossover_deg)", '''
def phase_margin(p):
    return round(180 + p, 2)
''', [[-135], [-180], [-120.5], [-90]], "Distance from -180 degrees.", approx=0.01),
  PL("Gain margin in dB", "Write gain_margin_db(mag_at_180): if the loop magnitude at the frequency where the phase is -180 degrees is m, the gain margin in dB is -20 log10(m), rounded to 2 decimals.", "gain_margin_db(mag_at_180)", '''
import math
def gain_margin_db(m):
    return round(-20 * math.log10(m), 2)
''', [[0.5], [0.1], [1], [2]], "A smaller m means more margin.", approx=0.01)]
))

CHS.append(CH(
 "State space and state feedback",
 ("State space", [
  "State vector | holds | Position, velocity",
  "A matrix | gives | Natural dynamics",
  "B matrix | gives | Input effect",
  "Controllability | asks | Can inputs steer all states",
  "Observability | asks | Can outputs reveal states",
  "State feedback | uses | u = -Kx",
  "Observer | estimates | Hidden states"]),
 ["State-space models write a system as x' = A x + B u and y = C x, handling many inputs and outputs and giving direct access to internal variables.",
  "State feedback u = -K x changes the closed-loop matrix to A - B K. If the system is controllable, K can place the closed-loop poles anywhere we like.",
  "If we cannot measure all states, an observer estimates them from the outputs. A controller plus an observer is the basis of modern control, including the Kalman filter."],
 [("State-space model", "x' = A x + B u, y = C x, a first-order matrix description of a linear system."),
  ("Controllability", "Whether the input can move the state to any desired value."),
  ("Observability", "Whether the state can be deduced from the outputs."),
  ("Pole placement", "Choosing the feedback gain K so that A - B K has chosen eigenvalues."),
  ("Observer", "A model-based estimator of the internal state from inputs and outputs.")],
 ["x' = A x + B u.",
  "u = -K x gives x' = (A - B K) x.",
  "Poles = eigenvalues of A - BK.",
  "Controllable if [B, AB, ...] has full rank.",
  "Kalman filter: the optimal observer."],
 [T("A mass on a spring has two state variables: position and velocity. Once you know both, you can predict the future given the forces. State space writes the equations of motion as one matrix equation, x dot equals A x plus B u, where x is a list of the state variables."),
  T("The A matrix says how the state drifts by itself and the B matrix says how the input pushes it. The eigenvalues of A are the poles. A system with an eigenvalue in the right half-plane is unstable, however its equations are dressed up."),
  T("State feedback uses all the state variables: u equals minus K x. Then x dot equals A minus B K, times x. We choose K to move the poles where we want, for example to give a damping ratio of 0.7 and a chosen speed. This is pole placement, and for a second-order system the arithmetic is a simple matching of coefficients."),
  T("Can you always do this? Only if the system is controllable: the input must be able to reach every state. The test builds the matrix with columns B, A B, A squared B and so on, and checks its rank. Likewise, observability asks whether the outputs reveal the state."),
  T("When a state cannot be measured, an observer runs a copy of the model alongside the plant and corrects it using the measured output. The Kalman filter does so optimally when noise is Gaussian. Combine an observer and state feedback and you have an output-feedback controller, widely used in aircraft, spacecraft and robots.")],
 [("What does x' = A x + B u describe?", ["A linear system in state space", "A filter", "A window", "A sort"], 0, "State model."),
  ("What are the poles in state space?", ["Eigenvalues of A", "Entries of B", "Rows of C", "The inputs"], 0, "Natural modes."),
  ("What does u = -K x change?", ["A to A - BK", "B to B + K", "C to K", "x to u"], 0, "Closed-loop matrix."),
  ("What does controllability ask?", ["Can inputs reach every state?", "Can we see states?", "Is it linear?", "Is it fast?"], 0, "Steering."),
  ("What is an observer for?", ["Estimating hidden states", "Adding noise", "Raising gain", "Plotting"], 0, "Model-based estimator."),
  ("What is a Kalman filter?", ["An optimal observer", "A window", "A PID", "A sorter"], 0, "With Gaussian noise.")],
 [("x' = Ax + Bu", "state equation"), ("eig(A - BK)", "closed-loop poles"), ("rank [B AB]", "controllability test")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("State", "memory of the system"), ("A matrix", "natural dynamics"), ("Controllable", "inputs can reach every state"), ("Observer", "estimates hidden states"), ("Pole placement", "choose K to set poles")]),
  PL("Matrix times vector", "Write matvec(A, x): the product of matrix A (list of rows) and vector x (list). Return a list of numbers.", "matvec(A, x)", '''
def matvec(A, x):
    out = []
    for row in A:
        s = 0
        for j in range(len(x)):
            s = s + row[j] * x[j]
        out.append(s)
    return out
''', [[[[1, 2], [3, 4]], [1, 1]], [[[0, 1], [-2, -3]], [1, 0]], [[[2]], [5]]], "Dot each row with x."),
  PL("Euler step in state space", "Write ss_step(A, B, x, u, dt): x_next = x + dt x (A x + B u), where B is a list (a column vector) and u is a number. Return the new x rounded to 4 decimals.", "ss_step(A, B, x, u, dt)", '''
def ss_step(A, B, x, u, dt):
    out = []
    for i in range(len(x)):
        s = 0.0
        for j in range(len(x)):
            s = s + A[i][j] * x[j]
        s = s + B[i] * u
        out.append(round(x[i] + dt * s, 4))
    return out
''', [[[[0, 1], [-2, -3]], [0, 1], [0, 0], 1, 0.1], [[[0, 1], [-2, -3]], [0, 1], [1, 0], 0, 0.1], [[[-1]], [1], [0], 2, 0.5]], "Compute A x plus B u, then step."),
  PL("Place poles", "For the double integrator x1' = x2, x2' = u with u = -k1 x1 - k2 x2, the closed-loop characteristic polynomial is s^2 + k2 s + k1. Write place(wn, zeta): the gains [k1, k2] giving s^2 + 2 zeta wn s + wn^2, rounded to 4 decimals.", "place(wn, zeta)", '''
def place(wn, zeta):
    return [round(wn * wn, 4), round(2 * zeta * wn, 4)]
''', [[2, 0.7], [1, 1], [5, 0.5], [3, 0.9]], "Match coefficients.", approx=0.0002),
  PL("Controllable 2x2?", "For x' = A x + B u with 2 states, the system is controllable when the determinant of [B, A B] is non-zero. Write controllable(A, B): True or False, where B is a list of 2 numbers.", "controllable(A, B)", '''
def controllable(A, B):
    ab0 = A[0][0] * B[0] + A[0][1] * B[1]
    ab1 = A[1][0] * B[0] + A[1][1] * B[1]
    det = B[0] * ab1 - B[1] * ab0
    return abs(det) > 1e-9
''', [[[[0, 1], [-2, -3]], [0, 1]], [[[1, 0], [0, 2]], [1, 0]], [[[1, 0], [0, 2]], [1, 1]], [[[0, 1], [0, 0]], [1, 0]]], "Form the 2x2 matrix from B and AB.")]
))

CHS.append(CH(
 "Digital control and practical design",
 ("Digital control", [
  "Sampling | discretises | Control",
  "ZOH | holds | Command between samples",
  "Discrete PID | runs | In code",
  "Delay | reduces | Phase margin",
  "Saturation | limits | The actuator",
  "Noise | corrupts | Measurements",
  "Robustness | covers | Model errors"]),
 ["Controllers run on computers at a fixed sample time T. A zero-order hold keeps each command constant between samples. The model and the PID must be discretised.",
  "Sampling and computation add delay, which eats phase margin, so a good rule is to sample 10 to 20 times faster than the closed-loop bandwidth.",
  "Real designs deal with actuator limits, sensor noise, dead zones, delays and modelling errors. Robustness means still working when the plant is not exactly as modelled."],
 [("Sample time", "The period T between controller updates."),
  ("Zero-order hold", "Holding the controller output constant between samples."),
  ("Dead time", "A pure delay between input and output effects."),
  ("Robustness", "Ability to keep performance despite model error and disturbances."),
  ("Feedforward", "Adding a command based on the known setpoint or disturbance instead of waiting for error.")],
 ["Sample 10 to 20 times faster than bandwidth.",
  "Delay costs phase: w T radians.",
  "Always limit actuator commands.",
  "Feedforward plus feedback is best.",
  "Test with model error."],
 [T("A modern controller is a few lines of code running in a loop. Read the sensor, compute the command, write the actuator, wait for the next tick. The tick period matters. Too slow and the loop cannot respond to changes in time. Too fast wastes computing and amplifies noise in the derivative."),
  T("Every delay costs phase. A delay of D seconds adds minus w D radians of phase at frequency w. At the crossover frequency this can cut the phase margin sharply, even push a stable loop into instability. That is why a long dead time, as in a long pipe or a network link, makes control hard."),
  T("The discrete PID is simple. The integral becomes a running sum times T, the derivative a difference over T. Add output limits and anti-windup. Filtering the measurement slightly keeps noise from turning into jitter in the command. Use fixed-size arithmetic with care."),
  T("Feedback reacts only after an error appears. If you know in advance what is coming, such as a setpoint change or a measurable disturbance, you can add a feedforward term that acts at once, and let feedback clean up the small remainder. Together they give fast, accurate control."),
  T("Finally, test the design against reality: change the plant gain by plus or minus thirty percent, add noise, add delay, saturate the actuator. A controller that survives is robust. Advanced methods such as model predictive control optimise the plan over a horizon within the constraints, and are now common in industry, though PID remains the workhorse.")],
 [("What does a zero-order hold do?", ["Holds the command constant between samples", "Removes noise", "Adds gain", "Samples faster"], 0, "Constant."),
  ("How fast should a controller sample?", ["10 to 20 times the bandwidth", "Equal to the bandwidth", "Half the bandwidth", "Once a minute"], 0, "Rule of thumb."),
  ("What does delay do to margins?", ["Reduces phase margin", "Increases it", "Nothing", "Adds gain"], 0, "w D lag."),
  ("What is feedforward?", ["Acting on known inputs before error appears", "Measuring the output", "Filtering noise", "Integrating error"], 0, "Anticipation."),
  ("Why limit the actuator command?", ["Real actuators saturate", "To save code", "To raise gain", "To reduce poles"], 0, "Physical limits."),
  ("What is MPC?", ["Optimising control over a future horizon", "A sensor", "A filter", "A PID variant without gains"], 0, "Model predictive control.")],
 [("T", "sample time"), ("w D", "phase lost to delay (radians)"), ("u = u_ff + u_fb", "feedforward plus feedback")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Sample time", "controller period"), ("Zero-order hold", "constant between samples"), ("Dead time", "pure delay"), ("Feedforward", "acts before error appears"), ("Robustness", "works despite model error")]),
  PL("Delay phase loss", "A delay of D seconds loses w x D radians of phase at angular frequency w. Write delay_phase_deg(w, D): the loss in degrees, rounded to 2 decimals.", "delay_phase_deg(w, D)", '''
import math
def delay_phase_deg(w, D):
    return round(math.degrees(w * D), 2)
''', [[10, 0.1], [2, 0.5], [100, 0.01], [1, 0]], "Convert radians to degrees.", approx=0.01),
  PL("Sample rate check", "Write sample_ok(bandwidth_hz, sample_hz): True if the sample rate is at least 10 times the closed-loop bandwidth, otherwise False.", "sample_ok(bandwidth_hz, sample_hz)", '''
def sample_ok(bandwidth_hz, sample_hz):
    return sample_hz >= 10 * bandwidth_hz
''', [[1, 10], [1, 5], [2, 100], [50, 400]], "Compare against ten times the bandwidth."),
  PL("Delayed loop", "A pure delay of d steps: the plant sees the command from d steps ago. Write delay_line(u, d): shift the list u right by d positions, filling the start with zeros, and keep the original length.", "delay_line(u, d)", '''
def delay_line(u, d):
    out = []
    for i in range(len(u)):
        if i - d >= 0:
            out.append(u[i - d])
        else:
            out.append(0)
    return out
''', [[[1, 2, 3, 4], 2], [[5, 6, 7], 0], [[1, 2], 5], [[], 1]], "Index back by d."),
  PL("Feedforward plus feedback", "Plant: y[k+1] = y[k] + 0.2 (u[k] - y[k]). Command u = ff + kp (r - y) where ff = r (the feedforward guess for a plant of gain 1). Write ff_sim(r, kp, steps, start): y after each step starting at y = start, rounded to 4 decimals.", "ff_sim(r, kp, steps, start)", '''
def ff_sim(r, kp, steps, start):
    y = float(start)
    out = []
    for k in range(steps):
        u = r + kp * (r - y)
        y = y + 0.2 * (u - y)
        out.append(round(y, 4))
    return out
''', [[1, 0, 4, 0], [2, 1, 4, 0], [1, 2, 3, 0.5], [3, 0, 3, 3]], "Add the feedforward and the feedback parts.")]
))
