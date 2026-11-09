"""AlphaGo course, chapters 1-4."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

GROUP = """
def group_of(board, r, c):
    n = len(board)
    color = board[r][c]
    seen = [[r, c]]
    stack = [[r, c]]
    libs = []
    while stack:
        p = stack.pop()
        for dr, dc in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            y = p[0] + dr
            x = p[1] + dc
            if 0 <= y < n and 0 <= x < n:
                ch = board[y][x]
                if ch == '.':
                    if [y, x] not in libs:
                        libs.append([y, x])
                elif ch == color and [y, x] not in seen:
                    seen.append([y, x])
                    stack.append([y, x])
    return [seen, libs]
"""

# ------------------------------------------------------------ 1
CHS.append(CH(
 "What is AlphaGo?",
 ("The big picture", [
  "AlphaGo | combines | Neural networks and tree search",
  "Policy network | reduces | Search breadth",
  "Value network | reduces | Search depth",
  "Supervised learning | uses | Human expert games",
  "Reinforcement learning | improves | The policy by self-play",
  "AlphaGo | beat | Fan Hui 5-0",
  "AlphaGo | beat | Lee Sedol 4-1"]),
 ["AlphaGo is the DeepMind program that became the first to beat a professional Go player on a full board without handicap. It did so in October 2015 against the European champion Fan Hui, and in March 2016 it beat Lee Sedol, one of the world's top players, four games to one.",
  "Its idea is to combine Monte Carlo tree search with deep neural networks. A policy network suggests promising moves, which cuts the breadth of the search. A value network judges positions, which cuts its depth.",
  "The networks were trained in stages: first to imitate human experts, then improved by self-play. This course builds each piece in small Python programs."],
 [("Go", "A two-player board game of surrounding territory, played on a 19 by 19 grid."),
  ("Policy network", "A neural network giving a probability for each move."),
  ("Value network", "A neural network estimating who is winning from a position."),
  ("Monte Carlo tree search", "A search that grows a tree from many simulated games."),
  ("Supervised learning", "Learning to copy labelled examples, here the moves of human experts."),
  ("Reinforcement learning", "Learning from outcomes, here from winning and losing self-play games.")],
 ["AlphaGo was published in Nature on 28 January 2016 by Silver, Huang and colleagues at DeepMind.",
  "It beat the European champion Fan Hui 5-0 in October 2015, the first win over a professional on a full board without handicap.",
  "It beat Lee Sedol 4-1 in March 2016.",
  "Four learned components: a fast rollout policy, an SL policy network, an RL policy network and a value network.",
  "Policy networks cut the breadth of the search; the value network cuts its depth.",
  "Later versions (Master, Zero) and AlphaZero removed the human data."],
 [T("For decades Go was seen as the hardest classic game for computers. Chess programs conquered the human champion in 1997, when Deep Blue beat Garry Kasparov. In Go the strongest programs of the time had only reached about amateur five dan, and still could not beat a professional without a handicap."),
  T("The Nature paper of 28 January 2016, by David Silver, Aja Huang and eighteen colleagues, changed that. Its abstract introduces value networks to evaluate board positions and policy networks to select moves. These deep neural networks are trained by a novel combination of supervised learning from human expert games and reinforcement learning from games of self-play. It also introduces a new search algorithm that combines Monte Carlo simulation with the value and policy networks."),
  T("The headline results: the program won 99.8 percent of its games against other Go programs, and defeated the human European Go champion by five games to zero. The champion was Fan Hui, a professional of rank two dan. The match took place in October 2015, and the news was held back until the paper appeared in January 2016."),
  T("The sequel was a five-game match in Seoul in March 2016 against Lee Sedol, a nine dan professional. AlphaGo won four games to one, and was later awarded an honorary nine dan by the Korea Baduk Association. Lee won the fourth game, the only loss AlphaGo suffered in its official games, a story told in chapter 12."),
  T("Here is the plan of the machine. A search must handle two problems. Go has about two hundred and fifty legal moves in a typical position and games last about a hundred and fifty moves, so the tree is enormous. The paper uses two general principles. A value function lets the search stop early by judging a position directly, reducing depth. A policy lets it look only at likely moves, reducing breadth."),
  T("AlphaGo has four learned components. A fast rollout policy is a small linear model that plays quickly. A supervised learning policy network, called the SL policy network, is a deep convolutional network trained to predict the moves of human experts. A reinforcement learning policy network starts from the SL network and is improved by self-play. A value network is trained to predict the winner of games played by that RL network against itself."),
  M(r"p_\sigma,\; p_\pi,\; p_\rho,\; v_\theta \;\longrightarrow\; \text{Monte Carlo tree search}"),
  T("A note on sources. This course follows the 2016 Nature paper, whose numbers I quote, and public accounts of the matches such as the AlphaGo and AlphaGo versus Lee Sedol articles. The labs are my own teaching miniatures on small boards and small games. DeepMind did not release AlphaGo's code, so nothing here is a copy of it."),
  T("The course path. Chapter 2 explains Go and its rules. Chapter 3 covers the programs that came before. Chapters 4 to 8 build the four learned components. Chapter 9 sets out the search, chapter 10 the engineering and ratings, chapter 11 a miniature version in code, and chapter 12 the matches, successors and criticisms.")],
 [("Who did AlphaGo beat in October 2015?", ["Fan Hui", "Lee Sedol", "Ke Jie", "Kasparov"], 0, "The European champion, 5-0."),
  ("What does a value network estimate?", ["Who is winning", "The next move", "The board size", "The komi"], 0, "It judges a position."),
  ("How were the networks trained?", ["Supervised learning from experts, then reinforcement learning from self-play", "Only by hand-written rules", "From chess games", "By random search"], 0, "A novel combination of both."),
  ("What was the result against Lee Sedol?", ["4-1 for AlphaGo", "5-0 for AlphaGo", "3-2 for Lee", "1-4 for AlphaGo"], 0, "March 2016, Seoul.")],
 [("When was the Nature paper published?", "28 January 2016."), ("What does the policy network reduce?", "The breadth of the search."), ("What does the value network reduce?", "The depth of the search."),
  ("Was the code released?", "No.")],
 [ORDER("The training pipeline", "Put the stages in order.", ["Train a fast rollout policy and an SL policy network on expert moves", "Initialize the RL policy network from the SL network", "Improve the RL network by self-play", "Generate self-play positions with outcomes", "Train the value network to predict the winner"]),
  MATCH("Components", "Match each component with its job.", [("Rollout policy", "Quickly plays out games"), ("SL policy network", "Predicts expert moves"), ("RL policy network", "Maximizes winning through self-play"), ("Value network", "Predicts the winner from a position"), ("MCTS", "Combines them in a search")]),
  MATCH("People and matches", "Match each name with its role.", [("Fan Hui", "European champion beaten 5-0"), ("Lee Sedol", "Nine dan opponent in Seoul"), ("David Silver", "First author of the Nature paper"), ("Deep Blue", "Beat Kasparov at chess in 1997"), ("Pachi", "Open-source Go program")]),
  FILL("Basics", "AlphaGo combines {{neural networks|deep neural networks}} with Monte Carlo {{tree search|tree-search}}. The {{policy}} network reduces breadth and the {{value}} network reduces depth.")]))

# ------------------------------------------------------------ 2
CHS.append(CH(
 "The game of Go",
 ("Rules", [
  "Players | alternate | Placing stones",
  "Group | has | Liberties",
  "Zero liberties | means | Capture",
  "Ko rule | forbids | Repeating positions",
  "Area scoring | counts | Stones and territory",
  "Komi | compensates | White for moving second",
  "Go | has | About 250 moves per turn"]),
 ["Go is played on a 19 by 19 grid. Black and White alternate placing a stone on an empty point. Connected stones of one colour form a group, and the empty points next to a group are its liberties. A group with no liberties is captured and removed.",
  "A move that repeats an earlier position is not allowed; this is the ko rule. At the end the players count area: a player's stones plus the empty points surrounded only by their stones. White receives komi, here 7.5 points, because Black moves first.",
  "The rules fit on a page, but a typical position has about two hundred and fifty legal moves and a game lasts about a hundred and fifty moves."],
 [("Liberty", "An empty point next to a stone or group."),
  ("Group", "Stones of one colour connected along grid lines."),
  ("Capture", "Removing a group that has no liberties."),
  ("Ko", "A situation where players could repeat a position forever; repeating is forbidden."),
  ("Komi", "Points added to White's score to compensate for Black's first move."),
  ("Area scoring", "Score = stones plus surrounded empty points; used with Chinese rules.")],
 ["Players alternate; Black moves first.",
  "A group is captured when it has no liberties.",
  "Suicide moves are generally forbidden and positions may not repeat (ko).",
  "Chinese area scoring counts stones and surrounded empty points; the Lee Sedol match used a 7.5 komi.",
  "Go's branching factor is about 250 and its depth about 150, versus about 35 and 80 for chess.",
  "Evaluating a Go position is hard because the board has no simple material count."],
 [T("Go is about two thousand five hundred years old and is played on a grid of nineteen lines by nineteen. Two players, Black and White, take turns putting a stone of their colour on an empty intersection. Black plays first. Stones never move. Once placed they stay until captured."),
  T("Stones of the same colour that touch along a grid line form a group. The empty points that touch a group along grid lines are its liberties. When Black plays the last liberty of a White group, the group is captured and removed from the board. A player may not make a move that leaves their own group with no liberties, unless that move captures something. This ban is called the suicide rule, and it varies slightly between rule sets."),
  T("Ko is the situation in which two players could capture one stone back and forth forever. Rules forbid a move that would recreate an earlier board position. Different rule sets phrase this differently, and the details matter in play. The labs here implement the simplest version: you may not immediately recreate the position of one move ago."),
  T("The game ends when both players pass. Under Chinese rules, as used in the Lee Sedol match, each player scores their stones plus the empty regions that only they border. White adds komi because Black has the advantage of the first move. The Lee match used seven and a half, and the half point guarantees there are no ties."),
  T("Now compare Go with chess in numbers from the paper. Chess has a branching factor of about thirty-five and a depth of about eighty. Go has a branching factor of about two hundred and fifty and a depth of about a hundred and fifty. Exhaustive search is hopeless in both, and Go is far worse."),
  M(r"b^{d}:\quad \text{chess } 35^{80}\ \approx\ 10^{123}, \qquad \text{Go } 250^{150}\ \approx\ 10^{360}"),
  T("The second difficulty is evaluation. In chess, counting material gives a useful first estimate of who is ahead. In Go every stone is worth the same, and the value of a position depends on the potential of groups, the ownership of regions and fine tactical fights. Programmers had struggled for decades to write a good evaluation function by hand. That is what makes learning an evaluation function so attractive."),
  T("The practice section builds the fundamental operations on a small board: neighbours, groups and liberties, playing a move with captures, and area scoring. A board is a list of strings, one per row, with X for Black, O for White and a dot for empty.")],
 [("What is a liberty?", ["An empty point next to a group", "A captured stone", "A pass", "A scoring unit"], 0, "Groups live by their liberties."),
  ("When is a group captured?", ["When it has no liberties", "When it has one stone", "When Black passes", "At move 100"], 0, "Zero liberties."),
  ("Why does White get komi?", ["Black moves first", "White is weaker", "To end ties in chess", "It is a penalty"], 0, "Compensation for the first move."),
  ("Which has the larger branching factor?", ["Go", "Chess", "They are equal", "Checkers"], 0, "About 250 against about 35.")],
 [("What is ko?", "A repeating-capture situation that rules forbid."), ("What is area scoring?", "Stones plus surrounded empty points."), ("What was komi in the Lee match?", "7.5 points."),
  ("Why is evaluation hard?", "No simple material count.")],
 [PL("Neighbours", "Write neighbours(r, c, n): the list of [row, col] pairs of the on-board points next to (r, c) on an n by n board, in the order up, down, left, right (skipping those off the board).",
     "neighbours(r, c, n)", """
