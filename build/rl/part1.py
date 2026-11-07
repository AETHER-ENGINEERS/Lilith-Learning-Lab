"""Reinforcement learning course, chapters 1-4: what RL is, Gymnasium, MDPs, exploration."""


def T(*items):
    return {"type": "text", "items": list(items)}


def C(code, lang="python"):
    return {"type": "code", "lang": lang, "code": code.strip("\n")}


CH = []

# ---------------------------------------------------------------- 1
CH.append({
    "title": "What is reinforcement learning?",
    "maps": [{"title": "The RL loop", "links": [
        "Agent | observes | State",
        "Agent | chooses | Action",
        "Action | changes | Environment",
        "Environment | returns | Reward",
        "Environment | returns | Next state",
        "Reward | shapes | Policy",
        "Policy | picks | Action",
        "Agent | wants to maximize | Return",
        "Environment [ch2] | is made with | Gymnasium [ch2]",
        "Policy [ch8] | is trained by | Stable-Baselines3 [ch8]"]}],
    "summary": [
        "Reinforcement learning, or RL, is learning by trial and error. An agent takes actions in an environment, gets a reward signal, and slowly learns which actions lead to more reward over time.",
        "Nobody gives the agent the right answers. Unlike supervised learning there are no labels, only a score that arrives after the fact, often delayed. The agent must work out which of its earlier actions deserve the credit or the blame.",
        "In this course you learn the ideas first, then practice them in Python with Gymnasium, which provides environments, and Stable-Baselines3, which provides ready-made algorithms."],
    "glossary": [
        {"term": "Agent", "def": "The learner and decision maker. In code it is usually a policy plus a learning algorithm."},
        {"term": "Environment", "def": "Everything the agent interacts with. It reacts to actions and produces observations and rewards."},
        {"term": "Observation", "def": "What the agent actually sees at a step. Often called the state when it contains everything that matters."},
        {"term": "Action", "def": "A choice the agent makes, such as push left or push right."},
        {"term": "Reward", "def": "A single number the environment sends after each step. It says how good that step was."},
        {"term": "Policy", "def": "The agent's rule for choosing actions from observations. Learning means improving the policy."},
        {"term": "Return", "def": "The total reward collected over time. The agent tries to maximize it, not just the next reward."},
        {"term": "Episode", "def": "One run from a start state until the task ends, for example one game."}],
    "keyPoints": [
        "RL learns from rewards, not from labeled examples.",
        "The loop is: observe, act, receive reward and next observation, repeat.",
        "The goal is a high total return over time, not a high immediate reward.",
        "Rewards can be delayed, so credit assignment is the hard part.",
        "The agent must explore to find good actions, and exploit what it already knows."],
    "lesson": [
        T("Imagine teaching a dog a trick. You cannot explain it in words. You wait for a good attempt and give a treat. Over many tries the dog connects what it did with the treat. That is reinforcement learning in one picture: the dog is the agent, the room is the environment, the treat is the reward.",
          "Compare this with supervised learning. There, every example comes with the correct answer, like a photo labeled cat. In RL nobody tells the agent the correct move. It only learns afterwards whether things went well, and the result of an action can show up many steps later. A chess move may only prove good or bad twenty moves on."),
        C("""# The whole RL idea as pseudo-Python
observation = env.reset()
done = False
total = 0
while not done:
    action = policy(observation)          # the agent decides
    observation, reward, done = env.step(action)   # the world answers
    total += reward                       # keep score
# learning = changing policy so that total goes up next time""", "python"),
        T("Where is RL used? Game playing, robot control, recommendation and ad systems, data center cooling, chip layout, and training language models from human feedback. It shines when you can simulate or safely try things many times, and when the right behavior is easier to score than to describe.",
          "It is also hard. Rewards can be sparse, training can be unstable, and a clever agent will happily exploit a badly designed reward. Later chapters show how to spot and manage this."),
        T("Course plan. First the ideas: Gymnasium environments, the Markov decision process, exploration, and tabular Q-learning. Then deep RL with neural networks. Then Stable-Baselines3: PPO, DQN, SAC, evaluation, callbacks, logging and your own environments.")],
    "quiz": [
        {"q": "What does an RL agent receive after each action?", "options": ["The correct action label", "A reward and a new observation", "A copy of the dataset", "Only the final score at the end of training"], "answer": 1, "explain": "The environment returns a reward and the next observation. There are no correct-answer labels."},
        {"q": "Which statement best separates RL from supervised learning?", "options": ["RL needs more data", "RL uses neural networks and supervised learning does not", "RL learns from rewards for its own actions instead of labeled answers", "RL cannot be used in simulation"], "answer": 2, "explain": "In RL the agent generates its own experience and is scored on it. Supervised learning is given labeled examples."},
        {"q": "What does the agent try to maximize?", "options": ["The next single reward", "The number of actions", "The total return over time", "The size of its model"], "answer": 2, "explain": "A good agent trades a small reward now for larger rewards later. Return is the total over time."},
        {"q": "Why is credit assignment hard?", "options": ["Rewards are always negative", "A reward may come long after the action that caused it", "Agents cannot remember", "Environments are always random"], "answer": 1, "explain": "With delayed rewards the agent must work out which of many earlier actions mattered."}],
    "cards": [
        {"q": "What are the two things the environment returns each step?", "a": "A reward and the next observation."},
        {"q": "What is a policy?", "a": "The agent's rule for choosing an action from an observation."},
        {"q": "What is an episode?", "a": "One run from the start of a task until it ends."},
        {"q": "Why can't RL just use labels?", "a": "Nobody knows the right action in advance. Only the outcome is scored."}],
    "practice": [
        {"type": "match", "title": "Match the RL words", "intro": "Match each term to what it means.",
         "pairs": [["Agent", "The learner that chooses actions"], ["Environment", "The world that reacts to actions"], ["Reward", "A number saying how good the last step was"], ["Policy", "A rule that picks actions from observations"], ["Return", "Total reward collected over time"]]},
        {"type": "order", "title": "One step of the loop", "intro": "Put the steps of the agent-environment loop in order.",
         "items": ["The agent receives an observation", "The agent chooses an action", "The environment applies the action", "The environment returns a reward and a new observation", "The agent uses the result to learn"]},
        {"type": "fill", "title": "Fill the loop", "text": "In the loop, the agent picks an {{action}} from a {{policy}}. The environment sends back a {{reward}} and the next {{observation|state}}. The agent wants the highest total {{return}}."}]
})

