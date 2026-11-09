"""AI course, chapters 6-10."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

B = []

B.append(CH(
 "First-order logic and inference",
 ("FOL", [
  "First-order logic | adds | Objects and relations", "Quantifiers | are | For all and there exists", "Unification | matches | Two expressions",
  "Skolemisation | removes | Existentials", "Resolution | proves | By contradiction", "Prolog | uses | Backward chaining", "Ontology | organises | Concepts"]),
 ["Propositional logic cannot say that all humans are mortal without listing every human. First-order logic adds objects, relations, functions and quantifiers, so general facts are stated once.",
  "Inference uses unification: finding a substitution that makes two expressions identical. With unification, rules can be chained forward or backward, and resolution works on clauses with variables.",
  "The labs write a small unifier and a term matcher."],
 [("Predicate", "A relation over objects, such as Brother(x, y)."), ("Quantifier", "For all (∀) or there exists (∃)."), ("Term", "An expression that names an object."),
  ("Unifier", "A substitution that makes two expressions the same."), ("Skolem constant", "A new name that stands for an existential witness."), ("Ontology", "A structured vocabulary of categories and relations.")],
 ["Use implies with for-all and and with there-exists.", "Not-for-all x P is the same as there-exists x not P.", "Unification finds the most general substitution.",
  "The occur check stops a variable from binding to a term containing it.", "FOL entailment is semi-decidable.", "Prolog uses backward chaining on Horn clauses."],
 [T("First-order logic talks about objects and the relations between them. Constants name objects, predicates state relations, and functions map objects to objects. With the quantifier for-all and there-exists we make general claims."),
  T("A common mistake is the wrong connective. For all x, if Human of x then Mortal of x uses implies. Writing and would claim that everything is human and mortal. For there-exists we use and: some x is human and happy."),
  T("To reason, we need to match general rules against specific facts. Unification does this. To unify Knows(John, x) with Knows(y, Mary), we bind y to John and x to Mary. The result is the most general unifier: it commits to as little as needed."),
  T("Forward chaining applies rules to facts to derive new facts until a goal appears. Backward chaining works from the goal, finding rules whose conclusion matches and treating their premises as sub-goals. Prolog is built on backward chaining."),
  T("Resolution extends to first-order logic by converting sentences to clauses: remove implications, move negations inward, replace existentials by Skolem constants or functions, drop universal quantifiers. Then resolve clauses that unify. It is refutation-complete."),
  T("Building a knowledge base is knowledge engineering. Decide the vocabulary, encode general axioms, add the specific problem, and test by asking queries. Large shared vocabularies, called ontologies, organise categories such as events, time and substances.")],
 [("Which connective goes with for-all?", ["Implies", "And", "Or", "Xor"], 0, "For all x, P(x) implies Q(x)."),
  ("What does unification produce?", ["A substitution making expressions identical", "A truth table", "A probability", "A heuristic"], 0, "Variable bindings."),
  ("What is Prolog based on?", ["Backward chaining", "Hill climbing", "Minimax", "Genetic search"], 0, "On Horn clauses.")],
 [("What is a Skolem constant?", "A name for an existential witness."), ("What does the occur check prevent?", "A variable binding to a term containing itself."), ("Not-for-all x P equals?", "There exists x not P."), ("Is FOL entailment decidable?", "Only semi-decidable.")],
 [MATCH("Quantifier rules", "Match each statement to the right form.", [("Everyone who is human is mortal", "For all x: Human(x) implies Mortal(x)"), ("Someone is human and happy", "Exists x: Human(x) and Happy(x)"), ("Not everyone is happy", "Exists x: not Happy(x)")]),
  PL("Unify variables", "Write unify(a, b): a and b are terms. A term is a string (a constant if it starts with an upper-case letter, a variable if lower-case) or a list [functor, arg1, ...]. Return the substitution as a list of [variable, term] pairs sorted by variable name, or the string 'fail'. You may skip the occur check.",
     "unify(a, b)", """
def is_var(t):
    return isinstance(t, str) and t[0].islower()

def walk(t, s):
    while is_var(t) and t in s:
        t = s[t]
    return t

