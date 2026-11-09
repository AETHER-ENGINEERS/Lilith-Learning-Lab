"""Direct Preference Optimization course."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "From RLHF to DPO",
 ("DPO", [
  "DPO | introduced by | Rafailov et al. 2023",
  "DPO | replaces | Reward model plus RL",
  "DPO | uses | Preference pairs",
  "DPO | is | A classification loss",
  "Reference model | anchors | The policy",
  "Beta | controls | Distance from reference",
  "DPO | appeared at | NeurIPS 2023"]),
 ["Direct Preference Optimization, DPO, is a way to align a language model with human preferences using a simple loss on pairs of responses, one preferred and one rejected. It was introduced by Rafael Rafailov and colleagues at Stanford, NeurIPS 2023.",
  "The usual route, RLHF, trains a reward model and then uses reinforcement learning such as PPO. DPO shows that, under the standard assumptions, the same goal can be reached by training the language model directly with a binary cross-entropy loss. No separate reward model and no sampling loop are needed.",
  "This course derives the loss step by step and builds each part in small Python labs."],
 [("Preference pair", "A prompt with a chosen (preferred) response and a rejected one."),
  ("RLHF", "Reinforcement learning from human feedback."),
  ("Reference model", "A frozen copy of the starting model."),
  ("Implicit reward", "The reward that the policy itself defines: beta times the log-ratio to the reference."),
  ("Beta", "A coefficient controlling how far the policy may move from the reference."),
  ("Binary cross-entropy", "The loss for a yes-or-no prediction.")],
 ["DPO: Rafailov, Sharma, Mitchell, Ermon, Manning and Finn, NeurIPS 2023.",
  "Input: triples (x, y_w, y_l) with a winner and a loser.",
  "Loss: -log sigmoid(beta (log pi/pi_ref (y_w) - log pi/pi_ref (y_l))).",
  "No reward model, no RL sampling during training.",
  "It assumes the Bradley-Terry model of preferences.",
  "It needs log-probabilities from the policy and the frozen reference."],
 [T("A language model trained on text can write fluently but does not know what people prefer. To align it, the standard pipeline of RLHF has three stages. Fine-tune on good examples. Train a reward model on human comparisons. Then optimise the language model against the reward model with reinforcement learning, with a penalty that keeps it close to the starting model."),
  T("That last stage is heavy. It samples from the model during training, it needs the reward model, a value model and a reference model in memory, and it is sensitive to hyperparameters. The question behind DPO is whether all that is necessary."),
  T("The DPO paper's answer is no. Its key observation is that the RL objective used in RLHF has a closed-form optimal policy, and that this relation can be turned around: the reward can be written in terms of the policy. Once the reward is expressed through the policy, the preference-learning step for the reward model becomes a loss on the policy itself."),
  M(r"\mathcal{L}_{\mathrm{DPO}}(\pi_\theta;\pi_{\mathrm{ref}}) \;=\; -\,\mathbb{E}_{(x,y_w,y_l)}\Bigl[\ \log \sigma\Bigl(\beta \log\frac{\pi_\theta(y_w\mid x)}{\pi_{\mathrm{ref}}(y_w\mid x)} \;-\; \beta \log\frac{\pi_\theta(y_l\mid x)}{\pi_{\mathrm{ref}}(y_l\mid x)}\Bigr)\Bigr]"),
  T("This is a binary classification loss. For each pair it asks: does the policy, relative to the reference, favour the winner over the loser? Training increases the log-probability ratio of winners and decreases that of losers. That is all. It can be implemented in a few lines on top of ordinary supervised fine-tuning code."),
  T("A note on sources. This course follows the DPO paper and standard descriptions of it. Later variants and comparisons are marked as background knowledge. The labs use tiny numerical examples, not a real language model.")],
 [("What does DPO remove from RLHF?", ["The separate reward model and RL loop", "The reference model", "The preference data", "The language model"], 0, "It trains with a classification loss."),
  ("What is one training example?", ["A prompt with a chosen and a rejected response", "A single response", "A reward score", "A token"], 0, "(x, y_w, y_l)."),
  ("What anchors the policy?", ["The frozen reference model", "The reward model", "The tokenizer", "The batch size"], 0, "Via the log-ratio."),
  ("Who introduced DPO?", ["Rafailov and colleagues", "Schulman and colleagues", "Vaswani and colleagues", "Silver and colleagues"], 0, "NeurIPS 2023.")],
 [("What does beta do?", "Controls the distance from the reference."), ("What kind of loss is DPO?", "Binary cross-entropy on pairs."), ("What preference model is assumed?", "Bradley-Terry."), ("What must be computed?", "Log-probs under policy and reference.")],
 [ORDER("RLHF versus DPO", "Put the DPO training steps in order.", ["Start from a supervised model and freeze a copy as the reference", "Collect preference pairs", "Compute policy and reference log-probabilities of both responses", "Compute the DPO loss", "Update the policy by gradient descent"]),
  MATCH("Terms", "Match each term with its meaning.", [("Chosen response", "The preferred answer"), ("Rejected response", "The less preferred answer"), ("Reference model", "Frozen starting model"), ("beta", "Strength of the anchor"), ("Implicit reward", "Beta times the log-ratio")]),
  FILL("Idea", "DPO trains the policy directly on {{preference|preferences}} pairs, with no separate {{reward}} model.")]))

CHS.append(CH(
 "Preference data and the Bradley-Terry model",
 ("Preferences", [
  "Bradley-Terry | models | Pairwise preferences",
  "Sigmoid | converts | Reward gaps to probabilities",
  "Reward gap | drives | Preference probability",
  "Equal rewards | give | One half",
  "Log-likelihood | trains | The reward",
  "Annotators | choose | The better response",
  "Noise | blurs | Labels"]),
 ["Human feedback usually comes as comparisons: given two responses, which is better? The Bradley-Terry model turns this into probability. If response A has reward r_A and B has r_B, the chance that A is preferred is the sigmoid of the reward gap.",
  "A reward model is trained by maximising the log-likelihood of the observed choices. RLHF does this as a separate stage. DPO reuses the same likelihood but with the reward expressed through the policy.",
  "The labs compute sigmoid, preference probabilities and the log-likelihood of a dataset."],
 [("Bradley-Terry model", "p(A beats B) = sigmoid(r_A - r_B)."),
  ("Sigmoid", "sigma(z) = 1 / (1 + exp(-z)); maps any number into (0, 1)."),
  ("Log-sigmoid", "log sigma(z): the log-probability of the observed choice."),
  ("Reward gap", "The difference r_w - r_l between winner and loser."),
  ("Log-likelihood", "The sum of log-probabilities of the data."),
  ("Annotator agreement", "How often different people make the same choice.")],
 ["p(y_w beats y_l) = sigmoid(r(y_w) - r(y_l)).",
  "sigmoid(0) = 0.5; large positive gap gives probability near 1.",
  "Training a reward model: minimise -log sigmoid(r_w - r_l).",
  "Only reward differences matter, not absolute values.",
  "Real labels are noisy; Bradley-Terry treats them as probabilistic.",
  "The model assumes preferences come from a single underlying score."],
 [T("Asking people to give a response a score from one to ten is unreliable: different people use the scale differently. Asking which of two responses is better is easier and more consistent. That is why preference data usually takes the form of comparisons."),
  T("To learn from comparisons we need a model of how they arise. The Bradley-Terry model, from 1952, supposes each item has a hidden score, and the chance that one beats another depends on the gap between scores. The bigger the gap, the more reliably the higher-scored item wins."),
  M(r"p(y_w \succ y_l \mid x) \;=\; \sigma\bigl(r(x,y_w) - r(x,y_l)\bigr), \qquad \sigma(z) = \frac{1}{1+e^{-z}}"),
  T("Look at the shape of the sigmoid. At zero it is one half: equal scores, a coin toss. For a gap of two it is about 0.88. For a gap of five, about 0.99. Because only the difference matters, adding the same number to all rewards changes nothing. This invariance will be important in the derivation."),
  T("Given a dataset of pairs, the reward model is trained by maximum likelihood: pick the scores that make the observed winners as probable as possible. Equivalently, minimise the negative log-likelihood. This is the classic first stage of RLHF."),
  M(r"\mathcal{L}_R(\phi) \;=\; -\,\mathbb{E}_{(x,y_w,y_l)}\bigl[\log \sigma\bigl(r_\phi(x,y_w) - r_\phi(x,y_l)\bigr)\bigr]"),
  T("DPO keeps exactly this loss. What changes is what plays the role of the reward. The next chapters show that the policy itself can define it.")],
 [("What is sigmoid(0)?", ["0.5", "0", "1", "Undefined"], 0, "Equal scores."),
  ("What does Bradley-Terry depend on?", ["The reward difference", "The absolute reward", "The length", "The prompt only"], 0, "Only gaps matter."),
  ("What is trained by -log sigmoid(r_w - r_l)?", ["A reward model", "A tokenizer", "A decoder", "A value head"], 0, "Maximum likelihood."),
  ("Why comparisons rather than scores?", ["They are more consistent", "They are cheaper to store", "They need no people", "They avoid language"], 0, "People disagree on scales.")],
 [("Who proposed the model?", "Bradley and Terry, 1952."), ("What happens if rewards shift equally?", "Nothing changes."), ("What does a gap of 5 give?", "About 0.99."), ("What is log sigmoid?", "Log-probability of the observed choice.")],
 [PL("Sigmoid", "Write sigmoid(z): 1 / (1 + exp(-z)), rounded to 9 decimals. Use import math.",
     "sigmoid(z)", """
