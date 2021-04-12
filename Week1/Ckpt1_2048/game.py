"""
print state & current score
input user 
move(move)
check()
valid move hai->continue or print final score
"""
from board import board

game_board = board()

while(True):
    print(game_board)
    move = input()     #Or move = agent(game_board) for testing an agent
    if(game_board.check_move()):
        game_board.update()
    else:
        print("Invalid Move!!!\n")
        continue
    if(not game_board.check_state()):
        break

print(game_board)
print("Game Over !!!")

    
    


