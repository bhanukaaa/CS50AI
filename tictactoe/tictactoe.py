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
    # If the number of X's == number of O's, assuming the X goes first, it is X's turn
    # If there are more X's than O's, it is O's turn
    numX = 0
    numO = 0
    # Counting how many of each marker is on the board
    for row in board:
        for column in row:
            if column == "X":
                numX += 1
            elif column == "O":
                numO += 1
    # Calculation logic
    if numX == numO:
        return "X"
    elif numO == (numX-1):
        return "O"
    else:
        raise Exception(
            "Error in calculating turn, An invalid move may have been made")


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] != "X" and board[i][j] != "O":
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if action is valid
    if board[action[0]][action[1]] == "X" or board[action[0]][action[1]] == "O":
        raise Exception("Invalid Action, Space Already Occupied")

    # Make deep copy
    newBoard = copy.deepcopy(board)

    # Apply action
    newBoard[action[0]][action[1]] = player(board)
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for Horizontal winners
    for i in range(3):
        marker = board[i][0]
        if board[i][1] == marker and board[i][2] == marker:
            return marker

    # Check for Vertical winners
    for j in range(3):
        marker = board[0][j]
        if board[1][j] == marker and board[2][j] == marker:
            return marker

    # Check for Diagonal winners
    middleMarker = board[1][1]
    if board[0][0] == middleMarker and board[2][2] == middleMarker:
        return middleMarker
    if board[0][2] == middleMarker and board[2][0] == middleMarker:
        return middleMarker

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Checking if winner function gives a Value
    if winner(board) is not None:
        return True

    # Counting number of markers to see if whole grid is filled
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] in ("X", "O"):
                count += 1
    if count == 9:
        return True

    # Return false if above conditions fail
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == "X":
            v, bestMove = maxValue(board)
            return bestMove
        else:
            v, bestMove = minValue(board)
            return bestMove


def maxValue(board):
    v = -999
    bestMove = None
    if terminal(board):
        return utility(board), None

    for action in actions(board):
        currV, currAction = minValue(result(board, action))
        if currV > v:
            v = currV
            bestMove = action
            if v == 1:
                return v, bestMove

    return v, bestMove


def minValue(board):
    v = 999
    bestMove = None
    if terminal(board):
        return utility(board), None

    for action in actions(board):
        currV, currAction = maxValue(result(board, action))
        if currV < v:
            v = currV
            bestMove = action
            if v == -1:
                return v, bestMove

    return v, bestMove
