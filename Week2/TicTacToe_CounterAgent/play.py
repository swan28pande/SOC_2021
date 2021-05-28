from MDP_generation import *
from MDP_Planning_VI import *
from blockingPlay import blockingMove
import random

numGames = 1000
reward = 0.0

for game_id in range(numGames):
    toss = random.random()
    player = 0
    opponent_char = 'O'
    my_char = 'X'
    if(toss>0.5):
        player = 1
        opponent_char = 'X'
        my_char = 'O'
    state = [['_','_','_'],['_','_','_'],['_','_','_']]
    while(True):
        if(player):
            action = policy[stateToId[str(state)]]
            for i in range(3):
                for j in range(3):
                    if(state[i][j]=='_'):
                        if(action==0):
                            state[i][j] = opponent_char
                        action -= 1
        else:
            sample = random.random()
            moves = blockingMove(state,opponent_char)
            move_id = 0
            tot_prob = 0.0
            for idx,move in enumerate(moves):
                tot_prob += move["probability"]
                if(tot_prob>sample):
                    move_id = idx
                    state[moves[move_id]["row_id"]][moves[move_id]["col_id"]] = my_char
                    break

        # Check state
        if(allValidStates[stateToId[str(state)]]["isTerminal"]):
            if(allValidStates[stateToId[str(state)]]["Status"]!="Draw"):
                if(player==1):
                    reward += 1.0
            break
        player ^= 1

print(reward)