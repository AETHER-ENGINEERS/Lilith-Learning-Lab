"""Reinforcement learning course, chapters 9-12: PPO and friends, training in practice, reward design, next steps."""
from part1 import T, C

CH = []

# ---------------------------------------------------------------- 9
CH.append({
    "title": "Policy gradients, PPO and choosing an algorithm",
    "maps": [{"title": "Algorithm families", "links": [
        "Value-based | includes | DQN [ch7]",
        "Policy-based | includes | Policy gradient",
        "Actor-critic | combines | Policy and value",
        "Actor-critic | includes | A2C",
        "Actor-critic | includes | PPO",
        "PPO | limits | Policy change per update",
        "SAC | handles | Continuous actions",
        "TD3 | handles | Continuous actions",
        "On-policy | reuses data | Rarely",
        "Off-policy | reuses data | Often via replay buffer [ch7]"]}],
    "summary": [
        "Value-based methods such as DQN learn Q and act greedily. Policy-gradient methods learn the policy directly: they nudge the probability of actions up when they led to a high return and down when they led to a low one.",
        "Actor-critic methods add a critic, a value function that tells how much better an action was than expected. That difference is called the advantage and it reduces noise. A2C and PPO are actor-critic methods.",
        "PPO, proximal policy optimization, clips the update so the new policy stays close to the old one. It is simple, stable, works for discrete and continuous actions, and is a strong default. For continuous control SAC and TD3 are often more sample efficient."],
    "glossary": [
        {"term": "Policy gradient", "def": "A method that adjusts policy parameters in the direction that increases expected return."},
        {"term": "Actor", "def": "The part of the agent that chooses actions, the policy network."},
        {"term": "Critic", "def": "The part that estimates values, used to judge the actor's actions."},
        {"term": "Advantage", "def": "How much better an action was than the average action in that state: Q minus V."},
        {"term": "PPO", "def": "Proximal Policy Optimization. Policy gradient with a clipped objective that keeps updates small."},
        {"term": "On-policy", "def": "Learns only from data gathered by the current policy, so old data is thrown away."},
        {"term": "Entropy bonus", "def": "A reward for keeping the policy random enough, to encourage exploration."},
        {"term": "SAC", "def": "Soft Actor-Critic: an off-policy actor-critic for continuous actions that maximizes reward plus entropy."}],
    "keyPoints": [
        "PPO and A2C are on-policy. DQN, SAC, TD3 and DDPG are off-policy.",
        "DQN: discrete actions only. SAC, TD3, DDPG: continuous only. PPO and A2C: both.",
        "PPO clip objective: min(ratio * A, clip(ratio, 1 - eps, 1 + eps) * A). Typical eps is 0.2.",
        "Start with PPO. Try SAC for continuous control when samples are expensive.",
        "On-policy methods usually want many parallel environments.",
        "Advantage estimates (GAE) trade bias against variance with lambda, typically 0.95."],
    "lesson": [
        T("A policy-gradient agent uses a network that outputs action probabilities. After running some episodes you increase the probability of each action in proportion to how good the outcome was. The idea is called REINFORCE. It is simple and noisy, because a single lucky episode can push the policy the wrong way."),
        T("To cut the noise, subtract a baseline. If the average outcome in a state is 10 and this action gave 12, the advantage is plus 2, and the action becomes more likely. If it gave 8, it becomes less likely. The critic network learns that baseline V(s). Together the actor and the critic form an actor-critic."),
        T("The danger with policy gradients is a step too big. One bad update can wreck the policy, and since the new data comes from the new policy, it may never recover. PPO guards against this. It computes the ratio of the new probability to the old one for each action and clips it to the range 1 minus epsilon to 1 plus epsilon, so there is no gain from moving further than that."),
        C("""# PPO clipped objective for one sample (maximize this)
ratio = new_prob / old_prob
clipped = max(1 - eps, min(ratio, 1 + eps))
objective = min(ratio * advantage, clipped * advantage)""", "python"),
        T("Each PPO iteration collects n_steps from each environment, then runs several epochs of mini-batch updates on that data, then throws it away. That is on-policy learning. The defaults in SB3 are n_steps 2048, batch_size 64, n_epochs 10, gamma 0.99, gae_lambda 0.95 and clip_range 0.2, which work well for many problems."),
        T("How to choose?"),
        C("""Algorithm | Actions            | Data      | Notes
PPO       | discrete, continuous | on-policy | strong default, parallel envs
A2C       | discrete, continuous | on-policy | simple, fast, noisier
DQN       | discrete             | off-policy| image games, replay buffer
SAC       | continuous           | off-policy| sample efficient, robust
TD3       | continuous           | off-policy| deterministic, careful tuning
DDPG      | continuous           | off-policy| older, sensitive""", "text"),
        T("SB3 gives all of these under the same interface. Extra algorithms live in the sb3-contrib package, for example recurrent PPO, TRPO and QR-DQN.")],
    "quiz": [
        {"q": "What does the critic in an actor-critic estimate?", "options": ["The next action", "A value function", "The reward function", "The environment dynamics"], "answer": 1, "explain": "The critic estimates values, which gives a baseline for judging actions."},
        {"q": "Which algorithm is limited to discrete action spaces?", "options": ["PPO", "SAC", "DQN", "A2C"], "answer": 2, "explain": "DQN takes a max over a fixed set of actions. SAC is continuous only."},
        {"q": "What does PPO's clipping accomplish?", "options": ["It clips the rewards", "It limits how far the new policy can move from the old one", "It limits the episode length", "It limits the replay buffer"], "answer": 1, "explain": "Clipping the probability ratio removes the incentive for large policy changes."},
        {"q": "You have a continuous-control robot task with expensive samples. Which is a sensible first thing to try besides PPO?", "options": ["DQN", "SAC", "Q-table", "Bandit"], "answer": 1, "explain": "SAC is off-policy and reuses data, so it is often more sample efficient on continuous control."}],
    "cards": [
        {"q": "Advantage in words?", "a": "How much better an action was than average for that state."},
        {"q": "On-policy vs off-policy?", "a": "On-policy learns from the current policy's data only. Off-policy can reuse older data."},
        {"q": "PPO clip range default?", "a": "0.2"},
        {"q": "Default algorithm to try first?", "a": "PPO."}],
    "practice": [
        {"type": "code", "title": "PPO clipped objective", "intro": "Write ppoObjective(ratio, adv, eps): min(ratio * adv, clip(ratio, 1 - eps, 1 + eps) * adv).", "fn": "ppoObjective",
         "starter": "function ppoObjective(ratio, adv, eps) {\n  // your code\n}",
         "tests": [{"args": [1.5, 1, 0.2], "expect": 1.2, "approx": 0.000001}, {"args": [0.5, 1, 0.2], "expect": 0.5, "approx": 0.000001}, {"args": [1.5, -1, 0.2], "expect": -1.5, "approx": 0.000001}, {"args": [0.5, -1, 0.2], "expect": -0.8, "approx": 0.000001}, {"args": [1, 3, 0.2], "expect": 3}],
         "hint": "Clip the ratio with Math.max(1 - eps, Math.min(ratio, 1 + eps)).",
         "solution": "function ppoObjective(ratio, adv, eps) {\n  const clipped = Math.max(1 - eps, Math.min(ratio, 1 + eps));\n  return Math.min(ratio * adv, clipped * adv);\n}"},
        {"type": "code", "title": "Advantage", "intro": "Write advantage(r, gamma, vNext, v): the one-step advantage r + gamma * vNext - v.", "fn": "advantage",
         "starter": "function advantage(r, gamma, vNext, v) {\n  // your code\n}",
         "tests": [{"args": [1, 0.9, 10, 9], "expect": 1, "approx": 0.000001}, {"args": [0, 0.5, 4, 3], "expect": -1, "approx": 0.000001}, {"args": [2, 1, 0, 2], "expect": 0}],
         "hint": "It is the TD target minus the current value.",
         "solution": "function advantage(r, gamma, vNext, v) {\n  return r + gamma * vNext - v;\n}"},
        {"type": "match", "title": "Pick the algorithm", "intro": "Match each situation to a sensible algorithm.", "pairs": [["Discrete actions, image input, replay buffer", "DQN"], ["Continuous control, sample efficient", "SAC"], ["Safe default for most tasks", "PPO"], ["Recurrent policy extra", "sb3-contrib RecurrentPPO"]]}]
})

