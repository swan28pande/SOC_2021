import numpy as np
from board import board
import copy
"""
Implementing an Expectimax Algorithm
Basically each node of the Expectimax Tree is a State of the Game
and the value of each Node is the increase in the score from the previous state of the board
"""

def expecti_minimax(board_state, is_current, depth_rem):
    # Return current score if max depth of tree reached or no other moves possible
    if depth_rem == 0 or not board_state.check_state():
        return board_state.score, 0
    else:
        # Current Board State calc. score of each move up to max_depth, chooses that move which Maximises Score
        # Returns Best Score of the Move as well as The Move itself
        if is_current:
            bs1 = copy.deepcopy(board_state)
            bs1.update('L')
            left = expecti_minimax(bs1, False, depth_rem)[0] if board_state.check_move('L') else -1

            bs2 = copy.deepcopy(board_state)
            bs2.update('R')
            right = expecti_minimax(bs2, False, depth_rem)[0] if board_state.check_move('R') else -1

            bs3 = copy.deepcopy(board_state)
            bs3.update('U')
            up = expecti_minimax(bs3, False, depth_rem)[0] if board_state.check_move('U') else -1

            bs4 = copy.deepcopy(board_state)
            bs4.update('D')
            down = expecti_minimax(bs4, False, depth_rem)[0] if board_state.check_move('D') else -1

            return max(left, right, down, up), np.argmax(np.array([left, right, up, down]))

        # If it is not the current Node then it takes the Expected Value of Scores of All Possible Moves L,R,U,D
        # is_current is True because we want the next moves to be the best as well
        # Returns Score as well as a 'None' Move
        else:
            bs1 = copy.deepcopy(board_state)
            bs1.update('L')
            left = expecti_minimax(bs1, True, depth_rem - 1)[0] if board_state.check_move('L') else -1

            bs2 = copy.deepcopy(board_state)
            bs2.update('R')
            right = expecti_minimax(bs2, True, depth_rem - 1)[0] if board_state.check_move('R') else -1

            bs3 = copy.deepcopy(board_state)
            bs3.update('U')
            up = expecti_minimax(bs3, True, depth_rem - 1)[0] if board_state.check_move('U') else -1

            bs4 = copy.deepcopy(board_state)
            bs4.update('D')
            down = expecti_minimax(bs4, True, depth_rem - 1)[0] if board_state.check_move('D') else -1

            # To return the score: Finds all allowed moves, performs each one; takes an average of the scores after each
            # allowed move and returns it, if zero allowed moves, returns score of the current board.
            counter = 0
            total = 0
            for mv in [left,right,up,down]:
                if(mv>0):
                    counter += 1
                    total += mv
            return (total/counter,0) if counter != 0 else (board_state.score,0)

def agent(game_board, max_depth=2):
    """
    The current game board is input,
    Choose a valid move
    """
    move_num = expecti_minimax(game_board, True, max_depth)[1]
    move = ['L', 'R', 'U', 'D'][move_num]
    return move
