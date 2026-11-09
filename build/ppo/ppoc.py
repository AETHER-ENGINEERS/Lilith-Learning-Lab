"""Proximal Policy Optimization course."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "From policy gradients to PPO",
 ("PPO", [
  "PPO | is | A policy gradient method",
  "PPO | introduced by | Schulman et al. 2017",
  "PPO | simplifies | TRPO",
  "Clipping | limits | Policy change",
  "PPO | reuses | Data for several epochs",
  "PPO | is | On-policy",
  "PPO | trains | RLHF language models"]),
 ["Proximal Policy Optimization, PPO, is a reinforcement learning algorithm from John Schulman and colleagues at OpenAI, 2017. It improves a policy by gradient ascent, but with a trick that stops each update from changing the policy too much.",
  "Plain policy gradient methods can ruin a policy with one oversized step. TRPO prevented this with a constraint but was complicated. PPO gets much of the benefit with a simple clipped objective that works with ordinary first-order optimizers.",
  "This course builds PPO piece by piece in small Python labs: returns, advantages, the ratio, clipping, the loss, the update loop and its use for language models."],
 [("Policy", "A rule giving the probability of each action in a state."),
  ("Policy gradient", "Improving the policy by gradient ascent on expected return."),
  ("TRPO", "Trust Region Policy Optimization: a constrained policy update using a KL limit."),
  ("Surrogate objective", "A stand-in objective whose gradient guides the policy update."),
  ("On-policy", "Learning from data collected by the current policy."),
  ("Epoch", "One pass over the collected batch.")],
 ["PPO: Schulman, Wolski, Dhariwal, Radford and Klimov, 2017.",
  "It keeps the new policy close to the old one by clipping the probability ratio.",
  "It is simpler than TRPO: no second-order optimisation, no explicit constraint.",
  "It reuses each batch for several epochs of minibatch updates.",
  "It is on-policy: after updating, fresh data is collected.",
  "It became a default choice for many RL problems and for RLHF fine-tuning of language models (background knowledge)."],
 [T("Reinforcement learning teaches an agent by reward. In policy gradient methods, the agent's behaviour is a neural network that outputs action probabilities, and we adjust its weights to make rewarding actions more likely. The simple version is the algorithm called REINFORCE."),
  T("There is a catch. A policy gradient estimate is noisy, and the policy changes the data it will see next. A step that is too large can send the policy to a bad region from which it never recovers, because the next batch of data is collected by the broken policy. Small steps are safe but slow. The art is to take the biggest safe step."),
  M(r"\theta_{k+1} \;=\; \arg\max_{\theta}\ \ \mathbb{E}\left[\, L^{\mathrm{CLIP}}(\theta) \,\right]\ \ \text{subject to staying near } \theta_k"),
  T("TRPO, by Schulman and colleagues in 2015, made this idea precise. It maximised a surrogate objective subject to a limit on the KL divergence between old and new policies. It worked well but needed second-order optimisation and was awkward with shared networks and with noise sources such as dropout."),
  T("PPO, in the 2017 paper, replaces the constraint by a clipped objective. It computes the ratio of new to old action probabilities and cuts off the incentive to move the ratio outside a small band around one. A first-order optimiser such as Adam can then take many gradient steps on the same batch. The paper reports that the clipped version performed best among the variants tried, which included an adaptive KL penalty."),
  T("PPO is on-policy. After a round of updates the old data is thrown away and new data is collected with the improved policy. It later became very widely used, including for fine-tuning language models from human feedback, which chapter 9 covers as background knowledge.")],
 [("Who introduced PPO?", ["Schulman and colleagues at OpenAI", "Mnih et al.", "Silver et al.", "Vaswani et al."], 0, "2017."),
  ("What does PPO simplify?", ["TRPO", "DQN", "A3C", "AlphaGo"], 0, "No constraint or second-order step."),
  ("What does clipping do?", ["Limits how far the policy moves", "Adds noise", "Speeds up rewards", "Removes the critic"], 0, "Via the probability ratio."),
  ("Is PPO on-policy?", ["Yes", "No", "Only for Atari", "Only offline"], 0, "Fresh data after each round.")],
 [("What is the gradient step problem?", "Too large a step can wreck the policy."), ("Who proposed TRPO?", "Schulman and colleagues, 2015."), ("What optimiser does PPO use?", "A first-order one such as Adam."), ("What is the key idea?", "Clip the probability ratio.")],
 [ORDER("A PPO round", "Put the steps in order.", ["Collect experience with the current policy", "Compute returns and advantages", "Run several epochs of minibatch updates with the clipped objective", "Discard the old data", "Collect new experience"]),
  MATCH("Names", "Match each name with its description.", [("REINFORCE", "Basic policy gradient"), ("TRPO", "KL-constrained update"), ("PPO", "Clipped surrogate update"), ("Surrogate objective", "Objective used for the update"), ("On-policy", "Fresh data from the current policy")]),
  FILL("Idea", "PPO keeps the new policy {{close|near}} to the old one by {{clipping|clip}} the probability ratio.")]))

CHS.append(CH(
 "Policy gradient recap",
 ("Policy gradient", [
  "Return | sums | Discounted rewards",
  "Log-probability | scores | An action",
  "Gradient | raises | Good actions",
  "Baseline | reduces | Variance",
  "Softmax policy | maps | Logits to probabilities",
  "Score function | is | Gradient of log pi",
  "Batch | averages | Many samples"]),
 ["A policy gradient step increases the log-probability of actions in proportion to how good they turned out to be. The measure of goodness is the return, or better, the return minus a baseline.",
  "For a softmax policy over discrete actions the gradient of the log-probability with respect to the logits has a simple form: the one-hot vector of the chosen action minus the probability vector.",
  "The labs compute discounted returns, the softmax, the log-probability gradient and a policy gradient update on a small bandit."],
 [("Return", "The discounted sum of future rewards, G_t."),
  ("Discount factor gamma", "A number below one that makes later rewards count less."),
  ("Softmax policy", "pi(a) = exp(theta_a) / sum_b exp(theta_b)."),
  ("Score function", "The gradient of the log-probability of an action."),
  ("Baseline", "A number subtracted from the return to reduce variance without bias."),
  ("Logits", "The raw scores before the softmax.")],
 ["G_t = r_t + gamma r_{t+1} + gamma^2 r_{t+2} + ...",
  "Policy gradient: grad J = E[ grad log pi(a|s) * (G - b) ].",
  "For a softmax policy: d log pi(a) / d theta = onehot(a) - pi.",
  "A baseline that depends only on the state leaves the gradient unbiased.",
  "A learned value function V(s) is the usual baseline.",
  "Common gamma in practice: 0.99."],
 [T("The policy gradient theorem tells us how to improve a stochastic policy. For a sampled action in a state, nudge the parameters in the direction that makes that action more probable, and nudge more strongly the better the outcome was. In symbols, the expected gradient of the return is the expectation of the score function times the return."),
  M(r"\nabla_{\theta} J(\theta) \;=\; \mathbb{E}\Bigl[\, \nabla_{\theta} \log \pi_{\theta}(a \mid s)\,\bigl(G_t - b(s)\bigr) \Bigr]"),
  T("The return G t is the sum of the rewards from time t on, each discounted by a factor gamma for each step into the future. A gamma of 0.99 is the usual default: rewards one hundred steps away count about a third as much."),
  T("The baseline b of s is subtracted to cut variance. Without it, if all returns are positive, every sampled action is pushed up, and only the relative sizes matter; the signal is buried in noise. A baseline that depends on the state only, never on the action, leaves the expected gradient unchanged. The best-known choice is the value function, a second network trained to predict the return."),
  T("For a discrete action space, a softmax policy has parameters theta, one logit per action. The gradient of the log-probability of the chosen action a with respect to the logits is neat: a one-hot vector for a, minus the vector of probabilities. Raising the logit of a, lowering the others in proportion to how likely they were."),
  T("Everything in PPO builds on this. The next chapters improve the weight multiplying the score function (the advantage) and limit the step (the ratio and clipping).")],
 [("What does the score function equal for a softmax policy?", ["onehot(a) minus pi", "pi minus one", "The return", "Zero"], 0, "For the logits."),
  ("What does a baseline do?", ["Reduces variance", "Adds bias", "Raises rewards", "Removes the policy"], 0, "If it depends only on the state."),
  ("What is gamma?", ["The discount factor", "The learning rate", "The clip range", "The entropy weight"], 0, "Below one."),
  ("What is the return?", ["Discounted sum of future rewards", "The next reward", "The policy", "The loss"], 0, "G_t.")],
 [("Typical gamma?", "0.99."), ("What multiplies the score function?", "Return minus baseline."), ("What is a good baseline?", "The value function."), ("What are logits?", "Raw scores before the softmax.")],
 [PL("Discounted returns", "Write returns(rewards, gamma): the list of discounted returns G_t = r_t + gamma * G_{t+1} for each step (G after the last step is 0). Round each to 6 decimals.",
     "returns(rewards, gamma)", """
