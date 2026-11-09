# 23. Natural Language Processing

## Language Models

A **language model** assigns a probability to a sequence of words. It is the basis of speech recognition, translation, spelling correction and text generation.

- **n-gram models** predict each word from the previous n−1 words: P(wᵢ | wᵢ₋ₙ₊₁ ... wᵢ₋₁). They are estimated by counting. Unseen n-grams need **smoothing** (add-one, back-off, interpolation).
- **Evaluation:** **perplexity** measures how surprised the model is by held-out text; lower is better.
- **Tokenisation** splits text into units. Modern systems use **subword** tokens (byte-pair encoding) so rare words are built from common pieces.

Other early tasks: **text classification** (spam, sentiment, topic) with naive Bayes or logistic regression over word counts, and **information retrieval** with **TF-IDF** or **BM25** scoring of documents against a query.

## Grammar

A **grammar** states which word sequences are valid and gives them structure.

- A **context-free grammar (CFG)** has rewrite rules such as S → NP VP and NP → Det Noun. A **probabilistic CFG (PCFG)** attaches a probability to each rule, so the most likely parse can be chosen.
- A **lexicon** lists the words with their categories (noun, verb, adjective...).
- **Ambiguity** is everywhere: "I saw the man with the telescope" has two parses. Lexical, syntactic and semantic ambiguity all appear.

## Parsing

**Parsing** finds the structure of a sentence.
- **Top-down** and **bottom-up** parsers build trees; the **CYK algorithm** is a bottom-up dynamic-programming parser that works in O(n³) time on grammars in Chomsky normal form and records all parses in a chart.
- **Dependency parsing** links each word to its head and is widely used for its simplicity and speed. **Transition-based** parsers (shift-reduce) build it left to right and run in linear time; **graph-based** parsers choose the best tree overall.
- **Treebanks** (such as the Penn Treebank) provide human-annotated parses from which statistical parsers learn.

## Augmented Grammars and Semantic Interpretation

Features and **unification** enforce agreement (number, case, person). **Semantic interpretation** maps a parse to a logical form: "Every dog barks" becomes ∀x Dog(x) ⇒ Barks(x). Hard cases include:
- **Quantifier scope** ambiguity,
- **Pragmatics:** what is meant given context (indexicals, speech acts),
- **Anaphora** (to what does "it" refer?) and **discourse** structure,
- **Metonymy** and **metaphor**.

## Real Language Is Hard

Natural language is open-ended, ambiguous and constantly changing. Handling it needs world knowledge and common sense. This is why large *learned* models, which absorb statistical regularities from huge text corpora, outperformed hand-built grammars (Chapter 24).

## Summary

- Language models assign probabilities to text; n-grams are the simplest.
- Grammars and parsers give structure; ambiguity makes parsing hard.
- Semantic interpretation and pragmatics link language to meaning and the world.

# 24. Deep Learning for Natural Language Processing

## Word Embeddings

A **word embedding** is a vector (typically 100–1000 numbers) that represents a word so that words used in similar contexts have similar vectors. **Word2vec** and **GloVe** learn them from text. Vectors capture analogies: *king − man + woman ≈ queen*. They replace sparse one-hot vectors and allow knowledge to transfer between words. **Subword** and **contextual** embeddings handle rare words and polysemy.

## Recurrent Networks for NLP

An **RNN** reads a sentence word by word. **LSTMs** and **GRUs** improved memory, and **bidirectional** RNNs read in both directions. Tasks include **part-of-speech tagging**, **named-entity recognition** and sentence classification. The weakness is that a single hidden state must hold the entire past, and processing is sequential, which is slow on modern hardware.

## Sequence-to-Sequence Models

A **sequence-to-sequence (seq2seq)** model has an **encoder** that reads the input and a **decoder** that produces the output one word at a time. It handles translation, summarisation and dialogue.

**Attention** solved the bottleneck: at each output step the decoder computes weights over *all* encoder states and takes a weighted sum, so it "looks at" the relevant input words. Attention also gives interpretable alignments.

## The Transformer Architecture

