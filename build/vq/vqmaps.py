# -*- coding: utf-8 -*-
"""Concept maps are the first CH argument in vq_a / vq_b; collected here for the builder."""
import vq_a, vq_b
MAPS = [(c["maps"][0]["title"], c["maps"][0]["links"]) for c in vq_a.CHS + vq_b.CHS]