def returns(rewards, gamma):
    out = [0.0] * len(rewards)
    g = 0.0
    for t in range(len(rewards) - 1, -1, -1):
        g = rewards[t] + gamma * g
        out[t] = round(g, 6)
    return out
""", [[[1, 1, 1], 0.9], [[0, 0, 1], 0.99], [[1], 0.5], [[2, 0, 3], 1.0], [[], 0.9]], "Work backwards from the end."),
  PL("Softmax", "Write softmax(theta): the softmax of a list of logits (subtract the maximum first), each rounded to 9 decimals. Use import math.",
     "softmax(theta)", """
import math
def softmax(theta):
    m = max(theta)
    es = [math.exp(t - m) for t in theta]
    s = sum(es)
    return [round(e / s, 9) for e in es]
""", [[[0, 0]], [[1, 2, 3]], [[0, 0, 0, 0]], [[5, 0]]], "Stable softmax."),
  PL("Score function", "Write score(theta, a): the gradient of log softmax(theta)[a] with respect to theta, onehot(a) minus the probabilities, each rounded to 9 decimals. Use import math.",
     "score(theta, a)", """
import math
def score(theta, a):
    m = max(theta)
    es = [math.exp(t - m) for t in theta]
    s = sum(es)
    p = [e / s for e in es]
    return [round((1.0 if i == a else 0.0) - p[i], 9) for i in range(len(theta))]
""", [[[0, 0], 0], [[0, 0], 1], [[1, 2, 3], 2], [[0, 0, 0, 0], 3]], "One-hot minus probabilities."),
  PL("Policy gradient step", "A bandit has a softmax policy with logits theta. Write pg_step(theta, samples, lr): samples is a list of [action, reward]; use the mean reward as a baseline; for each sample accumulate (reward - baseline) * score and divide by the number of samples; return the new logits theta + lr * gradient, each rounded to 6 decimals. Use import math.",
     "pg_step(theta, samples, lr)", """
import math
def pg_step(theta, samples, lr):
    m = max(theta)
    es = [math.exp(t - m) for t in theta]
    s = sum(es)
    p = [e / s for e in es]
    base = sum(r for a, r in samples) / len(samples)
    g = [0.0] * len(theta)
    for a, r in samples:
        for i in range(len(theta)):
            sc = (1.0 if i == a else 0.0) - p[i]
            g[i] += (r - base) * sc
    n = len(samples)
    return [round(theta[i] + lr * g[i] / n, 6) for i in range(len(theta))]
""", [[[0, 0], [[0, 1.0], [1, 0.0], [0, 1.0], [1, 0.0]], 0.5], [[0, 0, 0], [[2, 1.0], [0, 0.0], [1, 0.0]], 1.0], [[1.0, 0.0], [[0, 0.2], [1, 0.8]], 0.1]], "Mean reward as baseline; average the weighted scores."),
  ORDER("A policy gradient step", "Order the steps.", ["Sample actions from the policy", "Observe rewards", "Compute returns and a baseline", "Weight each score function by return minus baseline", "Step the parameters upward"]),
  MATCH("Terms", "Match each term with its meaning.", [("Return", "Discounted future reward"), ("Baseline", "Variance reduction"), ("Score function", "Gradient of log probability"), ("Logits", "Raw policy scores"), ("gamma", "Discount factor")]),
  FILL("Gradient", "The gradient of the log-probability for a softmax policy is the one-hot vector minus the {{probabilities|probability vector}}. A {{baseline}} reduces variance.")]))

CHS.append(CH(
 "Advantages and generalized advantage estimation",
 ("Advantage", [
  "Advantage | is | Q minus V",
  "TD residual | estimates | One-step advantage",
  "GAE | blends | Multi-step estimates",
  "Lambda | trades | Bias for variance",
  "Value function | predicts | Return",
  "Normalisation | rescales | Advantages",
  "Bootstrapping | uses | Value of the next state"]),
 ["The advantage of an action is how much better it is than the policy's average action in that state: A(s, a) = Q(s, a) - V(s). Weighting the policy gradient by the advantage is the standard way to reduce variance.",
  "Generalized advantage estimation, GAE, by Schulman and colleagues in 2015, builds advantage estimates from a learned value function. A parameter lambda interpolates between a low-variance, biased one-step estimate and a high-variance, unbiased Monte Carlo estimate.",
  "PPO typically uses GAE, with gamma of 0.99 and lambda of 0.95 as common defaults."],
 [("Advantage", "A(s, a) = Q(s, a) - V(s): how much better than average an action is."),
  ("Value function", "V(s): the expected return from state s under the policy."),
  ("TD residual", "delta_t = r_t + gamma V(s_{t+1}) - V(s_t)."),
  ("GAE", "A_t = sum_l (gamma lambda)^l delta_{t+l}."),
  ("Bootstrapping", "Using a value estimate in place of the rest of the return."),
  ("Advantage normalisation", "Subtracting the batch mean and dividing by the standard deviation.")],
 ["delta_t = r_t + gamma V(s_{t+1}) - V(s_t).",
  "GAE: A_t = delta_t + gamma lambda A_{t+1}.",
  "lambda = 0 gives the one-step estimate (low variance, more bias).",
  "lambda = 1 gives return minus value (higher variance, low bias).",
  "Common defaults: gamma 0.99, lambda 0.95 (practice, not the only choice).",
  "Normalising advantages per minibatch is common in implementations."],
 [T("A raw return tells you how much reward followed an action, but not whether that was good. If every state yields about 100 on average, a return of 101 is nothing special. The advantage subtracts what was expected: how much better than usual was this action? Positive advantage, make it likelier. Negative, less likely."),
  M(r"A^{\pi}(s,a) \;=\; Q^{\pi}(s,a) - V^{\pi}(s)"),
  T("We do not know Q, but we can estimate the advantage from experience and a learned value function V. The simplest estimate uses one step: the reward received plus the discounted value of the next state, minus the value of this state. This is the temporal-difference residual delta. It has low variance, because it uses only one random reward, but it is biased if V is wrong."),
  M(r"\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t), \qquad \hat{A}_t = \delta_t + \gamma\lambda\,\hat{A}_{t+1}"),
  T("Using more steps trades bias for variance. Generalized advantage estimation takes an exponentially weighted sum of the residuals, controlled by lambda. With lambda equal to zero it is the one-step residual. With lambda equal to one it is the full return minus the value, which is unbiased but noisy. Values around 0.95 are the common practical compromise."),
  T("The recursion runs backwards through the trajectory, just like the discounted return. At an episode end the future value is zero, so we multiply the next-state value and the running advantage by a mask that is zero after a terminal step. The labs implement this with a done flag."),
  T("Finally, many implementations normalise the advantages in each batch: subtract the mean, divide by the standard deviation. This keeps the scale of the gradient steady between batches. It is an implementation habit, not part of the theory.")],
 [("What is the advantage?", ["Q minus V", "V minus Q", "Reward", "Return"], 0, "How much better than average."),
  ("What does lambda = 0 give in GAE?", ["The one-step TD residual", "The full return", "Zero", "The value"], 0, "Low variance, more bias."),
  ("What does lambda = 1 give?", ["Return minus value", "Only the next reward", "Zero", "The policy"], 0, "Unbiased but noisy."),
  ("Why mask at episode ends?", ["There is no future value after a terminal step", "To save time", "To normalise", "To clip"], 0, "Done flag.")],
 [("Who proposed GAE?", "Schulman and colleagues, 2015."), ("What does delta use?", "One reward and two values."), ("Why normalise advantages?", "Steady gradient scale."), ("What does lambda trade?", "Bias for variance.")],
 [PL("TD residuals", "Write td_residuals(rewards, values, gamma): values has one more entry than rewards (the bootstrap value after the last step); return delta_t = r_t + gamma * V[t+1] - V[t] for each t, rounded to 6 decimals.",
     "td_residuals(rewards, values, gamma)", """
def td_residuals(rewards, values, gamma):
    out = []
    for t in range(len(rewards)):
        out.append(round(rewards[t] + gamma * values[t + 1] - values[t], 6))
    return out