# ---------------------------------------------------------------- 2
CH.append({
    "title": "Python setup and Gymnasium basics",
    "maps": [{"title": "Gymnasium at a glance", "links": [
        "Gymnasium | provides | Environments",
        "gym.make | creates | Environment",
        "Environment | has | Observation space",
        "Environment | has | Action space",
        "reset | returns | Observation and info",
        "step | returns | Five values",
        "Five values | include | terminated",
        "Five values | include | truncated",
        "Environment | is trained on by | Stable-Baselines3 [ch8]"]}],
    "summary": [
        "Gymnasium is the maintained successor to OpenAI Gym. It gives every environment the same small interface, so any agent can be paired with any environment.",
        "You create an environment with gym.make, start it with reset, and advance it with step. Step returns five values: observation, reward, terminated, truncated and info. Terminated means the task really ended; truncated means a time limit cut it off.",
        "Every environment describes its inputs and outputs with spaces. Discrete spaces hold integers, Box spaces hold arrays of numbers. Knowing the spaces tells you which algorithms and network shapes you can use."],
    "glossary": [
        {"term": "Gymnasium", "def": "The Python library that defines the standard environment interface and ships many example environments."},
        {"term": "gym.make", "def": "Function that builds an environment from its name, for example CartPole-v1."},
        {"term": "reset", "def": "Starts a new episode and returns the first observation and an info dictionary."},
        {"term": "step", "def": "Applies an action and returns observation, reward, terminated, truncated and info."},
        {"term": "terminated", "def": "True when the episode ended because of the task itself, such as falling over or reaching the goal."},
        {"term": "truncated", "def": "True when the episode was stopped by a limit such as a maximum number of steps, not by the task."},
        {"term": "Discrete space", "def": "A space of n integers, 0 up to n minus 1. Used for a fixed set of choices."},
        {"term": "Box space", "def": "A space of arrays of real numbers with lower and upper bounds. Used for continuous values."}],
    "keyPoints": [
        "Install with pip install gymnasium, and use a virtual environment.",
        "reset returns (observation, info). step returns (observation, reward, terminated, truncated, info).",
        "An episode is over when terminated or truncated is True.",
        "Terminated and truncated are different: only truncation means the future was cut off, not that it was bad.",
        "Pass a seed to reset to make runs repeatable.",
        "env.action_space.sample() gives a random valid action, handy for testing."],
    "lesson": [
        T("Start with a clean virtual environment, then install the library. Recent Stable-Baselines3 releases need Python 3.10 or newer, so use a current Python for the whole course."),
        C("""python -m venv rl-env
source rl-env/bin/activate        # Windows: rl-env\\Scripts\\activate
pip install --upgrade pip
pip install gymnasium
python -c "import gymnasium; print(gymnasium.__version__)"
""", "bash"),
        T("Here is the first program. CartPole is a cart with a pole balanced on top. The agent pushes the cart left or right to keep the pole up. Each step the pole stays up gives a reward of 1."),
        C("""import gymnasium as gym

env = gym.make("CartPole-v1")
obs, info = env.reset(seed=42)
print(env.observation_space)   # Box with 4 numbers
print(env.action_space)        # Discrete(2): 0 = push left, 1 = push right

total, done = 0.0, False
while not done:
    action = env.action_space.sample()            # random policy
    obs, reward, terminated, truncated, info = env.step(action)
    total += reward
    done = terminated or truncated
print("episode return:", total)
env.close()""", "python"),
        T("A random policy usually lasts only a few dozen steps. The four observation numbers are cart position, cart velocity, pole angle and pole angular velocity. The episode is terminated if the pole tilts past about twelve degrees or the cart leaves the track. In CartPole-v1 it is truncated at 500 steps, which is the best possible return.",
          "Why two flags? If the pole falls, the future is worth nothing: that is termination. If time simply ran out, the situation was still fine and a learning algorithm should still value the future. Treating a time limit as a real end teaches wrong values, so Gymnasium keeps them separate."),
        C("""# Watching an episode needs a render mode
env = gym.make("CartPole-v1", render_mode="human")      # opens a window
env = gym.make("CartPole-v1", render_mode="rgb_array")  # returns images to save as video

# Other environments to try
gym.make("FrozenLake-v1")     # tiny grid, Discrete observations
gym.make("Taxi-v3")           # 500 discrete states
gym.make("Pendulum-v1")       # continuous action: Box
# LunarLander needs:  pip install "gymnasium[box2d]"
""", "python"),
        T("Spaces matter. Discrete(2) means two actions. Box(low, high, shape) means an array of real numbers, for example a torque between minus two and two. Value-based methods such as DQN need discrete actions. Algorithms such as SAC and TD3 are for continuous Box actions. PPO handles both.")],
    "quiz": [
        {"q": "What does env.step(action) return in Gymnasium?", "options": ["obs, reward, done", "obs, reward, terminated, truncated, info", "reward only", "obs, info"], "answer": 1, "explain": "Gymnasium uses five values. The old Gym used a single done flag."},
        {"q": "CartPole-v1 hits 500 steps. Which flag is set?", "options": ["terminated", "truncated", "both are False", "reset"], "answer": 1, "explain": "A step limit is a truncation. The pole did not fall, so the episode was not terminated by the task."},
        {"q": "What does reset(seed=42) give you?", "options": ["A random action", "A repeatable starting state and the first observation", "A trained model", "The reward"], "answer": 1, "explain": "The seed makes the random start reproducible. reset returns (observation, info)."},
        {"q": "Which space describes a fixed set of choices such as left or right?", "options": ["Box", "Discrete", "Dict of floats", "Sequence"], "answer": 1, "explain": "Discrete(n) holds the integers 0 to n minus 1."}],
    "cards": [
        {"q": "How do you create CartPole?", "a": "env = gym.make(\"CartPole-v1\")"},
        {"q": "What does reset return?", "a": "A tuple: the first observation and an info dictionary."},
        {"q": "Terminated vs truncated?", "a": "Terminated: the task ended. Truncated: a limit such as max steps cut it off."},
        {"q": "How do you get a random valid action?", "a": "env.action_space.sample()"}],
    "practice": [
        {"type": "fill", "title": "Complete the loop", "text": "obs, info = env.{{reset}}(seed=0)\nobs, reward, {{terminated}}, {{truncated}}, info = env.{{step}}(action)\nThe episode is over when terminated {{or}} truncated is True."},
        {"type": "terminal", "title": "Install and first run", "intro": "A scripted shell. Do each task. Outputs are simulated examples.", "prompt": "(rl-env) $", "chips": ["pip install gymnasium", "python -c \"import gymnasium\"", "python cartpole_random.py"],
         "commands": [
             {"re": "^pip install gymnasium$", "out": ["Collecting gymnasium", "Installing collected packages: gymnasium", "Successfully installed gymnasium (simulated)"]},
             {"re": "^python -c \"import gymnasium\"$", "out": ["(no output means the import worked)"]},
             {"re": "^python cartpole_random\\.py$", "out": ["Box(4,)  Discrete(2)", "episode return: 21.0"]},
             {"re": "^python", "out": ["Try: python cartpole_random.py"], "cls": "warn"},
             {"re": "^pip", "out": ["Try: pip install gymnasium"], "cls": "warn"}],
         "tasks": [{"text": "Install gymnasium", "cmd": "^pip install gymnasium$"}, {"text": "Check that it imports", "cmd": "^python -c \"import gymnasium\"$"}, {"text": "Run the random CartPole script", "cmd": "^python cartpole_random\\.py$"}]},
        {"type": "write", "title": "Spot the bug", "prompt": "This loop never ends: while True: obs, r, terminated, truncated, info = env.step(a). Write the line you would add after it to stop correctly.",
         "checks": [{"re": "terminated", "msg": "checks terminated"}, {"re": "truncated", "msg": "checks truncated"}, {"re": "or", "msg": "uses or"}, {"re": "break|done", "msg": "breaks out or sets done"}],
         "solution": "if terminated or truncated: break"}]
})

