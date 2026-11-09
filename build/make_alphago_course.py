#!/usr/bin/env python3
"""Build the AlphaGo course. Usage: python3 make_alphago_course.py <out.json>"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "ago"))
import ago1, ago2, ago3  # noqa: E402
from make_trinity_course import split_long, stack  # noqa: E402


def app(name):
    with open(os.path.join(HERE, "ago", "apps", name), encoding="utf-8") as f:
        return f.read()


PRONOUNCE = {
    "AlphaGo Zero": "alpha go zero", "AlphaGo": "alpha go", "AlphaZero": "alpha zero", "MuZero": "mew zero",
    "Pachi": "pah chee", "Crazy Stone": "crazy stone", "Fuego": "fway go", "GnuGo": "new go", "Fan Hui": "fan hway",
    "Lee Sedol": "lee se dole", "Ke Jie": "kuh jee eh", "Aja Huang": "ah ja hwong", "KGS": "K G S", "Tygem": "tie gem",
    "Hassabis": "ha sah bis", "Schrittwieser": "shrit vee zer", "Szepesvari": "seh peh shvar ee", "Kocsis": "ko chish",
    "komi": "ko mee", "Komi": "Ko mee", "atari": "ah tah ree", "Baduk": "ba dook", "baduk": "ba dook", "Weiqi": "way chee",
    "Elo": "ee low", "UCB1": "U C B one", "UCT": "U C T", "UCB": "U C B", "MCTS": "M C T S", "PUCT": "P U C T",
    "softmax": "soft max", "Softmax": "Soft max", "REINFORCE": "re in force", "Kohs": "koze", "Kasparov": "kas par off",
    "Tromp": "tromp", "Wuzhen": "woo jen", "dan": "dahn", "GPUs": "G P Us", "GPU": "G P U", "CPUs": "C P Us", "CPU": "C P U",
}

SANDBOX = {
    "type": "terminal", "title": "AlphaGo lookup", "prompt": "go>",
    "intro": "A scripted lookup, not a real engine. Try: nets, search, elo, matches, help",
    "chips": ["nets", "search", "elo", "matches", "help"],
    "commands": [
        {"re": "^help$", "out": ["nets     the four learned components", "search   the selection and evaluation rules", "elo      the rating formula", "matches  the headline matches"]},
        {"re": "^nets$", "out": ["rollout policy (linear, 24.2%) | SL policy (13 layers, 57.0%) | RL policy (self-play) | value network (MSE 0.234)"]},
        {"re": "^search$", "out": ["a = argmax Q + c * P * sqrt(sum N) / (1 + N), c = 5 | V = 0.5 v + 0.5 z | play the most visited move"]},
        {"re": "^elo$", "out": ["expected score = 1 / (1 + 10^(-d/400))"]},
        {"re": "^matches$", "out": ["Oct 2015 Fan Hui 5-0", "Mar 2016 Lee Sedol 4-1", "Jan 2017 Master 60-0 online", "May 2017 Ke Jie 3-0"]},
        {"re": ".", "out": ["Unknown command. Type help."], "cls": "err"}],
    "tasks": []
}

EXAM = [
    ('Who did AlphaGo beat in October 2015?', ['Fan Hui', 'Lee Sedol', 'Ke Jie', 'Kasparov'], 0, '5-0.'),
    ('In which journal was the AlphaGo paper published?', ['Nature', 'Science', 'Cell', 'PNAS'], 0, '28 January 2016.'),
    ('What does the policy network reduce?', ['Breadth of the search', 'Depth of the search', 'The board size', 'The komi'], 0, 'It proposes likely moves.'),
    ('What does the value network reduce?', ['Depth of the search', 'Breadth of the search', 'The rules', 'Memory'], 0, 'It judges positions directly.'),
    ('What is a liberty?', ['An empty point next to a group', 'A captured stone', 'A pass', 'A scoring unit'], 0, 'Groups live by their liberties.'),
    ('When is a group captured?', ['When it has no liberties', 'When it has one stone', 'When the opponent passes', 'At move 100'], 0, 'Zero liberties.'),
    ('Why does White get komi?', ['Black moves first', 'White is weaker', 'To end ties in chess', 'It is a penalty'], 0, 'Compensation.'),
    ('About what branching factor does Go have?', ['250', '35', '10', '2'], 0, 'Chess is about 35.'),
    ('What do rollouts estimate?', ['The value of a position', 'The rules', 'The komi', 'The rating'], 0, 'By the win rate of sampled games.'),
    ('What does the UCB bonus do as a move is tried more?', ['It shrinks', 'It grows', 'It stays fixed', 'It flips sign'], 0, 'The count is in the denominator.'),
    ('How many input planes does the policy network use?', ['48', '3', '361', '8'], 0, 'Each is 19 by 19.'),
    ('What does softmax guarantee?', ['Positive numbers that sum to 1', 'A single winner', 'Integers', 'Legal moves only'], 0, 'Probabilities.'),
    ('What data trained the SL policy network?', ['Positions from the KGS Go Server', 'Self-play', 'Chess games', 'Random boards'], 0, '30 million positions.'),
    ('What accuracy did the SL network reach?', ['57.0 percent', '24.2 percent', '99 percent', '10 percent'], 0, 'With all input features.'),
    ('What is the gradient of -log p_a with respect to the logits?', ['p minus a one-hot vector', 'p times 2', 'Zero', 'The board'], 0, 'It pushes the right move up.'),
    ('Why does AlphaGo have a separate rollout policy?', ['The deep network is too slow for rollouts', 'It is more accurate', 'The rules differ', 'It is simpler to code'], 0, 'Speed: about 2 microseconds a move.'),
    ('What accuracy does the rollout policy have?', ['24.2 percent', '57.0 percent', '85 percent', '5 percent'], 0, 'Weaker but about 1,500 times faster.'),
    ('How is the RL policy network initialized?', ['From the SL network', 'At random', 'From the value network', 'From the rules'], 0, 'rho = sigma.'),
    ('What does a won game do to its moves in policy gradient?', ['Makes them more probable', 'Makes them less probable', 'Nothing', 'Removes them'], 0, 'z = +1.'),
    ('Why play against older versions?', ['It stabilizes training', 'It is faster', 'To save memory', 'To copy humans'], 0, 'Prevents overfitting to the current policy.'),
    ('How did the RL network do against Pachi with no search?', ['Won 85 percent', 'Lost most games', 'Won 11 percent', 'Tied'], 0, 'Against 11 percent for SL.'),
    ('What does the value network output?', ['The expected game outcome', 'A move', 'The komi', 'The number of liberties'], 0, 'A number between -1 and 1.'),
    ('Why did training the value network on KGS games overfit?', ['Positions in a game are correlated', 'Games were short', 'Go has no rules', 'The network was small'], 0, 'The network memorized outcomes.'),
    ('How were the 30 million value positions chosen?', ['One position from each separate self-play game', 'All positions from few games', 'The first move only', 'Random boards'], 0, 'This breaks correlation.'),
    ('In the search, what does u favour?', ['High prior and few visits', 'Low prior and many visits', 'Illegal moves', 'The last move'], 0, 'P over 1 plus N.'),
    ('What is c_puct in the paper?', ['5', '0.5', '40', '3'], 0, 'u = c * P * sqrt(sum N) / (1 + N).'),
    ('What is lambda in the leaf evaluation?', ['The rollout weight, 0.5', 'The komi', 'The learning rate', 'The thread count'], 0, 'V = (1 - lambda) v + lambda z.'),
    ('Which move does AlphaGo play at the root?', ['The most visited', 'The highest prior', 'A random one', 'The last explored'], 0, 'Visits are robust.'),
    ('What is virtual loss for?', ['To spread parallel threads over different paths', 'To lose games on purpose', 'To resign', 'To raise Q'], 0, 'A temporary penalty.'),
    ('What does a 400 Elo advantage give?', ['About 91 percent expected score', 'A guaranteed win', 'A draw', '50 percent'], 0, 'E = 1 / (1 + 10^-1).'),
    ('How many of 495 games did single-machine AlphaGo win against other programs?', ['494', '250', '1', '495'], 0, '99.8 percent.'),
    ('Who won game four of the Lee Sedol match?', ['Lee Sedol', 'AlphaGo', 'Nobody', 'Fan Hui'], 0, 'By resignation at move 180.'),
    ('What was the final score of the Lee Sedol match?', ['4-1 for AlphaGo', '5-0 for AlphaGo', '3-2 for Lee', '1-4 for AlphaGo'], 0, 'March 2016.'),
    ('What komi was used in the Lee match?', ['7.5', '6.5', '0', '5.5'], 0, 'Chinese rules.'),
    ('What did AlphaGo Zero remove?', ['Human game data', 'The search', 'The rules', 'The networks'], 0, 'It learned from self-play alone.'),
    ('What did Master win online?', ['60 games without a loss', '10 games', 'All but one', 'None'], 0, 'Late 2016 to early 2017.'),
    ('Why is the value flipped in the backup step?', ['Players alternate', 'Values are negative', 'To save memory', 'It is optional'], 0, 'A good result for the child is bad for the parent.'),
    ('Did DeepMind release the AlphaGo code?', ['No', 'Yes', 'Only the networks', 'Only for chess'], 0, 'The labs here are miniatures.'),
]


def build():
    chapters = ago1.CHS + ago2.CHS + ago3.CHS
    for ch in chapters:
        ch["summary"] = split_long(ch["summary"])
        for b in ch["lesson"]:
            if b["type"] == "math":
                b["tex"] = stack(b["tex"])
            if b["type"] == "text":
                b["items"] = split_long(b["items"])
    html = {"__GO__": app("go.html")}
    for ch in chapters:
        for lab in ch["practice"]:
            if lab["type"] == "webxdc" and lab["html"] in html:
                lab["html"] = html[lab["html"]]
    return {
        "format": "lilith-course", "version": 1, "id": "alphago",
        "title": "AlphaGo",
        "subtitle": "Deep neural networks and tree search for the game of Go",
        "author": "Lilith Learning Lab",
        "description": "A 12-chapter course on AlphaGo, the DeepMind program that beat a professional Go player and then Lee Sedol. Based on the 2016 Nature paper by Silver, Huang and colleagues and public accounts of the Fan Hui and Lee Sedol matches. Covers the rules of Go, Monte Carlo tree search before AlphaGo, the 48-plane input and the policy network, supervised learning from expert games, the fast rollout policy, policy-gradient self-play, the value network, the search with PUCT and mixed evaluation, hardware and Elo, a tic-tac-toe miniature, and the matches, successors and criticism. Python labs run on the built-in MicroPython engine. DeepMind did not release the code; the labs are teaching miniatures.",
        "pronounce": PRONOUNCE,
        "chapters": chapters,
        "finalExam": {"title": "Final exam: AlphaGo", "passMark": 70, "size": 20,
                      "questions": [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in EXAM]},
        "sandbox": SANDBOX,
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "alphago.course.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
    print("wrote", out)