def unify(a, b):
    s = {}
    def go(x, y):
        x = walk(x, s)
        y = walk(y, s)
        if x == y:
            return True
        if is_var(x):
            s[x] = y
            return True
        if is_var(y):
            s[y] = x
            return True
        if isinstance(x, list) and isinstance(y, list) and len(x) == len(y) and x[0] == y[0]:
            for i in range(1, len(x)):
                if not go(x[i], y[i]):
                    return False
            return True
        return False
    if go(a, b):
        return [[k, s[k]] for k in sorted(s)]
    return 'fail'
""", [[["Knows", "John", "x"], ["Knows", "y", "Mary"]], ["A", "A"], ["A", "B"], [["F", "x", "x"], ["F", "A", "B"]], [["F", "x", ["G", "y"]], ["F", "A", ["G", "B"]]]], "Walk through bindings; recurse on arguments.", approx=None),
  PL("Substitute", "Write subst(term, s): apply the substitution dict s to term (a string or a list as in unify; variables are lower-case strings). Return the new term; replace variables repeatedly until none are bound.",
     "subst(term, s)", """
def subst(term, s):
    if isinstance(term, list):
        return [term[0]] + [subst(t, s) for t in term[1:]]
    if term[0].islower() and term in s:
        return subst(s[term], s)
    return term
""", [[["F", "x", "y"], {"x": "A", "y": ["G", "z"], "z": "B"}], ["x", {"x": "A"}], ["C", {"x": "A"}], [["P", ["Q", "x"]], {"x": "R"}]], "Recurse into lists; chase bindings.", approx=None)]))

B.append(CH(
 "Planning and knowledge representation",
 ("Planning", [
  "Planning | finds | Action sequences", "PDDL | describes | Actions and states", "Precondition | must hold | Before an action", "Effect | changes | The state",
  "Delete relaxation | gives | A heuristic", "HTN | refines | High-level tasks", "Ontology | structures | Categories"]),
 ["Classical planning finds a sequence of actions that turns an initial state into a goal in a deterministic, fully observable world. States are sets of facts. Each action has preconditions and effects that add and delete facts.",
  "A planner can search forward from the start, backward from the goal, or use heuristics from relaxed problems. Hierarchical task networks plan with high-level tasks refined into primitive steps, and are the practical choice in many applications.",
  "Knowledge representation organises the world into categories with inheritance, and supports default reasoning that can be withdrawn."],
 [("Fact", "An atomic statement that is true in a state."), ("Precondition", "Facts that must hold for an action to apply."), ("Effect", "Facts added and deleted by an action."),
  ("PDDL", "A standard language for describing planning problems."), ("HTN", "Hierarchical task network planning."), ("Default reasoning", "Concluding something unless told otherwise.")],
 ["A planning problem = initial state, actions, goal.", "An action applies if its preconditions are a subset of the state.", "Applying: remove the delete list, add the add list.",
  "Forward search is simple; heuristics make it practical.", "The delete-relaxation ignores deletions to estimate distance.", "Nonmonotonic reasoning lets conclusions be withdrawn."],
 [T("Planning is search with structure. Instead of an opaque state, the state is a set of facts, such as At(Robot, Kitchen) and Holding(Cup). Each action lists what must be true to do it and what it changes."),
  T("Take the action Move from X to Y. Its precondition is At(X). Its effect adds At(Y) and deletes At(X). To check whether an action applies, test that its preconditions are all in the state. To apply it, remove the deleted facts and add the new ones."),
  T("With this representation a forward planner searches from the initial state by trying every applicable action. A backward planner starts at the goal and finds actions that could have produced it. Both can use A star with a heuristic."),
  T("A good heuristic comes from relaxation. Pretend actions never delete anything. Then each action only helps, and the number of steps to reach the goal in the relaxed problem is a lower bound on the real number. Modern planners are built on such heuristics."),
  T("Real tasks are better organised hierarchically. To travel, first book, then go to the airport, then fly. A hierarchical task network stores such recipes and refines abstract tasks into concrete steps. The designer's knowledge shrinks the search."),
  T("Knowledge representation also asks how to organise categories. Objects belong to categories, categories form hierarchies and properties are inherited. Defaults such as birds fly are useful even though penguins are exceptions, so reasoning must be able to withdraw a conclusion.")],
 [("When does an action apply?", ["When its preconditions are in the state", "When its effects are in the state", "Always", "When the goal is reached"], 0, "Preconditions must hold."),
  ("What does the delete relaxation ignore?", ["Delete effects", "Preconditions", "The goal", "Costs"], 0, "So actions only add."),
  ("What is HTN planning?", ["Refining high-level tasks into primitive actions", "Random search", "Gradient descent", "Table lookup"], 0, "Hierarchical decomposition.")],
 [("What is PDDL?", "A planning language."), ("What does an effect do?", "Adds and deletes facts."), ("Why default reasoning?", "To use typical facts."), ("Forward versus backward planning?", "Start-to-goal versus goal-to-start.")],
 [ORDER("Applying an action", "Put the steps of applying an action in order.", ["Check that all preconditions are in the state", "Remove the facts on the delete list", "Add the facts on the add list", "Continue from the new state"]),
  PL("Apply action", "Write apply_action(state, pre, add, delete): all lists of fact strings. If every fact in pre is in state, return the new state as a sorted list (remove delete, add add, no duplicates); otherwise return the string 'no'.",
     "apply_action(state, pre, add, delete)", """
