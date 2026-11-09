"""AIXI course, chapters 1-4."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

# ------------------------------------------------------------ 1
CHS.append(CH(
 "What is AIXI?",
 ("The big picture", [
  "AIXI | combines | Solomonoff induction",
  "AIXI | combines | Sequential decision theory",
  "AIXI | is | A reinforcement learning agent",
  "AIXI | assumes | A computable environment",
  "AIXI | weighs | Programs by length",
  "AIXI | is | Incomputable",
  "AIXI | proposed by | Marcus Hutter"]),
 ["AIXI is a mathematical definition of an ideal reinforcement learning agent, proposed by Marcus Hutter in 2000. It is not a program you can run. It answers a thought experiment: how would you act if you had unlimited computing power and no knowledge of your world?",
  "It joins two ideas. Solomonoff induction predicts what comes next by weighing every computable explanation of the past, simple ones more heavily. Expectimax planning then picks the action with the highest expected total reward under those predictions.",
  "The course builds both halves in small Python programs, then the real approximations and the serious criticisms."],
 [("AIXI", "Hutter's universal reinforcement learning agent: Solomonoff prediction plus expectimax planning. Pronounced eye-ksee."),
  ("Agent", "Whatever chooses actions: it reads percepts and writes actions."),
  ("Environment", "Everything outside the agent; it answers each action with a percept."),
  ("Percept", "What the agent receives each step: an observation and a reward."),
  ("Solomonoff induction", "Prediction that mixes all computable hypotheses, weighted by 2 to the minus program length."),
  ("Expectimax", "Planning that maximizes over your actions and averages over the environment's replies."),
  ("Incomputable", "Cannot be computed by any program, even given unlimited time.")],
 ["AIXI was proposed by Marcus Hutter in 2000; the main results are in his 2005 book Universal Artificial Intelligence.",
  "It acts in an unknown but computable environment and tries to maximize total reward.",
  "Prediction comes from a Solomonoff-style mixture; action comes from expectimax.",
  "There are no free parameters except the choice of universal Turing machine and the horizon.",
  "AIXI is incomputable, so it is a gold standard to approximate, not a program to run.",
  "It does not model itself as part of the world: that is its biggest conceptual limit."],
 [T("Intelligence is hard to define, and harder to define for machines unlike us. Marcus Hutter's answer, published first in 2000 and developed in his 2005 book, takes the problem from the top down: instead of building a clever system and hoping it is general, define the best possible agent mathematically, then ask how closely it can be approximated."),
  T("The setting is the general reinforcement learning problem. An agent and an environment talk in cycles. Each cycle the agent sends an action, and the environment replies with a percept made of an observation and a reward. The agent wants as much total reward as it can get, and it knows nothing about the environment except that some computer program could produce its replies."),
  T("AIXI has two halves. The first half is learning. Following Ray Solomonoff's 1964 theory of induction, it keeps every computable explanation of its experience, and trusts each in proportion to two to the power of minus the length of the shortest program that states it. Short explanations count for much more, a formal version of Occam's razor."),
  T("The second half is acting. Given its beliefs, AIXI looks ahead over all its possible action sequences and the environment's possible replies, and takes the action whose average future reward is highest. This look-ahead is called expectimax, because it takes a maximum over the agent's choices and an expectation over the environment's chance."),
  M(r"\text{AIXI} \;=\; \text{Solomonoff prediction} \;+\; \text{expectimax planning}"),
  T("What do we get? Hutter's analysis argues that the result is optimal in several senses, which chapter 9 lists, and chapter 12 shows how later work weakened several of those claims. The agent also has a price: it must consider all programs, including ones that never halt, so it cannot be computed."),
  T("Do not read AIXI as a design to build. Read it as a yardstick, like the ideal gas or the frictionless plane. It tells you what perfect general learning would be, which parts of that are hopeless for finite machines, and which approximations keep something of the spirit. The Monte Carlo AIXI work of Veness and colleagues, chapter 11, is the best known attempt."),
  T("A note on sources. This course follows Hutter's 2007 survey Universal Algorithmic Intelligence, the Veness and colleagues 2011 paper in the Journal of Artificial Intelligence Research, Legg and Hutter's universal intelligence paper, and papers by Leike and Hutter and by Orseau on the weaknesses. The toy programs are my own teaching examples, not code from those papers.")],
 [("What does AIXI maximize?", ["Total reward", "Program length", "Memory", "Speed"], 0, "It is a reinforcement learning agent."),
  ("What two ideas make up AIXI?", ["Solomonoff induction and expectimax planning", "Backpropagation and dropout", "Alpha-beta and hashing", "Clustering and sorting"], 0, "Prediction plus planning."),
  ("Can AIXI be run on a computer?", ["Yes, quickly", "No, it is incomputable", "Only on GPUs", "Only for chess"], 1, "It must weigh all programs."),
  ("What does AIXI assume about the environment?", ["It is computable", "It is random noise", "It is a chess board", "It is a human"], 0, "Some program can produce its replies.")],
 [("Who proposed AIXI?", "Marcus Hutter, in 2000."), ("What is a percept?", "An observation together with a reward."),
  ("What is expectimax?", "Maximize over actions, average over the environment's replies."), ("Why study something incomputable?", "As a yardstick and a source of approximations.")],
 [PL("Run the cycle", "An agent plays a two-action game. The environment pays reward 1 when the action is 1, otherwise 0. Write run_cycle(first, steps): the agent alternates its actions, starting with the action first (0 or 1). Return [total reward, list of rewards in order].",
     "run_cycle(first, steps)", """