""", [[[1, 1], [0.5, 0.5, 0.5], 0.9], [[0, 0, 1], [0, 0, 0, 0], 0.99], [[1], [2.0, 3.0], 0.5], [[], [1.0], 0.9]], "Use the next value."),
  PL("GAE", "Write gae(rewards, values, dones, gamma, lam): values has one more entry than rewards; dones[t] is 1 if the episode ended after step t (then the next value and the running advantage are cut off, mask = 1 - dones[t]). Compute delta_t = r_t + gamma * V[t+1] * mask - V[t] and A_t = delta_t + gamma * lam * mask * A_{t+1} backwards. Round each advantage to 6 decimals.",
     "gae(rewards, values, dones, gamma, lam)", """
def gae(rewards, values, dones, gamma, lam):
    T = len(rewards)
    adv = [0.0] * T
    last = 0.0
    for t in range(T - 1, -1, -1):
        mask = 1.0 - dones[t]
        delta = rewards[t] + gamma * values[t + 1] * mask - values[t]
        last = delta + gamma * lam * mask * last
        adv[t] = round(last, 6)
    return adv
""", [[[1, 1, 1], [0.5, 0.5, 0.5, 0.5], [0, 0, 0], 0.9, 0.95], [[1, 0, 1], [0.0, 1.0, 0.0, 2.0], [0, 1, 0], 0.99, 0.95], [[1, 1], [0, 0, 0], [0, 0], 0.9, 0.0], [[1, 1], [0, 0, 0], [0, 0], 0.9, 1.0]], "Backwards recursion with a mask."),
  PL("Value targets", "The value network is trained towards the return estimate R_t = A_t + V(s_t). Write value_targets(advantages, values): the list of A_t + V[t] for each t (values may be longer; use the first len(advantages) entries), rounded to 6 decimals.",
     "value_targets(advantages, values)", """
def value_targets(advantages, values):
    return [round(advantages[t] + values[t], 6) for t in range(len(advantages))]
""", [[[0.5, -0.5], [1.0, 2.0, 3.0]], [[0.0], [1.5, 0.0]], [[1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0]]], "Advantage plus value."),
  PL("Normalise advantages", "Write normalise(adv): subtract the mean and divide by (std + 1e-8), where std is the population standard deviation; round to 6 decimals. Use import math.",
     "normalise(adv)", """
import math
def normalise(adv):
    n = len(adv)
    mu = sum(adv) / n
    var = sum((a - mu) ** 2 for a in adv) / n
    s = math.sqrt(var)
    return [round((a - mu) / (s + 1e-8), 6) for a in adv]
""", [[[1, 2, 3]], [[0, 0, 0]], [[5, -5]], [[0.1, 0.2, 0.4, 0.8]]], "Zero mean and unit spread."),
  ORDER("Computing advantages", "Order the steps.", ["Roll out the policy and record rewards and values", "Compute TD residuals", "Accumulate them backwards with gamma times lambda", "Form value targets A plus V", "Normalise the advantages"]),
  MATCH("GAE", "Match each item with its meaning.", [("delta", "One-step TD residual"), ("lambda = 0", "One-step estimate"), ("lambda = 1", "Return minus value"), ("done mask", "Cut off after episode end"), ("Normalisation", "Mean 0, standard deviation 1")]),
  FILL("Advantages", "The advantage is Q minus {{V|the value}}; GAE blends estimates with the parameter {{lambda}}.")]))

CHS.append(CH(
 "Trust regions, KL divergence and the ratio",
 ("Trust region", [
  "Ratio | is | New over old probability",
  "KL divergence | measures | Policy change",
  "Trust region | limits | Update size",
  "TRPO | constrains | KL",
  "Surrogate | uses | Old-policy samples",
  "Importance sampling | corrects | Distribution shift",
  "Large ratio | signals | Big change"]),
 ["The data comes from the old policy, but we want to evaluate a new one. The probability ratio r = pi_new(a|s) / pi_old(a|s) corrects for this: it is importance sampling. The surrogate objective weights each advantage by r.",
  "The surrogate is a good approximation only near the old policy. TRPO keeps the policy there by bounding the average KL divergence between old and new. PPO will keep the ratio near one instead.",
  "The labs compute ratios from log-probabilities, KL divergence for categorical policies and a KL-penalised surrogate."],
 [("Probability ratio", "r(theta) = pi_theta(a|s) / pi_old(a|s)."),
  ("Importance sampling", "Reweighting samples from one distribution to estimate an average under another."),
  ("KL divergence", "A measure of how different one distribution is from another."),
  ("Trust region", "The neighbourhood of the current policy in which the surrogate can be trusted."),
  ("Surrogate objective", "L(theta) = E[ r(theta) * A ]."),
  ("Monotonic improvement", "TRPO's theory: a bounded KL step guarantees no (large) decrease.")],
 ["r = exp(log pi_new - log pi_old).",
  "Surrogate: L(theta) = E[ r * A ]. At theta = theta_old, r = 1.",
  "KL(p || q) = sum p log(p / q), zero only when p = q.",
  "TRPO: maximise the surrogate subject to mean KL <= delta.",
  "PPO-penalty variant: maximise L - beta * KL, adapting beta.",
  "PPO-clip: remove the incentive to push r outside [1 - eps, 1 + eps]."],
 [T("The samples in our batch were collected by the old policy. But the policy gradient involves expectations under the policy being improved. To correct, weight each sample by the ratio of its probability under the new policy to that under the old. This is importance sampling. The weighted advantage is the surrogate objective."),
  M(r"r_t(\theta) \;=\; \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\mathrm{old}}}(a_t \mid s_t)}, \qquad L(\theta) \;=\; \mathbb{E}\bigl[\, r_t(\theta)\,\hat{A}_t \,\bigr]"),
  T("At the start of an update the new policy equals the old one, so every ratio is one, and the gradient of L is the ordinary policy gradient. As the parameters move, the ratios depart from one. The farther they go, the less reliable the surrogate, since the data no longer matches the policy."),
  T("TRPO makes the limit explicit. It maximises L subject to the average KL divergence between old and new policies being below a small number. The KL divergence between two distributions is zero when they are equal and grows as they differ. A constraint on KL is a limit on how far the policy can move in distribution, not in parameter space."),
  M(r"D_{\mathrm{KL}}(p \,\|\, q) \;=\; \sum_a p(a)\,\log\frac{p(a)}{q(a)}"),
  T("Enforcing the constraint needs the second-order machinery of TRPO. The PPO paper explores two cheaper alternatives. One adds the KL as a penalty with a coefficient that is adapted to hit a target KL. The other clips the ratio, which is the subject of the next chapter. The paper found the clipped version performed best."),
  T("In practice we store the log-probabilities of the actions under the old policy at collection time. The ratio is then the exponential of the difference of log-probabilities, which is numerically stable.")],
 [("What does the ratio correct for?", ["Data collected by the old policy", "Reward scale", "Value error", "Entropy"], 0, "Importance sampling."),
  ("What is the ratio at the start of an update?", ["One", "Zero", "Two", "Undefined"], 0, "New equals old."),
  ("What does TRPO constrain?", ["Mean KL between policies", "The learning rate", "The batch size", "The reward"], 0, "A trust region."),
  ("When is KL zero?", ["When the distributions are equal", "Always", "Never", "When p is uniform"], 0, "Otherwise positive.")],
 [("How is the ratio computed?", "exp(log new - log old)."), ("What is the surrogate?", "E[r times A]."), ("What are PPO's two variants?", "KL penalty and clipping."), ("Why store old log-probs?", "To get the ratio.")],
 [PL("Probability ratio", "Write ratio(logp_new, logp_old): exp(logp_new - logp_old). Use import math.",
     "ratio(logp_new, logp_old)", """
import math
def ratio(logp_new, logp_old):
    return math.exp(logp_new - logp_old)
""", [[-1.0, -1.0], [-0.5, -1.0], [-2.0, -1.0], [0.0, -0.1], [-3.0, -1.5]], "One line.", approx=1e-9),
  PL("KL divergence", "Write kl(p, q): the KL divergence sum p_i * ln(p_i / q_i) of two probability lists (skip terms where p_i is 0). Use import math.",
     "kl(p, q)", """
import math
def kl(p, q):
    s = 0.0
    for a, b in zip(p, q):
        if a > 0:
            s += a * math.log(a / b)
    return s
