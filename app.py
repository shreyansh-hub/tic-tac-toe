from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

board = [' ' for _ in range(9)]
current_player = 'X'
game_mode = 'human'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    global current_player, game_mode
    data = request.json
    position = int(data['position'])
    game_mode = data['gameMode']
    
    if board[position] == ' ':
        board[position] = current_player
        winner = check_winner()
        
        if winner:
            result = f'Player {winner} wins!'
        elif ' ' not in board:
            result = 'It\'s a tie!'
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            result = f'Player {current_player}\'s turn'
            
            if game_mode == 'computer' and current_player == 'O':
                computer_move = make_computer_move()
                board[computer_move] = 'O'
                winner = check_winner()
                if winner:
                    result = 'Computer wins!'
                elif ' ' not in board:
                    result = 'It\'s a tie!'
                else:
                    current_player = 'X'
                    result = 'Your turn'
        
        return jsonify({'board': board, 'result': result})
    else:
        return jsonify({'error': 'Invalid move'}), 400

def check_winner():
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    return None

def make_computer_move():
    empty_cells = [i for i, cell in enumerate(board) if cell == ' ']
    return random.choice(empty_cells)

@app.route('/reset', methods=['POST'])
def reset_game():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    return jsonify({'board': board, 'result': 'Player X\'s turn'})

if __name__ == '__main__':
    app.run(debug=True)