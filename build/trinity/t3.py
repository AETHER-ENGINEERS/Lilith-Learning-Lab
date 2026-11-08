"""Curry-Howard-Lambek course, chapters 9-12."""
from tlib import T, C, M

CH = []

# ------------------------------------------------------------ 9
CH.append({
    "title": "The Lambek correspondence",
    "maps": [{"title": "Lambek's dictionary", "links": [
        "Type | is interpreted as | Object",
        "Context | is interpreted as | Product of objects",
        "Term | is interpreted as | Morphism",
        "Lambda abstraction | is interpreted as | Currying",
        "Application | is interpreted as | Evaluation",
        "Pair | is interpreted as | Pairing arrow",
        "Beta and eta | match | Universal property laws",
        "Cartesian closed category [ch8] | is | Model of the calculus",
        "Syntax [ch3] | builds | Free cartesian closed category",
        "Heyting algebra | is | Posetal model [ch6]"]}],
    "summary": [
        "The Lambek correspondence reads the typed lambda calculus inside any cartesian closed category. Each type is an object, each context is a product of objects, and each term of type B in context Gamma is an arrow from the context to B.",
        "Lambda abstraction becomes currying, application becomes the evaluation arrow, and pairs become the pairing arrow. The beta and eta equations of the calculus become exactly the universal property laws of products and exponentials.",
        "Going the other way, the syntax of the calculus itself forms a cartesian closed category, so the lambda calculus is the internal language of such categories. Proofs, programs and arrows are three descriptions of the same structure, which is the slogan computational trinitarianism."],
    "glossary": [
        {"term": "Interpretation", "def": "A map from syntax (types and terms) to a category (objects and arrows)."},
        {"term": "Internal language", "def": "The typed calculus that you can use to reason about a category as if its objects were types."},
        {"term": "Soundness", "def": "If two terms are equal by beta and eta, their interpretations are the same arrow."},
        {"term": "Syntactic category", "def": "The category whose objects are types and whose arrows are terms up to equality."},
        {"term": "Denotational semantics", "def": "Giving programs meaning as mathematical objects, such as functions between sets."},
        {"term": "Heyting algebra", "def": "A bicartesian closed preorder: the posetal case of the correspondence."},
        {"term": "Cartesian closed category", "def": "A category with a terminal object, products and exponentials."}],
    "keyPoints": [
        "Types are objects. A context x1:A1, ..., xn:An is the product A1 x ... x An.",
        "A term Gamma proves M : B is an arrow from the context to B.",
        "Lambda is currying, application is evaluation, pairs are pairing.",
        "Beta and eta equal the universal-property equations.",
        "Taking sets and functions as the category gives the standard set-theoretic semantics.",
        "Posetal case: propositions as objects, entailment as arrows, a Heyting algebra."],
    "lesson": [
        T("Fix a cartesian closed category. We interpret every type A as an object, written with double brackets. Base types are chosen objects, the arrow type is the exponential, and the pair type is the product."),
        M(r"[\![A \to B]\!] = [\![B]\!]^{[\![A]\!]} \qquad\qquad [\![A \times B]\!] = [\![A]\!] \times [\![B]\!] \qquad\qquad [\![1]\!] = 1"),
        T("A typing judgment says that in a context Gamma the term M has type B. The context itself becomes the product of its types. The judgment is interpreted as an arrow from that product to the object for B."),
        M(r"\Gamma \vdash M : B ;\leadsto; [\![M]\!] : [\![\Gamma]\!] \to [\![B]\!]"),
        T("Every term constructor then has a categorical meaning. A variable is a projection out of the context product. A lambda abstraction is currying: if the body is an arrow from the context times A to B, the abstraction is the curried arrow from the context to the exponential. Application is evaluation applied to the pair of the function and the argument."),
        M(r"[\![\lambda x.\, M]\!] = \Lambda [\![M]\!] \qquad\qquad [\![M\, N]\!] = \mathrm{ev} \circ \langle [\![M]\!], [\![N]\!] \rangle \qquad\qquad [\![(M, N)]\!] = \langle [\![M]\!], [\![N]\!] \rangle"),
        T("The equations of the calculus are not extra data; they are the universal properties again. Beta reduction is the statement that evaluating a curried arrow recovers the original arrow. Eta, which says lambda x. f x equals f, is the uniqueness half of the exponential property. Likewise fst of a pair is the first component, and a pair of the two projections of p is p."),
        M(r"\mathrm{ev} \circ (\Lambda f \times \mathrm{id}_A) = f \qquad\qquad \Lambda(\mathrm{ev} \circ (g \times \mathrm{id}_A)) = g"),
        T("This gives soundness: if two terms are equal by beta and eta, they denote the same arrow in every cartesian closed category. And there is a converse of sorts. The terms of the calculus, taken up to equality, form a cartesian closed category themselves, which is free on the chosen base types. The calculus is therefore the internal language of cartesian closed categories. Lambek and Scott made this precise, and it is what lets you reason about a category by writing programs in it."),
        T("Take the category of sets and functions. Interpret each base type as a set, and the interpretation becomes the usual set-theoretic semantics of the calculus: functions are functions, pairs are pairs. Take instead a Heyting algebra viewed as a category and the same recipe gives the semantics of intuitionistic propositional logic, where there is at most one arrow between objects, and so proofs of the same statement are all equal."),
        T("Put the three columns together. Logic: proposition, proof, implication, conjunction, true, false. Programming: type, program, function type, pair type, unit type, empty type. Category theory: object, morphism, exponential, product, terminal object, initial object. This table is the heart of the course, and the Trinity Explorer in the practice section lets you click through it row by row.")],
    "quiz": [
        {"q": "What does lambda abstraction become in a cartesian closed category?", "options": ["Evaluation", "Currying", "Projection", "A product"], "answer": 1, "explain": "The body is an arrow out of context times A, and the abstraction is its curried form."},
        {"q": "What does application become?", "options": ["Currying", "The evaluation arrow", "A coproduct", "The terminal arrow"], "answer": 1, "explain": "Application is evaluation composed with the pairing of function and argument."},
        {"q": "What is a context x:A, y:B interpreted as?", "options": ["A + B", "A x B", "B to the A", "The terminal object"], "answer": 1, "explain": "A context is interpreted as the product of its types."},
        {"q": "What does it mean to call the lambda calculus the internal language of a CCC?", "options": ["Programs can be compiled to machine code", "You can reason about the category by writing typed programs in it", "Types are hidden", "It has only products"], "answer": 1, "explain": "Terms are arrows, so equations between terms are equations between arrows."}],
    "cards": [
        {"q": "Interpretation of an arrow type?", "a": "The exponential object."},
        {"q": "Interpretation of a context?", "a": "The product of its types."},
        {"q": "Beta and eta correspond to?", "a": "The universal property equations of exponentials and products."},
        {"q": "Who made the correspondence precise?", "a": "Lambek (and Scott)."}],
    "practice": [
        {"type": "code", "title": "Count the denotation", "intro": "Interpret types in finite sets. A type is a number n (a base type with n elements), \"unit\" (1 element), \"void\" (0), [\"x\", A, B] (product), [\"+\", A, B] (sum) or [\"->\", A, B] (function). Write cardinality(type): the number of elements of the set it denotes.", "fn": "cardinality",
         "starter": "function cardinality(t) {\n  // your code\n}",
         "tests": [{"args": [3], "expect": 3}, {"args": ["unit"], "expect": 1}, {"args": ["void"], "expect": 0}, {"args": [["x", 2, 3]], "expect": 6}, {"args": [["+", "unit", ["x", 2, 3]]], "expect": 7}, {"args": [["->", 2, 3]], "expect": 9}, {"args": [["->", ["x", 2, 2], 2]], "expect": 16}, {"args": [["->", ["+", "unit", "unit"], ["->", "unit", 3]]], "expect": 9}, {"args": [["->", "void", 5]], "expect": 1}],
         "hint": "Recurse. A function type from A to B has cardinality(B) to the power cardinality(A).",
         "solution": "function cardinality(t) {\n  if (typeof t === 'number') return t;\n  if (t === 'unit') return 1;\n  if (t === 'void') return 0;\n  const a = cardinality(t[1]), b = cardinality(t[2]);\n  if (t[0] === 'x') return a * b;\n  if (t[0] === '+') return a + b;\n  return Math.pow(b, a);\n}"},
        {"type": "match", "title": "The dictionary", "intro": "Match each programming construct to its categorical meaning.", "pairs": [["Lambda abstraction", "Currying"], ["Application", "Evaluation arrow"], ["Pair", "Pairing arrow"], ["Variable", "Projection from the context"], ["Context", "Product of the types"]]},
        {"type": "webxdc", "title": "Trinity Explorer", "intro": "Tap rows to see one idea in logic, in programs and in category theory. Explore six rows to finish.", "height": 520, "html": "__TRINITY__"}]
})