""", [[[0.5, 0.5], [0.5, 0.5]], [[0.9, 0.1], [0.5, 0.5]], [[0.5, 0.5], [0.9, 0.1]], [[1.0, 0.0], [0.5, 0.5]], [[0.2, 0.3, 0.5], [0.3, 0.3, 0.4]]], "Skip zero terms.", approx=1e-9),
  PL("Surrogate", "Write surrogate(ratios, advantages): the mean of ratio_i * advantage_i. Round to 9 decimals.",
     "surrogate(ratios, advantages)", """
def surrogate(ratios, advantages):
    s = 0.0
    for r, a in zip(ratios, advantages):
        s += r * a
    return round(s / len(ratios), 9)
""", [[[1, 1, 1], [1, -1, 2]], [[1.2, 0.8], [1.0, 1.0]], [[0.5], [3.0]], [[2.0, 0.1], [-1.0, 5.0]]], "Average of ratio times advantage.", approx=1e-9),
  PL("KL-penalised surrogate", "Write penalised(ratios, advantages, kl_value, beta): the surrogate minus beta times kl_value, rounded to 9 decimals.",
     "penalised(ratios, advantages, kl_value, beta)", """
def penalised(ratios, advantages, kl_value, beta):
    s = 0.0
    for r, a in zip(ratios, advantages):
        s += r * a
    return round(s / len(ratios) - beta * kl_value, 9)
""", [[[1, 1], [1, 1], 0.0, 1.0], [[1.2, 0.8], [1.0, 1.0], 0.05, 2.0], [[1.5], [2.0], 0.1, 10.0]], "Penalty on the policy change.", approx=1e-9),
  ORDER("Why a ratio", "Order the argument.", ["Data is collected under the old policy", "We want to improve a new policy", "Weight each sample by new over old probability", "The weighting is accurate only near the old policy", "So limit how far the new policy moves"]),
  MATCH("Trust region", "Match each term with its meaning.", [("Ratio", "New over old probability"), ("KL divergence", "Distribution difference"), ("TRPO", "KL constraint"), ("PPO-penalty", "KL as a penalty"), ("PPO-clip", "Clip the ratio")]),
  FILL("Ratio", "The ratio is the {{new}} probability over the {{old}} probability.")]))

CHS.append(CH(
 "The clipped surrogate objective",
 ("Clipping", [
  "Clip | bounds | The ratio",
  "Epsilon | is | 0.2 typically",
  "Min | takes | The pessimistic term",
  "Positive advantage | stops at | 1 plus epsilon",
  "Negative advantage | stops at | 1 minus epsilon",
  "Clipped region | has | Zero gradient",
  "Objective | is | A lower bound"]),
 ["The PPO objective is L = E[ min( r A, clip(r, 1 - eps, 1 + eps) A ) ]. The clip cuts the ratio to the band from 1 - eps to 1 + eps, where eps is about 0.2. The min then picks the more pessimistic of the clipped and unclipped terms.",
  "If an action had positive advantage, increasing its probability helps only until the ratio reaches 1 + eps; beyond that the gradient is zero. If the advantage is negative, decreasing helps only until 1 - eps. This removes the incentive for large policy changes without a hard constraint.",
  "The labs compute the objective and its gradient in each region."],
 [("Clipping", "Limiting a value to a range: clip(x, lo, hi)."),
  ("Epsilon", "The clip range hyperparameter; 0.2 is a common value."),
  ("Pessimistic bound", "Taking the smaller of two estimates."),
  ("Clip fraction", "The share of samples whose ratio was outside the band."),
  ("Dead zone", "A region where the gradient is zero."),
  ("Per-sample loss", "The negative of the clipped term, averaged over a minibatch.")],
 ["L_clip = min(r A, clip(r, 1 - eps, 1 + eps) A).",
  "A > 0: gradient is zero once r > 1 + eps.",
  "A < 0: gradient is zero once r < 1 - eps.",
  "Otherwise the gradient is that of r A: r * A with respect to log pi.",
  "The min makes the objective a lower bound on the unclipped surrogate.",
  "eps = 0.2 was a good value in the paper's experiments (the paper compared several)."],
 [T("Here is the heart of PPO. Take the surrogate r times A, and cut off its improvement when the ratio strays too far. The clip function limits the ratio to the interval from one minus epsilon to one plus epsilon. The final objective takes the smaller of the clipped and unclipped values."),
  M(r"L^{\mathrm{CLIP}}(\theta) \;=\; \mathbb{E}_t\Bigl[\ \min\bigl(\, r_t(\theta)\,\hat{A}_t,\ \ \mathrm{clip}\bigl(r_t(\theta),\,1-\epsilon,\,1+\epsilon\bigr)\,\hat{A}_t \bigr) \Bigr]"),
  T("Case one: the advantage is positive. The action was better than average, so we want to raise its probability, which raises r. The unclipped term r A grows without limit. The clipped term stops growing at one plus epsilon times A. The min picks the clipped term once r passes the band. Its gradient is zero. The incentive to push this action further vanishes."),
  T("Case two: the advantage is negative. We want to lower r. The unclipped term r A, being negative, rises as r falls. The clipped term stops improving below one minus epsilon. The min picks the smaller value, so now the clipped term applies when r is below the band. Again the gradient is zero."),
  T("There is a subtle point in the min. Suppose the advantage is positive and r has already dropped below one minus epsilon, an action that became less likely despite being good. The unclipped term r A is the smaller one, so the min keeps it, and its gradient pushes r back up. The objective clips only the improvement, never the correction of a mistake. That makes it a pessimistic lower bound on the surrogate."),
  T("The value of epsilon sets how far a single update can go. The paper compared several values and found 0.2 worked well on its continuous control tasks. Many later implementations also use 0.1 to 0.3. The fraction of samples falling outside the band, the clip fraction, is a useful diagnostic during training.")],
 [("What happens to the gradient for A > 0 once r exceeds 1 + eps?", ["It is zero", "It doubles", "It flips sign", "It is infinite"], 0, "No incentive to go further."),
  ("What does the min do?", ["Takes the pessimistic term", "Takes the larger term", "Averages", "Clips"], 0, "A lower bound."),
  ("What is a typical epsilon?", ["0.2", "20", "0", "5"], 0, "Often between 0.1 and 0.3."),
  ("If A > 0 and r < 1 - eps, is the gradient zero?", ["No, the unclipped term applies", "Yes", "Only at r = 0", "Always"], 0, "Mistakes are not clipped.")],
 [("What is the clip fraction?", "Share of samples outside the band."), ("What does clipping remove?", "The incentive for large changes."), ("Is it a hard constraint?", "No, only a removed incentive."), ("What is the objective's shape for A > 0?", "Rises with r then flattens.")],
 [PL("Clipped objective", "Write clip_obj(r, adv, eps): min(r * adv, clip(r, 1 - eps, 1 + eps) * adv).",
     "clip_obj(r, adv, eps)", """
def clip_obj(r, adv, eps):
    c = r
    if c < 1 - eps:
        c = 1 - eps
    if c > 1 + eps:
        c = 1 + eps
    return min(r * adv, c * adv)
""", [[1.0, 1.0, 0.2], [1.5, 1.0, 0.2], [0.5, 1.0, 0.2], [1.5, -1.0, 0.2], [0.5, -1.0, 0.2], [1.1, 2.0, 0.2], [0.7, 1.0, 0.2]], "Clip the ratio then take the minimum.", approx=1e-9),
  PL("Gradient of the objective", "Write clip_grad(r, adv, eps): the derivative of the per-sample clipped objective with respect to log pi_new (note d r / d log pi = r). It is r * adv unless the sample is clipped: adv > 0 and r > 1 + eps, or adv < 0 and r < 1 - eps, in which case it is 0.",
     "clip_grad(r, adv, eps)", """
def clip_grad(r, adv, eps):
    if adv > 0 and r > 1 + eps:
        return 0.0
    if adv < 0 and r < 1 - eps:
        return 0.0
    return r * adv
""", [[1.0, 1.0, 0.2], [1.5, 1.0, 0.2], [0.5, 1.0, 0.2], [1.5, -1.0, 0.2], [0.5, -1.0, 0.2], [1.2, 1.0, 0.2]], "Zero only in the clipped regions.", approx=1e-9),
  PL("Mean clipped loss", "Write ppo_clip_loss(ratios, advs, eps): the NEGATIVE mean of the clipped objective over the samples (the loss to minimise), rounded to 9 decimals.",
     "ppo_clip_loss(ratios, advs, eps)", """
