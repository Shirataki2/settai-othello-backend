from copy import deepcopy
import game
from board import Board
import numpy as np


class MaxminPlayer:
    inf = float("inf")

    def __init__(self, color):
        self.color = color
        self.name = "MaxMin"

    def next_move(self, board, color, depth=2, W=None, w=None):
        if game.validate(board, color, 'pass'):
            return "pass"
        mov, val = self.max_val(
            board, -self.inf, self.inf, depth, color, W=W, w=w)
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

    def max_val(self, state, alpha, beta, depth, color, rev=False, W=None, w=None):
        if self.end_state(state):
            return None, self.utility(state, color)
        elif depth == 0:
            return None, self.evaluate(state, color, W=W, w=w)
        best = None
        v = -self.inf
        if not rev:
            moves = self.successors(state, color)
        else:
            moves = self.successors(state, game.opponent(color))
        for mov, state in moves:
            val = self.min_val(state, alpha, beta, depth -
                               1, color, rev, W=W, w=w)[1]
            if best is None or val > v:
                best = mov
                v = val
            if v >= beta:
                return best, v
            alpha = max(alpha, v)
        return best, v

    def min_val(self, state, alpha, beta, depth, color, rev=False, W=None, w=None):
        if self.end_state(state):
            return None, self.utility(state, color)
        elif depth == 0:
            return None, self.evaluate(state, color, W=W, w=w)
        best = None
        v = self.inf
        if rev:
            moves = self.successors(state, color)
        else:
            moves = self.successors(state, game.opponent(color))
        for mov, state in moves:
            val = self.max_val(state, alpha, beta, depth -
                               1, color, rev, W=W, w=w)[1]
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

    def evaluate(self, state, color, W=None, w=None):
        if not W:
            W = np.array(
                [
                    [70, -12,  0,  -1,  -1,  0, -12, 70],
                    [-12, -15, -3, -3, -3, -3, -15, -12],
                    [0, -3,  0,  -1,  -1,  0, -3,  0],
                    [-1, -3,  -1,  -1,  -1,  -1, -3,  -1],
                    [-1, -3,  -1,  -1,  -1,  -1, -3,  -1],
                    [0, -3,  0,  -1,  -1,  0, -3,  0],
                    [-12, -15, -3, -3, -3, -3, -15, -12],
                    [70, -12,  0,  -1,  -1,  0, -12, 70],
                ]
            )
        if not w:
            w = [3, 1, 1, 5, 1, 1, 1, -1]
        f_11, f_12, f_13, f_21, f_22, f_23, w_1, w_2 = w
        X = np.array(state)
        Y = np.zeros_like(X, dtype=int)
        Y[X == color] = w_1
        Y[X == game.opponent(color)] = w_2
        score = int((Y * W).sum())
        vp = int(f_21) * (int(f_22) * len(Board(state).valid_pos(self)) -
                          int(f_23) * len(Board(state).valid_pos(MaxminPlayer(game.opponent(color)))))
        dif = int(f_11) * (int(f_12) * np.bincount((X == color).ravel())[1] -
                           int(f_13) * np.bincount((X == game.opponent(color)).ravel())[1])
        score += vp + dif
        return -score

    def get_game_result(self, board_data, game_ended=False, opponent=None):
        pass
