import numpy as np
from board import board
"""
Implementing an Expectimax Algorithm
Basically each node of the Expectimax Tree is a State of the Game
and the value of each Node is the increase in the score from the previous state of the board
"""

def expectiMiniMax (board_state, is_current, max_depth):
    depth_rem = max_depth

    # Return current score if max depth of tree reached
    if (depth_rem == 0):
        return board_state.score, None
    else:
        # Current Board State calc. score of each move up to max_depth, chooses that move which Maximises Score
        # Returns Best Score of the Move as well as The Move itself
        if(is_current):
            left = expectiMiniMax(board_state.update('L'), False, depth_rem-1)[0] if board_state.check_move('L') \
                else board_state.score
            right = expectiMiniMax(board_state.update('R'), False, depth_rem - 1)[0] if board_state.check_move('R') \
                else board_state.score
            up = expectiMiniMax(board_state.update('U'), False, depth_rem - 1)[0] if board_state.check_move('U') \
                else board_state.score
            down = expectiMiniMax(board_state.update('D'), False, depth_rem - 1)[0] if board_state.check_move('D') \
                else board_state.score
            return max(left, right, down, up), argmax(np.array([left,right,up,down]))

        # If it is not the current Node then it takes the Expected Value of Scores of All Possible Moves L,R,U,D
        # is_current is True because we want the next moves to be the best as well
        # Returns Score as well as a 'None' Move
        else:
            left = expectiMiniMax(board_state.update('L'), True, depth_rem - 1)[0] if board_state.check_move('L') \
                else board_state.score
            right = expectiMiniMax(board_state.update('R'), True, depth_rem - 1)[0] if board_state.check_move('R') \
                else board_state.score
            up = expectiMiniMax(board_state.update('U'), True, depth_rem - 1)[0] if board_state.check_move('U') \
                else board_state.score
            down = expectiMiniMax(board_state.update('D'), True, depth_rem - 1)[0] if board_state.check_move('D') \
                else board_state.score
            return (left + right + down + up)/4, None

def agent(game_board, max_depth):
    """
    The current game board is input,
    Choose a valid move
    """
    # First Checks if the Board State has no moves possible
    if ~board_state.check_state():
        move = None
    else :
        move_num = expectiMiniMax(game_board, True, max_depth)[1]
        move = ['L', 'R', 'U', 'D'][move_num]
    return move
