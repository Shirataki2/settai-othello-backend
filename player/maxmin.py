from copy import deepcopy
import game
from board import Board
import numpy as np


class MaxminPlayer:
    inf = float("inf")

    def __init__(self, color):
        self.color = color
        self.name = "MaxMin"

    def next_move(self, board, color, depth=2):
        if game.validate(board, color, 'pass'):
            return "pass"
        mov, val = self.max_val(board, -self.inf, self.inf, depth, color)
        return mov

    def get_valid_pos(self):
        moves = []
        for y in range(8):
            for x in range(8):
                if game.validate(self._board, self._color, [x, y]):
                    moves.append([x, y])
        return moves

    def get_successors(self, poslist):
        if self._color == "B":
            idx = 0
        elif self._color:
            idx = 1
        suclist = []
        before_score = game.score(self._board)
        for pos in poslist:
            nb = deepcopy(self._board)
            game.do_move(nb, self._color, pos)
            after_score = game.score(nb)
            suclist.append([pos, nb, after_score[idx] - before_score[idx] - 1])
        return suclist

    def get_best_position(self, suclist):
        suclist = np.array(suclist)
        max_gain = suclist[:, 2].max()
        bps = []
        for mov, state, gain in suclist:
            if gain == max_gain:
                bps.append(mov)
        return bps

    def end_state(self, state):
        return game.validate(state, "B", "pass") and game.validate(state, "W", "pass")

    def max_val(self, state, alpha, beta, depth, color, rev=False):
        if self.end_state(state):
            return None, self.utility(state, color)
        elif depth == 0:
            return None, self.evaluate(state, color)
        best = None
        v = -self.inf
        if not rev:
            moves = self.successors(state, color)
        else:
            moves = self.successors(state, game.opponent(color))
        for mov, state in moves:
            val = self.min_val(state, alpha, beta, depth - 1, color, rev)[1]
            if best is None or val > v:
                best = mov
                v = val
            if v >= beta:
                return best, v
            alpha = max(alpha, v)
        return best, v

    def min_val(self, state, alpha, beta, depth, color, rev=False):
        if self.end_state(state):
            return None, self.utility(state, color)
        elif depth == 0:
            return None, self.evaluate(state, color)
        best = None
        v = self.inf
        if rev:
            moves = self.successors(state, color)
        else:
            moves = self.successors(state, game.opponent(color))
        for mov, state in moves:
            val = self.max_val(state, alpha, beta, depth - 1, color, rev)[1]
            if best is None or val < v:
                best = mov
                v = val
            if v <= alpha:
                return best, v
            beta = min(beta, v)
        return best, v

    def successors(self, state, color):
        suclist = []
        movs = []
        for y in range(8):
            for x in range(8):
                if game.validate(state, color, [x, y]):
                    movs.append([x, y])
        for mov in movs:
            nb = deepcopy(state)
            game.do_move(nb, color, mov)
            suclist.append([mov, nb])
        return suclist

    def utility(self, state, color):
        s = Board(state).score()
        ans = 0
        if s[0] == s[1]:
            ans = 0
        elif s[0] < s[1] and color == "W":
            ans = self.inf
        elif s[0] > s[1] and color == "B":
            ans = self.inf
        else:
            ans = -self.inf
        return ans

    def evaluate(self, state, color):
        W = np.array(
            [
                [99, 4,  8,  6,  6,  8, 4, 99],
                [4, -24, -4, -3, -3, -4, -24, 4],
                [8, -4,  7,  4,  4,  7, -4,  8],
                [6, -3,  4,  0,  0,  4, -3,  6],
                [6, -3,  4,  0,  0,  4, -3,  6],
                [8, -4,  7,  4,  4,  7, -4,  8],
                [4, -24, -4, -3, -3, -4, -24, 4],
                [99, 4,  8,  6,  6,  8, 4, 99],
            ]
        )
        X = np.array(state)
        Y = np.zeros_like(X, dtype=int)
        Y[X == color] = 1
        Y[X == game.opponent(color)] = -1
        score = int((Y * W).sum())
        return -score

    def get_game_result(self, board_data, game_ended=False, opponent=None):
        pass