# ------------------------------------------------------------ 10
CH.append({
    "title": "Dependent types and quantifiers",
    "maps": [{"title": "Dependent types", "links": [
        "Dependent function type | is | Pi type",
        "Dependent pair type | is | Sigma type",
        "Pi type | matches | Universal quantifier",
        "Sigma type | matches | Existential quantifier",
        "Identity type | matches | Equality",
        "Induction | is | Recursion",
        "Vector | has type | Indexed by length",
        "Martin-Lof type theory | is | Foundation",
        "Lean [ch11] | implements | Dependent types"]}],
    "summary": [
        "When a type can depend on a value, propositions can talk about values too. A dependent function type, or Pi type, matches the universal quantifier. A dependent pair type, or Sigma type, matches the existential quantifier. Equality becomes an identity type whose proofs are built from reflexivity.",
        "Proof by induction is the same thing as writing a recursive function. A vector type that records its length in the type makes some bugs impossible, such as taking the head of an empty list.",
        "This is Martin-Lof type theory and the logic of Lean, Rocq and Agda. The correspondence is the same, one dimension up: propositions about values are types that depend on values."],
    "glossary": [
        {"term": "Dependent type", "def": "A type that depends on a value, such as a vector of length n."},
        {"term": "Pi type", "def": "The type of functions whose result type depends on the argument. Matches for all."},
        {"term": "Sigma type", "def": "The type of pairs whose second component's type depends on the first. Matches there exists."},
        {"term": "Identity type", "def": "The type a equals b of proofs that a and b are equal. Reflexivity proves a equals a."},
        {"term": "Induction principle", "def": "The rule for proving a statement about every natural number from a base case and a step. As a program it is recursion."},
        {"term": "Witness", "def": "The value that proves an existence statement."},
        {"term": "Universe", "def": "A type whose elements are types. Needed to avoid paradoxes."},
        {"term": "Indexed family", "def": "A family of types parameterized by values, such as Vec A n."}],
    "keyPoints": [
        "For all x in A, P(x) is the Pi type: a function giving a proof of P(x) for each x.",
        "There exists x in A with P(x) is the Sigma type: a witness plus a proof about it.",
        "Equality is an inductive type whose constructor is reflexivity.",
        "Induction on the natural numbers is a recursive function.",
        "Indexing a vector by its length lets the type checker reject head of the empty vector.",
        "Dependent types are what make programs and proofs live in one language."],
    "lesson": [
        T("So far propositions were about abstract atoms. To prove statements about numbers, lists and programs, we want types to mention values. A dependent function type is a function whose result type depends on its argument. A dependent pair is a pair whose second part has a type depending on the first."),
        M(r"\forall x{:}A.\, P(x) \;\;\leftrightarrow\;\; \Pi x{:}A.\, P(x) \qquad\qquad \exists x{:}A.\, P(x) \;\;\leftrightarrow\;\; \Sigma x{:}A.\, P(x)"),
        T("When P does not mention x, the Pi type is the ordinary function type and the Sigma type is the ordinary pair type. So the quantifiers generalize the arrow and the product, just as the arrow and the product were the logical implication and conjunction."),
        T("A proof of the existence of a number n with n plus n equal to four is a witness together with a proof. In Lean the witness is two and the proof is reflexivity, because two plus two computes to four."),
        C("""theorem exists_two : ∃ n : Nat, n + n = 4 := ⟨2, rfl⟩

theorem all_succ_pos : ∀ n : Nat, 0 < n + 1 := fun n => Nat.succ_pos n

#check (⟨2, rfl⟩ : ∃ n : Nat, n + n = 4)   -- Exists.intro 2 rfl : ∃ n, n + n = 4""", "lean"),
        T("Equality is a type too. The equality a equals b has one constructor, reflexivity, which proves a equals a. Because Lean computes, if two sides reduce to the same value then reflexivity proves them equal. That is why n plus zero equals n is proved by rfl, while zero plus n equals n needs induction: addition recurses on its second argument."),
        C("""theorem add_zero' (n : Nat) : n + 0 = n := rfl          -- computes: n + 0 reduces to n

theorem zero_add' (n : Nat) : 0 + n = n := by            -- needs induction
  induction n with
  | zero => rfl
  | succ k ih => exact congrArg Nat.succ ih""", "lean"),
        T("Look at what induction is. To prove a statement for all n you give a proof for zero and a function that turns a proof for k into a proof for k plus one. That is exactly a recursive function whose result type depends on its argument. The induction principle is the dependent recursor."),
        T("Vectors show the practical payoff. A vector type carries its length. Append adds lengths in the type, and taking the head only works on a vector whose length is a successor, so the empty case is ruled out by the type checker rather than by a runtime error."),
        C("""inductive Vec (α : Type) : Nat → Type where
  | nil : Vec α 0
  | cons : α → Vec α n → Vec α (n + 1)

def Vec.append : Vec α m → Vec α n → Vec α (n + m)
  | .nil, ys => ys
  | .cons x xs, ys => .cons x (append xs ys)

def Vec.head : Vec α (n + 1) → α
  | .cons x _ => x            -- no case for nil: it cannot occur

#check @Vec.append   -- {α : Type} → {m n : Nat} → Vec α m → Vec α n → Vec α (n + m)""", "lean"),
        T("Where does this come from? Per Martin-Lof's intuitionistic type theory of the 1970s and 80s, which is the foundation behind Agda, Rocq and Lean. A dependent type theory unifies the logic and the programming language in a single system, so a verified program is just a program whose type is a precise specification."),
        T("A caution. The step from simple to dependent types raises the stakes of totality. Every function must terminate, because a non-terminating proof would prove anything. Proof assistants therefore check termination for recursive definitions, and that is why recursion in these languages has structural rules.")],
    "quiz": [
        {"q": "Which type corresponds to the existential quantifier?", "options": ["Pi type", "Sigma type", "Function type", "Unit type"], "answer": 1, "explain": "A dependent pair of a witness and a proof."},
        {"q": "What is a proof of there exists n with n + n = 4?", "options": ["A truth table", "A witness such as 2 and a proof that 2 + 2 = 4", "A function", "Nothing is needed"], "answer": 1, "explain": "A Sigma value: the witness and a proof about it."},
        {"q": "What is proof by induction in programming terms?", "options": ["Case analysis", "A recursive function whose result type depends on its argument", "A pair", "A wrapper"], "answer": 1, "explain": "The induction principle is the dependent recursor."},
        {"q": "Why can Vec.head omit the nil case?", "options": ["It is ignored at run time", "Its argument type is Vec A (n + 1), which is never empty", "nil cannot be written", "It is a bug"], "answer": 1, "explain": "The type excludes the empty vector."}],
    "cards": [
        {"q": "For all as a type?", "a": "The Pi type (dependent function)."},
        {"q": "There exists as a type?", "a": "The Sigma type (dependent pair)."},
        {"q": "Constructor of equality?", "a": "Reflexivity, refl (rfl in Lean)."},
        {"q": "Why must proof assistant functions terminate?", "a": "A non-terminating function could prove anything, including false."}],
    "practice": [
        {"type": "match", "title": "Quantifiers and types", "intro": "Match each logical idea to its type-theory form.", "pairs": [["For all x in A, P(x)", "Pi type"], ["There exists x in A with P(x)", "Sigma type"], ["a equals b", "Identity type"], ["Proof by induction", "Recursion"], ["A vector of length n", "Indexed family"]]},
        {"type": "fill", "title": "Witnesses", "text": "A proof of an existence statement is a {{witness}} together with a proof about it, which is a {{Sigma|dependent pair}} value. A proof of a universal statement is a {{function|Pi|dependent function}} from every x to a proof for x. Equality is proved by {{reflexivity|rfl|refl}}."},
        {"type": "write", "title": "Spot the benefit", "prompt": "In one or two sentences, explain how a vector type that includes its length helps prevent a bug.", "checks": [{"re": "length|size", "msg": "mentions length"}, {"re": "head|empty|index|bounds|error|bug", "msg": "mentions the bug it prevents"}], "solution": "The type records the length, so the checker can reject taking the head of an empty vector at compile time."}]
})

