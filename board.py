from game import validate


class Board:
    def __init__(self, board_data):
        self.board_data = board_data

    def show(self, qp=None):
        print("   " + "  ".join(map(chr, range(ord('A'), ord('H') + 1))))
        for (x, y) in zip(range(8), self.board_data):
            row = y
            if qp is not None:
                row = []
                for i, piece in enumerate(y):
                    pos = self.valid_pos(qp)
                    if piece == '.' and (x, i) in pos:
                        piece = qp.q.get(tuple(self.flattened_data(), (x, i)))
                        piece = round(piece, 2)
                    row.append(str(piece))
            y_str = "  ".join(row)
            print(str(x) + "  " + y_str)

    def valid_pos(self, player):
        moves = []
        for y in range(8):
            for x in range(8):
                if validate(self.board_data, player.color, [x, y]):
                    moves.append([x, y])
        return moves

    def flattened_data(self):
        return tuple([flatten for inner in self.board_data for flatten in inner])

    def is_game_over(self):
        return validate(self.board_data, "B", 'pass') and validate(self.board_data, "W", 'pass')

    def score(self):
        board = self.flattened_data()
        nb, nw = board.count("B"), board.count("W")
        return nb, nw