def ppo_clip_loss(ratios, advs, eps):
    tot = 0.0
    for r, a in zip(ratios, advs):
        c = r
        if c < 1 - eps:
            c = 1 - eps
        if c > 1 + eps:
            c = 1 + eps
        tot += min(r * a, c * a)
    return round(-tot / len(ratios), 9)
""", [[[1.0, 1.0], [1.0, -1.0], 0.2], [[1.5, 0.5], [1.0, 1.0], 0.2], [[1.5, 0.5], [-1.0, -1.0], 0.2], [[1.1], [2.0], 0.2]], "Average then negate.", approx=1e-9),
  PL("Clip fraction", "Write clip_fraction(ratios, eps): the fraction of ratios outside [1 - eps, 1 + eps].",
     "clip_fraction(ratios, eps)", """
def clip_fraction(ratios, eps):
    n = 0
    for r in ratios:
        if r < 1 - eps or r > 1 + eps:
            n += 1
    return n / len(ratios)
""", [[[1.0, 1.3, 0.7, 1.1], 0.2], [[1.0], 0.2], [[1.5, 1.6], 0.2], [[0.9, 1.1], 0.05]], "Count the samples outside the band.", approx=1e-12),
  ORDER("Reading the objective", "Order the checks for one sample.", ["Compute the ratio", "Clip it to the band", "Multiply both ratios by the advantage", "Take the smaller product", "Average over the minibatch"]),
  MATCH("Cases", "Match each case with the gradient.", [("A > 0, r in band", "r times A"), ("A > 0, r > 1 + eps", "Zero"), ("A < 0, r < 1 - eps", "Zero"), ("A > 0, r < 1 - eps", "r times A (corrects)"), ("A < 0, r > 1 + eps", "r times A (corrects)")]),
  FILL("Clip", "The objective takes the {{min|minimum|smaller}} of the clipped and unclipped terms, with epsilon about {{0.2}}.")]))

CHS.append(CH(
 "The full loss: value, entropy and the update",
 ("Total loss", [
  "Total loss | sums | Three terms",
  "Policy loss | is | Negative clipped objective",
  "Value loss | trains | The critic",
  "Entropy bonus | keeps | Exploration alive",
  "Coefficients | weight | The terms",
  "Shared network | needs | A combined loss",
  "Minibatch | gives | One gradient step"]),
 ["When the policy and value function share a network, PPO combines three terms: the clipped policy objective, a value function loss and an entropy bonus. L = L_clip - c1 L_value + c2 Entropy, maximised (or its negative minimised).",
  "The value loss is the squared error between the predicted value and the target return. The entropy bonus rewards a spread-out policy, which prevents it from becoming deterministic too early.",
  "Common defaults for the coefficients are c1 = 0.5 and c2 = 0.01; these are conventions in popular implementations, not requirements."],
 [("Value loss", "Squared error between V(s) and the target return."),
  ("Entropy", "H(pi) = -sum pi log pi: how spread out the policy is."),
  ("Entropy bonus", "A term added to the objective to encourage exploration."),
  ("Shared parameters", "Policy and value heads using the same body network."),
  ("Combined loss", "The weighted sum used for one optimiser step."),
  ("Minibatch", "A random subset of the collected batch.")],
 ["L = L_clip - c1 * L_value + c2 * H, maximised; minimise the negative.",
  "L_value = (V(s) - R)^2 (sometimes clipped).",
  "Entropy of a discrete policy: -sum p log p.",
  "Typical coefficients: c1 about 0.5 and c2 about 0.01 (implementation defaults).",
  "Without the entropy term the policy may collapse to a single action early.",
  "The PPO paper presents this combined objective for shared architectures."],
 [T("So far we have the policy part. The advantages come from a value function, which must be learned too. Often one network has two outputs, a policy head and a value head, sharing the early layers. Then a single loss must train both."),
  T("The value loss is simple: the squared difference between the value the network predicts and the target return, which we computed in chapter 3 as the advantage plus the old value. The entropy bonus is a third term. Entropy measures how spread out the policy is. A uniform policy has the highest entropy, a deterministic one has zero. Adding entropy to the objective gently pushes the policy to keep some randomness, which keeps exploration alive."),
  M(r"L(\theta) \;=\; \mathbb{E}_t\Bigl[\, L^{\mathrm{CLIP}}_t(\theta) \;-\; c_1\, L^{\mathrm{VF}}_t(\theta) \;+\; c_2\, S[\pi_\theta](s_t) \Bigr], \qquad L^{\mathrm{VF}} = \bigl(V_\theta(s_t) - V^{\mathrm{targ}}_t\bigr)^2"),
  T("The paper gives this combined objective for architectures that share parameters between the policy and the value function. The coefficients c one and c two weight the terms. In many popular implementations, c one is 0.5 and c two is 0.01. Those are common defaults rather than values the theory demands, and the best values depend on the problem."),
  T("In code we minimise rather than maximise, so the total loss is the negative of the above: the clip loss plus c1 times the value loss minus c2 times the entropy. Gradients flow through all three terms into the shared network. Some implementations also clip the value loss in a way parallel to the policy clip."),
  T("The labs compute the entropy, the value loss, the combined loss and one full gradient step for a tiny softmax policy with a clipped objective.")],
 [("What does the entropy bonus encourage?", ["Exploration", "Faster rewards", "Bigger batches", "Lower loss"], 0, "A spread-out policy."),
  ("What is the value loss?", ["Squared error to the target return", "KL divergence", "The advantage", "The ratio"], 0, "Trains the critic."),
  ("What are typical c1 and c2?", ["0.5 and 0.01", "10 and 10", "0 and 0", "1 and 1"], 0, "Implementation defaults."),
  ("Why a combined loss?", ["A shared network trains both heads", "To save RAM", "To clip", "To normalise"], 0, "One optimiser step.")],
 [("What is entropy of a deterministic policy?", "Zero."), ("What is the value target?", "A plus V from GAE."), ("Is c2 theory-determined?", "No, a tuned default."), ("What happens without entropy?", "Early collapse to one action.")],
 [PL("Entropy", "Write entropy(p): -sum p_i ln p_i for a probability list (skip zeros), rounded to 9 decimals. Use import math.",
     "entropy(p)", """
import math
def entropy(p):
    s = 0.0
    for x in p:
        if x > 0:
            s -= x * math.log(x)
    return round(s, 9)
""", [[[0.5, 0.5]], [[1.0, 0.0]], [[0.25, 0.25, 0.25, 0.25]], [[0.9, 0.1]]], "Skip zero entries.", approx=1e-9),
  PL("Value loss", "Write value_loss(values, targets): the mean of (value - target)^2, rounded to 9 decimals.",
     "value_loss(values, targets)", """
def value_loss(values, targets):
    s = 0.0
    for v, t in zip(values, targets):
        s += (v - t) ** 2
    return round(s / len(values), 9)
""", [[[1.0, 2.0], [1.0, 2.0]], [[0.0, 0.0], [1.0, -1.0]], [[0.5], [1.5]], [[1, 2, 3], [2, 2, 2]]], "Mean squared error.", approx=1e-9),
  PL("Total loss", "Write total_loss(clip_loss, v_loss, ent, c1, c2): clip_loss + c1 * v_loss - c2 * ent, rounded to 9 decimals.",
     "total_loss(clip_loss, v_loss, ent, c1, c2)", """
def total_loss(clip_loss, v_loss, ent, c1, c2):
    return round(clip_loss + c1 * v_loss - c2 * ent, 9)
""", [[-0.5, 1.0, 0.6, 0.5, 0.01], [0.0, 0.0, 0.0, 0.5, 0.01], [1.0, 2.0, 0.7, 1.0, 0.1], [-0.1, 0.4, 1.0, 0.25, 0.0]], "Minimise: clip + c1 value - c2 entropy.", approx=1e-9),
  PL("One clipped step on a softmax policy", "A softmax policy has logits theta. Write ppo_step(theta, samples, eps, lr): samples is a list of [action, advantage, old_prob]. Compute the current probabilities p; for each sample the ratio r = p[a]/old_prob; the gradient with respect to the logits of the clipped objective is g_a_term = (r * adv unless clipped, as before) times (onehot(a) - p); average over the samples; return the new logits theta + lr * mean gradient, each rounded to 6 decimals. Use import math.",
     "ppo_step(theta, samples, eps, lr)", """