def apply_action(state, pre, add, delete):
    for p in pre:
        if p not in state:
            return 'no'
    s = set(state)
    for d in delete:
        s.discard(d)
    for a in add:
        s.add(a)
    return sorted(s)
""", [[["at_a", "have_key"], ["at_a"], ["at_b"], ["at_a"]], [["at_a"], ["at_b"], ["x"], []], [["at_a"], ["at_a"], ["at_a"], []], [[], [], ["p"], []]], "Check, delete, add, sort.", approx=None),
  PL("Plan length", "Write plan_length(state, goal, actions): actions is a list of [pre, add, delete] lists of fact strings. Use breadth-first search over states (as frozensets or sorted tuples converted to strings). Return the fewest actions needed to reach a state containing every goal fact, or -1.",
     "plan_length(state, goal, actions)", """
def plan_length(state, goal, actions):
    start = tuple(sorted(set(state)))
    seen = {start: 0}
    queue = [start]
    i = 0
    while i < len(queue):
        cur = queue[i]
        i += 1
        ok = True
        for g in goal:
            if g not in cur:
                ok = False
        if ok:
            return seen[cur]
        for pre, add, dele in actions:
            good = True
            for p in pre:
                if p not in cur:
                    good = False
            if good:
                s = set(cur)
                for d in dele:
                    s.discard(d)
                for a in add:
                    s.add(a)
                nxt = tuple(sorted(s))
                if nxt not in seen:
                    seen[nxt] = seen[cur] + 1
                    queue.append(nxt)
    return -1
