"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    #2 variables to track the number of moves made for each player
    X_count = 0
    O_count = 0
    
    #loop through the board and add to the respective counts
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                X_count += 1
            if board[i][j] == O:
                O_count += 1
    
    #if the board is all empty, it is player X's turn
    if board == initial_state():
        return X
    #if there are more X moves than O moves, then it is player O's turn
    if X_count > O_count:
        return O
    #else it is player X's turn
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    #variable that stores all the possible actions
    actions = set()
    
    #if a spot on the board is empty, then it is a possible action
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    #make a copy of the board to return
    result_board = copy.deepcopy(board)
    
    #if the action is not in the set of possible actions, raise an exception
    if action not in actions(board):
        raise Exception("Invalid")
    
    #change the variable on the board to whoever's turn it is
    result_board[action[0]][action[1]] = player(board)
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    #checks the rows for 3 in a row
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2] == X):
            return X
        elif (board[i][0] == board[i][1] == board[i][2] == O):
            return O
        
    #checks the columns for 3 in a row
    for j in range(3):
        if (board[0][j] == board[1][j] == board[2][j] == X):
            return X
        elif (board[0][j] == board[1][j] == board[2][j] == O):
            return O
    
    #checks the diagonals
    if (board[0][0] == board[1][1] == board[2][2] == X):
        return X
    elif (board[0][0] == board[1][1] == board[2][2] == O):
        return O
    elif (board[2][0] == board[1][1] == board[0][2] == X):
        return X
    elif (board[2][0] == board[1][1] == board[0][2] == O):
        return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    #checks if there are any empty states for a tie
    empty_count = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == EMPTY:
                empty_count += 1
    
    #if there is a winner, return true
    if (winner(board) == X or winner(board) == O):
        return True
    #if there are no empty states, return true
    elif (empty_count == 0):
        return True
    #else return false
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    #if X wins, return 1
    if (winner(board) == X):
        return 1
    #if O wins, return -1
    if (winner(board) == O):
        return -1
    #else return 0
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    #if the game is over, there is no optimal action
    if terminal(board):
        return None
    
    #if the player is X, maximize the value 
    #if the player is O, minimize the value
    else: 
        for action in actions(board):
            if player(board) == X:
                if maximize(board) == minimize(result(board, action)):
                    return action
        
            elif player(board) == O:
                if minimize(board) == maximize(result(board, action)):
                    return action
       
   
def maximize(board):
    if terminal(board):
        return utility(board)
    
    value = float('-inf')
    #for all the possible actions, find the value that will maximize the value
    for action in actions(board):
        #changes the value to whatever value is bigger between the result of the action and the current value
        value = max(value, minimize(result(board, action)))
        
    return value
    
    
def minimize(board):
    if terminal(board):
        return utility(board)
    
    value = float('inf')
    #for all the possible actions, find the value that will minimize the value
    for action in actions(board):
        #changes the value to whatever value is smaller between the result of the action and the current value
        value = min(value, maximize(result(board, action)))
        
    return value
    