import math
def sigmoid(z):
    return round(1.0 / (1.0 + math.exp(-z)), 9)
""", [[0], [2], [-2], [5], [-5], [0.5]], "One line.", approx=1e-9),
  PL("Preference probability", "Write pref_prob(r_a, r_b): the Bradley-Terry probability that A beats B, rounded to 9 decimals. Use import math.",
     "pref_prob(r_a, r_b)", """
import math
def pref_prob(r_a, r_b):
    return round(1.0 / (1.0 + math.exp(-(r_a - r_b))), 9)
""", [[1.0, 1.0], [3.0, 1.0], [1.0, 3.0], [10.0, 5.0], [-1.0, -2.0]], "Sigmoid of the gap.", approx=1e-9),
  PL("Reward model loss", "Write rm_loss(pairs): pairs is a list of [r_w, r_l]; return the mean of -ln sigmoid(r_w - r_l), rounded to 9 decimals. Use import math.",
     "rm_loss(pairs)", """
import math
def rm_loss(pairs):
    s = 0.0
    for w, l in pairs:
        s += -math.log(1.0 / (1.0 + math.exp(-(w - l))))
    return round(s / len(pairs), 9)
""", [[[[1.0, 0.0]]], [[[0.0, 0.0]]], [[[2.0, 0.0], [0.0, 2.0]]], [[[5.0, 1.0], [3.0, 2.0], [1.0, 1.5]]]], "Mean negative log-probability.", approx=1e-9),
  PL("Accuracy", "Write pref_accuracy(pairs): the fraction of pairs [r_w, r_l] with r_w greater than r_l.",
     "pref_accuracy(pairs)", """
def pref_accuracy(pairs):
    n = 0
    for w, l in pairs:
        if w > l:
            n += 1
    return n / len(pairs)
""", [[[[1, 0], [0, 1], [2, 1]]], [[[1, 1]]], [[[3, 0], [4, 1]]], [[[0, 1], [0, 2]]]], "Count correct orderings.", approx=1e-12),
  ORDER("Learning rewards from comparisons", "Order the steps.", ["Show annotators two responses", "Record the preferred one", "Model the choice with Bradley-Terry", "Maximise the log-likelihood", "Obtain rewards that explain the choices"]),
  MATCH("Quantities", "Match each quantity with its value.", [("sigmoid(0)", "0.5"), ("Gap very large", "Probability near 1"), ("Gap very negative", "Probability near 0"), ("Equal rewards", "Coin toss"), ("Shift all rewards", "No change")]),
  FILL("Bradley-Terry", "The chance that A wins is the {{sigmoid}} of the reward {{gap|difference}}.")]))

CHS.append(CH(
 "The KL-regularised objective and its optimal policy",
 ("Optimal policy", [
  "RLHF objective | maximises | Reward minus KL",
  "KL term | keeps | Policy near reference",
  "Beta | weights | The KL penalty",
  "Optimal policy | is | Reference times exp of reward",
  "Partition function | normalises | The result",
  "Reward | defines | A tilt of the reference",
  "High beta | means | Stay close"]),
 ["The RL stage of RLHF maximises expected reward while keeping the policy near the reference model: a reward term minus beta times the KL divergence from the reference. This problem has a closed-form solution.",
  "The optimal policy is the reference policy reweighted by the exponential of reward over beta, then normalised. Responses with high reward get more probability, with beta controlling how strongly.",
  "The normaliser, called the partition function, is expensive to compute for language models. DPO's trick, in the next chapter, is that it will cancel."],
 [("KL-regularised objective", "E[r(x, y)] - beta * KL(pi || pi_ref)."),
  ("Optimal policy", "pi*(y|x) = pi_ref(y|x) exp(r(x,y)/beta) / Z(x)."),
  ("Partition function", "Z(x) = sum_y pi_ref(y|x) exp(r(x,y)/beta), the normaliser."),
  ("Tilting", "Reweighting a distribution by an exponential factor."),
  ("Temperature", "Here beta plays the role of a temperature on the reward."),
  ("Support", "The set of responses with nonzero probability.")],
 ["max over pi of E_{y~pi}[r(x,y)] - beta KL(pi(.|x) || pi_ref(.|x)).",
  "Solution: pi*(y|x) = pi_ref(y|x) exp(r(x,y)/beta) / Z(x).",
  "beta -> infinity: pi* approaches pi_ref; beta -> 0: pi* concentrates on the highest-reward response.",
  "Z(x) sums over all possible responses, which is intractable for language models.",
  "The same form appears in maximum-entropy RL and in statistical physics (Boltzmann).",
  "The paper derives this as a known result in the appendix."],
 [T("Here is the optimisation problem of RLHF's last stage. For each prompt we want a policy that earns high reward, but not at the price of drifting far from the reference. So we maximise the expected reward minus beta times the KL divergence from the reference."),
  M(r"\max_{\pi}\ \ \mathbb{E}_{y\sim\pi(\cdot\mid x)}\bigl[r(x,y)\bigr] \;-\; \beta\, D_{\mathrm{KL}}\bigl[\pi(\cdot\mid x)\,\|\,\pi_{\mathrm{ref}}(\cdot\mid x)\bigr]"),
  T("This can be solved exactly. The solution takes the reference distribution and multiplies each response's probability by an exponential factor in its reward. Then it divides by a constant so that probabilities sum to one. A response with high reward is made more likely, but never to the exclusion of the others, because the reference still contributes."),
  M(r"\pi^{*}(y\mid x) \;=\; \frac{1}{Z(x)}\,\pi_{\mathrm{ref}}(y\mid x)\,\exp\!\Bigl(\frac{1}{\beta}\,r(x,y)\Bigr), \qquad Z(x)=\sum_{y}\pi_{\mathrm{ref}}(y\mid x)\exp\!\Bigl(\frac{1}{\beta}\,r(x,y)\Bigr)"),
  T("Look at the two limits of beta. When beta is very large, the exponent is near zero, the factor is near one for every response, and the optimal policy is the reference. When beta is small, the exponent is huge for the best response, and the policy puts nearly all its probability there. So beta sets a dial between caution and greed."),
  T("The trouble is Z of x. It is a sum over every possible response, an astronomically large set for a language model. So we cannot evaluate the optimal policy directly, and RLHF falls back on RL sampling to approach it. DPO instead keeps the formula and uses it algebraically.")],
 [("What does the KL term do?", ["Keeps the policy near the reference", "Raises the reward", "Trains the reward model", "Adds data"], 0, "Weighted by beta."),
  ("What is the optimal policy?", ["Reference times exp(reward/beta), normalised", "The highest reward response only", "Uniform", "The reward model"], 0, "A tilt of the reference."),
  ("What happens as beta goes to infinity?", ["Optimal policy approaches the reference", "It becomes deterministic", "It diverges", "It becomes uniform"], 0, "The tilt vanishes."),
  ("Why is Z(x) a problem?", ["It sums over all responses", "It is negative", "It depends on beta only", "It is random"], 0, "Intractable.")],
 [("What is Z?", "The partition function."), ("What does small beta do?", "Concentrates on the best response."), ("What is the limit of large beta?", "The reference."), ("Where else does this form occur?", "Statistical physics.")],
 [PL("Optimal policy over a few responses", "Write optimal_policy(pi_ref, rewards, beta): the list pi*_i = pi_ref_i * exp(r_i / beta) / Z, rounded to 9 decimals. Use import math.",
     "optimal_policy(pi_ref, rewards, beta)", """