def neighbours(r, c, n):
    out = []
    for dr, dc in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        y = r + dr
        x = c + dc
        if 0 <= y < n and 0 <= x < n:
            out.append([y, x])
    return out
""", [[0, 0, 5], [2, 2, 5], [4, 4, 5], [0, 3, 5], [1, 0, 3]], "Try the four offsets and keep the ones inside the board."),
  PL("Group size and liberties", "A board is a list of equal-length strings of 'X', 'O' and '.'. Write group_info(board, r, c): [number of stones, number of liberties] of the group containing the stone at (r, c). If the point is empty return [0, 0].",
     "group_info(board, r, c)", GROUP + """
def group_info(board, r, c):
    if board[r][c] == '.':
        return [0, 0]
    g = group_of(board, r, c)
    return [len(g[0]), len(g[1])]
""", [[["X....", ".....", ".....", ".....", "....."], 0, 0], [["XX...", "XO...", ".....", ".....", "....."], 0, 0], [["XX...", "XO...", ".O...", ".....", "....."], 1, 1], [["XXO..", "XOO..", ".....", ".....", "....."], 0, 2], [[".....", ".....", ".....", ".....", "....."], 2, 2]], "Flood fill from the stone, collecting same-colour neighbours and distinct empty neighbours."),
  PL("Play a move", "Write play(board, r, c, color): place a stone of color ('X' or 'O') at (r, c). First remove every opponent group that now has no liberties. If your own group then has no liberties, or the point is occupied, the move is illegal. Return [new board as list of strings, number of stones captured], or [[], 0] if illegal.",
     "play(board, r, c, color)", GROUP + """
