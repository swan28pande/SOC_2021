from agent_template import agent
from board import board

n_iter = 1
avg_score = 0

# For one iteration corresponds to one game of 2048
for i in range(n_iter):
    game_board = board()
    while(True):
        # Checks if a move can actually be made.
        if game_board.check_state():
            move = agent(game_board, max_depth = 4)
            if(game_board.check_move(move)):
                game_board.update(move)
                print(game_board.score)
                # print(game_board)
            else:
                continue
            # Spawns new values of 2/4 on the gameboard after the move has been made
            game_board.spawn()
        else:
            break

    avg_score += (game_board.score-avg_score)/(i+1)
    # print("Iteration:{} , Score:{}".format(i+1,game_board.score))

print("Score:", avg_score.__round__(2))
