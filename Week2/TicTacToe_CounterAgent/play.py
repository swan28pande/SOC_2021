from MDP_generation import *
from MDP_Planning_VI import *
from blockingPlay import blockingMove
import random

numGames = 1000
reward = 0.0

#Iterating over the of episodes of an episodic task
for game_id in range(numGames):

    #To determine which player goes first
    #A live player plays with the opponent which is the RL Agent
    #Opponent is the RL Agent and My Char is the User
    toss = random.random()
    player = 0
    opponent_char = 'O'
    my_char = 'X'
    if(toss>0.5):
        player = 1
        opponent_char = 'X'
        my_char = 'O'

    #Initial state of the TicTacToe Board
    state = [['_','_','_'],['_','_','_'],['_','_','_']]

    while(True):
        #Move performed by the agent
        if(player):
            #You enter your state and the policy function gives out a corresponding Action
            action = policy[stateToId[str(state)]]
            for i in range(3):
                for j in range(3):
                    if(state[i][j]=='_'):
                        if(action==0):
                            state[i][j] = opponent_char
                        action -= 1

        #Move performed by US, for ease, it has been simulated for us; not relevant from PoV of RL
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

        # Check state, give the Learning Agent a Reward if it Wins the Game
        if(allValidStates[stateToId[str(state)]]["isTerminal"]):
            if(allValidStates[stateToId[str(state)]]["Status"]!="Draw"):
                if(player==1):
                    reward += 1.0
            break
        player ^= 1
print(reward)