# ---------------------------------------------------------------- 3
CH.append({
    "title": "Markov decision processes",
    "maps": [{"title": "The MDP", "links": [
        "MDP | consists of | States",
        "MDP | consists of | Actions",
        "MDP | consists of | Transition probabilities",
        "MDP | consists of | Rewards",
        "MDP | uses | Discount factor",
        "Discount factor | turns rewards into | Return",
        "Policy | is evaluated by | Value function",
        "Value function | obeys | Bellman equation",
        "Optimal policy | maximizes | Value function",
        "Value function [ch5] | is learned by | Q-learning [ch5]"]}],
    "summary": [
        "A Markov decision process, or MDP, is the math behind RL. It has states, actions, rules for how states change, rewards and a discount factor. The Markov property says the next state depends only on the current state and action, not on the longer history.",
        "The discount factor gamma, between zero and one, makes later rewards count less. The return is the sum of discounted rewards. A value function V(s) is the expected return from a state under a policy, and Q(s, a) is the expected return after taking action a in state s.",
        "The Bellman equation says a value equals the immediate reward plus the discounted value of what follows. Almost every RL algorithm is a way of solving or approximating this equation."],
    "glossary": [
        {"term": "MDP", "def": "Markov decision process: states, actions, transitions, rewards and a discount factor."},
        {"term": "Markov property", "def": "The future depends only on the current state and action, not on how you got there."},
        {"term": "Transition", "def": "The rule, possibly random, for which state comes next after an action."},
        {"term": "Discount factor (gamma)", "def": "A number from 0 to 1 that shrinks future rewards. Close to 1 means far-sighted."},
        {"term": "Return", "def": "Sum of discounted rewards: r0 + gamma r1 + gamma squared r2 and so on."},
        {"term": "State value V(s)", "def": "Expected return starting in state s and following the policy."},
        {"term": "Action value Q(s, a)", "def": "Expected return from taking action a in state s, then following the policy."},
        {"term": "Bellman equation", "def": "Recursive relation: value equals reward plus discounted value of the next state."}],
    "keyPoints": [
        "An MDP is states, actions, transitions, rewards and gamma.",
        "Return = r0 + gamma*r1 + gamma^2*r2 + ...",
        "Gamma near 0 is short-sighted. Gamma near 1 is far-sighted. 0.99 is a common default.",
        "V(s) scores states. Q(s, a) scores actions in states.",
        "The best policy picks the action with the highest Q in every state.",
        "If the observation hides important information, the problem is only partly observable and a plain MDP is not a perfect fit."],
    "lesson": [
        T("Everything in the first chapter fits in one tidy model. At each time step the agent is in a state s, picks an action a, the world moves to a new state s prime with some probability, and a reward r arrives. Repeat.",
          "The Markov property is a statement about the state, not about the world. If the state includes everything you need to predict what happens next, it is Markov. In CartPole, position and velocity of both cart and pole are enough. A single photo of the pole would not be, because it hides velocity. People then stack several frames."),
        T("Why discount? Two reasons. It keeps infinite sums finite, and it expresses a preference for sooner rewards. With gamma = 0.9, a reward of 10 that arrives three steps later is worth 10 x 0.9 x 0.9 x 0.9 = 7.29 now."),
        C("""def discounted_return(rewards, gamma):
    total = 0.0
    for t, r in enumerate(rewards):
        total += (gamma ** t) * r
    return total

print(discounted_return([1, 1, 1], 0.5))   # 1 + 0.5 + 0.25 = 1.75
print(discounted_return([0, 0, 8], 0.5))   # 8 * 0.25 = 2.0""", "python"),
        T("Value functions answer: how good is it to be here? Q-values answer: how good is it to do this here? If you know Q for every state and action, acting is easy: pick the largest.",
          "The Bellman idea: the return from now equals the reward now plus gamma times the return from the next state. So Q(s, a) = r + gamma x max over a prime of Q(s prime, a prime), when you act optimally afterwards. That one line is behind Q-learning in the next chapters, and DQN is the same idea with a neural network."),
        C("""# Bellman backup for one transition (optimal case)
#   Q(s, a)  <-  r + gamma * max_a' Q(s', a')
q_target = r + gamma * max(Q[s_next])
""", "python"),
        T("Finally, a policy can be deterministic (one action per state) or stochastic (a probability for each action). Stochastic policies help exploration and are used by PPO and A2C. Deterministic ones are often used at test time.")],
    "quiz": [
        {"q": "What does the Markov property say?", "options": ["Rewards are always positive", "The next state depends only on the current state and action", "The agent never explores", "Episodes have a fixed length"], "answer": 1, "explain": "The state must contain what is needed to predict what comes next, so history is not needed."},
        {"q": "With gamma = 0.5, what is the return of rewards [1, 1, 1]?", "options": ["3", "1.75", "1.5", "0.875"], "answer": 1, "explain": "1 + 0.5 + 0.25 = 1.75."},
        {"q": "What does Q(s, a) mean?", "options": ["The probability of reaching s", "Expected return after taking a in s, then following the policy", "The reward at s", "The number of steps in an episode"], "answer": 1, "explain": "Q scores a state and action together. V scores only a state."},
        {"q": "Gamma is set very close to 0. How does the agent behave?", "options": ["Far-sighted", "Short-sighted, caring about immediate reward", "It stops learning", "It acts randomly"], "answer": 1, "explain": "Future rewards are shrunk to almost nothing, so only the next rewards matter."}],
    "cards": [
        {"q": "Write the return formula.", "a": "G = r0 + gamma*r1 + gamma^2*r2 + ..."},
        {"q": "V(s) versus Q(s, a)?", "a": "V scores a state. Q scores an action taken in a state."},
        {"q": "Bellman optimality for Q?", "a": "Q(s,a) = r + gamma * max over a' of Q(s',a')"},
        {"q": "Common default gamma?", "a": "0.99"}],
    "practice": [
        {"type": "code", "title": "Write discountedReturn", "intro": "Write discountedReturn(rewards, gamma): the sum of gamma^t times reward t.", "fn": "discountedReturn",
         "starter": "function discountedReturn(rewards, gamma) {\n  // your code\n}",
         "tests": [{"args": [[1, 1, 1], 0.5], "expect": 1.75, "approx": 0.000001}, {"args": [[5], 0.9], "expect": 5}, {"args": [[0, 0, 8], 0.5], "expect": 2, "approx": 0.000001}, {"args": [[2, 2], 1], "expect": 4}, {"args": [[], 0.9], "expect": 0}],
         "hint": "Loop with an index t and add Math.pow(gamma, t) * rewards[t].",
         "solution": "function discountedReturn(rewards, gamma) {\n  let total = 0;\n  rewards.forEach((r, t) => { total += Math.pow(gamma, t) * r; });\n  return total;\n}"},
        {"type": "match", "title": "Match the symbols", "intro": "Match each symbol or phrase to its meaning.",
         "pairs": [["gamma", "Discount factor"], ["V(s)", "Value of a state"], ["Q(s, a)", "Value of an action in a state"], ["pi", "The policy"], ["s prime", "The next state"]]},
        {"type": "fill", "title": "Bellman in words", "text": "The value of a state equals the immediate {{reward}} plus gamma times the value of the {{next state|next}}. A gamma close to {{1}} makes the agent far-sighted."}]
})