import math
def optimal_policy(pi_ref, rewards, beta):
    w = [p * math.exp(r / beta) for p, r in zip(pi_ref, rewards)]
    z = sum(w)
    return [round(x / z, 9) for x in w]
""", [[[0.5, 0.5], [0.0, 0.0], 1.0], [[0.5, 0.5], [1.0, 0.0], 1.0], [[0.5, 0.5], [1.0, 0.0], 0.1], [[0.5, 0.5], [1.0, 0.0], 100.0], [[0.2, 0.3, 0.5], [0.0, 1.0, 2.0], 0.5]], "Weights then normalise."),
  PL("Partition function", "Write partition(pi_ref, rewards, beta): Z = sum of pi_ref_i * exp(r_i / beta), rounded to 9 decimals. Use import math.",
     "partition(pi_ref, rewards, beta)", """
import math
def partition(pi_ref, rewards, beta):
    s = 0.0
    for p, r in zip(pi_ref, rewards):
        s += p * math.exp(r / beta)
    return round(s, 9)
""", [[[0.5, 0.5], [0.0, 0.0], 1.0], [[0.5, 0.5], [1.0, 0.0], 1.0], [[1.0], [2.0], 2.0], [[0.25, 0.75], [4.0, 0.0], 2.0]], "Sum of tilted weights.", approx=1e-9),
  PL("KL divergence", "Write kl(p, q): sum p_i ln(p_i / q_i) (skip zero p_i), rounded to 9 decimals. Use import math.",
     "kl(p, q)", """
import math
def kl(p, q):
    s = 0.0
    for a, b in zip(p, q):
        if a > 0:
            s += a * math.log(a / b)
    return round(s, 9)
""", [[[0.5, 0.5], [0.5, 0.5]], [[0.9, 0.1], [0.5, 0.5]], [[1.0, 0.0], [0.5, 0.5]], [[0.2, 0.3, 0.5], [0.3, 0.3, 0.4]]], "Standard formula.", approx=1e-9),
  PL("RLHF objective", "Write rlhf_objective(pi, pi_ref, rewards, beta): sum_i pi_i r_i minus beta times KL(pi || pi_ref), rounded to 9 decimals. Use import math.",
     "rlhf_objective(pi, pi_ref, rewards, beta)", """
import math
def rlhf_objective(pi, pi_ref, rewards, beta):
    er = 0.0
    kl = 0.0
    for p, q, r in zip(pi, pi_ref, rewards):
        er += p * r
        if p > 0:
            kl += p * math.log(p / q)
    return round(er - beta * kl, 9)
""", [[[0.5, 0.5], [0.5, 0.5], [1.0, 0.0], 1.0], [[0.9, 0.1], [0.5, 0.5], [1.0, 0.0], 1.0], [[0.9, 0.1], [0.5, 0.5], [1.0, 0.0], 0.1], [[1.0, 0.0], [0.5, 0.5], [1.0, 0.0], 0.5]], "Expected reward minus the penalty.", approx=1e-9),
  ORDER("Solving the objective", "Order the steps.", ["Write reward minus beta times KL", "Find the distribution that maximises it", "Weight the reference by exp(r/beta)", "Divide by the partition function", "Obtain the optimal policy"]),
  MATCH("Beta", "Match each setting with its effect.", [("Beta large", "Stay near reference"), ("Beta small", "Chase reward"), ("Z", "Normaliser"), ("exp(r/beta)", "Tilt factor"), ("KL", "Distance from reference")]),
  FILL("Optimal", "The optimal policy tilts the {{reference}} by exp(r over {{beta}}) and normalises.")]))

CHS.append(CH(
 "Deriving the DPO loss",
 ("Derivation", [
  "Optimal policy | implies | Reward from policy",
  "Reward | equals | Beta log ratio plus log Z",
  "Log Z | depends on | Prompt only",
  "Reward gap | cancels | Log Z",
  "Bradley-Terry | then uses | Policy ratios",
  "Loss | is | Negative log sigmoid",
  "Policy | acts as | A reward model"]),
 ["Take the optimal policy formula and solve it for the reward: r equals beta times the log of the policy over the reference, plus beta times log Z of x. The reward is expressed through the policy.",
  "Substitute into the Bradley-Terry model. The reward gap between the winner and the loser contains log Z of x twice, with opposite signs, so it cancels. The preference probability depends only on the policy and reference.",
  "Maximum likelihood on the observed preferences then gives the DPO loss."],
 [("Reward reparameterisation", "r(x,y) = beta log(pi*(y|x)/pi_ref(y|x)) + beta log Z(x)."),
  ("Cancellation", "log Z(x) appears in both rewards of a pair and drops out of their difference."),
  ("Implicit reward", "r_hat(x,y) = beta log(pi_theta(y|x)/pi_ref(y|x))."),
  ("Log-ratio", "log pi_theta(y|x) - log pi_ref(y|x)."),
  ("Margin", "The implicit reward gap between winner and loser."),
  ("Closed-form", "Given by a formula, without iterative search.")],
 ["From pi*: r(x,y) = beta log(pi*(y|x)/pi_ref(y|x)) + beta log Z(x).",
  "Gap: r(x,y_w) - r(x,y_l) = beta log(pi*(y_w)/pi_ref(y_w)) - beta log(pi*(y_l)/pi_ref(y_l)).",
  "Z(x) cancels because both responses answer the same prompt.",
  "Replace pi* by the trainable pi_theta and maximise the Bradley-Terry likelihood.",
  "The result is the DPO loss; the policy network is the reward model.",
  "The paper states the language model is secretly a reward model."],
 [T("Start from the closed-form optimal policy of the last chapter. Take logarithms and rearrange. The log of the optimal policy equals the log of the reference, plus the reward over beta, minus log Z. Solve for the reward."),
  M(r"r(x,y) \;=\; \beta\,\log\frac{\pi^{*}(y\mid x)}{\pi_{\mathrm{ref}}(y\mid x)} \;+\; \beta\,\log Z(x)"),
  T("This is the key step. It says that any reward function corresponds to an optimal policy, and conversely any policy can be read as defining a reward, up to the term beta log Z of x. That extra term depends on the prompt, not on the response."),
  T("Now put this reward into the Bradley-Terry model. The probability of preferring the winner depends on the reward gap between winner and loser, for the same prompt. In the gap, the log Z terms are identical, so they subtract away. The intractable partition function disappears."),
  M(r"p^{*}(y_w\succ y_l\mid x) \;=\; \sigma\Bigl(\beta\log\frac{\pi^{*}(y_w\mid x)}{\pi_{\mathrm{ref}}(y_w\mid x)} - \beta\log\frac{\pi^{*}(y_l\mid x)}{\pi_{\mathrm{ref}}(y_l\mid x)}\Bigr)"),
  T("The last step is to treat the policy as the unknown. Replace the optimal policy by a trainable one, and fit it by maximum likelihood on the observed preferences. Minimising the negative log-likelihood gives the DPO loss from chapter 1. The paper summarises this by saying that the language model is secretly a reward model."),
  T("It is worth saying what is assumed. The derivation relies on the Bradley-Terry model being a good description of the preferences, and on the policy class being flexible enough to represent the optimum. Where these fail, DPO and RLHF can differ in practice. The labs below compute the implicit reward, the margin and the loss.")],
 [("What cancels in the derivation?", ["log Z(x)", "beta", "The reference", "The winner"], 0, "It is the same for both responses."),
  ("What is the implicit reward?", ["beta times the log ratio policy over reference", "The policy probability", "The reference probability", "The KL"], 0, "Up to a prompt term."),
  ("What is assumed about preferences?", ["Bradley-Terry", "Uniform", "Deterministic", "Independent of prompt"], 0, "Probabilistic from reward gaps."),
  ("What is the policy network in DPO?", ["Also a reward model, implicitly", "Only a generator", "A critic", "A tokenizer"], 0, "The paper's phrase.")],
 [("Why does Z cancel?", "Both responses share the prompt."), ("What gets trained?", "The policy parameters."), ("What replaces the reward model?", "The log-ratio to the reference."), ("What is the margin?", "Gap of implicit rewards.")],
 [PL("Implicit reward", "Write implicit_reward(logp, logp_ref, beta): beta * (logp - logp_ref), rounded to 9 decimals.",
     "implicit_reward(logp, logp_ref, beta)", """
