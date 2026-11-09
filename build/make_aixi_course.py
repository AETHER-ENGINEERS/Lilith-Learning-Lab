#!/usr/bin/env python3
"""Build the AIXI course. Usage: python3 make_aixi_course.py <out.json>"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "aixi"))
import aix1, aix2, aix3  # noqa: E402
from make_trinity_course import split_long, stack  # noqa: E402


def app(name):
    with open(os.path.join(HERE, "aixi", "apps", name), encoding="utf-8") as f:
        return f.read()


PRONOUNCE = {
    "AIXItl": "eye ksee tee ell", "MC-AIXI-CTW": "M C eye ksee C T W", "AIXI": "eye ksee", "Hutter": "hoot er", "Solomonoff": "sol oh mon off",
    "Kolmogorov": "kol mo gor off", "Chaitin": "chay tin", "Legg": "leg", "Leike": "lie kuh", "Orseau": "or so", "Veness": "ven ess",
    "Schmidhuber": "shmid hoo ber", "Vitanyi": "vee tah nee", "Krichevsky": "kri chev ski", "Trofimov": "tro fee mov", "Jeffreys": "jef reez",
    "Szepesvári": "seh peh shvar ee", "Kocsis": "ko chish", "rho-UCT": "row U C T", "UCT": "U C T", "UCB": "U C B", "CTW": "C T W",
    "expectimax": "expecti max", "Expectimax": "Expecti max", "Kraft": "kraft", "Pareto": "pa ray toe", "Thompson": "tomp son",
    "Upsilon": "up sigh lon", "Υ": "upsilon", "Godel": "ger dell", "Levin": "lev in", "nu one": "new one", "xi": "ksai",
}

SANDBOX = {
    "type": "terminal", "title": "AIXI lookup", "prompt": "aixi>",
    "intro": "A scripted lookup, not a real agent. Try: equation, prior, intelligence, mcaixi, help",
    "chips": ["equation", "prior", "intelligence", "mcaixi", "help"],
    "commands": [
        {"re": "^help$", "out": ["equation      the AIXI action rule", "prior         the universal prior", "intelligence  the Legg-Hutter measure", "mcaixi        the practical approximation"]},
        {"re": "^equation$", "out": ["a_k = argmax_a sum_percept ... max_a sum_percept [r_k+...+r_m] * sum_{q consistent} 2^-length(q)"]},
        {"re": "^prior$", "out": ["M(x) = sum of 2^-length(p) over programs p whose output starts with x"]},
        {"re": "^intelligence$", "out": ["Upsilon(pi) = sum_mu 2^-K(mu) * V(pi, mu)"]},
        {"re": "^mcaixi$", "out": ["Context tree weighting learns the model; rho-UCT plans by sampling (Veness et al., JAIR 2011)"]},
        {"re": ".", "out": ["Unknown command. Type help."], "cls": "err"}],
    "tasks": []
}

EXAM = [
    ('Who proposed AIXI?', ['Marcus Hutter', 'Alan Turing', 'Claude Shannon', 'John McCarthy'], 0, 'Proposed in 2000; results in the 2005 book.'),
    ('What two ideas make up AIXI?', ['Solomonoff induction and expectimax planning', 'Backpropagation and dropout', 'Alpha-beta and hashing', 'Clustering and sorting'], 0, 'Prediction plus planning.'),
    ('What does a percept contain?', ['An observation and a reward', 'Only an action', 'A program', 'A policy'], 0, 'o_t and r_t.'),
    ('Does AIXI assume the environment is Markov?', ['No, the whole history may matter', 'Yes', 'Only for games', 'Only with discounting'], 0, 'No Markov assumption.'),
    ('What does expectimax do at a chance node?', ['Averages over the environment replies', 'Maximizes', 'Prunes', 'Samples one action'], 0, 'Expectation over percepts.'),
    ('Why is exact expectimax impractical?', ['The tree grows exponentially with the horizon', 'It is not optimal', 'It needs labels', 'It forgets'], 0, 'Leaves multiply every step.'),
    ('Mixture probability xi(x) equals:', ['Sum of w_i nu_i(x)', 'Largest nu_i(x)', 'Product of nu_i(x)', 'Zero'], 0, 'A weighted average.'),
    ('The dominance property says:', ['xi(x) >= w_i nu_i(x) for each i', 'xi is deterministic', 'xi(x) = 1', 'xi is random'], 0, 'A sum is at least each term.'),
    ('What is the mixture\'s extra log-loss over model i at most?', ['ln(1/w_i)', 'The data length', 'Zero', 'w_i'], 0, 'A one-time cost.'),
    ('What is Kolmogorov complexity K(x)?', ['Length of the shortest program printing x', 'Number of ones in x', 'Runtime of x', 'Entropy of a coin'], 0, 'Shortest description.'),
    ('Is K computable?', ['No', 'Yes', 'Only for short strings', 'Only for binary strings'], 0, 'Incomputable.'),
    ('What does the invariance theorem say?', ['Machine choice changes K by a constant', 'K never changes', 'K is always small', 'K is linear'], 0, 'A fixed-length interpreter.'),
    ('What does the Kraft inequality say about prefix-free programs?', ['Sum of 2^-length is at most 1', 'Lengths are equal', 'All programs halt', 'There are finitely many'], 0, 'So they act as probabilities.'),
    ('How is the next-symbol probability in Solomonoff induction found?', ['M(xa) / M(x)', 'M(x) + M(a)', 'The longest program', 'A coin flip'], 0, 'Ratio of prior probabilities.'),
    ('The total prediction error of Solomonoff induction on computable data is bounded by:', ['A multiple of K of the source', 'The sequence length', 'Zero', 'A constant independent of the source'], 0, 'Depends on the complexity of mu.'),
    ('Why can Solomonoff induction not be run exactly?', ['M is only lower semicomputable', 'It is not Bayesian', 'It needs labels', 'It overfits'], 0, 'Halting is undecidable.'),
    ('In the halving argument, what happens at each mistake?', ['The surviving weight at least halves', 'Nothing', 'The weight doubles', 'The true model is removed'], 0, 'The losing side held at least half.'),
    ('What does the innermost sum in the AIXI equation count?', ['Weight of programs producing the history', 'The reward', 'The actions', 'The horizon'], 0, 'Sum of 2^-length over consistent programs.'),
    ('What are the explicit parameters of AIXI?', ['Universal machine and horizon', 'Learning rate and depth', 'Batch size', 'Seed'], 0, 'Plus a discount if used.'),
    ('What happens to a deterministic hypothesis contradicted by the history?', ['It is eliminated', 'It gains weight', 'It is copied', 'It is ignored'], 0, 'It is inconsistent.'),
    ('A geometric discount gives:', ['A fixed effective horizon', 'A growing horizon', 'No horizon', 'Negative rewards'], 0, 'gamma^k weights.'),
    ('How does the harmonic horizon behave?', ['Grows with the agent age', 'Is constant', 'Shrinks', 'Is zero'], 0, 'The tail is about 1/t.'),
    ('Why are immortal undiscounted agents lazy?', ['Postponing rewards costs nothing', 'They are slow', 'They forget', 'They overfit'], 0, 'Hutter\'s remark.'),
    ('What is Pareto optimality?', ['No other policy dominates', 'Highest reward', 'Shortest program', 'Random policy'], 0, 'A dominance property.'),
    ('Universal intelligence Upsilon is:', ['Sum over environments of 2^-K(mu) V(pi, mu)', 'Average reward on chess', 'An IQ score', 'The agent\'s speed'], 0, 'Legg and Hutter, 2007.'),
    ('What did Legg and Hutter require to avoid discounting?', ['Total reward at most 1 in each environment', 'No rewards', 'Only deterministic worlds', 'A finite alphabet'], 0, 'Bounded total reward.'),
    ('Why is AIXI incomputable?', ['It needs to know which programs halt', 'It uses randomness', 'It has no reward', 'It needs a GPU'], 0, 'Halting problem.'),
    ('What is the cost per cycle of AIXItl?', ['About t * 2^l', 'Constant', 'Linear in l', 'Logarithmic'], 0, 'Exponential in l.'),
    ('How does Levin search share time?', ['2^-length per program', 'Equally', 'By age', 'Randomly'], 0, 'Short programs first.'),
    ('The KT estimator after a zeros and b ones gives P(1) =', ['(b + 1/2) / (a + b + 1)', 'b / a', '1/2', 'a / b'], 0, 'A Jeffreys prior.'),
    ('In CTW, an inner node mixes:', ['Its own KT estimate and the product of its children', 'Only its children', 'Only its own KT', 'The parent'], 0, 'Equal weights.'),
    ('What does rho-UCT approximate?', ['Expectimax planning', 'Solomonoff induction', 'The halting problem', 'Rewards'], 0, 'Sampled search.'),
    ('What does the tree prior prefer?', ['Small trees', 'Large trees', 'Deep trees', 'Random trees'], 0, '2^-code length.'),
    ('What is dualism in AIXI?', ['The agent is outside the environment', 'Two reward signals', 'Two policies', 'Two games'], 0, 'It cannot model its own modification.'),
    ('What does the dogmatic prior do?', ['Makes AIXI stick to a chosen policy', 'Makes AIXI explore', 'Halts the agent', 'Sets all rewards to one'], 0, 'It fears punishment for deviating.'),
    ('Who showed AIXI is not asymptotically optimal in all computable environments?', ['Orseau', 'Turing', 'Minsky', 'Sutton'], 0, '2010 and 2013.'),
    ('Which method restores asymptotic optimality?', ['Thompson sampling', 'A bigger horizon', 'More rewards', 'Longer programs'], 0, 'Leike and colleagues, 2016.'),
    ('What do Leike and Hutter conclude about balanced Pareto optimality?', ['It is subjective, depending on the prior', 'It is objective', 'It is computable', 'It is false for all agents'], 0, 'Bad universal priors.'),
]


def build():
    chapters = aix1.CHS + aix2.CHS + aix3.CHS
    for ch in chapters:
        ch["summary"] = split_long(ch["summary"])
        for b in ch["lesson"]:
            if b["type"] == "math":
                b["tex"] = stack(b["tex"])
            if b["type"] == "text":
                b["items"] = split_long(b["items"])
    html = {"__AIXI__": app("aixi.html")}
    for ch in chapters:
        for lab in ch["practice"]:
            if lab["type"] == "webxdc" and lab["html"] in html:
                lab["html"] = html[lab["html"]]
    return {
        "format": "lilith-course", "version": 1, "id": "aixi",
        "title": "AIXI",
        "subtitle": "Universal artificial intelligence: induction, planning and the limits of the ideal agent",
        "author": "Lilith Learning Lab",
        "description": "A 12-chapter course on AIXI, Marcus Hutter's mathematical definition of an ideal reinforcement learning agent. Based on Hutter's Universal Algorithmic Intelligence survey, the Monte-Carlo AIXI paper by Veness and colleagues, Legg and Hutter's universal intelligence paper, and Leike, Hutter and Orseau on computability and bad priors. Covers the agent-environment cycle, expectimax, Bayesian mixtures, Kolmogorov complexity, Solomonoff induction, the AIXI equation, horizons, optimality, incomputability and AIXItl, MC-AIXI-CTW and critiques. Python labs run on the built-in MicroPython engine. The toy programs are teaching miniatures, not code from the papers.",
        "pronounce": PRONOUNCE,
        "chapters": chapters,
        "finalExam": {"title": "Final exam: AIXI", "passMark": 70, "size": 20,
                      "questions": [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in EXAM]},
        "sandbox": SANDBOX,
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "aixi.course.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
    print("wrote", out)
