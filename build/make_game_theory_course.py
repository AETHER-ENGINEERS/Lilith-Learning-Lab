#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Game Theory course. Usage: python3 make_game_theory_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "gt"))
import cmk, gt_a, gt_b, make_apps  # noqa: E402
make_apps.main()
CHS = gt_a.CHS + gt_b.CHS
PRONOUNCE = {"Nash": "nash", "Neumann": "noy mun", "Vickrey": "vick ree", "Axelrod": "ax el rod", "Rapoport": "rap uh port", "Shapley": "shap lee", "Condorcet": "con dor say", "Arrow": "arrow",
    "Gibbard": "gib erd", "Satterthwaite": "sat er thwayt", "Maynard": "may nerd", "Stackelberg": "shtack el berg", "Rubinstein": "roo bin stine", "Clarke": "clark", "Groves": "groves",
    "minimax": "min ih max", "maximin": "max ih min", "Pareto": "pa ray toe", "ESS": "E S S", "subgame": "sub game", "Bayesian": "bay zee un", "replicator": "rep lih kay ter", "equilibria": "ee kwih lib ree uh"}
SANDBOX = cmk.terminal("Game theory cheat sheet", "game>", "A scripted lookup. Try: nash, dominance, mixed, pd, backward, repeated, ess, vickrey, shapley", [
    ("nash", ["Nash equilibrium: each strategy is a best response to the others. Check each cell of the matrix."]),
    ("dominance", ["A dominated strategy is worse whatever the opponent does. Eliminate it, then repeat."]),
    ("mixed", ["Mix so the opponent is indifferent. 2x2: p = (d - c) / (a - b - c + d)."]),
    ("pd", ["Prisoner's dilemma: T > R > P > S. Defection dominates, mutual cooperation is better."]),
    ("backward", ["Backward induction: solve the last decision first and work toward the root."]),
    ("repeated", ["Grim trigger sustains cooperation when delta >= (T - R) / (T - P)."]),
    ("ess", ["ESS: resists small invasions. Hawk-dove with C > V: hawk share V / C."]),
    ("vickrey", ["Second-price auction: bid your true value; the winner pays the second-highest bid."]),
    ("shapley", ["Shapley value: average marginal contribution over all orders of joining."]),
])
EXAM = [
 ("What three things define a game?", ["Players, strategies and payoffs", "Rules, referee and prizes", "Cards, dice and boards", "Time, money and luck"], 0, "The ingredients."),
 ("What is a zero-sum game?", ["One player's gain equals the other's loss", "All players win", "Payoffs are zero for everyone", "There is no strategy"], 0, "Fixed total."),
 ("What is a dominant strategy?", ["Best whatever the others do", "The most common move", "A mixed strategy", "A threat"], 0, "No regret."),
 ("What is a Nash equilibrium?", ["Everyone best-responds to the others", "The fairest outcome", "The highest sum", "A tie"], 0, "No unilateral gain."),
 ("How do you find pure equilibria in a matrix?", ["Cells where both payoffs are best replies", "Add rows", "Pick the biggest cell", "Pick the first cell"], 0, "Star method."),
 ("Why do players mix strategies?", ["To avoid being exploited", "To save effort", "To please the audience", "To end the game"], 0, "Unpredictability."),
 ("What does the minimax theorem say?", ["In zero-sum games maximin equals minimax", "Every game is zero-sum", "Pure strategies always exist", "Mixing never helps"], 0, "Von Neumann."),
 ("What is the prisoner's dilemma ordering?", ["T > R > P > S", "R > T > S > P", "S > P > T > R", "P > S > R > T"], 0, "Temptation first."),
 ("What does the PD equilibrium look like?", ["Both defect, worse than mutual cooperation", "Both cooperate", "One defects", "Nobody plays"], 0, "Inefficient."),
 ("How many pure equilibria does the stag hunt have?", ["Two", "One", "Zero", "Three"], 0, "Stag and hare."),
 ("How does backward induction proceed?", ["From the last moves to the first", "From the first move onward", "Randomly", "By voting"], 0, "Leaves to root."),
 ("What is an empty threat?", ["A threat not worth carrying out", "A loud threat", "A silent move", "A tie"], 0, "Not credible."),
 ("What is subgame perfection?", ["Equilibrium in every subgame", "Perfect payoffs", "A mixed equilibrium", "A fair split"], 0, "Rules out empty threats."),
 ("What do people do in the ultimatum game?", ["Reject low offers", "Offer zero", "Accept anything", "Refuse to play"], 0, "Fairness matters."),
 ("What is tit for tat?", ["Cooperate first, then copy the opponent", "Always defect", "Always cooperate", "Randomise"], 0, "Rapoport."),
 ("Why can cooperation survive in repeated games?", ["The future carries rewards and punishments", "Payoffs change", "Rules forbid defection", "Players are kind"], 0, "Shadow of the future."),
 ("What does a known last round do?", ["Unravels cooperation", "Improves cooperation", "Makes all mix", "Nothing"], 0, "Backward induction."),
 ("What is an ESS?", ["A strategy that resists small invasions", "The highest-paying strategy", "A random mixture", "A threat"], 0, "Maynard Smith."),
 ("In replicator dynamics, when does a strategy spread?", ["Its fitness exceeds the average", "It is rare", "It is old", "It is nice"], 0, "x (f - average)."),
 ("In hawk-dove with C > V, hawk share at the ESS is:", ["V / C", "C / V", "1", "0"], 0, "Mixed."),
 ("What does the winner pay in a Vickrey auction?", ["The second-highest bid", "Their own bid", "Nothing", "The average"], 0, "Second price."),
 ("What is the best bid in a Vickrey auction?", ["Your true value", "Half your value", "Double", "Zero"], 0, "Dominant."),
 ("What is the winner's curse?", ["The winner tends to overpay", "Losers pay", "The auction fails", "Bids are void"], 0, "Optimistic estimates."),
 ("What is the Shapley value?", ["Average marginal contribution", "The largest payoff", "A fixed share", "The core"], 0, "Over all orders."),
 ("What is the core?", ["Allocations no coalition wants to leave", "The largest coalition", "The Shapley value", "A voting rule"], 0, "Stability."),
 ("What does the Condorcet paradox show?", ["Majority preferences can cycle", "Majorities always agree", "Voting is impossible", "Ties are rare"], 0, "A, B, C cycle."),
]
CFG = dict(id="game-theory", title="Game Theory",
    subtitle="Strategy, equilibrium, cooperation and auctions, with runnable Python labs and live simulations",
    description="A hands-on introduction to game theory: players, strategies and payoffs; dominance and Nash equilibrium; mixed strategies and the minimax theorem; the classic games of dilemma, trust, chicken and coordination; sequential games with backward induction and credible threats; repeated games and the evolution of cooperation; evolutionary game theory with replicator dynamics; auctions, bargaining and mechanism design; and cooperative games with the Shapley value and social choice with Arrow's theorem. Every chapter has Python labs verified in the built-in interpreter, a tournament of repeated-game strategies and a replicator dynamics lab.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="gt", apps={"__TOURN__": "tourn.html", "__EVOLVE__": "evolve.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "game-theory.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