def implicit_reward(logp, logp_ref, beta):
    return round(beta * (logp - logp_ref), 9)
""", [[-1.0, -1.0, 0.1], [-0.5, -1.0, 0.1], [-2.0, -1.0, 0.5], [-1.0, -3.0, 1.0]], "Beta times the log ratio.", approx=1e-9),
  PL("Margin", "Write margin(lw, lw_ref, ll, ll_ref, beta): the implicit reward of the winner minus that of the loser, rounded to 9 decimals.",
     "margin(lw, lw_ref, ll, ll_ref, beta)", """
def margin(lw, lw_ref, ll, ll_ref, beta):
    return round(beta * (lw - lw_ref) - beta * (ll - ll_ref), 9)
""", [[-1.0, -1.0, -1.0, -1.0, 0.1], [-0.5, -1.0, -2.0, -1.5, 0.1], [-1.0, -0.5, -0.5, -1.0, 1.0], [-2.0, -2.0, -1.0, -3.0, 0.5]], "Difference of two implicit rewards.", approx=1e-9),
  PL("DPO loss for one pair", "Write dpo_loss(lw, lw_ref, ll, ll_ref, beta): -ln sigmoid(margin), rounded to 9 decimals. Use import math.",
     "dpo_loss(lw, lw_ref, ll, ll_ref, beta)", """
import math
def dpo_loss(lw, lw_ref, ll, ll_ref, beta):
    m = beta * (lw - lw_ref) - beta * (ll - ll_ref)
    return round(-math.log(1.0 / (1.0 + math.exp(-m))), 9)
""", [[-1.0, -1.0, -1.0, -1.0, 0.1], [-0.5, -1.0, -2.0, -1.5, 0.1], [-2.0, -1.0, -0.5, -1.0, 1.0], [-1.0, -2.0, -3.0, -2.0, 0.5]], "The loss is ln 2 when the margin is zero.", approx=1e-9),
  PL("Batch loss and accuracy", "Write dpo_batch(pairs, beta): pairs is a list of [lw, lw_ref, ll, ll_ref]; return [mean DPO loss, fraction of pairs with a positive margin], both rounded to 9 decimals. Use import math.",
     "dpo_batch(pairs, beta)", """
import math
def dpo_batch(pairs, beta):
    tot = 0.0
    ok = 0
    for lw, lwr, ll, llr in pairs:
        m = beta * (lw - lwr) - beta * (ll - llr)
        tot += -math.log(1.0 / (1.0 + math.exp(-m)))
        if m > 0:
            ok += 1
    n = len(pairs)
    return [round(tot / n, 9), round(ok / n, 9)]
