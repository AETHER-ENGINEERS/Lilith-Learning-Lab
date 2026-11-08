"""Curry-Howard-Lambek course, chapters 5-8."""
from tlib import T, C, M

CH = []

# ------------------------------------------------------------ 5
CH.append({
    "title": "Computation is proof simplification",
    "maps": [{"title": "Normalization", "links": [
        "Detour | is | Introduction then elimination",
        "Detour | matches | Beta redex",
        "Cut elimination | matches | Beta reduction",
        "Normal proof | matches | Normal form",
        "Strong normalization | implies | Termination",
        "Strong normalization | implies | Consistency",
        "Consistency | means | No proof of false",
        "Type safety | needs | Progress and preservation",
        "Consistency [ch6] | is tested by | Classical axioms [ch6]"]}],
    "summary": [
        "A proof can contain a detour: you build a conjunction with and introduction and immediately take it apart with and elimination. Simplifying that detour away is the proof-theoretic twin of a beta reduction in a program.",
        "Running a program corresponds to normalizing a proof, and a normal proof is a program that has finished computing. Gentzen's cut elimination theorem is the same idea for his sequent calculus.",
        "Strong normalization of the simply typed lambda calculus shows that every well-typed program terminates, and as a bonus that the logic is consistent: there is no closed normal term of the empty type, so false cannot be proved."],
    "glossary": [
        {"term": "Detour", "def": "A step in a proof where an introduction rule is immediately followed by the matching elimination rule."},
        {"term": "Redex", "def": "A reducible expression, such as a lambda applied to an argument."},
        {"term": "Normal form", "def": "A term or proof with no redexes, so no detours."},
        {"term": "Cut elimination", "def": "Gentzen's result that proofs with detours can be rewritten to proofs without."},
        {"term": "Confluence", "def": "Different reduction orders reach the same normal form (Church-Rosser)."},
        {"term": "Preservation", "def": "If a term has type A and reduces, the result still has type A."},
        {"term": "Progress", "def": "A closed well-typed term is either a value or can take a reduction step."},
        {"term": "Consistency", "def": "The logic cannot prove false."}],
    "keyPoints": [
        "A beta redex is a proof detour; reducing it removes the detour.",
        "Normalization of a proof is evaluation of a program.",
        "Well-typed terms of the simply typed lambda calculus always terminate.",
        "Consistency follows: a closed proof of false would normalize to a closed normal term of the empty type, and there is none.",
        "Type safety is progress plus preservation: well-typed programs do not get stuck.",
        "Confluence says the normal form does not depend on the order of reduction."],
    "lesson": [
        T("Look at a detour. Take proofs of A and B, combine them with and introduction into a proof of A and B, then take the first component by and elimination. That proof is a roundabout way of writing the original proof of A. Removing the detour leaves the shorter proof."),
        M(r"\mathrm{fst}\,(M, N) \;\to\; M \qquad\qquad \mathrm{snd}\,(M, N) \;\to\; N"),
        T("In programs these are reduction rules. For functions the detour is implication introduction followed by implication elimination, and the reduction is beta."),
        M(r"(\lambda x.\, M)\, N \;\to_\beta\; M[N/x]"),
        T("For sums the detour is an injection followed by a case analysis. The case picks the matching branch and substitutes the carried value."),
        M(r"\mathrm{case}\;(\mathrm{inl}\, a)\;\mathrm{of}\;\{\mathrm{inl}\, x \Rightarrow M \mid \mathrm{inr}\, y \Rightarrow N\} \;\to\; M[a/x]"),
        T("A proof with no detours is in normal form. Normal proofs have a pleasant property, the subformula property: every formula that appears in the proof is a part of the conclusion or of an assumption. That makes normal proofs analyzable, and it is a key tool in proof theory."),
        T("Now the big theorem. For the simply typed lambda calculus every well-typed term has a normal form, and every reduction sequence from it ends. This is strong normalization. The standard proof uses a method called logical relations or reducibility candidates, introduced by Tait. The point to retain is the consequence: there are no infinite computations in typed programs of this kind."),
        T("Consistency follows by a short argument. Suppose the logic could prove false. Then there would be a closed term of the empty type. By strong normalization it would reduce to a closed normal term of the empty type. But there is no closed normal term of that type, because normal closed terms have a constructor at the head, and the empty type has no constructors. So false is not provable."),
        T("Type safety is a different guarantee, and is for programming languages with more features than STLC. It is stated as two lemmas. Progress: a closed well-typed term is a value or can step. Preservation: if a well-typed term steps, the result has the same type. Together they say that well-typed programs never get stuck."),
        T("Contrast with the untyped lambda calculus. The self-applying term omega applies a function to itself and reduces to itself forever. It cannot be typed in the simply typed calculus, because the type of x would have to be A and also A to B. That is exactly why typed calculi are consistent as logics, and why general recursion in a language is a logical danger: a recursive proof of anything would be a proof of false."),
        T("Use the Lambda Stepper in the practice section to watch beta reduction happen one step at a time, including the term omega that never stops.")],
    "quiz": [
        {"q": "What does a beta redex correspond to in a proof?", "options": ["An axiom", "A detour: introduction followed by elimination", "A hypothesis", "A truth table"], "answer": 1, "explain": "Beta reduction removes the detour created by a lambda applied to an argument."},
        {"q": "What does strong normalization of the simply typed lambda calculus guarantee?", "options": ["Every program is fast", "Every well-typed term reaches a normal form", "Every term is typable", "No term uses lambda"], "answer": 1, "explain": "No infinite reduction sequences exist from well-typed terms."},
        {"q": "Why does normalization give consistency?", "options": ["There is no closed normal term of the empty type", "All proofs are short", "Types are hidden", "Every term has a pair"], "answer": 0, "explain": "A closed proof of false would normalize to such a term, and none exists."},
        {"q": "Which two properties give type safety?", "options": ["Progress and preservation", "Confluence and eta", "Sums and products", "Currying and uncurrying"], "answer": 0, "explain": "Well-typed closed terms can step or are values, and stepping keeps the type."}],
    "cards": [
        {"q": "What is a detour?", "a": "An introduction rule immediately followed by its matching elimination."},
        {"q": "Why can omega not be typed?", "a": "x would have to have type A and type A to B at once."},
        {"q": "Proof normalization equals?", "a": "Evaluating a program."},
        {"q": "Progress + preservation gives?", "a": "Type safety."}],
    "practice": [
        {"type": "code", "title": "Is it in normal form?", "intro": "Terms are [\"var\", x], [\"lam\", x, body] or [\"app\", f, a]. Write isNormal(term): true when the term contains no beta redex, meaning no application whose function part is a lambda.", "fn": "isNormal",
         "starter": "function isNormal(term) {\n  // your code\n}",
         "tests": [{"args": [["var", "x"]], "expect": True}, {"args": [["lam", "x", ["var", "x"]]], "expect": True}, {"args": [["app", ["var", "f"], ["var", "x"]]], "expect": True}, {"args": [["app", ["lam", "x", ["var", "x"]], ["var", "y"]]], "expect": False}, {"args": [["lam", "z", ["app", ["lam", "x", ["var", "x"]], ["var", "z"]]]], "expect": False}, {"args": [["app", ["var", "f"], ["app", ["lam", "x", ["var", "x"]], ["var", "y"]]]], "expect": False}],
         "hint": "Recurse. An application is normal only if its function is not a lam and both its parts are normal.",
         "solution": "function isNormal(t) {\n  if (t[0] === 'var') return true;\n  if (t[0] === 'lam') return isNormal(t[2]);\n  if (t[1][0] === 'lam') return false;\n  return isNormal(t[1]) && isNormal(t[2]);\n}"},
        {"type": "match", "title": "Proof and program", "intro": "Match each proof idea to its program idea.", "pairs": [["Detour", "Beta redex"], ["Proof normalization", "Evaluation"], ["Normal proof", "Program that has finished"], ["Consistency", "No closed term of the empty type"]]},
        {"type": "webxdc", "title": "Lambda Stepper", "intro": "Type a lambda term, then step through beta reduction. Reduce any term to normal form in at least three steps to finish.", "height": 560, "html": "__LAMBDA__"}]
})