def run_cycle(first, steps):
    rewards = []
    a = first
    for t in range(steps):
        r = 0
        if a == 1:
            r = 1
        rewards.append(r)
        a = 1 - a
    return [sum(rewards), rewards]
""", [[0, 5], [1, 5], [1, 1], [0, 0], [0, 8]], "Loop over the steps; flip the action with 1 - a."),
  ORDER("One cycle", "Put the steps of one agent-environment cycle in order.", ["The agent picks an action", "The environment receives the action", "The environment sends an observation and a reward", "The agent adds the new percept to its history", "The agent picks the next action"]),
  MATCH("Terms", "Match each term with its meaning.", [("Agent", "Chooses actions"), ("Environment", "Answers actions with percepts"), ("Percept", "Observation plus reward"), ("Horizon", "How many steps ahead the agent cares about"), ("Solomonoff induction", "Weighs programs by length")]),
  FILL("Basics", "AIXI joins {{Solomonoff induction|Solomonoff}} prediction with {{expectimax}} planning. It is {{incomputable|not computable}}, so it serves as an ideal to approximate.")]))

# ------------------------------------------------------------ 2
CHS.append(CH(
 "The agent-environment cycle",
 ("Interaction", [
  "Agent | outputs | Actions",
  "Environment | outputs | Percepts",
  "Percept | contains | Observation and reward",
  "History | records | Actions and percepts",
  "Policy | maps | Histories to actions",
  "Environment | maps | Histories to percept probabilities",
  "Chronological | means | Replies depend only on the past"]),
 ["The formal setting is simple. Time runs in steps. At step t the agent picks an action a_t from a finite set and the environment replies with a percept, an observation o_t and a reward r_t. Everything seen so far is the history.",
  "A policy maps each history to an action. An environment maps each history and action to a distribution over percepts. There is no assumption that the world is Markov: the reply may depend on the whole past.",
  "The environment must be chronological: its reply at step t cannot depend on actions the agent has not taken yet. This sounds obvious but needs stating when everything is written as functions on strings."],
 [("Action", "A symbol the agent sends, from a finite set."),
  ("Observation", "The non-reward part of a percept."),
  ("Reward", "A number the agent wants to accumulate."),
  ("History", "The sequence of past actions and percepts."),
  ("Policy", "A rule choosing actions from histories."),
  ("Chronological", "Replies depend only on actions taken so far, never on future ones."),
  ("Markov", "The next step depends only on the current state; AIXI does not assume this.")],
 ["A step is an action followed by a percept (observation, reward).",
  "A history is the list of all action-percept pairs so far.",
  "A policy turns a history into an action; an environment turns a history and action into a percept distribution.",
  "No Markov assumption: the whole history may matter.",
  "Chronological environments cannot see future actions.",
  "Total reward over a horizon is the quantity the agent wants to maximize."],
 [T("Start with the vocabulary of the framework in Hutter's survey. There is a finite set of possible actions, a finite set of observations and a set of rewards, usually numbers between zero and one. In cycle k the agent outputs an action. The environment then produces a percept, which carries both an observation and a reward. Then cycle k plus one begins."),
  T("The history after k cycles is the list of all actions and percepts so far, in order. It is everything the agent has ever experienced. A policy is a function from histories to actions. The agent's whole behaviour is its policy, so comparing agents means comparing policies."),
  T("The environment is also a function of the history. In the deterministic case the next percept is a fixed function of the actions so far. In general it is a probability distribution over percepts, given the history and the action just taken. Veness and colleagues define an environment as a sequence of conditional probability functions that obey one consistency condition, that actions do not affect earlier percepts. Hutter calls such environments chronological."),
  M(r"\nu(x_t \mid a_1 x_1 \dots a_{t-1} x_{t-1}\, a_t)"),
  T("Read this as the probability that the environment nu produces percept x at step t, given all earlier actions and percepts and the action just taken. Nothing says the world has a hidden state with the Markov property. A single unseen switch that was flipped fifty steps ago may still matter, and that is allowed."),
  T("This generality is the point. Many problems that look different fit the same mould. A game against an opponent, a sequence to predict, a function to minimize or a supervised learning task can each be written as an environment with the right observations and rewards. Hutter's survey lists exactly these classes, and a chapter of his book is devoted to showing how each one fits."),
  T("The goal is stated through the reward. The agent wants to maximize the sum of rewards over a horizon m, the number of cycles it plans for. Chapter 8 returns to how the horizon is chosen. For now treat it as a fixed number of future steps."),
  T("The practice section builds a small deterministic environment with memory, so you can see how the reply depends on the history. You then run a policy in it and add up the reward.")],
 [("What does a percept contain?", ["An observation and a reward", "Only a reward", "Only an action", "A program"], 0, "o_t and r_t together."),
  ("What is a policy?", ["A map from histories to actions", "A reward", "An environment", "A program length"], 0, "It defines the agent's behaviour."),
  ("Does AIXI assume the environment is Markov?", ["Yes", "No, the whole history may matter", "Only for chess", "Only with discounting"], 1, "There is no Markov assumption."),
  ("What does chronological mean?", ["Replies cannot depend on future actions", "Steps are numbered", "Rewards grow", "Observations are sorted"], 0, "Actions do not affect earlier percepts.")],
 [("What is a history?", "All past actions and percepts, in order."), ("What does an environment return?", "A percept distribution given the history and action."),
  ("What is the reward for?", "It states the goal."), ("Why no Markov assumption?", "To keep the framework fully general.")],
 [PL("An environment with memory", "Write env_reply(actions): given the list of all actions so far (the last one is the current action, each 0 or 1), return [obs, reward]. obs is 1 if the number of 1s among the actions so far is odd, otherwise 0. reward is 1 if the current action equals the previous observation (the observation from the step before; before the first step it is 0), otherwise 0.",
     "env_reply(actions)", """