# ---------------------------------------------------------------- 10
CH.append({
    "title": "Training in practice: vector envs, callbacks and logging",
    "maps": [{"title": "A real training setup", "links": [
        "make_vec_env | creates | Parallel environments",
        "Monitor | records | Episode reward",
        "EvalCallback | evaluates | Model during training",
        "EvalCallback | saves | Best model",
        "CheckpointCallback | saves | Regular snapshots",
        "TensorBoard | shows | Training curves",
        "VecNormalize | normalizes | Observations and rewards",
        "Seeds | make runs | Reproducible",
        "Reward design [ch11] | decides | What is learned [ch11]"]}],
    "summary": [
        "Real projects train many environments in parallel with make_vec_env, evaluate on a separate environment, save the best model and log curves to TensorBoard. SB3's callbacks do the periodic work without you rewriting the training loop.",
        "Always use a Monitor so episode reward and length are recorded, a separate evaluation environment so you test what you train, and several random seeds because RL results vary widely between runs.",
        "VecNormalize normalizes observations and rewards, which helps in many continuous control tasks. If you use it, save and load its statistics together with the model."],
    "glossary": [
        {"term": "make_vec_env", "def": "Helper that builds several copies of an environment, each wrapped with a Monitor."},
        {"term": "DummyVecEnv", "def": "Runs several environments one after another in a single process."},
        {"term": "SubprocVecEnv", "def": "Runs each environment in its own process for real parallelism."},
        {"term": "Callback", "def": "An object whose methods are called during training, for example to evaluate or save."},
        {"term": "EvalCallback", "def": "Evaluates the model every eval_freq steps and can save the best model."},
        {"term": "TensorBoard", "def": "A web dashboard for training curves. Enable it with tensorboard_log."},
        {"term": "VecNormalize", "def": "A wrapper that keeps running statistics to normalize observations and rewards."},
        {"term": "Seed", "def": "A number that fixes random choices so a run can be repeated."}],
    "keyPoints": [
        "Use make_vec_env(\"CartPole-v1\", n_envs=8) to collect data faster.",
        "Evaluate on a separate environment, not the training one.",
        "EvalCallback(eval_env, best_model_save_path=..., eval_freq=...) keeps the best model.",
        "Log with tensorboard_log=\"./tb\" and view with tensorboard --logdir ./tb.",
        "Run at least 3 to 5 seeds before believing a result.",
        "When using VecNormalize, save it: env.save(\"vecnormalize.pkl\") and load it for evaluation with training=False."],
    "lesson": [
        T("Here is a complete small training script with the features you will want in any project. Read it top to bottom."),
        C("""from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback, StopTrainingOnRewardThreshold
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
import gymnasium as gym

if __name__ == "__main__":                       # needed for SubprocVecEnv on Windows and macOS
    train_env = make_vec_env("CartPole-v1", n_envs=8, seed=0)
    eval_env = Monitor(gym.make("CartPole-v1"))

    stop = StopTrainingOnRewardThreshold(reward_threshold=475, verbose=1)
    evalcb = EvalCallback(eval_env, callback_on_new_best=stop,
                          best_model_save_path="./best/", log_path="./logs/",
                          eval_freq=5_000, n_eval_episodes=10, deterministic=True)
    ckpt = CheckpointCallback(save_freq=20_000, save_path="./ckpt/", name_prefix="ppo_cp")

    model = PPO("MlpPolicy", train_env, tensorboard_log="./tb/", seed=0, verbose=1)
    model.learn(total_timesteps=200_000, callback=[evalcb, ckpt])

    best = PPO.load("./best/best_model")
    print(evaluate_policy(best, eval_env, n_eval_episodes=20))""", "python"),
        T("Note about eval_freq. With 8 parallel environments, eval_freq counts calls of the callback, which happen once per step of every environment together. To evaluate every N total timesteps divide by the number of environments: eval_freq = max(N // n_envs, 1).",
          "To watch training run tensorboard in a second terminal."),
        C("""pip install tensorboard
tensorboard --logdir ./tb/
# then open http://localhost:6006""", "bash"),
        T("Things to watch on the curves: ep_rew_mean should rise. For PPO, approx_kl and clip_fraction show how big updates are, explained_variance shows how well the critic predicts returns, and entropy_loss shows whether the policy has become too deterministic too early. A flat or falling ep_rew_mean over a long time is a sign to check rewards, learning rate and seeds."),
        T("Normalization. Reward scales and observation ranges vary wildly between tasks. VecNormalize keeps running averages and rescales. Remember that the statistics are part of the model: evaluating without them gives bad results."),
        C("""from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize

venv = VecNormalize(DummyVecEnv([lambda: gym.make("Pendulum-v1")]), norm_obs=True, norm_reward=True)
model = SAC("MlpPolicy", venv).learn(50_000)
model.save("sac_pendulum"); venv.save("vecnormalize.pkl")

# later, for evaluation
venv = VecNormalize.load("vecnormalize.pkl", DummyVecEnv([lambda: gym.make("Pendulum-v1")]))
venv.training = False; venv.norm_reward = False""", "python"),
        T("Reproducibility. Pass seed to the algorithm and to make_vec_env, and expect small differences anyway on GPU. For reporting, run several seeds and show the mean with its spread. Compare algorithms with the same budget of timesteps.")],
    "quiz": [
        {"q": "Why evaluate on a separate environment?", "options": ["It is faster", "Training environments may carry exploration state and wrappers that bias the result", "SB3 requires it to run", "To use more memory"], "answer": 1, "explain": "A separate evaluation environment lets you measure the deterministic policy cleanly, without training-time noise and stateful wrappers."},
        {"q": "Which callback saves the best model found so far?", "options": ["CheckpointCallback", "EvalCallback with best_model_save_path", "ProgressBarCallback", "StopTrainingOnMaxEpisodes"], "answer": 1, "explain": "EvalCallback evaluates periodically and keeps the best model on disk."},
        {"q": "How do you enable TensorBoard logging in SB3?", "options": ["verbose=2", "tensorboard_log=\"./tb/\"", "log=True", "It cannot be done"], "answer": 1, "explain": "Give the algorithm a tensorboard_log directory and run tensorboard on it."},
        {"q": "You used VecNormalize in training. What must you do for evaluation?", "options": ["Nothing", "Load the saved normalization statistics and set training to False", "Retrain the model", "Remove the model"], "answer": 1, "explain": "The statistics belong to the model. Save and reload them, and stop updating them in evaluation."}],
    "cards": [
        {"q": "How many envs for PPO?", "a": "Often 4 to 16 parallel environments, via make_vec_env(n_envs=...)."},
        {"q": "Which wrapper records episode reward?", "a": "Monitor."},
        {"q": "How to watch curves?", "a": "tensorboard --logdir ./tb/"},
        {"q": "How many seeds before trusting a result?", "a": "At least 3 to 5."}],
    "practice": [
        {"type": "fill", "title": "Set up training", "text": "env = {{make_vec_env}}(\"CartPole-v1\", n_envs=8)\nevalcb = {{EvalCallback}}(eval_env, best_model_save_path=\"./best/\", eval_freq=5000)\nmodel = PPO(\"MlpPolicy\", env, tensorboard_log=\"{{./tb/|./tb|tb}}\")\nmodel.learn(total_timesteps=200_000, callback={{evalcb}})"},
        {"type": "terminal", "title": "Check your training", "intro": "A scripted shell with simulated output.", "prompt": "(rl-env) $", "chips": ["python train.py", "tensorboard --logdir ./tb/", "ls best"],
         "commands": [
             {"re": "^python train\\.py$", "out": ["Using cpu device", "Eval num_timesteps=5000, episode_reward=123.40 +/- 20.10", "New best mean reward!", "... (simulated) ...", "Stopping training because the mean reward 500.00 is above the threshold 475.00"], "set": {"ran": "1"}},
             {"re": "^tensorboard --logdir \\./tb/?$", "out": ["TensorBoard 2.x at http://localhost:6006/ (Press CTRL+C to quit)"]},
             {"re": "^ls best$", "when": {"ran": "1"}, "out": ["best_model.zip"]},
             {"re": "^ls best$", "out": ["ls: cannot access 'best': run train.py first"], "cls": "warn"}],
         "tasks": [{"text": "Run train.py", "cmd": "^python train\\.py$"}, {"text": "Start TensorBoard", "cmd": "^tensorboard --logdir"}, {"text": "Check the best model was saved", "cmd": "^ls best$"}]},
        {"type": "write", "title": "Evaluate every 10000 steps", "prompt": "You train with n_envs=8 and want an evaluation every 10000 total timesteps. Write the eval_freq expression.",
         "checks": [{"re": "10000|10_000", "msg": "uses 10000"}, {"re": "//|/\\s*n_envs|/\\s*8", "msg": "divides by the number of envs"}, {"re": "n_envs|8", "msg": "uses the number of envs"}],
         "solution": "eval_freq = max(10_000 // n_envs, 1)"}]
})