# ------------------------------------------------------------ 11
CH.append({
    "title": "Proof assistants in practice",
    "maps": [{"title": "Using a proof assistant", "links": [
        "Proof assistant | checks | Types",
        "Theorem | is | Type",
        "Proof | is | Term",
        "Tactic | builds | Term",
        "Kernel | checks | Term",
        "Lean | is | Proof assistant",
        "Rocq | is | Proof assistant",
        "Agda | is | Proof assistant",
        "Classical axioms [ch6] | are marked by | Axiom check",
        "Verified software | is | Specification as type"]}],
    "summary": [
        "A proof assistant is a programming language whose type checker is a proof checker. You state a theorem as a type, build a term of that type, and the kernel verifies it. Lean, Rocq and Agda are well-known examples.",
        "You can write proofs directly as terms, as in earlier chapters, or use tactics, small commands that build the term step by step. Either way the kernel checks the final term, so a tactic bug cannot sneak in a wrong proof.",
        "Proof assistants have been used for verified compilers, operating system kernels and large libraries of mathematics. You can ask which axioms a proof depends on, which shows whether it used classical logic."],
    "glossary": [
        {"term": "Proof assistant", "def": "A program for writing and checking formal proofs, built on a type theory."},
        {"term": "Kernel", "def": "The small trusted core that type checks every proof term."},
        {"term": "Tactic", "def": "A command that constructs part of a proof term, such as induction or rewrite."},
        {"term": "Term-mode proof", "def": "A proof written directly as a lambda term."},
        {"term": "Prop", "def": "The Lean universe of propositions, whose proofs are irrelevant to computation."},
        {"term": "Axiom", "def": "A statement assumed without proof. Classical logic enters through axioms."},
        {"term": "Formal verification", "def": "Proving that a program meets a precise specification with a proof the machine checks."}],
    "keyPoints": [
        "A theorem is a type, a proof is a term of that type, the kernel is the checker.",
        "Term mode is the Curry-Howard correspondence written directly.",
        "Tactics build terms; only the kernel is trusted.",
        "#check shows a type, #eval runs a program, #print axioms lists assumptions.",
        "Lean, Rocq and Agda are constructive by default.",
        "A proof that depends on classical axioms is visible through #print axioms."],
    "lesson": [
        T("Here is the Curry-Howard correspondence in a real proof assistant. These proofs are written in Lean 4. Each theorem states a proposition as a type, and each proof is a function."),
        C("""theorem a_imp_a (A : Prop) : A → A := fun a => a

theorem and_swap' (A B : Prop) : A ∧ B → B ∧ A :=
  fun ⟨a, b⟩ => ⟨b, a⟩

theorem or_swap' (A B : Prop) : A ∨ B → B ∨ A :=
  fun h => h.elim (fun a => Or.inr a) (fun b => Or.inl b)

theorem curry' (A B C : Prop) : (A ∧ B → C) → (A → B → C) :=
  fun f a b => f ⟨a, b⟩

theorem dni (A : Prop) : A → ¬¬A := fun a k => k a

theorem distrib (A B C : Prop) : A ∧ (B ∨ C) → (A ∧ B) ∨ (A ∧ C) :=
  fun ⟨a, h⟩ => h.elim (fun b => Or.inl ⟨a, b⟩) (fun c => Or.inr ⟨a, c⟩)""", "lean"),
        T("Compare with chapter 4. The pair is the proof of and, the Or.inl and Or.inr are the injections, elimination is case analysis, and the double negation proof is the lambda that applies the refutation to the value. Nothing is new; only the syntax is Lean's."),
        T("The checker answers queries. The command check shows the type of an expression. The command eval runs a program. Typing a wrong proof gives a type error that reads like a failed type check, because it is one."),
        C("""#check Nat → Nat                         -- Nat → Nat : Type
#check fun (x : Nat) => x + 1            -- fun x => x + 1 : Nat → Nat
#check And.intro                         -- And.intro {a b : Prop} (left : a) (right : b) : a ∧ b
#check Prop                              -- Prop : Type
#eval 2 + 2                              -- 4

example : 2 + 2 = 4 := rfl               -- accepted
example : 2 + 2 = 5 := rfl               -- error: type mismatch""", "lean"),
        T("Tactics let you build proofs interactively. A tactic proof starts with by, and each command transforms the goal. The tactic framework produces a proof term at the end, and the kernel checks it, so you can use powerful automation without trusting it."),
        C("""theorem double_eq (n : Nat) : n + n = 2 * n := by omega

theorem and_comm' (A B : Prop) : A ∧ B → B ∧ A := by
  intro h
  exact ⟨h.2, h.1⟩""", "lean"),
        T("Axioms matter. Lean has a classical axiom, and you can ask which axioms a theorem uses. The swap proof depends on none. A proof of Peirce's law needs classical logic, and the check shows it. This is the constructive-versus-classical distinction of chapter 6, made visible to a tool."),
        C("""#print axioms and_swap'
-- 'and_swap'' does not depend on any axioms

theorem peirce (A B : Prop) : ((A → B) → A) → A :=
  fun f => Classical.byContradiction (fun na => na (f (fun a => absurd a na)))

#print axioms peirce
-- 'peirce' depends on axioms: [propext, Classical.choice, Quot.sound]""", "lean"),
        T("What is this used for? Mathematicians use Lean's Mathlib library to formalize mathematics. Software engineers use proof assistants to verify compilers and operating system kernels, such as the CompCert C compiler in Rocq and the seL4 microkernel in Isabelle. The common idea is the one you have learned: a specification is a type, a verified program is a term of that type.",
          "The Simulated Lean terminal in the practice section lets you try the commands from this chapter. Its outputs were copied from a real Lean run, but it is not a real Lean installation, so install Lean from the official site to go further.")],
    "quiz": [
        {"q": "What does the kernel of a proof assistant do?", "options": ["Suggests tactics", "Type checks every proof term", "Compiles to C", "Stores files"], "answer": 1, "explain": "It is the small trusted core that verifies the final term."},
        {"q": "What is a theorem in a proof assistant?", "options": ["A comment", "A type", "A string", "A tactic"], "answer": 1, "explain": "A proof is a term inhabiting that type."},
        {"q": "What does #print axioms tell you?", "options": ["The file size", "Which axioms a proof relies on", "The running time", "The tactic names"], "answer": 1, "explain": "A classical proof shows axioms such as Classical.choice."},
        {"q": "Why can tactics be used without trusting them?", "options": ["They are always correct", "They only produce terms, and the kernel checks the result", "They are slow", "They only work on small proofs"], "answer": 1, "explain": "A buggy tactic can fail, but cannot produce an invalid accepted proof."}],
    "cards": [
        {"q": "Theorem is to proof as?", "a": "Type is to term."},
        {"q": "Command to see a type in Lean?", "a": "#check"},
        {"q": "Command to see assumptions?", "a": "#print axioms"},
        {"q": "Three proof assistants?", "a": "Lean, Rocq (formerly Coq), Agda."}],
    "practice": [
        {"type": "terminal", "title": "Simulated Lean", "intro": "A scripted Lean shell. Outputs were copied from a real Lean 4 run, but this is not a real Lean installation. Try the chips or type the commands.", "prompt": "lean>",
         "chips": ["#check Nat → Nat", "#check And.intro", "#eval 2 + 2", "theorem and_swap' (A B : Prop) : A ∧ B → B ∧ A := fun ⟨a, b⟩ => ⟨b, a⟩", "#print axioms and_swap'", "example : 2 + 2 = 5 := rfl", "#check Classical.em"],
         "commands": [
             {"re": "^#check Nat (→|->) Nat$", "out": ["Nat → Nat : Type"]},
             {"re": "^#check \\(?fun \\(x : Nat\\) (=>|↦) x \\+ 1\\)?$", "out": ["fun x => x + 1 : Nat → Nat"]},
             {"re": "^#check And\\.intro$", "out": ["And.intro {a b : Prop} (left : a) (right : b) : a ∧ b"]},
             {"re": "^#check @Or\\.elim$", "out": ["@Or.elim : ∀ {a b c : Prop}, a ∨ b → (a → c) → (b → c) → c"]},
             {"re": "^#check Prop$", "out": ["Prop : Type"]},
             {"re": "^#check Type$", "out": ["Type : Type 1"]},
             {"re": "^#check Classical\\.em$", "out": ["Classical.em : ∀ (p : Prop), p ∨ ¬p"]},
             {"re": "^#eval 2 \\+ 2$", "out": ["4"]},
             {"re": "^example : 2 \\+ 2 = 4 := rfl$", "out": ["(no messages: Lean accepted it)"]},
             {"re": "^example : 2 \\+ 2 = 5 := rfl$", "out": ["error: Type mismatch", "  rfl", "has type", "  ?m.16 = ?m.16", "but is expected to have type", "  2 + 2 = 5"], "cls": "err"},
             {"re": "^theorem and_swap'? .*:= *fun", "out": ["(no messages: Lean accepted the theorem)"], "set": {"swap": "1"}},
             {"re": "^#print axioms and_swap'?$", "when": {"swap": "1"}, "out": ["'and_swap'' does not depend on any axioms"]},
             {"re": "^#print axioms and_swap'?$", "out": ["error: unknown constant 'and_swap'' (state the theorem first)"], "cls": "warn"},
             {"re": "^#print axioms peirce$", "out": ["'peirce' depends on axioms: [propext, Classical.choice, Quot.sound]"]}],
         "tasks": [{"text": "Check the type of a function type", "cmd": "^#check Nat"}, {"text": "Check And.intro", "cmd": "^#check And\\.intro$"}, {"text": "State and prove the swap theorem", "cmd": "^theorem and_swap"}, {"text": "Print its axioms", "cmd": "^#print axioms and_swap"}, {"text": "See an incorrect proof rejected", "cmd": "^example : 2 \\+ 2 = 5"}]},
        {"type": "fill", "title": "Proofs as terms", "text": "theorem a_imp_a (A : Prop) : A → A := {{fun a => a|fun x => x|fun h => h}}\nA theorem is a {{type}}, a proof is a {{term}}, and the {{kernel}} checks it."},
        {"type": "order", "title": "From idea to checked proof", "intro": "Put the proof assistant workflow in order.", "items": ["State the theorem as a type", "Write a proof term or tactics to build one", "The kernel type checks the term", "Check which axioms the proof uses", "Use the theorem in later proofs"]}]
})