def play(board, r, c, color):
    n = len(board)
    if board[r][c] != '.':
        return [[], 0]
    b = [list(row) for row in board]
    b[r][c] = color
    other = 'O'
    if color == 'O':
        other = 'X'
    captured = 0
    for dr, dc in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        y = r + dr
        x = c + dc
        if 0 <= y < n and 0 <= x < n and b[y][x] == other:
            g = group_of(b, y, x)
            if len(g[1]) == 0:
                for s in g[0]:
                    b[s[0]][s[1]] = '.'
                    captured += 1
    g = group_of(b, r, c)
    if len(g[1]) == 0:
        return [[], 0]
    return [[''.join(row) for row in b], captured]
""", [[["XO...", "O....", ".....", ".....", "....."], 0, 2, 'O'], [["XO...", "O....", ".....", ".....", "....."], 1, 1, 'X'], [["XO...", ".....", ".....", ".....", "....."], 1, 0, 'O'], [[".O...", "O.O..", ".O...", ".....", "....."], 1, 1, 'X'], [["XX...", "XO...", ".XO..", "..X..", "....."], 2, 1, 'O'], [[".X...", "X.X..", ".X...", ".....", "....."], 1, 1, 'O']], "Place the stone, check the opponent's neighbouring groups first, then your own."),
  PL("Area score", "Under Chinese area scoring a player's score is the number of their stones plus the empty points in regions bordered only by their stones. Write area_score(board, komi): return [black, white, black - white - komi] where black and white are the areas. Empty regions bordered by both colours (or none) count for nobody.",
     "area_score(board, komi)", """