# ---------------------------------------------------------------- 11
CH.append({
    "title": "Reward design, debugging and pitfalls",
    "maps": [{"title": "Why training fails", "links": [
        "Reward design | decides | What the agent learns",
        "Sparse reward | makes | Learning slow",
        "Reward shaping | adds | Intermediate rewards",
        "Bad shaping | causes | Reward hacking",
        "Bug in env | looks like | Bad algorithm",
        "check_env [ch6] | catches | Interface bugs",
        "Evaluation | needs | Several seeds [ch10]",
        "Hyperparameters | need | Systematic tuning"]}],
    "summary": [
        "An agent optimizes exactly the reward you wrote, not the one you meant. A badly designed reward gets exploited: the agent finds a loophole that scores high without doing the task. This is called reward hacking or specification gaming.",
        "Sparse rewards, where feedback comes only at the very end, make learning slow. Reward shaping adds intermediate signals, but it must reward progress toward the real goal and not creative shortcuts. Potential-based shaping is the safe form.",
        "When training fails, suspect the environment and the reward first, then the observation scaling, then the hyperparameters, and only then the algorithm. A short checklist and small test environments save time."],
    "glossary": [
        {"term": "Reward shaping", "def": "Adding extra reward signals that guide the agent toward the goal."},
        {"term": "Sparse reward", "def": "A reward that is zero almost everywhere and nonzero only on success."},
        {"term": "Reward hacking", "def": "When the agent exploits a loophole in the reward to score high without solving the task."},
        {"term": "Potential-based shaping", "def": "Shaping of the form gamma * phi(s') - phi(s). It does not change the best policy."},
        {"term": "Curriculum", "def": "Starting with easy versions of a task and making it harder as the agent improves."},
        {"term": "Overfitting to a seed", "def": "Performing well only on the starting states or random numbers seen in training."},
        {"term": "Hyperparameter", "def": "A setting chosen by you, not learned, such as the learning rate or n_steps."}],
    "keyPoints": [
        "Write the reward for the outcome you want, then ask how it could be gamed.",
        "Dense hints help, but mistakes in shaping teach the wrong behavior.",
        "Log and watch the agent. Plot an episode, render a video, read the numbers.",
        "Test the environment by hand before training: step with fixed actions and check rewards.",
        "Solve a smaller version of the task first.",
        "Change one thing at a time and keep the seed fixed when comparing."],
    "lesson": [
        T("The classic story is a boat racing game where the agent learned to spin in circles collecting small bonus items, scoring higher than any agent that finished the race. The reward said points, not finish. The agent did what the reward said.",
          "A simpler example: a cleaning robot rewarded for dust collected could learn to dump dust and re-collect it. A walking robot rewarded for forward speed might learn to fall forward as fast as it can. These are not bugs in the learning algorithm. They are bugs in the reward."),
        T("Sparse rewards are the opposite problem. In a maze with a reward only at the exit, a random agent might never find it, and nothing is learned. Shaping adds hints, such as a small reward for getting closer to the goal. Do it carefully. If you reward distance reduction and also forget a penalty for loops, the agent can step back and forth forever collecting points.",
          "The safe version is potential-based shaping. Define a potential phi(s), for example minus the distance to the goal. Add gamma times phi of the next state minus phi of the current state to the reward. Stepping away costs exactly what stepping back gains, so loops give nothing, and the best policy is unchanged."),
        C("""# Potential-based shaping inside step()
def phi(pos):             # potential: higher is closer to the goal
    return -abs(self.goal - pos)

shaped = reward + self.gamma * phi(new_pos) - phi(old_pos)""", "python"),
        T("A debugging checklist. First, run check_env and fix every warning. Second, step the environment by hand with a fixed action list and read the rewards and flags."),
        T("Third, confirm that a trivial policy, such as always going right in LineWorld, gets the reward you expect.",
          "Fourth, look at observation scale: values near zero to one or minus one to one train faster than values in the thousands.",
          "Fifth, try a known-good algorithm on a known-good environment to check your install. Sixth, only then tune the learning rate, the n_steps or the network size."),
        T("Other pitfalls. Reporting one lucky seed. Evaluating with exploration noise on. Mixing up terminated and truncated in a custom environment. Training for too few steps: CartPole takes thousands, Atari takes millions. Using a policy trained with VecNormalize without the saved statistics. A reward whose scale is so large that gradients explode.",
          "Finally, remember the safety side: an agent in the real world will exploit unexpected loopholes in the real world. Test in simulation, add limits and keep a human in the loop.")],
    "quiz": [
        {"q": "What is reward hacking?", "options": ["Stealing data", "The agent exploits a loophole to score high without doing the task", "A faster algorithm", "Increasing gamma"], "answer": 1, "explain": "The agent optimizes the reward as written, which may not match what you intended."},
        {"q": "Why is potential-based shaping considered safe?", "options": ["It makes rewards bigger", "It does not change which policy is best", "It removes exploration", "It removes randomness"], "answer": 1, "explain": "The extra terms cancel along any cycle, so the optimal policy stays the same."},
        {"q": "Training is not working. What should you check first?", "options": ["Buy a GPU", "Environment and reward correctness", "Try a different library", "Increase total_timesteps tenfold"], "answer": 1, "explain": "Most failures are environment or reward bugs. Check them before the algorithm."},
        {"q": "A maze gives reward only at the exit and a random agent never finds it. What is this called?", "options": ["Dense reward", "Sparse reward", "Negative reward", "Delayed discount"], "answer": 1, "explain": "A sparse reward gives almost no learning signal until the goal is reached by chance."}],
    "cards": [
        {"q": "Potential-based shaping formula?", "a": "F = gamma * phi(s') - phi(s)"},
        {"q": "Reward hacking in one line?", "a": "Agent scores high by exploiting the reward, not by solving the task."},
        {"q": "First debugging step?", "a": "check_env, then step the env by hand and read the rewards."},
        {"q": "Why several seeds?", "a": "RL results vary a lot between runs."}],
    "practice": [
        {"type": "code", "title": "Potential-based shaping", "intro": "Write shapedReward(r, gamma, phiNext, phi): r + gamma * phiNext - phi.", "fn": "shapedReward",
         "starter": "function shapedReward(r, gamma, phiNext, phi) {\n  // your code\n}",
         "tests": [{"args": [0, 0.9, -1, -2], "expect": 1.1, "approx": 0.000001}, {"args": [0, 1, -2, -1], "expect": -1}, {"args": [1, 0.5, 4, 2], "expect": 1}, {"args": [0, 0.99, 0, 0], "expect": 0}],
         "hint": "Moving to a state with higher potential should give a positive bonus.",
         "solution": "function shapedReward(r, gamma, phiNext, phi) {\n  return r + gamma * phiNext - phi;\n}"},
        {"type": "match", "title": "Name the problem", "intro": "Match the symptom to the likely cause.", "pairs": [["Reward is zero everywhere for a long time", "Sparse reward"], ["Agent loops to farm points", "Reward hacking from bad shaping"], ["Great on one seed, poor on others", "Overfitting or luck: use more seeds"], ["Warnings from check_env", "Interface bug in the environment"]]},
        {"type": "order", "title": "Debugging order", "intro": "Put the debugging steps in a sensible order.", "items": ["Run check_env and fix warnings", "Step the environment by hand and read the rewards", "Check observation scale", "Try a known-good algorithm on a known-good environment", "Tune hyperparameters"]}]
})