# ---------------------------------------------------------------- 4
CH.append({
    "title": "Exploration, exploitation and bandits",
    "maps": [{"title": "Explore or exploit", "links": [
        "Agent | must balance | Exploration",
        "Agent | must balance | Exploitation",
        "Exploration | tries | Unknown actions",
        "Exploitation | repeats | Best known action",
        "Epsilon-greedy | mixes | Exploration",
        "Epsilon-greedy | mixes | Exploitation",
        "Bandit | is an MDP with | One state",
        "Bandit | estimates | Action values",
        "Epsilon-greedy [ch7] | is used by | DQN [ch7]"]}],
    "summary": [
        "An agent that always repeats the best action it knows may never discover a better one. An agent that always tries new things never cashes in. This is the exploration versus exploitation trade-off.",
        "A multi-armed bandit is the simplest setting: one state, several actions, each paying a random reward. It isolates the trade-off. The agent keeps a running average of rewards per action and picks mostly the best one.",
        "Epsilon-greedy is the classic rule: with probability epsilon pick a random action, otherwise pick the one with the highest estimate. Epsilon is often decayed over time. Deep RL uses the same idea."],
    "glossary": [
        {"term": "Exploration", "def": "Trying actions to learn more about them, even if they look worse right now."},
        {"term": "Exploitation", "def": "Choosing the action that currently looks best to collect reward."},
        {"term": "Bandit", "def": "A problem with one state and several actions, each with an unknown reward distribution."},
        {"term": "Epsilon-greedy", "def": "With probability epsilon act randomly, otherwise act greedily."},
        {"term": "Greedy action", "def": "The action with the highest current value estimate."},
        {"term": "Sample average", "def": "Estimate of an action's value: the mean of the rewards seen so far for that action."},
        {"term": "Regret", "def": "How much reward was lost compared to always picking the best action."}],
    "keyPoints": [
        "Without exploration the agent can lock onto a poor choice forever.",
        "Estimate each action's value with a running average.",
        "Incremental update: new_estimate = old + (reward - old) / count.",
        "Epsilon-greedy is simple and works well. Typical epsilon is 0.1, or decays from 1.0 to a small value.",
        "Random start estimates or optimistic start values also push exploration.",
        "Evaluate a trained agent greedily, with exploration turned off."],
    "lesson": [
        T("Picture five slot machines with different, hidden average payouts. You have 1000 pulls. Pull one machine only and you may never learn another was better. Pull all machines equally forever and you waste pulls on bad ones. The art is in between.",
          "The agent keeps two lists: the estimated value of each arm and how many times it has pulled it. After a pull with reward r, it updates the average without storing history."),
        C("""import random

n_arms = 5
Q = [0.0] * n_arms        # value estimates
N = [0] * n_arms          # pull counts

def choose(epsilon):
    if random.random() < epsilon:
        return random.randrange(n_arms)             # explore
    return max(range(n_arms), key=lambda a: Q[a])   # exploit

def update(arm, reward):
    N[arm] += 1
    Q[arm] += (reward - Q[arm]) / N[arm]            # running average""", "python"),
        T("Choosing epsilon. Too small and learning is slow to find better arms. Too large and you keep wasting pulls. A common schedule starts epsilon high and decays it linearly. Stable-Baselines3's DQN does exactly this with the parameters exploration_fraction and exploration_final_eps.",
          "Bandits matter beyond slot machines: choosing which ad to show, which article to recommend, or which version of a web page to test. Full RL adds the idea that actions also change the future state, which is what the next chapters add."),
        T("Try the Bandit Lab in the practice section. Pull the arms by hand first, then switch on epsilon-greedy and watch the estimates settle.")],
    "quiz": [
        {"q": "What is exploitation?", "options": ["Trying random actions", "Choosing the action that currently looks best", "Resetting the environment", "Increasing gamma"], "answer": 1, "explain": "Exploitation uses current knowledge to collect reward."},
        {"q": "With epsilon-greedy and epsilon = 0.1, how often is the action random?", "options": ["About 90% of the time", "About 10% of the time", "Never", "Only at the start"], "answer": 1, "explain": "With probability epsilon the action is random, otherwise greedy."},
        {"q": "What is a multi-armed bandit?", "options": ["A problem with one state and several actions with unknown rewards", "A neural network type", "A policy gradient method", "An environment wrapper"], "answer": 0, "explain": "It is the simplest RL problem and isolates the exploration question."},
        {"q": "Which update keeps an average without storing all rewards?", "options": ["Q = reward", "Q = Q + (reward - Q) / N", "Q = Q * N", "Q = max(Q, reward)"], "answer": 1, "explain": "This incremental mean moves the estimate a fraction 1/N toward each new reward."}],
    "cards": [
        {"q": "Explore vs exploit in one line?", "a": "Try new things to learn, or repeat the best known thing to earn."},
        {"q": "Epsilon-greedy rule?", "a": "Random action with probability epsilon, otherwise the greedy action."},
        {"q": "Running average update?", "a": "Q += (reward - Q) / N"},
        {"q": "Which SB3 DQN parameters control epsilon?", "a": "exploration_fraction and exploration_final_eps (and exploration_initial_eps)."}],
    "practice": [
        {"type": "code", "title": "Greedy action", "intro": "Write greedyAction(q): the index of the largest value. If values tie, return the lowest index.", "fn": "greedyAction",
         "starter": "function greedyAction(q) {\n  // your code\n}",
         "tests": [{"args": [[0.1, 0.5, 0.2]], "expect": 1}, {"args": [[3, 1, 3]], "expect": 0}, {"args": [[-2, -1]], "expect": 1}, {"args": [[7]], "expect": 0}],
         "hint": "Keep the best index so far and only replace it when a value is strictly larger.",
         "solution": "function greedyAction(q) {\n  let best = 0;\n  for (let i = 1; i < q.length; i++) if (q[i] > q[best]) best = i;\n  return best;\n}"},
        {"type": "code", "title": "Epsilon-greedy", "intro": "Write epsGreedy(q, eps, r1, r2). If r1 < eps return Math.floor(r2 * q.length) (explore). Otherwise return the index of the largest value, lowest index on ties.", "fn": "epsGreedy",
         "starter": "function epsGreedy(q, eps, r1, r2) {\n  // your code\n}",
         "tests": [{"args": [[0.1, 0.5, 0.2], 0.1, 0.05, 0.9], "expect": 2}, {"args": [[0.1, 0.5, 0.2], 0.1, 0.5, 0.9], "expect": 1}, {"args": [[1, 0], 0.5, 0.2, 0.1], "expect": 0}, {"args": [[3, 3, 1], 0, 0, 0.9], "expect": 0}],
         "hint": "r1 and r2 stand in for random numbers so the tests are repeatable.",
         "solution": "function epsGreedy(q, eps, r1, r2) {\n  if (r1 < eps) return Math.floor(r2 * q.length);\n  let best = 0;\n  for (let i = 1; i < q.length; i++) if (q[i] > q[best]) best = i;\n  return best;\n}"},
        {"type": "webxdc", "title": "Bandit Lab", "intro": "An interactive app. Pull arms by hand or switch on epsilon-greedy. Finish by making 40 pulls.", "height": 430, "html": "__BANDIT__"}]
})