""", [[["a"], ["c"], [[["a"], ["b"], ["a"]], [["b"], ["c"], ["b"]]]], [["a"], ["a"], []], [["a"], ["z"], [[["a"], ["b"], []]]], [["a"], ["d"], [[["a"], ["b"], ["a"]], [["b"], ["c"], ["b"]], [["c"], ["d"], ["c"]], [["a"], ["d"], ["a"]]]]], "BFS on sets of facts.", approx=None)]))

B.append(CH(
 "Uncertainty: probability and Bayes' rule",
 ("Probability", [
  "Probability | measures | Degrees of belief", "Joint distribution | answers | Every query", "Conditional probability | updates | Belief given evidence",
  "Bayes' rule | reverses | Conditioning", "Independence | factors | The joint", "Naive Bayes | assumes | Conditional independence", "Base rate | must be | Respected"]),
 ["An agent rarely knows the whole truth. Probability theory gives it a language for degrees of belief. Combined with utility it yields decision theory.",
  "From a full joint distribution any query can be answered by summing matching entries and dividing. Bayes' rule reverses a conditional: it turns the chance of symptoms given a disease into the chance of the disease given symptoms.",
  "The labs compute posteriors and a naive Bayes score."],
 [("Prior", "Belief before seeing evidence."), ("Posterior", "Belief after seeing evidence."), ("Conditional probability", "P(a | b) = P(a and b) / P(b)."),
  ("Independence", "Knowing one tells nothing about the other."), ("Likelihood", "P(evidence | hypothesis)."), ("Base rate", "How common the hypothesis is overall.")],
 ["Probabilities lie in 0..1 and sum to 1 over possible worlds.", "P(a or b) = P(a) + P(b) - P(a and b).", "Bayes: P(h | e) = P(e | h) P(h) / P(e).",
  "Ignoring the base rate causes many errors.", "Full joint tables grow as 2^n.", "Naive Bayes: P(cause, e1..en) = P(cause) times the product of P(ei | cause)."],
 [T("Logic fails when we are not sure. A patient with a toothache may have a cavity, or gum disease, or something else. Probability expresses how likely each is, given what we know."),
  T("The full joint distribution lists the probability of every combination of values. Given it, we can answer any question. To find the probability of a cavity given a toothache, sum the entries with both and divide by the sum of entries with a toothache."),
  M(r"P(h \mid e) \;=\; \frac{P(e \mid h)\,P(h)}{P(e)}"),
  T("This is Bayes' rule. It is useful because diagnostic knowledge, the chance of a disease given symptoms, is hard to collect, while causal knowledge, the chance of symptoms given the disease, is easier and more stable."),
  T("Here is a worked case. A disease affects 1 person in 10,000. A test catches it 99 percent of the time but gives a false alarm 1 percent of the time. If you test positive, the chance you are ill is about 1 percent. In 10,000 people there is one true positive and about 100 false positives. The base rate dominates."),
  T("Full joint tables are too large, so we use independence. Naive Bayes assumes the effects are independent given the cause, so the joint is the prior times a product of simple likelihoods. It is crude, but works well for tasks like spam filtering.")],
 [("What does Bayes' rule give?", ["P(h | e) from P(e | h) and priors", "P(e) only", "A heuristic", "A search tree"], 0, "It reverses conditioning."),
  ("In the rare disease example, why is the posterior small?", ["The base rate is tiny", "The test is random", "Probabilities do not apply", "False alarms are impossible"], 0, "Few ill people, many healthy."),
  ("What does naive Bayes assume?", ["Effects are independent given the cause", "Causes are equal", "No priors", "Effects are the same"], 0, "That keeps the model small.")],
 [("What is a prior?", "Belief before evidence."), ("What is a likelihood?", "P(evidence | hypothesis)."), ("Why full joints are hard?", "They grow exponentially."), ("What does normalising do?", "Makes values sum to one.")],
 [FILL("Bayes", "Bayes' rule multiplies the {{prior}} by the {{likelihood}} and divides by the probability of the evidence."),
  PL("Posterior", "Write posterior(prior, sens, fpr): prior = P(disease); sens = P(positive | disease); fpr = P(positive | no disease). Return P(disease | positive), rounded to 9 decimals.",
     "posterior(prior, sens, fpr)", """
def posterior(prior, sens, fpr):
    num = sens * prior
    den = num + fpr * (1 - prior)
    return round(num / den, 9)
""", [[0.0001, 0.99, 0.01], [0.5, 0.9, 0.1], [0.01, 0.8, 0.096], [0.3, 1.0, 0.0]], "Total probability in the denominator.", approx=1e-9),
  PL("Naive Bayes class", "Write nb_classify(priors, likes, features): priors is a dict class to probability; likes is a dict class to a dict feature to P(feature | class); features is a list of observed feature names. Return the class with the highest prior times the product of likelihoods (ties: first in dict order).",
     "nb_classify(priors, likes, features)", """
def nb_classify(priors, likes, features):
    best = None
    bs = -1.0
    for c in priors:
        s = priors[c]
        for f in features:
            s = s * likes[c][f]
        if s > bs:
            bs = s
            best = c
    return best
