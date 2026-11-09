#!/usr/bin/env python3
"""Build the AlphaZero course. Usage: python3 make_alphazero_course.py <out.json>"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "az"))
import azc1, azc2, azc3  # noqa: E402
from make_trinity_course import split_long, stack  # noqa: E402


def app(name):
    with open(os.path.join(HERE, "az", "apps", name), encoding="utf-8") as f:
        return f.read()


PRONOUNCE = {
    "AlphaGo Zero": "alpha go zero", "AlphaZero": "alpha zero", "AlphaGo": "alpha go", "MuZero": "mew zero", "KataGo": "kata go",
    "Leela Chess Zero": "lee la chess zero", "Leela Zero": "lee la zero", "Leela": "lee la", "Lc0": "L C zero",
    "Stockfish": "stock fish", "Elmo": "el mo", "Elo": "ee low", "shogi": "show gee", "joseki": "joe seh kee",
    "PUCT": "P U C T", "MCTS": "M C T S", "UCB1": "U C B one", "UCT": "U C T", "TPUs": "T P Us", "TPU": "T P U",
    "Dirichlet": "dee rish lay", "Tromp-Taylor": "tromp taylor", "Syzygy": "siz ih jee", "NNUE": "N N U E",
    "tabula rasa": "tabula rah sa", "Szepesvári": "seh peh shvar ee", "Kocsis": "ko chish", "Schrittwieser": "shrit vee zer",
    "Hassabis": "ha sah bis", "negamax": "nega max", "Negamax": "Nega max", "softmax": "soft max", "Softmax": "Soft max",
    "TCEC": "T C E C", "Gumbel": "gum bel", "Pascutto": "pas coo toe", "Kaufman": "kaw man", "Fan Hui": "fan hway",
    "Lee Sedol": "lee se dole",
}

SANDBOX = {
    "type": "terminal", "title": "AlphaZero lookup", "prompt": "az>",
    "intro": "A scripted lookup, not a real engine. Try: loop, puct, loss, results, help",
    "chips": ["loop", "puct", "loss", "results", "help"],
    "commands": [
        {"re": "^help$", "out": ["loop     the self-play and training loop", "puct     the selection rule", "loss     the training loss", "results  the headline matches"]},
        {"re": "^loop$", "out": ["search with the network -> play a game against itself -> store (state, pi, z) -> train the network -> repeat"]},
        {"re": "^puct$", "out": ["choose the move maximizing Q + c * P * sqrt(sum N) / (1 + N)"]},
        {"re": "^loss$", "out": ["l = (z - v)^2 - pi . log p + c * ||theta||^2"]},
        {"re": "^results$", "out": ["2017 chess vs Stockfish 8: +28 =72 -0 (100 games)", "2018 chess vs Stockfish 9 dev: +155 =839 -6 (1000 games)"]},
        {"re": ".", "out": ["Unknown command. Type help."], "cls": "err"}],
    "tasks": []
}

EXAM = [
    ('What does AlphaZero need to know about a game?', ['Opening books', 'Only the rules', 'Human games', 'A handwritten evaluation'], 1, 'It starts tabula rasa.'),
    ('What does the network f(s) output?', ['A move only', 'Move probabilities and a value', 'A board image', 'A win count'], 1, '(p, v) = f_theta(s).'),
    ('In which journal was the final AlphaZero paper published?', ['Nature', 'Science', 'Cell', 'PNAS'], 1, 'Science, 7 December 2018.'),
    ('What did AlphaGo Zero remove compared with AlphaGo Lee?', ['The neural network', 'Human game data', 'Search', 'Self-play'], 1, 'It learned from self-play alone.'),
    ('Which games were in the first AlphaZero paper?', ['Chess, shogi and Go', 'Chess only', 'Go only', 'Chess and checkers'], 0, 'Three games, one algorithm.'),
    ('What does negamax return for a lost position?', ['+1', '0', '-1', 'Undefined'], 2, 'The mover has lost.'),
    ('What does alpha-beta pruning change?', ['The minimax value', 'The number of nodes examined', 'The rules', 'The evaluation'], 1, 'Same value, fewer nodes.'),
    ('What did classical engines use at the depth limit?', ['A neural network', 'A handwritten evaluation', 'Random play', 'A rollout'], 1, 'Expert-designed features.'),
    ('What are the four phases of an MCTS simulation?', ['Selection, expansion, evaluation, backup', 'Read, write, run, halt', 'Train, test, deploy, repeat', 'Shuffle, deal, bid, play'], 0, 'Walk down, add, evaluate, update.'),
    ('Why does UCB1 have an exploration bonus?', ['To favour rarely tried moves', 'To make search slower', 'To remove randomness', 'To count wins'], 0, 'It balances exploration and exploitation.'),
    ('What replaces the random rollout in AlphaZero?', ['A lookup table', "The network's value estimate", 'Alpha-beta', 'Nothing'], 1, 'The leaf is evaluated by f.'),
    ('How many move planes does chess use in the output?', ['64', '73', '119', '8'], 1, '8 x 8 x 73 = 4,672 slots.'),
    ('What does a softmax produce?', ['Sorted scores', 'Probabilities that sum to 1', 'A single move', 'Zeros'], 1, 'Positive numbers summing to one.'),
    ('What happens to illegal moves in the policy?', ['They are masked to zero and the rest renormalized', 'They are kept', 'They get negative probability', 'They are repeated'], 0, 'A legal-move mask.'),
    ('Which statistics does each tree edge store?', ['N, W, Q and P', 'Only N', 'Only P', 'The board'], 0, 'Visits, total value, mean value, prior.'),
    ('In PUCT, what happens to the bonus U as an edge is visited more?', ['It grows', 'It shrinks', 'It is constant', 'It becomes the value'], 1, 'N is in the denominator.'),
    ('Why is the value negated going up the tree?', ['The players alternate', 'Values are negative', 'To save memory', 'It is a bug'], 0, "Each edge is scored from its mover's view."),
    ('What is Dirichlet noise added to?', ['The weights', 'The root priors', 'The board', 'The reward'], 1, 'To force exploration.'),
    ('Which game used the smallest Dirichlet alpha?', ['Chess', 'Shogi', 'Go', 'All equal'], 2, 'Go has the most legal moves (0.03).'),
    ('What does temperature near zero do?', ['Samples uniformly', 'Plays the most-visited move', 'Passes', 'Resigns'], 1, 'N^(1/tau) concentrates on the maximum.'),
    ('What is z for a drawn game?', ['+1', '-1', '0', 'Undefined'], 2, 'Draws score zero.'),
    ('What is the policy training target?', ['The move played', 'The search visit distribution', 'A random vector', 'The value'], 1, 'Cross-entropy with pi.'),
    ('What does the value head learn to predict?', ['The game outcome z', 'The next move', 'The weights', 'The search time'], 0, 'Squared error against z.'),
    ('Which term in the loss limits weight size?', ['(z - v)^2', 'pi . log p', 'c ||theta||^2', 'None'], 2, 'L2 regularization.'),
    ('How was the learning rate changed in training?', ['It rose steadily', 'It was lowered in stages from 0.2', 'It stayed constant', 'It was random'], 1, '0.2, 0.02, 0.002, 0.0002.'),
    ('What did AlphaGo Zero use that AlphaZero dropped?', ['A neural network', 'Gating of new networks at a 55 percent margin', 'Self-play', 'Search'], 1, 'AlphaZero updates one network continually.'),
    ('What does AlphaZero optimize?', ['Win probability only', 'The expected outcome including draws', 'Game length', 'Captures'], 1, 'That suits chess.'),
    ('Why no symmetry augmentation for chess?', ['The rules are asymmetric', 'It is too slow', 'Boards are small', 'It was forgotten'], 0, 'Rotating a chess board changes the game.'),
    ('What was the 2017 chess match result against Stockfish 8?', ['+28 =72 -0', '+155 =839 -6', '+0 =0 -100', '+50 =0 -50'], 0, '100 games, one minute per move.'),
    ('What was the 2018 chess match result?', ['+28 =72 -0', '+155 =839 -6', '+60 =40 -0', '+6 =839 -155'], 1, '1000 games, 3 hours plus 15 s.'),
    ('Which was a criticism of the first match?', ['Stockfish had little hash memory and no opening book', 'Too few games', 'AlphaZero used a book', 'Stockfish ran on TPUs'], 0, 'Settings limited Stockfish.'),
    ('About how many positions per second did AlphaZero search in chess?', ['80 thousand', '70 million', '1 billion', '100'], 0, 'Stockfish searched about 70 million.'),
    ('What does MuZero remove?', ['The network', 'The need to be given the rules', 'Self-play', 'Search'], 1, 'It learns a model of the environment.'),
    ('Which program reproduced AlphaZero for chess?', ['Leela Chess Zero', 'Deep Blue', 'Elmo', 'Stockfish 8'], 0, 'A volunteer-trained project.'),
    ('Which is an assumption of AlphaZero?', ['Hidden information', 'A fast exact simulator of the rules', 'One player', 'No search'], 1, 'Search needs the simulator.'),
    ('In the tiny tic-tac-toe search, what is the value of a non-terminal leaf?', ['+1', '-1', '0', 'The prior'], 2, 'The stub network has no opinion.'),
]




def build():
    chapters = azc1.CHS + azc2.CHS + azc3.CHS
    for ch in chapters:
        ch["summary"] = split_long(ch["summary"])
        for b in ch["lesson"]:
            if b["type"] == "math":
                b["tex"] = stack(b["tex"])
            if b["type"] == "text":
                b["items"] = split_long(b["items"])
    html = {"__PUCT__": app("puct.html")}
    for ch in chapters:
        for lab in ch["practice"]:
            if lab["type"] == "webxdc" and lab["html"] in html:
                lab["html"] = html[lab["html"]]
    return {
        "format": "lilith-course", "version": 1, "id": "alphazero",
        "title": "AlphaZero",
        "subtitle": "Self-play, tree search and learning without human knowledge",
        "author": "Lilith Learning Lab",
        "description": "A 12-chapter course on AlphaZero, the DeepMind algorithm that learns chess, shogi and Go from self-play with only the rules. Based on the AlphaZero preprint and Science paper by Silver and colleagues, the AlphaGo Zero Nature paper and reports on the matches and the debate that followed. Covers game search, Monte Carlo tree search, the policy and value network, PUCT, exploration noise and temperature, self-play data, the loss and training, differences from AlphaGo Zero, results and criticism, a working tic-tac-toe search and successors such as MuZero. Python labs run on the built-in MicroPython engine. The original program was never released; the capstone is a teaching miniature.",
        "pronounce": PRONOUNCE,
        "chapters": chapters,
        "finalExam": {"title": "Final exam: AlphaZero", "passMark": 70, "size": 20,
                      "questions": [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in EXAM]},
        "sandbox": SANDBOX,
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "alphazero.course.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
    print("wrote", out)
