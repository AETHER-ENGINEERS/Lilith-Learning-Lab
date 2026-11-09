# Lilith Learning Lab

A standalone, offline Android app with a talking, animated Teacher. It comes **empty**: you import courses as JSON files, and it teaches them as animated lectures with concept maps, glossary, key points, quizzes, practice labs, a final exam and progress tracking.

* Every chapter: concept map (with an animated tour), summary, glossary, key points, lesson, then quiz and practice.
* Practice labs: fill, order, match, write, code (JavaScript, runs on the device), **python** (MicroPython 1.29 in WebAssembly, built in, runs on the device, ~0.7 MB), scripted terminal, and **webxdc** apps that can travel inside the course JSON.
* Final exam: a course can define `finalExam`; otherwise it is built from the chapter quizzes.
* Courses are stored on the device, can be deleted, and can be shared as JSON. Progress is kept per course.
* No internet permission. Voice uses the phone's own text-to-speech.

## Courses (`courses/`)

* `jetson-agx-xavier.course.json`: the NVIDIA Jetson AGX Xavier course (23 chapters).
* `rl-python-gymnasium-sb3.course.json`: Reinforcement Learning with Python (12 chapters: RL basics, Gymnasium, MDPs, bandits, Q-learning, custom environments, DQN, Stable-Baselines3, PPO/SAC, training in practice, reward design, next steps). Has a final exam, a bandit lab and a gridworld Q-learning lab.
* `curry-howard-lambek.course.json`: Curry-Howard-Lambek, computational trinitarianism (12 chapters: natural deduction, the lambda calculus, propositions as types, normalization, constructive vs classical logic, categories, products/sums/exponentials, the Lambek correspondence, dependent types, proof assistants, linear logic/monads/HoTT). Uses LaTeX math, has a Lambda Stepper app, a Trinity Explorer app, a simulated Lean terminal and a final exam. Lean examples were checked with Lean 4.35; other code is illustrative.
* `operating-systems.course.json`: Operating Systems, theory and practice (15 chapters based on the Tutorialspoint OS tutorial: overview, types, services, processes, scheduling, threads, memory, virtual memory, I/O, file systems, security, Linux). 60 labs, 30 of them Python labs that run on the built-in MicroPython, a Scheduler Gantt app and a 24-question exam pool. The PDF's scheduling figures were lost, so the scheduling examples use one consistent data set; the PDF's swap-time arithmetic slip (2 s written as 200 ms) is corrected. Built by `build/make_os_course.py`.
* `compiler-design.course.json`: Compiler Design, theory and practice (17 chapters based on the Tutorialspoint Compiler Design tutorial: architecture and phases, lexical analysis, regular expressions, finite automata, syntax analysis, top-down and bottom-up parsing, error recovery, semantic analysis, runtime environments, symbol tables, intermediate code, code generation, optimization). 83 labs, 45 of them Python labs that run on the built-in MicroPython (tokenizer, DFA runner, FIRST/FOLLOW, LL(1) and LR parsers, type checker, three-address code, peephole passes, basic blocks and more), an LL(1) stepper app and a 28-question exam pool. Errors in the source tutorial are corrected in the lessons (the palindrome grammar, the three-address example, the final-state arrow claim). Built by `build/make_compiler_course.py`.
* `godel-machine.course.json`: Gödel Machine (12 chapters on Schmidhuber's self-referential, provably optimal self-improving solver: Gödel's ideas, machine model and utility, axioms, proof searcher, target theorem, global optimality, bias-optimal proof search, examples, related work such as AIXI and OOPS, limits and the Löbian obstacle). 47 labs, 20 of them Python labs on the built-in MicroPython (Gödel numbering, a proof checker, Levin-style search, expectimax, a toy Gödel machine), a Switch Explorer app and a 28-question exam pool. It is a theoretical design with no full implementation; speculative claims are marked as the author's own. Built by `build/make_godel_course.py`.
* `theory-of-computation.course.json`: Theory of Computation (12 chapters based on Tom Carter's 2005 notes: strings and languages, countability, finite automata, regular expressions, Markov models, context free grammars, recognizers and generators, the Chomsky hierarchy, Turing machines, universal machines and halting, big-O and NP, complexity of strings). 61 labs, 36 of them Python labs on the built-in MicroPython (DFA/NFA runners, regex matcher, grammar generator, Turing machine simulator, SAT, entropy), a Turing machine stepper app and a 35-question exam pool. Imprecise statements in the notes are corrected in the lessons. Built by `build/make_theory_course.py`.
* `alphazero.course.json`: AlphaZero (12 chapters on DeepMind's self-play algorithm: game search, Monte Carlo tree search, the policy and value network, PUCT, exploration noise and temperature, self-play data, the loss and training, differences from AlphaGo Zero, results and the debate over the Stockfish matches, a working tic-tac-toe search, and successors such as MuZero). 59 labs, 31 of them Python labs on the built-in MicroPython (minimax and alpha-beta, UCB1, softmax and move masks, PUCT selection and backup, losses, Elo, a tiny AlphaZero search), a PUCT explorer app and a 36-question exam pool. The original program was never released; the capstone is a teaching miniature. Built by `build/make_alphazero_course.py`.
* `aixi.course.json`: AIXI (12 chapters on Marcus Hutter's universal reinforcement learning agent: the agent-environment cycle, expectimax planning, Bayesian mixtures, Kolmogorov complexity and the universal prior, Solomonoff induction, the AIXI equation, horizons and discounting, Pareto optimality and Legg-Hutter universal intelligence, incomputability and AIXItl, the Monte Carlo AIXI approximation with context tree weighting, and the critiques: dualism, bad priors, asymptotic optimality). 72 labs, 35 of them Python labs on the built-in MicroPython (toy universal machine and prior, Bayes updates, expectimax, the AIXI rule on a finite world class, discounting, Pareto fronts, KT and CTW, UCB, a tiny learning agent), an AIXI explorer app and a 38-question exam pool. The toy programs are teaching miniatures, not code from the papers. Built by `build/make_aixi_course.py`.
* `sample-percentages.course.json`: a tiny second-subject sample.

Course format: see the header of `build/src/course.js` or use "Template" and "AI prompt" in the app's library.

## Build

* `build/make_course.py <out.json>`, `build/make_rl_course.py <out.json>` and `build/make_sample.py <out.json>` regenerate the courses.
* `python3 build/build_web.py --web <dir>` writes the web app (`index.html` + `avatar/`).
* `node build/tests/test_course.js`, `python3 build/tests/ui_test.py <web dir> courses [shots]` (Playwright) run the tests.
* `android/build_apk.sh` builds and signs the APK with the plain Android SDK tools (no Gradle). It creates a local keystore on first run; do not commit it.

## Jade

`jade/tools/lilith_tool.js` (search, read, quiz, validate courses) and `jade/skills/lilith-learning-lab/SKILL.md`. `xavier_tool.js` adds a trtexec builder, DLA checker and simulated shell for the Xavier course.

Avatar art is the non-explicit frame set only. The APK is untested on a physical device from the build environment.


## Math (LaTeX)

Lesson text, quiz options, glossary entries and labs accept LaTeX: `$x^2$` inline, `$$...$$` or `\[...\]` displayed, `\(...\)` inline, `\$` for a literal dollar sign. A lesson block `{"type":"math","tex":"..."}` is a displayed formula. KaTeX 0.19.1 (MIT) is bundled and runs offline. The Teacher's voice reads formulas as words and captions show a plain unicode form. In JSON, double every backslash.
