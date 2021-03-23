def drawOrEnd(curr_utility,all_utilities,drawsLeft):
    """
    Input : utility of current item, the utility list, draws remaining
    Output: returns a boolean value whether to draw again or end the game
    """
    #Change the code below
    #Sample agent shown below always draw i.e. always return True
    expected_utility = [sum(all_utilities)/len(all_utilities)]
    for num_moves in range(1,drawsLeft):
        better = [utility for utility in all_utilities if utility>expected_utility[-1]]
        p = len(better)/len(all_utilities)
        expected_utility.append(p*(sum(better)/len(better)) + (1-p)*expected_utility[-1])

    if(curr_utility>expected_utility[drawsLeft-1]):
        return False
    else:
        return True