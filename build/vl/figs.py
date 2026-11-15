# -*- coding: utf-8 -*-
import os
from figs_a import ALL_A
from figs_b import ALL_B
ALL = dict(ALL_A); ALL.update(ALL_B)


def build_all(outdir="/tmp/vl_figs"):
    os.makedirs(outdir, exist_ok=True); res = {}
    for fn, f in ALL.items():
        svg = f().render(); open(os.path.join(outdir, fn), "w", encoding="utf-8").write(svg); res[fn] = svg
    return res


if __name__ == "__main__":
    r = build_all(); print(len(r), "figures", sum(len(v) for v in r.values()) // 1024, "KB")