import math
def ppo_step(theta, samples, eps, lr):
    m = max(theta)
    es = [math.exp(t - m) for t in theta]
    s = sum(es)
    p = [e / s for e in es]
    g = [0.0] * len(theta)
    for a, adv, old in samples:
        r = p[a] / old
        if adv > 0 and r > 1 + eps:
            w = 0.0
        elif adv < 0 and r < 1 - eps:
            w = 0.0
        else:
            w = r * adv
        for i in range(len(theta)):
            g[i] += w * ((1.0 if i == a else 0.0) - p[i])
    n = len(samples)
    return [round(theta[i] + lr * g[i] / n, 6) for i in range(len(theta))]
""", [[[0.0, 0.0], [[0, 1.0, 0.5], [1, -1.0, 0.5]], 0.2, 0.5], [[1.0, 0.0, 0.0], [[0, 1.0, 0.3], [1, -0.5, 0.35], [2, 0.2, 0.35]], 0.2, 0.3], [[0.0, 0.0], [[0, 1.0, 0.3]], 0.2, 1.0], [[2.0, 0.0], [[1, -1.0, 0.5]], 0.2, 0.5]], "Zero weight in the clipped regions."),
  ORDER("Building the loss", "Order the steps.", ["Compute the ratio and clipped policy loss", "Compute the value loss against the targets", "Compute the entropy of the policy", "Combine them with the coefficients", "Backpropagate and take an optimiser step"]),
  MATCH("Loss terms", "Match each term with its role.", [("Clip loss", "Improves the policy safely"), ("Value loss", "Trains the critic"), ("Entropy", "Keeps exploration"), ("c1", "Value weight"), ("c2", "Entropy weight")]),
  FILL("Loss", "The total loss adds the clip loss and the {{value}} loss and subtracts an {{entropy}} bonus.")]))

CHS.append(CH(
 "The PPO algorithm and its practical details",
 ("The loop", [
  "Rollout | collects | T steps from N actors",
  "Batch | splits into | Minibatches",
  "Epochs | reuse | The same batch",
  "KL early stop | halts | Large updates",
  "Gradient clipping | bounds | Update norm",
  "Learning rate | anneals | Over training",
  "Seeds | affect | Results strongly"]),
 ["The algorithm runs in rounds. Actors run the current policy for T steps and record states, actions, rewards, values and old log-probabilities. Advantages are computed. Then the batch is shuffled and split into minibatches, and for K epochs we take a gradient step on the combined loss for each minibatch.",
  "Implementations add practical touches: gradient norm clipping, learning rate annealing, advantage normalisation, observation normalisation and sometimes an early stop when the measured KL grows too large. Many of these are conventions found in popular code, which studies have shown can matter as much as the clip itself.",
  "The labs implement minibatch splitting, gradient clipping, learning rate annealing and the early-stop test."],
 [("Rollout", "A fixed number of environment steps collected with the current policy."),
  ("Actor", "A copy of the environment (or process) generating experience."),
  ("Minibatch", "A subset of the batch used for one gradient step."),
  ("Gradient clipping", "Rescaling the gradient if its norm exceeds a limit."),
  ("Annealing", "Gradually reducing a hyperparameter such as the learning rate."),
  ("Early stopping on KL", "Ending the epochs early if the policy has moved too far.")],
 ["Collect T steps from N parallel actors; batch size = N * T.",
  "Run K epochs of minibatch gradient steps on that batch.",
  "Compute advantages once, with the old value estimates.",
  "Clip the global gradient norm (0.5 is a common value).",
  "Anneal the learning rate linearly to zero (a common choice).",
  "Results vary a lot between random seeds; report several."],
 [T("Now the whole algorithm. A round has two phases. In the collection phase, N actors each run the current policy for T steps. Record for each step the observation, the action, the reward, whether the episode ended, the value estimate and the log-probability of the action. This gives a batch of N times T samples."),
  T("Then compute advantages with GAE and the value targets. These are fixed for the round: they use the value estimates from collection time. In the update phase, shuffle the batch, split it into minibatches and loop for K epochs. For each minibatch, compute the new log-probabilities, the ratios, the clipped loss, the value loss and the entropy, and take a gradient step."),
  M(r"\text{round:}\quad \text{collect } N\!\times\!T \text{ samples} \;\to\; \hat A_t \;\to\; \text{for } k=1..K:\ \text{for each minibatch: } \theta \leftarrow \theta - \alpha\,\nabla_\theta(-L)"),
  T("Reusing the batch for several epochs is the point of the clip. Plain policy gradient could use a batch once, since a second pass would overshoot. With clipping the gradient vanishes for samples whose ratio has moved far enough, so repeated passes are safe."),
  T("A body of practice grew around the algorithm. Gradient norm clipping rescales an oversized gradient. The learning rate is often annealed. Observations may be normalised by running statistics. Some implementations stop the epochs early if the measured approximate KL divergence between old and new policies exceeds a threshold. Engstrom and colleagues and others have noted that some of these details have large effects on performance, so that the clip alone does not explain PPO's results. Treat that as a caution when comparing papers."),
  T("Finally, RL results vary a lot between random seeds. A single good run says little. Report the mean and spread over several seeds.")],
 [("What is the batch size?", ["Actors times steps", "Epochs", "Minibatch count", "Gamma"], 0, "N times T."),
  ("Why can PPO reuse a batch?", ["Clipping makes extra epochs safe", "Data is free", "The ratio is always one", "The critic is fixed"], 0, "Gradients vanish for moved samples."),
  ("What does gradient clipping do?", ["Rescales large gradients", "Clips the ratio", "Removes entropy", "Stops training"], 0, "By global norm."),
  ("Why report several seeds?", ["Results vary a lot", "Seeds are free", "The paper says so", "To use more GPUs"], 0, "One run proves little.")],
 [("What is K?", "The number of epochs per round."), ("When are advantages computed?", "Once per round."), ("What is early stopping on KL?", "Ending epochs if KL gets large."), ("Which details matter?", "Normalisation, annealing, clipping.")],
 [PL("Minibatch indices", "Write minibatches(n, size): split the indices 0..n-1 in order into consecutive minibatches of the given size (the last may be shorter). Return the list of lists.",
     "minibatches(n, size)", """
def minibatches(n, size):
    out = []
    i = 0
    while i < n:
        out.append(list(range(i, min(i + size, n))))
        i += size
    return out
""", [[10, 4], [8, 4], [3, 5], [0, 4]], "Consecutive slices."),
  PL("Clip the gradient norm", "Write clip_grad_norm(grad, max_norm): if the Euclidean norm of the list grad exceeds max_norm, rescale it to have norm max_norm; otherwise return it unchanged. Round each entry to 6 decimals. Use import math.",
     "clip_grad_norm(grad, max_norm)", """
import math
def clip_grad_norm(grad, max_norm):
    n = math.sqrt(sum(g * g for g in grad))
    if n > max_norm:
        k = max_norm / n
        return [round(g * k, 6) for g in grad]
    return [round(g, 6) for g in grad]
""", [[[3, 4], 1.0], [[0.3, 0.4], 1.0], [[0, 0], 0.5], [[6, 8], 5.0]], "Scale by max over norm."),
  PL("Learning rate annealing", "Write lr_at(step, total, lr0): linear annealing from lr0 at step 0 to 0 at step total, lr0 * (1 - step / total).",
     "lr_at(step, total, lr0)", """
def lr_at(step, total, lr0):
    return lr0 * (1 - step / total)
""", [[0, 100, 0.001], [50, 100, 0.001], [100, 100, 0.001], [25, 200, 0.0003]], "Straight line down.", approx=1e-12),
  PL("Approximate KL and early stop", "Write approx_kl(old_logp, new_logp): the mean of (old_logp - new_logp) over the samples, a common estimate of KL(old || new), and write it so the function returns [that estimate rounded to 9 decimals, 1 if it exceeds 0.015 else 0].",
     "approx_kl(old_logp, new_logp)", """
def approx_kl(old_logp, new_logp):
    s = 0.0
    for a, b in zip(old_logp, new_logp):
        s += a - b
    k = s / len(old_logp)
    return [round(k, 9), 1 if k > 0.015 else 0]
