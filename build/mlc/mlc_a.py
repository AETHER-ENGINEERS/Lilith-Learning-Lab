# -*- coding: utf-8 -*-
"""Meta-learning for compositionality, part 1: chapters 1-5. Based on Lake and Baroni (2023), Nature 623, 115-121 (CC BY 4.0)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "Why systematicity matters",
 ("Systematicity", []),
 ["People understand new combinations of words they already know. If you know what skip means and what twice means, you understand skip twice the first time you hear it. This skill is called systematic generalization, or compositionality.",
  "In 1988 the scientists Jerry Fodor and Zenon Pylyshyn argued that neural networks could not do this. For decades the argument has been debated, and even today's big networks often stumble on tests of it.",
  "In 2023 Brenden Lake and Marco Baroni published a paper in the journal Nature that trains a plain neural network in a new way, called meta-learning for compositionality or MLC. This course walks through that paper step by step."],
 [("Systematicity", "Understanding new combinations of known parts."),
  ("Compositionality", "Meaning of a whole built from the meanings of its parts and how they are put together."),
  ("Generalization", "Doing well on cases you were not trained on."),
  ("Neural network", "A learning program made of many simple adjustable units."),
  ("Fodor and Pylyshyn", "Authors of the 1988 argument that networks lack systematicity."),
  ("MLC", "Meta-learning for compositionality, the method from the paper.")],
 ["Systematic means new combinations of known parts.",
  "Humans do it easily, even from a few examples.",
  "Fodor and Pylyshyn (1988) said networks cannot.",
  "MLC is a training method, not a new kind of network.",
  "The paper is Lake and Baroni, Nature 2023."],
 [T("Think about learning a new word. Suppose you learn the word skip. Then someone says skip backwards. You have never heard those two together, yet you know exactly what to do. You did not need a lesson for that sentence."),
  T("That everyday magic is called systematic generalization. You take parts you already know and snap them together in a new way. Language works like Lego: a few pieces, endlessly many buildings."),
  T("The grid in the figure shows the idea. The green boxes are phrases you have met. The dashed pink boxes are phrases you have never met. A person who understands the pieces can read every box."),
  T("Why is this a big deal for computers? In 1988, Jerry Fodor and Zenon Pylyshyn wrote that neural networks could not do this kind of thing, because a network just matches patterns it has seen. They said real thinking needs rules for combining parts."),
  T("Many experiments since then agree that ordinary neural networks struggle. They can learn the phrases in their training set, but they often fail on new combinations. Even recent giant language models still make systematic mistakes on carefully built tests, as the paper's supplement reports for GPT-4."),
  T("This is the puzzle the paper tackles. Can a plain neural network, with no hand-built rule machinery, become systematic like people? The authors say yes, if it is trained in the right way. The rest of this course unpacks how."),
  C("# how many phrases from a few parts?\nverbs = 3\nmodifiers = 3\nprint('phrases with one modifier or none:', verbs * (modifiers + 1))", "python"),
  T("With only 3 verbs and 3 modifiers you already have 12 phrases. A person learns the 6 or so they hear and understands all 12. A system that only memorises would know the 6 and be lost on the rest. That gap is what the paper measures."),
  T("A word on honesty. This course is an educational retelling of the paper, written in our own words with our own simple examples. The paper is open access under a Creative Commons Attribution 4.0 licence. Please read the original too: Lake and Baroni, Nature 623, 115 to 121, 2023.")],
 [("What is systematic generalization?", ["Using known parts in new combinations", "Memorising every phrase", "Typing faster", "Guessing at random"], 0, "Lego pieces in new buildings."),
  ("If you know skip and twice, what does skip twice show?", ["You can combine known parts", "You memorised it", "A network error", "Nothing"], 0, "No lesson needed."),
  ("Who argued in 1988 that networks lack systematicity?", ["Fodor and Pylyshyn", "Lake and Baroni", "Turing", "Shannon"], 0, "The old challenge."),
  ("What is MLC?", ["A training method for a plain network", "A new kind of chip", "A programming language", "A game"], 0, "Meta-learning for compositionality."),
  ("Where was the paper published?", ["Nature, 2023", "A newspaper", "A blog", "A textbook from 1950"], 0, "Open access, CC BY 4.0."),
  ("Do giant language models solve systematicity completely?", ["Not yet", "Yes always", "They never try", "Nobody knows what they are"], 0, "Supplement tests on GPT-4 still show trouble.")],
 [("Systematicity", "New combinations of known parts"), ("Fodor and Pylyshyn", "Said networks cannot do it"), ("MLC", "Meta-learning for compositionality"), ("Lego", "Few pieces, endless buildings")],
 [MATCH("Match the idea", "Pair each term with its meaning.", [("Systematicity", "new combinations of known parts"), ("Generalization", "doing well on unseen cases"), ("MLC", "training through a stream of episodes"), ("Neural network", "many simple adjustable units")]),
  FILL("Big idea", "People are {{systematic}}: if you know skip and twice you understand {{skip twice}}. In 1988 {{Fodor}} and Pylyshyn doubted that neural networks could do this. The 2023 paper uses a training method called {{MLC}}."),
  PL("Count the phrases", "Write phrases(verbs, modifiers): how many phrases can you make with one verb and either no modifier or one modifier? That is verbs times (modifiers plus 1).", "phrases(verbs, modifiers)", '''
def phrases(verbs, modifiers):
    return verbs * (modifiers + 1)
''', [[3, 3], [4, 2], [10, 0], [5, 5]], "Add one for the no-modifier case."),
  PL("Spot the new ones", "Write new_phrases(seen, everything): return the phrases in everything that are not in seen, keeping their order.", "new_phrases(seen, everything)", '''
def new_phrases(seen, everything):
    out = []
    for p in everything:
        if p not in seen:
            out.append(p)
    return out
''', [[["skip", "walk twice"], ["skip", "skip twice", "walk twice", "walk"]], [[], ["a", "b"]], [["x"], ["x"]]], "Keep a phrase only if it is not in seen."),
  ORDER("Order the argument", "Put the story of the paper in order.", ["Humans combine known parts in new ways", "Fodor and Pylyshyn doubt networks can", "Networks still struggle on tests", "MLC trains a network on a stream of episodes"])]))

CHS.append(CH(
 "A tiny language and its rules",
 ("Pseudolanguage", []),
 ["To study systematic generalization, the researchers invented a small made-up language. A handful of nonsense words stand for coloured circles, and a few function words act on them.",
  "Each sentence has an exact answer, a row of coloured circles, that you can work out by following rules. The rules are called an interpretation grammar.",
  "The words and rules in this course are our own simple illustration in the same spirit as the paper's task. The meanings of the words are different for every person, so nobody can have memorised them."],
 [("Pseudolanguage", "A made-up language used for an experiment."),
  ("Primitive word", "A word that stands for one thing, such as a colour."),
  ("Function word", "A word that changes or combines other words."),
  ("Interpretation grammar", "Rules that turn a sentence into its answer."),
  ("Instruction", "A sentence in the language, with an answer."),
  ("Query", "A new instruction you must answer.")],
 ["Primitive words stand for colours.",
  "Function words act on other words.",
  "Our three: fep repeats, blicket sandwiches, kiki swaps.",
  "A grammar gives every sentence one exact answer.",
  "Word meanings are re-shuffled for each person."],
 [T("Imagine a game with a secret language. There are four colour words: dax is red, wif is green, lug is blue and zup is yellow. When you say a colour word, you point at a circle of that colour."),
  T("Words like these, that name one thing directly, are called primitives. Now add words that do things to other words. We call them function words, just like a function in a program takes input and returns an output."),
  T("Our first function word is fep. It repeats the circle three times: dax fep means red red red. The second is blicket. It sandwiches: wif blicket dax means green, red, green. The third is kiki. It swaps the order: lug kiki wif means green, blue."),
  T("The figure below lists all of them. Notice how little there is to learn: seven words in total. Yet they combine into endless sentences."),
  T("Sentences are read in pieces. In lug fep kiki wif the word kiki splits the sentence into two parts. The left part, lug fep, makes three blue circles. The right part, wif, is one green circle. Kiki then puts the right part first, so you get green then three blue."),
  C("# a tiny interpreter for our language\nlex = {'dax': 'R', 'wif': 'G', 'lug': 'B', 'zup': 'Y'}\nprint(lex['lug'] * 3)  # lug fep\nprint('G' + 'R' + 'G')   # wif blicket dax\nprint('G' + 'B')        # lug kiki wif", "python"),
  T("The rules for combining pieces are called an interpretation grammar. A grammar is a recipe that says how the meaning of a whole sentence comes from its parts. Our recipe is: split on kiki, then split each part on blicket, then apply fep to repeat."),
  T("In the paper's experiment the word meanings are changed for every participant, so dax might be red for you and blue for someone else. That is the key. Nobody can rely on memory of the language, and everybody must figure the rules out from the examples they get."),
  T("The paper's own task uses the same kind of design: four primitive words that map to coloured circles and three function words. Ours is simplified and not a copy of their stimuli, but the thinking skills needed are the same.")],
 [("What does a primitive word do?", ["Stands for one thing, like a colour", "Combines other words", "Counts words", "Ends a sentence"], 0, "dax means red."),
  ("What does fep do in our language?", ["Repeats three times", "Swaps order", "Sandwiches", "Deletes"], 0, "dax fep is red red red."),
  ("What is wif blicket dax?", ["Green, red, green", "Red, green", "Green, green, red", "Red, red"], 0, "x, then y, then x."),
  ("What is lug kiki wif?", ["Green, blue", "Blue, green", "Blue, blue", "Green, green"], 0, "Kiki swaps the order."),
  ("What is an interpretation grammar?", ["Rules that give a sentence its meaning", "A dictionary", "A list of colours", "A typing test"], 0, "A recipe for meaning."),
  ("Why shuffle word meanings per person?", ["So nobody can rely on memory", "To confuse the experts", "To save time", "No reason"], 0, "Forces rule discovery.")],
 [("dax fep", "Three copies"), ("wif blicket dax", "Green red green"), ("lug kiki wif", "Green blue"), ("Interpretation grammar", "Recipe for meaning")],
 [MATCH("Match the word to its job", "Pair each word type with its role.", [("dax", "primitive: names a colour"), ("fep", "function: repeats three times"), ("blicket", "function: x then y then x"), ("kiki", "function: swaps the order")]),
  FILL("The rules", "The word fep makes {{three}} copies. The word {{blicket}} gives x, then y, then x. The word kiki {{swaps}} the order. A set of rules that gives every sentence its answer is an interpretation {{grammar}}."),
  PL("Three rules", "Write apply_rule(rule, a, b): a and b are strings of colour letters. If rule is 'fep' return a repeated 3 times (ignore b). If rule is 'blicket' return a + b + a. If rule is 'kiki' return b + a.", "apply_rule(rule, a, b)", '''
def apply_rule(rule, a, b):
    if rule == 'fep':
        return a * 3
    if rule == 'blicket':
        return a + b + a
    return b + a
''', [["fep", "R", ""], ["blicket", "R", "G"], ["kiki", "R", "G"], ["fep", "RG", ""]], "Three small cases."),
  PL("Read a sentence", "Write interpret(sentence): the words are dax R, wif G, lug B, zup Y. Split the sentence on kiki (the second part goes first), split each part on blicket (x then y then x, left to right), and let fep make three copies of the piece before it. Return the colours as a string such as RGR.", "interpret(sentence)", '''
def interpret(sentence):
    lex = {'dax': 'R', 'wif': 'G', 'lug': 'B', 'zup': 'Y'}
    def atom(tokens):
        x = lex[tokens[0]]
        for t in tokens[1:]:
            if t == 'fep':
                x = x * 3
        return x
    parts = [[]]
    for t in sentence.split(' '):
        if t == 'kiki':
            parts.append([])
        else:
            parts[-1].append(t)
    out = ''
    for part in parts:
        groups = [[]]
        for t in part:
            if t == 'blicket':
                groups.append([])
            else:
                groups[-1].append(t)
        res = atom(groups[0])
        for g in groups[1:]:
            res = res + atom(g) + res
        out = res + out
    return out
''', [["dax"], ["lug fep"], ["wif blicket dax"], ["lug kiki wif"], ["lug fep kiki wif"], ["dax fep blicket lug"], ["zup kiki dax blicket wif"]], "Split on kiki, then on blicket, then repeat for fep."),
  ORDER("Order the reading", "Put the steps for reading lug fep kiki wif in order.", ["Split the sentence at kiki", "Make three blue circles for lug fep", "Make one green circle for wif", "Put the green part first, then the blue part"])]))

CHS.append(CH(
 "How people learn it: the few-shot experiment",
 ("Human experiment", []),
 ["In the paper's first experiment, 25 people learned such a language from only 14 study examples and then answered 10 new questions. This is few-shot learning: very few examples.",
  "People matched the exact rule 80.7 percent of the time, and 72.5 percent of their answers were right even when the answer was longer than any study example. Their mistakes were not random.",
  "The mistakes followed habits that you will meet in the next chapter. These habits are the clue that the researchers wanted their network to copy."],
 [("Few-shot", "Learning from a handful of examples."),
  ("Study example", "An instruction shown together with its answer."),
  ("Query", "A new instruction whose answer you must give."),
  ("Exact match", "An answer that is perfectly right, piece by piece."),
  ("Participant", "A person taking part in an experiment."),
  ("Catch trial", "An easy check used to spot people not paying attention.")],
 ["14 study examples, then 10 queries.",
  "People matched the rule 80.7 percent of the time.",
  "72.5 percent right on answers longer than any studied.",
  "Mistakes were patterned, not random.",
  "Meanings were re-shuffled for each person."],
 [T("Here is how the first experiment went. A person sat down and saw a few instructions with their answers, such as a word and its coloured circle. They studied 14 of these. The study moved in four stages from single words to words with functions."),
  T("Then came the test. The person saw 10 new instructions with no answers and had to build each answer from coloured circles. Some queries were chosen so that the answer was longer than any answer in the study set. That is a harder test of the rules."),
  T("The figure shows the results. In 80.7 percent of the 10-query answers, people produced exactly the answer the rules give. On the harder long-answer queries they were right 72.5 percent of the time. For people who see a made-up language for a few minutes, that is a strong performance."),
  T("The researchers recruited 30 people online and excluded 5 who missed the easy catch trials, leaving 25. Every person got a different assignment of words to meanings, so nobody could share answers or rely on a pattern from the internet."),
  T("Now the interesting part. When people were wrong, they were not wrong at random. About a quarter of the errors followed one pattern: using one circle per word, as if each word made its own piece. Another common mistake was to just write the pieces in the order they appeared. These patterns hint at hidden habits."),
  T("Habits like these are important for the research question. The paper wants a neural network that is as systematic as people and also as human-like in its mistakes. A perfect rule follower would be too clean. People are somewhere between clean rules and flexible guesses."),
  T("Try it yourself in the lab below. You will get a fresh language each time. Study the examples, then answer the questions. You may find that you make the same kind of slips as the people in the study.")],
 [("How many study examples did people get?", ["14", "100", "2", "1000"], 0, "Few-shot."),
  ("How many query instructions followed?", ["10", "1", "50", "None"], 0, "10 queries."),
  ("How often did people match the exact rule?", ["80.7 percent", "100 percent", "10 percent", "50 percent exactly"], 0, "Strong but not perfect."),
  ("What was special about some queries?", ["Longer answers than any studied", "They were in French", "They had no words", "They were easier"], 0, "A tougher test."),
  ("Were people's mistakes random?", ["No, they followed patterns", "Yes always", "They never made any", "Nobody checked"], 0, "Habits show up."),
  ("Why did meanings change per person?", ["So nobody could rely on memory", "To save money", "For fun", "It did not"], 0, "Forces rule discovery.")],
 [("14 then 10", "Study then query"), ("80.7%", "Matched the rule"), ("72.5%", "Right on longer outputs"), ("Patterned errors", "Hidden habits")],
 [MATCH("Match the number", "Pair each number with what it measures.", [("80.7%", "people matched the rule"), ("72.5%", "right on longer outputs"), ("14", "study examples"), ("10", "query instructions")]),
  FILL("The experiment", "People studied {{14}} instructions and then answered {{10}} new ones. They matched the rule {{80.7}} percent of the time. Their mistakes followed {{patterns}} instead of being random."),
  PL("Exact match rate", "Write exact_rate(answers, truths): the two lists are the same length and hold strings. Return the percent of positions where the answer equals the truth, rounded to 1 decimal.", "exact_rate(answers, truths)", '''
def exact_rate(answers, truths):
    good = 0
    for i in range(len(answers)):
        if answers[i] == truths[i]:
            good += 1
    return round(100.0 * good / len(answers), 1)
''', [[["RRR", "GB", "RG"], ["RRR", "GB", "GR"]], [["R"], ["R"]], [["R", "G", "B", "Y"], ["R", "G", "G", "Y"]]], "Count the equal positions."),
  PL("Longer than studied", "Write longer_share(answers, study_answers): return the percent (rounded to 1 decimal) of answers whose length is greater than the longest string in study_answers.", "longer_share(answers, study_answers)", '''
def longer_share(answers, study_answers):
    longest = 0
    for s in study_answers:
        if len(s) > longest:
            longest = len(s)
    n = 0
    for a in answers:
        if len(a) > longest:
            n += 1
    return round(100.0 * n / len(answers), 1)
''', [[["RRRR", "RG", "RRRRR"], ["RRR", "G", "GBG"]], [["R"], ["RR"]], [["RRRR", "RRRRR"], ["R"]]], "Find the longest study answer first."),
  ORDER("Order the experiment", "Put the steps of the study in order.", ["Learn a language from 14 examples", "Answer 10 new instructions", "Compare answers with the exact rule", "Look for patterns in the mistakes"])]))

CHS.append(CH(
 "Three habits of the human mind",
 ("Inductive biases", []),
 ["When examples do not settle an answer, people lean on built-in habits called inductive biases. The paper finds three that matter in this task: one-to-one mapping, iconic concatenation and mutual exclusivity.",
  "In a second experiment, 29 people guessed answers to seven instructions with no examples at all. That reveals their habits in the open. Most people used all of the habits at once.",
  "The goal of the paper is a network that is systematic like an algebra and also has these human habits, without having them written in by hand."],
 [("Inductive bias", "A built-in preference that guides guessing."),
  ("One-to-one mapping", "Each input word gives its own output piece."),
  ("Iconic concatenation", "Output pieces appear in the order of the words."),
  ("Mutual exclusivity", "Different instructions get different answers."),
  ("Open-ended task", "A test with no examples, to expose guessing habits."),
  ("Algebraic answer", "The exact answer the grammar gives.")],
 ["Inductive biases guide guesses when data runs out.",
  "One-to-one: one piece per word.",
  "Iconic concatenation: pieces in the order heard.",
  "Mutual exclusivity: different words, different answers.",
  "58.6 percent of people used all three together."],
 [T("Suppose someone shows you the words dax and wif with their colours and then asks what dax zorp wif means. You never saw zorp. What do you write? Most people write red then green: the pieces for the words they know, in the order they appear."),
  T("That is a habit. When knowledge runs out, the mind falls back on a default guess. Scientists call such a default an inductive bias: a push in a certain direction that comes from inside the learner, not from the examples."),
  T("The paper highlights three such habits. The first is one-to-one mapping. A word gets its own piece of the answer: two known words give two circles. The second is iconic concatenation: the pieces come in the same order as the words."),
  T("The third is mutual exclusivity. If two different instructions both appear, give them different answers. People assume that different words mean different things. Children use the same trick when they learn language."),
  T("The researchers measured this in a second experiment. In it, 29 people saw no examples at all and simply guessed answers to seven instructions. Doing this with no help shows the habits in the open."),
  T("The figure shows the result. A strong 93.1 percent gave each instruction its own unique answer. 79.3 percent used iconic concatenation, 62.1 percent used one-to-one mappings, and 58.6 percent used all three together."),
  C("# a one-to-one, in-order guess for an unknown function word\nlex = {'dax': 'R', 'wif': 'G', 'lug': 'B', 'zup': 'Y'}\nwords = 'dax zorp wif'.split(' ')\nguess = ''\nfor w in words:\n    if w in lex:\n        guess = guess + lex[w]\nprint(guess)", "python"),
  T("Why does this matter for machines? A plain neural network trained the usual way has no reason to prefer these guesses. A perfect symbolic program would follow the exact rule but would have no flexible guessing at all. People sit between. The researchers wanted a network that sits there too."),
  T("There is a neat twist. The habits are not wired into the network. They are written into the examples the network practises on, as you will see when we meet the training recipe. The network learns the habits from data, the way a child might.")],
 [("What is an inductive bias?", ["A built-in preference for guessing", "A mistake", "A kind of data", "A computer part"], 0, "A push from inside the learner."),
  ("What is one-to-one mapping?", ["One output piece per input word", "One word for everything", "Always one answer", "A random answer"], 0, "Two known words, two pieces."),
  ("What is iconic concatenation?", ["Output pieces in the order of the words", "Reversed pieces", "Only one piece", "Random order"], 0, "Same order as heard."),
  ("What is mutual exclusivity?", ["Different instructions get different answers", "All answers are the same", "Only one word is allowed", "Never guess"], 0, "Different words, different meanings."),
  ("What share of people gave every instruction a unique answer?", ["93.1 percent", "5 percent", "50 percent", "100 percent"], 0, "The strongest habit."),
  ("Where does MLC get the habits from?", ["From the data it practises on", "From hand-built code", "From a rulebook of grammar", "From nowhere"], 0, "Learned, not wired.")],
 [("One-to-one", "A piece per word"), ("Iconic order", "Pieces in word order"), ("Mutual exclusivity", "Different words, different answers"), ("93.1%", "Unique answers")],
 [MATCH("Match the habit", "Pair each habit with its description.", [("one-to-one", "each word gives its own piece"), ("iconic concatenation", "pieces appear in word order"), ("mutual exclusivity", "different instructions, different answers"), ("inductive bias", "a built-in guessing preference")]),
  FILL("The habits", "Without examples people use {{inductive}} biases. Giving each word its own piece is {{one-to-one}} mapping. Keeping the order of words is iconic {{concatenation}}. Giving different instructions different answers is mutual {{exclusivity}}."),
  PL("A one-to-one guess", "Write guess(sentence): the colour words are dax R, wif G, lug B, zup Y. Any other word is unknown. Split the sentence on spaces and return the colours of the known words in order, joined into a string. This is the one-to-one, in-order guess.", "guess(sentence)", '''
def guess(sentence):
    lex = {'dax': 'R', 'wif': 'G', 'lug': 'B', 'zup': 'Y'}
    out = ''
    for w in sentence.split(' '):
        if w in lex:
            out = out + lex[w]
    return out
''', [["dax zorp wif"], ["lug"], ["zup fep dax"], ["blorp"]], "Skip words that are not in the dictionary."),
  PL("All different?", "Write all_different(answers): return True if every answer in the list is different from the others, otherwise False. This checks mutual exclusivity.", "all_different(answers)", '''
def all_different(answers):
    seen = []
    for a in answers:
        if a in seen:
            return False
        seen.append(a)
    return True
''', [[["RG", "GR", "RRR"]], [["RG", "RG"]], [[]], [["R", "G", "R"]]], "Remember the answers you have seen."),
  PL("Share of people", "Write share(count, total): the percent of people who used a habit, rounded to 1 decimal.", "share(count, total)", '''
def share(count, total):
    return round(100.0 * count / total, 1)
''', [[27, 29], [23, 29], [18, 29], [17, 29]], "Count over total times 100."),
  ORDER("Order the guess", "Put the steps of a human-like guess in order.", ["See an instruction with an unknown word", "Keep one piece for each known word", "Put the pieces in the order heard", "Give a different answer to a different instruction"])]))

CHS.append(CH(
 "Why standard networks stumble",
 ("Standard networks", []),
 ["A standard neural network learns from many examples of one fixed task. It can memorise the training phrases very well, but memorising is not understanding.",
  "In the paper, a basic sequence-to-sequence network with no study examples and no meta-learning scored zero percent exact match on the few-shot task, because it never sees the new meanings.",
  "The network MLC uses is just as ordinary: a transformer with an encoder and a decoder. The difference is what it has been trained to do, not how it is built."],
 [("Sequence-to-sequence", "A network that turns one sequence into another."),
  ("Transformer", "A network that uses attention to relate all the pieces of its input."),
  ("Encoder", "The part that reads the input."),
  ("Decoder", "The part that writes the output one symbol at a time."),
  ("Attention", "A way for each piece to look at the other pieces."),
  ("Memorising", "Storing answers without learning a rule.")],
 ["Standard training teaches one fixed task.",
  "Memorising fails on new meanings.",
  "A basic seq2seq model scored 0 percent on the few-shot task.",
  "MLC uses a plain transformer encoder-decoder.",
  "The change is in the training, not the architecture."],
 [T("What happens when you train a normal network on our language? Give it thousands of sentences and answers. It will learn them. But if the meaning of dax changes for the next person, everything it memorised is wrong."),
  T("A good learner should not need to retrain for each new language. It should read the examples it is given and work out the meanings on the spot, like a person. A normal network has no way to do that, because its examples live in its training, not in its input."),
  T("The paper's baseline, a basic sequence-to-sequence network, shows this. It gets no study examples at test time. Its exact-match accuracy on the few-shot task is zero. It is a pure memoriser trying to guess at meanings it never saw."),
  T("Now meet the machine they use. It is a transformer. You can think of it as two parts. The encoder reads everything in the input and builds a rich description of it. The decoder then writes the answer one symbol at a time, glancing back at the encoder's description."),
  T("The figure shows the setup. In MLC the input is a single long string. It holds the study examples and the query together. So at test time the network has the examples in front of it, just like a person does."),
  T("This network is small: 3 layers and about 1.4 million adjustable numbers. By today's standards that is tiny. There are no special rule engines inside. The authors want to show that the training procedure, not clever hardware, makes the difference."),
  C("# a pure memoriser: it only knows what it has seen\nstudy = {'dax': 'R', 'lug fep': 'BBB'}\nfor q in ['dax', 'lug fep', 'lug']:\n    print(q, '->', study.get(q, '?'))", "python"),
  T("The code above is the memoriser in miniature. It answers questions it has seen and says a question mark for everything else, even lug on its own. A systematic learner would work out that lug means blue from lug fep. That reasoning step is what we want from a neural network.")],
 [("Why does a memoriser fail on a new language?", ["The meanings changed", "It is too fast", "It has no memory", "Nobody trained it"], 0, "Memorised answers are now wrong."),
  ("What did the basic seq2seq baseline score on the few-shot task?", ["0 percent", "100 percent", "80 percent", "50 percent"], 0, "It never sees the new meanings."),
  ("What does an encoder do?", ["Reads the input", "Writes the output", "Stores the weights", "Prints the result"], 0, "Reads everything first."),
  ("What does a decoder do?", ["Writes the output one symbol at a time", "Reads the input", "Cleans data", "Draws pictures"], 0, "One symbol at a time."),
  ("How big is the MLC transformer?", ["3 layers, about 1.4 million weights", "1000 layers", "One neuron", "A trillion weights"], 0, "Small and ordinary."),
  ("Where does the paper's change come from?", ["The training procedure", "A new chip", "Extra rule code inside", "More memory"], 0, "Same network, new training.")],
 [("Memoriser", "Knows only what it has seen"), ("Encoder", "Reads input"), ("Decoder", "Writes output"), ("0%", "Basic seq2seq on few-shot")],
 [MATCH("Match the part", "Pair each term with its job.", [("encoder", "reads the study examples and query"), ("decoder", "writes the answer one symbol at a time"), ("attention", "lets pieces look at each other"), ("memoriser", "stores answers without a rule")]),
  FILL("The network", "MLC uses a plain {{transformer}} with an encoder and a {{decoder}}. It has about 1.4 million weights. A basic model with no study examples scored {{0}} percent on the few-shot task because it only {{memorises}}."),
  PL("A memoriser", "Write memoriser(study, query): study is a list of [instruction, answer] pairs and query is a string. Return the answer for the query if it appears in study, otherwise return '?'.", "memoriser(study, query)", '''
def memoriser(study, query):
    for pair in study:
        if pair[0] == query:
            return pair[1]
    return '?'
''', [[[["dax", "R"], ["lug fep", "BBB"]], "dax"], [[["dax", "R"], ["lug fep", "BBB"]], "lug"], [[], "dax"], [[["a", "X"]], "a"]], "Loop over the pairs."),
  ORDER("Order the network", "Put the steps of how the transformer answers in order.", ["The input holds study examples and the query", "The encoder reads the whole input", "The decoder starts writing the answer", "The answer is finished one symbol at a time"])]))
