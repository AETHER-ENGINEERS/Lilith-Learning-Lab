# -*- coding: utf-8 -*-
"""Game theory course, part 2: sequential, repeated, evolutionary, auctions, cooperative, social choice."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Sequential games and backward induction",
 ("Sequential games", [
  "Extensive form | is | A game tree",
  "Information set | hides | Earlier moves",
  "Backward induction | solves | From the end",
  "Subgame perfect | rules out | Empty threats",
  "First-mover advantage | is | Commitment value",
  "Stackelberg | has | A leader",
  "Ultimatum game | tests | Fairness"]),
 ["When players move in turn and see earlier moves, the game is drawn as a tree. Backward induction solves it by starting at the last decisions and working back to the root.",
  "A subgame perfect equilibrium is a Nash equilibrium that is also an equilibrium in every subgame. It rules out empty threats, plans nobody would carry out when the time came.",
  "Moving first can be an advantage when it commits you, as in Stackelberg competition, but can be a disadvantage when it reveals information."],
 [("Extensive form", "A game represented as a tree of decisions in order, with payoffs at the leaves."),
  ("Backward induction", "Solving a finite sequential game by reasoning from the last move to the first."),
  ("Subgame perfect equilibrium", "A strategy profile that is a Nash equilibrium in every subgame."),
  ("Empty threat", "A threat that would not be in the threatener's interest to carry out."),
  ("Commitment", "Limiting your own future options in order to change others' behaviour.")],
 ["Solve from the leaves upward.",
  "At each node, the mover picks the best payoff for themselves.",
  "Subgame perfect = backward induction in finite perfect-information games.",
  "Commitment can create value.",
  "Ultimatum game: theory vs people."],
 [T("Chess is a sequential game: each player sees the board before moving. We draw such a game as a tree. Each node belongs to one player, each branch is a move, and each leaf shows the payoffs. To solve it, imagine yourself at the last decision. The mover there simply takes the best option. Replace that node by its outcome, and move one step up."),
  T("This is backward induction. At each step, the player on move picks the branch giving them the highest payoff, given the already-solved continuations. When you reach the root you know the whole path. In a finite game with perfect information, this gives a clear prediction. It also shows that chess has a best result under perfect play, though it is too large to compute."),
  T("Consider an entrant deciding whether to enter a market with a monopolist. The monopolist threatens a price war if the entrant enters. But if the entrant does enter, a price war hurts the monopolist too, so it would rather accommodate. The threat is empty. Backward induction predicts entry and accommodation, a subgame perfect equilibrium. Threats must be credible to count."),
  T("Because commitment can make a threat credible, giving up options can be powerful. A general who burns the bridges behind the army shows there is no retreat. A company that builds extra capacity makes a price war credible. In Stackelberg competition, the firm that moves first and commits to a large output forces the follower to adjust, and earns more than in the simultaneous game."),
  T("The ultimatum game tests the theory. One person proposes how to split ten pounds, and the other accepts or rejects, in which case both get nothing. Theory says offer the smallest amount and the other accepts. In experiments people often offer nearly half and reject offers under about thirty percent. Fairness and emotion are part of the payoffs.")],
 [("How is a sequential game drawn?", ["As a tree", "As a matrix only", "As a line", "As a table of words"], 0, "Extensive form."),
  ("How does backward induction work?", ["Solve the last moves first", "Solve the first move first", "Guess", "Randomise"], 0, "From the leaves."),
  ("What is an empty threat?", ["One not worth carrying out", "A loud threat", "A tie", "A mixed strategy"], 0, "Not credible."),
  ("What does subgame perfection rule out?", ["Non-credible threats", "All equilibria", "Mixing", "First moves"], 0, "Empty threats."),
  ("Why can commitment help?", ["It makes threats credible", "It removes payoffs", "It adds players", "It lowers cost"], 0, "Burn the bridges."),
  ("What do people do in the ultimatum game?", ["Offer near half and reject low offers", "Always offer zero", "Always reject", "Always accept"], 0, "Fairness.")],
 [("backward induction", "solve from the end"), ("SPE", "subgame perfect equilibrium")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Extensive form", "game tree"), ("Backward induction", "solve from the last move"), ("Empty threat", "not credible"), ("Subgame perfect", "equilibrium in every subgame"), ("Commitment", "limits own options")]),
  PL("Solve a game tree", "A tree is either a leaf [payoff_player0, payoff_player1] (a list of two numbers) or a node ['player', child1, child2, ...] where player is 0 or 1. Write solve(tree): the payoff pair reached by backward induction (the mover picks the child whose payoff for them is highest; ties go to the first such child).", "solve(tree)", '''
def solve(tree):
    return _solve(tree)

def _solve(tree):
    if not isinstance(tree[0], str):
        return tree
    p = tree[1]
    best = None
    for child in tree[2:]:
        v = _solve(child)
        if best is None or v[p] > best[p]:
            best = v
    return best
''', [[["n", 0, [2, 1], [1, 3]]], [["n", 0, ["n", 1, [3, 1], [0, 0]], [2, 2]]], [["n", 1, ["n", 0, [1, 5], [2, 2]], ["n", 0, [4, 4], [0, 0]]]]], "Recursion: solve children, then choose for the mover."),
  PL("Entry game", "An entrant chooses In or Out. If Out, payoffs (0, 4) (entrant, incumbent). If In, the incumbent chooses Fight (payoffs -1, -1) or Accommodate (payoffs 2, 2). Write entry(fight_payoff_inc, accommodate_payoff_inc): by backward induction return 'in' if the entrant enters and 'out' if not, where the entrant gets -1 after Fight and 2 after Accommodate, and the incumbent's payoffs are the arguments.", "entry(fight_payoff_inc, accommodate_payoff_inc)", '''
def entry(fight_payoff_inc, accommodate_payoff_inc):
    if fight_payoff_inc > accommodate_payoff_inc:
        entrant_gets = -1
    else:
        entrant_gets = 2
    if entrant_gets > 0:
        return 'in'
    return 'out'
''', [[-1, 2], [3, 2], [2, 2], [0, 1]], "Find the incumbent's choice first."),
  PL("Stackelberg leader", "Two firms with demand price = 100 - (q1 + q2), zero cost. The follower best-responds q2 = (100 - q1) / 2. Write leader_profit(q1): the leader's profit q1 x (100 - q1 - q2), rounded to 2 decimals.", "leader_profit(q1)", '''
def leader_profit(q1):
    q2 = (100 - q1) / 2.0
    return round(q1 * (100 - q1 - q2), 2)
''', [[50], [40], [20], [100], [60]], "Plug the follower's reply into the leader's profit.", approx=0.01),
  PL("Ultimatum acceptance", "Write ultimatum(offer, total, threshold): the responder accepts when offer / total >= threshold. Return the list [accepted (True/False), proposer's share] where the proposer's share is total - offer if accepted, otherwise 0.", "ultimatum(offer, total, threshold)", '''
def ultimatum(offer, total, threshold):
    if offer / float(total) >= threshold:
        return [True, total - offer]
    return [False, 0]
''', [[3, 10, 0.3], [2, 10, 0.3], [5, 10, 0.5], [0, 10, 0.1]], "A rejection leaves nothing.")]
))

CHS.append(CH(
 "Repeated games and the evolution of cooperation",
 ("Repeated games", [
  "Repeated game | has | Many rounds",
  "Shadow of the future | encourages | Cooperation",
  "Tit for tat | copies | Last move",
  "Trigger strategy | punishes | Defection",
  "Discount factor | weighs | The future",
  "Folk theorem | allows | Many equilibria",
  "Reputation | sustains | Trust"]),
 ["If the prisoner's dilemma is played once, defection wins. If it is played repeatedly with no known end, the future can discipline the present: cooperating may be worth it to keep the other cooperating.",
  "Robert Axelrod's tournaments found that a simple strategy, tit for tat (cooperate first, then copy the opponent's last move), outscored far more elaborate ones. It is nice, retaliatory, forgiving and clear.",
  "The folk theorem says that when players value the future enough, almost any feasible outcome better than the minimum can be sustained as an equilibrium of the repeated game."],
 [("Repeated game", "A game in which the same stage game is played many times."),
  ("Tit for tat", "Cooperate on the first round, then do whatever the opponent did last round."),
  ("Grim trigger", "Cooperate until the opponent defects once, then defect forever."),
  ("Discount factor", "The weight delta between 0 and 1 on payoffs one round later."),
  ("Folk theorem", "In infinitely repeated games with patient players, many outcomes can be sustained in equilibrium.")],
 ["Grim trigger sustains cooperation if delta >= (T - R) / (T - P).",
  "Sum of delta^t = 1 / (1 - delta).",
  "Last-round unravelling: known end means defect.",
  "Tit for tat: nice, retaliating, forgiving, clear.",
  "Reputation and repeat business support cooperation."],
 [T("Shopkeepers who sell to the same neighbours every day tend to be honest. A one-time tourist trap can cheat. The difference is the future. In a repeated game, a player who defects today may lose cooperation tomorrow. The shadow of the future turns a dilemma into a problem that can be solved."),
  T("Grim trigger is a simple example: cooperate until the other defects once, then defect forever. Is cooperation worth it? Cooperating forever pays R each round, worth R over one minus delta in total, where delta is how much you value tomorrow compared with today. Defecting pays T once and then P forever. Cooperation wins when delta is at least T minus R over T minus P."),
  T("If the number of rounds is known, the logic unravels. On the last round, defection is dominant. So on the second-to-last, the future gives no reward for cooperating, and so on back to the first round. In practice people do cooperate in finite games, and uncertainty about the end or about the opponent's type restores cooperation."),
  T("In the 1980s, Robert Axelrod invited experts to submit programs for a computer tournament of the repeated prisoner's dilemma. The winner was the shortest, tit for tat, submitted by Anatol Rapoport. It starts by cooperating and then copies the opponent's previous move. Axelrod noted that successful strategies were nice, never defecting first, yet retaliatory, forgiving and clear."),
  T("The folk theorem is the general result. When players are patient enough, any outcome that gives each player more than their worst-case payoff can be an equilibrium of the repeated game. Cooperation is possible, but so are many other outcomes. Which one emerges depends on norms, history and institutions. The lab lets you run a tournament of strategies yourself.")],
 [("Why can cooperation survive in repeated games?", ["Future punishment and reward", "Players are kind", "Payoffs change", "The rules forbid defection"], 0, "Shadow of the future."),
  ("What does tit for tat do?", ["Cooperates first, then copies", "Always defects", "Always cooperates", "Plays randomly"], 0, "Rapoport."),
  ("What is grim trigger?", ["Defect forever after one defection", "Forgive at once", "Copy the last move", "Randomise"], 0, "Permanent punishment."),
  ("What does a high discount factor mean?", ["The future matters a lot", "The future is ignored", "Payoffs are halved", "The game ends"], 0, "Patience."),
  ("What does a known last round cause?", ["Unravelling of cooperation", "More cooperation", "Mixed strategies", "Nothing"], 0, "Backward induction."),
  ("What does the folk theorem say?", ["Many outcomes are equilibria for patient players", "Only defection is possible", "All games are zero-sum", "Mixing is impossible"], 0, "Many equilibria.")],
 [("1 / (1 - delta)", "sum of discounted rounds"), ("delta >= (T - R) / (T - P)", "grim trigger condition")],
 [APP("TOURN", "Strategy tournament", "Play a round-robin tournament of the repeated prisoner's dilemma between classic strategies and one you control by choosing a rule. Run the tournament with at least four strategies and see who wins.", 780),
  MATCH("Match the strategy", "Pair each strategy with its behaviour.", [("Tit for tat", "copy the last move"), ("Grim trigger", "defect forever after a defection"), ("Always defect", "never cooperate"), ("Always cooperate", "never defect"), ("Random", "coin flip")]),
  PL("Tit for tat match", "Write tft_vs(opp_moves): given the list of opponent moves ('C' or 'D'), return tit for tat's own moves: 'C' first, then the opponent's previous move each round (same length as opp_moves).", "tft_vs(opp_moves)", '''
def tft_vs(opp_moves):
    out = []
    for i in range(len(opp_moves)):
        if i == 0:
            out.append('C')
        else:
            out.append(opp_moves[i - 1])
    return out
''', [[['C', 'C', 'D', 'C']], [['D', 'D', 'D']], [['C']], [[]]], "Look at the previous opponent move."),
  PL("Score a match", "Write score(a_moves, b_moves, T, R, P, S): the total payoff of player A over the rounds, where each pair of moves earns R for CC, S for A=C vs B=D, T for A=D vs B=C, and P for DD. Return A's total as an integer.", "score(a_moves, b_moves, T, R, P, S)", '''
def score(a_moves, b_moves, T, R, P, S):
    total = 0
    for i in range(len(a_moves)):
        a = a_moves[i]
        b = b_moves[i]
        if a == 'C' and b == 'C':
            total = total + R
        elif a == 'C' and b == 'D':
            total = total + S
        elif a == 'D' and b == 'C':
            total = total + T
        else:
            total = total + P
    return total
''', [[['C', 'C', 'C'], ['C', 'C', 'C'], 5, 3, 1, 0], [['D', 'D'], ['C', 'D'], 5, 3, 1, 0], [['C', 'D', 'C'], ['D', 'D', 'C'], 5, 3, 1, 0]], "Add the right payoff for each round."),
  PL("Discounted value", "Write discounted(payoff, delta, rounds): the sum of payoff x delta^t for t = 0 to rounds-1, rounded to 4 decimals.", "discounted(payoff, delta, rounds)", '''
def discounted(payoff, delta, rounds):
    s = 0.0
    for t in range(rounds):
        s = s + payoff * delta ** t
    return round(s, 4)
''', [[3, 0.9, 5], [1, 0.5, 10], [2, 1, 4], [4, 0, 3]], "Weight round t by delta to the t.", approx=0.0002),
  PL("Minimum patience", "Write min_delta(T, R, P): the smallest discount factor for which grim trigger sustains cooperation, (T - R) / (T - P), rounded to 4 decimals.", "min_delta(T, R, P)", '''
def min_delta(T, R, P):
    return round((T - R) / float(T - P), 4)
''', [[5, 3, 1], [4, 3, 1], [10, 6, 2], [6, 5, 2]], "Compare cooperating forever with defecting once.", approx=0.0002)]
))

CHS.append(CH(
 "Evolutionary game theory",
 ("Evolution", [
  "Population | plays | Strategies",
  "Fitness | is | Payoff",
  "ESS | resists | Invaders",
  "Replicator dynamics | grows | Fitter strategies",
  "Hawk-dove | has | Mixed ESS",
  "Frequency | is | Population share",
  "Mutation | tests | Stability"]),
 ["Evolutionary game theory replaces rational thought by selection: strategies that earn more payoff spread in the population, those that earn less shrink. No one needs to be clever.",
  "An evolutionarily stable strategy (ESS) is one that, once common, cannot be invaded by a small group using a different strategy. Every strict Nash equilibrium is an ESS.",
  "Replicator dynamics describe how the share of each strategy changes: x' = x (f - average fitness). In hawk-dove the population settles at a mix of hawks and doves."],
 [("Evolutionarily stable strategy", "A strategy that, if adopted by most of a population, cannot be displaced by a rare mutant."),
  ("Replicator dynamics", "Equations in which a strategy's share grows when its payoff is above the population average."),
  ("Hawk-dove game", "A contest over a resource in which hawks fight and doves share or retreat."),
  ("Fitness", "The payoff a strategy earns against the current population, interpreted as reproductive success."),
  ("Frequency dependence", "A strategy's success depends on how common each strategy is.")],
 ["x' = x (f(x) - average).",
  "Hawk-dove ESS: share of hawks = V / C when C > V.",
  "ESS: resists a small invasion.",
  "Stable fixed point of the dynamics.",
  "Payoffs become offspring."],
 [T("Biologists noticed that animals seldom fight to the death over territory, even though fighting is natural. John Maynard Smith and George Price explained this in 1973 with game theory. Evolution is a game where strategies are inherited and payoffs are offspring."),
  T("In the hawk-dove game, hawks always escalate and doves display and retreat. The resource is worth V. A fight costs C to the loser, sharing the cost. Two doves split V. A hawk beats a dove and takes all. Two hawks fight, getting V minus C over two each on average. If C exceeds V, hawks can't take over: a population of all hawks is invaded by doves, and all doves is invaded by hawks."),
  T("The balance is a mixed equilibrium in which a fraction V over C of the population are hawks. At that mix, hawks and doves earn the same. Any drift toward more hawks makes hawks do worse, and the population returns. This fixed point is an evolutionarily stable state."),
  T("The replicator equation formalises this. The growth rate of strategy i's share is its share times the amount by which its fitness exceeds the average. Strategies above the average spread. Fixed points are where all present strategies earn the same. The same maths describes the spread of ideas, habits and behaviours in cultures, where success is copied."),
  T("Evolutionary game theory explains the persistence of altruism, signalling and conventions. It also reveals that cooperation in the prisoner's dilemma dies out in a well-mixed population but can survive when like meets like, through kinship, reputation or local neighbourhoods. The lab shows the dynamics for several games.")],
 [("What replaces rationality in evolutionary game theory?", ["Selection", "Planning", "Luck only", "Communication"], 0, "Fitter spreads."),
  ("What is an ESS?", ["A strategy that resists invaders", "The best strategy always", "A mixed strategy only", "A random choice"], 0, "Maynard Smith."),
  ("In hawk-dove with C > V, what is the hawk share?", ["V / C", "C / V", "1", "0"], 0, "Mixed ESS."),
  ("When does a strategy grow in replicator dynamics?", ["Its fitness is above average", "It is rare", "It is nice", "It is old"], 0, "x (f - avg)."),
  ("Is a strict Nash equilibrium an ESS?", ["Yes", "No", "Only in zero-sum", "Only with mixing"], 0, "It resists mutants."),
  ("What can sustain cooperation in a population?", ["Kinship or reputation", "Nothing", "Speed", "Random mixing only"], 0, "Like meets like.")],
 [("x_i' = x_i (f_i - f_avg)", "replicator equation"), ("V / C", "hawk fraction in the ESS")],
 [APP("EVOLVE", "Replicator dynamics lab", "Choose a game (prisoner's dilemma, hawk-dove, stag hunt) and a starting share, then watch the population evolve. Try all three games to complete the lab.", 760),
  MATCH("Match the term", "Pair each term with its meaning.", [("ESS", "resists small invasions"), ("Fitness", "payoff against the population"), ("Replicator dynamics", "shares follow fitness"), ("Hawk-dove", "fight or retreat"), ("Frequency dependence", "success depends on how common others are")]),
  PL("Hawk-dove payoffs", "Write hd_payoffs(V, C): the symmetric payoff matrix as [[hawk vs hawk, hawk vs dove], [dove vs hawk, dove vs dove]] = [[(V - C) / 2, V], [0, V / 2]], each rounded to 3 decimals.", "hd_payoffs(V, C)", '''
def hd_payoffs(V, C):
    return [[round((V - C) / 2.0, 3), round(float(V), 3)], [0, round(V / 2.0, 3)]]
''', [[2, 4], [4, 2], [6, 10]], "Build the four entries.", approx=0.002),
  PL("Hawk fraction at the ESS", "Write hawk_ess(V, C): the hawk share of the mixed ESS: 1 if V >= C, otherwise V / C. Round to 4 decimals.", "hawk_ess(V, C)", '''
def hawk_ess(V, C):
    if V >= C:
        return 1
    return round(V / float(C), 4)
''', [[2, 4], [4, 2], [3, 3], [1, 10]], "Pure hawk when the prize beats the cost.", approx=0.0002),
  PL("Replicator step", "For a two-strategy population with share x of strategy 1, matrix A (payoffs [[a, b], [c, d]]) and a time step dt, write replicator(x, A, dt): f1 = a x + b (1-x), f2 = c x + d (1-x), average = x f1 + (1-x) f2, new x = x + dt x (f1 - average). Round to 4 decimals.", "replicator(x, A, dt)", '''
def replicator(x, A, dt):
    f1 = A[0][0] * x + A[0][1] * (1 - x)
    f2 = A[1][0] * x + A[1][1] * (1 - x)
    avg = x * f1 + (1 - x) * f2
    return round(x + dt * x * (f1 - avg), 4)
''', [[0.5, [[3, 0], [5, 1]], 0.1], [0.5, [[-1, 2], [0, 1]], 0.1], [0.2, [[4, 0], [3, 2]], 0.1], [0.9, [[4, 0], [3, 2]], 0.1]], "Compute both fitnesses and the average.", approx=0.0002),
  PL("Run the dynamics", "Write evolve(x0, A, dt, steps): apply the replicator step repeatedly and return the final share rounded to 3 decimals.", "evolve(x0, A, dt, steps)", '''
def evolve(x0, A, dt, steps):
    x = float(x0)
    for i in range(steps):
        f1 = A[0][0] * x + A[0][1] * (1 - x)
        f2 = A[1][0] * x + A[1][1] * (1 - x)
        avg = x * f1 + (1 - x) * f2
        x = x + dt * x * (f1 - avg)
    return round(x, 2)
''', [[0.5, [[3, 0], [5, 1]], 0.1, 50], [0.5, [[-1, 2], [0, 1]], 0.1, 100], [0.4, [[4, 0], [3, 2]], 0.1, 100], [0.6, [[4, 0], [3, 2]], 0.1, 100]], "Repeat the step.", approx=0.02)]
))

CHS.append(CH(
 "Auctions, bargaining and mechanism design",
 ("Mechanism design", [
  "Auction | allocates | By bids",
  "Second-price | rewards | Honest bids",
  "First-price | invites | Shading",
  "Winner's curse | punishes | Overbidding",
  "Mechanism design | engineers | Rules",
  "Incentive compatible | means | Truth is best",
  "Nash bargaining | splits | The surplus"]),
 ["Auctions are games with money. In a sealed-bid second-price (Vickrey) auction the highest bidder wins but pays the second-highest bid, and bidding your true value is a dominant strategy.",
  "In a first-price auction you pay what you bid, so you shade your bid below your value. Under standard assumptions both formats give the seller the same expected revenue, the revenue equivalence theorem.",
  "Mechanism design runs game theory backward: choose the rules so that selfish play produces the outcome you want. Vickrey, Clarke and Groves showed how truthful reporting can be made optimal."],
 [("Vickrey auction", "A sealed-bid auction in which the highest bidder wins and pays the second-highest bid."),
  ("Bid shading", "Bidding less than your true value in a first-price auction."),
  ("Winner's curse", "In common-value auctions the winner tends to have overestimated the value."),
  ("Mechanism design", "Designing rules of a game so that self-interested behaviour achieves a desired goal."),
  ("Nash bargaining solution", "The split that maximises the product of the players' gains over their disagreement payoffs.")],
 ["Vickrey: bid your value.",
  "First price, 2 bidders uniform: bid v / 2.",
  "Revenue equivalence: same expected revenue.",
  "Nash bargaining: maximise (u1 - d1)(u2 - d2).",
  "Incentive compatible: truth-telling is optimal."],
 [T("Auctions price art, spectrum licences, oil fields and the ads you see online. They are games where the rules decide who wins and what is paid. The sealed-bid second-price auction has a lovely property. The winner pays the second-highest bid, so your own bid only decides whether you win, not what you pay. Therefore bid your true value."),
  T("Why is truth best? If you bid higher than your value you may win at a price above your value and lose money. If you bid lower you may lose an auction you'd have profited from. Bidding exactly your value is never worse and sometimes better, so it is a dominant strategy. Search engines use a variation of this to sell ad slots."),
  T("In a first-price auction the winner pays their own bid, so honest bidding earns zero profit. You bid below your value, trading a lower chance of winning against a higher profit if you win. With two bidders whose values are uniform between zero and one, the optimal bid is half your value. Surprisingly, the seller's expected revenue is the same as in the Vickrey auction."),
  T("When the item has the same value to everyone but each bidder has only a noisy estimate, the winner is the one with the most optimistic estimate and likely overpaid. This is the winner's curse. Wise bidders shade their bids to correct for it. Oil companies learned this the hard way."),
  T("Mechanism design asks: what rules make people reveal what we need to know? Besides auctions, it covers matching students to schools, kidneys to patients and the design of voting rules. Bargaining theory covers the two-person case: Nash's solution splits the surplus to maximise the product of gains, and Rubinstein's alternating offers model shows that patience gives bargaining power.")],
 [("What does the winner pay in a Vickrey auction?", ["The second-highest bid", "Their own bid", "Nothing", "The average bid"], 0, "Second price."),
  ("What is the best bid in a Vickrey auction?", ["Your true value", "Zero", "Double your value", "Half your value"], 0, "Dominant."),
  ("What is bid shading?", ["Bidding below value in a first-price auction", "Hiding the bid", "Bidding in secret", "Bidding twice"], 0, "Trade-off."),
  ("What is the winner's curse?", ["The winner tends to overpay", "The winner is cursed", "Losers pay", "Bids are void"], 0, "Optimistic estimates."),
  ("What is mechanism design?", ["Designing rules for desired outcomes", "Building machines", "Solving matrices", "Drawing trees"], 0, "Reverse game theory."),
  ("What does Nash bargaining maximise?", ["The product of gains", "The sum of payoffs", "One player's gain", "Time"], 0, "(u1-d1)(u2-d2).")],
 [("b = v / 2", "first-price bid, uniform, 2 bidders"), ("max (u1-d1)(u2-d2)", "Nash bargaining")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Vickrey auction", "winner pays second price"), ("First-price auction", "winner pays own bid"), ("Winner's curse", "winner overpays"), ("Mechanism design", "design rules for goals"), ("Nash bargaining", "maximise product of gains")]),
  PL("Second-price auction", "Write vickrey(bids): the list [winner index, price] where the highest bidder (the first one if tied) wins and pays the second-highest bid (equal to the highest if tied; 0 if there is only one bid).", "vickrey(bids)", '''
def vickrey(bids):
    w = 0
    for i in range(len(bids)):
        if bids[i] > bids[w]:
            w = i
    others = []
    for i in range(len(bids)):
        if i != w:
            others.append(bids[i])
    price = max(others) if others else 0
    return [w, price]
''', [[[10, 8, 5]], [[3, 9, 9]], [[7]], [[1, 2, 3, 4]]], "The winner pays the best of the others."),
  PL("First-price auction profit", "Write fp_profit(value, bid, rival_bid): the winner's profit in a first-price auction: value - bid if bid > rival_bid, 0 otherwise.", "fp_profit(value, bid, rival_bid)", '''
def fp_profit(value, bid, rival_bid):
    if bid > rival_bid:
        return value - bid
    return 0
''', [[10, 6, 4], [10, 6, 8], [10, 10, 5], [5, 5, 5]], "Pay your own bid when you win."),
  PL("Expected profit with shading", "With one rival whose bid is uniformly random between 0 and 1, the probability of winning with bid b is b (for 0 <= b <= 1). Write exp_profit(value, b): (value - b) x b, rounded to 4 decimals.", "exp_profit(value, b)", '''
def exp_profit(value, b):
    return round((value - b) * b, 4)
''', [[1, 0.5], [1, 0.3], [0.8, 0.4], [0.6, 0.6]], "Profit times win probability.", approx=0.0002),
  PL("Nash bargaining split", "Two players split a surplus S with disagreement payoffs d1 and d2 (utility is linear in money). The Nash solution gives player 1: d1 + (S - d1 - d2) / 2. Write nash_split(S, d1, d2): the list [player 1 payoff, player 2 payoff] rounded to 3 decimals.", "nash_split(S, d1, d2)", '''
def nash_split(S, d1, d2):
    gain = (S - d1 - d2) / 2.0
    return [round(d1 + gain, 3), round(d2 + gain, 3)]
''', [[10, 0, 0], [10, 2, 0], [10, 3, 1], [100, 20, 40]], "Share the surplus above disagreement equally.", approx=0.002)]
))

CHS.append(CH(
 "Cooperative games and social choice",
 ("Cooperative games", [
  "Coalition | is | A group of players",
  "Characteristic function | gives | Coalition value",
  "Shapley value | is | Fair share",
  "Core | is | Stable allocations",
  "Voting | aggregates | Preferences",
  "Arrow | proves | Impossibility",
  "Condorcet | finds | Cycles"]),
 ["Cooperative game theory asks how a group that can bind its members should split the gains. A characteristic function says what each coalition can achieve alone.",
  "The Shapley value gives each player their average marginal contribution over all orders in which the coalition could form. It is the unique allocation satisfying fairness axioms. The core is the set of allocations no coalition could improve on by leaving.",
  "Social choice asks how to combine individual rankings into a group decision. Condorcet's paradox shows majorities can cycle, and Arrow's impossibility theorem shows that no ranking method satisfies a short list of fairness conditions."],
 [("Coalition", "A subset of players who agree to act together."),
  ("Characteristic function", "A function v(S) giving the value a coalition S can secure."),
  ("Shapley value", "A player's average marginal contribution across all orders of joining the coalition."),
  ("Core", "The allocations that no coalition can improve upon by breaking away."),
  ("Condorcet paradox", "A situation where majority preferences form a cycle: A beats B, B beats C, C beats A.")],
 ["phi_i = average of v(S + i) - v(S) over orders.",
  "Efficient: Shapley values add to v(all).",
  "Core: no coalition gets less than v(S).",
  "Condorcet winner beats every other option.",
  "Arrow: no perfect ranking rule."],
 [T("Three friends each bring something to a business. One has money, one skill and one a customer list. Alone, none can earn much, but together they earn a lot. How should the profit be split? The characteristic function lists what every possible group, called a coalition, can earn, and the question is what each member deserves."),
  T("Lloyd Shapley's answer is to imagine the group forming one member at a time, in random order, and to pay each member what they add to the groups already there, their marginal contribution. Averaging over all orders gives the Shapley value. It adds up to the total, treats equal players equally, and gives nothing to someone who adds nothing. It is used to explain machine learning predictions and to share costs among airlines using one runway."),
  T("The core takes a different view: an allocation is stable if no subgroup could do better by leaving. Some games have a core, others have none, and in some it contains many allocations. The Shapley value is always defined and is sometimes outside the core."),
  T("Voting is social choice. Suppose three voters rank candidates A, B and C as A over B over C, B over C over A, and C over A over B. A majority prefers A to B, a majority prefers B to C, and a majority prefers C to A. The majority preference runs in a circle. This is the Condorcet paradox, found in 1785."),
  T("Kenneth Arrow proved in 1951 that no voting method that ranks three or more options can satisfy a short list of reasonable conditions: unanimity, independence of irrelevant options, and no dictator. Gibbard and Satterthwaite later showed that any reasonable method can be manipulated by insincere voting. Every voting system has trade-offs, and choosing one means choosing which flaws to accept.")],
 [("What does the characteristic function give?", ["The value of each coalition", "The winner", "A strategy", "A probability"], 0, "v(S)."),
  ("What is the Shapley value?", ["Average marginal contribution", "Largest payoff", "A fixed share", "The core"], 0, "Over all orders."),
  ("What does the core ensure?", ["No coalition wants to break away", "Equal shares", "Maximum profit", "Fair voting"], 0, "Stability."),
  ("What is Condorcet's paradox?", ["Majority preference can cycle", "Majorities always agree", "Voting is impossible", "Ties are rare"], 0, "A over B over C over A."),
  ("What did Arrow prove?", ["No ranking rule meets all fairness conditions", "All voting works", "Majority is best", "Dictators are fair"], 0, "1951."),
  ("What do Gibbard and Satterthwaite show?", ["Reasonable voting rules can be manipulated", "Voting is honest", "Ties are impossible", "Ranking is easy"], 0, "Strategic voting.")],
 [("v(S)", "worth of coalition S"), ("phi_i", "Shapley value of player i"), ("A > B > C > A", "Condorcet cycle")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Coalition", "group acting together"), ("Shapley value", "average marginal contribution"), ("Core", "no group wants to leave"), ("Condorcet paradox", "majority cycle"), ("Arrow's theorem", "no perfect ranking rule")]),
  PL("Shapley value for 3 players", "Write shapley(v): v is a dict-free list of 8 values giving the worth of coalitions indexed by bitmask (bit 0 = player 0, bit 1 = player 1, bit 2 = player 2), so v[0] = 0 and v[7] is the grand coalition. Return the list of Shapley values for players 0, 1, 2 (averaging over all 6 orders), rounded to 3 decimals.", "shapley(v)", '''
def shapley(v):
    orders = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
    phi = [0.0, 0.0, 0.0]
    for o in orders:
        mask = 0
        for p in o:
            phi[p] = phi[p] + v[mask | (1 << p)] - v[mask]
            mask = mask | (1 << p)
    return [round(x / 6.0, 3) for x in phi]
''', [[[0, 0, 0, 10, 0, 10, 10, 20]], [[0, 6, 6, 6, 6, 6, 6, 6]], [[0, 0, 0, 0, 0, 0, 0, 12]], [[0, 1, 2, 4, 3, 5, 6, 9]]], "Add each player's marginal contribution in every order."),
  PL("Efficiency check", "Write efficient(v, alloc): True if the allocation list alloc adds up to v[7], the grand coalition's worth (compare with a tolerance of 0.001).", "efficient(v, alloc)", '''
def efficient(v, alloc):
    return abs(sum(alloc) - v[7]) < 0.001
''', [[[0, 0, 0, 10, 0, 10, 10, 20], [10, 5, 5]], [[0, 0, 0, 10, 0, 10, 10, 20], [10, 5, 4]], [[0, 0, 0, 0, 0, 0, 0, 12], [4, 4, 4]]], "Sum the allocation."),
  PL("In the core?", "Write in_core(v, alloc): True if for every coalition mask from 1 to 7 the sum of alloc over its members is at least v[mask], and the total equals v[7] (tolerance 0.001).", "in_core(v, alloc)", '''
def in_core(v, alloc):
    if abs(sum(alloc) - v[7]) > 0.001:
        return False
    for mask in range(1, 8):
        s = 0
        for p in range(3):
            if mask & (1 << p):
                s = s + alloc[p]
        if s < v[mask] - 0.001:
            return False
    return True
''', [[[0, 0, 0, 10, 0, 10, 10, 20], [8, 6, 6]], [[0, 0, 0, 10, 0, 10, 10, 20], [20, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 12], [4, 4, 4]], [[0, 0, 0, 10, 0, 10, 10, 12], [4, 4, 4]]], "Test each of the seven coalitions."),
  PL("Pairwise majority", "Write majority(ballots, a, b): ballots is a list of rankings (each a list of candidate names, best first). Return the candidate preferred by more voters, between a and b, or 'tie' if equal.", "majority(ballots, a, b)", '''
def majority(ballots, a, b):
    na = 0
    nb = 0
    for r in ballots:
        if r.index(a) < r.index(b):
            na = na + 1
        else:
            nb = nb + 1
    if na > nb:
        return a
    if nb > na:
        return b
    return 'tie'
''', [[[['A', 'B', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B']], 'A', 'B'], [[['A', 'B', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B']], 'B', 'C'], [[['A', 'B', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B']], 'C', 'A'], [[['A', 'B'], ['B', 'A']], 'A', 'B']], "Count which comes earlier on each ballot.")]
))
