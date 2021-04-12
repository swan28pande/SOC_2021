import random
import copy

board_size = 4    # 4 x 4 board
prob = 0.8        # probability of getting a 2

class board:
    #Class variables : State , score

    def __init__(self):
        #randomly initiliaze state & set score to zero
        self.score = 0
        self.State = []
        all_pos = []
        for i in range(board_size):
            row = []
            for j in range(board_size):
                row.append('_')
                all_pos.append((i,j))
            self.State.append(row)
        random.shuffle(all_pos)
        pos1 = all_pos[0]
        if(random.random()>prob):
            self.State[pos1[0]][pos1[1]] = 4
        else:
            self.State[pos1[0]][pos1[1]] = 2
        pos2 = all_pos[1]
        if(random.random()>prob):
            self.State[pos2[0]][pos2[1]] = 4
        else:
            self.State[pos2[0]][pos2[1]] = 2

    def __str__(self):   
        #return string that would be printed after every move
        #The string must contain the curr score & board state
        s = ""
        for i in range(board_size):
            for j in range(board_size):
                s += str(self.State[i][j])
                s += '\t'
            s += '\n'
        s += "Your current score is {}\n".format(self.score)
        s += "Press W,A,S,D to move Up,Left,Down,Right respectively\n"
        return s

    def check_move(self,move):
        #Check if the move i.e 'U','D','L','R' is valid from the current state
        ok = False
        A = self.State
        if(move=='U'):
            for i in range(1,board_size):
                for j in range(board_size):
                    if(A[i][j]!='_' and (A[i-1][j]=='_' or A[i-1][j]==A[i][j])):
                        ok = True
        elif(move=='R'):
            for i in range(board_size):
                for j in range(0,board_size-1):
                    if(A[i][j]!='_' and (A[i][j+1]=='_' or A[i][j+1]==A[i][j])):
                        ok = True
        elif(move=='D'):
            for i in range(0,board_size-1):
                for j in range(board_size):
                    if(A[i][j]!='_' and (A[i+1][j]=='_' or A[i+1][j]==A[i][j])):
                        ok = True
        else:
            for i in range(board_size):
                for j in range(1,board_size):
                    if(A[i][j]!='_' and (A[i][j-1]=='_' or A[i][j]==A[i][j-1])):
                        ok = True
        return ok

    def check_state(self):
        #Check if there are any other valid moves availables or else return false i.e. gameOver
        return self.check_move('U') or self.check_move('D') or self.check_move('L') or self.check_move('R')

    def spawn(self):
        x = random.random()
        empty_pos = []
        for i in range(board_size):
            for j in range(board_size):
                if(self.State[i][j]=='_'):
                    empty_pos.append((i,j))
        random.shuffle(empty_pos)
        pos = empty_pos[0]
        if(x>0.8):
            self.State[pos[0]][pos[1]] = 4
        else:
            self.State[pos[0]][pos[1]] = 2

    def update(self,move):
        #Update game state & score given the move i.e 'U','D','L','R'
        A = self.State
        if(move=='U'):
            for j in range(board_size):
                for i in range(1,board_size):
                    if(A[i][j]!='_'):
                        for k in range(i-1,-1,-1):
                            if(A[k][j]=='_'):
                                if(k==0):
                                    A[k][j]=A[i][j]
                                    A[i][j]='_'
                                    break
                                else:
                                    continue
                            elif(A[k][j]==A[i][j]):
                                A[k][j] *= 2
                                A[i][j] = '_'
                                self.score += A[k][j]
                                break
                            else:
                                if((k+1)!=i):
                                    A[k+1][j]=A[i][j]
                                    A[i][j]='_'
                                    break
                                else:
                                    break
        elif(move=='R'):
            for i in range(board_size):
                for j in range(board_size-1,-1,-1):
                    if(A[i][j]!='_'):
                        for k in range(j+1,board_size):
                            if(A[i][k]=='_'):
                                if(k==board_size-1):
                                    A[i][k]=A[i][j]
                                    A[i][j]='_'
                                    break
                                else:
                                    continue
                            elif(A[i][j]==A[i][k]):
                                A[i][k] *= 2
                                A[i][j] = '_'
                                self.score += A[i][k]
                                break
                            else:
                                if((k-1)!=j):
                                    A[i][k-1]=A[i][j]
                                    A[i][j]='_'
                                    break
                                else:
                                    break
        elif(move=='D'):
            for j in range(board_size):
                for i in range(board_size-1,-1,-1):
                    if(A[i][j]!='_'):
                        for k in range(i+1,board_size):
                            if(A[k][j]=='_'):
                                if(k==board_size-1):
                                    A[k][j]=A[i][j]
                                    A[i][j]='_'
                                    break
                                else:
                                    continue
                            elif(A[k][j]==A[i][j]):
                                A[k][j] *= 2
                                A[i][j] = '_'
                                self.score += A[k][j]
                                break
                            else:
                                if((k-1)!=i):
                                    A[k-1][j]=A[i][j]
                                    A[i][j]='_'
                                    break
                                else:
                                    break
        else:
            for i in range(board_size):
                for j in range(1,board_size):
                    if(A[i][j]!='_'):
                        for k in range(j-1,-1,-1):
                            if(A[i][k]=='_'):
                                if(k==0):
                                    A[i][k]=A[i][j]
                                    A[i][j]='_'
                                    break
                                else:
                                    continue
                            elif(A[i][j]==A[i][k]):
                                A[i][k] *= 2
                                A[i][j] = '_'
                                self.score += A[i][k]
                                break
                            else:
                                if((k+1)!=j):
                                    A[i][k+1]=A[i][j]
                                    A[i][j]='_'
                                    break
                                else:
                                    break