def area_score(board, komi):
    n = len(board)
    black = 0
    white = 0
    seen = []
    for r in range(n):
        for c in range(n):
            ch = board[r][c]
            if ch == 'X':
                black += 1
            elif ch == 'O':
                white += 1
            elif [r, c] not in seen:
                region = [[r, c]]
                seen.append([r, c])
                stack = [[r, c]]
                touch = []
                while stack:
                    p = stack.pop()
                    for dr, dc in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                        y = p[0] + dr
                        x = p[1] + dc
                        if 0 <= y < n and 0 <= x < n:
                            q = board[y][x]
                            if q == '.':
                                if [y, x] not in seen:
                                    seen.append([y, x])
                                    region.append([y, x])
                                    stack.append([y, x])
                            elif q not in touch:
                                touch.append(q)
                if touch == ['X']:
                    black += len(region)
                elif touch == ['O']:
                    white += len(region)
    return [black, white, black - white - komi]
""", [[["XX.OO", "XX.OO", "XX.OO", "XX.OO", "XX.OO"], 0.5], [["XXXXX", "X...X", "X.O.X", "X...X", "XXXXX"], 2.5], [["XX...", "XX...", ".....", "...OO", "...OO"], 7.5], [[".....", ".....", ".....", ".....", "....."], 1.5], [["XO", ".."], 0.5]], "Count stones directly; flood-fill each empty region and record which colours touch it.", approx=1e-9),
  PL("How big is the tree?", "Write log10_tree(b, d): d times the base-10 logarithm of b, rounded to 1 decimal place (the exponent of b to the power d). Use import math.",
     "log10_tree(b, d)", """
import math
def log10_tree(b, d):
    return round(d * math.log10(b), 1)
