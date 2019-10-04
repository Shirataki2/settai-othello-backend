from copy import deepcopy, copy
import game
from board import Board
import numpy as np
import random


class Q:
    def __init__(self, alpha, gamma, initial_q=1):
        self._initial_q = initial_q
        self._values = {}
        self.alpha = alpha
        self.gamma = gamma

    def get(self, state, act):
        act = tuple(act)
        v = self._values.get((state, act))
        if v is None:
            return self._initial_q
        return v

    def set(self, s, a, q):
        self._values[s, a] = q

    def update(self, s, a, r, mq):
        a = tuple(a)
        pQ = self.get(s, a)
        nq = pQ + self.alpha * ((r + self.gamma * mq) - pQ)
        self.set(s, a, nq)


class NaivePlayer:
    def __init__(self, color):
        self.color = color
        self.name = "Naive"

    def next_move(self, board, color):
        b = Board(board)
        pos = b.valid_pos(self)
        if len(pos) == 0:
            return "pass"
        for y in range(8):
            for x in range(8):
                if (y, x) in pos:
                    return y, x

    def next_move_r(self, board, color):
        return self.next_move(board, color)

    def get_game_result(self, board_data, game_ended=False, opponent=None):
        pass


class QLearningPlayer:
    def __init__(self, color, e=.4, alpha=.3):
        self.color = color
        self.name = "QLearn"
        self.q = Q(alpha, .9)
        self.nqs = []
        self.e = e
        self.act_ctr = 0
        self.last_board = None
        self.last_move = None

    def next_move(self, board, color):
        return self.policy(board, color)

    def policy(self, board, color):
        self.last_board = Board(board.copy())
        b = Board(board)
        poslist = b.valid_pos(self)
        if len(poslist) == 0:
            return "pass"
        if random.random() < self.e * 0.99999 ** float(self.act_ctr):
            return random.choice(poslist)
        else:
            qs = []
            for pos in poslist:
                qs.append(self.q.get(
                    tuple(self.last_board.flattened_data()), pos)
                )
            mq = max(qs)
            if qs.count(mq) > 1:
                best_actions = [i for i in range(len(poslist)) if qs[i] == mq]
                i = random.choice(best_actions)
            else:
                i = qs.index(mq)
            m = poslist[i]
        self.last_move = m
        return m

    def get_game_result(self, board_data, game_ended=False, opponent=None):
        b = Board(deepcopy(board_data))
        act = opponent.next_move(b.board_data, opponent.color)
        game.do_move(b.board_data, opponent.color, act)
        is_over = b.is_game_over()
        r = 0
        if is_over:
            tmp = b.board_data
            nb, nw = tmp.count("B"), tmp.count("W")
            is_bwin = nb > nw
            is_wwin = nb < nw
            is_draw = nb == nw
            if is_draw:
                r = 0
            elif self.color == "B":
                r = 1 if is_bwin else -1
            elif self.color == "W":
                r = 1 if is_wwin else -1
        if self.last_move != None:
            self.learn(self.last_board, self.last_move, r, b, is_over)
        if not is_over:
            self.act_ctr += 1
            self.last_move = None
            self.last_board = None

    def learn(self, s, a, r, fs, game_ended):
        flat = s.flattened_data()
        qli = []
        for pos in fs.valid_pos(self):
            qli.append(self.q.get(fs.flattened_data(), tuple(pos)))
        if game_ended or len(qli) == 0:
            mq_new = 0
        else:
            mq_new = max(qli)
        self.q.update(tuple(flat), a, r, mq_new)