# ------------------------------------------------------------ 6
CH.append({
    "title": "Constructive and classical logic",
    "maps": [{"title": "Constructive vs classical", "links": [
        "Intuitionistic logic | matches | Typed lambda calculus",
        "Classical logic | adds | Excluded middle",
        "Excluded middle | is equivalent to | Double negation elimination",
        "Excluded middle | is equivalent to | Peirce's law",
        "Peirce's law | matches | call/cc",
        "Double negation translation | embeds | Classical in intuitionistic",
        "Constructive existence | gives | A witness",
        "Heyting algebra | models | Intuitionistic logic",
        "Control operators | match | Classical reasoning"]}],
    "summary": [
        "Constructive, or intuitionistic, logic is the logic that matches programs: to prove something exists you must be able to build it. It rejects the law of excluded middle, A or not A, as a general principle, because that law gives no way to decide which side holds.",
        "Classical logic adds excluded middle, or equivalently double negation elimination or Peirce's law. None of these has a program in the pure typed lambda calculus. Remarkably, Griffin discovered in 1990 that the type of Peirce's law is exactly the type of the call with current continuation operator, so control operators give classical logic a computational meaning.",
        "Classical logic is not lost: the double negation translation maps classical statements to intuitionistic ones, so constructive proofs can still carry classical reasoning, at the price of weaker conclusions."],
    "glossary": [
        {"term": "Excluded middle", "def": "The law that for every proposition A, either A or not A holds."},
        {"term": "Double negation elimination", "def": "The law that not not A implies A."},
        {"term": "Peirce's law", "def": "The law ((A to B) to A) to A. Classically valid, constructively not provable."},
        {"term": "Constructive proof", "def": "A proof that gives an explicit witness or algorithm."},
        {"term": "call/cc", "def": "Call with current continuation: a control operator that captures the rest of the computation."},
        {"term": "Double negation translation", "def": "A translation that embeds classical logic into intuitionistic logic by inserting double negations."},
        {"term": "Heyting algebra", "def": "A lattice with an implication operation. It is the algebra of intuitionistic logic."}],
    "keyPoints": [
        "Intuitionistic logic matches pure typed programs; classical logic needs more.",
        "A to not not A is provable constructively. Not not A to A is not.",
        "Excluded middle, double negation elimination and Peirce's law are equivalent over intuitionistic logic.",
        "A constructive proof of an exists statement yields a witness.",
        "call/cc has the type of Peirce's law, so classical reasoning means control effects.",
        "Classical logic can be embedded into intuitionistic logic by a double negation translation."],
    "lesson": [
        T("Excluded middle says every statement is either true or false. It sounds obvious, but as a program it would be a function that, for any proposition, hands you either a proof or a refutation. For the statement that a given program halts, no such function can exist, since the halting problem is undecidable. A constructive logic therefore does not assume it."),
        M(r"A \vee \neg A \qquad\qquad \neg\neg A \to A \qquad\qquad ((A \to B) \to A) \to A"),
        T("These three laws are the classical principles: excluded middle, double negation elimination and Peirce's law. Over intuitionistic logic they are equivalent, meaning that if you add any one as an axiom you can derive the other two. None is derivable without it."),
        T("Some of their neighbors are provable constructively. From a you can get not not a, since given a refutation k of a you can apply it to a. And not not not A implies not A holds too. What fails is the converse for double negation."),
        M(r"\lambda a.\, \lambda k.\, k\, a \;:\; A \to \neg\neg A \qquad\qquad \lambda h.\, \lambda a.\, h\,(\lambda k.\, k\, a) \;:\; \neg\neg\neg A \to \neg A"),
        T("A classic example of a non-constructive proof: there exist irrational numbers x and y such that x to the y is rational. Consider the square root of two to the square root of two. Either it is rational, and we are done, or it is irrational, and then raise it to the square root of two to get two. The proof never says which case holds, so it gives no witness. Constructive proofs avoid this."),
        T("Classical reasoning is not rejected as unsound. It just has a computational cost. In 1990 Timothy Griffin observed that the type of the control operator call with current continuation is Peirce's law. The operator captures what remains of the computation and lets you jump back to it, which is exactly the freedom classical logic gives you to change your mind.",
          "Another approach is to translate. The Godel-Gentzen negative translation puts double negations in front of the atoms and some connectives, and it turns every classically provable statement into an intuitionistically provable one. So constructive logic can express classical reasoning, in the weaker form that the statement is not false."),
        T("On the semantic side, intuitionistic logic is interpreted in Heyting algebras and, more generally, in toposes. A classic example takes the open sets of a topological space as the truth values. Implication is then an operation on open sets, and excluded middle fails unless every open set is also closed.",
          "The practical lesson for proof assistants is that Lean, Rocq and Agda are constructive by default, and you opt into classical axioms when you need them. In Lean the axiom is called Classical.em, and a proof that uses it is clearly marked as classical.")],
    "quiz": [
        {"q": "Which of these is provable in intuitionistic logic?", "options": ["not not A implies A", "A implies not not A", "A or not A", "Peirce's law"], "answer": 1, "explain": "Given a and a refutation k of A, apply k to a. The other three need a classical axiom."},
        {"q": "What is the type of Peirce's law?", "options": ["A to A", "((A to B) to A) to A", "A to B to A", "(A and B) to A"], "answer": 1, "explain": "That is the statement; Griffin showed call/cc inhabits it."},
        {"q": "Why does constructive logic not assume excluded middle?", "options": ["It is false", "It gives no algorithm to decide which side holds", "It is too short", "It uses types"], "answer": 1, "explain": "A proof of A or not A would have to tell you which one holds."},
        {"q": "What does the double negation translation do?", "options": ["Embeds classical logic into intuitionistic logic", "Removes all negations", "Turns programs into types", "Makes proofs shorter"], "answer": 0, "explain": "It maps classically valid statements to intuitionistically provable ones."}],
    "cards": [
        {"q": "Which direction of double negation is constructive?", "a": "A implies not not A. Not not A implies A needs a classical axiom."},
        {"q": "What type does call/cc have?", "a": "Peirce's law, ((A to B) to A) to A."},
        {"q": "Why is excluded middle not computable in general?", "a": "It would decide statements such as halting."},
        {"q": "Name the usual classical axioms.", "a": "Excluded middle, double negation elimination, Peirce's law."}],
    "practice": [
        {"type": "match", "title": "Provable or not?", "intro": "Match each statement to whether it is provable in intuitionistic logic.", "pairs": [["A implies not not A", "Provable"], ["not not not A implies not A", "Provable"], ["A or not A", "Needs a classical axiom"], ["not not A implies A", "Needs a classical axiom"], ["((A to B) to A) to A", "Needs a classical axiom"]]},
        {"type": "fill", "title": "Griffin's observation", "text": "The type of {{Peirce's law|peirce}} is the type of {{call/cc|callcc|call with current continuation}}. So {{classical|classical logic}} reasoning has a computational meaning as control {{effects|operators}}."},
        {"type": "write", "title": "No algorithm", "prompt": "In one or two sentences, explain why a function that decides A or not A for every statement A cannot exist, using the halting problem.", "checks": [{"re": "halt", "msg": "mentions halting"}, {"re": "decid|algorithm|program|function", "msg": "mentions deciding"}], "solution": "If it existed it would decide for every program whether it halts, but the halting problem is undecidable."}]
})