def env_reply(actions):
    prev_obs = sum(actions[:-1]) % 2
    obs = sum(actions) % 2
    reward = 0
    if actions[-1] == prev_obs:
        reward = 1
    return [obs, reward]
""", [[[0]], [[1]], [[1, 1]], [[1, 0]], [[1, 1, 0, 1]], [[0, 0, 0]]], "The previous observation is the parity of all actions except the last."),
  PL("Run a policy", "Using the same environment (obs is the parity of the number of 1s among actions so far; reward is 1 when the current action equals the previous observation, which starts at 0), write total_reward(steps): the agent plays 'copy the last observation' (its first action is 0, afterwards it plays the most recent observation). Return the total reward over steps steps.",
     "total_reward(steps)", """
def total_reward(steps):
    actions = []
    last_obs = 0
    total = 0
    for t in range(steps):
        a = last_obs
        actions.append(a)
        prev_obs = sum(actions[:-1]) % 2
        obs = sum(actions) % 2
        if a == prev_obs:
            total += 1
        last_obs = obs
    return total
""", [[1], [2], [5], [10], [0]], "Keep the action list; compute the parity before and after adding the new action."),
  MATCH("Symbols", "Match each symbol with its role.", [("a_t", "Action at step t"), ("o_t", "Observation at step t"), ("r_t", "Reward at step t"), ("x_t", "Percept: observation and reward"), ("m", "Horizon")]),
  ORDER("Build a history", "Put these in the order they appear in a history.", ["a1", "x1", "a2", "x2", "a3"]),
  FILL("Setting", "A {{policy}} maps histories to actions. An environment is {{chronological}} when its replies never depend on future actions. A percept is an observation and a {{reward}}.")]))

# ------------------------------------------------------------ 3
CHS.append(CH(
 "Planning with a known model: expectimax",
 ("Expectimax", [
  "Expectimax | alternates | Max and expectation",
  "Max node | is | Agent choice",
  "Chance node | is | Environment reply",
  "Leaf | holds | Accumulated reward",
  "Value | equals | Expected total reward",
  "Optimal policy | maximizes | Value",
  "Tree size | grows | Exponentially with horizon"]),
 ["Suppose the agent knows the environment exactly. Then choosing actions is a planning problem. Draw a tree: at agent nodes pick the best action, at chance nodes average over the environment's replies, and add up rewards along the way. This is expectimax.",
  "The value of a history is the expected total reward the best policy can still collect. The recursion is: value is the maximum over actions of the expected, over percepts, of reward plus the value of the longer history.",
  "The tree grows exponentially with the horizon, which is the first reason AIXI cannot be run. The second is that the environment is not known, which is where Solomonoff induction comes in."],
 [("Expectimax", "Game-tree search with max nodes for the agent and expectation nodes for chance."),
  ("Value function", "The expected total future reward under a policy or the best policy."),
  ("Optimal policy", "A policy that attains the highest value."),
  ("Bellman equation", "The recursion value = max over actions of the expectation of reward plus next value."),
  ("Horizon", "The number of future steps counted."),
  ("Chance node", "A node where the environment draws the next percept.")],
 ["With a known environment, optimal action is a search problem.",
  "Max over actions, expectation over percepts, sum of rewards.",
  "V(h) = max_a sum_x P(x | h a) [ r(x) + V(h a x) ] with V = 0 at the horizon.",
  "The search tree has (actions x percepts)^horizon leaves.",
  "AIXI uses this same recursion, with the true environment replaced by a mixture.",
  "Sampling approximations such as UCT avoid expanding the whole tree."],
 [T("Forget learning for a chapter. Assume the agent is told the exact environment, meaning a rule that gives the probability of each percept after each history and action. What should it do? This is a decision problem under uncertainty, and the classical solution is dynamic programming, the Bellman equation."),
  T("Define the value of a history h with k steps left as the expected total reward from now on, if the agent plays the best possible way. With no steps left the value is zero. With steps left, try each action a. For each, the environment answers with percept x with some probability. The percept brings reward r and a longer history. Average reward plus future value over the percepts, then pick the action with the highest average."),
  M(r"V_k(h) \;=\; \max_{a}\; \sum_{x} P(x \mid h, a)\,\bigl[\, r(x) + V_{k-1}(h\,a\,x)\,\bigr], \qquad V_0 = 0"),
  T("Written as a tree, the actions form max nodes and the percepts form chance nodes, stacked alternately. The leaves are at depth k. The number of leaves is the number of actions times the number of percepts, raised to the power k. A binary action, a binary reward and a horizon of twenty already give about a trillion leaves, which is why exact planning only works for small cases."),
  T("Two observations will matter later. First, an optimal policy exists for every finite horizon and can be found by the backward recursion above. Second, because the environment's replies can depend on the full history, the tree must be indexed by histories, not by states. AIXI uses exactly this recursion. The only change is that the true probabilities are replaced by a mixture, the subject of the next chapters."),
  T("Veness and colleagues note that expectimax cannot be done exactly at scale and use a Monte Carlo tree search instead, in a version of the UCT algorithm they call rho-UCT. It samples trajectories through the tree and spends more effort on promising branches. Chapter 11 sets out how it works."),
  T("In the practice section you evaluate small expectimax trees, then plan in a stochastic environment whose reward chances depend on the previous action.")],
 [("What does expectimax maximize over?", ["The agent's actions", "The environment's replies", "Program length", "Memory"], 0, "Max nodes are agent choices."),
  ("What does it average over?", ["The environment's possible percepts", "Actions", "Steps", "Programs"], 0, "Chance nodes average."),
  ("What is the value at zero steps remaining?", ["Zero", "One", "Infinity", "Undefined"], 0, "No more reward can be collected."),
  ("Why is exact expectimax impractical?", ["The tree grows exponentially", "Rewards are random", "It needs training", "It is not optimal"], 0, "Leaves multiply at every step.")],
 [("What is the Bellman equation?", "Value = max over actions of expected reward plus next value."), ("How many leaves does the tree have?", "(actions x percepts) to the power of the horizon."),
  ("What replaces the true environment in AIXI?", "A mixture over many environments."), ("How is the tree approximated?", "By Monte Carlo sampling such as UCT.")],
 [PL("Evaluate an expectimax tree", "A tree is a number (a leaf), or ['max', [children]], or ['chance', [[probability, child], ...]]. Write expectimax(tree) returning its value: the largest child for max, the probability-weighted sum for chance.",
     "expectimax(tree)", """