""", [[35, 80], [250, 150], [2, 10], [10, 5]], "d * log10(b), then round to one decimal."),
  ORDER("Capturing", "Put the steps of a capture in order.", ["A player places a stone", "Look at each adjacent enemy group", "Count its liberties", "Remove groups with zero liberties", "Check that your own group still has a liberty"]),
  FILL("Rules", "A group with no {{liberties}} is captured. The {{ko}} rule forbids repeating a position. White receives {{komi}} because Black moves first.")]))

# ------------------------------------------------------------ 3
CHS.append(CH(
 "Before AlphaGo: search and Monte Carlo",
 ("Computer Go", [
  "Alpha-beta search | works for | Chess",
  "Hand-written evaluation | fails for | Go",
  "Monte Carlo rollouts | estimate | Position value",
  "MCTS | grows | Search tree",
  "UCT | balances | Exploration and exploitation",
  "Crazy Stone and Zen | used | MCTS",
  "Pachi | was | Open-source MCTS program"]),
 ["Chess programs search deeply with alpha-beta and a hand-written evaluation. In Go that approach stalled: the tree is too wide and no one could write a good evaluation. Programs stayed weak amateurs.",
  "Progress came from Monte Carlo methods. To judge a position, play many random games from it and count the wins. Monte Carlo tree search builds a tree and spends more simulations on moves that look promising, with a bandit rule such as UCT choosing which to explore.",
  "By 2015 the strongest programs, such as Crazy Stone and Zen, used MCTS and reached strong amateur level. AlphaGo's contribution was to guide that search with learned networks."],
 [("Alpha-beta search", "A pruned minimax search used by chess engines."),
  ("Rollout", "A game played to the end, usually with fast or random moves, to estimate a position's value."),
  ("Monte Carlo", "Estimating by random sampling."),
  ("UCB1 and UCT", "A bandit rule adding an exploration bonus, applied to tree search."),
  ("Win rate", "Wins divided by simulations."),
  ("Pachi", "An open-source Monte Carlo Go program ranked about two amateur dan in the paper.")],
 ["Hand-written evaluation functions for Go never reached strong play.",
  "Monte Carlo rollouts estimate a position by the win rate of random games played from it.",
  "MCTS repeats selection, expansion, simulation and backup.",
  "UCT selects the child with the best average plus an exploration bonus that shrinks with visits.",
  "The strongest programs before AlphaGo reached about five-dan amateur level.",
  "Rollouts are noisy and need many simulations."],
 [T("For Go, the classical recipe failed. Alpha-beta search needs an evaluation to apply when it stops. In chess a short list of features gives a decent one. In Go no one managed to hand-write an evaluation that worked, and the branching factor of two hundred and fifty means the search cannot go deep anyway. For many years the best programs played at weak amateur level."),
  T("The first breakthrough around 2006 was to give up on evaluation functions and estimate value by sampling. To judge a position, play many games from it using fast random or lightly guided moves until the end, and count how often each side wins. This is a Monte Carlo rollout. With enough rollouts the win rate is a usable measure, even though each random game is a poor player."),
  T("The next step was to apply the sampling inside a tree. Monte Carlo tree search starts with just the current position as the root. Each simulation does four things. It selects a path down the existing tree. It expands a new node at the end of the path. It plays a rollout from the new node to the end of the game. It backs up the result, updating win counts along the path. As simulations accumulate, the tree grows deeper along promising lines."),
  T("How to select? Treat each choice of move at a node as a slot machine arm. The UCB1 rule from the multi-armed bandit literature picks the arm with the best average reward plus a bonus that grows with the logarithm of the total plays and shrinks with the arm's own plays. Applying this rule at every node of the tree is the UCT algorithm of Kocsis and Szepesvari. The dates and names here are my background knowledge, and the Nature paper cites this work."),
  M(r"a = \arg\max_a \left[\, \frac{W_a}{N_a} + c\,\sqrt{\frac{\ln N}{N_a}} \,\right]"),
  T("By the time of the paper, the strongest open-source program, Pachi, which uses 100,000 simulations per move, was ranked at two amateur dan. Programs such as Crazy Stone and Zen were stronger. Yet even the best ones could not beat a professional without a handicap, a gap of many levels."),
  T("Rollouts have a hidden weakness. A random game is not like a real game, so its result can mislead: a position that looks equal to random play may be lost against good play. The remedy used by strong programs was to make rollouts smarter with local patterns. AlphaGo keeps rollouts, with a small linear policy, but mixes them with a learned value, as chapter 9 shows."),
  T("The practice section builds the UCB score and a flat Monte Carlo evaluator on a simple stone-taking game, with a tiny deterministic random generator so that results are reproducible.")],
 [("What do rollouts estimate?", ["The value of a position", "The board size", "The komi", "The rules"], 0, "By the win rate of sampled games."),
  ("What does the UCB bonus do as a move is tried more?", ["It shrinks", "It grows", "It stays fixed", "It flips sign"], 0, "The count is in the denominator."),
  ("Which was an MCTS Go program?", ["Pachi", "Deep Blue", "Stockfish", "Elmo"], 0, "An open-source MCTS program."),
  ("What are the four phases of MCTS?", ["Selection, expansion, simulation, backup", "Read, write, run, halt", "Train, test, deploy, repeat", "Shuffle, deal, bid, play"], 0, "Walk down, add, play out, update.")],
 [("What is a rollout?", "A game played to the end to estimate value."), ("What is UCT?", "UCB applied at each node of the tree."), ("Why not alpha-beta for Go?", "Too wide and no good evaluation."),
  ("What was the pre-AlphaGo level?", "About amateur five dan.")],
 [PL("UCB score", "Write ucb(wins, plays, total, c): wins / plays + c * sqrt(ln(total) / plays). Use import math. If plays is 0 return 1000000.0.",
     "ucb(wins, plays, total, c)", """
