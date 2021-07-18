import numpy as np
import random
import math
import matplotlib.pyplot as plt
from board import board
from dqn import dqn
import numpy as np

"""
Implementing Deep Q-Learning Algorithm
"""

N = 4
action_map = ['U','R','D','L']

class agent():
    def __init__(self):
        self.DQN = dqn() 

    def get_action(self,game_board,eps):
        invalid_actions = []
        for idx,action in enumerate(action_map):
            if(not game_board.check_move(action)):
                invalid_actions.append(idx)

        sample = random.random()
        if(sample<eps):
            while(True):
                action = random.randint(0,3)
                if(action in invalid_actions):
                    continue
                else:
                    return action
        else:
            qvals = self.DQN.qvalues(game_board.State)
            for action in invalid_actions:
                qvals[action] = -1e6
            return np.argmax(qvals)

    def generate_episode(self,eps):
        """
        Generate an episode & corresponding rewards
        """
        game_board = board()
        states = [game_board.State]
        actions = []
        rewards = []
        prev_score = 0
        while(game_board.check_state()):
            action = self.get_action(game_board,eps)
            game_board.update(action_map[action])
            game_board.spawn()
            states.append(game_board.State)
            actions.append(action)
            rewards.append(game_board.score-prev_score)
            prev_score = game_board.score
        
        return {"States":states,"Actions":actions,"Rewards":rewards},prev_score
    
    def train(self,n_epochs=1000):
        """
        Generates episodes & update qvalues
        """
        for epoch in range(n_epochs):
            eps = max(0.01,1.0/(1+epoch/10))
            episodes = []
            scores = []
            for episode_id in range(10):
                episode,score = self.generate_episode(eps)
                episodes.append(episode)
                scores.append(score)
            print("Epoch:",(epoch+1))
            print(sum(scores)/len(scores))
            self.DQN.update(episodes)

    def test(self,n):
        for i in range(n):
            game_board = board()
            while(game_board.check_state()):
                action = self.get_action(game_board,0.0)
                print(game_board.State,action)
                game_board.update(action)
            print(i,':',game_board.score)

Agent = agent()
Agent.train()
Agent.test(10)