""", [[[[-1.0, -1.0, -1.0, -1.0]], 0.1], [[[-0.5, -1.0, -2.0, -1.5], [-2.0, -1.0, -0.5, -1.0]], 0.5], [[[-1.0, -2.0, -3.0, -2.0], [-1.0, -2.0, -3.0, -2.0]], 1.0]], "Average the per-pair loss."),
  ORDER("Deriving DPO", "Order the argument.", ["Start from the KL-regularised objective", "Write its optimal policy", "Solve that formula for the reward", "Put the reward into Bradley-Terry so log Z cancels", "Fit the policy by maximum likelihood"]),
  MATCH("Pieces", "Match each piece with its role.", [("log Z", "Cancels in the gap"), ("Implicit reward", "Beta times log ratio"), ("Margin", "Winner minus loser reward"), ("Bradley-Terry", "Preference model"), ("Policy", "Also the reward model")]),
  FILL("Derivation", "The partition function {{cancels|drops out}} because both responses answer the same {{prompt}}.")]))

CHS.append(CH(
 "The gradient: who gets updated and how much",
 ("Gradient", [
  "Gradient | raises | Winner log-prob",
  "Gradient | lowers | Loser log-prob",
  "Weight | is | Sigmoid of the wrong ordering",
  "Wrong pair | gets | Large weight",
  "Right pair | gets | Small weight",
  "Beta | scales | The gradient",
  "Naive unlikelihood | lacks | The weight"]),
 ["Differentiating the DPO loss gives a clean result. For each pair, increase the log-probability of the winner and decrease that of the loser, and scale the step by a weight. The weight is the sigmoid of the negative margin: large when the implicit reward model ranks the pair wrongly, small when it is already right.",
  "This dynamic weighting is important. The paper reports that a naive version without it, which simply pushes winners up and losers down, can cause the model to degenerate.",
  "The labs compute the weight, the gradient with respect to log-probabilities and one update step on a small table-based policy."],
 [("Gradient weight", "sigma(r_hat_l - r_hat_w): how wrongly the implicit reward orders the pair."),
  ("Log-probability gradient", "The direction that raises or lowers log pi_theta of a response."),
  ("Implicit ranking error", "A pair where the loser has the higher implicit reward."),
  ("Degeneration", "Output quality collapsing when the loss lacks the weighting."),
  ("Tabular policy", "A policy stored as a table of logits, used in the labs."),
  ("Learning rate", "The size of each gradient step.")],
 ["grad L = -beta * w * (grad log pi(y_w) - grad log pi(y_l)), averaged over pairs.",
  "w = sigmoid(r_hat(y_l) - r_hat(y_w)) = 1 - sigmoid(margin).",
  "When the margin is large and positive, w is near 0: the pair is already satisfied.",
  "When the margin is negative, w approaches 1: a strong update.",
  "Scaling by beta means larger beta takes larger steps in log-probability, for the same learning rate.",
  "The paper notes the importance of the weight in avoiding degeneration."],
 [T("What does a step of DPO do? Differentiate the loss with respect to the policy parameters. The result has a pleasingly interpretable form. It increases the log-probability of the chosen response, it decreases the log-probability of the rejected one, and it multiplies this by a weight."),
  M(r"\nabla_\theta \mathcal{L}_{\mathrm{DPO}} \;=\; -\beta\ \mathbb{E}\Bigl[\ \underbrace{\sigma\bigl(\hat r_\theta(x,y_l) - \hat r_\theta(x,y_w)\bigr)}_{\text{weight}}\ \bigl(\nabla_\theta\log\pi_\theta(y_w\mid x) - \nabla_\theta\log\pi_\theta(y_l\mid x)\bigr)\Bigr]"),
  T("The weight is the interesting part. It equals the sigmoid of the amount by which the implicit reward model gets the pair wrong. If the model already rates the winner far above the loser, the weight is near zero and the example barely matters. If the model has the pair backwards, the weight is near one and the example pushes hard."),
  T("This focus on mistakes is why DPO behaves sensibly. Easy pairs stop contributing once learned, so training effort goes where the model disagrees with the labels. The paper also points out that a simpler objective, which just raises winners and lowers losers without this weighting, can make the model degenerate, as nothing stops it from lowering probabilities without limit."),
  T("The gradient also shows what beta does. It multiplies the whole expression, and it appears inside the weight through the implicit rewards. A large beta makes the implicit reward gaps large for a given change in log-probabilities, so the weights fall to zero sooner: the policy stays near the reference. A small beta lets the policy move farther before the pair counts as satisfied."),
  T("The labs use a tabular policy, with one logit per response, to see these effects without a neural network. For a softmax over a few candidate responses, the gradient of the log-probability with respect to the logits is the one-hot vector minus the probabilities, as you saw in the PPO course.")],
 [("What does the DPO gradient do to the winner?", ["Raises its log-probability", "Lowers it", "Ignores it", "Doubles the reward"], 0, "And lowers the loser's."),
  ("When is the weight large?", ["When the pair is ranked wrongly", "When the pair is ranked rightly", "When beta is zero", "At the start only"], 0, "sigmoid of the negative margin."),
  ("What happens to easy pairs?", ["They contribute little", "They dominate", "They are removed", "They flip"], 0, "Weight near zero."),
  ("Why keep the weight?", ["It prevents degeneration", "It saves memory", "It speeds up reading", "It is optional with no effect"], 0, "As reported by the paper.")],
 [("What is w?", "sigmoid of the negative margin."), ("Bigger beta means?", "Stay closer to the reference."), ("What is updated?", "Winner up, loser down."), ("What are the labs' policy tables?", "One logit per response.")],
 [PL("Gradient weight", "Write dpo_weight(margin): sigmoid(-margin), rounded to 9 decimals. Use import math.",
     "dpo_weight(margin)", """
import math
def dpo_weight(margin):
    return round(1.0 / (1.0 + math.exp(margin)), 9)
""", [[0.0], [2.0], [-2.0], [10.0], [-10.0]], "Close to 1 for wrong orderings.", approx=1e-9),
  PL("Logit gradient for one pair", "A tabular policy over k candidate responses has logits theta. For a pair (winner index w, loser index l) the gradient of the loss with respect to theta is -beta * weight * ((onehot(w) - p) - (onehot(l) - p)) = -beta * weight * (onehot(w) - onehot(l)), where p is unaffected. Write pair_grad(k, w, l, beta, weight): that list of length k, each rounded to 9 decimals.",
     "pair_grad(k, w, l, beta, weight)", """
def pair_grad(k, w, l, beta, weight):
    g = [0.0] * k
    g[w] = -beta * weight
    g[l] = beta * weight
    return [round(x, 9) for x in g]
""", [[3, 0, 1, 0.1, 0.5], [2, 1, 0, 1.0, 1.0], [4, 3, 0, 0.5, 0.25], [3, 2, 1, 0.2, 0.0]], "Minus beta weight on the winner, plus on the loser.", approx=1e-9),
  PL("One DPO step on a tabular policy", "A policy over k responses is softmax(theta); the reference is softmax(theta_ref). Write dpo_step(theta, theta_ref, pairs, beta, lr): for each pair [w, l] compute log pi and log pi_ref (log of the softmax probabilities), margin = beta*((lp_w - ref_w) - (lp_l - ref_l)), weight = sigmoid(-margin); the gradient of the loss with respect to the logits uses the full softmax gradients: -beta*weight*((onehot(w)-p) - (onehot(l)-p)) = -beta*weight*(onehot(w)-onehot(l)). Average over the pairs and return theta minus lr times that average, rounded to 6 decimals. Use import math.",
     "dpo_step(theta, theta_ref, pairs, beta, lr)", """
import math
def dpo_step(theta, theta_ref, pairs, beta, lr):
    def logsm(t):
        m = max(t)
        s = sum(math.exp(x - m) for x in t)
        return [x - m - math.log(s) for x in t]
    lp = logsm(theta)
    lr_ref = logsm(theta_ref)
    k = len(theta)
    g = [0.0] * k
    for w, l in pairs:
        margin = beta * ((lp[w] - lr_ref[w]) - (lp[l] - lr_ref[l]))
        weight = 1.0 / (1.0 + math.exp(margin))
        g[w] += -beta * weight
        g[l] += beta * weight
    n = len(pairs)
    return [round(theta[i] - lr * g[i] / n, 6) for i in range(k)]
