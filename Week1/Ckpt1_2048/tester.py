from random_agent import agent
from board import board

n_iter = 100
avg_score = 0

for i in range(n_iter):
    game_board = board()
    while(True):
        move = agent(game_board)
        if(game_board.check_move(move)):
            game_board.update(move)
        else:
            continue
        if(not game_board.check_state()):
            break
    avg_score += (game_board.score-avg_score)/(i+1)
    #print("Iteration:{} , Score:{}".format(i+1,game_board.score))

print("Score:",avg_score.__round__(2))
