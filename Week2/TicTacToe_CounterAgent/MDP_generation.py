import copy
import json
from blockingPlay import blockingMove

#It generates all the possible states, given num_X, num_O, pos and State
#num_X = the number of X's to be added
#num_O = the number of Os to be added
#pos = the number of positions which are filled?
#State is the current state of the board

def getStates(num_X,num_O,pos,States):
    """
    The positions of each cell are indexed as follows
    0 1 2
    3 4 5
    6 7 8
    --'pos' just indicates the position where the next char is placed
    --Basically all states with num_X X's and num_O O's are generated
      wherein these X's and O's are filled from pos onwards.
    --The recursion basically makes the cell at pos X,O or empty
      and then solves the new subproblems.
    """

    if(pos==9):
        if(num_X==0 and num_O==0):
            return copy.deepcopy(States)
        else:
            return []

    else:
        States_O,States_X,States_empty = [],[],[]
        if(num_X>0):
            for state in States:
                state[pos//3][pos%3] = 'X'
            States_X = getStates(num_X-1,num_O,pos+1,States)
            for state in States:
                state[pos//3][pos%3] = '_'

        if(num_O>0):
            for state in States:
                state[pos//3][pos%3] = 'O'
            States_O = getStates(num_X,num_O-1,pos+1,States)
            for state in States:
                state[pos//3][pos%3] = '_'
        
        num_empty = 9-num_X-num_O
        if(num_empty>0):
            States_empty = getStates(num_X,num_O,pos+1,States)

        allStates = []
        for state in (States_X+States_O+States_empty):
            allStates.append(state)

        return allStates

#Function to generate all valid states of the TicTacToe Game Board
def generateStates():
    """
    Generate validStates & terminal states
    Here, validStates refer to those which are attainable & non-terminal
    & terminalStates are attainable & terminal
    """
    allStates = []
    for numFilled in range(10):
        States = getStates(numFilled-numFilled//2,numFilled//2,0,[[['_','_','_'],['_','_','_'],['_','_','_']]])
        # print(numFilled,':',len(States))
        for state in States:
            allStates.append(state)
    return allStates

#Checks if the game has ended or not. Checks the ending condition of TicTacToe
def check_State(state,player_char):
    for i in range(3):
        if(player_char==state[i][0] and (state[i][0]==state[i][1] and state[i][0]==state[i][2])):
            return True

    for i in range(3):
        if(player_char==state[0][i] and (state[0][i]==state[1][i] and state[0][i]==state[2][i])):
            return True

    if(player_char==state[1][1]):
        if(state[0][0]==state[1][1] and state[0][0]==state[2][2]):
            return True
        if(state[2][0]==state[1][1] and state[2][0]==state[0][2]):
            return True

    return False

# Generate all the valid states
allStates = generateStates()

allValidStates = {}
stateToId = {}
MDP = {}

currId = -1
for state in allStates:
    Win_X = check_State(state,'X')
    Win_O = check_State(state,'O')
    ctr_X,ctr_O = 0,0

    #Count the total number of X's and O's in the board
    for i in range(3):
        for j in range(3):
            if(state[i][j]=='X'):
                ctr_X += 1
            if(state[i][j]=='O'):
                ctr_O += 1
    
    isTerminal = False
    Status = "Ongoing"

    #Ignore all the states in which X and O both win
    #We generate all kinds of states without thinking about their validity
    if(Win_X and Win_O):
        continue

    #If O wins the game to rules of TicTacToe, mark this game as Terminal
    elif(Win_X):
        if(ctr_X==ctr_O+1):
            isTerminal = True
            Status = "Win: X"
            currId += 1
        else:
            continue

    #If O wins the game to rules of TicTacToe, mark this game as Terminal
    elif(Win_O):
        if(ctr_X==ctr_O):
            isTerminal = True
            Status = "Win: O"
            currId += 1
        else:
            continue

    #If there is a draw, mark that state as Terminal
    elif(ctr_X+ctr_O==9):
        isTerminal = True
        Status = "Draw"
        currId += 1
    else:
        currId += 1
    
    #Saving all valid states and the next moves possible of those valid states
    move = []
    if(not isTerminal):
        opponent_char = 'X'
        if ctr_X==ctr_O:
            opponent_char = 'O'
        move = blockingMove(state,opponent_char)

    allValidStates[currId] = {"State":str(state),"isTerminal":isTerminal,"Status":Status,"move":move}
    stateToId[str(state)] = currId
    
#Saving information about each state, action associated with each state, the reward, the policy and the next states
currId = -1
for state in allStates:
    #Iterate only over the valid states
    if(str(state) not in stateToId.keys()):
        continue
    currId += 1
    ctr_X,ctr_O = 0,0
    isTerminal = allValidStates[stateToId[str(state)]]["isTerminal"]

    #Count total no. of X's and total no. of O's on the Board
    for i in range(3):
        for j in range(3):
            if(state[i][j]=='X'):
                ctr_X += 1
            if(state[i][j]=='O'):
                ctr_O += 1
    yourPlay = 'O'
    if(ctr_X==ctr_O):
        yourPlay = 'X'

    #Note if a state is terminal or not
    if(isTerminal):
        MDP[currId] = {"isTerminal":isTerminal}
    else:
        actions = {}
        validActions = []
        for i in range(3):
            for j in range(3):
                if(state[i][j]=='_'):
                    validActions.append([i,j])
        
        #Iterate over all the blank positions on the board
        for action_id,action in enumerate(validActions):
            currState = copy.deepcopy(state)
            currState[action[0]][action[1]] = yourPlay

            #Book-keeping for all Terminal States after the action is performed
            if(allValidStates[stateToId[str(currState)]]["isTerminal"]):
                reward = 0.0
                if(allValidStates[stateToId[str(currState)]]["Status"]!="Draw"):
                    reward = 1.0
                prob = 1.0
                actions[action_id] = [{"nextState":stateToId[str(currState)],"prob":prob,"reward":reward}]

            #
            else:
                moves = allValidStates[stateToId[str(currState)]]["move"]
                transitions = []

                #Iterating over all possible logical moves for the state achieved after performing the action
                for move in moves:
                    nextState = copy.deepcopy(currState)
                    nextState[move["row_id"]][move["col_id"]] = 'O'
                    if yourPlay=='O':
                        nextState[move["row_id"]][move["col_id"]] = 'X'
                    reward = 0.0
                    prob = move["probability"]
                    transitions.append({"nextState":stateToId[str(nextState)],"prob":prob,"reward":reward})
                actions[action_id] = transitions

        MDP[currId] = {"isTerminal":isTerminal,"actions":actions}

if __name__=="__main__":
    #To save all the possible valid states in a JSON File
    with open("ttt_agent.json","w") as output:
        json.dump(allValidStates,output,indent=4)

    #To save the maps of all possible VALID states to an ID
    with open("ttt_state2Id.json","w") as output:
        json.dump(stateToId,output,indent=4)

    #To save the actions, policy and reward associated with each state
    with open("ttt_MDP.json","w") as output:
        json.dump(MDP,output,indent=4)