def expectimax(tree):
    if not isinstance(tree, list):
        return tree
    if tree[0] == 'max':
        best = None
        for child in tree[1]:
            v = expectimax(child)
            if best is None or v > best:
                best = v
        return best
    total = 0
    for p, child in tree[1]:
        total += p * expectimax(child)
    return total
""", [[3], [["max", [1, 4, 2]]], [["chance", [[0.5, 4], [0.5, 2]]]], [["max", [["chance", [[0.5, 4], [0.5, 0]]], ["chance", [[0.25, 8], [0.75, 1]]], 2.5]]], [["chance", [[0.5, ["max", [1, 3]]], [0.5, ["max", [2, 0]]]]]]], "Check whether the node is a list; recurse on children."),
  PL("Plan in a known stochastic world", "There are two actions, 0 and 1. The chance of reward 1 depends on the previous action (before step 1 it is 0): probs[prev][a] is that chance (reward 0 otherwise). Write plan(probs, steps): return [best expected total reward over steps steps, the best first action]. Break ties by choosing the smaller action.",
     "plan(probs, steps)", """
def plan(probs, steps):
    def val(prev, k):
        if k == 0:
            return [0.0, 0]
        best = -1.0
        arg = 0
        for a in range(2):
            v = probs[prev][a] + val(a, k - 1)[0]
            if v > best + 1e-12:
                best = v
                arg = a
        return [best, arg]
    return val(0, steps)
