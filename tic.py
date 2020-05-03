import numpy as np
from math import inf as infinity

games = [[' ',' ',' '],
              [' ',' ',' '],
              [' ',' ',' ']]
players = ['X','O']

def moves_status(state, player, block):
    if state[int((block-1)/3)][(block-1)%3] is ' ':
        state[int((block-1)/3)][(block-1)%3] = player
    else:
        block = int(input("Block is not empty, ya blockhead! Choose again: "))
        moves_status(state, player, block)
    
def copy_game_status(state):
    new_state = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state
    
def check_current_state(games):
    # Check if draw
    flag = 0
    for i in range(3):
        for j in range(3):
            if games[i][j] is ' ':
                flag = 1
    if flag is 0:
        return None, "Draw"
    
    # Check horizontals
    if (games[0][0] == games[0][1] and games[0][1] == games[0][2] and games[0][0] is not ' '):
        return games[0][0], "Done"
    if (games[1][0] == games[1][1] and games[1][1] == games[1][2] and games[1][0] is not ' '):
        return games[1][0], "Done"
    if (games[2][0] == games[2][1] and games[2][1] == games[2][2] and games[2][0] is not ' '):
        return games[2][0], "Done"
    
    # Check verticals
    if (games[0][0] == games[1][0] and games[1][0] == games[2][0] and games[0][0] is not ' '):
        return games[0][0], "Done"
    if (games[0][1] == games[1][1] and games[1][1] == games[2][1] and games[0][1] is not ' '):
        return games[0][1], "Done"
    if (games[0][2] == games[1][2] and games[1][2] == games[2][2] and games[0][2] is not ' '):
        return games[0][2], "Done"
    
    # Check diagonals
    if (games[0][0] == games[1][1] and games[1][1] == games[2][2] and games[0][0] is not ' '):
        return games[1][1], "Done"
    if (games[2][0] == games[1][1] and games[1][1] == games[0][2] and games[2][0] is not ' '):
        return games[1][1], "Done"
    
    return None, "Not Done"

def board(games):
    print('----------------')
    print('| ' + str(games[0][0]) + ' || ' + str(games[0][1]) + ' || ' + str(games[0][2]) + ' |')
    print('----------------')
    print('| ' + str(games[1][0]) + ' || ' + str(games[1][1]) + ' || ' + str(games[1][2]) + ' |')
    print('----------------')
    print('| ' + str(games[2][0]) + ' || ' + str(games[2][1]) + ' || ' + str(games[2][2]) + ' |')
    print('----------------')
    
    
def Bestmove_minimax(state, player):
    '''
    Minimax Algorithm
    '''
    winner_loser , done = check_current_state(state)
    if done == "Done" and winner_loser == 'O': # If AI won
        return 1
    elif done == "Done" and winner_loser == 'X': # If Human won
        return -1
    elif done == "Draw":    # Draw condition
        return 0
        
    moves = []
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if state[i][j] is ' ':
                empty_cells.append(i*3 + (j+1))
    
    for empty_cell in empty_cells:
        move = {}
        move['index'] = empty_cell
        new_state = copy_game_status(state)
        moves_status(new_state, player, empty_cell)
        
        if player == 'O':    # If AI
            result = Bestmove_minimax(new_state, 'X')    # make more depth tree for human
            move['score'] = result
        else:
            result = Bestmove_minimax(new_state, 'O')    # make more depth tree for AI
            move['score'] = result
        
        moves.append(move)

    # Find best move
    best_move = None
    if player == 'O':   # If AI player
        best = -infinity
        for move in moves:
            if move['score'] > best:
                best = move['score']
                best_move = move['index']
    else:
        best = infinity
        for move in moves:
            if move['score'] < best:
                best = move['score']
                best_move = move['index']
                
    return best_move

# PLaying
play_again = 'Y'
while play_again == 'Y' or play_again == 'y':
    games = [[' ',' ',' '],
              [' ',' ',' '],
              [' ',' ',' ']]
    current_state = "Not Done"
    print("\nNew Game!")
    board(games)
    player_choice = input("Choose which player goes first - X (You - the petty human) or O(The mighty AI): ")
    winner = None
    
    if player_choice == 'X' or player_choice == 'x':
        current_player_idx = 0
    else:
        current_player_idx = 1
        
    while current_state == "Not Done":
        if current_player_idx == 0: # Human's turn
            block_choice = int(input("Oye, your turn! Choose where to place (1 to 9): "))
            moves_status(games ,players[current_player_idx], block_choice)
        else:   # AI's turn
            block_choice = Bestmove_minimax(games, players[current_player_idx])
            moves_status(games ,players[current_player_idx], block_choice)
            print("AI plays move: " + str(block_choice))
        board(games)
        winner, current_state = check_current_state(games)
        if winner is not None:
            print(str(winner) + " won!")
        else:
            current_player_idx = (current_player_idx + 1)%2
        
        if current_state is "Draw":
            print("Draw!")
            
    play_again = input('Wanna try again?(Y/N) : ')
    if play_again == 'N':
        print('Suit yourself!')