""", [[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [[0, 1]], 0.1, 1.0], [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [[0, 1], [0, 2]], 0.5, 0.5], [[1.0, 0.0], [0.0, 0.0], [[0, 1]], 1.0, 0.5], [[0.0, 1.0], [0.0, 0.0], [[0, 1]], 1.0, 0.5]], "Raise the winner's logit, lower the loser's, weighted."),
  ORDER("One update", "Order the steps for one pair.", ["Compute log-probabilities under policy and reference", "Form the implicit reward margin", "Compute the weight sigmoid(-margin)", "Raise the winner and lower the loser by that weight", "Take a gradient step"]),
  MATCH("Gradient", "Match each item with its meaning.", [("Weight near 1", "Pair ranked wrongly"), ("Weight near 0", "Pair already satisfied"), ("Winner", "Log-prob pushed up"), ("Loser", "Log-prob pushed down"), ("Large beta", "Stay near reference")]),
  FILL("Weights", "Pairs the model ranks {{wrongly|incorrectly}} get a {{large|big|high}} weight.")]))

CHS.append(CH(
 "Implementing DPO: sequences, batches and practicalities",
 ("Implementation", [
  "Response log-prob | sums | Token log-probs",
  "Reference log-probs | can be | Precomputed",
  "Prompt tokens | are | Masked out",
  "Batch | holds | Chosen and rejected",
  "Beta | typically | 0.1",
  "Learning rate | is | Small",
  "SFT first | is | Usual"]),
 ["A response is a sequence of tokens. Its log-probability is the sum of the log-probabilities of its tokens given the prompt and the earlier tokens. DPO needs this sum for the chosen and the rejected response under both the policy and the reference.",
  "Prompt tokens must be masked, so that only response tokens contribute. Reference log-probabilities do not change, so they can be computed once and stored.",
  "In the paper's experiments beta of 0.1 was a typical value. Learning rates are small, since the policy starts near the reference. A supervised fine-tuning stage usually comes first."],
 [("Sequence log-probability", "The sum over response tokens of log pi(token | context)."),
  ("Masking", "Excluding prompt (and padding) tokens from the sum."),
  ("Precomputing", "Calculating reference log-probabilities once before training."),
  ("SFT", "Supervised fine-tuning, usually done before DPO."),
  ("Beta", "A typical value is 0.1; chosen by experiment."),
  ("Length bias", "A tendency for sums of log-probabilities to favour shorter or longer responses.")],
 ["log pi(y|x) = sum over response tokens of log pi(y_t | x, y_<t).",
  "Only response tokens count; prompt and padding are masked.",
  "Reference log-probabilities can be precomputed once.",
  "Common beta about 0.1 (the paper explores 0.1 to 0.5 in places); tuned per task.",
  "DPO usually starts from a supervised fine-tuned model that also serves as the reference.",
  "Longer responses have lower total log-probability, which can interact with the loss."],
 [T("So far we treated a response as a single item with a probability. A real response is a sequence of tokens. By the chain rule of probability, the probability of the whole response is the product of the token probabilities, each conditioned on the prompt and the tokens before. Taking logs turns the product into a sum."),
  M(r"\log \pi_\theta(y\mid x) \;=\; \sum_{t=1}^{|y|}\ \log \pi_\theta\bigl(y_t \mid x,\, y_{<t}\bigr)"),
  T("In code, run the model on the concatenated prompt and response once. It outputs a distribution over the vocabulary at each position. Pick out the log-probability of the actual next token at each response position. Mask out the prompt positions, since the prompt is given, not generated, and padding positions. Sum what remains."),
  T("Each training step needs four such sums: the policy and the reference, for the chosen and the rejected response. The reference model is frozen, so its sums never change. A common saving is to compute them once before training and store them with the data, so the reference need not be in memory during the updates."),
  T("Practical advice from the paper and common implementations: begin from a model already fine-tuned on good responses, and use that same model as the reference. Use a small learning rate, since a large one will quickly leave the neighbourhood where the reference is a sensible anchor. Beta of 0.1 is a common starting value. Larger values keep the model closer."),
  T("One known subtlety is length. A longer response has a more negative total log-probability simply because it has more tokens, so the log-ratios can interact with length. Several later methods normalise by length. I come back to this in the chapter on variants. The labs compute sequence log-probabilities with masks and build one batch of DPO inputs.")],
 [("How is a response log-probability computed?", ["Sum of token log-probs", "Product of logits", "Mean of rewards", "Max token"], 0, "Chain rule in logs."),
  ("Why mask prompt tokens?", ["The prompt is given, not generated", "To save time", "To add noise", "To change beta"], 0, "Only response tokens count."),
  ("Why precompute reference log-probs?", ["The reference is frozen", "It is faster to read", "Beta is fixed", "It improves accuracy"], 0, "Saves memory."),
  ("What typical beta is used?", ["About 0.1", "About 100", "Exactly 0", "About 10,000"], 0, "Tuned per task.")],
 [("What model is the usual reference?", "The SFT model."), ("How many log-prob sums per pair?", "Four."), ("Why a small learning rate?", "Stay near the reference."), ("What is length bias?", "Totals favour short responses.")],
 [PL("Sequence log-probability", "Write seq_logprob(token_logps, mask): the sum of token_logps[i] where mask[i] is 1 (response tokens), rounded to 9 decimals.",
     "seq_logprob(token_logps, mask)", """
def seq_logprob(token_logps, mask):
    s = 0.0
    for lp, m in zip(token_logps, mask):
        if m == 1:
            s += lp
    return round(s, 9)
""", [[[-1.0, -2.0, -0.5], [0, 1, 1]], [[-1.0, -1.0], [1, 1]], [[-3.0, -0.1, -0.2, -5.0], [0, 0, 1, 0]], [[-1.0], [0]]], "Skip masked positions.", approx=1e-9),
  PL("Response mask", "Write response_mask(prompt_len, total_len, pad_from): a list of length total_len with 1 for positions from prompt_len up to (not including) pad_from, 0 elsewhere.",
     "response_mask(prompt_len, total_len, pad_from)", """
def response_mask(prompt_len, total_len, pad_from):
    return [1 if (i >= prompt_len and i < pad_from) else 0 for i in range(total_len)]
""", [[2, 6, 5], [0, 3, 3], [3, 5, 5], [2, 4, 2]], "Between the prompt and the padding."),
  PL("Build a DPO input", "Write dpo_inputs(chosen_lp, chosen_ref_lp, rejected_lp, rejected_ref_lp, chosen_mask, rejected_mask): return [lw, lw_ref, ll, ll_ref], each the masked sum of the token log-probs, rounded to 9 decimals.",
     "dpo_inputs(chosen_lp, chosen_ref_lp, rejected_lp, rejected_ref_lp, chosen_mask, rejected_mask)", """
def dpo_inputs(chosen_lp, chosen_ref_lp, rejected_lp, rejected_ref_lp, chosen_mask, rejected_mask):
    def msum(a, m):
        s = 0.0
        for x, k in zip(a, m):
            if k == 1:
                s += x
        return round(s, 9)
    return [msum(chosen_lp, chosen_mask), msum(chosen_ref_lp, chosen_mask), msum(rejected_lp, rejected_mask), msum(rejected_ref_lp, rejected_mask)]
""", [[[-1.0, -1.0], [-1.1, -1.1], [-2.0, -2.0], [-1.9, -1.9], [1, 1], [1, 1]], [[-1.0, -2.0], [-1.0, -2.0], [-0.5, -0.5, -0.5], [-0.6, -0.6, -0.6], [0, 1], [1, 1, 0]], [[-0.1], [-0.2], [-0.3], [-0.4], [1], [1]]], "Four masked sums."),
  PL("Per-token length normalisation", "Write avg_logprob(token_logps, mask): the masked sum divided by the number of unmasked tokens (0 if none), rounded to 9 decimals.",
     "avg_logprob(token_logps, mask)", """
def avg_logprob(token_logps, mask):
    s = 0.0
    n = 0
    for lp, m in zip(token_logps, mask):
        if m == 1:
            s += lp
            n += 1
    if n == 0:
        return 0
    return round(s / n, 9)
