"""Reinforcement learning course, chapters 5-8: Q-learning, custom envs, deep RL/DQN, SB3 quickstart."""
from part1 import T, C

CH = []

# ---------------------------------------------------------------- 5
CH.append({
    "title": "Tabular Q-learning",
    "maps": [{"title": "Q-learning", "links": [
        "Q-table | stores | Action values",
        "Q-learning | updates | Q-table",
        "Q-learning | uses | Learning rate alpha",
        "Q-learning | uses | Discount factor [ch3]",
        "Q-learning | is | Off-policy",
        "Behavior policy | explores with | Epsilon-greedy [ch4]",
        "Q-table | needs | Small discrete spaces",
        "Large spaces [ch7] | need | Neural networks [ch7]",
        "FrozenLake | is solved with | Q-table"]}],
    "summary": [
        "Q-learning learns the action values Q(s, a) from experience. Keep a table with one row per state and one column per action. After each step, move the table entry a little toward the target: reward plus gamma times the best value in the next state.",
        "The learning rate alpha sets how big that move is. Q-learning is off-policy: it learns about the greedy policy while behaving with an exploring policy such as epsilon-greedy.",
        "Tables only work when the number of states is small and discrete, like FrozenLake with 16 states or Taxi with 500. Bigger problems need function approximation, which is the next big idea."],
    "glossary": [
        {"term": "Q-table", "def": "An array of shape (number of states, number of actions) holding the current Q estimates."},
        {"term": "Q-learning", "def": "A method that updates Q toward reward plus gamma times the maximum Q of the next state."},
        {"term": "Learning rate (alpha)", "def": "How far each update moves the estimate toward the target. Between 0 and 1."},
        {"term": "TD target", "def": "The value r + gamma * max Q(s', a') that the old estimate is nudged toward."},
        {"term": "TD error", "def": "Target minus current estimate. The size of the surprise."},
        {"term": "Off-policy", "def": "Learning about one policy (greedy) while following another (exploring)."},
        {"term": "FrozenLake", "def": "A Gymnasium grid world: reach the goal over ice without falling into holes. Slippery by default."}],
    "keyPoints": [
        "Update: Q[s,a] += alpha * (r + gamma * max(Q[s']) - Q[s,a]).",
        "At a terminal state there is no next value: the target is just r.",
        "Behave with epsilon-greedy, evaluate with greedy.",
        "Alpha around 0.1 to 0.5 and gamma around 0.9 to 0.99 are typical for small tasks.",
        "FrozenLake is slippery: the same action can move you somewhere else, so expect noisy learning.",
        "Tables do not scale: add one state variable and the table grows multiplicatively."],
    "lesson": [
        T("Q-learning is the Bellman idea turned into a learning rule. You do not need a model of the environment. You just act, watch what happens and adjust.",
          "Each experience is a tuple (s, a, r, s prime, done). From it compute a target: if the episode ended, the target is r. Otherwise it is r plus gamma times the best Q in s prime. The old estimate then moves a fraction alpha toward the target."),
        C("""import numpy as np
import gymnasium as gym

env = gym.make("FrozenLake-v1", is_slippery=False)   # deterministic version to start
n_s, n_a = env.observation_space.n, env.action_space.n
Q = np.zeros((n_s, n_a))
alpha, gamma = 0.5, 0.95
eps, eps_min, eps_decay = 1.0, 0.05, 0.999
rng = np.random.default_rng(0)

for episode in range(5000):
    s, _ = env.reset()
    done = False
    while not done:
        if rng.random() < eps:
            a = env.action_space.sample()
        else:
            a = int(np.argmax(Q[s]))
        s2, r, terminated, truncated, _ = env.step(a)
        target = r if terminated else r + gamma * np.max(Q[s2])
        Q[s, a] += alpha * (target - Q[s, a])
        s, done = s2, terminated or truncated
    eps = max(eps_min, eps * eps_decay)

policy = np.argmax(Q, axis=1)     # greedy policy: best action for each state""", "python"),
        T("Notice the line that uses terminated, not truncated, to cut off the future. A time-limit truncation should still bootstrap from the next state, because the future was not actually zero.",
          "FrozenLake action numbers are 0 left, 1 down, 2 right, 3 up. The default map is four by four with a start in the top left and a goal in the bottom right. With is_slippery=True the move only goes the intended way a third of the time, so learning needs many more episodes and the best success rate is well below 100 percent."),
        T("Why is it off-policy? The max in the target assumes you act greedily from the next state, even though you actually explored. That lets Q-learning learn the optimal values while still exploring. SARSA, a close relative, uses the action actually taken instead and is called on-policy."),
        T("Open the Gridworld Lab in the practice section. Train the agent for a few hundred episodes and watch the arrows turn toward the goal.")],
    "quiz": [
        {"q": "What is the Q-learning target for a non-terminal step?", "options": ["r", "r + gamma * max Q(s', a')", "Q(s, a)", "gamma * r"], "answer": 1, "explain": "The target adds the discounted best next value to the immediate reward."},
        {"q": "At a terminal transition the target is...", "options": ["r + gamma * max Q(s')", "r", "0 always", "Q(s, a)"], "answer": 1, "explain": "No future exists after termination, so the target is just the reward."},
        {"q": "Why is Q-learning called off-policy?", "options": ["It does not use a policy", "It learns the greedy policy while acting with an exploring one", "It only works offline", "It ignores rewards"], "answer": 1, "explain": "The max in the target is the greedy policy, while behavior can be epsilon-greedy."},
        {"q": "Which problem can a Q-table handle?", "options": ["Raw camera images", "A 16-state grid world", "A continuous torque", "A game with billions of states"], "answer": 1, "explain": "Tables need a small number of discrete states and actions."}],
    "cards": [
        {"q": "Q-learning update?", "a": "Q[s,a] += alpha * (r + gamma*max(Q[s']) - Q[s,a])"},
        {"q": "What is the TD error?", "a": "Target minus the current estimate."},
        {"q": "FrozenLake actions?", "a": "0 left, 1 down, 2 right, 3 up."},
        {"q": "Why do tables fail on big problems?", "a": "The number of states explodes and unseen states have no entries."}],
    "practice": [
        {"type": "code", "title": "The Q-learning update", "intro": "Write qUpdate(q, r, qNextMax, alpha, gamma): return the new Q value after one update.", "fn": "qUpdate",
         "starter": "function qUpdate(q, r, qNextMax, alpha, gamma) {\n  // your code\n}",
         "tests": [{"args": [0, 1, 0, 0.5, 0.9], "expect": 0.5, "approx": 0.000001}, {"args": [2, 0, 4, 0.5, 0.5], "expect": 2, "approx": 0.000001}, {"args": [1, 1, 2, 0.1, 0.5], "expect": 1.1, "approx": 0.000001}, {"args": [0, 0, 0, 0.5, 0.9], "expect": 0}],
         "hint": "target = r + gamma * qNextMax, then q + alpha * (target - q).",
         "solution": "function qUpdate(q, r, qNextMax, alpha, gamma) {\n  const target = r + gamma * qNextMax;\n  return q + alpha * (target - q);\n}"},
        {"type": "order", "title": "One Q-learning step", "intro": "Put the steps of a single Q-learning step in order.", "items": ["Choose an action with epsilon-greedy", "Step the environment and get r and the next state", "Compute the target from r and the best next Q", "Move Q[s, a] toward the target by alpha", "Set the next state as the current state"]},
        {"type": "webxdc", "title": "Gridworld Lab", "intro": "Train a tiny Q-learning agent on a grid. The goal is the star, the pit is red. Finish when the greedy path reaches the goal.", "height": 520, "html": "__GRID__"}]
})