""", [[[-1.0, -2.0], [-1.0, -2.0]], [[-1.0, -2.0], [-1.1, -2.1]], [[-1.0], [-1.5]], [[-0.5, -0.5], [-0.49, -0.5]]], "Mean log-probability difference."),
  ORDER("PPO round", "Order the algorithm.", ["Collect N by T steps with the current policy", "Compute GAE advantages and value targets", "Shuffle and split into minibatches", "For K epochs, take clipped-loss gradient steps", "Repeat with fresh data"]),
  MATCH("Practice", "Match each practice with its purpose.", [("Gradient clipping", "Bound the update"), ("Learning rate annealing", "Smaller steps late"), ("Advantage normalisation", "Steady gradient scale"), ("KL early stop", "Avoid big updates"), ("Several seeds", "Honest comparison")]),
  FILL("Loop", "PPO reuses each {{batch}} for K {{epochs|epoch}} of minibatch updates.")]))

CHS.append(CH(
 "PPO for language models (RLHF)",
 ("RLHF", [
  "RLHF | tunes | A language model",
  "Reward model | scores | Responses",
  "Policy | is | The language model",
  "Action | is | A token",
  "KL penalty | anchors | To a reference model",
  "PPO | updates | The policy",
  "DPO | avoids | The RL loop"]),
 ["Reinforcement learning from human feedback, RLHF, fine-tunes a language model with PPO. A reward model trained on human preferences scores whole responses. The language model is the policy, each token is an action, and the response is the episode. This chapter is background knowledge: it goes beyond the 2017 PPO paper.",
  "To stop the model drifting into gibberish that fools the reward model, the reward includes a penalty on the KL divergence between the tuned model and a frozen reference model. Often a value head is added to the language model to supply advantages.",
  "The labs compute a KL-penalised token reward and the per-token advantages."],
 [("RLHF", "Reinforcement learning from human feedback."),
  ("Reward model", "A network trained on human preference data to score responses."),
  ("Reference model", "The frozen starting model that the policy is kept close to."),
  ("KL penalty", "A cost on the per-token log-probability gap to the reference."),
  ("Reward hacking", "Exploiting flaws in the reward model to get a high score without real quality."),
  ("Response", "The sequence of tokens generated for a prompt.")],
 ["Policy = language model; state = prompt plus tokens so far; action = next token.",
  "Reward model gives a score at the end of the response.",
  "Per-token KL penalty: -beta * (log pi(token) - log pi_ref(token)).",
  "A value head predicts expected final reward for advantages (GAE).",
  "PPO-clip stabilises the updates.",
  "Alternatives skip the RL step: DPO trains directly on preferences (see the DPO course)."],
 [T("A language model trained to predict text imitates the internet. To make it helpful, one wants to push it toward answers people prefer. RLHF does this in three steps. First, fine-tune on examples of good responses. Second, train a reward model on human comparisons of pairs of responses: it learns to give the preferred one a higher score. Third, use reinforcement learning, in practice often PPO, to adjust the language model to get high reward-model scores. This three-step recipe was used in OpenAI's InstructGPT work."),
  T("In the RL step the language model is the policy. The state is the prompt plus the tokens generated so far, and the action is the next token. The response is one episode. The reward model scores the finished response, so almost all reward arrives at the final token, a sparse-reward setting that makes the value function and GAE valuable."),
  M(r"r_t \;=\; \begin{cases} -\beta\,\bigl(\log \pi_\theta(a_t \mid s_t) - \log \pi_{\mathrm{ref}}(a_t \mid s_t)\bigr) & t < T \\ r_{\mathrm{RM}}(x, y) \;-\; \beta\,\bigl(\log \pi_\theta - \log \pi_{\mathrm{ref}}\bigr) & t = T \end{cases}"),
  T("A pure reward-model objective would let the policy drift to strange outputs that exploit the reward model, which is only an imperfect proxy. So each token gets a penalty proportional to how much the tuned model's log-probability exceeds the reference model's. Summed over the response, this is a sample estimate of the KL divergence from the reference. The coefficient beta sets how tightly the model is held."),
  T("PPO's clipping fits this setting well. Generating responses is expensive, so reusing a batch for several epochs saves cost, and clipping keeps the policy from lurching. But the machinery is heavy: the policy, the reference, the reward model and a value model must all be held in memory. That cost motivated simpler alternatives. Direct Preference Optimization, covered in its own course, optimises preferences without a reward model or RL loop. Group-relative methods such as GRPO drop the value model. These are later developments, background knowledge here."),
  T("In the labs, the penalty and the shaped reward are computed per token on small lists, and then fed to the GAE routine of chapter 3.")],
 [("What is the policy in RLHF?", ["The language model", "The reward model", "The reference model", "The dataset"], 0, "Tokens are the actions."),
  ("Why a KL penalty to a reference model?", ["To stop drifting and reward hacking", "To speed up", "To add data", "To shrink the model"], 0, "The reward model is an imperfect proxy."),
  ("When does the reward model give its score?", ["At the end of the response", "At each token", "Before the prompt", "Never"], 0, "Sparse reward."),
  ("Which method removes the RL loop?", ["DPO", "TRPO", "A3C", "DQN"], 0, "Direct Preference Optimization.")],
 [("What are the three RLHF steps?", "Supervised fine-tuning, reward model, RL."), ("Which models must be in memory?", "Policy, reference, reward, value."), ("What does beta control?", "How tightly we hold to the reference."), ("Is this in the 2017 PPO paper?", "No, it is later work.")],
 [PL("Per-token KL penalty", "Write kl_penalty(logp, logp_ref, beta): the list of per-token penalties -beta * (logp_i - logp_ref_i), each rounded to 9 decimals.",
     "kl_penalty(logp, logp_ref, beta)", """
def kl_penalty(logp, logp_ref, beta):
    return [round(-beta * (a - b), 9) for a, b in zip(logp, logp_ref)]
""", [[[-1.0, -2.0], [-1.0, -2.0], 0.1], [[-0.5, -1.0], [-1.0, -1.5], 0.2], [[-2.0], [-1.0], 0.5], [[-1.0, -1.0, -1.0], [-1.2, -0.8, -1.0], 1.0]], "Penalise tokens more likely than under the reference."),
  PL("Shaped rewards", "Write shaped_rewards(logp, logp_ref, beta, rm_score): the per-token rewards: the KL penalty for every token, plus rm_score added to the last token. Round each to 9 decimals.",
     "shaped_rewards(logp, logp_ref, beta, rm_score)", """
def shaped_rewards(logp, logp_ref, beta, rm_score):
    out = [-beta * (a - b) for a, b in zip(logp, logp_ref)]
    out[-1] += rm_score
    return [round(x, 9) for x in out]
""", [[[-1.0, -2.0], [-1.0, -2.0], 0.1, 1.5], [[-0.5, -1.0, -1.5], [-1.0, -1.5, -1.5], 0.2, -0.5], [[-1.0], [-2.0], 0.5, 2.0]], "The score arrives at the last token."),
  PL("Sequence KL estimate", "Write seq_kl(logp, logp_ref): the sum over tokens of (logp_i - logp_ref_i), a sample estimate of the KL divergence from the reference, rounded to 9 decimals.",
     "seq_kl(logp, logp_ref)", """
def seq_kl(logp, logp_ref):
    s = 0.0
    for a, b in zip(logp, logp_ref):
        s += a - b
    return round(s, 9)
""", [[[-1.0, -2.0], [-1.0, -2.0]], [[-0.5, -1.0], [-1.0, -1.5]], [[-2.0], [-1.0]], [[], []]], "Sum of log-ratios.", approx=1e-9),
  PL("Advantages for a response", "Write response_advantages(rewards, values, gamma, lam): GAE for one response (episode ends after the last token): values has one more entry than rewards but the final bootstrap value counts as 0. Return the advantages rounded to 6 decimals.",
     "response_advantages(rewards, values, gamma, lam)", """
def response_advantages(rewards, values, gamma, lam):
    T = len(rewards)
    adv = [0.0] * T
    last = 0.0
    for t in range(T - 1, -1, -1):
        nxt = values[t + 1] if t + 1 < T else 0.0
        delta = rewards[t] + gamma * nxt - values[t]
        last = delta + gamma * lam * last
        adv[t] = round(last, 6)
    return adv
