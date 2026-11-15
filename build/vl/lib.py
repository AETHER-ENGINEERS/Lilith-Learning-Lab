# -*- coding: utf-8 -*-
"""Helpers for the Verilog labs: self-checking testbench generators and level builders."""


def _w(w): return "" if w == 1 else "[%d:0] " % (w - 1)


def combtb(top, ins, outs, rows, gap=5, name="dut"):
    """ins/outs: [(name, width)]; rows: [(in_values, out_values)] -> self-checking testbench text (prints ALL PASS)."""
    L = ["`timescale 1ns/1ps", "module tb;"]
    for n, w in ins: L.append("  reg %s%s;" % (_w(w), n))
    for n, w in outs: L.append("  wire %s%s;" % (_w(w), n))
    conn = ", ".join(".%s(%s)" % (n, n) for n, _ in ins + outs)
    L.append("  %s %s(%s);" % (top, name, conn))
    L += ["  integer errs;", "  initial begin", '    $dumpfile("dump.vcd"); $dumpvars(0, tb);', "    errs = 0;"]
    first = True
    for iv, ov in rows:
        L.append("    %s#%d;" % ("" if first else "", gap) if False else "")
        L.append("    " + " ".join("%s = %d'd%d;" % (n, w, v) for (n, w), v in zip(ins, iv)) + " #%d;" % gap)
        for (n, w), v in zip(outs, ov):
            lhs = ", ".join("%s" % x for x, _ in ins)
            fmt = " ".join("%s=%%0d" % x for x, _ in ins)
            L.append('    if (%s !== %d\'d%d) begin errs = errs + 1; $display("FAIL: %s -> %s=%%0d, expected %d", %s, %s); end' % (n, w, v, fmt, n, v, lhs, n))
    L += ['    if (errs == 0) $display("ALL PASS: %d rows"); else $display("%%0d wrong outputs", errs);' % len(rows), "    #%d $finish;" % gap, "  end", "endmodule", ""]
    return "\n".join(x for x in L if x != "")


def rows_from(fn, ins, vectors):
    """vectors: list of input value lists; fn returns a list of output values."""
    return [(list(v), list(fn(*v))) for v in vectors]


def exhaustive(widths):
    import itertools
    return [list(t) for t in itertools.product(*[range(2 ** w) for w in widths])]


def sample(widths, n=24):
    """corners plus a deterministic spread"""
    import itertools
    out = []; seen = set()
    mx = [2 ** w - 1 for w in widths]
    for t in [[0] * len(widths), mx[:]] + [[(m if i == j else 0) for j, m in enumerate(mx)] for i in range(len(widths))]:
        if tuple(t) not in seen: seen.add(tuple(t)); out.append(t)
    s = 12345
    while len(out) < n:
        s = (s * 1103515245 + 12345) & 0x7fffffff
        t = []; x = s
        for m in mx:
            t.append((x >> 4) % (m + 1)); x = (x * 69069 + 1) & 0x7fffffff
        if tuple(t) not in seen: seen.add(tuple(t)); out.append(t)
    return out


def LV(title, text, hint, starter, solution, tb, goals=None, edit="design", extra=()):
    """One level. edit='design': student edits design.v, tb.v is read-only. edit='tb': student edits tb.v, design.v read-only."""
    g = [{"t": "It compiles", "re": "COMPILE"}] + (goals if goals is not None else [{"t": "Every test row passes (ALL PASS)", "re": "ALL PASS"}]) + list(extra)
    if edit == "design":
        files = [{"name": "design.v", "src": starter, "edit": True}, {"name": "tb.v", "src": tb, "edit": False}]
        sol = {"design.v": solution}
    elif edit == "tb":
        files = [{"name": "design.v", "src": starter, "edit": False}, {"name": "tb.v", "src": tb, "edit": True}]
        sol = {"tb.v": solution}
    else:
        raise ValueError(edit)
    return {"title": title, "text": text, "hint": hint, "files": files, "solution": sol, "goals": g}


def seqtb(top, ins, outs, script, clk="clk", params="", gap=5):
    """Sequential self-checking testbench. ins/outs: [(name, width)] (the clock is added automatically if clk).
    script items: ('in', {name: value}) set inputs; ('tick',) or ('tick', n); ('exp', {name: value}, label); ('wait', n)."""
    L = ["`timescale 1ns/1ps", "module tb;"]
    if clk: L.append("  reg %s = 0;" % clk)
    for n, w in ins: L.append("  reg %s%s = 0;" % (_w(w), n))
    for n, w in outs: L.append("  wire %s%s;" % (_w(w), n))
    pins = ([clk] if clk else []) + [n for n, _ in ins] + [n for n, _ in outs]
    L.append("  %s %sdut(%s);" % (top, params, ", ".join(".%s(%s)" % (p, p) for p in pins)))
    L += ["  integer errs = 0;"]
    if clk: L += ["  task tick; begin #2 %s = 1; #3 %s = 0; #2; end endtask" % (clk, clk)]
    W = dict(ins + outs)
    L += ["  initial begin", '    $dumpfile("dump.vcd"); $dumpvars(0, tb);', "    #1;"]
    for st in script:
        if st[0] == "in":
            L.append("    " + " ".join("%s = %d'd%d;" % (n, W[n], v) for n, v in st[1].items()) + " #1;")
        elif st[0] == "tick":
            for _ in range(st[1] if len(st) > 1 else 1): L.append("    tick;")
        elif st[0] == "wait":
            L.append("    #%d;" % st[1])
        elif st[0] == "exp":
            for n, v in st[1].items():
                L.append('    if (%s !== %d\'d%d) begin errs = errs + 1; $display("FAIL [%s]: %s=%%0d, expected %d", %s); end' % (n, W[n], v, st[2] if len(st) > 2 else "", n, v, n))
    L += ['    if (errs == 0) $display("ALL PASS"); else $display("%0d checks failed", errs);', "    #5 $finish;", "  end", "endmodule"]
    return "\n".join(L) + "\n"
