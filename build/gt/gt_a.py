# -*- coding: utf-8 -*-
"""Game theory course, part 1: basics, equilibrium, mixed strategies, classic games."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


PD = "[[[3, 3], [0, 5]], [[5, 0], [1, 1]]]"

CHS.append(CH(
 "Games, players and payoffs",
 ("Basics", [
  "Game | has | Players",
  "Player | chooses | A strategy",
  "Payoff | measures | Outcome value",
  "Utility | encodes | Preferences",
  "Normal form | is | A payoff matrix",
  "Rational | means | Maximising payoff",
  "Common knowledge | is | Known by all"]),
 ["Game theory studies strategic situations where each person's best choice depends on what the others choose. A game lists the players, the strategies each can pick, and the payoff each gets for every combination.",
  "A two-player game with few strategies is shown as a payoff matrix: rows for one player, columns for the other, and each cell holds a pair of payoffs.",
  "Players are assumed rational: they pick strategies to maximise their own utility, and they know the others do the same. Games can be simultaneous or sequential, one-shot or repeated, competitive or cooperative."],
 [("Game", "A model of strategic interaction: players, strategies and payoffs."),
  ("Strategy", "A complete plan of action for a player."),
  ("Payoff", "The number a player receives for an outcome, expressing how much they like it."),
  ("Normal form", "A game described by a matrix of payoffs for every combination of strategies."),
  ("Zero-sum game", "A game in which one player's gain is exactly the other's loss.")],
 ["Players, strategies, payoffs.",
  "Cell (row, column) = (payoff of row, payoff of column).",
  "Rationality: maximise your own payoff.",
  "Payoff numbers express preference, not money alone.",
  "Zero-sum: payoffs add to a constant."],
 [T("Two shopkeepers on the same street must each decide whether to cut prices. If both cut, profits fall. If only one cuts, that shop takes the customers. If neither cuts, both do fine. Each shopkeeper's best move depends on the other's choice. That is a game."),
  T("To write a game down, list three things. The players. For each player, the strategies available. And the payoffs: for every combination of strategies, a number for each player saying how good the result is for them. The payoff numbers are utilities, which capture preferences, including risk and values, not only money."),
  T("For two players with a few strategies, the payoffs go in a matrix. The row player chooses a row, the column player chooses a column, and the cell shows two numbers, first the row player's payoff and then the column player's. Reading the matrix is the first skill of the subject."),
  T("Some games are purely competitive. In a zero-sum game, such as poker without the house cut, one player's gain is exactly the other's loss. Most real situations are mixed: there are gains from cooperation and also conflicts, and understanding the tension between them is the heart of the matter."),
  T("The assumptions matter. We say players are rational, meaning each tries to get the highest payoff, and that rationality is common knowledge: I know you are rational, you know that I know, and so on. Later chapters relax this, with evolution and learning, but we begin with the clean case.")],
 [("What does a game list?", ["Players, strategies and payoffs", "Only winners", "Only money", "Only rules of chess"], 0, "Three ingredients."),
  ("What is in a payoff matrix cell?", ["A payoff for each player", "A strategy name", "A probability", "The winner"], 0, "A pair."),
  ("What is a zero-sum game?", ["One player's gain equals the other's loss", "Everyone wins", "Nobody plays", "Payoffs are zero for all"], 0, "Fixed total."),
  ("What does rational mean here?", ["Maximising your own payoff", "Being kind", "Being random", "Being slow"], 0, "Self-interested."),
  ("What are payoffs?", ["Numbers expressing preferences", "Only cash", "Only probabilities", "Names"], 0, "Utility."),
  ("What does common knowledge mean?", ["Everyone knows, and knows that everyone knows", "Public gossip", "Only the referee knows", "Nobody knows"], 0, "Nested knowledge.")],
 [("(a, b)", "row payoff, column payoff"), ("zero-sum", "payoffs add to a constant"), ("u(x)", "utility of x")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Player", "decision maker"), ("Strategy", "complete plan of action"), ("Payoff", "value of an outcome"), ("Normal form", "payoff matrix"), ("Zero-sum", "gains equal losses")]),
  PL("Read a cell", "Write payoffs(game, r, c): the pair of payoffs [row payoff, column payoff] at row index r and column index c of a game given as a list of rows of [a, b] pairs.", "payoffs(game, r, c)", '''
def payoffs(game, r, c):
    return game[r][c]
''', [[[[[3, 3], [0, 5]], [[5, 0], [1, 1]]], 0, 1], [[[[3, 3], [0, 5]], [[5, 0], [1, 1]]], 1, 1], [[[[1, -1], [-1, 1]], [[-1, 1], [1, -1]]], 1, 0]], "Index the row then the column."),
  PL("Is it zero-sum?", "Write zero_sum(game): True if every cell's two payoffs add to the same constant (the sum is the same in all cells), otherwise False.", "zero_sum(game)", '''
def zero_sum(game):
    total = None
    for row in game:
        for cell in row:
            s = cell[0] + cell[1]
            if total is None:
                total = s
            elif s != total:
                return False
    return True
''', [[[[[1, -1], [-1, 1]], [[-1, 1], [1, -1]]]], [[[[3, 3], [0, 5]], [[5, 0], [1, 1]]]], [[[[2, 3], [4, 1]], [[0, 5], [5, 0]]]]], "Compare each cell's sum with the first."),
  PL("Expected payoff", "Write expected(payoffs, probs): the expected value of a list of payoffs under a list of probabilities, rounded to 4 decimals.", "expected(payoffs, probs)", '''
def expected(payoffs, probs):
    s = 0.0
    for i in range(len(payoffs)):
        s = s + payoffs[i] * probs[i]
    return round(s, 4)
''', [[[3, 0], [0.5, 0.5]], [[10, 0, 5], [0.2, 0.3, 0.5]], [[1, 2, 3], [1, 0, 0]]], "Multiply and add.", approx=0.0002),
  PL("Best response", "Write best_response(game, col): the row index with the highest row payoff when the column player plays column index col. If several rows tie return the smallest index.", "best_response(game, col)", '''
def best_response(game, col):
    best = 0
    for r in range(len(game)):
        if game[r][col][0] > game[best][col][0]:
            best = r
    return best
''', [[[[[3, 3], [0, 5]], [[5, 0], [1, 1]]], 0], [[[[3, 3], [0, 5]], [[5, 0], [1, 1]]], 1], [[[[2, 2], [2, 0]], [[2, 1], [2, 1]]], 0]], "Compare the first payoff in each row of that column.")]
))

CHS.append(CH(
 "Dominance and Nash equilibrium",
 ("Equilibrium", [
  "Dominant strategy | beats | All others",
  "Dominated | is never | Best",
  "Best response | is | Top reply",
  "Nash equilibrium | is | Mutual best replies",
  "Pure strategy | is | Single choice",
  "Iterated elimination | removes | Dominated strategies",
  "Multiple equilibria | need | Selection"]),
 ["A strategy strictly dominates another if it gives a higher payoff whatever the opponent does. A rational player never plays a dominated strategy, and removing dominated strategies can simplify a game, sometimes solving it.",
  "A best response is the strategy that maximises your payoff given what the others do. A Nash equilibrium is a combination of strategies where each player's strategy is a best response to the others, so no one gains by changing alone.",
  "To find pure Nash equilibria in a matrix, check every cell: is the row payoff the best in its column, and the column payoff the best in its row?"],
 [("Dominant strategy", "A strategy that is at least as good as all alternatives whatever the others do, and better in some case."),
  ("Best response", "The strategy that maximises a player's payoff given the others' choices."),
  ("Nash equilibrium", "A profile of strategies in which each is a best response to the others."),
  ("Pure strategy", "A strategy chosen with certainty, without randomisation."),
  ("Iterated elimination", "Repeatedly deleting strictly dominated strategies.")],
 ["Nash: no one can gain by switching alone.",
  "Check each cell: row best in column and column best in row.",
  "Dominated strategies are never Nash strategies.",
  "A game may have none, one or several pure equilibria.",
  "Nash proved mixed equilibria always exist."],
 [T("Two drivers approach a narrow bridge from opposite ends. If both stay, they crash. If one yields, the other passes. The question is what happens if each assumes the other is also thinking carefully. We need a solution concept, a rule that picks out the sensible outcomes of a game. The most famous is the Nash equilibrium."),
  T("Start with the easy case, dominance. If one of my strategies pays more than another whatever you do, I would never play the lower one. Remove it. Then check whether your strategies have become dominated in the smaller game. Repeat. If the process leaves one cell, the game is solved by iterated elimination."),
  T("Often nothing is dominated, so we use the best response idea. Given what you do, what is my best reply? A Nash equilibrium is a cell where my strategy is a best reply to yours and yours is a best reply to mine. Neither of us can do better by changing our own choice, so the outcome is stable."),
  T("To find the equilibria in a matrix, mark with a star the best payoff for the row player in each column, and the best payoff for the column player in each row. Any cell where both payoffs are starred is a pure Nash equilibrium. Some games have none, some have exactly one, and some have several."),
  T("John Nash proved in 1950 that every finite game has at least one equilibrium if mixed strategies are allowed, which the next chapter explains. He won the Nobel Prize in 1994 for it. A stable outcome is not the same as a good one: in the prisoner's dilemma, the unique equilibrium is worse for both than another outcome.")],
 [("What is a dominated strategy?", ["One that is worse whatever the opponent does", "One that wins sometimes", "A random one", "The best one"], 0, "Never optimal."),
  ("What is a Nash equilibrium?", ["Everyone is best-responding to the others", "Everyone is happy", "A tie", "The highest sum"], 0, "No unilateral gain."),
  ("How can you find pure equilibria in a matrix?", ["Mark best replies and find cells with both marked", "Add all payoffs", "Pick the largest cell", "Pick the first cell"], 0, "Star method."),
  ("Is a Nash equilibrium always efficient?", ["No", "Yes", "Only in zero-sum", "Only with two players"], 0, "Prisoner's dilemma."),
  ("What did Nash prove?", ["Every finite game has an equilibrium in mixed strategies", "Every game is zero-sum", "Games have no solutions", "Dominance always exists"], 0, "1950."),
  ("Can a game have several equilibria?", ["Yes", "No", "Only zero", "Only one"], 0, "Coordination games.")],
 [("BR(s)", "best response"), ("(s1*, s2*)", "equilibrium profile"), ("u_i(s*) >= u_i(s_i, s*_-i)", "Nash condition")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Dominant strategy", "best whatever others do"), ("Best response", "best given others' choice"), ("Nash equilibrium", "mutual best responses"), ("Pure strategy", "chosen with certainty"), ("Iterated elimination", "remove dominated strategies repeatedly")]),
  PL("Pure Nash equilibria", "Write nash(game): all cells (r, c) of a two-player game (list of rows of [a, b] pairs) where the row payoff is the maximum in its column and the column payoff is the maximum in its row (ties count as best). Return the list of [r, c] pairs sorted.", "nash(game)", '''
def nash(game):
    out = []
    nr = len(game)
    nc = len(game[0])
    for r in range(nr):
        for c in range(nc):
            a = game[r][c][0]
            b = game[r][c][1]
            ok = True
            for r2 in range(nr):
                if game[r2][c][0] > a:
                    ok = False
            for c2 in range(nc):
                if game[r][c2][1] > b:
                    ok = False
            if ok:
                out.append([r, c])
    return out
''', [[[[[3, 3], [0, 5]], [[5, 0], [1, 1]]]], [[[[2, 2], [0, 0]], [[0, 0], [1, 1]]]], [[[[1, -1], [-1, 1]], [[-1, 1], [1, -1]]]], [[[[4, 4], [1, 3]], [[3, 1], [2, 2]]]]], "Check all rows in the column and all columns in the row."),
  PL("Row dominant strategy", "Write row_dominant(game): the index of a row that strictly dominates all other rows (payoff greater in every column against every other row), or -1 if there is none.", "row_dominant(game)", '''
def row_dominant(game):
    nr = len(game)
    nc = len(game[0])
    for r in range(nr):
        good = True
        for r2 in range(nr):
            if r2 == r:
                continue
            for c in range(nc):
                if not game[r][c][0] > game[r2][c][0]:
                    good = False
        if good:
            return r
    return -1
''', [[[[[3, 3], [0, 5]], [[5, 0], [1, 1]]]], [[[[2, 2], [0, 0]], [[0, 0], [1, 1]]]], [[[[1, 0], [1, 0]], [[0, 1], [0, 1]]]]], "Compare row r with every other row in every column."),
  PL("Eliminate dominated rows", "Write eliminate_rows(game): repeatedly delete any row strictly dominated by another row (all of its row payoffs are lower in every column), considering only rows. Return the list of remaining row indexes (original numbering) in order.", "eliminate_rows(game)", '''
def eliminate_rows(game):
    alive = list(range(len(game)))
    nc = len(game[0])
    changed = True
    while changed:
        changed = False
        for r in alive:
            for r2 in alive:
                if r2 == r:
                    continue
                dom = True
                for c in range(nc):
                    if not game[r2][c][0] > game[r][c][0]:
                        dom = False
                if dom:
                    alive.remove(r)
                    changed = True
                    break
            if changed:
                break
    return alive
''', [[[[[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 0], [0, 3]]]], [[[[3, 3], [0, 5]], [[5, 0], [1, 1]]]], [[[[1, 0], [1, 0]], [[0, 1], [0, 1]]]]], "Stop when no row is dominated."),
  PL("Social welfare", "Write welfare(game, r, c): the sum of both players' payoffs in cell (r, c). Then return the pair [best cell sum over the whole game, sum at cell (r, c)].", "welfare(game, r, c)", '''
def welfare(game, r, c):
    best = None
    for row in game:
        for cell in row:
            s = cell[0] + cell[1]
            if best is None or s > best:
                best = s
    return [best, game[r][c][0] + game[r][c][1]]
''', [[[[[3, 3], [0, 5]], [[5, 0], [1, 1]]], 1, 1], [[[[3, 3], [0, 5]], [[5, 0], [1, 1]]], 0, 0], [[[[2, 2], [0, 0]], [[0, 0], [1, 1]]], 1, 1]], "Search all cells for the best total.")]
))

CHS.append(CH(
 "Mixed strategies and zero-sum games",
 ("Mixed strategies", [
  "Mixed strategy | randomises | Choices",
  "Indifference | makes | Opponent unreadable",
  "Expected payoff | averages | Over chances",
  "Minimax | limits | Worst case",
  "Value of game | is | Guaranteed payoff",
  "Saddle point | is | Pure solution",
  "Von Neumann | proved | Minimax theorem"]),
 ["In matching pennies there is no pure equilibrium: whichever side you pick, the opponent wants to switch. The solution is to randomise, a mixed strategy, so the opponent cannot exploit a pattern.",
  "In a mixed equilibrium each player chooses probabilities that make the other player indifferent between their strategies. For a 2x2 game this gives a simple formula.",
  "In a zero-sum game, von Neumann's minimax theorem says the maximin value (the best guaranteed payoff) equals the minimax value (what the opponent can hold you to). This common number is the value of the game."],
 [("Mixed strategy", "A probability distribution over pure strategies."),
  ("Indifference principle", "In a mixed equilibrium each player's mixing makes the other indifferent among the strategies they use."),
  ("Maximin", "The strategy that maximises the worst-case payoff."),
  ("Value of a game", "The payoff both players can guarantee in a zero-sum game under optimal play."),
  ("Saddle point", "A cell that is the minimum in its row and maximum in its column, giving a pure solution.")],
 ["2x2 mixing: choose p to make the opponent indifferent.",
  "Matching pennies: 50-50.",
  "Zero-sum: maximin = minimax.",
  "Saddle point: pure equilibrium exists.",
  "Mixed Nash always exists in finite games."],
 [T("In rock paper scissors, any pattern gets punished. If you always choose rock, your opponent chooses paper. The only unexploitable play is to mix evenly. The probabilities are chosen not to make you win, but to leave the opponent with no better reply than any other."),
  T("Here is the indifference idea in a 2 by 2 game. Suppose the column player plays the first column with probability q. The row player's expected payoffs from the two rows are linear in q. Choosing q so that those two are equal makes the row player indifferent, and then the row player can randomise in any way without loss. The row player's mixing is found by the same trick on the other side."),
  T("Mixed strategies can be seen as real randomisation, as in penalty kicks and poker bluffs, or as uncertainty about what the other will do. Studies of penalty kicks in football show that professionals mix almost exactly as the theory predicts, since a predictable kicker is a lost kicker."),
  T("Zero-sum games have a lovely extra property. One player wants to maximise, the other to minimise. If I choose to guarantee my best worst-case, called maximin, and you choose to hold me to the lowest, called minimax, von Neumann proved in 1928 that the two numbers agree when mixed strategies are allowed. That number is the value of the game."),
  T("If a cell is both the smallest in its row and the largest in its column, it is a saddle point and the game is solved with pure strategies. Otherwise the solution mixes, and for bigger games it is found by linear programming, one of the great practical algorithms.")],
 [("Why mix strategies?", ["To avoid being exploited", "To confuse yourself", "To save time", "To win every time"], 0, "Unpredictability."),
  ("What does the indifference principle say?", ["Mix so the opponent is indifferent", "Be indifferent to losing", "Ignore the opponent", "Pick the highest payoff"], 0, "Equal expected payoffs."),
  ("What is the value of a zero-sum game?", ["The guaranteed payoff under optimal play", "The highest cell", "The average cell", "Zero always"], 0, "Maximin = minimax."),
  ("Who proved the minimax theorem?", ["John von Neumann", "John Nash", "Alan Turing", "Isaac Newton"], 0, "1928."),
  ("Matching pennies has what equilibrium?", ["Both mix 50-50", "Both play heads", "Both play tails", "Pure only"], 0, "Symmetric."),
  ("What is a saddle point?", ["Min of its row and max of its column", "A tie", "A mixed strategy", "A loss"], 0, "Pure solution.")],
 [("p = (d - b) / (a - b - c + d)", "2x2 mixing ratio"), ("max min = min max", "minimax theorem")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Mixed strategy", "random choice with probabilities"), ("Indifference", "equal expected payoffs"), ("Maximin", "best worst case"), ("Saddle point", "pure solution of a zero-sum game"), ("Value", "guaranteed zero-sum payoff")]),
  PL("Matching pennies mix", "For a zero-sum 2x2 game with row payoffs [[a, b], [c, d]], the row player's probability of the first row that makes the column player indifferent is p = (d - c) / (a - b - c + d). Write mix_row(a, b, c, d), rounded to 4 decimals (assume the denominator is not zero).", "mix_row(a, b, c, d)", '''
def mix_row(a, b, c, d):
    return round((d - c) / float(a - b - c + d), 4)
''', [[1, -1, -1, 1], [2, 0, 0, 1], [3, 1, 0, 2], [0, 1, 1, 0]], "Solve p a + (1-p) c = p b + (1-p) d.", approx=0.0002),
  PL("Value of 2x2 game", "Write game_value(a, b, c, d): the value of the zero-sum game with row payoffs [[a, b], [c, d]] when there is no saddle point: (a d - b c) / (a - b - c + d), rounded to 4 decimals.", "game_value(a, b, c, d)", '''
def game_value(a, b, c, d):
    return round((a * d - b * c) / float(a - b - c + d), 4)
''', [[1, -1, -1, 1], [2, 0, 0, 1], [3, 1, 0, 2], [4, 1, 2, 3]], "Use the standard formula.", approx=0.0002),
  PL("Maximin and minimax", "Write maximin_minimax(M): for a zero-sum game with row player's payoff matrix M (list of rows), return the list [maximin, minimax] using pure strategies only: the maximum over rows of the row minimum, and the minimum over columns of the column maximum.", "maximin_minimax(M)", '''
def maximin_minimax(M):
    mm = None
    for row in M:
        lo = min(row)
        if mm is None or lo > mm:
            mm = lo
    mx = None
    for c in range(len(M[0])):
        hi = M[0][c]
        for r in range(len(M)):
            if M[r][c] > hi:
                hi = M[r][c]
        if mx is None or hi < mx:
            mx = hi
    return [mm, mx]
''', [[[[3, 1], [2, 4]]], [[[1, -1], [-1, 1]]], [[[2, 3], [1, 0]]], [[[5, 5], [5, 5]]]], "Row minima then column maxima."),
  PL("Has a saddle point?", "Write has_saddle(M): True if the pure maximin equals the pure minimax of the zero-sum matrix M, otherwise False.", "has_saddle(M)", '''
def has_saddle(M):
    mm = max([min(row) for row in M])
    cols = []
    for c in range(len(M[0])):
        cols.append(max([M[r][c] for r in range(len(M))]))
    return mm == min(cols)
''', [[[[3, 1], [2, 4]]], [[[1, -1], [-1, 1]]], [[[2, 3], [1, 0]]], [[[5, 5], [5, 5]]]], "They agree exactly when a saddle exists.")]
))

CHS.append(CH(
 "Classic games: dilemmas, coordination and conflict",
 ("Classic games", [
  "Prisoner's dilemma | pits | Self against group",
  "Stag hunt | rewards | Trust",
  "Chicken | rewards | Nerve",
  "Battle of the sexes | needs | Coordination",
  "Public goods | invite | Free riding",
  "Tragedy of the commons | overuses | Shared resource",
  "Pareto optimal | means | No free improvement"]),
 ["A handful of small games capture whole families of social situations. The prisoner's dilemma: defecting is dominant yet mutual cooperation is better for both. The stag hunt: two equilibria, one safe, one rewarding.",
  "Chicken (or hawk-dove) rewards the one who does not swerve but ruins both if neither swerves. The battle of the sexes: two people prefer to be together but disagree on where.",
  "The tension between individual incentive and group benefit appears in arms races, climate, overfishing, vaccination and team projects."],
 [("Prisoner's dilemma", "A game where defection is a dominant strategy but mutual cooperation gives both a better payoff."),
  ("Stag hunt", "A coordination game with a risky high-payoff equilibrium and a safe low-payoff one."),
  ("Chicken", "An anti-coordination game where each prefers to go straight if the other swerves."),
  ("Pareto optimal", "An outcome where no player can be made better off without making another worse off."),
  ("Tragedy of the commons", "Overuse of a shared resource because each user bears only a share of the cost.")],
 ["PD: T > R > P > S.",
  "Stag hunt: trust gives R, safe gives P.",
  "Chicken: two asymmetric equilibria.",
  "Coordination games: several equilibria.",
  "Nash does not imply Pareto optimal."],
 [T("Two suspects are held apart. Each can stay silent or betray the other. If both stay silent, they each get a short sentence. If one betrays, the betrayer goes free and the other gets a long sentence. If both betray, both get a medium sentence. Whatever the other does, betraying is better for me. So both betray, and both end up worse than if they had stayed silent. That is the prisoner's dilemma."),
  T("The numbers have a standard ordering. Temptation to defect T beats reward for mutual cooperation R, which beats punishment for mutual defection P, which beats the sucker's payoff S. With T above R above P above S, defection dominates. Many real problems share this shape: arms races, price wars, polluting, doping in sport, and overfishing."),
  T("The stag hunt changes the incentives. Two hunters can hunt a stag together, which pays well, or each hunt a hare alone, which pays modestly but surely. Both stag and both hare are equilibria. The question is trust: if I doubt you, I take the hare. Many cooperation problems are stag hunts rather than dilemmas, and fix themselves with communication and reputation."),
  T("Chicken is the game of two cars driving at each other. Going straight while the other swerves is best, swerving while the other goes straight is bad but survivable, and neither swerving is a catastrophe. The equilibria are the two asymmetric ones, and each side tries to look committed, by throwing away the steering wheel, for example. Brinkmanship has this structure."),
  T("In the battle of the sexes, a couple wants to spend the evening together but one prefers the opera and the other the football. Both would rather go together to either than apart. This is a pure coordination game with two good equilibria and a fight about which. Conventions such as driving on the right solve this on a large scale.")],
 [("In the prisoner's dilemma, what is dominant?", ["Defect", "Cooperate", "Mix", "Wait"], 0, "Whatever the other does."),
  ("What is the PD payoff ordering?", ["T > R > P > S", "R > T > S > P", "S > P > R > T", "P > R > T > S"], 0, "Temptation first."),
  ("How many pure equilibria does the stag hunt have?", ["Two", "One", "Zero", "Four"], 0, "Stag and hare."),
  ("What does Chicken reward?", ["Not swerving when the other does", "Always swerving", "Cooperation only", "Random play"], 0, "Nerve."),
  ("What is the tragedy of the commons?", ["Overuse of a shared resource", "A lost game", "A Greek play", "A tie"], 0, "Free riding."),
  ("Is the PD equilibrium Pareto optimal?", ["No", "Yes", "Only for two players", "Only when repeated"], 0, "Both could do better.")],
 [("T > R > P > S", "prisoner's dilemma ordering"), ("2R > T + S", "stops alternating exploitation")],
 [MATCH("Match the game", "Pair each game with its feature.", [("Prisoner's dilemma", "defection dominates"), ("Stag hunt", "trust versus safety"), ("Chicken", "do not swerve if the other does"), ("Battle of the sexes", "coordinate on which event"), ("Public goods", "tempting to free ride")]),
  PL("Is it a prisoner's dilemma?", "Write is_pd(T, R, P, S): True if T > R > P > S and 2R > T + S, otherwise False.", "is_pd(T, R, P, S)", '''
def is_pd(T, R, P, S):
    return T > R and R > P and P > S and 2 * R > T + S
''', [[5, 3, 1, 0], [4, 3, 2, 1], [5, 3, 1, 2], [10, 3, 1, 0], [6, 4, 2, 0]], "Check all the inequalities."),
  PL("Build the PD", "Write make_pd(T, R, P, S): the symmetric game as a list of rows of [row, col] pairs, with strategies ordered cooperate, defect: [[[R, R], [S, T]], [[T, S], [P, P]]].", "make_pd(T, R, P, S)", '''
def make_pd(T, R, P, S):
    return [[[R, R], [S, T]], [[T, S], [P, P]]]
''', [[5, 3, 1, 0], [4, 3, 2, 1]], "Fill the matrix carefully."),
  PL("Classify a 2x2 symmetric game", "For a symmetric 2x2 game with row payoffs a (both play first), b (I play first, other second), c (I play second, other first), d (both play second) write classify(a, b, c, d): return 'dilemma' if c > a and d > b (second strategy dominant) and a > d; 'coordination' if a > c and d > b; 'chicken' if c > a and b > d; otherwise 'other'.", "classify(a, b, c, d)", '''
def classify(a, b, c, d):
    if c > a and d > b and a > d:
        return 'dilemma'
    if a > c and d > b:
        return 'coordination'
    if c > a and b > d:
        return 'chicken'
    return 'other'
''', [[3, 0, 5, 1], [4, 0, 3, 2], [3, 1, 4, 0], [1, 1, 1, 1]], "Check the three patterns in order."),
  PL("Common pool", "Each of n players chooses to harvest h units; the pool yields total harvest T = n x h and each unit sells for max(0, 10 - T). Write profit(n, h): one player's profit h x max(0, 10 - n x h).", "profit(n, h)", '''
def profit(n, h):
    return h * max(0, 10 - n * h)
''', [[2, 1], [2, 3], [4, 2], [4, 3], [1, 5]], "More harvest by everyone lowers the price.")]
))