# ---------------------------------------------------------------- 6
CH.append({
    "title": "Custom environments and wrappers",
    "maps": [{"title": "Building an environment", "links": [
        "Custom env | subclasses | gym.Env",
        "Custom env | defines | Observation space",
        "Custom env | defines | Action space",
        "Custom env | implements | reset",
        "Custom env | implements | step",
        "check_env | validates | Custom env",
        "Wrapper | modifies | Environment",
        "Wrapper | can change | Reward or observation",
        "Reward design [ch11] | affects | Learning [ch11]"]}],
    "summary": [
        "To teach an agent your own task you write a Gymnasium environment: a class that subclasses gym.Env, declares its observation and action spaces, and implements reset and step.",
        "Spaces must match the data you return exactly, including shape and dtype. Stable-Baselines3 provides check_env to catch mistakes early. Fix every warning before training, because bad environments waste hours.",
        "Wrappers add behavior around an existing environment without editing it: limit time, scale rewards, clip actions, stack frames. They are small and composable."],
    "glossary": [
        {"term": "gym.Env", "def": "Base class for environments. You subclass it and implement reset and step."},
        {"term": "observation_space", "def": "Attribute describing the shape, type and bounds of observations."},
        {"term": "action_space", "def": "Attribute describing the valid actions."},
        {"term": "check_env", "def": "SB3 helper that runs sanity checks on an environment and warns about problems."},
        {"term": "Wrapper", "def": "A class that wraps an environment and changes its inputs, outputs or rules."},
        {"term": "TimeLimit", "def": "A wrapper that truncates episodes after a maximum number of steps. Applied via max_episode_steps."},
        {"term": "info", "def": "A dictionary for extra data. The agent should not learn from it, but you can log it."}],
    "keyPoints": [
        "Subclass gym.Env, set the two spaces in __init__, implement reset and step.",
        "reset(seed=None, options=None) must call super().reset(seed=seed) and return (obs, info).",
        "step returns (obs, reward, terminated, truncated, info).",
        "Observations must match the space: same shape and dtype (float32 for Box).",
        "Run check_env(env) before training.",
        "Prefer wrappers over editing environment code when you only change data going in or out."],
    "lesson": [
        T("Here is a tiny custom environment. The agent stands on a line of cells and must walk to the right end. It is small enough to read in one go, and it follows every rule SB3 expects."),
        C("""import numpy as np
import gymnasium as gym
from gymnasium import spaces

class LineWorld(gym.Env):
    metadata = {"render_modes": ["ansi"]}

    def __init__(self, size=8, render_mode=None):
        super().__init__()
        self.size = size
        self.render_mode = render_mode
        self.action_space = spaces.Discrete(2)             # 0 = left, 1 = right
        self.observation_space = spaces.Box(0.0, 1.0, shape=(1,), dtype=np.float32)
        self.pos = 0

    def _obs(self):
        return np.array([self.pos / (self.size - 1)], dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)           # seeds self.np_random
        self.pos = 0
        return self._obs(), {}

    def step(self, action):
        self.pos = max(0, self.pos - 1) if action == 0 else self.pos + 1
        terminated = self.pos >= self.size - 1
        reward = 1.0 if terminated else -0.01     # small cost per step
        return self._obs(), reward, terminated, False, {}

    def render(self):
        if self.render_mode == "ansi":
            return "".join("A" if i == self.pos else "." for i in range(self.size))""", "python"),
        T("Check it before you train. check_env builds the checks SB3 relies on, such as whether reset and step return the right types and whether observations fit the declared space.",
          "Register the class to build it by name, or just create it directly. For a time limit use TimeLimit or register with max_episode_steps."),
        C("""from stable_baselines3.common.env_checker import check_env
env = LineWorld()
check_env(env, warn=True)          # silent means it passed

# Register to use gym.make("LineWorld-v0")
gym.register(id="LineWorld-v0", entry_point=LineWorld, max_episode_steps=50)
env = gym.make("LineWorld-v0")""", "python"),
        T("Wrappers follow a simple pattern: subclass a wrapper type, override one method. Use gym.ObservationWrapper to change what the agent sees, gym.RewardWrapper to change the reward, and gym.ActionWrapper to change actions. Because they stack, you can add them one at a time and keep each easy to test."),
        C("""class ScaleReward(gym.RewardWrapper):
    def __init__(self, env, scale=0.1):
        super().__init__(env)
        self.scale = scale
    def reward(self, reward):
        return reward * self.scale

env = ScaleReward(gym.make("CartPole-v1"), scale=0.01)""", "python"),
        T("Common bugs: observation dtype float64 when the space says float32, a reset that forgets to return info, a step that returns four values, and a Box with bounds the data goes outside. check_env finds most of these.")],
    "quiz": [
        {"q": "Which two methods must a custom Gymnasium environment implement?", "options": ["fit and predict", "reset and step", "train and test", "act and learn"], "answer": 1, "explain": "reset starts an episode and step advances it."},
        {"q": "What should reset return?", "options": ["Only the observation", "(observation, info)", "(obs, reward, done)", "Nothing"], "answer": 1, "explain": "Gymnasium reset returns a pair: the first observation and an info dictionary."},
        {"q": "Which tool checks that your environment follows the API?", "options": ["check_env", "evaluate_policy", "VecNormalize", "Monitor"], "answer": 0, "explain": "stable_baselines3.common.env_checker.check_env raises errors and warnings for common mistakes."},
        {"q": "You want to multiply every reward by 0.1 without touching the environment code. What do you use?", "options": ["A second environment", "A RewardWrapper", "A callback", "A different policy"], "answer": 1, "explain": "gym.RewardWrapper overrides reward() and leaves the wrapped environment unchanged."}],
    "cards": [
        {"q": "Minimum parts of a custom env?", "a": "Subclass gym.Env, define observation_space and action_space, implement reset and step."},
        {"q": "Why call super().reset(seed=seed)?", "a": "It seeds the environment's random generator, self.np_random."},
        {"q": "Which dtype for Box observations?", "a": "float32 is the usual choice."},
        {"q": "Three wrapper base classes?", "a": "ObservationWrapper, RewardWrapper, ActionWrapper."}],
    "practice": [
        {"type": "fill", "title": "Complete the environment", "text": "class MyEnv(gym.{{Env}}):\n    def {{reset}}(self, seed=None, options=None):\n        super().reset(seed=seed)\n        return obs, {}\n    def {{step}}(self, action):\n        return obs, reward, terminated, truncated, info\nRun {{check_env}}(env) before training."},
        {"type": "match", "title": "Match the wrapper", "intro": "Match what you want to change to the wrapper to use.", "pairs": [["Change what the agent sees", "ObservationWrapper"], ["Rescale the reward", "RewardWrapper"], ["Clip or remap actions", "ActionWrapper"], ["Stop after N steps", "TimeLimit"]]},
        {"type": "write", "title": "Fix the step", "prompt": "A step() returns: return obs, reward, done, info. Write the correct return line for Gymnasium.",
         "checks": [{"re": "obs", "msg": "returns obs"}, {"re": "reward", "msg": "returns reward"}, {"re": "terminated", "msg": "has terminated"}, {"re": "truncated", "msg": "has truncated"}, {"re": "info", "msg": "has info"}],
         "solution": "return obs, reward, terminated, truncated, info"}]
})

