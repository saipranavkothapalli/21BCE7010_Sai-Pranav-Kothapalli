from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app)

game_state = {
    'board': [['' for _ in range(5)] for _ in range(5)],
    'turn': 'Player1',
    'players': {
        'Player1': {'characters': ['A-P', 'A-P', 'A-H1', 'A-H2', 'A-P'], 'row': 0},
        'Player2': {'characters': ['B-P', 'B-P', 'B-H1', 'B-H2', 'B-P'], 'row': 4}
    }
}

def initialize_board():
    for i in range(5):
        game_state['board'][0][i] = game_state['players']['Player1']['characters'][i]
        game_state['board'][4][i] = game_state['players']['Player2']['characters'][i]

def switch_turn():
    game_state['turn'] = 'Player2' if game_state['turn'] == 'Player1' else 'Player1'

@app.route('/')
def index():
    return render_template('client.html')

@socketio.on('connect')
def handle_connect():
    initialize_board()
    emit('game_state', game_state)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'data': f'{game_state["turn"]}\'s turn'}, room=room)

@socketio.on('move')
@socketio.on('move')
def handle_move(data):
    room = data['room']
    move = data['move']
    current_player = game_state['turn']
    if move_piece(current_player, move):
        emit('update_board', game_state, room=room)
        switch_turn()
        emit('message', {'data': f'{game_state["turn"]}\'s turn'}, room=room)
        emit('move_made', {'move': move}, room=room)
    else:
        emit('message', {'data': 'Invalid move'}, room=room)


def move_piece(player, move):
    piece_type, direction = move['piece'], move['direction']
    start_pos = move['start_pos']
    opponent = 'Player2' if player == 'Player1' else 'Player1'

    print(f"Attempting to move {piece_type} in direction {direction} from {start_pos}")

    if piece_type.endswith('P'):
        return move_pawn(player, opponent, start_pos, direction)
    elif piece_type.endswith('H1'):
        return move_hero1(player, opponent, start_pos, direction)
    elif piece_type.endswith('H2'):
        return move_hero2(player, opponent, start_pos, direction)
    return False

def move_pawn(player, opponent, start_pos, direction):
    row, col = start_pos['row'], start_pos['col']
    new_row, new_col = row, col

    if direction == 'L':
        new_col -= 1
    elif direction == 'R':
        new_col += 1
    elif direction == 'F':
        new_row += 1 if player == 'Player1' else -1
    elif direction == 'B':
        new_row -= 1 if player == 'Player1' else +1

    print(f"Pawn move to ({new_row}, {new_col})")

    return update_board(player, opponent, row, col, new_row, new_col)

def move_hero1(player, opponent, start_pos, direction):
    row, col = start_pos['row'], start_pos['col']
    new_row, new_col = row, col

    if direction == 'L':
        new_col -= 2
    elif direction == 'R':
        new_col += 2
    elif direction == 'F':
        new_row += 2 if player == 'Player1' else -2
    elif direction == 'B':
        new_row -= 2 if player == 'Player1' else +2

    print(f"Hero1 move to ({new_row}, {new_col})")

    return update_board(player, opponent, row, col, new_row, new_col)

def move_hero2(player, opponent, start_pos, direction):
    row, col = start_pos['row'], start_pos['col']
    new_row, new_col = row, col

    if direction == 'FL':
        new_row += 2 if player == 'Player1' else -2
        new_col -= 2
    elif direction == 'FR':
        new_row += 2 if player == 'Player1' else -2
        new_col += 2
    elif direction == 'BL':
        new_row -= 2 if player == 'Player1' else +2
        new_col -= 2
    elif direction == 'BR':
        new_row -= 2 if player == 'Player1' else +2
        new_col += 2

    print(f"Hero2 move to ({new_row}, {new_col})")

    return update_board(player, opponent, row, col, new_row, new_col)

def update_board(player, opponent, row, col, new_row, new_col):
    if is_valid_move(new_row, new_col) and (game_state['board'][new_row][new_col] == '' or game_state['board'][new_row][new_col] in game_state['players'][opponent]['characters']):
        game_state['board'][new_row][new_col] = game_state['board'][row][col]
        game_state['board'][row][col] = ''
        print(f"Move successful: ({row}, {col}) to ({new_row}, {new_col})")
        return True
    print(f"Move invalid: ({new_row}, {new_col})")
    return False

def is_valid_move(row, col):
    return 0 <= row < 5 and 0 <= col < 5

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
