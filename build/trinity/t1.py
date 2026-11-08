"""Curry-Howard-Lambek course, chapters 1-4."""
from tlib import T, C, M

CH = []

# ------------------------------------------------------------ 1
CH.append({
    "title": "Three views of one idea",
    "maps": [{"title": "Computational trinitarianism", "links": [
        "Logic [ch2] | has | Propositions and proofs",
        "Programming [ch3] | has | Types and programs",
        "Category theory [ch7] | has | Objects and morphisms",
        "Propositions and proofs | correspond to | Types and programs",
        "Types and programs | correspond to | Objects and morphisms",
        "Objects and morphisms | correspond to | Propositions and proofs",
        "Curry-Howard [ch4] | links | Logic [ch2]",
        "Curry-Howard [ch4] | links | Programming [ch3]",
        "Lambek [ch9] | links | Programming [ch3]",
        "Lambek [ch9] | links | Category theory [ch7]"]}],
    "summary": [
        "Logic, programming and category theory look like three separate subjects, but they describe the same structure in three vocabularies. A proposition is a type, a proof is a program, and both are an object and a morphism in a category.",
        "The first link is the Curry-Howard correspondence between proofs and programs. The second is the Lambek correspondence between typed programs and categories. Together they are often called the Curry-Howard-Lambek correspondence, or computational trinitarianism, a slogan associated with Robert Harper.",
        "Why care? Each view brings tools to the others. Logic gives you a way to say what a program means. Programming gives a proof something you can run. Category theory gives the common language that shows the three are the same shape."],
    "glossary": [
        {"term": "Curry-Howard correspondence", "def": "The match between logical propositions and types, and between proofs and programs."},
        {"term": "Lambek correspondence", "def": "The match between typed lambda calculus and cartesian closed categories."},
        {"term": "Computational trinitarianism", "def": "The slogan that logic, type theory and category theory are three aspects of one thing."},
        {"term": "Proposition", "def": "A statement that can be true or false, such as A implies B."},
        {"term": "Type", "def": "A classification of programs by the kind of value they compute."},
        {"term": "Category", "def": "A collection of objects with arrows (morphisms) between them that compose."},
        {"term": "Constructive proof", "def": "A proof that shows how to build the thing it claims exists."}],
    "keyPoints": [
        "Three views: logic (propositions, proofs), programs (types, terms), categories (objects, morphisms).",
        "Curry-Howard: a proof of A implies B is a function from proofs of A to proofs of B.",
        "Lambek: a typed program is an arrow between objects in a cartesian closed category.",
        "The correspondence is exact for constructive (intuitionistic) logic, not for classical logic out of the box.",
        "This is the idea behind proof assistants such as Lean, Rocq and Agda.",
        "You do not need advanced math to start: every idea in this course is introduced with small examples."],
    "lesson": [
        T("Start with something you already know. A function that takes a pair and returns its first component has the type from A and B to A. Now read the same shape as logic: from A and B, conclude A. It is a valid inference. The function is a proof, and the type is the statement it proves."),
        C("""def first(pair: tuple[int, str]) -> int:
    return pair[0]

# As logic:   A and B  implies  A
# As a type:  (A x B) -> A
# As a proof: the program first""", "python"),
        T("Now the identity function. It has the type from A to A. As a statement, A implies A. As a program, it returns its argument. As a proof, assume A and conclude A, which is exactly what the function does with its input.",
          "Notice how little work the word proof does here. The program is the proof. Checking that the program has that type is checking the proof."),
        M(r"A \to A \qquad\qquad A \wedge B \to A \qquad\qquad A \to (B \to A)"),
        T("Three statements, three programs: the identity, the first projection, and the function that takes a and then b and returns a. All of them are provable, all of them are programs, and all of them are arrows in a category.",
          "The third view says the same again. Treat each type as a dot and each function as an arrow between dots. Programs compose by running one after another. There is an identity arrow at every dot. That is already the definition of a category, which you meet in chapter 7."),
        C("""Logic               Programming            Category theory
---------------------------------------------------------------
proposition         type                   object
proof               program (term)         morphism (arrow)
A implies B         function type A -> B   exponential object
A and B             pair type A x B        product
A or B              sum type A + B         coproduct
true                unit type              terminal object
false               empty type             initial object""", "text"),
        T("A word of care. Not every logic fits so neatly. Classical logic, which allows excluded middle and double negation elimination, needs extra machinery, and chapter 6 shows how it connects to control operators like call with current continuation.",
          "Where we are going: logic and natural deduction in chapter 2, typed lambda calculus in chapter 3, the correspondence in chapter 4, computation as proof simplification in chapter 5, classical versus constructive in chapter 6, categories in chapters 7 and 8, the Lambek step in chapter 9, then dependent types, proof assistants and the wider picture."),
        T("A little history, hedged because the details are debated. Haskell Curry noticed in the 1930s and 1950s that the types of combinators look like axioms of implicational logic. William Howard wrote down the full correspondence for natural deduction in 1969, circulated as a note and published in 1980. Joachim Lambek connected deductive systems and categories in the late 1960s and 1970s. Per Martin-Lof's type theory then made the idea a foundation for mathematics and programming.")],
    "quiz": [
        {"q": "In the Curry-Howard correspondence, what corresponds to a proof?", "options": ["A type", "A program", "A category", "A symbol"], "answer": 1, "explain": "A proof of a proposition is a program whose type is that proposition."},
        {"q": "Which type is the logical statement A and B implies A?", "options": ["A -> B", "(A x B) -> A", "A + B", "A -> (B + A)"], "answer": 1, "explain": "From a pair you can take the first component, so (A x B) -> A is inhabited by the first projection."},
        {"q": "What is the Lambek side of the triangle?", "options": ["Typed programs as arrows in a cartesian closed category", "Proofs as truth tables", "Types as numbers", "Logic as hardware"], "answer": 0, "explain": "Lambek connected typed lambda calculus with cartesian closed categories."},
        {"q": "What does the unit type correspond to in logic?", "options": ["False", "True", "A or B", "Negation"], "answer": 1, "explain": "The unit type has exactly one value, so it is always inhabited, like the proposition true."}],
    "cards": [
        {"q": "Propositions as ...?", "a": "Types."},
        {"q": "Proofs as ...?", "a": "Programs."},
        {"q": "Types and programs as ...?", "a": "Objects and morphisms of a category."},
        {"q": "Who is the slogan computational trinitarianism associated with?", "a": "Robert Harper (it is also used on the nLab)."}],
    "practice": [
        {"type": "match", "title": "Translate the vocabulary", "intro": "Match each logic word with its programming word.", "pairs": [["Proposition", "Type"], ["Proof", "Program"], ["A implies B", "Function from A to B"], ["A and B", "Pair of A and B"], ["True", "Unit type"]]},
        {"type": "fill", "title": "Fill the triangle", "text": "Logic says {{proposition}}, programming says {{type}}, and category theory says {{object}}. A proof is a {{program|term}}, which is also a {{morphism|arrow}}."},
        {"type": "write", "title": "Read it three ways", "prompt": "Take the identity function from A to A. In one or two sentences, say what it is as a proof, as a program and as a category-theory arrow.", "checks": [{"re": "proof|prove", "msg": "mentions proof"}, {"re": "program|function", "msg": "mentions program"}, {"re": "arrow|morphism|identity", "msg": "mentions arrow or identity"}], "solution": "As a proof it shows A implies A. As a program it returns its input. As an arrow it is the identity morphism on A."}]
})

