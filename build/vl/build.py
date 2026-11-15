# -*- coding: utf-8 -*-
"""Builds the standalone webxdc Verilog lab pages: Icarus Verilog engine (VeriSim, GPL-2.0) + UI + one lab config."""
import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack


def _rd(*p):
    return open(os.path.join(HERE, *p), encoding="utf-8").read()


def lab_html(title, intro, levels, gen="2005"):
    for lv in levels:
        lv.setdefault("gen", gen)
    cfg = json.dumps({"title": title, "intro": intro, "levels": levels}).replace("</", "<\\/")
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title><style>%s</style></head><body>'
            '<script>%s</script><script>window.VLCFG=%s;</script><script>%s</script></body></html>') % (title, _rd("vlab.css"), pack.engine_js().replace("</script", "<\\/script"), cfg, _rd("vlab.js"))


def cmos_html(title, intro, levels):
    cfg = json.dumps({"title": title, "intro": intro, "levels": levels}).replace("</", "<\\/")
    return ('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title><style>%s</style></head><body>'
            '<script>window.CMOSCFG=%s;</script><script>%s</script></body></html>') % (title, _rd("vlab.css"), cfg, _rd("cmos.js"))