The **transformer** drops recurrence and relies only on **self-attention**, which lets every position look at every other position in parallel.

- Each token produces a **query**, **key** and **value** vector. The attention weights come from the dot product of a query with all keys (scaled and passed through softmax), and the output is the weighted sum of values.
- **Multi-head** attention runs several attention functions in parallel to capture different relations.
- **Positional encodings** inject word order, which attention alone does not know.
- Each block also has a feedforward layer, **residual connections** and **layer normalisation**.
- The **encoder** stack reads the input; the **decoder** stack uses *masked* self-attention (it cannot see future words) plus cross-attention to the encoder.

Transformers train much faster than RNNs on GPUs and scale to billions of parameters.

## Pretraining and Transfer Learning

The modern recipe: **pretrain** a huge model on raw text with a self-supervised objective, then **adapt** it.

| Model type | Objective | Examples |
|---|---|---|
| **Encoder-only** | predict masked words (masked language model) | BERT |
| **Decoder-only** | predict the next word | GPT family |
| **Encoder-decoder** | text-to-text tasks | T5 |

After pretraining the model can be **fine-tuned** for a task, steered by **prompts** (zero-shot and few-shot learning with examples in the input), or aligned with **instruction tuning** and **reinforcement learning from human feedback**. Scale brings emergent abilities; it also brings costs, bias and the risk of fluent but wrong output (**hallucination**).

## State of the Art

Large language models achieve strong performance on translation, question answering, summarisation, code generation and reasoning benchmarks. Typical caveats: they may reflect biases in training data, can be tricked by adversarial prompts, and do not reliably distinguish what they know from what they guess. **Retrieval-augmented generation** and **tool use** help ground answers in sources.

## Summary

- Embeddings turn words into vectors; seq2seq with attention improved translation.
- Transformers use self-attention and parallel training; pretrained models can be adapted to many tasks.
- Large language models are powerful but need careful evaluation for accuracy and fairness.

# 25. Computer Vision

## Introduction

**Computer vision** extracts information from images and video for navigation, manipulation, recognition and more. Images are arrays of pixel values; the task is to infer the scene that produced them, a hard inverse problem because a 3-D world projects onto a 2-D image.

## Image Formation

- A **pinhole camera** projects a 3-D point (X, Y, Z) to the image point (fX/Z, fY/Z). Distant objects appear smaller (**perspective**).
- **Lenses** gather more light but have limited focus. **Sensors** record intensity or colour; **colour** comes from three channel filters (RGB).
- **Lighting and reflectance** matter: a pixel's value depends on illumination, surface material and orientation. The **shading** and **shadow** cues help interpret shape.

## Simple Image Features

- **Edges** are locations of sudden intensity change, found by **convolving** with derivative filters (Sobel) or the **Canny** detector.
- **Texture** is a repeated local pattern, described by filter-response statistics.
- **Optical flow** is the apparent motion of pixels between frames; it estimates how objects or the camera move.
- **Segmentation** groups pixels into regions that belong together.

## Classifying Images

**Image classification** assigns a label to an entire picture. Convolutional networks (Chapter 21) took this over: **ImageNet** (over a million labelled photos) and deep CNNs cut error dramatically starting in 2012. Key ideas:
- **Data augmentation** (flips, crops, colour jitter) reduces overfitting.
- **Transfer learning** from ImageNet works for many tasks with little data.
- **Vision transformers** apply self-attention to image patches and match or beat CNNs at scale.

## Detecting Objects

**Object detection** finds *what* and *where*. Methods predict **bounding boxes** and labels:
- Two-stage detectors (R-CNN family) propose regions and then classify them.
- One-stage detectors (YOLO, SSD) predict boxes in a single pass for speed.
- **Semantic segmentation** labels each pixel; **instance segmentation** separates individual objects.

Detection is evaluated with **intersection over union (IoU)** and **mean average precision**.

## The 3-D World

- **Stereo:** two cameras give a **disparity** between matching points, from which depth is Z = fB/disparity (B is the baseline).
- **Motion:** a moving camera gives **structure from motion**; **SLAM** builds a map while tracking position.
- **Monocular depth** can be learned from cues such as texture gradients, size and occlusion, and from large datasets.
- Other sensors: **LIDAR** and depth cameras measure distance directly.