""", [[[[0.5, 0.2], [0.9, 0.1]], 1], [[[0.5, 0.2], [0.9, 0.1]], 3], [[[0.1, 0.9], [0.9, 0.1]], 4], [[[0.3, 0.3], [0.3, 0.3]], 2], [[[0.2, 0.8], [0.7, 0.6]], 5]], "Recurse on (previous action, steps left); add the immediate chance to the future value.", approx=1e-9),
  ORDER("Backward recursion", "Order the steps of exact planning with a known model.", ["Set the value to zero at the horizon", "For each action, list the possible percepts", "Add reward and next-step value for each percept", "Average over percepts by their probabilities", "Take the maximum over actions"]),
  MATCH("Nodes", "Match each node with its job.", [("Max node", "The agent picks the best action"), ("Chance node", "The environment draws a percept"), ("Leaf", "Search stops and no more reward is counted"), ("Root", "The current history")]),
  FILL("Planning", "Expectimax takes a {{maximum|max}} over actions and an {{expectation|average}} over percepts. The number of leaves grows {{exponentially}} with the horizon.")]))

# ------------------------------------------------------------ 4
CHS.append(CH(
 "Bayesian mixtures and prediction",
 ("Mixtures", [
  "Hypothesis class | contains | Candidate environments",
  "Prior | assigns | Weight to each",
  "Bayes rule | updates | Weights by likelihood",
  "Mixture | predicts | Weighted average",
  "Mixture | dominates | Every member",
  "Dominance | bounds | Loss by log of 1 over weight",
  "Posterior | sharpens | On consistent members"]),
 ["When the environment is unknown, a Bayesian keeps several candidates, each with a prior weight. As data arrives, candidates that predicted it badly lose weight. To predict, average the candidates' predictions using the current weights.",
  "The mixture has a remarkable property. It assigns every observed sequence at least its prior weight times the probability that the true candidate gave it. So it can never do much worse than the best candidate, and the extra cost is at most the log of one over that candidate's weight.",
  "AIXI uses the largest sensible class, all computable environments, and a particular prior, which is the topic of the next chapters."],
 [("Hypothesis class", "The set of environments the agent considers possible."),
  ("Prior", "Weights on hypotheses before seeing data; they sum to at most one."),
  ("Posterior", "Weights after seeing data, by Bayes rule."),
  ("Mixture", "A weighted average of the hypotheses' probabilities; written xi."),
  ("Dominance", "xi(x) is at least w times nu(x) for every member nu with weight w."),
  ("Likelihood", "The probability a hypothesis gave to the data actually seen.")],
 ["Bayes rule: new weight is proportional to old weight times likelihood.",
  "Mixture probability xi(x) = sum of w_i times nu_i(x).",
  "Dominance: xi(x) >= w_i nu_i(x) for each i.",
  "Hence the log-loss of the mixture exceeds the best member's by at most ln(1/w_i).",
  "For deterministic hypotheses, the mixture's mistakes are bounded by the log of one over the true hypothesis's weight in bits.",
  "A class containing the truth with positive prior weight is called a grain of truth."],
 [T("A hypothesis here is a complete probabilistic model of the environment: given a history it says how likely each next percept is. Suppose the agent has a list of such models, nu one, nu two and so on, and a prior weight for each, w one, w two, adding up to at most one. How should it predict?"),
  T("The Bayesian mixture is the answer. The agent's probability of any data x is the weighted sum of the models' probabilities. Written as an equation, xi of x equals the sum over i of w i times nu i of x. It is a legitimate probability model in its own right."),
  M(r"\xi(x) \;=\; \sum_i w_i\,\nu_i(x)"),
  T("Bayes rule updates the weights. After seeing x, the posterior weight of model i is its old weight times the probability it gave to x, divided by the mixture's probability of x. A model that predicted x well gains weight. A model that gave x probability zero loses all weight and never returns. Predicting the next symbol means averaging the models' next-symbol predictions with these posterior weights."),
  T("Now the key inequality. Because the mixture is a sum of non-negative terms, it is at least each single term. So xi of x is at least w i times nu i of x, for every member i. Taking logarithms, the mixture's log-loss on the data exceeds the log-loss of model i by at most the log of one over w i. This holds for any data, whatever the truth."),
  T("If the data really is drawn from model i, the mixture's total loss exceeds the best possible by a constant that depends only on the prior weight of the truth, not on how long the data goes on. A good prior weight is therefore a bounded one-time cost. Solomonoff chose weights so that every computable model gets a decent share, and the next chapters show how."),
  T("There is a catch that foreshadows chapter 12. Dominance only helps when the truth is in the class with positive weight, the so-called grain of truth. And in the agent setting, the data depends on what the agent does, so a mixture that predicts passively well may still act badly."),
  T("The practice section implements Bayes updating, the mixture prediction and the regret bound for coin-flip hypotheses.")],
 [("What is the mixture probability of x?", ["The weighted sum of the models' probabilities", "The largest probability", "The smallest probability", "A random choice"], 0, "xi(x) = sum w_i nu_i(x)."),
  ("What does a model that gave the data probability zero get after Bayes update?", ["Weight zero", "More weight", "The same weight", "Weight one"], 0, "It is eliminated."),
  ("Dominance means:", ["xi(x) is at least w_i nu_i(x)", "xi(x) is zero", "xi is deterministic", "xi equals the prior"], 0, "A sum is at least each term."),
  ("What is the extra loss of the mixture over model i bounded by?", ["ln(1/w_i)", "The data length", "Zero", "w_i"], 0, "A one-time cost set by the prior.")],
 [("What is a grain of truth?", "The true environment is in the class with positive weight."), ("What is a posterior?", "Weights after seeing data."),
  ("Why can't the mixture be much worse than the best member?", "Dominance."), ("What happens to impossible hypotheses?", "Their weight drops to zero.")],
 [PL("Bayes update", "Given prior weights and likelihoods (the probability each hypothesis gave to the data just seen), return the normalized posterior weights. Write bayes_update(weights, likelihoods).",
     "bayes_update(weights, likelihoods)", """