import math
def ucb(wins, plays, total, c):
    if plays == 0:
        return 1000000.0
    return wins / plays + c * math.sqrt(math.log(total) / plays)
""", [[3, 10, 100, 1.0], [0, 0, 50, 1.0], [7, 8, 1000, 0.5], [1, 20, 21, 2.0], [5, 5, 5, 1.0]], "Return a huge value for untried moves so they are tried first.", approx=1e-9),
  PL("Flat Monte Carlo on a stone game", "Players alternately take 1, 2 or 3 stones from a pile; whoever takes the last stone wins. Random playouts use a generator x = (75 * x + 74) % 65537, starting from seed; to choose among k legal moves use x % k (moves in ascending order). Write flat_mc(stones, playouts, seed): for each first move m = 1..min(3, stones) in order, play playouts random games (the opponent moves next after m) and count the wins of the player who made move m; the generator state carries over between games. Return the list of win counts.",
     "flat_mc(stones, playouts, seed)", """
def flat_mc(stones, playouts, seed):
    x = seed
    wins = []
    for m in range(1, min(3, stones) + 1):
        w = 0
        for g in range(playouts):
            left = stones - m
            me_to_move = False
            if left == 0:
                w += 1
                continue
            while True:
                k = min(3, left)
                x = (75 * x + 74) % 65537
                take = 1 + x % k
                left -= take
                if left == 0:
                    if me_to_move:
                        w += 1
                    break
                me_to_move = not me_to_move
        wins.append(w)
    return wins
""", [[5, 20, 1], [4, 30, 7], [10, 25, 3], [2, 10, 5], [7, 40, 11]], "Track whose turn it is; the player who takes the last stone wins."),
  PL("Pick the best move", "Write best_move(wins): the 1-based index (the number of stones to take) of the largest win count; ties go to the smaller move.",
     "best_move(wins)", """
def best_move(wins):
    best = -1
    arg = 1
    for i in range(len(wins)):
        if wins[i] > best:
            best = wins[i]
            arg = i + 1
    return arg
