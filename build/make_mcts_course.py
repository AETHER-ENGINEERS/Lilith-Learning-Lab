#!/usr/bin/env python3
"""Build the MCTS course. Usage: python3 make_mcts_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mct"))
import cmk, mct  # noqa: E402

PRONOUNCE = {
    "MCTS": "M C T S", "UCT": "U C T", "UCB1": "U C B one", "UCB": "U C B", "PUCT": "P U C T", "RAVE": "rave", "AMAF": "A M A F",
    "Coulom": "koo lom", "Remi": "ray mee", "Kocsis": "ko chish", "Szepesvari": "seh peh shvar ee", "Cesa-Bianchi": "chay zah bee ang kee",
    "Abramson": "ab ram son", "Gelly": "zhay lee", "MuZero": "mew zero", "AlphaGo": "alpha go", "AlphaZero": "alpha zero",
    "LCG": "L C G", "SE": "S E", "Nim": "nim", "ply": "ply", "plies": "plies", "negamax": "nega max", "Negamax": "Nega max",
    "minimax": "mini max", "Minimax": "Mini max", "alpha-beta": "alpha beta", "Alpha-beta": "Alpha beta", "argmax": "arg max",
    "lcg": "L C G", "playout": "play out", "playouts": "play outs", "Playout": "Play out", "Playouts": "Play outs",
}

SANDBOX = cmk.terminal("MCTS lookup", "mc>", "A scripted lookup, not a real search. Try: steps, uct, final, nim", [
    ("steps", ["1 selection: descend by the tree policy", "2 expansion: add a child", "3 simulation: play to the end", "4 backpropagation: update N and W up the path"]),
    ("uct", ["UCT child score = W/N + C sqrt(ln N_parent / N_child)", "UCB1 (Auer et al. 2002): mean + c sqrt(2 ln N / n_i)"]),
    ("final", ["robust child = most visits (usual choice)", "max child = highest mean", "secure child = best lower confidence bound"]),
    ("nim", ["take 1 to 3 stones, last stone wins", "piles that are multiples of 4 are lost for the player to move"]),
    ("puct", ["Q + c P sqrt(sum N) / (1 + N): the AlphaGo selection rule"]),
])

EXAM = [
 ("What does MCTS do?", ["Grows a search tree guided by random simulations", "Trains a classifier", "Sorts moves", "Compresses boards"], 0, "Selection, expansion, simulation, backpropagation."),
 ("Who gave Monte Carlo tree search its name?", ["Remi Coulom", "Auer", "Silver", "Browne"], 0, "2006."),
 ("Who proposed UCT?", ["Kocsis and Szepesvari", "Coulom", "Auer et al.", "Hassabis"], 0, "Also 2006."),
 ("Which survey is the standard overview?", ["Browne et al., 2012", "Silver et al., 2016", "Vaswani et al., 2017", "Schulman et al., 2017"], 0, "A Survey of Monte Carlo Tree Search Methods."),
 ("What does anytime mean?", ["It can stop at any moment with a best answer", "It runs forever", "It uses no memory", "It needs a clock"], 0, "More time gives better play."),
 ("What are the four MCTS steps?", ["Selection, expansion, simulation, backpropagation", "Train, test, deploy, monitor", "Encode, decode, sample, score", "Read, write, copy, delete"], 0, "In that order."),
 ("What does minimax compute?", ["Exact values by working back from the leaves", "Random averages", "Visit counts", "Move priors"], 0, "Needs the whole tree."),
 ("Why is exact search hopeless in Go?", ["The tree is astronomically large", "The rules are secret", "Moves are random", "Boards are tiny"], 0, "Branching about 250, depth about 150."),
 ("In Nim (take 1 to 3), which piles are lost for the player to move?", ["Multiples of 4", "Odd piles", "Multiples of 3", "Piles above 10"], 0, "Including zero."),
 ("What is a playout?", ["A simulated game to the end", "A tree node", "A final move", "A scoring rule"], 0, "Usually random moves."),
 ("How does the error of a Monte Carlo average shrink?", ["Like one over the square root of n", "Like one over n squared", "Linearly", "It does not"], 0, "Ten times more samples, about three times more accurate."),
 ("Why use a seeded generator in tests?", ["Repeatable results", "Better randomness", "A smaller tree", "Faster playouts"], 0, "Same seed, same run."),
 ("Can random-play win rate differ from perfect-play value?", ["Yes", "Never", "Only in Nim", "Only for draws"], 0, "Random opponents blunder."),
 ("What does UCB1 add to the mean?", ["A confidence bonus larger for rarely tried arms", "Random noise", "The depth", "The prior"], 0, "Optimism under uncertainty."),
 ("What does regret measure?", ["Reward lost against always playing the best arm", "Time used", "Memory used", "Arm count"], 0, "UCB1 has logarithmic regret."),
 ("What is exploration?", ["Trying arms to learn about them", "Using the best arm", "Stopping", "Counting"], 0, "Versus exploitation."),
 ("How many nodes does expansion add per iteration?", ["One", "All children", "None", "The whole tree"], 0, "In plain MCTS."),
 ("What does a node store?", ["Visit count N and total reward W", "The rules", "The board image", "The learning rate"], 0, "Mean = W/N."),
 ("Why does the reward flip during backpropagation?", ["Players alternate", "To save memory", "Rewards are negative", "To break ties"], 0, "A win for one is a loss for the other."),
 ("What does UCT choose inside the tree?", ["The child with the highest mean plus bonus", "A random child", "The first child", "The deepest child"], 0, "UCB1 at each node."),
 ("What does a larger exploration constant C do?", ["Explores more", "Explores less", "Nothing", "Shrinks the tree"], 0, "Larger bonus."),
 ("What did Kocsis and Szepesvari prove?", ["UCT converges to the minimax value for finite games", "UCT is always fast", "UCT needs no memory", "UCT never loses"], 0, "Asymptotically."),
 ("Which final move is the usual choice?", ["The most visited child", "The least visited", "A random child", "The shallowest"], 0, "The robust child."),
 ("Why distrust a high mean with very few visits?", ["It may be a lucky sample", "It is illegal", "It is too deep", "It is slow"], 0, "Few samples."),
 ("What is a secure child?", ["One maximising a lower confidence bound", "The most visited", "The first", "The highest prior"], 0, "Mean minus a margin."),
 ("What does AMAF credit?", ["Moves played later in the playout", "Only the first move", "Illegal moves", "The terminal state"], 0, "As if they had been played first."),
 ("What does RAVE blend?", ["AMAF and ordinary tree statistics", "Two trees", "Two players", "Two seeds"], 0, "Trusting AMAF early."),
 ("What does first-play urgency do?", ["Gives unvisited children a finite score", "Visits the root twice", "Removes leaves", "Doubles C"], 0, "Instead of infinity."),
 ("What does progressive widening do?", ["Allows more children as visits grow", "Prunes children", "Adds noise", "Halves C"], 0, "ceil(k visits^alpha)."),
 ("What is virtual loss for?", ["Steering parallel threads to different branches", "Lowering winners", "Saving memory", "Ending the search"], 0, "A temporary penalty."),
 ("How is a draw scored in the tree?", ["One half", "Zero", "One", "Minus one"], 0, "Between win and loss."),
 ("When does MCTS shine compared with alpha-beta?", ["Large branching and no good evaluation function", "Tiny trees", "Solved games", "One-move games"], 0, "Like Go."),
 ("What is a trap state?", ["One precise reply refutes an attractive move", "A repeated position", "A draw", "A pass"], 0, "Sampling can miss it."),
 ("What does PUCT add to UCT?", ["A policy prior", "A random move", "A bigger tree", "A timer"], 0, "Used by AlphaGo."),
 ("What replaced random playouts in AlphaGo?", ["A value network", "A bigger tree only", "A lookup table", "A human"], 0, "Alongside a policy network."),
 ("What does MCTS require?", ["A model of the environment", "A labelled dataset", "A GPU", "A human opponent"], 0, "Rules or a learned model as in MuZero."),
]

CFG = dict(id="mcts", title="Monte Carlo Tree Search", subtitle="Playouts, bandits, UCT and enhancements, with Python labs on Nim",
    description="Monte Carlo tree search from first principles (Coulom 2006; Kocsis and Szepesvari 2006; Browne et al. 2012): game trees and minimax, random playouts, multi-armed bandits and UCB1, the four steps, a complete UCT search on Nim, choosing the final move, RAVE and other enhancements, two-player perspective, and the road to AlphaGo's PUCT. Theory plus Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="mct", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "mcts.course.json")
    cmk.main(CFG, mct.CHS, [sys.argv[0], out])