def bayes_update(weights, likelihoods):
    raw = []
    for w, l in zip(weights, likelihoods):
        raw.append(w * l)
    total = sum(raw)
    return [x / total for x in raw]
""", [[[0.5, 0.5], [0.9, 0.1]], [[0.25, 0.75], [0.5, 0.5]], [[0.5, 0.25, 0.25], [0.0, 1.0, 0.5]], [[1.0], [0.3]], [[0.2, 0.3, 0.5], [0.1, 0.2, 0.7]]], "Multiply weight by likelihood, then divide by the total.", approx=1e-9),
  PL("Mixture prediction", "Each hypothesis is a coin with probability theta of heads (a 1). After the bits seen so far the weights are posterior weights. Write predict_next(bits, thetas, weights): update the prior weights on the bits (each 1 has likelihood theta, each 0 has 1 - theta), and return the mixture probability that the next bit is 1.",
     "predict_next(bits, thetas, weights)", """
def predict_next(bits, thetas, weights):
    w = list(weights)
    for b in bits:
        for i in range(len(w)):
            if b == 1:
                w[i] = w[i] * thetas[i]
            else:
                w[i] = w[i] * (1 - thetas[i])
    total = sum(w)
    p = 0.0
    for i in range(len(w)):
        p += w[i] / total * thetas[i]
    return p
