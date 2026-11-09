#!/usr/bin/env python3
"""Build the PPO course. Usage: python3 make_ppo_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "ppo"))
import cmk, ppoc  # noqa: E402

PRONOUNCE = {
    "PPO": "P P O", "TRPO": "T R P O", "GAE": "G A E", "RLHF": "R L H F", "KL": "K L", "DPO": "D P O", "GRPO": "G R P O",
    "A2C": "A two C", "SAC": "sack", "REINFORCE": "re in force", "Schulman": "shul man", "Wolski": "wol ski", "Dhariwal": "dah ree wal",
    "Klimov": "klee mov", "InstructGPT": "instruct G P T", "OpenAI": "open A I", "softmax": "soft max", "Softmax": "Soft max",
    "Engstrom": "eng strum", "argmax": "arg max", "logits": "low jits", "Logits": "Low jits", "gamma": "gamma", "lambda": "lambda",
    "epsilon": "epsilon", "Adam": "adam", "MuJoCo": "mu jo co", "Atari": "ah tah ree", "GPUs": "G P Us", "pi": "pie",
}

SANDBOX = cmk.terminal("PPO lookup", "pp>", "A scripted lookup, not a real trainer. Try: clip, gae, loss, defaults", [
    ("clip", ["L_clip = min(r A, clip(r, 1-eps, 1+eps) A), r = pi_new / pi_old", "eps about 0.2; gradient is zero when A>0 and r>1+eps, or A<0 and r<1-eps"]),
    ("gae", ["delta_t = r_t + gamma V(s_t+1) - V(s_t)", "A_t = delta_t + gamma lambda A_t+1   (gamma 0.99, lambda 0.95 common)"]),
    ("loss", ["L = L_clip - c1 L_value + c2 Entropy", "common defaults c1 = 0.5, c2 = 0.01"]),
    ("defaults", ["common practice, not requirements: gamma 0.99, lambda 0.95, eps 0.2, grad clip 0.5, linear lr annealing"]),
    ("rlhf", ["reward = reward-model score - beta * (log pi - log pi_ref) per token"]),
])

EXAM = [
 ("Who introduced PPO?", ["Schulman and colleagues at OpenAI", "Mnih et al.", "Silver et al.", "Vaswani et al."], 0, "2017."),
 ("What does PPO simplify?", ["TRPO", "DQN", "AlphaGo", "A3C"], 0, "No constraint or second-order step."),
 ("Is PPO on-policy?", ["Yes", "No", "Only offline", "Only for Atari"], 0, "Fresh data after each round."),
 ("What is the return?", ["Discounted sum of future rewards", "The next reward", "The policy", "The loss"], 0, "G_t."),
 ("What is the score function of a softmax policy w.r.t. the logits?", ["onehot(a) minus pi", "pi minus one", "The return", "Zero"], 0, "Raises the chosen logit."),
 ("What does a baseline do?", ["Reduces variance", "Adds bias", "Raises reward", "Removes the policy"], 0, "Depends on the state only."),
 ("What is the advantage?", ["Q minus V", "V minus Q", "The reward", "The ratio"], 0, "Better than average by how much."),
 ("What does GAE with lambda = 0 give?", ["The one-step TD residual", "Full return minus value", "Zero", "The ratio"], 0, "Low variance, more bias."),
 ("What does GAE with lambda = 1 give?", ["Return minus value", "One-step residual", "Zero", "Entropy"], 0, "Unbiased but noisy."),
 ("Why mask at episode ends in GAE?", ["No future value after a terminal step", "To normalise", "To clip", "To save time"], 0, "Done flag."),
 ("What is the probability ratio?", ["New over old action probability", "Old over new", "Reward over value", "KL over entropy"], 0, "Importance sampling."),
 ("What is the ratio at the start of an update?", ["One", "Zero", "Two", "Undefined"], 0, "New equals old."),
 ("What does TRPO constrain?", ["Mean KL between old and new policy", "Learning rate", "Batch size", "Reward"], 0, "A trust region."),
 ("When is KL divergence zero?", ["When the distributions are equal", "Always", "Never", "When one is uniform"], 0, "Otherwise positive."),
 ("What is the PPO clipped objective?", ["min(rA, clip(r, 1-eps, 1+eps)A)", "r times A only", "A minus V", "log pi times A"], 0, "Pessimistic bound."),
 ("A > 0 and r > 1 + eps: what is the gradient?", ["Zero", "r times A", "Negative", "Infinite"], 0, "No incentive to go further."),
 ("A > 0 and r < 1 - eps: what is the gradient?", ["r times A, correcting the mistake", "Zero", "Negative", "Undefined"], 0, "Mistakes are not clipped."),
 ("What is a common epsilon?", ["0.2", "20", "0", "5"], 0, "Between 0.1 and 0.3."),
 ("What is the clip fraction?", ["Share of samples outside the band", "Size of epsilon", "Average ratio", "Value loss"], 0, "A diagnostic."),
 ("What does the entropy bonus encourage?", ["Exploration", "Lower variance", "Larger batches", "Faster reward"], 0, "A spread-out policy."),
 ("What is the value loss?", ["Squared error to the target return", "KL", "The ratio", "The advantage"], 0, "Trains the critic."),
 ("Common default c1 and c2?", ["0.5 and 0.01", "10 and 10", "0 and 0", "1 and 1"], 0, "Implementation defaults, not requirements."),
 ("Why can PPO reuse a batch for several epochs?", ["Clipping makes extra epochs safe", "Data is free", "The ratio is always one", "The critic is frozen"], 0, "Gradients vanish for moved samples."),
 ("What is the batch size?", ["Actors times steps", "Epochs", "Gamma", "Clip range"], 0, "N times T."),
 ("What does gradient norm clipping do?", ["Rescales large gradients", "Clips the ratio", "Removes entropy", "Stops training"], 0, "By global norm."),
 ("Why report several seeds?", ["RL results vary a lot", "Seeds are free", "The paper requires it", "More GPUs"], 0, "One run proves little."),
 ("In RLHF, what is the policy?", ["The language model", "The reward model", "The reference model", "The dataset"], 0, "Tokens are actions."),
 ("Why a KL penalty to a reference model?", ["To limit drift and reward hacking", "To speed up", "To add data", "To shrink the model"], 0, "The reward model is a proxy."),
 ("When does the reward model score a response?", ["At the end of the response", "At every token", "Before the prompt", "Never"], 0, "Sparse reward."),
 ("Which method skips the RL loop for language models?", ["DPO", "TRPO", "A2C", "DQN"], 0, "Direct Preference Optimization."),
 ("What does explained variance near 0 mean?", ["The critic is poor", "A perfect critic", "Tiny KL", "High entropy"], 0, "Fix the critic first."),
 ("What is entropy collapse?", ["Entropy falling near zero too early", "Entropy rising", "KL falling", "Return falling"], 0, "Exploration is lost."),
 ("Why inspect samples and not only rewards?", ["To catch reward hacking", "To save time", "To clip", "To anneal"], 0, "The reward is a proxy."),
 ("Which is off-policy?", ["SAC", "PPO", "A2C", "TRPO"], 0, "It reuses old data."),
 ("What is GRPO (background)?", ["PPO-like with group-based advantages", "A reward model", "A tokenizer", "A critic"], 0, "No learned value function."),
 ("What is the surrogate objective?", ["E[r times A]", "E[A]", "Value minus return", "KL"], 0, "Importance-weighted advantage."),
 ("Why normalise advantages per batch?", ["Steady gradient scale", "To raise reward", "To clip", "To get entropy"], 0, "An implementation habit."),
]

CFG = dict(id="ppo", title="Proximal Policy Optimization (PPO)", subtitle="Policy gradients, GAE, clipping and RLHF, with Python labs",
    description="PPO (Schulman et al., 2017) built piece by piece: policy gradient recap, advantages and GAE, the probability ratio and trust regions, the clipped surrogate objective, the full loss, the training loop and its practical details, PPO for language models (background), and diagnostics. Theory plus Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="ppo", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "ppo.course.json")
    cmk.main(CFG, ppoc.CHS, [sys.argv[0], out])
