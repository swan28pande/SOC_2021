import numpy as np
import random
import math
import matplotlib.pyplot as plt
from board import board
from qtable import qtable
import numpy as np
import copy

"""
Implementing Deep Q-Learning Algorithm
"""

N = 4
n_epochs = 1000000

class agent():
    def __init__(self):
        self.qtable= qtable()
        self.eps = 0.2
        self.scores = []

        

    

    def get_action(self,state):

        sample = random.random()
        # Alternate between choosing an epsilon greedy policy and model predicted action
        if(sample<self.eps):
            return random.randint(0,3)
        else:
            return np.argmax(self.qtable.forstate(state))

    def generate_episode(self):
        """
        Generate an episode & corresponding rewards
        """
        game_board = board()
        transition_list= [] # Stores Transitions as (s,a,s',r)
        current_score = 0
        while( game_board.check_state()):
            s = game_board.State
            action = self.get_action(s)
            game_board.update(action)
            s_prime = game_board.State
            rewards.append(game_board.score-current_score)
            current_score = game_board.score
            transition_list.append((s,action,s_prime,reward))
        return transition_list, current_score


   
    
    def learning_curve(self):
        plt.plot(np.arange(n_epochs/1000),self.scores)
        plt.show()
    
    def train(self):
        """
        Generates episodes & update qvalues
        """
        scores = []
        for epoch in range(n_epochs):
            self.eps = 0.5/(1.0+math.sqrt(epoch/10000))
            episode,score = self.generate_episode()
            scores.append(score)
            self.qvalues.update(episode)
            if(epoch%1000==0):
                self.scores.append(sum(scores)/1000.0)
                print(epoch,':',score)
                scores = []
        self.learning_curve()


    def test(self,n):
        for i in range(n):
            game_board = board()
            while(game_board.check_state()):
                action = np.argmax(self.qtable.forstate(game_board.State))
                print(game_board.State,action)
                game_board.update(action)
            print(i,':',game_board.score)

Agent = agent()
Agent.train()
Agent.test(10)

    