# ------------------------------------------------------------ 2
CH.append({
    "title": "Logic and natural deduction",
    "maps": [{"title": "Natural deduction", "links": [
        "Judgment | has form | Context turnstile Proposition",
        "Connective | has | Introduction rule",
        "Connective | has | Elimination rule",
        "Introduction rule | builds | Proof",
        "Elimination rule | uses | Proof",
        "BHK interpretation | explains | Proofs as constructions",
        "Implication | introduced by | Discharging assumption",
        "Intuitionistic logic [ch6] | omits | Excluded middle [ch6]",
        "Natural deduction | becomes | Lambda calculus [ch3]"]}],
    "summary": [
        "Natural deduction is a way to write proofs as trees of small rules. Each logical connective has an introduction rule, which says how to prove it, and an elimination rule, which says how to use it.",
        "A judgment has the form Gamma proves A: from the assumptions in Gamma we can conclude A. Proving an implication means assuming the premise and proving the conclusion; that assumption is then discharged.",
        "The Brouwer-Heyting-Kolmogorov, or BHK, reading explains the rules constructively: a proof of A and B is a pair of proofs, a proof of A implies B is a method turning proofs of A into proofs of B, and there is no proof of false."],
    "glossary": [
        {"term": "Judgment", "def": "A claim of the form Gamma proves A, meaning A follows from assumptions Gamma."},
        {"term": "Context", "def": "The list of assumptions available, written Gamma."},
        {"term": "Introduction rule", "def": "A rule that tells you how to prove a connective."},
        {"term": "Elimination rule", "def": "A rule that tells you how to use a proven connective."},
        {"term": "Discharge", "def": "To remove an assumption once the implication that depends on it has been proven."},
        {"term": "BHK interpretation", "def": "The constructive meaning of proofs: pairs for and, functions for implies, tagged proofs for or."},
        {"term": "Ex falso", "def": "From false you may conclude anything."},
        {"term": "Intuitionistic logic", "def": "Logic without excluded middle, matching constructive proofs."}],
    "keyPoints": [
        "Propositions: atoms, true, false, and, or, implies. Negation of A is A implies false.",
        "Every connective has an introduction rule and an elimination rule.",
        "Implication introduction discharges an assumption.",
        "Or elimination is proof by cases.",
        "BHK: and is a pair, implies is a function, or is a tagged choice, false has no proof.",
        "A proof tree is a data structure, and that is why it can later be read as a program."],
    "lesson": [
        T("The grammar of propositions is small. A proposition is an atom P, or true, or false, or A and B, or A or B, or A implies B. We write negation not A as an abbreviation for A implies false."),
        M(r"A, B \;::=\; P \;\mid\; \top \;\mid\; \bot \;\mid\; A \wedge B \;\mid\; A \vee B \;\mid\; A \to B \qquad\qquad \neg A := A \to \bot"),
        T("A judgment Gamma proves A is read: assuming everything in Gamma, A holds. The rules say how judgments follow from other judgments. We write the premises above a line and the conclusion below. Here are the rules for implication."),
        M(r"\frac{\Gamma, A \vdash B}{\Gamma \vdash A \to B}\;(\to\!I) \qquad\qquad \frac{\Gamma \vdash A \to B \quad \Gamma \vdash A}{\Gamma \vdash B}\;(\to\!E)"),
        T("Implication introduction says: to prove A implies B, assume A and prove B. The assumption is only available inside that proof. Implication elimination is modus ponens: from A implies B and A, conclude B. Now the rules for and."),
        M(r"\frac{\Gamma \vdash A \quad \Gamma \vdash B}{\Gamma \vdash A \wedge B}\;(\wedge I) \qquad \frac{\Gamma \vdash A \wedge B}{\Gamma \vdash A}\;(\wedge E_1) \qquad \frac{\Gamma \vdash A \wedge B}{\Gamma \vdash B}\;(\wedge E_2)"),
        T("To prove A and B, prove both. From A and B you can take either part. Now the rules for or, where the elimination rule is a proof by cases."),
        M(r"\frac{\Gamma \vdash A}{\Gamma \vdash A \vee B}\;(\vee I_1) \qquad \frac{\Gamma \vdash B}{\Gamma \vdash A \vee B}\;(\vee I_2) \qquad \frac{\Gamma \vdash A \vee B \quad \Gamma, A \vdash C \quad \Gamma, B \vdash C}{\Gamma \vdash C}\;(\vee E)"),
        T("To prove A or B, prove one of them and say which. To use A or B, show that C follows in both cases. Finally, false has no introduction rule, and its elimination rule says that from false anything follows."),
        M(r"\frac{\Gamma \vdash \bot}{\Gamma \vdash C}\;(\bot E) \qquad\qquad \frac{}{\Gamma, A \vdash A}\;(\text{hyp})"),
        T("Example: prove A and B implies B and A. Assume p of type A and B. By the two elimination rules we get B and A. By and introduction we get B and A. Discharging the assumption gives the implication."),
        T("The BHK reading, from Brouwer, Heyting and Kolmogorov, says what a proof is. A proof of A and B is a pair of a proof of A and a proof of B. A proof of A or B is a proof of A or a proof of B, together with a tag saying which. A proof of A implies B is a method that transforms any proof of A into a proof of B. There is no proof of false.",
          "Read like this, a proof is a thing you can build and inspect. In chapter 3 we make that literal with lambda calculus.")],
    "quiz": [
        {"q": "How do you prove A implies B in natural deduction?", "options": ["Prove A and prove B separately", "Assume A and prove B", "Prove not B", "Assume B and prove A"], "answer": 1, "explain": "Implication introduction assumes A, proves B, and discharges the assumption."},
        {"q": "What does the elimination rule for or look like?", "options": ["Take the first component", "Proof by cases: show C follows from A and from B", "Assume false", "Apply modus ponens"], "answer": 1, "explain": "To use A or B you must handle both cases."},
        {"q": "In the BHK interpretation, a proof of A and B is...", "options": ["A choice of A or B", "A pair of a proof of A and a proof of B", "A function", "Nothing"], "answer": 1, "explain": "And corresponds to a pair."},
        {"q": "How is not A defined here?", "options": ["A and false", "A implies false", "false implies A", "A or false"], "answer": 1, "explain": "Negation is the implication from A to false."}],
    "cards": [
        {"q": "Rule name for modus ponens?", "a": "Implication elimination (arrow elimination)."},
        {"q": "What does discharging an assumption mean?", "a": "The assumption is used inside an implication proof and then removed from the context."},
        {"q": "Ex falso quodlibet?", "a": "From false, anything follows."},
        {"q": "BHK for or?", "a": "A proof of A or a proof of B, tagged with which one."}],
    "practice": [
        {"type": "match", "title": "Rules and what they do", "intro": "Match each rule to its job.", "pairs": [["Implication introduction", "Assume the premise, prove the conclusion"], ["Implication elimination", "Modus ponens"], ["And introduction", "Prove both parts"], ["Or elimination", "Proof by cases"], ["Ex falso", "From false conclude anything"]]},
        {"type": "order", "title": "Prove A and B implies B and A", "intro": "Put the proof steps in order.", "items": ["Assume p proves A and B", "Take the second part of p, which proves B", "Take the first part of p, which proves A", "Combine them with and introduction to get B and A", "Discharge p to conclude A and B implies B and A"]},
        {"type": "fill", "title": "BHK in words", "text": "A proof of A and B is a {{pair}}. A proof of A implies B is a {{function|method}}. A proof of A or B is a tagged proof of one side, either {{left|inl}} or {{right|inr}}. There is no proof of {{false}}."}]
})