""", [[{"spam": 0.4, "ham": 0.6}, {"spam": {"free": 0.5, "meet": 0.05}, "ham": {"free": 0.05, "meet": 0.4}}, ["free"]], [{"spam": 0.4, "ham": 0.6}, {"spam": {"free": 0.5, "meet": 0.05}, "ham": {"free": 0.05, "meet": 0.4}}, ["meet"]], [{"a": 0.5, "b": 0.5}, {"a": {"x": 0.9, "y": 0.1}, "b": {"x": 0.2, "y": 0.8}}, ["x", "y"]]], "Multiply prior by each likelihood.", approx=None)]))

B.append(CH(
 "Bayesian networks",
 ("Bayes nets", [
  "Bayesian network | is | A directed acyclic graph", "CPT | quantifies | Each node", "Parents | cause | Their child",
  "D-separation | tests | Independence", "Enumeration | sums out | Hidden variables", "Variable elimination | speeds | Exact inference", "Sampling | approximates | Posteriors"]),
 ["A Bayesian network shows how variables depend on one another. Each node is a variable with a table giving its probability conditioned on its parents. The network represents the full joint compactly as a product of those local tables.",
  "To answer a query, sum over the hidden variables. Variable elimination does this efficiently. For networks that are too large, sampling methods approximate the answer.",
  "The labs compute a joint probability and answer a query by enumeration."],
 [("Node", "A random variable."), ("CPT", "Conditional probability table for a node given its parents."), ("Parent", "A node with an arrow into another."),
  ("Hidden variable", "A variable that is neither evidence nor the query."), ("Markov blanket", "Parents, children and the children's other parents."), ("Explaining away", "Evidence for one cause lowers belief in another.")],
 ["The joint is the product of P(X | parents(X)).", "A network with n Boolean nodes and at most k parents needs n times 2^k numbers.", "Enumeration sums the joint over hidden variables.",
  "A node is independent of non-descendants given its parents.", "Exact inference is hard in general; easy on trees.", "Likelihood weighting and Gibbs sampling approximate."],
 [T("Imagine a burglar alarm. A burglary or an earthquake may set it off. If it rings, either neighbour may call you. A Bayesian network draws arrows from burglary and earthquake to alarm, and from alarm to each call."),
  T("Each node stores a table. Burglary has a small prior. The alarm's table gives its chance of ringing for each combination of burglary and earthquake. A call's table depends only on the alarm."),
  M(r"P(x_1,\dots,x_n) \;=\; \prod_{i} P\bigl(x_i \mid \mathrm{parents}(x_i)\bigr)"),
  T("To find the chance of a burglary given that both neighbours called, enumerate: sum the joint over every value of the hidden variables (earthquake and alarm), then normalise across burglary or no burglary."),
  T("The network also shows independence. If you already know the alarm state, the calls tell you nothing more about the burglary. And when the alarm is observed, burglary and earthquake become competing explanations: hearing about an earthquake makes a burglary less likely. This is explaining away."),
  T("Variable elimination avoids repeating work by storing intermediate tables and summing out variables one at a time. When exact inference is too costly, approximate methods draw samples: likelihood weighting fixes the evidence and weights each sample, and Gibbs sampling walks through states by resampling one variable at a time.")],
 [("How does a Bayes net define the joint?", ["Product of each node given its parents", "Sum of the priors", "Maximum of tables", "Average of nodes"], 0, "The chain rule with independence."),
  ("What is explaining away?", ["A cause becomes less likely when another is confirmed", "Causes cancel", "Evidence is ignored", "A node is removed"], 0, "Competing explanations."),
  ("What does enumeration do with hidden variables?", ["Sums over them", "Ignores them", "Fixes them to zero", "Takes the maximum"], 0, "Marginalisation.")],
 [("What is a CPT?", "A conditional probability table."), ("What is a Markov blanket?", "Parents, children and co-parents."), ("What is Gibbs sampling?", "Resampling one variable at a time."), ("What is d-separation?", "A graph test for independence.")],
 [ORDER("Answering a query", "Put the steps of enumeration in order.", ["Fix the evidence variables", "For each query value, sum the joint over hidden variables", "Compute each joint term as a product of CPT entries", "Normalise the results so they sum to one"]),
  PL("Joint probability", "Write joint(cpt, parents, values): cpt maps a variable to a dict from a string key to P(variable true). The key is the parents' values joined as 'T'/'F' letters in the order given by parents[variable] (empty string if no parents). values maps variable to true/false. Return the probability of the full assignment, rounded to 9 decimals.",
     "joint(cpt, parents, values)", """