# ---------------------------------------------------------------- 7
CH.append({
    "title": "Deep RL and DQN",
    "maps": [{"title": "From tables to networks", "links": [
        "Large state space | breaks | Q-table [ch5]",
        "Neural network | approximates | Q function",
        "DQN | trains | Q network",
        "DQN | uses | Replay buffer",
        "DQN | uses | Target network",
        "DQN | explores with | Epsilon-greedy [ch4]",
        "Replay buffer | breaks | Correlated samples",
        "Target network | stabilizes | Training",
        "DQN [ch8] | is available in | Stable-Baselines3 [ch8]",
        "DQN | needs | Discrete actions"]}],
    "summary": [
        "When there are too many states for a table, a neural network approximates Q. It takes the observation and outputs one Q-value per action. Training is gradient descent on the TD error.",
        "Naive training is unstable because consecutive samples are correlated and the target moves as the network changes. DQN fixes this with a replay buffer, which stores past experience and trains on random mini-batches, and a target network, a slowly updated copy used to compute targets.",
        "DQN works for discrete actions only. It is exploring with epsilon-greedy, and it is the base for many improvements such as Double DQN and dueling networks."],
    "glossary": [
        {"term": "Function approximation", "def": "Using a parametric model, such as a neural network, instead of a table to represent values or policies."},
        {"term": "DQN", "def": "Deep Q-Network: Q-learning with a neural network, a replay buffer and a target network."},
        {"term": "Replay buffer", "def": "A memory of past transitions from which random mini-batches are sampled for training."},
        {"term": "Target network", "def": "A delayed copy of the Q network used to compute stable training targets."},
        {"term": "Mini-batch", "def": "A small random group of transitions used for one gradient step."},
        {"term": "Off-policy", "def": "Able to learn from old data collected by older versions of the policy, which is why a replay buffer works."},
        {"term": "Soft update", "def": "Slowly blending the online weights into the target network: target = tau * online + (1 - tau) * target."}],
    "keyPoints": [
        "Network input is the observation. Output is a Q-value for each action.",
        "Loss is the squared (or Huber) difference between Q(s, a) and the target r + gamma * max Q_target(s').",
        "Replay: store (s, a, r, s', done) and train on random samples.",
        "Target network: update it every so many steps, or blend with a small tau.",
        "DQN needs discrete actions. Use SAC, TD3 or PPO for continuous ones.",
        "Start training after the buffer has some data (learning_starts in SB3)."],
    "lesson": [
        T("A table fails when the observation is an image or a vector of real numbers. Instead of one row per state, a network learns a smooth function. Similar states get similar values, so what is learned in one place transfers to others. That is also what causes trouble: updating one state moves the values of many.",
          "Two tricks make it work. First, the replay buffer. Experiences arrive in order and neighboring steps look alike, which makes gradient steps biased. Storing them and sampling at random mixes old and new, and lets each experience be reused many times."),
        T("Second, the target network. Look at the target: r + gamma times the maximum of Q at the next state. If the same network produces both the prediction and the target, every update moves the goalpost. So the target is computed by a frozen copy that is refreshed only now and then."),
        C("""# DQN training step in outline (PyTorch style)
s, a, r, s2, done = buffer.sample(batch_size)
with torch.no_grad():
    next_q = target_net(s2).max(dim=1).values
    target = r + gamma * (1 - done) * next_q
q = q_net(s).gather(1, a.unsqueeze(1)).squeeze(1)
loss = torch.nn.functional.smooth_l1_loss(q, target)
optimizer.zero_grad(); loss.backward(); optimizer.step()
if step % target_update_interval == 0:
    target_net.load_state_dict(q_net.state_dict())""", "python"),
        T("Hyperparameters to know: the learning rate, the buffer size, the batch size, how often to update the target, how long epsilon decays, and learning_starts. In Stable-Baselines3 they are all constructor arguments of DQN.",
          "Limits: DQN overestimates values (Double DQN reduces this), it is sample hungry, and it only handles a discrete action set. For robots with continuous controls you need a different family, which chapter 9 introduces.")],
    "quiz": [
        {"q": "What does a DQN network output?", "options": ["One action", "A Q-value for each action", "The reward", "A probability of termination"], "answer": 1, "explain": "Given an observation, it predicts Q for every discrete action. The agent picks the largest."},
        {"q": "Why use a replay buffer?", "options": ["To speed up the environment", "To break correlation between consecutive samples and reuse data", "To store the policy", "To normalize rewards"], "answer": 1, "explain": "Random mini-batches from stored experience are closer to independent and each experience is reused."},
        {"q": "What is the purpose of the target network?", "options": ["To act in the environment", "To keep the learning targets stable", "To store rewards", "To pick random actions"], "answer": 1, "explain": "Targets from a frozen copy do not shift on every gradient step."},
        {"q": "Which action spaces does DQN support?", "options": ["Only continuous", "Only discrete", "Both", "Neither"], "answer": 1, "explain": "DQN takes a max over a fixed set of actions, so they must be discrete."}],
    "cards": [
        {"q": "Two tricks that make DQN stable?", "a": "A replay buffer and a target network."},
        {"q": "DQN target for a transition?", "a": "r + gamma * (1 - done) * max Q_target(s')"},
        {"q": "Soft update formula?", "a": "target = tau * online + (1 - tau) * target"},
        {"q": "When not to use DQN?", "a": "When actions are continuous."}],
    "practice": [
        {"type": "code", "title": "Soft update", "intro": "Write softUpdate(target, online, tau): return a new array where each value is tau * online + (1 - tau) * target.", "fn": "softUpdate",
         "starter": "function softUpdate(target, online, tau) {\n  // your code\n}",
         "tests": [{"args": [[1, 2], [3, 4], 0.5], "expect": [2, 3]}, {"args": [[0, 0], [10, 20], 0.1], "expect": [1, 2], "approx": 0.000001}, {"args": [[5], [9], 0], "expect": [5]}, {"args": [[5], [9], 1], "expect": [9]}],
         "hint": "Use map and index into both arrays.",
         "solution": "function softUpdate(target, online, tau) {\n  return target.map((t, i) => tau * online[i] + (1 - tau) * t);\n}"},
        {"type": "code", "title": "DQN target", "intro": "Write dqnTarget(r, gamma, done, nextQs): return r when done is true, otherwise r + gamma * the largest value in nextQs.", "fn": "dqnTarget",
         "starter": "function dqnTarget(r, gamma, done, nextQs) {\n  // your code\n}",
         "tests": [{"args": [1, 0.9, False, [1, 3, 2]], "expect": 3.7, "approx": 0.000001}, {"args": [1, 0.9, True, [1, 3, 2]], "expect": 1}, {"args": [0, 0.5, False, [-1, -2]], "expect": -0.5, "approx": 0.000001}],
         "hint": "Math.max(...nextQs) gives the largest value.",
         "solution": "function dqnTarget(r, gamma, done, nextQs) {\n  return done ? r : r + gamma * Math.max(...nextQs);\n}"},
        {"type": "match", "title": "Why each piece exists", "intro": "Match each DQN part to its job.", "pairs": [["Replay buffer", "Reuse past data and decorrelate samples"], ["Target network", "Give stable learning targets"], ["Epsilon-greedy", "Keep exploring"], ["Q network", "Predict a value per action"]]}]
})