# ------------------------------------------------------------ 3
CH.append({
    "title": "The simply typed lambda calculus",
    "maps": [{"title": "Simply typed lambda calculus", "links": [
        "Term | is | Variable",
        "Term | is | Abstraction",
        "Term | is | Application",
        "Abstraction | has type | Function type",
        "Application | removes | Function type",
        "Typing rules | assign | Types to terms",
        "Beta reduction | computes | Application",
        "Normal form | is | Result",
        "Typing rules [ch4] | match | Natural deduction [ch2]"]}],
    "summary": [
        "The lambda calculus is the smallest programming language: variables, functions written with lambda, and application. The simply typed version gives every term a type built from base types and function arrows.",
        "Three typing rules do everything: a variable has the type its context gives it, a lambda abstraction has a function type, and applying a function of type A to B to an argument of type A gives type B. Computation is beta reduction, which substitutes the argument into the body.",
        "Well-typed terms in this calculus always finish computing. That strong normalization property is the computational reflection of logical consistency, which we use in chapter 5."],
    "glossary": [
        {"term": "Lambda abstraction", "def": "An anonymous function written lambda x. M, where x is the parameter and M the body."},
        {"term": "Application", "def": "Calling a function on an argument, written M N."},
        {"term": "Type context", "def": "A list of variables with their types, written Gamma."},
        {"term": "Function type", "def": "The type A to B of functions that take an A and return a B."},
        {"term": "Beta reduction", "def": "The computation step that replaces a parameter with the argument inside the body."},
        {"term": "Substitution", "def": "Replacing a variable by a term, taking care not to capture other variables."},
        {"term": "Normal form", "def": "A term with no beta redex left, so no further computation is possible."},
        {"term": "Strong normalization", "def": "Every reduction sequence from a well-typed term ends in a normal form."}],
    "keyPoints": [
        "Terms: variables, lambda abstractions, applications.",
        "Types: base types and A to B, where the arrow is right associative.",
        "Typing judgment: Gamma proves M has type A.",
        "Beta: applying lambda x. M to N reduces to M with x replaced by N.",
        "Well-typed terms cannot loop; the untyped lambda calculus can.",
        "The identity has type A to A. The constant function K has type A to B to A."],
    "lesson": [
        T("Here is the whole syntax. A term M is a variable, or a lambda abstraction with a type annotation on the parameter, or an application. A type is a base type or a function type."),
        M(r"M, N \;::=\; x \;\mid\; \lambda x{:}A.\, M \;\mid\; M\, N \qquad\qquad A, B \;::=\; b \;\mid\; A \to B"),
        T("The arrow associates to the right, so A to B to C means A to the function type B to C. Application associates to the left, so f a b means the application of f a to b."),
        M(r"\frac{x{:}A \in \Gamma}{\Gamma \vdash x : A}\;(\text{var}) \qquad \frac{\Gamma, x{:}A \vdash M : B}{\Gamma \vdash \lambda x{:}A.\, M : A \to B}\;(\text{abs}) \qquad \frac{\Gamma \vdash M : A \to B \quad \Gamma \vdash N : A}{\Gamma \vdash M\, N : B}\;(\text{app})"),
        T("Read these as logic and you have the rules of implication from chapter 2: the variable rule is hypothesis, abstraction is implication introduction, and application is implication elimination. That is the Curry-Howard correspondence for the arrow fragment, and the next chapter spells it out."),
        T("Two examples of typing. The identity function takes any x of type A and returns it. The function K takes x and then y and returns x."),
        M(r"\vdash \lambda x{:}A.\, x \;:\; A \to A \qquad\qquad \vdash \lambda x{:}A.\, \lambda y{:}B.\, x \;:\; A \to B \to A"),
        T("Computation is beta reduction. Applying a lambda abstraction to an argument replaces the parameter by the argument."),
        M(r"(\lambda x{:}A.\, M)\, N \;\to_\beta\; M[N/x]"),
        T("Substitution has one subtlety. If the argument mentions a variable with the same name as a bound variable in the body, the bound variable must be renamed first, otherwise it captures the wrong thing. This is called capture-avoiding substitution, and implementations usually rename bound variables or use de Bruijn indices.",
          "Eta conversion is the other common equation: lambda x. f x equals f when x is not free in f. Together, beta and eta make function equality extensional."),
        C("""# The same idea in Python
identity = lambda x: x
K = lambda x: lambda y: x

assert identity(5) == 5
assert K("a")("b") == "a"

# Types in Python hints (checked by mypy, not at run time)
from typing import Callable, TypeVar
A = TypeVar("A"); B = TypeVar("B")
def K_typed(x: A) -> Callable[[B], A]:
    return lambda y: x""", "python"),
        T("Why simply typed? Because the types are just function arrows and base types, nothing else. There is no polymorphism and no dependent types yet. That keeps the calculus small enough to match intuitionistic implication exactly. We will add pairs, sums, unit and empty types in the next chapter."),
        T("A striking fact, proved by Tait with logical relations and by others since: every well-typed term in this calculus reaches a normal form. The Y combinator and the self-applying term omega cannot be typed, so non-termination is excluded. We use this in chapter 5 to show that logic is consistent.")],
    "quiz": [
        {"q": "What is the type of lambda x:A. x?", "options": ["A", "A to A", "A to B", "B to A"], "answer": 1, "explain": "The identity takes an A and returns an A."},
        {"q": "What is the typing rule for application?", "options": ["If M : A to B and N : A then M N : B", "If M : A and N : B then M N : A to B", "If M : A then M N : A", "Application has no rule"], "answer": 0, "explain": "Applying a function to an argument of the right type gives the result type."},
        {"q": "What does beta reduction do?", "options": ["Renames a variable", "Substitutes the argument into the body", "Deletes a term", "Changes a type"], "answer": 1, "explain": "(lambda x. M) N becomes M with N substituted for x."},
        {"q": "Which property do all well-typed STLC terms have?", "options": ["They contain pairs", "They always reach a normal form", "They are polymorphic", "They use side effects"], "answer": 1, "explain": "Strong normalization: no infinite reduction from a well-typed term."}],
    "cards": [
        {"q": "Typing rule for lambda?", "a": "If Gamma, x : A proves M : B then Gamma proves lambda x:A. M : A to B."},
        {"q": "Beta rule?", "a": "(lambda x. M) N reduces to M[N/x]."},
        {"q": "Type of K?", "a": "A to B to A."},
        {"q": "Which rule matches hypothesis in logic?", "a": "The variable rule."}],
    "practice": [
        {"type": "code", "title": "A type checker", "intro": "Write typeOf(term, ctx) for the simply typed lambda calculus. A term is [\"var\", x], [\"lam\", x, T, body] or [\"app\", f, a]. A type is a string such as \"A\" or [\"->\", T1, T2]. ctx maps variable names to types. Return the type, or the string \"error\" if the term is not typable.", "fn": "typeOf",
         "starter": "function typeOf(term, ctx) {\n  // your code\n}",
         "tests": [{"args": [["lam", "x", "A", ["var", "x"]], {}], "expect": ["->", "A", "A"]}, {"args": [["lam", "x", "A", ["lam", "y", "B", ["var", "x"]]], {}], "expect": ["->", "A", ["->", "B", "A"]]}, {"args": [["app", ["lam", "x", "A", ["var", "x"]], ["var", "a"]], {"a": "A"}], "expect": "A"}, {"args": [["app", ["var", "a"], ["var", "a"]], {"a": "A"}], "expect": "error"}, {"args": [["var", "z"], {}], "expect": "error"}, {"args": [["app", ["lam", "x", "A", ["var", "x"]], ["var", "b"]], {"b": "B"}], "expect": "error"}],
         "hint": "var: look in ctx. lam: extend ctx with x:T and return [\"->\", T, typeOf(body)]. app: the function type must be [\"->\", A, B] and the argument must have type A (compare with JSON.stringify).",
         "solution": "function typeOf(term, ctx) {\n  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);\n  if (term[0] === 'var') return term[1] in ctx ? ctx[term[1]] : 'error';\n  if (term[0] === 'lam') {\n    const body = typeOf(term[3], Object.assign({}, ctx, { [term[1]]: term[2] }));\n    return body === 'error' ? 'error' : ['->', term[2], body];\n  }\n  const f = typeOf(term[1], ctx), a = typeOf(term[2], ctx);\n  if (f === 'error' || a === 'error') return 'error';\n  return Array.isArray(f) && f[0] === '->' && same(f[1], a) ? f[2] : 'error';\n}"},
        {"type": "match", "title": "Rules as logic", "intro": "Match each typing rule to the logical rule it mirrors.", "pairs": [["Variable rule", "Hypothesis"], ["Lambda abstraction", "Implication introduction"], ["Application", "Implication elimination (modus ponens)"], ["Beta reduction", "Removing a detour in a proof"]]},
        {"type": "fill", "title": "Parse the arrows", "text": "The type A to B to C means A to (B to C), so the arrow is {{right|right-associative|right associative}}. The term f a b means (f a) b, so application is {{left|left-associative|left associative}}. The identity function has type A {{to|->}} A."}]
})