""", [[[], [0.2, 0.8], [0.5, 0.5]], [[1, 1, 1], [0.2, 0.8], [0.5, 0.5]], [[0, 0, 0, 0], [0.2, 0.8], [0.5, 0.5]], [[1, 0, 1, 1], [0.25, 0.5, 0.75], [0.25, 0.5, 0.25]], [[1], [0.0, 1.0], [0.9, 0.1]]], "Update the weights bit by bit, normalize, then average theta.", approx=1e-9),
  PL("Regret bound", "With hypotheses that are coins (theta = chance of a 1) and prior weights, compute for the bit string bits and hypothesis index i: [regret, bound] where regret is ln nu_i(bits) minus ln xi(bits) (nu_i is the probability model i gives to the whole string, xi the mixture), and bound is ln(1 / weights[i]). Write regret_bound(bits, thetas, weights, i). Use import math.",
     "regret_bound(bits, thetas, weights, i)", """
import math
def regret_bound(bits, thetas, weights, i):
    def prob(theta):
        p = 1.0
        for b in bits:
            if b == 1:
                p *= theta
            else:
                p *= 1 - theta
        return p
    xi = 0.0
    for th, w in zip(thetas, weights):
        xi += w * prob(th)
    nu = prob(thetas[i])
    return [math.log(nu) - math.log(xi), math.log(1 / weights[i])]
""", [[[1, 1, 0, 1], [0.25, 0.75], [0.5, 0.5], 1], [[0, 0, 0, 0, 0], [0.1, 0.5, 0.9], [0.25, 0.5, 0.25], 0], [[1, 0, 1, 0, 1, 0], [0.5, 0.9], [0.1, 0.9], 0], [[1, 1, 1, 1], [0.3, 0.6, 0.9], [0.2, 0.3, 0.5], 2]], "The mixture is a weighted sum of the two products; take logs at the end.", approx=1e-9),
  ORDER("One Bayesian step", "Order the steps.", ["Start with the prior weights", "See a new bit", "Compute each model's probability for that bit", "Multiply weights by these probabilities", "Normalize to get the posterior"]),
  MATCH("Terms", "Match each term with its role.", [("Prior", "Weights before data"), ("Likelihood", "How well a model predicted the data"), ("Posterior", "Weights after data"), ("Mixture", "Weighted average of all models"), ("Grain of truth", "The true model has positive weight")]),
  FILL("Mixtures", "The {{mixture}} probability is a weighted sum. {{Dominance}} says it is at least the prior weight times each member's probability. A model that gave the data probability zero has weight {{zero|0}}.")]))