# ------------------------------------------------------------ 7
CH.append({
    "title": "Categories: objects, arrows and composition",
    "maps": [{"title": "Category basics", "links": [
        "Category | has | Objects",
        "Category | has | Morphisms",
        "Morphism | has | Domain and codomain",
        "Morphisms | compose by | Composition",
        "Composition | is | Associative",
        "Every object | has | Identity",
        "Isomorphism | is | Invertible morphism",
        "Functor | maps | Categories to categories",
        "Types and functions [ch8] | form | A category",
        "Proofs [ch9] | form | A category"]}],
    "summary": [
        "A category is a collection of objects and arrows between them. Arrows compose, composition is associative, and each object has an identity arrow that changes nothing. That is the whole definition.",
        "Many things are categories: sets and functions, a preorder where there is an arrow when one element is below another, a monoid with a single object, and, most importantly for us, a logic whose objects are propositions and whose arrows are proofs of entailment.",
        "An isomorphism is an arrow with a two-sided inverse. Category theory studies structure through arrows, not through what the objects are made of, which is exactly the right level to compare logic and programming."],
    "glossary": [
        {"term": "Object", "def": "A thing in a category; for us a proposition, a type or a set."},
        {"term": "Morphism", "def": "An arrow f : A to B from a domain A to a codomain B."},
        {"term": "Composition", "def": "Given f : A to B and g : B to C, the arrow g after f : A to C."},
        {"term": "Identity", "def": "For each object A, an arrow id on A that leaves any arrow unchanged under composition."},
        {"term": "Isomorphism", "def": "An arrow f : A to B with an inverse g : B to A such that both composites are identities."},
        {"term": "Functor", "def": "A map between categories that sends objects to objects and arrows to arrows, keeping identities and composition."},
        {"term": "Commuting diagram", "def": "A drawing in which any two paths between the same objects give equal arrows."}],
    "keyPoints": [
        "Category: objects, morphisms, composition, identities.",
        "Laws: (h after g) after f equals h after (g after f); id after f equals f equals f after id.",
        "Examples: Set (sets and functions), preorders, monoids, types and programs.",
        "A proof system is a category: objects are propositions, arrows are proofs of A entails B.",
        "Isomorphic objects are interchangeable for every purpose the category cares about.",
        "A functor preserves structure; later it maps syntax to meaning."],
    "lesson": [
        T("The definition fits on one line of notation. A category has objects, and for every pair of objects A and B a collection of arrows from A to B. Arrows that line up compose."),
        M(r"f : A \to B,\;\; g : B \to C \;\;\Longrightarrow\;\; g \circ f : A \to C \qquad\qquad \mathrm{id}_A : A \to A"),
        T("Two laws must hold. Composition is associative, so you can drop the brackets. Identity arrows do nothing."),
        M(r"h \circ (g \circ f) = (h \circ g) \circ f \qquad\qquad \mathrm{id}_B \circ f = f = f \circ \mathrm{id}_A"),
        T("Example one: the category Set. Its objects are sets and its arrows are functions. Composition is ordinary function composition and the identity is the function that returns its input.",
          "Example two: a preorder, such as the natural numbers with less than or equal. There is exactly one arrow from m to n when m is at most n. Composition says that m at most n and n at most k give m at most k, and the identity says that every number is at most itself. Here an arrow is a fact, not a function."),
        T("Example three: a monoid, such as strings with concatenation, is a category with a single object. The arrows are the elements, composition is the monoid operation and the identity arrow is the empty string."),
        T("Example four, which matters most to us: types and programs. Objects are types and arrows are programs, taken up to computation. This category is what Haskell programmers call Hask, although the real thing has some wrinkles with laziness. In a logic the same recipe gives a category whose objects are propositions and whose arrows from A to B are proofs of A entails B. Composition of proofs is cut, and identity is the trivial proof from A to A."),
        C("""# Categories hide inside everyday code
def compose(g, f):
    return lambda x: g(f(x))

identity = lambda x: x

# Laws, spot-checked
f = lambda x: x + 1
g = lambda x: x * 2
h = lambda x: x - 3
for x in range(5):
    assert compose(h, compose(g, f))(x) == compose(compose(h, g), f)(x)   # associativity
    assert compose(identity, f)(x) == f(x) == compose(f, identity)(x)     # identity""", "python"),
        T("An isomorphism is an arrow with an inverse in both directions. In Set the isomorphisms are the bijections. The type of pairs A x B is isomorphic to B x A via the swap function, which is its own inverse. Isomorphic types carry the same information in different clothes."),
        M(r"A \times B \;\cong\; B \times A \qquad\qquad (A \times B) \times C \;\cong\; A \times (B \times C)"),
        T("A functor is a map between categories that sends each object to an object and each arrow to an arrow, preserving identities and composition. In programming, a functor in the Haskell sense is a type constructor with a map operation. In logic and semantics, a functor takes syntax to meaning: it sends each type to a set and each program to a function, which is how chapter 9 interprets lambda calculus.")],
    "quiz": [
        {"q": "What data does a category consist of?", "options": ["Objects, morphisms, composition and identities", "Sets and truth tables", "Only functions", "Types and values"], "answer": 0, "explain": "Plus the associativity and identity laws."},
        {"q": "In a preorder viewed as a category, what is an arrow from m to n?", "options": ["A function", "The fact that m is below or equal to n", "A number", "A proof of false"], "answer": 1, "explain": "There is at most one arrow, and it expresses the order."},
        {"q": "What is an isomorphism?", "options": ["Any arrow", "An arrow with a two-sided inverse", "An identity", "A functor"], "answer": 1, "explain": "f and g with g after f and f after g both identities."},
        {"q": "In the logic-as-category, what are the arrows from A to B?", "options": ["Truth values", "Proofs that A entails B", "Programs only", "Symbols"], "answer": 1, "explain": "Composition of such arrows is cut, and identities are trivial proofs."}],
    "cards": [
        {"q": "Category laws?", "a": "Associativity of composition, and identity arrows."},
        {"q": "Category with one object?", "a": "A monoid."},
        {"q": "Isomorphism in Set?", "a": "A bijection."},
        {"q": "What does a functor preserve?", "a": "Identities and composition."}],
    "practice": [
        {"type": "code", "title": "Compose finite functions", "intro": "A function from {0..n-1} is an array f, meaning f(i) = f[i]. Write composeTables(f, g): the array for g after f, so h[i] = g[f[i]].", "fn": "composeTables",
         "starter": "function composeTables(f, g) {\n  // your code\n}",
         "tests": [{"args": [[1, 0, 2], [2, 2, 0]], "expect": [2, 2, 0]}, {"args": [[0, 1], [1, 0]], "expect": [1, 0]}, {"args": [[2, 2, 2], [5, 6, 7]], "expect": [7, 7, 7]}],
         "hint": "Map each index of f through g.",
         "solution": "function composeTables(f, g) {\n  return f.map(x => g[x]);\n}"},
        {"type": "code", "title": "Is it an isomorphism?", "intro": "In the category of finite sets an arrow f from {0..n-1} to {0..n-1} (an array of length n) is an isomorphism exactly when it is a bijection. Write isIso(f): true when every value 0 to n-1 appears exactly once.", "fn": "isIso",
         "starter": "function isIso(f) {\n  // your code\n}",
         "tests": [{"args": [[1, 0, 2]], "expect": True}, {"args": [[0, 0, 1]], "expect": False}, {"args": [[2, 1, 0, 3]], "expect": True}, {"args": [[0, 3]], "expect": False}, {"args": [[]], "expect": True}],
         "hint": "Use a Set of the values and check its size and range.",
         "solution": "function isIso(f) {\n  const n = f.length;\n  const s = new Set(f);\n  return s.size === n && f.every(x => Number.isInteger(x) && x >= 0 && x < n);\n}"},
        {"type": "match", "title": "Categories in the wild", "intro": "Match each category to its objects and arrows.", "pairs": [["Set", "Sets and functions"], ["A preorder", "Elements and order facts"], ["A monoid", "One object, elements as arrows"], ["A logic", "Propositions and proofs of entailment"]]}]
})

