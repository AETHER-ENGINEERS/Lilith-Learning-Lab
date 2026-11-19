# -*- coding: utf-8 -*-
"""Expanded ELI5 blocks for the CTMV course (one per chapter)."""
import re


def _split(t, lim=380):
    if len(t) <= lim:
        return [t]
    cuts = [m.end() for m in re.finditer(r"[.!?] (?=[A-Z(])", t)]
    if not cuts:
        return [t]
    k = min(cuts, key=lambda c: abs(c - len(t) / 2))
    return _split(t[:k].rstrip(), lim) + _split(t[k:], lim)


def E(pic, words, tryit, keep):
    return ("\n\n".join(_split(pic) + _split("Now the real words. " + words) + ["Try it. " + tryit, "If you remember one thing: " + keep]), "")


FEY = [
 E('You keep a drawer of notes. A search finds notes with the same words, but not the notes that are secretly about the same thing. You want a helper who notices.', 'The Commutative Tri-Modal Vault, CTMV, is a design for notes and AI memory. It answers four failures: ideas that never meet, collections that decay, old and new facts that clash, and memory locked to one model.', 'Name the four failures.', 'Islands, decay, conflict, lock-in.'),
 E('One town, three ways: a photo, a street map and a list of distances. They all describe the same town, and each answers different questions.', 'The same notes are kept as V, plain files, G, facts and rules, and M, vectors. V is the truth. G and M are built from it and can be rebuilt.', 'Say which view is precious.', 'V is truth, G is logic, M is feel.'),
 E('A recipe card in your own handwriting. You can read it, copy it and carry it to any kitchen. Nobody can take it away by changing an oven.', 'The vault is a folder of markdown notes with a heading, tags, prose, claim lines of three words, and links. Writes use a temp file and a rename so a note is never half-written.', 'Write a claim line about rain and floods.', 'Plain files, three-word claims, write then rename.'),
 E('A very careful librarian. You tell her two facts, and ask if one leads to the other. She does not guess. She points to your two facts and the rule that joins them, or says she does not know.', 'G turns claim lines into facts. Rules derive more facts, constraints catch contradictions, and answers are proven, contradicted or unknown, with a proof.', 'Say what unknown means.', 'Facts, rules, constraints; proven, contradicted, unknown.'),
 E('A map of a library where similar books sit close, even if their titles share no words. The map helps you find your way, but it does not say who is right.', 'M gives each note a vector. Nearby vectors mean similar notes. The labs use SQLite with sqlite-vec and a toy hashing embedder so results repeat. Nearness cannot tell cause, time or contradiction.', 'Say why nearest is not always best.', 'Text to vector to neighbour; nearness is not truth.'),
 E('Two friends look for a restaurant, one with a map and one following the smell of food. If they reach the same door, map and nose agree. If not, one of them knows something.', 'Embedding directly, phi, and extracting facts then warping, f of pi, should land in the same place. Delta measures how far apart they land. A high delta is a clue.', 'Say what a high delta can mean.', 'Two routes, one place; delta is the gap.'),
 E('A teacher says, this reminds me of something from another subject. That is where understanding jumps, and plain search cannot say it.', 'A bridge is a pair of notes that share an idea in G, sit far apart in M and have no link in V. A near pair with nothing shared is a false friend. You decide what to keep.', 'Give an example bridge.', 'Far in M, shared in G, unlinked in V.'),
 E('A gardener walks the garden and leaves sticky notes: crowded here, these two would look nice together, nothing planted there. You decide what to do.', 'The gardener checks contradictions, latent syntheses, gaps and orphans, and writes suggestions. It never edits your notes, and rejected suggestions are remembered.', 'Name the four checks.', 'Look, list, leave the decision to you.'),
 E('A map where a motorway makes two towns feel close and a river makes neighbours feel far. You did not move the towns, only the travel time.', 'Warping changes distance: causal links shrink it by one minus lambda, conflicts add mu. Vectors do not move. With both at zero you get plain search.', 'Say what lambda and mu do.', 'Pull causes, push conflicts, change the ruler.'),
 E('Ask a colleague why the site went down. A poor one gives you five emails. A good one gives the cause, what made it worse, and says two people disagree.', 'Retrieval finds the nearest note, hops along warped edges within a reach, drops notes that a newer note replaced, and flags notes in an open dispute.', 'Say replaced versus disputed.', 'Seed, hop, drop, flag.'),
 E('Recipe cards in your own handwriting. You can change ovens, cooks and kitchens. A recipe stuck inside a smart oven is lost when the oven goes.', 'The files are the memory. Throw away G and M, replay from the files, and the facts come out identical. A new embedding model changes M only. Fingerprints prove the replay.', 'Say what replay rebuilds.', 'Files are the memory.'),
 E('A new gadget built from parts already in your toolbox. You still have to test it before you trust it.', 'The labs use the Jade Agent Kit for files, SQLite and sqlite-vec, and the Jade Vault reasoner. A real embedder is the missing part. CTMV is a design; measure it by planting known bridges and conflicts.', 'Say how to test the design.', 'Build, plant, measure.'),
 E('A child builds towers from blocks. Each time a new idea makes the tower simpler to describe, she gets a little happy. A pile of random blocks is exciting to look at but gives no such feeling, so she does not keep staring at it.', 'Artificial curiosity rewards compression progress. A hypothesis that makes the vault shorter to describe is worth testing. Noise surprises you but teaches nothing. A leap is such a hypothesis chosen by that score and checked by the reasoner. Creativity combines known patterns into new ones, and a small agent can do science by planning experiments, being curious, inventing and predicting.', 'In Lab 5, ask which hypothesis compresses your notes most, take the leap, then add a filler note and see it score below zero.', 'Be curious about what you can learn, not about what only surprises you.'),
]
