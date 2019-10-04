import random
from board import Board
from game import validate


class RandomPlayer:
    def __init__(self, color):
        self.color = color
        self.name = "Random"

    def next_move(self, board_data, color):
        board = Board(board_data)
        pos = board.valid_pos(self)
        if len(pos) == 0:
            return "pass"
        selected_move = random.choice(pos)
        return selected_move

    def next_move_r(self, board_data, color, time):
        return self.next_move(board_data, color)

    def get_game_result(self, board_data, game_ended=False, opponent=None):
        pass
