"""
print state & current score
input user 
move(move)
check()
valid move hai->continue or print final score
"""
from board import board

game_board = board()

key_to_move = {'w':'U','a':'L','s':'D','d':'R'}

while(True):
    print(game_board)
    key = input()     
    move = key_to_move[key]
    if(game_board.check_move(move)):
        game_board.update(move)
    else:
        print("Invalid Move!!!\n")
        continue
    if(not game_board.check_state()):
        break

print(game_board)
print("Game Over !!!")