def joint(cpt, parents, values):
    p = 1.0
    for v in cpt:
        key = ''
        for q in parents[v]:
            if values[q]:
                key += 'T'
            else:
                key += 'F'
        pt = cpt[v][key]
        if values[v]:
            p = p * pt
        else:
            p = p * (1 - pt)
    return round(p, 9)
""", [[{"b": {"": 0.01}, "e": {"": 0.02}, "a": {"TT": 0.95, "TF": 0.94, "FT": 0.29, "FF": 0.001}}, {"b": [], "e": [], "a": ["b", "e"]}, {"b": True, "e": False, "a": True}], [{"b": {"": 0.01}, "e": {"": 0.02}, "a": {"TT": 0.95, "TF": 0.94, "FT": 0.29, "FF": 0.001}}, {"b": [], "e": [], "a": ["b", "e"]}, {"b": False, "e": False, "a": False}], [{"x": {"": 0.5}, "y": {"T": 0.9, "F": 0.2}}, {"x": [], "y": ["x"]}, {"x": True, "y": True}]], "Multiply each node's probability.", approx=1e-9),
  PL("Burglary query", "Write p_burglary(pb, pe, pa, pj, pm): pb = P(burglary), pe = P(earthquake), pa = a dict with keys 'TT','TF','FT','FF' (burglary then earthquake) for P(alarm), pj and pm are dicts with keys 'T','F' for P(John calls | alarm) and P(Mary calls | alarm). Return P(burglary | John and Mary both call), rounded to 6 decimals.",
     "p_burglary(pb, pe, pa, pj, pm)", """
def p_burglary(pb, pe, pa, pj, pm):
    tot = {}
    for b in (True, False):
        s = 0.0
        for e in (True, False):
            for a in (True, False):
                p = pb if b else 1 - pb
                p = p * (pe if e else 1 - pe)
                key = ('T' if b else 'F') + ('T' if e else 'F')
                p = p * (pa[key] if a else 1 - pa[key])
                ak = 'T' if a else 'F'
                p = p * pj[ak] * pm[ak]
                s += p
        tot[b] = s
    return round(tot[True] / (tot[True] + tot[False]), 6)