# ------------------------------------------------------------ 8
CH.append({
    "title": "Products, sums and exponentials",
    "maps": [{"title": "Universal constructions", "links": [
        "Product | is defined by | Projections and pairing",
        "Coproduct | is defined by | Injections and copairing",
        "Exponential | is defined by | Evaluation and currying",
        "Terminal object | is | Empty product",
        "Initial object | is | Empty coproduct",
        "Product [ch4] | models | Conjunction",
        "Coproduct [ch4] | models | Disjunction",
        "Exponential [ch4] | models | Implication",
        "Cartesian closed category | has | Terminal, products, exponentials",
        "Cartesian closed category [ch9] | is | Model of lambda calculus [ch9]"]}],
    "summary": [
        "Products, coproducts and exponentials are characterized by universal properties: each is the best object with a given set of arrows, unique up to isomorphism. They are the category-theory versions of pairs, sums and function types.",
        "A product A x B has two projections and a pairing operation. A coproduct A + B has two injections and a case operation.",
        "An exponential B to the A has an evaluation arrow and a currying operation, which turns arrows out of C x A into arrows C to B to the A.",
        "A category with a terminal object, binary products and exponentials is called cartesian closed. Adding an initial object and coproducts makes it bicartesian closed. This is the structure needed to interpret the typed lambda calculus."],
    "glossary": [
        {"term": "Universal property", "def": "A description of an object by how arrows into or out of it behave, which determines it up to isomorphism."},
        {"term": "Product", "def": "An object A x B with projections to A and B such that any pair of arrows into A and B factors uniquely through it."},
        {"term": "Coproduct", "def": "An object A + B with injections from A and B such that any pair of arrows out of A and B factors uniquely through it."},
        {"term": "Terminal object", "def": "An object with exactly one arrow into it from every object. Written 1."},
        {"term": "Initial object", "def": "An object with exactly one arrow out of it to every object. Written 0."},
        {"term": "Exponential", "def": "An object B to the A with an evaluation arrow from (B to the A) x A to B, representing arrows A to B inside the category."},
        {"term": "Cartesian closed category", "def": "A category with a terminal object, finite products and exponentials."},
        {"term": "Adjunction", "def": "A pair of functors with a natural bijection between arrows. Currying is the adjunction between product with A and exponential by A."}],
    "keyPoints": [
        "Product: arrows into A x B correspond to pairs of arrows into A and into B.",
        "Coproduct: arrows out of A + B correspond to pairs of arrows out of A and out of B.",
        "Exponential: arrows C x A to B correspond to arrows C to B to the A (currying).",
        "Terminal is the empty product and initial is the empty coproduct.",
        "Cartesian closed: terminal object, products, exponentials. These model simply typed lambda calculus.",
        "In finite sets the sizes obey: product is multiplication, coproduct is addition, exponential is power."],
    "lesson": [
        T("A product is defined by what arrows do, not by what it is made of. The product of A and B is an object P with two projection arrows, one to A and one to B, such that for every object C with arrows f to A and g to B there is exactly one arrow from C to P that gives f and g back when followed by the projections."),
        M(r"\pi_1 \circ \langle f, g\rangle = f \qquad\qquad \pi_2 \circ \langle f, g\rangle = g \qquad\qquad \langle f, g\rangle : C \to A \times B"),
        T("In Set the product is the set of pairs, and the pairing arrow builds a pair from the two component functions. The dual notion, the coproduct, swaps the direction of every arrow. It has injections into the sum and a case arrow out of it."),
        M(r"[f, g] \circ \mathrm{in}_1 = f \qquad\qquad [f, g] \circ \mathrm{in}_2 = g \qquad\qquad [f, g] : A + B \to C"),
        T("In Set the coproduct is the disjoint union, and in programs it is the sum type: a value tagged left or right. Terminal and initial objects are the zero-fold cases. The terminal object 1 has one arrow in from everything, and in Set it is a one-element set. The initial object 0 has one arrow out to everything, and in Set it is the empty set."),
        T("Now the exponential, which is the interesting one. We want an object that stands for all arrows from A to B, so that functions become ordinary values. It comes with an evaluation arrow that applies such a function to an argument."),
        M(r"\mathrm{ev} : B^A \times A \to B \qquad\qquad \Lambda f : C \to B^A \;\text{ for each } f : C \times A \to B"),
        T("This is currying. An arrow from C times A to B can be turned into an arrow from C to the function object, and back again. The correspondence is a bijection."),
        M(r"\mathrm{Hom}(C \times A,\, B) \;\cong\; \mathrm{Hom}(C,\, B^A)"),
        T("A cartesian closed category, or CCC, has a terminal object, binary products, and exponentials. Set is one. So is the category of types and functions in a typed language. A preorder that is cartesian closed has meets as products and a Heyting-style implication as the exponential, and the isomorphism above becomes the rule that C and A entails B exactly when C entails A implies B. Add joins and a bottom element and you have a Heyting algebra, the algebra of intuitionistic logic."),
        T("There is also a pleasant arithmetic. In the category of finite sets, a set with m elements and a set with n elements have a product of m times n elements, a coproduct of m plus n, and an exponential of n to the m, which is the number of functions. Many identities of school algebra then come for free as isomorphisms of types: the exponent of a sum is a product of exponents, and the exponent of a product is an iterated exponent, which is currying again."),
        M(r"C^{A+B} \;\cong\; C^A \times C^B \qquad\qquad C^{A \times B} \;\cong\; (C^B)^A \qquad\qquad A \times (B + C) \;\cong\; (A \times B) + (A \times C)")],
    "quiz": [
        {"q": "What does the product of A and B come with?", "options": ["Two projections and a unique pairing property", "Two injections", "A single arrow", "An evaluation arrow"], "answer": 0, "explain": "Projections to A and to B, and each pair of arrows into them factors uniquely."},
        {"q": "What is the terminal object in Set?", "options": ["The empty set", "A one-element set", "The natural numbers", "A two-element set"], "answer": 1, "explain": "Every set has exactly one function into a one-element set."},
        {"q": "Which statement is currying?", "options": ["Hom(C x A, B) is isomorphic to Hom(C, B to the A)", "A x B is isomorphic to B x A", "A + 0 is isomorphic to A", "1 is isomorphic to 0"], "answer": 0, "explain": "Arrows out of a product correspond to arrows into an exponential."},
        {"q": "How many functions are there from a 3-element set to a 2-element set?", "options": ["6", "8", "9", "5"], "answer": 1, "explain": "Exponential: 2 to the power 3 equals 8."}],
    "cards": [
        {"q": "Coproduct in Set?", "a": "Disjoint union."},
        {"q": "Exponential in Set?", "a": "The set of functions B to the A."},
        {"q": "What makes a category cartesian closed?", "a": "Terminal object, binary products and exponentials."},
        {"q": "Sizes in finite sets?", "a": "Product multiplies, coproduct adds, exponential is a power."}],
    "practice": [
        {"type": "code", "title": "Counting inhabitants", "intro": "Write homSize(kind, a, b) for finite sets with a and b elements: 'product' gives a*b, 'coproduct' gives a+b, 'exponential' gives the number of functions from an a-element set to a b-element set, 'terminal' gives 1 and 'initial' gives 0.", "fn": "homSize",
         "starter": "function homSize(kind, a, b) {\n  // your code\n}",
         "tests": [{"args": ["product", 3, 4], "expect": 12}, {"args": ["coproduct", 3, 4], "expect": 7}, {"args": ["exponential", 3, 2], "expect": 8}, {"args": ["exponential", 2, 3], "expect": 9}, {"args": ["terminal", 5, 5], "expect": 1}, {"args": ["initial", 5, 5], "expect": 0}],
         "hint": "An exponential from an a-set to a b-set is Math.pow(b, a).",
         "solution": "function homSize(kind, a, b) {\n  if (kind === 'product') return a * b;\n  if (kind === 'coproduct') return a + b;\n  if (kind === 'exponential') return Math.pow(b, a);\n  if (kind === 'terminal') return 1;\n  return 0;\n}"},
        {"type": "match", "title": "Universal constructions", "intro": "Match each construction to its logical and programming reading.", "pairs": [["Product", "And, pair type"], ["Coproduct", "Or, sum type"], ["Exponential", "Implies, function type"], ["Terminal object", "True, unit type"], ["Initial object", "False, empty type"]]},
        {"type": "fill", "title": "School algebra for types", "text": "A function from Bool times Bool to Bool: there are {{16}} of them, since 2 to the power 4 is 16. The type A to (B to C) is isomorphic to (A times B) to C by {{currying|curry}}. A sum type adds the sizes and a pair type {{multiplies|multiply}} them."}]
})
