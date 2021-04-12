import random

def agent(game_board):
    """
    The current game board is input,
    Choose a valid move
    """
    x = random.randint(0,3)
    if(x==0):
        return 'U'
    elif(x==1):
        return 'R'
    elif(x==2):
        return 'D'
    else:
        return 'L'