#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Control Theory course. Usage: python3 make_control_theory_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "ctl"))
import cmk, ctl_a, ctl_b, make_apps  # noqa: E402
make_apps.main()
CHS = ctl_a.CHS + ctl_b.CHS
PRONOUNCE = {"PID": "P I D", "Laplace": "la plahss", "Routh": "rowth", "Hurwitz": "hur vits", "Kalman": "kal mun", "Nyquist": "nye kwist", "Bode": "bo dee", "eigenvalues": "eye gun val yooz",
    "eigenvalue": "eye gun val yoo", "zeta": "zay tuh", "tau": "tau", "wn": "omega n", "MPC": "M P C", "feedforward": "feed forward", "linearisation": "lin ee ar eye zay shun", "Runge": "run guh",
    "Kutta": "koo tah", "damping": "damp ing", "overdamped": "over damped", "underdamped": "under damped", "dB": "decibels", "ZOH": "Z O H"}
SANDBOX = cmk.terminal("Control cheat sheet", "ctl>", "A scripted lookup. Try: error, tau, zeta, poles, pid, margins, state, sample", [
    ("error", ["e = r - y: setpoint minus output."]),
    ("tau", ["First-order step: y = K (1 - e^(-t/tau)). 63 percent at tau, 95 percent at 3 tau."]),
    ("zeta", ["Overshoot = exp(-pi zeta / sqrt(1 - zeta^2)). Settling about 4 / (zeta wn)."]),
    ("poles", ["Stable if every pole has a negative real part."]),
    ("pid", ["u = Kp e + Ki integral(e) + Kd de/dt. Limit the output and prevent windup."]),
    ("margins", ["Phase margin above 45 degrees, gain margin above 6 dB."]),
    ("state", ["x' = A x + B u; with u = -K x the poles are eig(A - BK)."]),
    ("sample", ["Sample 10 to 20 times faster than the closed-loop bandwidth."]),
])
EXAM = [
 ("What is the plant?", ["The system being controlled", "The sensor", "The target", "The noise"], 0, "Motor, room, rocket."),
 ("How is the error defined?", ["Setpoint minus output", "Output minus noise", "Input times gain", "Sensor minus actuator"], 0, "e = r - y."),
 ("Which controller ignores the output?", ["Open loop", "Closed loop", "PID", "Observer"], 0, "Oven timer."),
 ("What does the time constant tau mean?", ["Time to reach 63 percent of the step", "Final value", "Noise level", "Gain"], 0, "First-order."),
 ("After 3 tau, how much of a step is done?", ["About 95 percent", "About 63 percent", "About 50 percent", "100 percent"], 0, "1 - e^-3."),
 ("What does Euler's method do?", ["Steps the state by rate times dt", "Solves exactly", "Tunes PID", "Finds margins"], 0, "A simple simulation."),
 ("What does zeta below 1 mean?", ["Underdamped, with overshoot", "Overdamped", "Unstable", "No poles"], 0, "Rings."),
 ("Which damping is fastest without overshoot?", ["Critical damping", "Underdamping", "Zero damping", "Negative damping"], 0, "zeta = 1."),
 ("Where must poles lie for stability?", ["Left half of the s-plane", "Right half", "On the imaginary axis only", "At the origin"], 0, "Negative real part."),
 ("What is the closed-loop transfer function with unity feedback?", ["L / (1 + L)", "L x (1 + L)", "1 / L", "L - 1"], 0, "Loop gain over one plus loop gain."),
 ("What is the Routh-Hurwitz test for?", ["Stability from coefficients", "Noise", "Sampling", "Tuning"], 0, "No root-finding."),
 ("What does the I in PID remove?", ["Steady-state error", "Noise", "Delay", "Overshoot only"], 0, "Persistent offset."),
 ("What does the D term do?", ["Damps using the error trend", "Removes offset", "Adds delay", "Cuts gain"], 0, "Derivative."),
 ("What is integrator windup?", ["Integral growth while the actuator saturates", "A noise source", "A sensor fault", "A filter"], 0, "Anti-windup helps."),
 ("What does too large a Kp cause?", ["Overshoot and oscillation", "Slow response", "No error", "Less noise"], 0, "Eager."),
 ("What does a Bode plot show?", ["Gain and phase against frequency", "Poles only", "Time response", "Noise"], 0, "Frequency response."),
 ("What is 0 dB?", ["A gain of one", "A gain of zero", "A gain of ten", "Infinite gain"], 0, "20 log 1."),
 ("A good phase margin is about:", ["45 to 60 degrees", "0 degrees", "5 degrees", "180 degrees"], 0, "Rule of thumb."),
 ("What does root locus show?", ["Closed-loop poles as gain varies", "Frequency response", "Noise", "Bit depth"], 0, "Pole paths."),
 ("In x' = A x + B u, the poles are:", ["Eigenvalues of A", "Entries of B", "Rows of C", "Inputs"], 0, "Natural modes."),
 ("With u = -K x, the closed-loop matrix is:", ["A - BK", "A + BK", "BK", "AK"], 0, "State feedback."),
 ("What does controllability mean?", ["Inputs can reach every state", "Outputs reveal all states", "System is linear", "System is fast"], 0, "Steering."),
 ("What is an observer?", ["An estimator of hidden states", "A noise source", "A PID gain", "A filter window"], 0, "Model-based."),
 ("What does delay do to phase margin?", ["Reduces it", "Raises it", "Nothing", "Adds gain"], 0, "w D lag."),
 ("What is feedforward?", ["Acting on known inputs before error appears", "Measuring output", "Integrating error", "Filtering noise"], 0, "Anticipation."),
 ("How fast should the loop sample?", ["10 to 20 times the bandwidth", "Equal to the bandwidth", "Half the bandwidth", "Once a day"], 0, "Rule of thumb."),
]
CFG = dict(id="control-theory", title="Control Theory",
    subtitle="Feedback, stability, PID, frequency methods and state space, with runnable Python labs and a PID tuner",
    description="A hands-on introduction to classical and modern control: feedback and the control problem, modelling with differential equations and Euler simulation, first and second-order responses with damping and overshoot, transfer functions, poles and Routh-Hurwitz stability, PID design with anti-windup, root locus and Bode margins, state-space models with pole placement, controllability and observers, and digital implementation including delay, sampling and feedforward. Every chapter has Python labs verified in the built-in interpreter, and two interactive labs let you move poles around the s-plane and tune a PID loop live.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="ctl", apps={"__POLES__": "poles.html", "__PID__": "pid.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "control-theory.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
