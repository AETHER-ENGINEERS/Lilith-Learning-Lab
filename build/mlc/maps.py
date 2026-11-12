# -*- coding: utf-8 -*-
"""One hierarchical concept map per chapter: a root, branches, leaves and a few cross links to other chapters."""
def M(title, text):
    return (title, [ln.strip() for ln in text.strip().split("\n") if ln.strip()])

MAPS = [[M("Systematicity", """
Systematicity | needs | Known parts
Systematicity | needs | New combinations
Systematicity | is tested by | Challenges to networks
Known parts | are like | Lego pieces
Known parts | include | Verbs such as skip
Known parts | include | Modifiers such as twice
New combinations | example | Skip backwards
New combinations | shown by | People easily
Challenges to networks | began with | Fodor and Pylyshyn 1988
Challenges to networks | still seen in | Large language models
Challenges to networks | answered by | MLC [ch7]
""")],
[M("Pseudolanguage", """
Pseudolanguage | has | Primitive words
Pseudolanguage | has | Function words
Pseudolanguage | has | A grammar
Primitive words | name | Coloured circles
Primitive words | include | dax wif lug zup
Function words | include | fep
Function words | include | blicket
Function words | include | kiki
fep | repeats | Three times
blicket | makes | x then y then x
kiki | swaps | The order
A grammar | gives | One exact answer
A grammar | is hidden from | Participants [ch3]
""")],
[M("Human experiment", """
Human experiment | has | Study phase
Human experiment | has | Query phase
Human experiment | has | Results
Study phase | shows | 14 examples
Study phase | shuffles | Word meanings per person
Query phase | asks | 10 new instructions
Query phase | includes | Longer answers than studied
Results | are | 80.7 percent rule matches
Results | are | 72.5 percent on longer outputs
Results | include | Patterned mistakes
Patterned mistakes | are explained by | Inductive biases [ch4]
""")],
[M("Inductive biases", """
Inductive biases | include | One-to-one mapping
Inductive biases | include | Iconic concatenation
Inductive biases | include | Mutual exclusivity
Inductive biases | are measured by | Open-ended task
One-to-one mapping | means | One piece per word
Iconic concatenation | means | Pieces in word order
Mutual exclusivity | means | Different words, different answers
Open-ended task | has | 29 people
Open-ended task | found | 93.1 percent mutual exclusivity
Open-ended task | found | 58.6 percent all three habits
Inductive biases | are learned by MLC from | Training targets [ch7]
""")],
[M("Standard networks", """
Standard networks | learn | One fixed task
Standard networks | fail | New meanings
Standard networks | include | Basic seq2seq
Standard networks | include | Transformer
One fixed task | leads to | Memorising
Memorising | cannot handle | Changed meanings
Basic seq2seq | scored | 0 percent on few-shot
Transformer | has | Encoder
Transformer | has | Decoder
Transformer | size in MLC | 3 layers and 1.4 million weights
Encoder | reads | Study examples and query
Decoder | writes | The answer symbol by symbol
Memorising | is fixed by | Meta-learning [ch6]
""")],
[M("Meta-learning", """
Meta-learning | practises | Learning itself
Meta-learning | uses | Episodes
Meta-learning | ends with | Frozen weights
Episodes | have | Study examples
Episodes | have | One query
Episodes | come in | A stream
A stream | changes | Word meanings each time
Word meanings each time | forces | Inferring from examples
Frozen weights | mean | No task-specific updates
Frozen weights | still allow | New tasks as input
Meta-learning | is put to work in | The MLC recipe [ch7]
""")],
[M("MLC recipe", """
MLC recipe | uses | Random grammars
MLC recipe | uses | Mixed targets
MLC recipe | uses | One plain transformer
Random grammars | make | Fresh episodes
Fresh episodes | pack | Study plus query as one input
Mixed targets | include | 80 percent algebraic
Mixed targets | include | 20 percent human-like
Human-like | learned from | Targets, not wiring
One plain transformer | trained with | Adam and 50 epochs
MLC recipe | has | Four variants
Four variants | include | Joint MLC
Four variants | include | Copy only
MLC recipe | is judged in | Results [ch8]
""")],
[M("Results", """
Results | compare | MLC and people
Results | compare | MLC and baselines
Results | use | Two scores
MLC and people | rule following | 82.4 against 80.7
MLC and people | longer outputs | 77.8 against 72.5
MLC and people | item difficulty | Correlation 0.788
MLC and baselines | basic seq2seq | 0 percent
MLC and baselines | symbolic model | Needs built-in biases
Two scores | include | Exact match
Two scores | include | Log-likelihood
Log-likelihood | prefers | Higher numbers
Results | continue on | Benchmarks [ch9]
""")],
[M("Benchmarks", """
Benchmarks | include | SCAN
Benchmarks | include | COGS
Benchmarks | show | Limits
SCAN | turns | Commands into actions
SCAN | add jump | 99.27 down to 0.22 percent
SCAN | around right | 51.13 down to 0.04 percent
COGS | turns | Sentences into logical forms
COGS | lexical | 6.08 down to 0.87 percent
Limits | include | SCAN length split
Limits | include | Three COGS structure splits
Limits | have | 100 percent error
Limits | are discussed in | Limits and lessons [ch10]
""")],
[M("Limits and lessons", """
Limits and lessons | include | Limits
Limits and lessons | include | Future work
Limits and lessons | include | Reading skills
Limits | include | New structures
Limits | include | New symbols
Limits | include | Full natural language
Future work | adds meta-training to | Language models
Future work | adds meta-training to | Vision models
Future work | looks at | Children learning words
Reading skills | include | Figures and tables first
Reading skills | include | Check data and code
New symbols | need | A pointer mechanism
""")]]