# ---------------------------------------------------------------- 12
CH.append({
    "title": "Where to go next",
    "maps": [{"title": "After the basics", "links": [
        "Continuous control [ch9] | uses | SAC and TD3 [ch9]",
        "Robotics | uses | MuJoCo and Isaac",
        "Atari | uses | CnnPolicy and frame stacking",
        "RL Zoo | provides | Tuned hyperparameters",
        "sb3-contrib | adds | More algorithms",
        "Multi-agent RL | extends | Single agent RL",
        "Offline RL | learns from | Fixed datasets",
        "RLHF | trains | Language models"]}],
    "summary": [
        "You now know the loop, the math, tabular and deep value learning, policy gradients, the SB3 toolkit and how to build and debug environments. The best next step is to build something of your own.",
        "Useful extensions: continuous control tasks with SAC, image-based tasks with CnnPolicy, the RL Zoo for tuned hyperparameters and training scripts, sb3-contrib for extra algorithms, and multi-agent and offline RL when your problem calls for it.",
        "Plan a project: choose a small environment, make a baseline, define the evaluation, and improve one thing at a time."],
    "glossary": [
        {"term": "RL Zoo", "def": "A training framework with tuned hyperparameters and scripts for many environments, built on SB3."},
        {"term": "sb3-contrib", "def": "A companion package with additional algorithms such as RecurrentPPO, TRPO and QR-DQN."},
        {"term": "Frame stacking", "def": "Giving the agent the last few frames as one observation so it can sense motion."},
        {"term": "Multi-agent RL", "def": "Several agents learn at once in a shared environment, cooperating or competing."},
        {"term": "Offline RL", "def": "Learning a policy from a fixed dataset without interacting with the environment."},
        {"term": "Sim-to-real", "def": "Training in simulation and transferring the policy to a physical system."},
        {"term": "RLHF", "def": "Reinforcement learning from human feedback, used to fine-tune language models."}],
    "keyPoints": [
        "Keep a baseline and change one thing at a time.",
        "For images use CnnPolicy and frame stacking (VecFrameStack).",
        "Use the RL Zoo for known-good hyperparameters.",
        "Real systems need safety limits and careful reward checks.",
        "Read the SB3 docs on algorithms and tips, and read the original papers once you have the habit.",
        "Share environments and models you build so others can check them."],
    "lesson": [
        T("Suggested projects, in rising difficulty: a grid or line world of your own with Q-learning; a custom environment trained with PPO; Pendulum or MountainCarContinuous with SAC; LunarLander with PPO or DQN; an Atari game with CnnPolicy; a robotics simulation. At each step write down what you expect before running."),
        C("""# Image-based environment sketch with SB3
from stable_baselines3.common.env_util import make_atari_env
from stable_baselines3.common.vec_env import VecFrameStack
env = make_atari_env("PongNoFrameskip-v4", n_envs=8, seed=0)
env = VecFrameStack(env, n_stack=4)
model = PPO("CnnPolicy", env, verbose=1)""", "python"),
        T("Atari needs extra packages (the ale-py package and the ROM license acceptance that comes with it) and a lot of training steps, often millions, so a GPU helps. Check the current installation notes before starting.",
          "For continuous control the RL Zoo contains tuned settings such as network size, learning rate and noise choices for many tasks. Start with those rather than guessing."),
        T("How to keep learning. Keep a notebook of experiments: environment version, algorithm, hyperparameters, seed and result. Reproduce a published result before inventing your own. When you hit something odd, shrink the problem until you can explain it.",
          "Thank you for learning with Lilith. Use the final exam to check yourself, and revisit the chapters where your score was lowest.")],
    "quiz": [
        {"q": "Which policy type is used for image observations?", "options": ["MlpPolicy", "CnnPolicy", "BoxPolicy", "TablePolicy"], "answer": 1, "explain": "CnnPolicy uses a convolutional network for images."},
        {"q": "Where can you find tuned hyperparameters for many environments?", "options": ["RL Zoo", "numpy", "Pillow", "pip"], "answer": 0, "explain": "The RL Baselines3 Zoo provides tuned configs and training scripts."},
        {"q": "Why stack frames for an Atari agent?", "options": ["To reduce memory", "So it can perceive motion", "To increase reward", "To make training deterministic"], "answer": 1, "explain": "A single frame hides velocity. Several frames reveal motion."},
        {"q": "What is offline RL?", "options": ["RL without a computer", "Learning from a fixed dataset without new interaction", "RL with no rewards", "Training on a phone"], "answer": 1, "explain": "Offline RL uses logged data only."}],
    "cards": [
        {"q": "Good first project?", "a": "A tiny custom environment solved with PPO."},
        {"q": "Where are extra algorithms?", "a": "The sb3-contrib package."},
        {"q": "Which wrapper stacks frames?", "a": "VecFrameStack"},
        {"q": "Key habit for experiments?", "a": "Log environment, algorithm, hyperparameters, seed and result."}],
    "practice": [
        {"type": "order", "title": "Plan a project", "intro": "Put the project steps in a good order.", "items": ["Pick a small environment", "Run a random policy as a baseline", "Train a default PPO", "Evaluate over several seeds", "Change one thing and compare"]},
        {"type": "write", "title": "Your next project", "prompt": "In one or two sentences, name an environment you will try next and which algorithm you will use. Include one of: PPO, SAC, DQN.",
         "checks": [{"re": "PPO|SAC|DQN", "msg": "names an algorithm"}, {"re": ".{20,}", "msg": "has a real sentence"}],
         "solution": "I will try Pendulum-v1 with SAC and compare it to PPO over three seeds."}]
})
