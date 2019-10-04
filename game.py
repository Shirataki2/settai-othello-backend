import argparse


def opponent(x: str) -> str:
    if x.lower() == 'b':
        return 'W'
    elif x.lower() == 'w':
        return 'B'
    else:
        return '.'


def vaild_position(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8


def can_flip(board, color: str, pos: [int, int], dirction: [int, int]):
    cX, cY = pos[0] + dirction[0], pos[1] + dirction[1]
    if not vaild_position(cX, cY):
        return False
    if board[cX][cY] != opponent(color):
        return False
    while True:
        cX, cY = cX + dirction[0], cY + dirction[1]
        if not vaild_position(cX, cY):
            return False
        if board[cX][cY] == color:
            return True
        if board[cX][cY] == '.':
            return False


def validate_move(board, color: str, pos: [int, int]) -> bool:
    if board[pos[0]][pos[1]] != '.':
        return False
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx != 0 or dy != 0:
                if can_flip(board, color, pos, [dx, dy]):
                    return True
    return False


def validate(board, color, move):
    if move == "pass":
        for y in range(8):
            for x in range(8):
                if validate_move(board, color, [x, y]):
                    return False
        return True
    else:
        return validate_move(board, color, move)


def do_flip(board, color, pos, direction):
    cX, cY = pos[0] + direction[0], pos[1] + direction[1]
    while board[cX][cY] == opponent(color):
        board[cX][cY] = color
        cX, cY = cX + direction[0], cY + direction[1]


def do_move(board, color, pos):
    if pos != 'pass':
        if validate_move(board, color, pos):
            board[pos[0]][pos[1]] = color
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx != 0 or dy != 0:
                        if can_flip(board, color, pos, [dx, dy]):
                            do_flip(board, color, pos, [dx, dy])


def create_board():
    import numpy as np
    res = np.array([['.'] * 8] * 8)
    res[3][3] = 'B'
    res[4][4] = 'B'
    res[4][3] = 'W'
    res[3][4] = 'W'
    return res.tolist()


def get_player_instance(name, color, depth=1):
    from player.random import RandomPlayer
    from player.minmax import MinmaxPlayer
    from player.maxmin import MaxminPlayer
    from player.qlearn import QLearningPlayer

    if name == "random":
        return RandomPlayer(color)
    if name == "minmax":
        return MinmaxPlayer(color)
    if name == "maxmin":
        return MaxminPlayer(color)
    if name == "qlearn":
        return QLearningPlayer(color)
    return RandomPlayer(color)


if __name__ == "__main__":
    from player.qlearn import QLearningPlayer
    verbose = False
    ct = 320.
    rev = ""
    parser = argparse.ArgumentParser()
    parser.add_argument("--p1", default="qlearn", type=str)
    parser.add_argument("--p2", default="random", type=str)
    args = parser.parse_args()
    p1 = get_player_instance(args.p1, "B")
    p2 = get_player_instance(args.p2, "W")
    from trainer import Trainer
    trainer = Trainer(False, False, 300)
    trainer.play(p1, p2, verbose, ct)
    if isinstance(p1, QLearningPlayer):
        import pickle
        with open("q.pickle", "wb") as f:
            pickle.dump(p1.q._values, f)