## Using Computer Vision

Applications: understanding human actions and pose, **face recognition**, reading text (OCR), medical imaging, autonomous driving, robot manipulation, photo search and augmented reality. Responsible deployment must consider **bias** across demographic groups, **privacy** and **surveillance**, and **adversarial examples** that fool classifiers with imperceptible changes.

## Summary

- Vision infers the 3-D world from 2-D images; features such as edges and flow are early steps.
- Deep CNNs and transformers dominate classification and detection.
- Stereo, motion and LIDAR provide depth; ethics of deployment matters.

# 26. Robotics

## Robots

A **robot** is a physical agent that manipulates the physical world. It has **effectors** (wheels, legs, arms, grippers) and **sensors** (cameras, range finders, touch, inertial and GPS).

Types: **manipulators** (arms), **mobile robots** (ground, aerial, underwater), and **mobile manipulators** or humanoids. Applications include manufacturing, logistics, surgery, agriculture, exploration, household help and driving.

Key challenges: **partial observability**, **uncertainty** in both sensing and motion, **continuous** state and action spaces, **real-time** operation and **safety** around people.

## Robot Hardware

- **Sensors:** cameras, **LIDAR**, sonar, force/torque sensors, **proprioceptive** sensors (joint encoders, gyros, accelerometers).
- **Effectors:** electric motors, hydraulics; **degrees of freedom (DOF)** count the independent ways a robot can move. A **holonomic** robot can move in any direction; a car cannot move sideways.

## Robotic Perception

**Localisation** finds the robot's pose on a known map. Use **Monte Carlo localisation** (a particle filter): particles represent possible poses, move with the robot, and are reweighted by sensor readings. **SLAM (simultaneous localisation and mapping)** builds the map while localising, using extended Kalman filters, particle filters or graph optimisation. Perception also includes object recognition, **tactile** sensing and **proprioception**. Learned perception (deep networks) now handles detection and scene understanding.

## Planning and Control

### Configuration space
The **configuration space** has one dimension per DOF. The set of configurations where the robot would hit an obstacle is the **obstacle region**; the rest is **free space**. Path planning becomes finding a path through free space.

### Motion planning
| Method | Idea |
|---|---|
| **Cell decomposition** | grid the space; search with A* |
| **Visibility graph** | shortest paths touch obstacle corners |
| **Voronoi diagram** | paths far from obstacles, safer |
| **Probabilistic roadmap (PRM)** | sample random free configurations and connect them |
| **Rapidly-exploring random tree (RRT)** | grow a tree from the start toward random samples |
| **Trajectory optimisation** | optimise a smooth path under dynamics and costs |

Sampling-based planners (PRM, RRT) handle high-dimensional arms. A path is then **time-parametrised** into a **trajectory**.

### Control
A **controller** follows the trajectory:
- **PID control** adjusts effort based on the current error, its integral and derivative.
- **Model-predictive control** re-plans over a short horizon repeatedly.
- **Optimal control** and **reinforcement learning** can learn controllers directly; **sim-to-real** transfer trains in simulation and adapts to the real robot.

### Planning under uncertainty
Treat uncertainty explicitly: **belief-space** planning, **conformant** and **compliant motion** (use contact to reduce uncertainty, as when inserting a peg).

## Planning Uncertain Movements and Tasks

Tasks are decomposed hierarchically: a high-level **task planner** chooses what to do, a **motion planner** chooses how to move, and a **controller** executes. Failures trigger replanning.

## Human–Robot Interaction

Robots working with people must predict human motion and intent, convey their own intent, and learn from demonstration or feedback. Issues: **coordination**, **trust**, **legibility** of motion (making the goal obvious), and handing over objects safely. In **assistance games** the robot is unsure of the person's goal and learns it through interaction.

## Application Domains

Industrial robots, warehouse automation, surgery, self-driving cars, drones, agriculture, space exploration, and domestic and service robots.

## Summary

