import random

N = 4
decay_factor = 0.9

class game:
    def __init__(self,play):
        self.state = []
        self.score = 0
        self.snake_pos = [(random.randint(0,N-1),random.randint(0,N-1))]
        self.game_over = False
        self.prev_move = -1
        self.dr = [(-1,0),(1,0),(0,1),(0,-1)]
        self.isPlay = play

        empty = []
        for i in range(N):
            temp = []
            for j in range(N):
                temp.append(".")
                if(self.snake_pos != (i,j)):
                    empty.append((i,j))
            self.state.append(temp)
        self.state[self.snake_pos[0][0]][self.snake_pos[0][1]] = 'O'

        random.shuffle(empty)
        self.reward_pos = empty[0]
        self.state[self.reward_pos[0]][self.reward_pos[1]] = '#'
        self.points = 1.0
        
        if(self.isPlay):
            self.display()

    def spawn_reward(self):
        empty = []
        for i in range(N):
            for j in range(N):
                if(self.state[i][j]=='.'):
                    empty.append((i,j))
        if(len(empty)==0):
            self.game_over = True
            return
        random.shuffle(empty)
        self.reward_pos = empty[0]
        self.state[self.reward_pos[0]][self.reward_pos[1]] = '#'
        self.points = 1.0

    def display(self):
        print("Current Score :",self.score)
        for i,pos in enumerate(self.snake_pos):
            self.state[pos[0]][pos[1]] = chr(ord('a')+i)
        for i in range(N):
            for j in range(N):
                print(self.state[i][j],end=' ')
            print('\n')
        print()
        for i,pos in enumerate(self.snake_pos):
            self.state[pos[0]][pos[1]] = 'O'

    def get_move(self):
        valid_moves = {'w':0,'s':1,'d':2,'a':3}
        while(True):
            move = input("Give the next move (w,a,s,d) ...\n")
            if(move not in valid_moves.keys()):
                print("Invalid input!!!, choose N/S/E/W")
                continue
            else:
                move_id = valid_moves[move]
                if(len(self.snake_pos)>1):
                    if(self.snake_pos[1][0]==self.snake_pos[0][0]+self.dr[move_id][0] and self.snake_pos[1][1]==self.snake_pos[0][1]+self.dr[move_id][1]):
                        print("Invalid move, u can't take a U turn")
                        continue
                    else:
                        return move_id
                else:
                    return move_id

    def valid_pos(self,pos):
        return ((pos[0]>=0 and pos[0]<N) and (pos[1]>=0 and pos[1]<N))

    def move(self,move):
        next_pos = (self.dr[move][0]+self.snake_pos[0][0],self.dr[move][1]+self.snake_pos[0][1])
        if(not self.valid_pos(next_pos)):
            self.game_over = True
        else:
            if(self.state[next_pos[0]][next_pos[1]]=='#'):
                self.snake_pos.insert(0,next_pos)
                self.state[next_pos[0]][next_pos[1]] = 'O'
                self.reward_pos = -1
                self.score += self.points
            else:
                prev_pos = self.snake_pos.pop()
                self.state[prev_pos[0]][prev_pos[1]] = '.'
                if(next_pos in self.snake_pos):
                    self.game_over = True
                else:
                    self.snake_pos.insert(0,next_pos)
                    self.state[next_pos[0]][next_pos[1]] = 'O'
                    self.points *= decay_factor
        self.prev_move = move
        if(self.reward_pos == -1):
            self.spawn_reward()
        if(not self.game_over and self.isPlay):
            self.display()

    def play(self):
        while(not self.game_over):
            move = self.get_move()
            self.move(move)
        print("\nGame Over!!!")
        print("Your final score is :",Game.score)

Game = game(play=True)
Game.play()



        