""", [[[-1.0, -2.0, -3.0], [1, 1, 1]], [[-1.0, -2.0, -3.0], [0, 1, 1]], [[-1.0], [0]], [[-0.5, -0.5], [1, 1]]], "Divide by the count.", approx=1e-9),
  ORDER("Preparing training data", "Order the steps.", ["Fine-tune a supervised model and keep a frozen copy", "Tokenise prompt plus chosen and rejected responses", "Build masks that cover only response tokens", "Precompute reference log-probabilities", "Train the policy with the DPO loss"]),
  MATCH("Details", "Match each detail with its reason.", [("Mask the prompt", "Only generated tokens count"), ("Precompute reference", "Frozen, saves memory"), ("SFT first", "Good starting point"), ("Small learning rate", "Stay near reference"), ("Length normalisation", "Reduce length bias")]),
  FILL("Code", "A response log-probability is the {{sum}} of token log-probabilities over the {{response|generated}} tokens.")]))

CHS.append(CH(
 "Choosing beta and understanding behaviour",
 ("Behaviour", [
  "Beta | trades | Reward for closeness",
  "Likelihood displacement | lowers | Chosen probability",
  "Overfitting | memorises | Pairs",
  "Reference quality | limits | Results",
  "Data quality | decides | Alignment",
  "Off-policy data | can mismatch | The reference",
  "Evaluation | compares | Win rates"]),
 ["Beta is the most important knob. Small beta lets the policy move far from the reference, which can give larger gains and more risk. Large beta keeps it close. The right value depends on the data and the model.",
  "DPO is trained offline on a fixed set of pairs. If the responses came from another model, the reference may give them very low probability. Many practitioners therefore fine-tune on the preferred responses first.",
  "A reported effect, sometimes called likelihood displacement, is that DPO can lower the probability of both the chosen and the rejected response, so long as the gap grows. This is background knowledge from later analyses."],
 [("Likelihood displacement", "Chosen and rejected log-probabilities both fall while their gap grows."),
  ("Offline training", "Learning from a fixed dataset without sampling new responses."),
  ("Distribution shift", "Mismatch between the data and what the model would generate."),
  ("Win rate", "The share of comparisons in which one model's response is preferred."),
  ("Overfitting", "Fitting the training pairs too closely; the margin keeps growing."),
  ("Reward accuracy", "The share of pairs with a positive implicit reward margin.")],
 ["Larger beta keeps the policy closer to the reference.",
  "Training on pairs not generated by the reference can cause distribution shift.",
  "Margins can grow without bound; with noisy labels this overfits.",
  "Both chosen and rejected log-probs may decline (later analyses; background).",
  "Track: loss, reward accuracy, margin, chosen/rejected rewards, KL to reference.",
  "Final evaluation uses held-out prompts and win rates against a baseline."],
 [T("Consider the roles of beta again. In the loss, beta multiplies the log-ratio. In the optimal policy it sets the temperature of the reward tilt. A small beta says: I trust the preference data, and I let the policy drift. A large beta says: stay close. The paper's experiments use values such as 0.1 and compare behaviour as the KL to the reference grows."),
  M(r"\hat r_\theta(x,y) \;=\; \beta \log\frac{\pi_\theta(y\mid x)}{\pi_{\mathrm{ref}}(y\mid x)}"),
  T("DPO trains offline on a fixed dataset, so the data matters a great deal. Suppose the responses came from a very different model. Then under the reference both may be very unlikely, and the log-ratios behave strangely. A common remedy, noted in the paper, is to first fine-tune the reference on the preferred responses."),
  T("A further effect has been described in later analyses. The loss only cares about the gap between chosen and rejected. It can be reduced by lowering the rejected probability a lot while lowering the chosen one a little. So both probabilities can fall. Some observers call this likelihood displacement. Variants add a term that keeps the chosen likelihood up. I mark this as background knowledge, not a result of the original paper."),
  T("Overfitting is another risk. With a clean dataset the margin can be increased without limit by driving the loser's probability toward zero. With noisy labels this memorises noise. Early stopping, a larger beta, a smaller learning rate or label smoothing can all help."),
  T("To monitor training, log the loss, the reward accuracy, the average margin, the implicit rewards of the chosen and rejected responses, and an estimate of the KL divergence to the reference. For the final judgement use held-out prompts and compare responses against a baseline, by human raters or by a model judge, and report the win rate.")],
 [("What does a larger beta do?", ["Keeps the policy closer to the reference", "Lets it drift", "Removes the reference", "Changes the data"], 0, "Smaller steps in log-ratio terms."),
  ("What is reward accuracy?", ["Share of pairs with positive margin", "Reward model size", "Win rate", "Loss"], 0, "A training diagnostic."),
  ("Why SFT on preferred responses first?", ["So they are likely under the reference", "To save memory", "To remove beta", "To shorten prompts"], 0, "Reduces distribution shift."),
  ("What is likelihood displacement?", ["Both chosen and rejected probabilities fall", "Only rejected rises", "Loss goes up", "Beta changes"], 0, "Later analysis, background.")],
 [("What is the final metric?", "Win rate on held-out prompts."), ("What is offline training?", "Fixed dataset, no new samples."), ("How to curb overfitting?", "Early stop, larger beta, smaller lr."), ("What to log?", "Loss, accuracy, margin, KL.")],
 [PL("Optimal policy for a given beta", "With two responses, reference probabilities p_ref = [0.5, 0.5] and rewards [1.0, 0.0], write prob_best(beta): the optimal policy's probability on the first response, rounded to 9 decimals. Use import math.",
     "prob_best(beta)", """
import math
def prob_best(beta):
    a = 0.5 * math.exp(1.0 / beta)
    b = 0.5
    return round(a / (a + b), 9)
""", [[0.1], [0.5], [1.0], [10.0], [100.0]], "A two-way tilt.", approx=1e-9),
  PL("Diagnostics", "Write diagnostics(margins, chosen_rewards, rejected_rewards): return [reward accuracy (fraction of margins above 0), mean margin, mean chosen reward, mean rejected reward], each rounded to 9 decimals.",
     "diagnostics(margins, chosen_rewards, rejected_rewards)", """
def diagnostics(margins, chosen_rewards, rejected_rewards):
    n = len(margins)
    acc = sum(1 for m in margins if m > 0) / n
    return [round(acc, 9), round(sum(margins) / n, 9), round(sum(chosen_rewards) / n, 9), round(sum(rejected_rewards) / n, 9)]
""", [[[0.5, -0.2, 1.0], [0.2, 0.1, 0.4], [-0.3, 0.3, -0.6]], [[1.0, 1.0], [0.5, 0.5], [-0.5, -0.5]], [[-1.0], [-0.5], [0.5]]], "Four summary numbers."),
  PL("Displacement check", "Write displaced(chosen_before, chosen_after, rejected_before, rejected_after): True if the chosen log-prob fell AND the gap (chosen minus rejected) grew.",
     "displaced(chosen_before, chosen_after, rejected_before, rejected_after)", """
def displaced(chosen_before, chosen_after, rejected_before, rejected_after):
    gap_before = chosen_before - rejected_before
    gap_after = chosen_after - rejected_after
    return chosen_after < chosen_before and gap_after > gap_before
""", [[-1.0, -1.5, -2.0, -4.0], [-1.0, -0.5, -2.0, -3.0], [-1.0, -1.5, -2.0, -2.0], [-1.0, -1.0, -2.0, -3.0]], "Two conditions."),
  PL("Win rate", "Write win_rate(outcomes): outcomes is a list of 'win', 'loss' or 'tie'; return (wins + 0.5 * ties) / games, or 0 for an empty list.",
     "win_rate(outcomes)", """
def win_rate(outcomes):
    if len(outcomes) == 0:
        return 0
    s = 0.0
    for o in outcomes:
        if o == 'win':
            s += 1
        elif o == 'tie':
            s += 0.5
    return s / len(outcomes)
