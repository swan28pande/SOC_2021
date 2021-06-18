import random

N = 4
decay_factor = 0.9

class game:
    def __init__(self):
        self.score = 0
        self.snake_pos = [(random.randint(0,N-1),random.randint(0,N-1))]
        self.game_over = False
        self.dr = [(-1,0),(1,0),(0,1),(0,-1)]
        self.points = 0
        self.spawn_reward()

    def spawn_reward(self):
        empty = []
        for i in range(N):
            for j in range(N):
                if((i,j) not in self.snake_pos):
                    empty.append((i,j))
        if(len(empty)==0):
            self.game_over = True
        else:
            random.shuffle(empty)
            self.reward_pos = empty[0]
            self.points = 1.0

    def valid_pos(self,pos):
        return ((pos[0]>=0 and pos[0]<N) and (pos[1]>=0 and pos[1]<N))

    def move(self,move):
        next_pos = (self.dr[move][0]+self.snake_pos[0][0],self.dr[move][1]+self.snake_pos[0][1])
        if(not self.valid_pos(next_pos)):
            self.game_over = True
        else:
            if(next_pos==self.reward_pos):
                self.snake_pos.insert(0,next_pos)
                self.reward_pos = -1
                self.score += self.points
            else:
                self.snake_pos.pop()
                if(next_pos in self.snake_pos):
                    self.game_over = True
                else:
                    self.snake_pos.insert(0,next_pos)
                    self.points *= decay_factor
        if(self.reward_pos == -1 and not self.game_over):
            self.spawn_reward()
        if(self.game_over):
            self.reward_pos = -1

