import numpy as np
import random
import math
import matplotlib.pyplot as plt
from simulate import game

N = 4
n_epochs = 1000000

def valid_pos(pos,snake_pos,reward_pos):
    return (pos!=reward_pos and pos not in snake_pos) and ((pos[0]>=0 and pos[0]<N) and (pos[1]>=0 and pos[1]<N))

def populate_qtable(snake_pos,reward_pos,qtable,drs):
    qtable[str(reward_pos)+':'+str(snake_pos)] = np.zeros(4)
    for dr in drs:
        next_pos = (snake_pos[-1][0]+dr[0],snake_pos[-1][1]+dr[1])
        if(valid_pos(next_pos,snake_pos,reward_pos)):
            snake_pos.append(next_pos)
            populate_qtable(snake_pos,reward_pos,qtable,drs)
            snake_pos.pop()

class agent():
    def __init__(self):
        """
        randomly initialize the Q-table
        """
        self.dr = [(-1,0),(1,0),(0,1),(0,-1)]
        self.lr = 0.2
        self.eps = 0.2
        self.qtable = {}
        self.scores = []
        for i in range(N*N):
            reward_pos = (i//N,i%N)
            snake_pos = []
            for j in range(N*N):
                if(j!=i):
                    snake_pos.append((j//N,j%N))
                    populate_qtable(snake_pos,reward_pos,self.qtable,self.dr)
                    snake_pos.pop()

    def get_action(self,state):
        """
        Get the action using the q-table
        """
        sample = random.random()
        if(sample<self.eps):
            return random.randint(0,3)
        else:
            return np.argmax(self.qtable[state])
    
    def generate_episode(self):
        """
        Generate an episode & corresponding rewards
        """
        Game = game()
        states = [str(Game.reward_pos)+':'+str(Game.snake_pos)]
        actions = []
        rewards = []
        prev_score = 0
        while(not Game.game_over):
            action = self.get_action(str(Game.reward_pos)+':'+str(Game.snake_pos))
            Game.move(action)
            states.append(str(Game.reward_pos)+':'+str(Game.snake_pos))
            actions.append(action)
            rewards.append(Game.score-prev_score)
            prev_score = Game.score
        
        return {"States":states,"Actions":actions,"Rewards":rewards},prev_score

    def update_qtable(self,episode):
        """
        update q-table using the episode
        """
        n = len(episode["Rewards"])
        for i in range(n):
            state1 = episode["States"][i]
            state2 = episode["States"][i+1]
            action = episode["Actions"][i]
            reward = episode["Rewards"][i]
            cumm_reward = reward
            if(state2[0] != '-'):
                cumm_reward += np.mean(self.qtable[state2])
            self.qtable[state1][action] += self.lr*(cumm_reward-self.qtable[state1][action])
        
    
    def learning_curve(self):
        plt.plot(np.arange(n_epochs/1000),self.scores)
        plt.show()

    def train(self):
        """
        Generates episodes & update q-table
        """
        scores = []
        for epoch in range(n_epochs):
            self.eps = 0.5/(1.0+math.sqrt(epoch/10000))
            episode,score = self.generate_episode()
            scores.append(score)
            self.update_qtable(episode)
            if(epoch%1000==0):
                self.scores.append(sum(scores)/1000.0)
                print(epoch,':',score)
                scores = []
        self.learning_curve()
    def test(self,n):
        for i in range(n):
            Game = game()
            while(not Game.game_over):
                action = np.argmax(self.qtable[str(Game.reward_pos)+':'+str(Game.snake_pos)])
                print(str(Game.reward_pos)+':'+str(Game.snake_pos),action)
                Game.move(action)
            print(i,':',Game.score)

Agent = agent()
Agent.train()
Agent.test(10)
