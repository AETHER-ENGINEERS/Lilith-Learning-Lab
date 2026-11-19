from __future__ import annotations
from egglog import *
class Sg(Expr):
    @classmethod
    def p(cls) -> Sg: ...
    @classmethod
    def m(cls) -> Sg: ...
    def mul(self, o: Sg) -> Sg: ...
class Nat(Expr):
    @classmethod
    def z(cls) -> Nat: ...
    def s(self) -> Nat: ...
class Seq(Expr):
    @classmethod
    def nil(cls) -> Seq: ...
    @classmethod
    def cons(cls, s: Sg, r: Seq) -> Seq: ...
    def app(self, s: Sg) -> Seq: ...
    def pol(self) -> Sg: ...
    def size(self) -> Nat: ...
class Cyc(Expr):
    def __init__(self, s: Seq) -> None: ...
eg = EGraph()
a, x = vars_("a x", Sg); r = var("r", Seq)
eg.register(
    rewrite(Sg.p().mul(Sg.p())).to(Sg.p()), rewrite(Sg.p().mul(Sg.m())).to(Sg.m()), rewrite(Sg.m().mul(Sg.p())).to(Sg.m()), rewrite(Sg.m().mul(Sg.m())).to(Sg.p()),
    rewrite(Seq.nil().app(x)).to(Seq.cons(x, Seq.nil())), rewrite(Seq.cons(a, r).app(x)).to(Seq.cons(a, r.app(x))),
    rewrite(Cyc(Seq.cons(a, r))).to(Cyc(r.app(a))),
    rewrite(Seq.nil().pol()).to(Sg.p()), rewrite(Seq.cons(a, r).pol()).to(a.mul(r.pol())),
    rewrite(Seq.nil().size()).to(Nat.z()), rewrite(Seq.cons(a, r).size()).to(r.size().s()),
)
def mk(signs):
    s = Seq.nil()
    for g in reversed(signs): s = Seq.cons(Sg.p() if g == '+' else Sg.m(), s)
    return s
c1 = Cyc(mk('++-')); c2 = Cyc(mk('-++')); c3 = Cyc(mk('+-+')); c4 = Cyc(mk('+--'))
eg.register(c1, c2, c3, c4); eg.run(30)
print('rot equal 1~2', eg.check(eq(c1).to(c2)), '1~3', eg.check(eq(c1).to(c3)))
try: eg.check(eq(c1).to(c4)); print('1~4 True')
except Exception as e: print('1~4 False')
print(eg.extract(c1), '|', eg.extract(c2))
print(eg.extract(mk('++-').pol()), eg.extract(mk('--').pol()), eg.extract(mk('+--+').size()))
