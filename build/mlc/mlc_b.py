# -*- coding: utf-8 -*-
"""Meta-learning for compositionality, part 2: chapters 6-10. Based on Lake and Baroni (2023), Nature 623, 115-121 (CC BY 4.0)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "Meta-learning: learning how to learn",
 ("Meta-learning", []),
 ["Meta-learning means practising the skill of learning itself. Instead of learning one task, a network sees a long stream of small tasks, each with its own examples.",
  "Because the meanings of the words change in every task, the network cannot memorise them. The only thing that helps across tasks is the skill of reading the examples and working out the rule.",
  "That skill is what we want: look at a few examples, work out the pattern, apply it to a new question."],
 [("Meta-learning", "Learning how to learn by practising many small tasks."),
  ("Episode", "One small task: some study examples plus a query."),
  ("Few-shot task", "A task with only a few examples."),
  ("Stream", "A long series of different episodes."),
  ("Task-specific weights", "Extra numbers adjusted for only one task."),
  ("Frozen weights", "Numbers that stop changing at test time.")],
 ["An episode is a tiny task with its own examples.",
  "Meta-learning practises a stream of episodes.",
  "Word meanings change each episode.",
  "So the network cannot memorise; it must infer.",
  "At test time the weights are frozen."],
 [T("When you were small, you did not learn each new game from scratch. You got good at learning games: watch a few turns, spot the rule, play. That skill, learning to learn, is what meta-learning tries to train."),
  T("To train it, you do not show one big task. You show many small ones. Each small task is called an episode. An episode has a few study examples and one query, a question to answer using those examples."),
  T("The figure compares the two ways of training. On the left is the usual way: one fixed world, the same answers again and again. On the right is a stream of episodes in which dax means red in one, green in another, blue in a third."),
  T("In the stream, the meaning of every word is shuffled. So the network can never rely on remembering what dax means. The only thing that works in every episode is reading the study examples and working out the meanings fresh."),
  T("After lots of practice the network has not learned the meaning of any word. It has learned something deeper: a procedure for finding meanings from examples and combining them. That procedure is the thing that generalises to a new language, just like people."),
  T("Here is the crucial point about how this is used afterwards. At test time the network's weights are frozen. No learning happens in the usual sense. The new task is handled by feeding the study examples in as part of the input. The network does the rest in a single forward pass."),
  C("# rename the words: the same sentence means something new\nmeanings = ['R', 'G', 'B', 'Y']\nfor shift in range(3):\n    m = meanings[shift:] + meanings[:shift]\n    print('episode', shift + 1, ': dax =', m[0])", "python"),
  T("The code makes a different world for each episode by rotating the meanings. The real training shuffles meanings much more widely, but the idea is the same: the network never sees the same meaning set twice in a row.")],
 [("What is an episode?", ["A small task with study examples and a query", "A TV show", "A single weight", "A kind of data file"], 0, "A mini task."),
  ("Why shuffle word meanings in every episode?", ["So the network must infer them from examples", "To save memory", "To confuse people", "It is random noise"], 0, "No memorising."),
  ("What does meta-learning practise?", ["Learning itself", "One fixed task", "Typing", "Drawing"], 0, "Learning how to learn."),
  ("What happens to the weights at test time?", ["They are frozen", "They are rewritten", "They are deleted", "They double"], 0, "No task-specific updates."),
  ("How is a new task given to the network?", ["As study examples in the input", "By retraining it", "By editing code", "By a voice command"], 0, "Examples are the input."),
  ("What does the network learn in the end?", ["A procedure for inferring and combining meanings", "The meaning of dax", "A dictionary", "Nothing"], 0, "A skill, not facts.")],
 [("Episode", "Study examples plus one query"), ("Stream", "Many different episodes"), ("Frozen weights", "No updates at test time"), ("Learn to learn", "Meta-learning")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("episode", "a small task with examples and a query"), ("meta-learning", "practising how to learn"), ("frozen weights", "no changes at test time"), ("stream", "a long series of episodes")]),
  FILL("Learning to learn", "A small task with a few examples and a query is an {{episode}}. Training on a long {{stream}} of them is called {{meta-learning}}. After training the {{weights}} are frozen."),
  PL("Rename the words", "Write rename(sentence, mapping): mapping is a list of [old, new] pairs. Split the sentence on spaces, swap every word that appears as an old word with its new word, and join with spaces again.", "rename(sentence, mapping)", '''
def rename(sentence, mapping):
    out = []
    for w in sentence.split(' '):
        for pair in mapping:
            if pair[0] == w:
                w = pair[1]
                break
        out.append(w)
    return ' '.join(out)
''', [["dax fep", [["dax", "wif"]]], ["dax wif", [["dax", "wif"], ["wif", "dax"]]], ["lug", []], ["a b c", [["b", "z"]]]], "Look each word up in the pairs."),
  PL("Rotate the meanings", "Write rotate(meanings, k): return the list meanings moved left by k places, with the front part going to the back. Use meanings[k:] + meanings[:k].", "rotate(meanings, k)", '''
def rotate(meanings, k):
    return meanings[k:] + meanings[:k]
''', [[["R", "G", "B", "Y"], 1], [["R", "G", "B", "Y"], 2], [["R", "G"], 0], [["a", "b", "c"], 3]], "Two slices glued together."),
  ORDER("Order the training", "Put the steps of meta-training in order.", ["Make a new world of word meanings", "Show a few study examples from it", "Ask a query about the same world", "Adjust the network and start a new episode"])]))

CHS.append(CH(
 "The MLC recipe",
 ("MLC recipe", []),
 ["MLC stands for meta-learning for compositionality. It is a recipe for training a standard transformer on a stream of episodes made from randomly generated grammars.",
  "Each episode has study examples and a query. The target answer is the exact rule answer 80 percent of the time and a human-like guess 20 percent of the time, so the network learns both rules and habits.",
  "Because the guessing habits are written into the targets, the network learns them from data. The network itself has no built-in rules."],
 [("MLC", "Meta-learning for compositionality."),
  ("Interpretation grammar", "The rules that make an episode's answers."),
  ("Target answer", "The answer the network is trained to produce."),
  ("Algebraic answer", "The exact answer the grammar's rules give."),
  ("Heuristic answer", "A human-like guess that follows the habits."),
  ("Joint training", "Training on more than one kind of task together.")],
 ["Episodes come from random grammars.",
  "Study examples plus a query go in as one input.",
  "80 percent of targets are exact algebraic answers.",
  "20 percent follow human-like habits.",
  "No rule machinery is added to the network."],
 [T("Now we can put the pieces together. To build one episode, the recipe first draws a brand-new grammar at random: a new set of word meanings and function rules. It then writes study examples and a query using that grammar."),
  T("All of it goes into the network as one string, with the study examples and then the query. The network must output the answer for the query. The figure shows an episode. You can see the study examples, the query and the target."),
  T("How is the target chosen? Here is the clever bit. In 80 percent of episodes, the target is the strict algebraic answer: exactly what the rules say. In the other 20 percent, it is a human-like answer that follows the habits from the last chapter."),
  T("The 80 and 20 are tuned so that the network's overall accuracy is similar to people's. Because the habits only show up in the targets, nothing special is added to the network. It simply learns from data that sometimes answers follow rules and sometimes follow human guessing habits."),
  T("The paper trains several versions. In MLC the targets are exact algebraic answers and bias-based answers. In algebraic-only MLC the targets are strictly the rules. In joint MLC the network is trained on both the few-shot task and the open-ended task, with extra bridging episodes. The copy-only version practises just copying study examples."),
  C("# build the one-string input the network reads\nstudy = [['dax', 'R'], ['lug fep', 'BBB']]\nquery = 'dax fep'\nparts = []\nfor pair in study:\n    parts.append(pair[0] + ' = ' + pair[1])\nprint(' | '.join(parts) + ' | ' + query)", "python"),
  T("Training details are modest: the Adam optimizer, 25 episodes per batch and 50 passes over the data, on a single graphics card. Dropout of 0.1 keeps the network from overfitting. The model is not large, so this is not about raw computing power."),
  T("In short, the recipe is: random grammars, many episodes, mixed targets, one plain transformer. That is the whole of MLC. The interesting finding is how far this simple recipe goes.")],
 [("How is an MLC episode drawn?", ["From a randomly generated grammar", "From a fixed dictionary", "From the internet", "By hand each time"], 0, "A new world every time."),
  ("What does the network read as input?", ["Study examples and the query together", "Only the query", "Only the study examples", "A picture"], 0, "One long input."),
  ("How often is the target the exact algebraic answer?", ["80 percent", "100 percent", "20 percent", "0 percent"], 0, "The remaining 20 percent follow habits."),
  ("What are the 20 percent targets like?", ["Human-like guesses", "Random noise", "Blank", "Copies of the query"], 0, "They carry the habits."),
  ("Is any rule machinery added to the network?", ["No", "Yes, a grammar engine", "Yes, a database", "Yes, a calculator"], 0, "A plain transformer."),
  ("What does the copy-only variant practise?", ["Copying study examples", "Translating French", "Solving puzzles", "Searching the web"], 0, "A control variant.")],
 [("80% / 20%", "Algebraic and human-like targets"), ("Random grammar", "New world every episode"), ("One input", "Study plus query"), ("Plain transformer", "Nothing added")],
 [MATCH("Match the variant", "Pair each MLC variant with its training.", [("MLC (algebraic only)", "strictly exact rule answers"), ("MLC", "rules plus human-like guesses"), ("MLC (joint)", "both tasks, with bridge episodes"), ("MLC (copy only)", "only copies study examples")]),
  FILL("The recipe", "Each episode comes from a randomly generated {{grammar}}. The target is the exact algebraic answer {{80}} percent of the time and a human-like answer {{20}} percent of the time. The network reads the study examples and the query as one {{input}}."),
  PL("Pack the input", "Write pack(study, query): study is a list of [instruction, answer] pairs. Join each pair as 'instruction = answer', put ' | ' between them, then add ' | ' and the query at the end.", "pack(study, query)", '''
def pack(study, query):
    parts = []
    for pair in study:
        parts.append(pair[0] + ' = ' + pair[1])
    return ' | '.join(parts) + ' | ' + query
''', [[[["dax", "R"], ["lug fep", "BBB"]], "dax fep"], [[["a", "X"]], "b"], [[], "q"]], "Join with ' | '. Remember the query at the end."),
  PL("Pick the target", "Write target(algebraic, heuristic, r): r is a number from 0 to 1. If r is less than 0.8 return algebraic, otherwise return heuristic. This mimics the 80/20 split.", "target(algebraic, heuristic, r)", '''
def target(algebraic, heuristic, r):
    if r < 0.8:
        return algebraic
    return heuristic
''', [["RRR", "RG", 0.1], ["RRR", "RG", 0.79], ["RRR", "RG", 0.8], ["a", "b", 0.95]], "Under 0.8 it is the exact answer."),
  ORDER("Order one episode", "Put the steps of building one training episode in order.", ["Draw a random grammar", "Write study examples from it", "Write a query and its target", "Pack everything as one input"])]))

CHS.append(CH(
 "Results: does MLC act like people?",
 ("Results", []),
 ["MLC can be compared with people on the very same tasks. On the few-shot task its best run reached perfect exact-match accuracy, and its sampled answers matched human behaviour closely.",
  "Sampled answers followed the rule 82.4 percent of the time, against 80.7 for people, and handled longer outputs 77.8 percent of the time against 72.5. Its types of mistakes also looked human.",
  "A basic network scored zero, and a purely symbolic model with built-in biases needed much more hand-built structure to come close."],
 [("Exact-match accuracy", "Share of answers that are perfectly right."),
  ("Log-likelihood", "How probable a model thinks the human data is; higher is better."),
  ("Sampling", "Letting the model pick answers by chance, as people do."),
  ("Greedy decoding", "Always picking the most likely symbol."),
  ("Symbolic model", "A model with hand-written rules."),
  ("Baseline", "A simple model used for comparison.")],
 ["Best MLC run: perfect exact match on rule answers.",
  "Sampled MLC: 82.4 percent systematic, people 80.7.",
  "Longer outputs: MLC 77.8, people 72.5.",
  "MLC predicted which items were hard for people.",
  "Basic seq2seq scored 0 percent."],
 [T("Let us look at the scoreboard. First, a perfectly obedient network. Take the most systematic MLC run and let it always choose its most likely symbol. It reached 100 percent exact-match accuracy on the best responses. The rules were learned fully."),
  T("But people are not perfectly obedient. So the researchers let the network guess by chance, using its learned probabilities, as people do. In this mode MLC was systematic 82.4 percent of the time, close to people's 80.7. On longer outputs MLC got 77.8 percent against people's 72.5."),
  T("The figure compares them side by side. The blue bars are people, the purple bars are MLC. The two are close, and both are far above the red bar: a basic sequence-to-sequence network scored zero."),
  T("There is a deeper test of human-likeness than overall scores. When MLC made mistakes, they looked like human mistakes, such as one-to-one answers and iconic concatenation. MLC also predicted which test items would be hard for people: the match between the model's item difficulty and human difficulty was a strong correlation of 0.788."),
  T("The paper scores models by log-likelihood: how likely the model thinks the actual human answers were. Higher is better. The joint MLC model scored about minus 349 on the few-shot task, a symbolic model with the same biases scored about minus 357, and a basic network scored minus 1,265, a huge gap."),
  T("On the open-ended task, where there are no examples, MLC answered like the most common person in 65 percent of its samples and also captured partial use of the habits. Its joint version beat the symbolic model with built-in biases by a wide margin there too."),
  C("# log-likelihood of three answers the model thought likely\nimport math\nprobs = [0.5, 0.25, 0.8]\nprint('log-likelihood:', round(sum(math.log(p) for p in probs), 2))", "python"),
  T("The log-likelihood sum is easy to read: each answer's probability goes through a logarithm, so common answers contribute small negative numbers, and surprising answers contribute big negative numbers. A model that finds human answers more likely has a total closer to zero.")],
 [("What did the best MLC run score on exact rule answers?", ["100 percent", "50 percent", "0 percent", "10 percent"], 0, "Always picking the likeliest symbol."),
  ("How systematic was sampled MLC?", ["82.4 percent", "20 percent", "100 percent", "0 percent"], 0, "People got 80.7."),
  ("On longer outputs, who did better?", ["MLC 77.8 vs people 72.5", "People by far", "Neither", "A basic network"], 0, "Close, with MLC slightly ahead."),
  ("What does a higher log-likelihood mean?", ["The model finds human answers more likely", "A worse model", "More noise", "A slower model"], 0, "Closer to zero is better."),
  ("Which model had the log-likelihood of minus 1,265?", ["Basic seq2seq", "MLC (joint)", "Symbolic oracle", "People"], 0, "A huge gap."),
  ("What did MLC predict about people?", ["Which items were hard for them", "Their names", "Their age", "Nothing"], 0, "Correlation 0.788.")],
 [("100%", "Best MLC, greedy"), ("82.4 vs 80.7", "MLC vs people, rule following"), ("77.8 vs 72.5", "MLC vs people, longer outputs"), ("-349 vs -1265", "MLC joint vs basic, log-likelihood")],
 [MATCH("Match the score", "Pair each score with what it describes.", [("100%", "best MLC exact match, greedy"), ("82.4%", "sampled MLC, rule following"), ("80.7%", "people, rule following"), ("0%", "basic seq2seq, few-shot")]),
  FILL("Scoreboard", "Sampled MLC followed the rule {{82.4}} percent of the time, close to people's {{80.7}}. A basic network scored {{0}} percent. Models are compared by log-{{likelihood}}, where higher is better."),
  PL("Log-likelihood", "Write loglik(probs): probs is a list of probabilities between 0 and 1 that a model gave to the human answers. Return the sum of their natural logs, rounded to 2 decimals. Use import math.", "loglik(probs)", '''
import math
def loglik(probs):
    total = 0.0
    for p in probs:
        total = total + math.log(p)
    return round(total, 2)
''', [[[0.5, 0.25, 0.8]], [[1.0]], [[0.1, 0.1]], [[0.9, 0.7, 0.6, 0.5]]], "Add up the logs."),
  PL("Best model", "Write best(names, scores): both lists have the same length and a higher score is better. Return the name with the highest score.", "best(names, scores)", '''
def best(names, scores):
    top = 0
    for i in range(len(scores)):
        if scores[i] > scores[top]:
            top = i
    return names[top]
''', [[["MLC", "Symbolic", "Basic"], [-349.2, -357.2, -1264.7]], [["a", "b"], [-1, -2]], [["x"], [0]]], "Remember the index of the highest score."),
  ORDER("Order the evidence", "Put the steps of judging whether MLC acts like people in order.", ["Give the network and people the same tasks", "Compare accuracy on the exact rule", "Compare the kinds of mistakes", "Score how likely the human answers are"])]))

CHS.append(CH(
 "Benchmarks: SCAN and COGS",
 ("Benchmarks", []),
 ["Besides the human tasks, the paper tests MLC on two machine-learning benchmarks: SCAN, which turns commands into actions, and COGS, which turns sentences into logical forms.",
  "On the lexical generalization tests MLC slashed error rates. For example on SCAN add jump the error fell from 99.27 percent for a basic network to 0.22 percent.",
  "But MLC still fails some tests, such as the SCAN length split and three COGS structural splits, where the error stays at 100 percent."],
 [("SCAN", "A benchmark of commands like jump twice turned into actions."),
  ("COGS", "A benchmark of sentences turned into logical forms."),
  ("Lexical generalization", "Using a known word in a new situation."),
  ("Productivity", "Handling longer or deeper sentences than seen before."),
  ("Exact-match error rate", "Share of answers that are not perfectly right."),
  ("Split", "A way of dividing data into training and test sets.")],
 ["SCAN turns commands into actions.",
  "COGS turns sentences into logical forms.",
  "MLC cut lexical errors sharply.",
  "Add jump: 99.27 percent down to 0.22 percent.",
  "Length and some structure splits still fail."],
 [T("The benchmark SCAN is a classic test. A command like jump twice must become the actions JUMP JUMP. The words walk, run, look and jump are primitives, and words like twice and thrice are modifiers. It is the same compositional puzzle as our colour language."),
  T("In the add jump test, the network sees the word jump only on its own in training, never together with twice or thrice. It is tested on jump twice. A system with true compositional skill would succeed. A normal network fails: the paper reports a 99.27 percent error rate for the basic model."),
  T("MLC applies the same idea you saw before: practise on episodes in which the word meanings are shuffled. The input holds study examples and a query, and the network must work out the meaning of the shuffled words and combine them. This time it was applied with standard transformer parts and modular reading of study examples."),
  T("The results are striking. On SCAN add jump the error fell from 99.27 to 0.22 percent. On around right it fell from 51.13 to 0.04 percent. On opposite right it fell from 100 to 0.06 percent. On COGS lexical generalization it fell from 6.08 to 0.87 percent. The figure shows the gaps."),
  T("COGS is the second benchmark. It asks a network to turn English sentences into logical forms, meaning structured statements. The lexical generalization split tests whether a known word can be used in a new role."),
  C("# error rate: wrong answers divided by all answers, as a percent\nwrong, total = 22, 10000\nprint(round(100 * wrong / total, 2), 'percent error')", "python"),
  T("MLC does not solve everything. It fails on the SCAN length split, where the commands in the test are much longer than any in training, and on three COGS structural splits where it must handle new sentence shapes. On these the error rate stays at 100 percent."),
  T("This is an important lesson about reading results honestly. A method can be superb at one kind of generalization, new uses of known words, and still be stuck on others, such as new lengths and new structures. Always ask which test a number came from.")],
 [("What does SCAN translate?", ["Commands into actions", "Pictures into text", "English into French", "Numbers into words"], 0, "jump twice becomes JUMP JUMP."),
  ("What does COGS translate?", ["Sentences into logical forms", "Commands into actions", "Music into notes", "Code into binary"], 0, "Structured meanings."),
  ("What was the basic network's error on SCAN add jump?", ["99.27 percent", "0.22 percent", "50 percent", "1 percent"], 0, "It almost always failed."),
  ("What was MLC's error on SCAN add jump?", ["0.22 percent", "99.27 percent", "100 percent", "6 percent"], 0, "A huge improvement."),
  ("Which tests does MLC still fail?", ["SCAN length and some COGS structure splits", "All of them", "None", "Only lexical ones"], 0, "100 percent error remains."),
  ("What is lexical generalization?", ["Using a known word in a new situation", "Longer sentences", "New grammar", "Spelling"], 0, "The kind MLC is good at.")],
 [("SCAN", "Commands to actions"), ("COGS", "Sentences to logical forms"), ("99.27% to 0.22%", "Add jump"), ("100% still", "Length and structure splits")],
 [MATCH("Match the test", "Pair each item with its description.", [("SCAN", "commands to actions"), ("COGS", "sentences to logical forms"), ("add jump", "jump seen only alone in training"), ("length split", "test commands longer than training")]),
  FILL("Benchmarks", "On SCAN add jump MLC cut the error from {{99.27}} percent to {{0.22}} percent. SCAN turns {{commands}} into actions. COGS turns sentences into {{logical}} forms. MLC still fails the SCAN {{length}} split."),
  PL("Tiny SCAN", "Write scan(command): the words walk, jump, look and run give WALK, JUMP, LOOK and RUN. The word twice repeats the action before it two times, and thrice three times. A command may join two pieces with 'and', which puts the second piece after the first. Return the actions as a list of strings.", "scan(command)", '''
def scan(command):
    names = {'walk': 'WALK', 'jump': 'JUMP', 'look': 'LOOK', 'run': 'RUN'}
    out = []
    for piece in command.split(' and '):
        words = piece.split(' ')
        act = [names[words[0]]]
        if len(words) > 1:
            if words[1] == 'twice':
                act = act * 2
            elif words[1] == 'thrice':
                act = act * 3
        out = out + act
    return out
''', [["jump"], ["jump twice"], ["walk thrice"], ["look and run twice"], ["run twice and jump thrice"]], "Handle each piece, then join them."),
  PL("Error rate", "Write error_rate(wrong, total): the percent of answers that are wrong, rounded to 2 decimals.", "error_rate(wrong, total)", '''
def error_rate(wrong, total):
    return round(100.0 * wrong / total, 2)
''', [[22, 10000], [1, 3], [0, 50], [9927, 10000]], "Wrong over total times 100."),
  ORDER("Order the benchmark", "Put the steps of the SCAN add jump test in order.", ["Train on commands where jump appears only alone", "Train on twice and thrice with other verbs", "Test on jump twice", "Count exact-match errors"])]))

CHS.append(CH(
 "Limits, lessons and where to go next",
 ("Limits and lessons", []),
 ["MLC shows that a plain neural network can acquire human-like systematic generalization from a smart training stream. It is a big step but not a finished story.",
  "The authors list honest limits: entirely new structures, new symbols that were never seen, and full natural language are all outside what has been shown.",
  "Future work may add this kind of specialised training to large language models and vision models, and may draw lessons from how children learn."],
 [("Limitation", "Something a method cannot yet do."),
  ("Meta-training distribution", "The kinds of episodes used in training."),
  ("Pointer mechanism", "A way for a network to copy symbols it has never seen."),
  ("Hierarchical Bayesian model", "A statistical way to learn biases from many tasks."),
  ("Open access", "Free to read for everyone."),
  ("Replication", "Checking that a result holds again.")],
 ["MLC works inside its meta-training distribution.",
  "It cannot yet handle entirely new structures.",
  "It cannot emit brand new symbols without extra machinery.",
  "It is not yet shown on full natural language.",
  "Children's word learning may offer further clues."],
 [T("Good science always lists what it did not do. The authors are clear about the limits of MLC. First, it handles episodes like those it practised on. If you hand it an entirely new structure that was not in its training stream, it has no way to cope."),
  T("Second, it cannot invent new symbols. A pointer mechanism would be needed to let it copy a word it has never seen. Third, it has been tested on made-up tasks and benchmarks, not on full natural language or images."),
  T("The figure sums it up. On the left are the strengths: new combinations of known words, human-like habits learned from data, a plain transformer and strong results on lexical benchmarks. On the right are the things still to do."),
  T("How does MLC relate to other ideas? The authors say it resembles hierarchical Bayesian modelling, a statistical method that learns biases from many tasks, but uses neural networks for more expressive power. It also sits between symbolic models, which are rule-based, and standard neural nets, which are pattern-based."),
  T("Where might it go next? The authors suggest adding specialised meta-training to large language models or vision models. They also draw a developmental parallel: children get better at learning new words as they gain experience, as if they too were meta-learning."),
  T("What can you take from the paper as a learner? A powerful idea: sometimes you do not need a new kind of machine. You need a new kind of practice. Changing what a network practises can change what it understands."),
  T("Now you can read the original. Open the paper and look at Figure 1, then Figure 2, then Table 1. Check how each number matches what you have learned here. Notice how the authors share their data and code so that others can repeat the work, which is how science earns trust."),
  C("# a checklist for reading any results paper\nchecklist = ['What was the task?', 'What was compared?', 'Which numbers matter?', 'What did it not do?']\nfor i, q in enumerate(checklist):\n    print(i + 1, q)", "python")],
 [("Can MLC handle entirely new structures?", ["Not yet", "Always", "It never tries", "Only on Tuesdays"], 0, "Outside its meta-training distribution."),
  ("What is needed to emit new symbols?", ["A pointer mechanism", "More layers", "A bigger screen", "Nothing"], 0, "Copying unseen words."),
  ("Which parallel do the authors draw?", ["Children becoming better word learners", "Plants growing", "Clocks", "Cooking"], 0, "Learning with experience."),
  ("What might come next?", ["Meta-training for large language models", "Deleting networks", "Ignoring humans", "Stopping research"], 0, "Specialised training."),
  ("What does the paper share?", ["Data and code", "Nothing", "Only the abstract", "Passwords"], 0, "So others can repeat it."),
  ("What is the big lesson?", ["A new practice can change what a network understands", "Networks are magic", "Rules are useless", "People are slow"], 0, "Training matters.")],
 [("Limits", "New structures, new symbols, full language"), ("Next", "Language and vision models"), ("Children", "Better word learners with experience"), ("Big lesson", "New practice, new skill")],
 [MATCH("Match the limit", "Pair each statement with what it means.", [("new structures", "outside the meta-training episodes"), ("new symbols", "needs a pointer mechanism"), ("full language", "not yet tested"), ("replication", "others repeat it with shared data")]),
  FILL("Where next", "MLC works within its meta-training {{distribution}}. Emitting brand new symbols would need a {{pointer}} mechanism. The authors compare it with how {{children}} get better at learning words. The big lesson: a new kind of {{practice}} can change what a network learns."),
  ORDER("Order your reading", "Put the steps for reading the paper in order.", ["Read the abstract", "Study the figures and tables", "Check the methods", "Note the limits"])]))
