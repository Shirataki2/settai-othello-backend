from flask import Flask, jsonify, make_response, request, Response
from flask_cors import CORS
from copy import deepcopy

from game import get_player_instance
from board import Board
from game import create_board, validate, do_move

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Othello Backend Working"


@app.route('/eval', methods=["POST"])
def evaluate():
    data = request.get_json()
    b1 = data["board"]
    b2 = []
    for i in range(8):
        b2.append(list(b1[i*8:(i+1)*8]))
    mode = "maxmin" if data["mode"] == 'settai' else "minmax"
    depth = int(data["difficulty"]) * 2 - 1
    p = get_player_instance(mode, "B")
    b = Board(b2)
    b3 = deepcopy(b.board_data)
    vp = b.valid_pos(p)
    return jsonify({
        "put": vp
    })


@app.route('/put', methods=["POST"])
def put():
    data = request.get_json()
    b1 = data["board"]
    x = int(data["x"])
    y = int(data["y"])
    b2 = []
    for i in range(8):
        b2.append(list(b1[i*8:(i+1)*8]))
    mode = "maxmin" if data["mode"] == 'settai' else "minmax"
    depth = int(data["difficulty"]) * 2 - 1
    p = get_player_instance(mode, "B")
    q = get_player_instance(mode, "W")
    b = Board(b2)
    # PLAYER'S TURN
    if x >= 0:
        if validate(b.board_data, "B", [x, y]):
            do_move(b.board_data, "B", [x, y])
    plisult = deepcopy(b.board_data)
    nm = q.next_move(b.board_data, "W", depth)
    if validate(b.board_data, "W", nm):
        do_move(b.board_data, "W", nm)
    qlisult = b.board_data
    return jsonify({
        "player": plisult,
        "com": qlisult,
        "pos": nm
    })


if __name__ == "__main__":
    app.run("0.0.0.0", 9090, True)