# ------------------------------------------------------------ 12
CH.append({
    "title": "Beyond the triangle",
    "maps": [{"title": "Extensions of the correspondence", "links": [
        "Linear logic | matches | Linear types",
        "Linear types | model | Resources used once",
        "Linear logic | matches | Monoidal closed categories",
        "Monads | model | Computational effects",
        "Homotopy type theory | reads types as | Spaces",
        "Identity type | reads as | Paths",
        "Univalence | says | Equivalence is equality",
        "Quantum computing | uses | Dagger compact categories",
        "Rosetta Stone | connects | Physics, topology, logic, computation"]}],
    "summary": [
        "The correspondence is a pattern, not a single theorem. Change the logic and you change the programming language and the categories. Linear logic, where assumptions must be used exactly once, matches linear types and symmetric monoidal closed categories.",
        "Moggi showed that monads model computational effects such as state, exceptions and input and output. Homotopy type theory reads types as spaces and equalities as paths, and adds the univalence axiom. Categorical quantum mechanics uses categories with extra structure to describe quantum processes.",
        "You now have the core triangle. The best next steps are to try a proof assistant, to read a category theory text for programmers, and to write your own small type checker."],
    "glossary": [
        {"term": "Linear logic", "def": "A logic by Girard where each assumption must be used exactly once, so hypotheses behave like resources."},
        {"term": "Linear type", "def": "A type whose values must be used exactly once. Related ideas include ownership in Rust."},
        {"term": "Monad", "def": "A structure for sequencing computations with effects, introduced into semantics by Moggi."},
        {"term": "Homotopy type theory", "def": "Type theory read as homotopy theory, with types as spaces and equalities as paths."},
        {"term": "Univalence", "def": "Voevodsky's axiom that equivalent types are equal."},
        {"term": "Monoidal category", "def": "A category with a tensor product and unit, more general than a cartesian product."},
        {"term": "Rosetta Stone", "def": "Baez and Stay's table of analogies between physics, topology, logic and computation, via category theory."}],
    "keyPoints": [
        "Change the logic, and the types and categories change with it.",
        "Linear logic: use each assumption exactly once. Linear types and monoidal categories match.",
        "Rust-style ownership is closely related to affine and linear types.",
        "Monads package effects. Effects are not part of the pure correspondence.",
        "Homotopy type theory: types are spaces, equalities are paths.",
        "Next steps: use Lean, read about categories, implement a small type checker."],
    "lesson": [
        T("The correspondence is not a one-off. Whenever a logic has a good proof theory, you can look for a matching calculus and a matching class of categories. This chapter surveys four directions and then suggests where to go next."),
        T("First, linear logic, introduced by Jean-Yves Girard in 1987. In ordinary logic you can use an assumption as many times as you like, or not at all. In linear logic each assumption is used exactly once, so hypotheses behave like physical resources: a coin cannot be spent twice. The matching programs are linear lambda calculi, and the matching categories are symmetric monoidal closed categories, where the tensor product replaces the cartesian product."),
        M(r"A \otimes B \;\;\text{(both resources)} \qquad\qquad A \multimap B \;\;\text{(consume an } A \text{ to produce a } B\text{)}"),
        T("Programming languages use the idea. Rust's ownership system is closely related to affine types, where a value may be used at most once. Linear types are also used to control memory, protocols and quantum data, which cannot be copied."),
        T("Second, effects. Pure typed lambda calculus has no state, exceptions or input and output. Eugenio Moggi showed in 1989 and 1991 that a monad, a categorical structure, gives a uniform semantics for these effects, and Philip Wadler brought the idea into Haskell. Logically, monads correspond to a form of modality sometimes called lax logic, though this link is less tidy than the core triangle."),
        T("Third, homotopy type theory. Take dependent type theory and read each type as a space, each element as a point, and each equality proof as a path between points. Identity types then behave like path spaces, and the induction principle for equality is path induction. Vladimir Voevodsky's univalence axiom says that equivalent types are equal. Cubical type theory gives a version in which univalence also computes."),
        T("Fourth, physics. John Baez and Mike Stay's Rosetta Stone paper sets out a table of analogies between physics, topology, logic and computation, all through category theory. In categorical quantum mechanics, work by Abramsky and Coecke, quantum processes are arrows in a dagger compact category, and the diagrammatic calculus replaces linear algebra for some purposes."),
        T("Each of these pairs a logic with a calculus and a category. The core triangle you learned is the simplest member of the family, and it is the best place to start."),
        T("Where to go next. Install Lean and work through the official introductory book, Theorem Proving in Lean. Read an introduction to category theory for programmers. Write a small type checker for the simply typed lambda calculus in your favorite language; the lab in chapter 3 was a start. Try proving the exercises of this course in Lean. And look for the pattern: whenever you meet a new logic, ask what programs and what categories it has.")],
    "quiz": [
        {"q": "What is the key rule in linear logic?", "options": ["Use each assumption exactly once", "Use assumptions any number of times", "Never use assumptions", "Only use true assumptions"], "answer": 0, "explain": "Hypotheses behave like consumable resources."},
        {"q": "Which categories match linear logic?", "options": ["Cartesian closed categories only", "Symmetric monoidal closed categories", "Preorders", "Groups"], "answer": 1, "explain": "The tensor product replaces the cartesian product."},
        {"q": "Who introduced monads into semantics of effects?", "options": ["Eugenio Moggi", "Haskell Curry", "Joachim Lambek", "William Howard"], "answer": 0, "explain": "Moggi, with Wadler bringing monads into Haskell."},
        {"q": "In homotopy type theory what does an equality proof correspond to?", "options": ["A path between points", "A number", "A program", "A function"], "answer": 0, "explain": "Identity types behave like path spaces."}],
    "cards": [
        {"q": "Linear logic slogan?", "a": "Use each hypothesis exactly once."},
        {"q": "Monads are for?", "a": "Modeling computational effects."},
        {"q": "HoTT slogan?", "a": "Types are spaces, equalities are paths."},
        {"q": "Good first project?", "a": "Write a type checker for the simply typed lambda calculus."}],
    "practice": [
        {"type": "match", "title": "Logic, calculus and category", "intro": "Match each logic to its related programming idea.", "pairs": [["Intuitionistic logic", "Simply typed lambda calculus"], ["Linear logic", "Linear types, ownership"], ["Dependent type theory", "Lean, Rocq, Agda"], ["Homotopy type theory", "Types as spaces"]]},
        {"type": "write", "title": "Your next step", "prompt": "In one or two sentences, name one thing you will do next with this material, such as installing Lean or writing a type checker.", "checks": [{"re": "Lean|Rocq|Agda|type checker|category|proof", "msg": "names a next step"}, {"re": ".{20,}", "msg": "has a real sentence"}], "solution": "I will install Lean and prove the exercises from chapter 11."},
        {"type": "order", "title": "Learning path", "intro": "Put a sensible learning path in order.", "items": ["Learn natural deduction", "Learn the simply typed lambda calculus", "See the Curry-Howard dictionary", "Meet categories and the Lambek step", "Try a proof assistant"]}]
})