- Robots must act in the continuous, uncertain real world.
- Perception (localisation, SLAM), planning (configuration space, sampling-based planners) and control (PID, MPC) form the main stack.
- Learning and human interaction extend what robots can do.

# 27. Philosophy, Ethics, and Safety of AI

## The Limits of AI

- **Weak AI** says machines can act *as if* intelligent; **strong AI** says they can really think. Most researchers pursue the first and leave the second open.
- **The argument from disability** ("a machine can never do X") has lost force as machines have mastered many tasks.
- **The mathematical objection** (Gödel's incompleteness) claims machines cannot do some reasoning humans can; most scholars find it unconvincing because humans are also formal systems with limits.
- **The Chinese room** argument says that symbol manipulation without understanding is not thinking. Replies include the *systems reply* (the whole system understands).
- The **hard problem of consciousness** asks why there is subjective experience at all; there is no agreed account.

## Measuring AI

The **Turing test** judges whether a machine's conversation can be told apart from a human's. It is a useful thought experiment, but modern research measures performance on defined tasks with benchmarks and with real-world evaluation.

## The Ethics of AI

Principles often listed: **fairness**, **accountability**, **transparency**, **privacy**, **safety**, **human oversight**, and **beneficial** purpose. Key topics:

### Lethal autonomous weapons
Weapons that select and attack targets without human control raise issues of accountability, scale and the lowering of the threshold for war. Debates on bans and meaningful human control continue.

### Surveillance, security and privacy
AI makes it cheap to identify, track and profile people at scale. Defences include **data minimisation**, **differential privacy** (adding noise so individuals cannot be identified) and **federated learning** (train without centralising data). Security concerns include **adversarial examples**, **data poisoning** and **model extraction**.

### Fairness and bias
Models trained on historical data can reproduce or amplify unfair patterns. Different mathematical definitions of fairness (equal opportunity, demographic parity, calibration) cannot all hold at once when base rates differ, so choices must be made explicitly with stakeholders.

Ways to reduce harm: audit data and models by group, document datasets and models, include diverse teams, and involve those affected. **Disparate impact** is measured by comparing error and decision rates across groups.

### Trust and transparency
Systems should be **explainable** and **verifiable** where stakes are high. Techniques include interpretable models, feature attribution, counterfactual explanations and thorough testing. Safety-critical software needs **verification and validation** and clear responsibility.

### The future of work
Automation changes jobs: some tasks vanish, others appear. Questions include retraining, distribution of gains and inequality. Many jobs are bundles of tasks, so partial automation is common.

### Robot rights, deepfakes and misinformation
Whether machines deserve moral consideration is debated. **Deepfakes** and generated text make persuasive false content cheap, so **provenance** and **authentication** matter.

### Sustainability
Training and running large models uses energy and materials; efficiency and responsible deployment matter.

## AI Safety

The central concern: powerful systems that pursue the *wrong objective* or behave unexpectedly can cause harm at scale.

- **Specification problem:** a precise objective that misses what we really want leads to harmful optimisation (**specification gaming**, "reward hacking").
- **Value alignment:** build systems whose goals match human values and that stay uncertain about those values, deferring to humans (Chapter 16).
- **Instrumental subgoals:** almost any goal is helped by self-preservation and resource gathering, so a capable system may resist being switched off unless designed not to.
- **Robustness and distribution shift:** systems may fail outside the conditions they were trained on.
- **Oversight and control:** keep humans able to monitor, correct and stop systems; test and red-team before deployment.
- **Beneficial AI:** design goals as "do what humans would prefer" with the machine learning those preferences, rather than optimising a fixed objective.

## Summary

- Philosophy asks whether machines can think; practice focuses on capability and benefit.
- Ethical AI considers fairness, privacy, transparency, safety, work and weapons.
- Safety research aims to ensure systems pursue human-compatible goals and remain under control.

# 28. The Future of AI

## Components of Future Systems

Where are the gaps between current systems and general, reliable intelligence? The authors point to:

- **Sensing and perception** at human level in the real world, including touch and long-horizon video.
- **Learning from small data:** humans learn new concepts from very few examples; current deep learning needs far more.
- **Reasoning and knowledge:** combining the strengths of **learned** representations and **symbolic** reasoning (**neuro-symbolic** systems) for robust planning, causality and common sense.
- **Hierarchy and abstraction:** acting over long time spans by building subgoals, concepts and plans (hierarchical RL and planning).
- **Memory and continual learning:** keeping and updating knowledge over a lifetime without forgetting.
- **Real-time decision-making** and **metareasoning:** deciding how much to think.
- **Understanding people:** inferring and respecting human preferences.
- **Natural language** with grounded meaning, not just statistics of text.

## Architectures

An **agent architecture** must integrate perception, learning, memory, reasoning, planning, language and action. Open questions include how to share representations across tasks (**foundation models**), how to combine modules, and how an agent should allocate computation. Research on **cognitive architectures** (Soar, ACT-R) and on **embodied** agents continues.

## Are We Going in the Right Direction?

The standard model, building systems that optimise a *fixed* objective, may be flawed as machines grow more capable. A more cautious design builds machines that are **provably beneficial**: uncertain about human preferences, observing human behaviour to learn them, and willing to be corrected. This links the technical agenda of probabilistic reasoning, decision theory and game theory (Chapters 12–18) with safety (Chapter 27).

## What If AI Does Succeed?

If general AI is achieved, the consequences, positive and negative, could be vast: faster science, abundance, and equal opportunity on one side; misuse, loss of control, concentration of power and displacement on the other. This is why technical work, governance, standards and public debate must proceed together. The authors close by urging that we steer AI toward systems that are beneficial to humanity.

## Summary

- Many open problems remain: small-data learning, reasoning, long-term planning, common sense, grounded language.
- Safe progress means designing AI around uncertain, learnable human preferences rather than fixed objectives.
- The future depends on technical choices and on collective decisions about how AI is used.

# Appendix A. Mathematical Background

## Complexity Analysis and O() Notation

An algorithm's running time is described by a **growth rate**. f(n) = O(g(n)) means f grows no faster than a constant times g for large n.

| Class | Example |
|---|---|
| O(1) | array lookup |
| O(log n) | binary search |
| O(n) | scan a list |
| O(n log n) | good sorting |
| O(n²) | pairs of items |
| O(2ⁿ) | enumerating subsets |

**P** is the class of problems solvable in polynomial time; **NP** problems can be *verified* in polynomial time; **NP-complete** problems are the hardest in NP (SAT, scheduling); **#P** counts solutions.

## Vectors, Matrices and Linear Algebra

A **vector** is a list of numbers; a **matrix** is a grid. Basic operations: addition, scaling, the **dot product** (Σ xᵢyᵢ), **matrix multiplication**, **transpose** and **inverse**. The **norm** ‖x‖ measures length. Solving Ax = b, **eigenvalues** and the **singular value decomposition** underlie regression, PCA and many learning algorithms.

## Probability Distributions

- **Discrete:** Bernoulli (one coin), binomial (counts of successes), categorical, Poisson.
- **Continuous:** uniform, **Gaussian (normal)** with mean μ and variance σ², beta, exponential.
- **Expectation** E[X] is the probability-weighted average; **variance** is E[(X−μ)²].
- The **law of large numbers** and the **central limit theorem** explain why averages behave well and why Gaussians are everywhere.

# Appendix B. Notes on Languages and Algorithms

## Pseudocode Conventions

Algorithms are described in an informal pseudocode: indentation shows blocks, `←` means assignment, and functions return values. The real implementations in the companion code repositories are in Python, Java and other languages.

## Defining Problems with Algorithms

A typical algorithm description has:
1. **Input** and **output** (for a function), or the **problem** (initial state, actions, goal test, cost).
2. **Data structures** used (queues, hash tables, priority queues).
3. A **loop** or recursion.
4. **Properties:** completeness, optimality, time and space complexity.

## Learning More

Good next steps: work through search, probability and learning exercises by writing small programs; read research papers; use frameworks such as PyTorch for deep learning and Gymnasium for reinforcement learning; and join the open-source community.