""", [[[3, 9, 4]], [[5, 5, 5]], [[0]], [[1, 2, 8, 8]], [[7, 6]]], "Scan the list, remembering the first maximum."),
  ORDER("One MCTS simulation", "Order the phases.", ["Select a path through the tree", "Expand a new node", "Play a rollout to the end of the game", "Score the result", "Back the result up the path"]),
  MATCH("Terms", "Match each term with its meaning.", [("Rollout", "A sampled game to the end"), ("UCB", "Mean plus exploration bonus"), ("UCT", "UCB inside tree search"), ("Alpha-beta", "Pruned minimax"), ("Win rate", "Wins over simulations")]),
  FILL("Monte Carlo", "A {{rollout}} plays a game to the end. {{UCT|UCB}} adds an exploration bonus that shrinks as a move is tried more. Even the best Monte Carlo programs could not beat a {{professional}} without a handicap.")]))

# ------------------------------------------------------------ 4
CHS.append(CH(
 "Looking at the board: features and policy networks",
 ("Inputs and outputs", [
  "Board | becomes | Feature planes",
  "Policy network | takes | 48 planes of 19 by 19",
  "Convolutional layers | build | Position representation",
  "Softmax | outputs | Move probabilities",
  "Legal mask | removes | Illegal moves",
  "Value network | adds | Colour plane",
  "Temperature | sharpens or flattens | Probabilities"]),
 ["A neural network cannot read a board directly. AlphaGo turns each position into a stack of 19 by 19 binary planes: where the black, white and empty stones are, how recently each move was played, how many liberties each group has, and so on. The paper lists 48 such planes.",
  "A convolutional network turns the planes into a probability for every point of the board. A final softmax makes the numbers positive and sum to one. Illegal moves are given probability zero by a mask before the numbers are renormalized.",
  "This chapter builds the encodings and the softmax in code. The training comes in the next chapters."],
 [("Feature plane", "A 19 by 19 grid of zeros and ones describing one property of the position."),
  ("Convolutional network", "A network whose layers apply the same small filters at every board position."),
  ("Softmax", "Turns scores into probabilities: exp(z_i) divided by the sum of exp(z_j)."),
  ("Legal mask", "Setting illegal moves to probability zero and renormalizing."),
  ("Liberties plane", "Binary planes marking groups with 1, 2, 3 and so on liberties."),
  ("Temperature", "An exponent applied to probabilities to sharpen or flatten the distribution.")],
 ["The policy network input is 48 binary 19 by 19 planes; the value network adds a plane for the player's colour.",
  "Planes include stone colour (3), turns since a move was played (8), liberties (8), capture size (8), self-atari size (8), liberties after move (8), ladder capture and escape, and sensibleness.",
  "The output is a probability for each of 361 points.",
  "Softmax: p_i = exp(z_i) / sum_j exp(z_j).",
  "Illegal moves are masked out and the rest renormalized.",
  "In search, the paper uses a softmax temperature of 0.67 on the SL policy network for priors."],
 [T("Think of a photograph. A photograph has three colour channels, each a grid of numbers. AlphaGo treats a Go position the same way. The board is a nineteen by nineteen image with many channels, and each channel is a yes-or-no map of one fact about the position."),
  T("The paper's list, in its Extended Data tables, has forty-eight planes for the policy network. Three planes give stone colour: points with the player's stones, the opponent's stones, and empty points. One plane is all ones. Eight planes record how many turns ago each stone was played. Eight record how many liberties each group has. Others mark how many stones a move would capture, how many stones a move would put in atari, how many liberties a stone would have after it is played, and whether a ladder would capture or escape. One marks moves that are sensible. The value network adds a plane for whose turn it is."),
  T("Why features instead of the raw board alone? The paper reports that using only the raw board position and the move history, the network reached 55.7 percent accuracy at predicting expert moves, against 57.0 percent with all features. The extra planes help a little, as hand-written knowledge about liberties and ladders saves the network from having to discover them."),
  T("The network is a stack of convolutional layers, thirteen for the SL policy network. Each layer applies small filters, with rectifier nonlinearities between them. The final layer produces one score for each of the 361 points. A softmax turns the scores into probabilities."),
  M(r"p_i \;=\; \frac{e^{z_i}}{\sum_j e^{z_j}}"),
  T("Not all of the 361 points are legal. Some are occupied and some break the ko or suicide rules. The search should never consider them. A legal mask sets the probability of illegal points to zero and divides the rest by their total, so the result still sums to one."),
  T("One more knob: the temperature. If every probability is raised to a power below one and the result renormalized, the distribution flattens and makes rare moves more likely. The paper applies a softmax temperature of 0.67 to the SL policy network when it produces priors for the tree search, to spread the search over more candidate moves. The exact transformation used in the practice section is my own simple version of the idea."),
  T("In the practice section you write the softmax, the legal mask, three stone planes and the temperature operation.")],
 [("How many input planes does the policy network use?", ["48", "3", "361", "8"], 0, "Each is a 19 by 19 binary map."),
  ("What does softmax guarantee?", ["Positive numbers that sum to 1", "A single winner", "Integer outputs", "Legal moves only"], 0, "Probabilities."),
  ("Why mask illegal moves?", ["They must never be chosen", "To save memory", "To flip colours", "To raise the temperature"], 0, "Then renormalize."),
  ("What accuracy did raw board plus history alone reach?", ["55.7 percent", "100 percent", "10 percent", "24.2 percent"], 0, "Against 57.0 percent with all features.")],
 [("What does a plane hold?", "Zeros and ones for one fact about the board."), ("What is the output size?", "361 move probabilities."), ("What does temperature below 1 do here?", "Flattens the distribution."),
  ("What does the value network add?", "A colour-to-move plane.")],
 [PL("Softmax", "Write softmax(z): the list of exp(z_i) / sum of exp(z_j). Subtract the maximum first for numerical safety. Use import math.",
     "softmax(z)", """