""", [[[0.0, 0.0, 1.0], [0.2, 0.4, 0.8, 0.0], 1.0, 0.95], [[0.1, 0.1], [0.0, 0.0, 0.0], 0.99, 0.95], [[1.0], [0.5, 0.0], 1.0, 1.0], [[0.0, 0.0, 0.0, 2.0], [1.0, 1.0, 1.0, 1.0, 0.0], 1.0, 1.0]], "Last-token bootstrap is zero."),
  ORDER("RLHF with PPO", "Order the pipeline.", ["Fine-tune the model on good examples", "Collect human preference comparisons", "Train a reward model", "Sample responses from the policy", "Update with PPO using reward minus a KL penalty"]),
  MATCH("RLHF", "Match each component with its role.", [("Policy", "The language model being tuned"), ("Reference model", "Frozen anchor"), ("Reward model", "Scores responses"), ("KL penalty", "Limits drift"), ("Value head", "Provides advantages")]),
  FILL("RLHF", "The reward model scores the whole {{response}}, and a {{KL|kl}} penalty to a reference model limits drift.")]))

CHS.append(CH(
 "Diagnostics, pitfalls and relatives",
 ("Beyond PPO", [
  "Clip fraction | shows | How often clipping acts",
  "Explained variance | rates | The critic",
  "Entropy collapse | signals | Lost exploration",
  "Reward hacking | exploits | Proxy rewards",
  "A2C | is | Simpler on-policy relative",
  "SAC | is | Off-policy relative",
  "GRPO and DPO | are | Language-model relatives"]),
 ["Training curves lie. To understand a PPO run, watch several diagnostics: the approximate KL, the clip fraction, the entropy, the explained variance of the value function and the return itself. A healthy run shows small KL and moderate clip fraction, entropy that falls slowly and a value function that explains much of the return.",
  "Common failure modes: entropy collapse, value function that lags, learning rate too high, advantage scale wrong, reward hacking. Many fixes are simple once the right plot is on screen.",
  "PPO has relatives: A2C, TRPO, off-policy methods such as SAC, and for language models GRPO and DPO. The labs compute the diagnostics."],
 [("Explained variance", "1 - Var(return - value) / Var(return): how much of the return the critic explains."),
  ("Entropy collapse", "Policy entropy falling to near zero too early."),
  ("Reward hacking", "Exploiting the reward function rather than solving the task."),
  ("A2C", "Advantage actor-critic: a synchronous, simpler on-policy actor-critic."),
  ("SAC", "Soft actor-critic: an off-policy method with an entropy objective."),
  ("GRPO", "Group relative policy optimization: PPO-like, with advantages from groups of samples (background).")],
 ["Watch: approximate KL, clip fraction, entropy, explained variance, episode return.",
  "Explained variance near 1 is good; near 0 or negative means a poor critic.",
  "A clip fraction near 0 suggests tiny updates; near 1 suggests too large.",
  "Entropy collapse: raise c2, check advantage scale, lower the learning rate.",
  "Reward hacking: inspect behaviour, not just the reward number.",
  "PPO is on-policy and sample-hungry; off-policy methods can be more data-efficient."],
 [T("A PPO run produces numbers on every step. Which ones to trust? None alone. Look at a handful together. The return, or the reward model score, is what you want to rise. The approximate KL between old and new policies tells you how far each round moves; if it is huge, the updates are too large. The clip fraction tells you how often clipping acts. The entropy tells you whether exploration survives. The explained variance tells you whether the critic is any good."),
  M(r"\mathrm{EV} \;=\; 1 - \frac{\mathrm{Var}(R_t - V(s_t))}{\mathrm{Var}(R_t)}"),
  T("Explained variance near one means the value function predicts returns well. Near zero means it is no better than a constant, and negative means worse. A poor critic produces noisy advantages and slow learning, so fix it first, for instance with a higher value coefficient or more epochs."),
  T("Typical pathologies each have a signature. Entropy collapse: entropy drops quickly toward zero, the policy becomes deterministic and learning stalls. Policy collapse after a good start: the learning rate or epochs are too large, and the KL and clip fraction spike. Reward hacking: the reward climbs while real behaviour gets worse; the cure is to look at samples, not only at the curve."),
  T("PPO sits in a family. A2C is the simpler, single-update on-policy actor-critic. TRPO is the constrained ancestor. Off-policy actor-critic methods such as SAC reuse old data and can need far fewer environment steps, at the price of more delicate tuning. For language models, GRPO computes advantages from a group of sampled responses to the same prompt instead of a learned value function, and DPO skips reinforcement learning entirely. I name GRPO and DPO as later developments."),
  T("Where to go next: read the PPO paper itself, then the generalized advantage estimation paper, then implement PPO on a small environment with your favourite library and plot the five diagnostics. The final labs here compute them from small arrays.")],
 [("What does an explained variance near 0 mean?", ["The critic is poor", "A perfect critic", "A tiny KL", "High entropy"], 0, "Fix the critic first."),
  ("What is entropy collapse?", ["Entropy dropping to near zero too early", "Entropy rising", "KL dropping", "Return falling"], 0, "Exploration is lost."),
  ("Which family member skips the RL loop for language models?", ["DPO", "A2C", "SAC", "TRPO"], 0, "Direct Preference Optimization."),
  ("Why look at samples, not only rewards?", ["To catch reward hacking", "To save time", "To clip", "To anneal"], 0, "The reward is a proxy.")],
 [("Name two diagnostics.", "Clip fraction and explained variance."), ("What is SAC?", "An off-policy actor-critic."), ("What does GRPO replace?", "The learned value function."), ("What is A2C?", "A simple on-policy actor-critic.")],
 [PL("Explained variance", "Write explained_variance(returns, values): 1 - Var(returns - values) / Var(returns) with population variances (return 0 if Var(returns) is 0), rounded to 6 decimals.",
     "explained_variance(returns, values)", """
def explained_variance(returns, values):
    n = len(returns)
    mu = sum(returns) / n
    var_r = sum((r - mu) ** 2 for r in returns) / n
    if var_r == 0:
        return 0
    diff = [r - v for r, v in zip(returns, values)]
    md = sum(diff) / n
    var_d = sum((d - md) ** 2 for d in diff) / n
    return round(1 - var_d / var_r, 6)
""", [[[1, 2, 3], [1, 2, 3]], [[1, 2, 3], [2, 2, 2]], [[1, 2, 3, 4], [1.1, 1.9, 3.2, 3.8]], [[5, 5, 5], [1, 2, 3]]], "One minus the unexplained share."),
  PL("Entropy trend", "Write entropy_collapsed(entropies, floor): True if the last value of the list is below floor and below half of the first value.",
     "entropy_collapsed(entropies, floor)", """
def entropy_collapsed(entropies, floor):
    last = entropies[-1]
    first = entropies[0]
    return last < floor and last < first / 2
""", [[[1.0, 0.8, 0.05], 0.1], [[1.0, 0.9, 0.8], 0.1], [[0.2, 0.15, 0.09], 0.1], [[1.0, 0.04], 0.1]], "Both conditions must hold."),
  PL("Health check", "Write health(kl, clip_frac, ev): return a list of warnings (strings in this order, only those that apply): 'kl high' if kl > 0.05; 'clipping heavy' if clip_frac > 0.5; 'critic poor' if ev < 0.1. Return [] if all is fine.",
     "health(kl, clip_frac, ev)", """
def health(kl, clip_frac, ev):
    out = []
    if kl > 0.05:
        out.append('kl high')
    if clip_frac > 0.5:
        out.append('clipping heavy')
    if ev < 0.1:
        out.append('critic poor')
    return out
""", [[0.01, 0.1, 0.8], [0.1, 0.6, 0.05], [0.02, 0.7, 0.9], [0.0, 0.0, -0.2]], "Test each threshold."),
  PL("Compare two runs", "Write better_run(returns_a, returns_b): 'a' if the mean of the LAST three returns of a is larger than of b, 'b' if smaller, 'tie' if equal.",
     "better_run(returns_a, returns_b)", """
def better_run(returns_a, returns_b):
    ma = sum(returns_a[-3:]) / len(returns_a[-3:])
    mb = sum(returns_b[-3:]) / len(returns_b[-3:])
    if ma > mb:
        return 'a'
    if ma < mb:
        return 'b'
    return 'tie'
""", [[[1, 2, 3, 4], [1, 2, 3, 5]], [[5, 5, 5, 5], [1, 1, 1, 1]], [[1, 1, 1], [1, 1, 1]], [[10], [2, 3]]], "Compare the recent averages."),
  ORDER("Debugging a run", "Order a sensible routine.", ["Plot return and entropy", "Check approximate KL and clip fraction", "Check explained variance of the critic", "Inspect sampled behaviour", "Change one hyperparameter and re-run with several seeds"]),
  MATCH("Relatives", "Match each method with its feature.", [("TRPO", "KL-constrained, second-order"), ("A2C", "Simple on-policy actor-critic"), ("SAC", "Off-policy with entropy objective"), ("GRPO", "Group-based advantages (background)"), ("DPO", "Preference learning without RL loop")]),
  FILL("Diagnostics", "Low explained {{variance}} means a poor critic, and falling {{entropy}} may signal collapse.")]))
