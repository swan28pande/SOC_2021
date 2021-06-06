#This is a heuristic algorithm to simulate the playing of the game by a USER
#This program opposes the RL Agent and acts as a Real User Playing the game

def marginalScore(state,positions,opponent_char):
    ctr_opponent = 0
    ctr_self = 0
    ctr_empty = 0
    
    for pos in positions:
        if(state[pos[0]][pos[1]]=='_'):
            ctr_empty += 1
        elif(state[pos[0]][pos[1]]==opponent_char):
            ctr_opponent += 1
        else:
            ctr_self += 1

    if(ctr_self):
        return 1
    else:
        return (10 + 20*(ctr_opponent)**2)


def blockingScore(state,row_id,col_id,opponent_char):
    Score = 0
    #Add blocking score for its row
    Score += marginalScore(state,[[row_id,0],[row_id,1],[row_id,2]],opponent_char)
    #Add blocking score for its column
    Score += marginalScore(state,[[0,col_id],[1,col_id],[2,col_id]],opponent_char)

    #Add blocking score for diag1
    valid1 = [[0,0],[1,1],[2,2]]
    if([row_id,col_id] in valid1):
        Score += marginalScore(state,valid1,opponent_char)

    #Add blocking score for diag2
    valid2 = [[2,0],[1,1],[0,2]]
    if([row_id,col_id] in valid2):
        Score += marginalScore(state,valid2,opponent_char)

    return Score

#Function which figures out the best move possible
def blockingMove(state,opponent_char):
    move = []
    totScore = 0.0
    for i in range(3):
        for j in range(3):
            if(state[i][j]=='_'):
                move.append([i,j,blockingScore(state,i,j,opponent_char)])
                totScore += (move[-1][2]*move[-1][2])
    
    for idx,x in enumerate(move):
        move[idx] = {"row_id":x[0],"col_id":x[1],"probability":(x[2]*x[2])/totScore}

    return move

