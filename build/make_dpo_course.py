#!/usr/bin/env python3
"""Build the DPO course. Usage: python3 make_dpo_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "dpo"))
import cmk, dpoc  # noqa: E402

PRONOUNCE = {
    "DPO": "D P O", "RLHF": "R L H F", "PPO": "P P O", "KL": "K L", "IPO": "I P O", "KTO": "K T O", "ORPO": "or poh", "SimPO": "sim P O",
    "GRPO": "G R P O", "SFT": "S F T", "Rafailov": "rah fye loff", "Bradley-Terry": "bradley terry", "NeurIPS": "neur ips",
    "Kahneman-Tversky": "kah nuh man ter ski", "sigmoid": "sig moid", "Sigmoid": "Sig moid", "softmax": "soft max", "OpenAI": "open A I",
    "Z(x)": "Z of x", "pi": "pie", "InstructGPT": "instruct G P T", "log-ratio": "log ratio", "tau": "tau",
}

SANDBOX = cmk.terminal("DPO lookup", "dp>", "A scripted lookup, not a real trainer. Try: loss, optimal, grad, beta", [
    ("loss", ["L = -log sigmoid( beta log(pi(yw)/ref(yw)) - beta log(pi(yl)/ref(yl)) )", "Rafailov et al., NeurIPS 2023"]),
    ("optimal", ["pi*(y|x) = ref(y|x) exp(r(x,y)/beta) / Z(x)", "so r = beta log(pi*/ref) + beta log Z(x); log Z cancels in a pair"]),
    ("grad", ["weight = sigmoid(r_hat(yl) - r_hat(yw))", "winner log-prob up, loser log-prob down, scaled by beta * weight"]),
    ("beta", ["small: policy may drift far; large: stays near the reference", "0.1 is a common starting value"]),
    ("variants", ["IPO, KTO, ORPO, SimPO, online DPO, GRPO: later work, background"]),
])

EXAM = [
 ("Who introduced DPO?", ["Rafailov and colleagues", "Schulman and colleagues", "Vaswani and colleagues", "Silver and colleagues"], 0, "NeurIPS 2023."),
 ("What does DPO remove from RLHF?", ["The separate reward model and RL loop", "The preference data", "The reference model", "The language model"], 0, "A classification loss instead."),
 ("What is one DPO training example?", ["A prompt with a chosen and a rejected response", "A single response", "A reward score", "A token"], 0, "(x, y_w, y_l)."),
 ("What is the DPO loss form?", ["-log sigmoid of a scaled log-ratio difference", "Squared error to a reward", "Cross-entropy on tokens only", "KL only"], 0, "Binary cross-entropy on pairs."),
 ("What anchors the policy in DPO?", ["The frozen reference model", "The tokenizer", "The batch size", "The reward model"], 0, "Via the log-ratio."),
 ("What does the Bradley-Terry model give?", ["Preference probability from a reward gap", "Token probabilities", "KL divergence", "Gradients"], 0, "Sigmoid of the gap."),
 ("What is sigmoid(0)?", ["0.5", "0", "1", "Undefined"], 0, "Equal rewards."),
 ("Which reward changes leave Bradley-Terry unchanged?", ["Adding the same constant to all", "Doubling all", "Negating all", "Randomising"], 0, "Only gaps matter."),
 ("What does the RLHF objective maximise?", ["Expected reward minus beta times KL to the reference", "Reward only", "KL only", "Entropy only"], 0, "A regularised objective."),
 ("What is the optimal policy of that objective?", ["Reference times exp(r/beta), normalised", "The best response only", "Uniform", "The reward model"], 0, "A tilt."),
 ("What happens as beta grows large?", ["Optimal policy approaches the reference", "It becomes deterministic", "It diverges", "It becomes uniform"], 0, "The tilt vanishes."),
 ("What is Z(x)?", ["The partition function", "The reward", "The margin", "The prompt length"], 0, "Sum over all responses."),
 ("Why is Z(x) hard to compute?", ["It sums over all possible responses", "It is negative", "It is random", "It needs labels"], 0, "Intractable for language models."),
 ("What cancels in the DPO derivation?", ["log Z(x)", "beta", "The reference", "The winner"], 0, "Both responses share the prompt."),
 ("What is the implicit reward?", ["beta times the log ratio of policy to reference", "The policy probability", "The KL", "The margin"], 0, "Up to a prompt-dependent term."),
 ("What is the margin?", ["Winner's implicit reward minus loser's", "Loss minus reward", "Beta times KL", "Policy minus reference"], 0, "Positive when the pair is ranked right."),
 ("What is the DPO loss when the margin is zero?", ["ln 2", "0", "1", "Infinite"], 0, "-log 0.5."),
 ("What does the DPO gradient do to the chosen response?", ["Raises its log-probability", "Lowers it", "Ignores it", "Clips it"], 0, "And lowers the rejected one's."),
 ("When is the gradient weight large?", ["When the pair is ranked wrongly", "When it is ranked rightly", "When beta is 0", "At the end"], 0, "sigmoid(-margin)."),
 ("Why keep the dynamic weight?", ["Without it the model can degenerate", "It saves memory", "It speeds training only", "It is a rounding step"], 0, "As reported by the paper."),
 ("How is a response log-probability computed?", ["Sum of token log-probs", "Product of logits", "Mean reward", "Max token"], 0, "Chain rule in logs."),
 ("Why mask prompt tokens?", ["The prompt is given, not generated", "To save time", "To add noise", "To change beta"], 0, "Only response tokens count."),
 ("Why can reference log-probs be precomputed?", ["The reference is frozen", "They are small", "Beta is fixed", "They are random"], 0, "They never change."),
 ("What model usually serves as the reference?", ["The supervised fine-tuned model", "A random model", "The reward model", "The tokenizer"], 0, "Also the starting point."),
 ("What beta is a common starting value?", ["About 0.1", "About 100", "Exactly 0", "About 10,000"], 0, "Tuned per task."),
 ("What does a larger beta do?", ["Keeps the policy closer to the reference", "Lets it drift", "Removes the reference", "Changes the data"], 0, "Smaller moves in log-ratio terms."),
 ("What is reward accuracy?", ["Share of pairs with positive margin", "Reward model size", "Win rate", "Loss"], 0, "A training diagnostic."),
 ("Why fine-tune on preferred responses first?", ["So they are likely under the reference", "To save memory", "To remove beta", "To shorten prompts"], 0, "Reduces distribution shift."),
 ("What is likelihood displacement (background)?", ["Both chosen and rejected probabilities fall", "Only rejected rises", "Loss increases", "Beta changes"], 0, "Later analysis."),
 ("What is DPO's training regime?", ["Offline on a fixed set of pairs", "Online with fresh samples", "Unsupervised", "Reinforcement with a simulator"], 0, "No sampling loop."),
 ("What is the final evaluation metric?", ["Win rate on held-out prompts", "Training loss", "Beta", "Token count"], 0, "Compared with a baseline."),
 ("Which variant needs no reference model (background)?", ["ORPO", "DPO", "IPO", "PPO"], 0, "Odds-ratio term added to SFT."),
 ("What does KTO use (background)?", ["Single-response good or bad labels", "Pairs only", "A reward model", "A tree search"], 0, "Not pairs."),
 ("What does SimPO normalise by (background)?", ["Response length", "Beta", "The reference", "The batch size"], 0, "Average log-probability."),
 ("What does GRPO drop (background)?", ["The value model", "The policy", "The reward", "The prompts"], 0, "Group statistics instead."),
]

CFG = dict(id="dpo", title="Direct Preference Optimization (DPO)", subtitle="From RLHF to a simple preference loss, with Python labs",
    description="DPO (Rafailov et al., NeurIPS 2023) derived step by step: preference data and Bradley-Terry, the KL-regularised objective and its optimal policy, the loss, its gradient, implementation with sequence log-probabilities, choosing beta, and later variants (background). Theory plus Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="dpo", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "dpo.course.json")
    cmk.main(CFG, dpoc.CHS, [sys.argv[0], out])