# ------------------------------------------------------------ 4
CH.append({
    "title": "Propositions as types",
    "maps": [{"title": "The Curry-Howard dictionary", "links": [
        "Proposition | is | Type",
        "Proof | is | Program",
        "Implication | is | Function type",
        "Conjunction | is | Pair type",
        "Disjunction | is | Sum type",
        "True | is | Unit type",
        "False | is | Empty type",
        "Implication introduction | is | Lambda abstraction",
        "Implication elimination | is | Application",
        "Provable | means | Inhabited",
        "Proof assistants [ch11] | check | Types"]}],
    "summary": [
        "Extend the lambda calculus with pairs, tagged sums, a unit type and an empty type, and every rule of natural deduction has a matching program construct. Implication becomes the function type, and becomes the pair type, or becomes the sum type, true becomes unit and false becomes the empty type.",
        "A proposition is provable exactly when its type has a closed program, we say the type is inhabited. Writing the program is writing the proof, and type checking is proof checking.",
        "Currying is the first famous example: the proposition A and B implies C is equivalent to A implies B implies C, and the two functions curry and uncurry are the proofs of each direction."],
    "glossary": [
        {"term": "Inhabited type", "def": "A type that has at least one program (closed term). Inhabited means provable."},
        {"term": "Product type", "def": "The type A x B of pairs, matching logical and."},
        {"term": "Sum type", "def": "The type A + B of values tagged left or right, matching logical or."},
        {"term": "Unit type", "def": "The type with exactly one value, matching true."},
        {"term": "Empty type", "def": "The type with no values, matching false. Also called Void."},
        {"term": "Currying", "def": "Turning a function of a pair into a function that takes its arguments one at a time."},
        {"term": "Case analysis", "def": "Program construct that handles each side of a sum, matching or elimination."},
        {"term": "Absurd", "def": "The function from the empty type to any type, matching ex falso."}],
    "keyPoints": [
        "A and B is the pair type; its introduction is making a pair and its eliminations are fst and snd.",
        "A or B is the sum type; its introductions are inl and inr, and its elimination is case.",
        "A implies B is the function type; introduction is lambda, elimination is application.",
        "True is the unit type with one value. False is the empty type with none.",
        "Not A is the function type A to empty. A proof of a negation is a program that turns any A into a contradiction.",
        "Provable means inhabited. Type checking is proof checking."],
    "lesson": [
        T("Here is the full dictionary. Each row is a logical rule and the programming construct that implements it."),
        C("""Logic rule                    Program                      Typing
------------------------------------------------------------------------------
hypothesis                    variable x                   x : A
implies introduction          lambda x. M                  A -> B
implies elimination           application M N              B
and introduction              pair (M, N)                  A x B
and elimination               fst P, snd P                 A, B
or introduction               inl M, inr N                 A + B
or elimination                case S of inl x.. | inr y..  C
true introduction             unit value ()                1
false elimination             absurd M                     C   (from 0)""", "text"),
        T("In Haskell the correspondence is visible in the standard library. The tuple type is and, Either is or, the function arrow is implies and Void is false."),
        C("""swap :: (a, b) -> (b, a)
swap (x, y) = (y, x)               -- proves  A and B  implies  B and A

orSwap :: Either a b -> Either b a
orSwap (Left x)  = Right x
orSwap (Right y) = Left y          -- proves  A or B  implies  B or A

curryProof :: ((a, b) -> c) -> (a -> b -> c)
curryProof f = \\x y -> f (x, y)    -- A and B implies C  gives  A implies B implies C

absurd' :: Void -> a
absurd' v = case v of {}           -- false implies anything""", "haskell"),
        T("The same proofs in Python type hints. A static checker such as mypy verifies them, which is a small version of proof checking."),
        C("""from typing import Callable, TypeVar
A = TypeVar("A"); B = TypeVar("B"); C = TypeVar("C")

def swap(p: tuple[A, B]) -> tuple[B, A]:
    return (p[1], p[0])

def curry(f: Callable[[tuple[A, B]], C]) -> Callable[[A], Callable[[B], C]]:
    return lambda a: lambda b: f((a, b))

def uncurry(f: Callable[[A], Callable[[B], C]]) -> Callable[[tuple[A, B]], C]:
    return lambda p: f(p[0])(p[1])""", "python"),
        T("Now negation. Not A means A implies false. A proof of not A is a program that, given any A, produces a value of the empty type. Since no such value exists, the program can only be written if A has no values either. The program that turns a value into a negation of a negation is easy: given a, and given k a proof of not A, apply k to a."),
        M(r"\lambda a.\, \lambda k.\, k\, a \;:\; A \to \neg\neg A"),
        T("Equally important are the types that have no program. The type A to B with unrelated A and B cannot be inhabited, which matches the fact that A implies B is not provable for arbitrary propositions. And the types that correspond to excluded middle or double negation elimination have no program in this calculus; chapter 6 explains why.",
          "This is the gain of proofs as programs. Proving a theorem means finding a program; refuting provability means a type that no program can have; and checking a proof is type checking.")],
    "quiz": [
        {"q": "Which type corresponds to A or B?", "options": ["A x B", "A + B (a sum type)", "A -> B", "The unit type"], "answer": 1, "explain": "Or corresponds to a tagged sum such as Either."},
        {"q": "A proposition is provable exactly when...", "options": ["Its type has a program", "Its type has a name", "Its type is a base type", "Its type has a function"], "answer": 0, "explain": "Provable means inhabited by a closed program."},
        {"q": "What is the type of the proof of A implies not not A?", "options": ["A to ((A to 0) to 0)", "A + A", "(A to 0) to A", "0 to A"], "answer": 0, "explain": "Not not A is (A to 0) to 0, and lambda a. lambda k. k a has that type."},
        {"q": "What does the Haskell function absurd correspond to?", "options": ["Modus ponens", "Ex falso: from false anything follows", "Or introduction", "Currying"], "answer": 1, "explain": "Void to a is the proof of false implies A."}],
    "cards": [
        {"q": "And as a type?", "a": "The pair (product) type A x B."},
        {"q": "Or as a type?", "a": "The sum type A + B (Either)."},
        {"q": "False as a type?", "a": "The empty type, Void."},
        {"q": "Not A as a type?", "a": "A -> Void (A to the empty type)."}],
    "practice": [
        {"type": "code", "title": "Swap a pair", "intro": "Write swapPair(p): given [a, b] return [b, a]. This is the proof of A and B implies B and A.", "fn": "swapPair",
         "starter": "function swapPair(p) {\n  // your code\n}",
         "tests": [{"args": [[1, 2]], "expect": [2, 1]}, {"args": [["x", "y"]], "expect": ["y", "x"]}, {"args": [[[1], {"k": 2}]], "expect": [{"k": 2}, [1]]}],
         "hint": "Return a new array with the components in the other order.",
         "solution": "function swapPair(p) {\n  return [p[1], p[0]];\n}"},
        {"type": "code", "title": "Distribute and over or", "intro": "Prove A and (B or C) implies (A and B) or (A and C). A pair is [a, s], where s is {\"tag\": \"inl\" or \"inr\", \"v\": value}. Return {\"tag\": same tag, \"v\": [a, value]}.", "fn": "distribute",
         "starter": "function distribute(p) {\n  // your code\n}",
         "tests": [{"args": [[1, {"tag": "inl", "v": 2}]], "expect": {"tag": "inl", "v": [1, 2]}}, {"args": [["a", {"tag": "inr", "v": "c"}]], "expect": {"tag": "inr", "v": ["a", "c"]}}],
         "hint": "Case analysis on the tag: keep the tag, pair the first component with the value.",
         "solution": "function distribute(p) {\n  const a = p[0], s = p[1];\n  return { tag: s.tag, v: [a, s.v] };\n}"},
        {"type": "match", "title": "Logic to types", "intro": "Match each proposition to its type.", "pairs": [["A and B", "Pair type A x B"], ["A or B", "Sum type A + B"], ["A implies B", "Function type A to B"], ["True", "Unit type"], ["False", "Empty type"], ["Not A", "A to the empty type"]]}]
})
