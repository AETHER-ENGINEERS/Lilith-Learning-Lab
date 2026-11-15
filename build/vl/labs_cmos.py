# -*- coding: utf-8 -*-
"""CMOS switch labs for chapters 2 and 3 (no engine needed)."""
SW = ("Lab 1: Transistors are switches", "Flip the gate voltage and watch the switch. An nMOS closes when its gate is 1; a pMOS closes when its gate is 0.", 720, [
    {"kind": "switch", "mode": "n", "title": "The nMOS switch", "text": "Press Gate = 1 and Gate = 0. An nMOS transistor conducts when the gate is high.", "goals": [{"t": "Gate = 1: the nMOS conducts (lamp lit)", "k": "g1"}, {"t": "Gate = 0: the nMOS is open (lamp dark)", "k": "g0"}]},
    {"kind": "switch", "mode": "p", "title": "The pMOS switch", "text": "A pMOS is the mirror image: it conducts when the gate is LOW.", "goals": [{"t": "Gate = 0: the pMOS conducts (lamp lit)", "k": "g0"}, {"t": "Gate = 1: the pMOS is open (lamp dark)", "k": "g1"}]},
    {"kind": "switch", "mode": "inv", "title": "Put them together: the CMOS inverter", "text": "A pMOS to VDD and an nMOS to ground share one gate input A. Whichever is on drags Y to its rail. Try both inputs: the output is always the opposite of the input, and the two are never on together.", "goals": [{"t": "A = 0 gives Y = 1 (pMOS on)", "k": "in0"}, {"t": "A = 1 gives Y = 0 (nMOS on)", "k": "in1"}]},
])
def G(title, text, ins, expr, fn, start, sol, inner=None, rest=None):
    d = {"kind": "gate", "title": title, "text": text, "ins": ins, "expr": expr, "start": start, "sol": sol}
    if inner: d["inner"] = inner; d["rest"] = rest
    return d, fn
_lv = []
_defs = [
 ("NAND: series down, parallel up", "Two inputs A and B. Choose how the nMOS transistors (pull-down) and the pMOS transistors (pull-up) are connected: in series or in parallel. Y must be 1 unless both inputs are 1. The pull-up and pull-down must never both conduct, and one must always conduct.", ["A", "B"], "NOT (A AND B)", lambda v: not (v[0] and v[1]),
  {"pu": {"top": "S"}, "pd": {"top": "S"}}, {"pu": {"top": "P"}, "pd": {"top": "S"}}, None, None),
 ("NOR: parallel down, series up", "Now Y must be 1 only when both inputs are 0. Use the duality: where one network is in series, the other is in parallel.", ["A", "B"], "NOT (A OR B)", lambda v: not (v[0] or v[1]),
  {"pu": {"top": "P"}, "pd": {"top": "S"}}, {"pu": {"top": "S"}, "pd": {"top": "P"}}, None, None),
 ("AND-OR-INVERT: Y = NOT (A·B + C)", "A complex gate in one stage. The pull-down has two levels: A and B form a group, which is then combined with C. The pull-up is the dual of the pull-down.", ["A", "B", "C"], "NOT ((A AND B) OR C)", lambda v: not ((v[0] and v[1]) or v[2]),
  {"pu": {"top": "S", "inner": "S"}, "pd": {"top": "S", "inner": "S"}}, {"pu": {"top": "S", "inner": "P"}, "pd": {"top": "P", "inner": "S"}}, ["A", "B"], ["C"]),
 ("OR-AND-INVERT: Y = NOT ((A + B)·C)", "Same idea with the roles swapped: the group is an OR, combined with C by an AND.", ["A", "B", "C"], "NOT ((A OR B) AND C)", lambda v: not ((v[0] or v[1]) and v[2]),
  {"pu": {"top": "S", "inner": "S"}, "pd": {"top": "P", "inner": "P"}}, {"pu": {"top": "P", "inner": "S"}, "pd": {"top": "S", "inner": "P"}}, ["A", "B"], ["C"]),
]
GATES_JS = []
for t, tx, ins, expr, fn, start, sol, inner, rest in _defs:
    d = {"kind": "gate", "title": t, "text": tx, "ins": ins, "expr": expr, "start": start, "sol": sol}
    if inner: d["inner"] = inner; d["rest"] = rest
    # truth table for the JS side
    import itertools
    d["table"] = {"".join(map(str, v)): int(bool(fn(list(v)))) for v in itertools.product([0, 1], repeat=len(ins))}
    GATES_JS.append(d)
GATES = ("Lab 2: Build CMOS gates", "Choose series or parallel for each transistor network and check the truth table. A good gate always has exactly one network conducting.", 1100, GATES_JS)
LABS_CMOS = [SW, GATES]