""", [[['win', 'loss', 'tie', 'win']], [[]], [['loss', 'loss']], [['tie', 'tie']]], "Ties count half.", approx=1e-12),
  ORDER("Tuning DPO", "Order a sensible routine.", ["Fine-tune on preferred responses", "Train with beta 0.1", "Watch reward accuracy and KL", "Adjust beta or the learning rate", "Evaluate win rate on held-out prompts"]),
  MATCH("Effects", "Match each setting with its likely effect.", [("Large beta", "Policy stays close"), ("Small beta", "Policy drifts far"), ("Noisy labels", "Overfitting risk"), ("Off-policy pairs", "Distribution shift"), ("Held-out prompts", "Honest evaluation")]),
  FILL("Tuning", "A larger {{beta}} keeps the policy {{closer|close|near}} to the reference.")]))

CHS.append(CH(
 "Variants, relatives and where DPO fits",
 ("Family", [
  "IPO | changes | The loss shape",
  "KTO | uses | Single-response labels",
  "ORPO | drops | The reference model",
  "SimPO | uses | Length-normalised reward",
  "GRPO | uses | Group advantages",
  "PPO | is | The RL alternative",
  "Online DPO | samples | Fresh responses"]),
 ["DPO started a family. IPO modifies the loss to avoid overfitting. KTO works with thumbs-up or thumbs-down labels on single responses. ORPO combines supervised fine-tuning and preference learning without a reference model. SimPO uses length-normalised log-probabilities. Online versions sample fresh responses during training. GRPO keeps the reinforcement learning loop but replaces the value model by group statistics.",
  "All of these are later work and are background knowledge in this course. Details differ and evidence about which is best is mixed; treat comparisons with some care.",
  "The labs implement small versions of three of these ideas."],
 [("IPO", "Identity Preference Optimization: squared-error loss on the margin, aimed at reducing overfitting."),
  ("KTO", "Kahneman-Tversky Optimization: learns from labels on single responses."),
  ("ORPO", "Odds Ratio Preference Optimization: no reference model."),
  ("SimPO", "Simple Preference Optimization: average log-probability as the reward."),
  ("Online DPO", "DPO with fresh samples from the current policy, labelled by a judge."),
  ("GRPO", "Group Relative Policy Optimization: PPO-like with group-normalised advantages.")],
 ["IPO: loss = (margin_in_logratio - 1/(2 tau))^2 style regression to a target gap.",
  "SimPO: reward = beta / |y| * log pi(y|x), with a target margin gamma.",
  "KTO: needs only 'good' or 'bad' labels per response.",
  "ORPO: adds an odds-ratio penalty to the SFT loss; no reference model.",
  "Online methods reduce distribution shift by sampling from the current policy.",
  "These variants are later than the DPO paper; evidence on which is best is mixed."],
 [T("DPO's simplicity made it popular, and its limits prompted many variants. Here is a map, with the usual warning that this is the fast-moving part of the field."),
  T("IPO changes the loss from log-sigmoid to a squared error pushing the margin toward a fixed target. The aim is to stop the margin from growing without limit when labels are very consistent, which curbs overfitting. KTO is designed for data where you only have thumbs-up or thumbs-down on single responses rather than pairs. ORPO folds preference learning into supervised fine-tuning with an odds-ratio term, and does not need a reference model, saving memory. SimPO scores a response by its average, not total, log-probability, which treats length more evenly."),
  M(r"\text{SimPO reward: } \ r(x,y) = \frac{\beta}{|y|}\log \pi_\theta(y\mid x), \qquad \text{loss} = -\log\sigma\bigl(r(x,y_w) - r(x,y_l) - \gamma\bigr)"),
  T("A different line addresses the offline nature of DPO. Online or iterative DPO samples new responses from the current policy, has a judge rank them, trains on the new pairs, and repeats. This removes the distribution shift, but brings back a sampling loop, which was what DPO aimed to avoid. Seen this way, PPO-style RLHF and DPO sit at two ends of a spectrum."),
  T("GRPO keeps online reinforcement learning but drops the value model: for each prompt it samples a group of responses, and the advantage of each is its reward minus the group mean, divided by the group standard deviation. It has been popular for reasoning models trained with verifiable rewards."),
  T("How to choose? DPO is a strong default when you have a good preference dataset and limited compute. PPO-like methods give more control when you have a reliable reward signal and can afford sampling. Whatever you pick, evaluate on held-out prompts. Where to go next: read the DPO paper, then try the loss on a small open model with a preference dataset, and plot the diagnostics from chapter 7.")],
 [("Which variant needs no reference model?", ["ORPO", "DPO", "IPO", "PPO"], 0, "It adds an odds-ratio term to SFT."),
  ("What does KTO use?", ["Single-response good or bad labels", "Pairs only", "A reward model", "A tree"], 0, "Not pairs."),
  ("What does SimPO normalise by?", ["Response length", "Beta", "The reference", "The batch"], 0, "Average log-probability."),
  ("What does online DPO fix?", ["Distribution shift from offline data", "Memory use", "Tokenization", "The learning rate"], 0, "By sampling from the current policy.")],
 [("Are variants in the original paper?", "No, they are later work."), ("What does GRPO drop?", "The value model."), ("DPO or PPO default?", "DPO with a good dataset and limited compute."), ("What is IPO's aim?", "Reduce overfitting.")],
 [PL("IPO-style loss", "Write ipo_loss(margin_logratio, tau): the squared error (margin_logratio - 1 / (2 * tau)) ** 2, where margin_logratio is the winner minus loser log-ratio (without beta). Round to 9 decimals.",
     "ipo_loss(margin_logratio, tau)", """
def ipo_loss(margin_logratio, tau):
    return round((margin_logratio - 1.0 / (2.0 * tau)) ** 2, 9)
""", [[0.0, 0.1], [5.0, 0.1], [10.0, 0.1], [1.0, 0.5]], "Regress the gap to a target.", approx=1e-9),
  PL("SimPO reward", "Write simpo_reward(logp_sum, length, beta): beta * logp_sum / length, rounded to 9 decimals.",
     "simpo_reward(logp_sum, length, beta)", """
def simpo_reward(logp_sum, length, beta):
    return round(beta * logp_sum / length, 9)
""", [[-10.0, 10, 2.0], [-30.0, 20, 2.0], [-5.0, 5, 1.0], [-1.0, 2, 0.5]], "Length-normalised.", approx=1e-9),
  PL("SimPO loss", "Write simpo_loss(lp_w, len_w, lp_l, len_l, beta, gamma): -ln sigmoid(reward_w - reward_l - gamma) using the SimPO reward, rounded to 9 decimals. Use import math.",
     "simpo_loss(lp_w, len_w, lp_l, len_l, beta, gamma)", """
import math
def simpo_loss(lp_w, len_w, lp_l, len_l, beta, gamma):
    m = beta * lp_w / len_w - beta * lp_l / len_l - gamma
    return round(-math.log(1.0 / (1.0 + math.exp(-m))), 9)
""", [[-10.0, 10, -20.0, 10, 2.0, 0.5], [-10.0, 10, -10.0, 10, 2.0, 0.0], [-30.0, 20, -20.0, 20, 2.0, 0.5], [-5.0, 5, -10.0, 10, 1.0, 0.0]], "Normalise before comparing."),
  PL("Group advantages", "Write group_advantages(rewards): the GRPO-style advantage of each sampled response, (reward - mean) / (std + 1e-8) with population std, rounded to 6 decimals. Use import math.",
     "group_advantages(rewards)", """
import math
def group_advantages(rewards):
    n = len(rewards)
    mu = sum(rewards) / n
    var = sum((r - mu) ** 2 for r in rewards) / n
    s = math.sqrt(var)
    return [round((r - mu) / (s + 1e-8), 6) for r in rewards]
""", [[[1.0, 0.0, 0.0, 1.0]], [[1.0, 1.0, 1.0]], [[0.0, 1.0]], [[0.1, 0.5, 0.9, 0.3]]], "Normalise within the group."),
  ORDER("Online preference learning", "Order the loop.", ["Sample several responses from the current policy", "Have a judge rank them", "Form preference pairs", "Update the policy with a preference loss", "Repeat with the improved policy"]),
  MATCH("Relatives", "Match each method with its feature.", [("IPO", "Squared-error margin target"), ("KTO", "Single-response labels"), ("ORPO", "No reference model"), ("SimPO", "Length-normalised reward"), ("GRPO", "Group-relative advantages")]),
  FILL("Family", "{{GRPO}} drops the value model; {{online|iterative}} DPO samples new responses.")]))
