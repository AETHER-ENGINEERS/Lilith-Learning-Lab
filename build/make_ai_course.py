#!/usr/bin/env python3
"""Build the Artificial Intelligence course. Usage: python3 make_ai_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "aimac"))
import cmk, ai1, ai2, ai3  # noqa: E402

PRONOUNCE = {
    "AI": "A I", "AIMA": "A I M A", "A*": "A star", "CSP": "C S P", "MDP": "M D P", "POMDP": "pom D P", "HMM": "H M M", "BFS": "B F S",
    "MRV": "M R V", "SAT": "sat", "PDDL": "P D D L", "HTN": "H T N", "CPT": "C P T", "ReLU": "relu", "IoU": "I o U", "PID": "P I D",
    "SLAM": "slam", "KB": "K B", "FOL": "F O L", "MCTS": "M C T S", "TD": "T D", "Wumpus": "wum pus", "Russell": "russell", "Norvig": "nor vig",
    "Vickrey": "vick ree", "Skolem": "sko lem", "Kalman": "kal man", "Bayes": "bays", "Bayesian": "bay zhun", "Markov": "mar kov",
    "Viterbi": "vi ter bee", "Nash": "nash", "softmax": "soft max", "epsilon": "ep si lon", "gamma": "gam uh",
}

SANDBOX = cmk.terminal("AI cheat sheet", "ai>", "A scripted lookup, not a real solver. Try: astar, bayes, bellman, nash, qlearn", [
    ("astar", ["f(n) = g(n) + h(n)", "optimal if h never overestimates the true cost"]),
    ("bayes", ["P(h | e) = P(e | h) P(h) / P(e)", "mind the base rate"]),
    ("bellman", ["U(s) = R(s) + gamma max_a sum P(s' | s, a) U(s')", "value iteration applies it repeatedly"]),
    ("nash", ["no player gains by changing strategy alone", "prisoner's dilemma: both defect"]),
    ("qlearn", ["Q(s,a) += alpha (r + gamma max Q(s',a') - Q(s,a))", "epsilon-greedy explores"]),
    ("entropy", ["H = - sum p log2 p", "information gain = entropy before minus after a split"]),
])

EXAM = [
 ("What is a rational agent?", ["One that maximises expected performance", "One that is always right", "One that copies humans", "One that never learns"], 0, "Rationality is about expected outcomes."),
 ("What does PEAS describe?", ["A task environment", "A search tree", "A neural net", "A proof"], 0, "Performance, Environment, Actuators, Sensors."),
 ("Which agent compares outcomes by a numeric score?", ["Utility-based", "Simple reflex", "Table lookup", "Random"], 0, "Utility ranks outcomes."),
 ("Which uninformed search finds the fewest steps?", ["Breadth-first", "Depth-first", "Hill climbing", "Random"], 0, "It expands level by level."),
 ("What does A* use to order the frontier?", ["g(n) + h(n)", "h(n) only", "Depth only", "Random"], 0, "Cost so far plus estimate."),
 ("What makes a heuristic admissible?", ["It never overestimates", "It is exact", "It is large", "It is random"], 0, "Needed for optimality."),
 ("What can trap hill climbing?", ["A local maximum", "A global maximum", "A heuristic", "A queue"], 0, "No better neighbour."),
 ("What does minimax assume?", ["An optimal opponent", "A random opponent", "No opponent", "A weak opponent"], 0, "Worst-case planning."),
 ("What does alpha-beta pruning change?", ["Speed, not the result", "The result", "The rules", "The evaluation"], 0, "Same value, fewer nodes."),
 ("What does a CSP consist of?", ["Variables, domains, constraints", "States and actions", "Rewards", "Layers"], 0, "That is the definition."),
 ("What does MRV choose?", ["The variable with fewest legal values", "A random variable", "The largest domain", "The last variable"], 0, "Fail early."),
 ("What is a model in propositional logic?", ["A truth assignment to all symbols", "A neural net", "A plan", "A policy"], 0, "True or false for each symbol."),
 ("When does KB entail a?", ["a holds in every model of KB", "a is in KB", "a is false", "KB is empty"], 0, "The definition of entailment."),
 ("What does unification produce?", ["A substitution making terms identical", "A probability", "A plan", "A heuristic"], 0, "Variable bindings."),
 ("Which connective goes with for-all?", ["Implies", "And", "Or", "Not"], 0, "For all x, P implies Q."),
 ("What does an action's precondition state?", ["Facts needed to apply it", "Facts it adds", "Its cost", "Its name"], 0, "They must be in the state."),
 ("What does the delete relaxation ignore?", ["Delete effects", "Preconditions", "The goal", "The start"], 0, "Actions only add facts."),
 ("What does Bayes' rule compute?", ["P(h | e) from P(e | h)", "P(e) only", "A search path", "A reward"], 0, "It reverses conditioning."),
 ("Why can a positive test for a rare disease be misleading?", ["The base rate is low", "Tests never work", "Probability fails", "The disease is invisible"], 0, "Few ill, many healthy."),
 ("What does naive Bayes assume?", ["Features independent given the class", "All classes equal", "No priors", "No features"], 0, "Conditional independence."),
 ("How does a Bayes net define the joint?", ["Product of each node given its parents", "Sum of nodes", "Max of nodes", "Average"], 0, "Chain rule."),
 ("What is explaining away?", ["Evidence for one cause lowers another", "Removing a node", "Ignoring evidence", "Cancelling causes"], 0, "Competing explanations."),
 ("What does the Markov assumption say?", ["The present depends on a bounded past", "The future is random", "All history matters", "Nothing changes"], 0, "Keeps models small."),
 ("What are the filtering steps?", ["Predict, weight by evidence, normalise", "Sample, sort", "Search, prune", "Train, test"], 0, "Recursive update."),
 ("What should a rational agent maximise?", ["Expected utility", "Best outcome", "Expected money", "Probability"], 0, "Principle of maximum expected utility."),
 ("What is the solution of an MDP?", ["A policy", "A single plan", "A heuristic", "A proof"], 0, "An action for each state."),
 ("What is a Nash equilibrium?", ["No player gains by deviating alone", "The best joint outcome", "A random play", "A dominant strategy for all"], 0, "Mutual best replies."),
 ("What should you bid in a Vickrey auction?", ["Your true value", "Half", "Double", "Zero"], 0, "A dominant strategy."),
 ("What is overfitting?", ["Fitting noise so new data are predicted poorly", "Low learning rate", "A perfect model", "Too little training"], 0, "Training error low, test error high."),
 ("What does entropy measure?", ["Uncertainty", "Speed", "Accuracy", "Size"], 0, "Zero when certain."),
 ("What does gradient descent do?", ["Moves weights against the gradient", "Sorts data", "Adds noise", "Counts features"], 0, "Small steps downhill."),
 ("Why do networks need nonlinear activations?", ["Layers would collapse to one linear map", "To save memory", "To remove bias", "To load data"], 0, "Linear composes to linear."),
 ("What does the Q-learning update move Q toward?", ["Reward plus discounted best next Q", "Zero", "The policy", "The loss"], 0, "The TD target."),
 ("What is epsilon-greedy?", ["Random action with small probability", "Always greedy", "Always random", "A loss"], 0, "Explore and exploit."),
 ("What does a language model estimate?", ["Probability of word sequences", "Depth", "Torque", "Utility"], 0, "It predicts text."),
 ("How do two cameras give depth?", ["Disparity between images", "Counting edges", "Colour", "Blur"], 0, "Depth = f B / d."),
 ("Why would a safe AI be uncertain about its objective?", ["To stay open to correction", "To run faster", "To avoid learning", "To use less data"], 0, "It then defers to humans."),
]

CFG = dict(id="artificial-intelligence", title="Artificial Intelligence: A Modern Approach, Condensed", subtitle="Agents, search, logic, probability, learning and more, with Python labs",
    description="A condensed course based on the structure of Russell and Norvig's Artificial Intelligence: A Modern Approach (4th edition), written in original words: rational agents, search and games, constraint satisfaction, logic and planning, probability and Bayesian networks, temporal models, decisions and MDPs, game theory, machine learning, neural networks and reinforcement learning, and applications and ethics. Theory plus Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="aimac", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "artificial-intelligence.course.json")
    cmk.main(CFG, ai1.A + ai2.B + ai3.C, [sys.argv[0], out])