""", [[0.001, 0.002, {"TT": 0.95, "TF": 0.94, "FT": 0.29, "FF": 0.001}, {"T": 0.9, "F": 0.05}, {"T": 0.7, "F": 0.01}]], "Enumerate e and a; normalise over b.", approx=1e-6)]))

B.append(CH(
 "Reasoning over time",
 ("Time", [
  "Markov assumption | limits | History", "Filtering | estimates | Current state", "Prediction | looks | Ahead", "HMM | has | One hidden state",
  "Kalman filter | handles | Linear Gaussian", "Particle filter | uses | Samples", "Smoothing | revises | Past beliefs"]),
 ["Worlds change, and an agent must track hidden state over time from noisy observations. Temporal models assume the state depends on a bounded past (the Markov assumption) and each observation depends only on the current state.",
  "Filtering computes the belief about the present from all evidence so far, and can be updated recursively in constant time per step. Hidden Markov models, Kalman filters and particle filters are the main tools.",
  "The labs write one step of a prediction and a filtering update."],
 [("Hidden state", "What we want to know but cannot see."), ("Transition model", "P(next state | current state)."), ("Sensor model", "P(observation | state)."),
  ("Filtering", "Estimating the current state from all evidence."), ("HMM", "Hidden Markov model with one discrete state variable."), ("Particle filter", "Filtering by tracking weighted samples.")],
 ["Markov assumption: the present depends on a bounded past.", "Sensor assumption: observation depends on the current state only.", "Filtering update: predict, then weight by the evidence, then normalise.",
  "Smoothing uses future evidence to improve past estimates.", "Kalman filters: linear dynamics with Gaussian noise.", "Particle filters: propagate, weight, resample."],
 [T("A guard in a windowless room wants to know whether it is raining outside. The only clue each day is whether the visitor carries an umbrella. The weather is a hidden state that changes slowly; the umbrella is a noisy observation."),
  T("A model needs two tables. The transition model says how likely tomorrow's weather is, given today's. The sensor model says how likely an umbrella is, given the weather. With the Markov assumption, tomorrow depends on today only, not on the whole past."),
  M(r"P(X_{t+1}\mid e_{1:t+1}) \;\propto\; P(e_{t+1}\mid X_{t+1}) \sum_{x_t} P(X_{t+1}\mid x_t)\,P(x_t\mid e_{1:t})"),
  T("This is the filtering update. First predict: push the current belief through the transition model. Then update: multiply by how well each state explains the new observation, and normalise. The cost per step does not grow with time, so an agent can filter forever."),
  T("Other tasks use the same machinery. Prediction runs the transition model forward with no new evidence. Smoothing improves an estimate of the past using later evidence. The most likely sequence, found by the Viterbi algorithm, is used in speech recognition."),
  T("When the state is continuous, a Kalman filter keeps a Gaussian belief and is exact for linear dynamics. For nonlinear or multimodal problems, a particle filter keeps many samples: it moves each, weights it by the evidence, and resamples. Robots use particle filters to locate themselves on maps.")],
 [("What does the Markov assumption say?", ["The present depends only on a bounded past", "The future is random", "Nothing changes", "All history matters"], 0, "That keeps the model small."),
  ("What are the two steps of a filtering update?", ["Predict, then weight by evidence", "Sample, then sort", "Search, then prune", "Train, then test"], 0, "Then normalise."),
  ("What does a particle filter track?", ["Weighted samples", "A single mean", "A table of rules", "A tree"], 0, "Propagate, weight, resample.")],
 [("What is smoothing?", "Revising past estimates with later evidence."), ("What is the sensor model?", "P(observation | state)."), ("Why can filtering run forever?", "Constant cost per step."), ("Where are Kalman filters exact?", "Linear Gaussian systems.")],
 [MATCH("Tasks", "Match each task with what it computes.", [("Filtering", "Current state from evidence so far"), ("Prediction", "Future state"), ("Smoothing", "Past state using later evidence"), ("Viterbi", "Most likely state sequence")]),
  PL("Predict step", "Write predict(belief, trans): belief is a list of probabilities over states; trans[i][j] = P(next = j | current = i). Return the predicted belief list, each rounded to 9 decimals.",
     "predict(belief, trans)", """
def predict(belief, trans):
    n = len(belief)
    out = []
    for j in range(n):
        s = 0.0
        for i in range(n):
            s += belief[i] * trans[i][j]
        out.append(round(s, 9))
    return out
""", [[[0.5, 0.5], [[0.7, 0.3], [0.3, 0.7]]], [[1.0, 0.0], [[0.7, 0.3], [0.3, 0.7]]], [[0.2, 0.3, 0.5], [[0.5, 0.25, 0.25], [0.2, 0.6, 0.2], [0.1, 0.1, 0.8]]]], "Sum over previous states.", approx=1e-9),
  PL("Filter step", "Write filter_step(belief, trans, sensor, obs): sensor[j][o] = P(observation o | state j); obs is the observed index. Predict with trans, weight by the observation, normalise; return the new belief, each rounded to 9 decimals.",
     "filter_step(belief, trans, sensor, obs)", """
def filter_step(belief, trans, sensor, obs):
    n = len(belief)
    pred = []
    for j in range(n):
        s = 0.0
        for i in range(n):
            s += belief[i] * trans[i][j]
        pred.append(s)
    w = [pred[j] * sensor[j][obs] for j in range(n)]
    tot = sum(w)
    return [round(x / tot, 9) for x in w]
""", [[[0.5, 0.5], [[0.7, 0.3], [0.3, 0.7]], [[0.9, 0.1], [0.2, 0.8]], 0], [[0.5, 0.5], [[0.7, 0.3], [0.3, 0.7]], [[0.9, 0.1], [0.2, 0.8]], 1], [[0.818181818, 0.181818182], [[0.7, 0.3], [0.3, 0.7]], [[0.9, 0.1], [0.2, 0.8]], 0]], "Predict, weight, normalise.", approx=1e-8)]))