# ---------------------------------------------------------------- 8
CH.append({
    "title": "Stable-Baselines3 quickstart",
    "maps": [{"title": "SB3 workflow", "links": [
        "Stable-Baselines3 | provides | Algorithms",
        "Algorithms | include | PPO",
        "Algorithms | include | DQN",
        "Algorithms | include | SAC",
        "Algorithm | takes | Policy and env",
        "learn | trains | Model",
        "predict | gets | Action from Model",
        "evaluate_policy | measures | Mean reward",
        "save and load | persist | Model",
        "Algorithms [ch9] | differ in | Action space support [ch9]"]}],
    "summary": [
        "Stable-Baselines3, or SB3, is a library of reliable, well-tested RL algorithms built on PyTorch. It works directly with Gymnasium environments, so training is a few lines.",
        "The core pattern: create an algorithm with a policy name and an environment, call learn with a number of timesteps, then use predict to act, evaluate_policy to measure, and save to keep the model.",
        "Install with pip install stable-baselines3, or the extras bundle for plotting and logging. Recent releases need Python 3.10 or newer and a current PyTorch."],
    "glossary": [
        {"term": "Stable-Baselines3", "def": "A PyTorch library of RL algorithms such as PPO, A2C, DQN, SAC, TD3 and DDPG."},
        {"term": "MlpPolicy", "def": "The default network for vector observations: a multilayer perceptron."},
        {"term": "learn", "def": "Method that trains the model for total_timesteps environment steps."},
        {"term": "predict", "def": "Returns an action for an observation. Use deterministic=True when evaluating."},
        {"term": "evaluate_policy", "def": "Helper that runs episodes and returns the mean and standard deviation of the episode reward."},
        {"term": "total_timesteps", "def": "Number of environment steps used for training, not the number of episodes."},
        {"term": "Vectorized environment", "def": "SB3 wraps each environment so it can run in batches. Resets happen automatically."}],
    "keyPoints": [
        "pip install stable-baselines3 (add [extra] for plotting and TensorBoard support).",
        "model = PPO(\"MlpPolicy\", env, verbose=1); model.learn(total_timesteps=...).",
        "model.predict(obs, deterministic=True) returns (action, state). Ignore the second value for feed-forward policies.",
        "evaluate_policy(model, env, n_eval_episodes=10) returns (mean_reward, std_reward).",
        "model.save(\"name\") and PPO.load(\"name\") keep and restore a model.",
        "Evaluate on a separate environment instance from the one you trained on."],
    "lesson": [
        T("This is the hello world of SB3. It trains PPO on CartPole and watches the result. It usually reaches the maximum of 500 within about fifty thousand steps."),
        C("""pip install "stable-baselines3[extra]"
""", "bash"),
        C("""import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

env = gym.make("CartPole-v1")
model = PPO("MlpPolicy", env, verbose=1, seed=0)
model.learn(total_timesteps=50_000)

eval_env = gym.make("CartPole-v1")
mean_r, std_r = evaluate_policy(model, eval_env, n_eval_episodes=10, deterministic=True)
print(f"mean reward {mean_r:.1f} +/- {std_r:.1f}")

model.save("ppo_cartpole")
del model
model = PPO.load("ppo_cartpole")""", "python"),
        T("Using the model yourself. predict takes one observation and returns an action. The second value is a recurrent state which is None for normal policies."),
        C("""env = gym.make("CartPole-v1", render_mode="human")
obs, info = env.reset()
done = False
while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
env.close()""", "python"),
        T("Behind the scenes SB3 wraps your environment in a vectorized environment and a Monitor, which records episode reward and length. The vectorized API differs slightly from Gymnasium: reset returns only observations, step returns four values and resets finished environments by itself. You see this if you call model.get_env().",
          "Switching algorithm is a one-word change. DQN for CartPole, SAC for Pendulum. The policy string stays MlpPolicy for vector inputs, CnnPolicy for images, and MultiInputPolicy for dictionary observations. Use policy_kwargs to change the network, for example policy_kwargs=dict(net_arch=[64, 64])."),
        C("""from stable_baselines3 import DQN, SAC
dqn = DQN("MlpPolicy", "CartPole-v1", verbose=0)       # a string id works as well
sac = SAC("MlpPolicy", "Pendulum-v1", verbose=0)
model = PPO("MlpPolicy", "CartPole-v1",
            policy_kwargs=dict(net_arch=[64, 64]), learning_rate=3e-4)""", "python"),
        T("Treat total_timesteps as a budget and judge the model by evaluation, not by the training log alone. Always check how the reward curve changes with different seeds. RL results vary a lot from run to run.")],
    "quiz": [
        {"q": "Which call trains an SB3 model?", "options": ["model.fit()", "model.learn(total_timesteps=...)", "model.train()", "model.run()"], "answer": 1, "explain": "SB3 uses learn with a timestep budget."},
        {"q": "What does model.predict(obs, deterministic=True) return?", "options": ["Only the action", "(action, state)", "The reward", "The next observation"], "answer": 1, "explain": "It returns the action and an optional recurrent state, which is None for normal policies."},
        {"q": "Which helper gives mean and standard deviation of episode reward?", "options": ["Monitor", "evaluate_policy", "check_env", "make_vec_env"], "answer": 1, "explain": "evaluate_policy returns (mean_reward, std_reward)."},
        {"q": "Which policy string is used for vector observations?", "options": ["CnnPolicy", "MlpPolicy", "MultiInputPolicy", "BoxPolicy"], "answer": 1, "explain": "MlpPolicy for vectors, CnnPolicy for images, MultiInputPolicy for dictionaries."}],
    "cards": [
        {"q": "Minimal SB3 training code?", "a": "model = PPO(\"MlpPolicy\", env); model.learn(total_timesteps=50_000)"},
        {"q": "How do you save and load?", "a": "model.save(\"name\") and PPO.load(\"name\")"},
        {"q": "Does total_timesteps count episodes?", "a": "No. It counts environment steps."},
        {"q": "Which policy for images?", "a": "CnnPolicy"}],
    "practice": [
        {"type": "fill", "title": "Train and test", "text": "from stable_baselines3 import {{PPO}}\nmodel = PPO(\"{{MlpPolicy}}\", env, verbose=1)\nmodel.{{learn}}(total_timesteps=50_000)\naction, _ = model.{{predict}}(obs, deterministic=True)\nmodel.{{save}}(\"my_model\")"},
        {"type": "order", "title": "The SB3 workflow", "intro": "Put the steps in the usual order.", "items": ["Create the environment", "Create the model with a policy and the environment", "Call learn with a timestep budget", "Evaluate on a separate environment", "Save the model"]},
        {"type": "terminal", "title": "Train from the shell", "intro": "A scripted shell. The output is a simulated example, not a measurement.", "prompt": "(rl-env) $", "chips": ["pip install \"stable-baselines3[extra]\"", "python train_cartpole.py", "ls"],
         "commands": [
             {"re": "^pip install \"?stable-baselines3(\\[extra\\])?\"?$", "out": ["Collecting stable-baselines3[extra]", "Installing collected packages: torch, stable-baselines3", "Successfully installed stable-baselines3 (simulated)"]},
             {"re": "^python train_cartpole\\.py$", "out": ["Using cpu device", "---------------------------------", "| rollout/           |          |", "|    ep_len_mean     | 21.3     |", "|    ep_rew_mean     | 21.3     |", "... (training) ...", "mean reward 500.0 +/- 0.0   (simulated)", "saved ppo_cartpole.zip"], "set": {"trained": "1"}},
             {"re": "^ls$", "when": {"trained": "1"}, "out": ["ppo_cartpole.zip  train_cartpole.py"]},
             {"re": "^ls$", "out": ["train_cartpole.py"]},
             {"re": "^pip", "out": ["Try: pip install \"stable-baselines3[extra]\""], "cls": "warn"}],
         "tasks": [{"text": "Install Stable-Baselines3", "cmd": "^pip install \"?stable-baselines3"}, {"text": "Run the training script", "cmd": "^python train_cartpole\\.py$"}, {"text": "List the files to see the saved model", "cmd": "^ls$"}]}]
})