import math
def softmax(z):
    m = max(z)
    e = [math.exp(x - m) for x in z]
    s = sum(e)
    return [x / s for x in e]
""", [[[0.0, 0.0]], [[1.0, 2.0, 3.0]], [[10.0, 0.0]], [[-1.0, -1.0, -1.0, -1.0]], [[0.5]]], "Exponentiate the shifted scores and divide by their sum.", approx=1e-9),
  PL("Mask illegal moves", "Write masked(p, legal): legal is a list of 0/1 flags. Zero the probability of illegal moves and renormalize the rest so they sum to 1. If nothing is legal return the zeros.",
     "masked(p, legal)", """
def masked(p, legal):
    q = [a * b for a, b in zip(p, legal)]
    s = sum(q)
    if s == 0:
        return q
    return [x / s for x in q]
""", [[[0.5, 0.3, 0.2], [1, 0, 1]], [[0.25, 0.25, 0.25, 0.25], [0, 0, 1, 1]], [[0.6, 0.4], [0, 0]], [[0.1, 0.9], [1, 1]], [[1.0], [1]]], "Multiply by the flags, then divide by the new total.", approx=1e-9),
  PL("Stone planes", "A board is a list of strings of 'X', 'O' and '.'. Write stone_planes(board, me): return three flat lists (row by row): 1 where my stones are, 1 where the opponent's are, 1 where empty. me is 'X' or 'O'. Return [mine, theirs, empty].",
     "stone_planes(board, me)", """
def stone_planes(board, me):
    mine = []
    theirs = []
    empty = []
    for row in board:
        for ch in row:
            mine.append(1 if ch == me else 0)
            if ch == '.':
                theirs.append(0)
                empty.append(1)
            else:
                theirs.append(0 if ch == me else 1)
                empty.append(0)
    return [mine, theirs, empty]
""", [[["X.", ".O"], "X"], [["X.", ".O"], "O"], [["...", "...", "..."], "X"], [["XO", "OX"], "O"]], "Loop over the characters row by row."),
  PL("Flatten the distribution", "Write temper(p, beta): raise each probability to the power beta, renormalize and round each result to 9 decimals. (A beta below 1 flattens; above 1 sharpens.)",
     "temper(p, beta)", """
def temper(p, beta):
    q = [x ** beta for x in p]
    s = sum(q)
    return [round(x / s, 9) for x in q]
""", [[[0.7, 0.2, 0.1], 0.67], [[0.7, 0.2, 0.1], 1.0], [[0.7, 0.2, 0.1], 2.0], [[0.5, 0.5], 0.3], [[1.0], 0.5]], "Use the ** operator, then divide by the sum.", approx=1e-9),
  ORDER("From board to move", "Order the steps of the policy network.", ["Encode the board as feature planes", "Apply the convolutional layers", "Produce a score for each point", "Apply the softmax", "Mask illegal points and renormalize"]),
  MATCH("Planes", "Match each plane group with its content.", [("Stone colour", "Mine, theirs, empty"), ("Liberties", "Number of liberties of each group"), ("Turns since", "How long ago a stone was played"), ("Ladder", "Whether a ladder captures or escapes"), ("Colour to play", "Added for the value network")]),
  FILL("Policy", "The policy network takes {{48}} planes and ends with a {{softmax}}. Illegal moves are removed by a {{mask|legal mask}} and the rest renormalized.")]))
