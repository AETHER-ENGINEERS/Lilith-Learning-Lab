#!/usr/bin/env python3
"""Build the Curry-Howard-Lambek course. Usage: python3 make_trinity_course.py <out.json>"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "trinity"))
import t1, t2, t3  # noqa: E402


def app(name):
    with open(os.path.join(HERE, "trinity", "apps", name), encoding="utf-8") as f:
        return f.read()


PRONOUNCE = {
    "Lambek": "lam beck", "Curry": "curry", "Howard": "how ward", "Martin-Löf": "mar tin loff", "Martin-Lof": "mar tin loff",
    "Girard": "zhee rar", "Gentzen": "gent sen", "Rocq": "rock", "Coq": "coke", "Agda": "ag dah", "Idris": "id riss",
    "STLC": "S T L C", "HoTT": "hot", "BHK": "B H K", "Heyting": "hay ting", "Tait": "tate", "Moggi": "mow jee",
    "Voevodsky": "vo evod sky", "Wadler": "wad ler", "Abramsky": "a bram ski", "Coecke": "coo kuh", "Baez": "by ez",
    "Mathlib": "math lib", "CompCert": "comp cert", "seL4": "S E L 4", "Isabelle": "iz a bell", "Lean": "lean",
    "Prop": "prop", "CCC": "C C C", "Sigma": "sigma", "Pi": "pie", "refl": "reflexivity", "rfl": "reflexivity",
    "Haskell": "has kell", "Church": "church", "Prawitz": "prah wits", "Lawvere": "law veer", "Scott": "scott",
    "Hilbert": "hill bert", "Brouwer": "brow er", "Kolmogorov": "kol mo gor off", "Tarski": "tar ski", "Kleisli": "kly slee",
    "isomorphism": "eye so mor fizm", "morphism": "mor fizm", "functor": "funk tor", "Heyting algebra": "hay ting algebra",
}

SANDBOX = {
    "type": "terminal", "title": "Trinity lookup", "prompt": "trinity>",
    "intro": "A scripted lookup tool, not a real type checker. Try: type K, type S, type I, type fst, type swap, type curry, dict, help",
    "chips": ["type I", "type K", "type S", "type fst", "type swap", "type curry", "dict", "help"],
    "commands": [
        {"re": "^help$", "out": ["type <I|K|S|fst|snd|swap|curry|uncurry|compose>   principal type and the tautology it proves", "dict                                              the logic / program / category dictionary"]},
        {"re": "^type I$", "out": ["I = λx. x : A → A", "Proves: A implies A. Category: the identity arrow."]},
        {"re": "^type K$", "out": ["K = λx. λy. x : A → B → A", "Proves: weakening, A implies (B implies A)."]},
        {"re": "^type S$", "out": ["S = λf. λg. λx. f x (g x) : (A → B → C) → (A → B) → A → C", "Proves: distribution of implication. Uses x twice (contraction)."]},
        {"re": "^type fst$", "out": ["fst = λp. p.1 : A × B → A", "Proves: A and B implies A. Category: a projection."]},
        {"re": "^type snd$", "out": ["snd = λp. p.2 : A × B → B", "Proves: A and B implies B. Category: a projection."]},
        {"re": "^type swap$", "out": ["swap = λp. (p.2, p.1) : A × B → B × A", "Proves: and is commutative. Category: the symmetry isomorphism."]},
        {"re": "^type curry$", "out": ["curry = λf. λa. λb. f (a, b) : (A × B → C) → A → B → C", "Category: the exponential adjunction, forward."]},
        {"re": "^type uncurry$", "out": ["uncurry = λf. λp. f p.1 p.2 : (A → B → C) → A × B → C", "Category: the exponential adjunction, backward."]},
        {"re": "^type compose$", "out": ["compose = λf. λg. λx. f (g x) : (B → C) → (A → B) → A → C", "Proves: implication is transitive. Category: composition."]},
        {"re": "^type ", "out": ["Unknown name. Try: I K S fst snd swap curry uncurry compose"], "cls": "warn"},
        {"re": "^dict$", "out": ["logic         program        category", "implication   function type  exponential", "and           pair           product", "true          unit           terminal object", "false         empty type     initial object", "or            sum            coproduct", "proof         program        arrow", "cut elim.     evaluation     equality of arrows"]},
        {"re": ".", "out": ["Unknown command. Type help."], "cls": "warn"}],
    "tasks": []
}

EXAM = [
    ("Under Curry-Howard, a proof of A implies B corresponds to what?", ["A pair", "A function from A to B", "A set", "A tautology"], 1, "Implication is the function type."),
    ("Which type corresponds to logical conjunction?", ["Sum type", "Product (pair) type", "Function type", "Unit type"], 1, "A proof of A and B is a pair."),
    ("Which type corresponds to disjunction?", ["Product", "Sum (tagged union)", "Unit", "Function"], 1, "A proof of A or B is a tagged value of one side."),
    ("Which type has no values and corresponds to falsity?", ["Unit", "Bool", "The empty type", "Nat"], 2, "No closed term inhabits it."),
    ("Normalizing a program corresponds to what in logic?", ["Weakening", "Cut elimination", "Contraction", "Negation"], 1, "Reducing a redex removes a detour in the proof."),
    ("What does the combinator K prove?", ["A implies A", "A implies (B implies A)", "Excluded middle", "Double negation elimination"], 1, "K ignores its second argument, which is weakening."),
    ("Which of these is NOT provable intuitionistically?", ["A implies not not A", "A or not A for arbitrary A", "(A and B) implies (B and A)", "Not (A and not A)"], 1, "Excluded middle needs a classical axiom."),
    ("Which fact makes simply typed lambda calculus a good logic?", ["It has loops", "Every well-typed term normalizes", "It has no functions", "It has side effects"], 1, "Strong normalization keeps the logic consistent."),
    ("What does the exponential object B^A represent?", ["Maps from B to A", "Maps from A to B", "Pairs of A and B", "A union B"], 1, "It is the object of functions from A to B."),
    ("What does lambda abstraction become in a CCC?", ["Evaluation", "Currying", "Projection", "Coproduct"], 1, "It is the transpose across the exponential adjunction."),
    ("A context x:A, y:B is interpreted as what?", ["A + B", "A x B", "B^A", "1"], 1, "Contexts are products."),
    ("A Heyting algebra is what, categorically?", ["A group", "A bicartesian closed preorder", "A monoid", "A topos only"], 1, "It is the posetal case of the correspondence."),
    ("Which type corresponds to the existential quantifier?", ["Pi type", "Sigma type", "Function type", "Sum type"], 1, "A witness paired with a proof about it."),
    ("What is induction on the naturals in programming terms?", ["A loop", "A recursive function with a dependent result type", "An exception", "A module"], 1, "The induction principle is the dependent recursor."),
    ("What do tactics produce in a proof assistant?", ["Comments", "Proof terms checked by the kernel", "Machine code only", "Axioms"], 1, "Only the kernel needs to be trusted."),
    ("In linear logic, how often is each assumption used?", ["Any number of times", "Exactly once", "Never", "At least twice"], 1, "Hypotheses behave like resources."),
]


def split_long(items, limit=300):
    out = []
    for t in items:
        while len(t) > limit:
            cut = t.rfind('. ', 0, limit)
            if cut < 80:
                break
            out.append(t[:cut + 1]); t = t[cut + 2:]
        out.append(t)
    return out


def stack(tex):
    parts = [x.strip() for x in re.split(r'\\q?quad(?:\s*\\q?quad)*', tex) if x.strip()]
    if len(parts) < 2:
        return tex
    return '\\begin{gathered} ' + ' \\\\[0.6em] '.join(parts) + ' \\end{gathered}'


def build():
    chapters = t1.CH + t2.CH + t3.CH
    for ch in chapters:
        ch["summary"] = split_long(ch["summary"])
        for b in ch["lesson"]:
            if b["type"] == "math":
                b["tex"] = stack(b["tex"])
            if b["type"] == "text":
                b["items"] = split_long(b["items"])
    html = {"__LAMBDA__": app("lambda.html"), "__TRINITY__": app("trinity.html")}
    for ch in chapters:
        for lab in ch["practice"]:
            if lab["type"] == "webxdc" and lab["html"] in html:
                lab["html"] = html[lab["html"]]
    return {
        "format": "lilith-course", "version": 1, "id": "curry-howard-lambek",
        "title": "Curry-Howard-Lambek",
        "subtitle": "Computational trinitarianism: logic, programs and categories",
        "author": "Lilith Learning Lab",
        "description": "A course on the three-way correspondence between logic, programming languages and category theory, usually called computational trinitarianism. It builds from natural deduction and the simply typed lambda calculus to cartesian closed categories, then dependent types, proof assistants and the wider family of correspondences. Math uses LaTeX. Lean examples were checked against Lean 4; other code is illustrative.",
        "pronounce": PRONOUNCE,
        "chapters": chapters,
        "finalExam": {"title": "Final exam: Curry-Howard-Lambek", "passMark": 70, "size": 16,
                      "questions": [{"q": q, "options": o, "answer": a, "explain": e} for q, o, a, e in EXAM]},
        "sandbox": SANDBOX,
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "trinity.course.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=1)
    print("wrote", out)
