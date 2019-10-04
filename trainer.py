import random
import time
import tqdm
from copy import deepcopy

from board import Board
from game import create_board, validate, do_move
from player.qlearn import QLearningPlayer


class Trainer:
    def __init__(self, show_board=True, show_result=True, n_play=1, stat=100, debug=False):
        self._show_board = show_board
        self._show_result = show_result
        self._nplay = n_play
        self._stat = stat
        self._debug = debug

    def play(self, p1, p2, verbose=False, t=128):
        ctr = [0, 0, 0]
        bar = tqdm.trange(self._nplay)
        _p1, _p2 = p1, p2
        for i in bar:
            (p2, p1) = (p1, p2)
            if self._show_board:
                print(f"P1: {p1.name}({p1.color}) | P2: {p2.name}({p2.color})")
            board = Board(create_board())
            p1t, p2t = t, t
            p1tr, p2tr = 2*t, 2*t
            while not board.is_game_over():
                tmp = deepcopy(board.board_data)
                t1 = time.time()
                next_move = p1.next_move(tmp, p1.color)
                t2 = time.time()
                p1t = p1t - (t2 - t1)
                p1tr = p1tr - (t2 - t1)
                if p1tr < 0:
                    if p1.color == "B":
                        return 0, 16, board.board_data, f"BAD move: {str(next_move)}"
                    else:
                        return 16, 0, board.board_data, f"BAD move: {str(next_move)}"
                if validate(board.board_data, p1.color, next_move):
                    do_move(board.board_data, p1.color, next_move)
                else:
                    if p1.color == 'B':
                        return 0, 16, board.board_data, f"BAD move: {str(next_move)}"
                    else:
                        return 16, 0, board.board_data, f"BAD move: {str(next_move)}"
                p1.get_game_result(board.board_data, opponent=p2)
                (p1, p2) = (p2, p1)
                (p1t, p2t) = (p2t, p1t)
                (p1tr, p2tr) = (p2tr, p1tr)
                if self._show_board:
                    if isinstance(p1, QLearningPlayer) and self._debug:
                        board.show(p1)
                    else:
                        board.show()
            res = board.score()
            if res[0] > res[1]:
                ctr[0] += 1
            elif res[0] < res[1]:
                ctr[1] += 1
            else:
                ctr[2] += 1
            bar.set_description(
                f"P1({_p1.name}): {ctr[0]}, P2({_p2.name}): {ctr[1]} DRAW: {ctr[2]}"
            )
            # if self._nplay > 1 and (i - 1) % self._stat == 0:
            #     print(
            #         f"Win(EPISODE: {i}): P1({p1.name}): {ctr[0]} | P2({p2.name}): {ctr[1]} DRAW: {ctr[2]}"
            #     )
        print(
            f"Episode Finished(N: {self._nplay}) P1({p1.name}): {ctr[0]}, P2({p2.name}): {ctr[1]},DRAW: {ctr[2]}"
        )
