# 19. Learning from Examples

## Forms of Learning

An agent **learns** when its performance on future tasks improves after observing the world. Design choices: *which component* to improve, *what prior knowledge* to use, *how the data is represented*, and *what feedback* is available.

| Type | Feedback | Example |
|---|---|---|
| **Supervised** | input–output pairs | classify emails as spam or not |
| **Unsupervised** | no labels | group customers by behaviour |
| **Semi-supervised** | a few labels plus many unlabelled examples | web page categories |
| **Reinforcement** | rewards and punishments | learning to play a game |

In **supervised learning** the task is to find a hypothesis h that approximates the unknown function f from examples (x, y). If y is a category it is **classification**; if y is a number it is **regression**.

## Supervised Learning Basics

- A **hypothesis space** is the set of functions the learner may choose from.
- **Consistent** hypotheses agree with the training data. With noise, choose the one that **generalises** best to new data.
- **Bias** is the error from the hypothesis space being too simple (**underfitting**). **Variance** is the error from sensitivity to the particular training set (**overfitting**). More flexible models have lower bias and higher variance: the **bias–variance tradeoff**.
- Prefer simple hypotheses (**Ockham's razor**).
- A **model-selection** loop picks hyperparameters on a **validation set**, then reports the final error on a held-out **test set**. **Cross-validation** reuses data when it is scarce. Never tune on the test set.

### Measures
For classification count **error rate**, **precision**, **recall** and their combination (F1). For skewed classes use the **confusion matrix** and **ROC / precision–recall curves** rather than plain accuracy. **Loss functions** make the cost of errors explicit: squared error (L2), absolute error (L1), 0/1 loss.

## Decision Trees

A **decision tree** tests one attribute at each internal node and gives a prediction at each leaf. To grow one:
1. If all examples have the same label, make a leaf.
2. Otherwise choose the attribute with the highest **information gain** (largest reduction in **entropy**).
3. Split and recurse.

Entropy of a distribution is H = −Σ p log₂ p. A fair coin has 1 bit; a certain outcome has 0.

Trees are easy to read and handle mixed data types. They overfit, so they are **pruned** (stop splitting if the gain is not significant) or combined into ensembles.

## Linear Models

- **Linear regression** fits y = w·x + b by minimising squared error. The solution can be found in closed form (**normal equations**) or by **gradient descent**.
- **Logistic regression** passes the linear score through the **sigmoid** σ(z) = 1/(1 + e⁻ᶻ) and gives a probability; it is trained by gradient descent on the log-loss.
- **Regularisation** adds a penalty to the loss: **L2 (ridge)** shrinks weights; **L1 (lasso)** drives many weights to exactly zero, giving sparse models.
- **Gradient descent** repeats w ← w − α ∇L(w); **stochastic** and **mini-batch** versions use a few examples per step and are the workhorse of modern learning.

## Nonparametric Models

These keep the data and use it directly.
- **k-nearest neighbours:** predict by the majority (or average) of the k closest examples. Works well in few dimensions; suffers from the **curse of dimensionality** (in high dimensions everything is far).
- **Locally weighted regression** fits a small linear model around the query.
- **Nearest neighbour search** is sped up with k-d trees or locality-sensitive hashing.

## Support Vector Machines

An **SVM** finds the linear separator with the **maximum margin** (the widest gap between classes). Only the closest examples (**support vectors**) matter. The **kernel trick** lets an SVM learn nonlinear boundaries: replace the dot product with a kernel function k(x, x′) (for example polynomial or Gaussian), which implicitly maps data into a high-dimensional space.

## Ensemble Learning

Combine several models to get a better one.
- **Bagging:** train each model on a bootstrap resample and average/vote. **Random forests** bag decision trees and also randomise the features at each split, reducing variance.
- **Boosting:** train models in sequence, each focusing on examples the previous ones got wrong (**AdaBoost**, **gradient boosting**). Gradient-boosted trees (XGBoost, LightGBM) are the dominant method on tabular data.
- **Stacking** trains a model on the outputs of other models.

## Developing Machine Learning Systems

Practical steps:
1. **Problem formulation** and a clear metric.
2. **Data collection, cleaning and splitting**; watch for **data leakage** and **class imbalance**.
3. **Feature engineering**, normalisation, handling of missing values.
4. **Model selection** and hyperparameter tuning (grid or random search).
5. **Error analysis** and **debugging** (learning curves show if more data or a richer model would help).
6. **Deployment and monitoring** for **dataset shift**, when the live data differs from the training data.

Learning from data also raises concerns about **fairness**, **privacy** and **explainability**, covered in Chapter 27.

## Summary

- Supervised learning fits a function to labelled examples; generalisation is the goal.
- Decision trees, linear models, nearest neighbours, SVMs and ensembles are the classic toolbox.
- Good practice: separate data for training, validation and testing; regularise; analyse errors.

# 20. Learning Probabilistic Models

## Statistical Learning

Learning can be seen as **Bayesian inference**: the **hypotheses** are models, and the **data** are evidence. By Bayes' rule P(h | d) ∝ P(d | h) P(h).

Three practical estimators:
- **Bayesian learning** averages predictions over all hypotheses weighted by their posterior. It is optimal but usually intractable.
- **Maximum a posteriori (MAP)** picks the single most probable hypothesis. It adds a **prior** that penalises complex models.
- **Maximum likelihood (ML)** picks the hypothesis that makes the data most likely; it is MAP with a uniform prior.

For many data, the prior matters less and all three agree.

## Learning with Complete Data

- **Maximum-likelihood parameter learning** for a discrete model: the best estimate is the **observed frequency**. For a coin with 7 heads in 10 flips, the ML estimate is 0.7.
- With few samples this overfits (zero counts give zero probabilities); a **prior** such as the **beta distribution** (equivalent to adding "pseudo-counts", i.e. **Laplace smoothing**) fixes it.
- **Naive Bayes classifier:** learn P(class) and P(feature | class) by counting; classify by choosing the class with the highest posterior. Fast, robust, good for text.
- **Continuous models:** ML estimates for a Gaussian are the sample mean and variance. **Linear regression** is ML estimation with Gaussian noise.
- **Bayesian networks:** with complete data, each CPT is estimated independently from counts. **Structure learning** searches over graphs with a score that balances fit and complexity (BIC).
- **Nonparametric density estimation** (kernel density, nearest neighbour) estimates a distribution without a fixed form.

## Learning with Hidden Variables: the EM Algorithm

Many models have **hidden (latent)** variables, which makes direct estimation hard. The **expectation–maximisation (EM)** algorithm alternates:
- **E-step:** use the current parameters to compute the expected values (soft assignments) of the hidden variables.
- **M-step:** re-estimate the parameters as if those expected values had been observed.

Each iteration never decreases the likelihood, but EM can get stuck in a local maximum, so it is run from several starting points.

### Unsupervised clustering with Gaussian mixtures
A **mixture of Gaussians** says each point comes from one of k Gaussian components. EM learns the component means, covariances and mixing weights. The **k-means** algorithm is a "hard" version: assign each point to the nearest centre, move each centre to the mean of its points, repeat.

### Other uses of EM
- **Hidden Markov models:** the **Baum–Welch** algorithm.
- **Bayesian networks with hidden variables**, **topic models** and **missing data**.

## Summary

- Learning can be viewed as probabilistic inference: Bayes, MAP and ML.
- With complete data, parameters are estimated by counting; with hidden variables, EM is the standard tool.
- Priors and smoothing prevent overfitting from small samples.

# 21. Deep Learning

## Simple Feedforward Networks

A **neural network** is a graph of simple computing units. Each unit computes a weighted sum of its inputs, adds a **bias**, and applies a nonlinear **activation function**.

| Activation | Formula | Note |
|---|---|---|
| Sigmoid | 1/(1+e⁻ᶻ) | outputs 0–1; saturates |
| Tanh | (eᶻ−e⁻ᶻ)/(eᶻ+e⁻ᶻ) | outputs −1 to 1 |
| **ReLU** | max(0, z) | default for hidden layers; cheap, avoids saturation |
| Softmax | e^zᵢ / Σ e^zⱼ | turns scores into a probability distribution |

A **feedforward network** has *layers*: input, one or more **hidden layers**, and output. With enough hidden units a network can approximate any continuous function (**universal approximation**). **Deep** networks use many layers, which lets each layer build more abstract features out of the previous one: pixels → edges → parts → objects.

## Computation Graphs and Back-Propagation

A network is a **computation graph**. Training minimises a **loss** (cross-entropy for classification, squared error for regression). **Back-propagation** computes the gradient of the loss with respect to every weight by applying the chain rule backward from the output, reusing intermediate results. **Automatic differentiation** in modern frameworks (PyTorch, TensorFlow, JAX) does this for any program.

Training loop:
1. Forward pass to compute predictions and the loss on a mini-batch.
2. Backward pass to get gradients.
3. Update the weights with an **optimiser**.

Common optimisers: **SGD with momentum**, **RMSprop**, **Adam** (adaptive per-weight step sizes).

### Practical problems
- **Vanishing and exploding gradients** in deep nets: use ReLU, careful **weight initialisation** and **residual (skip) connections**.
- **Batch normalisation** and **layer normalisation** rescale activations to stabilise training.
- **Overfitting:** use **regularisation**, **dropout** (randomly zero units during training), **data augmentation** and **early stopping**.

## Convolutional Networks

For images, a fully connected layer has too many weights and ignores spatial structure. A **convolutional neural network (CNN)**:
- uses small **filters (kernels)** shared across positions, exploiting **local** patterns and **translation equivariance**;
- applies **pooling** layers to reduce size and gain small-shift invariance;
- stacks many **convolution + nonlinearity** blocks, then a classifier.

CNNs such as **AlexNet**, **VGG** and **ResNet** transformed image recognition. **Residual networks** let hundreds of layers train because each block learns a correction to its input.

## Recurrent Networks

A **recurrent neural network (RNN)** processes sequences by passing a **hidden state** from one step to the next. Plain RNNs struggle with long-range dependencies because gradients vanish. **LSTM** and **GRU** cells use **gates** that control what to keep, forget and output, giving much longer memory.

## Unsupervised and Transfer Learning

- **Autoencoders** learn to compress and reconstruct data; the compressed code is a useful representation. **Variational autoencoders (VAEs)** make this a generative model.
- **Generative adversarial networks (GANs)** train a **generator** to fool a **discriminator** that tries to tell real from fake.
- **Self-supervised learning** invents labels from the data itself (predict the next word, fill a masked patch), allowing training on huge unlabelled datasets.
- **Transfer learning:** pre-train a large model once, then **fine-tune** it on a small task. This is the dominant recipe in vision and language.

## Applications

Deep learning gives state-of-the-art results in image classification and detection, speech recognition, machine translation, game playing, protein structure prediction and more. Its limits include data hunger, brittleness to small adversarial changes, lack of explanation, and energy cost.

## Summary

- Neural networks stack units with nonlinear activations; back-propagation computes gradients; optimisers update weights.
- CNNs exploit spatial structure; RNNs and gated cells handle sequences.
- Pre-training and fine-tuning make deep learning practical with small datasets.

# 22. Reinforcement Learning

## Learning from Rewards

In **reinforcement learning (RL)** an agent is not told the right action. It receives only a **reward** signal after acting and must discover which behaviour is good. The environment is an MDP whose transition and reward functions the agent does *not* know. The agent's aim is a policy that maximises expected discounted return.

Two big problems:
- **Credit assignment:** which of many earlier actions led to this reward?
- **Exploration vs. exploitation:** try new actions to learn, or use the best known one to earn?

**Passive** RL evaluates a *fixed* policy; **active** RL also chooses actions. **Model-based** agents learn the model and plan with it; **model-free** agents learn values or policies directly.

## Passive Reinforcement Learning

Goal: estimate the utility Uπ(s) of states under policy π.

| Method | Idea |
|---|---|
| **Direct utility estimation** | average the observed returns from each state; ignores the structure of Bellman equations, so it learns slowly |
| **Adaptive dynamic programming (ADP)** | learn the transition model from counts, then solve the Bellman equations |
| **Temporal-difference (TD) learning** | after each step, nudge U(s) toward the one-step target: U(s) ← U(s) + α [r + γU(s′) − U(s)] |

TD learning needs no model, updates after every step and is the basis of most modern RL.

## Active Reinforcement Learning

### Exploration
- **ε-greedy:** with small probability ε take a random action.
- **Optimism in the face of uncertainty:** treat unvisited actions as if they were great, so the agent tries them (UCB, optimistic initial values).
- **Multi-armed bandits** are the single-state version; **Thompson sampling** and UCB manage the tradeoff with regret guarantees.

### Q-learning
**Q-learning** learns the action-value function Q(s, a), the expected return of taking a in s and following the best policy after:

Q(s, a) ← Q(s, a) + α [ r + γ maxₐ′ Q(s′, a′) − Q(s, a) ]

It is **off-policy**: it learns the optimal policy while following an exploratory one. **SARSA** is **on-policy**: it uses the action actually taken next.

## Generalisation in Reinforcement Learning

Tables fail when there are many states. **Function approximation** represents Q or U as a parameterised function (a linear model or a neural net) and updates the parameters by gradient steps.

- **Deep Q-networks (DQN)** use a CNN to approximate Q from raw pixels. Stability comes from **experience replay** (train on random old transitions) and a slowly updated **target network**. DQN reached human level on many Atari games.
- Function approximation with bootstrapping and off-policy updates can diverge (the "deadly triad"), so care is needed.
- **Reward shaping** adds hints, but badly designed rewards produce unintended behaviour. **Potential-based shaping** keeps the optimal policy unchanged. **Hierarchical RL** learns temporally extended actions ("options") and subgoals.

## Policy Search

Instead of learning values, **policy search** adjusts the parameters θ of a policy πθ directly to increase the expected return.

- The **policy gradient theorem** gives ∇J(θ) = E[∇ log πθ(a | s) × (return)]. The **REINFORCE** algorithm estimates it from sampled episodes; variance is reduced with a **baseline**.
- **Actor–critic** methods learn both a policy (the *actor*) and a value function (the *critic*) that reduces variance.
- Modern stable variants: **trust-region** and **proximal policy optimisation (PPO)**, which limit how much the policy can change in one update.

Policy search copes with continuous actions and is popular in robotics.

## Apprenticeship and Inverse Reinforcement Learning

When designing a reward is hard, learn from a demonstrator.
- **Imitation (behavioural cloning)** copies the expert's actions; errors compound when the agent drifts to unfamiliar states.
- **Inverse reinforcement learning (IRL)** infers the reward function that makes the demonstrator's behaviour look optimal, then optimises it.
- **Learning from human feedback** trains a reward model from human preferences between outputs and then optimises it (RLHF), a key step in aligning language models.

## Applications

Game playing (backgammon, Atari, Go, StarCraft), robot control, recommendation, data-centre cooling, resource management and chip design.

## Summary

- RL learns from rewards without a model of the world; the key challenges are credit assignment and exploration.
- TD learning and Q-learning estimate values; deep networks let them scale.
- Policy-gradient methods optimise behaviour directly; inverse RL and human feedback help specify goals.
