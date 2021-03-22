from environment import Bag
from my_agent import drawOrEnd

global maxDraws
maxDraws = 5

def evaluate_agent(myBag):
    drawsLeft = maxDraws
    curr_utility = 0
    utilities = myBag.show_utility()

    while(drawsLeft):
        draw = drawOrEnd(curr_utility,utilities,drawsLeft)
        if(draw):
            curr_utility = myBag.sample_item()
        else:
            break
        drawsLeft -= 1

    if(drawsLeft):
        score = curr_utility
    else:
        score = myBag.sample_item()

    return score

sum_score = 0
curr_score = 0
num_iterations = 1000

for iteration in range(num_iterations):
    myBag = Bag()
    curr_score = evaluate_agent(myBag)
    sum_score += curr_score

score = sum_score/num_iterations

print("Your score is {} ,the best possible score is {}".format(score,100))