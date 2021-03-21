import random
import math

def simulate():
    """
    return True if the needle falls on the line , False otherwise
    """
    spacing = 1.0
    stick_length = 0.5
    #Randomly choose the positon at which it falls
    pos_x = spacing*random.random()          #random number between 0-1
    angle = math.pi*random.random()  #random orientaion i.e. angle with horizontal

    #Check if it falls on a line
    leftmost = pos_x-stick_length*math.cos(angle)
    rightmost = pos_x+stick_length*math.cos(angle)

    if(leftmost<0 or rightmost>1):
        return True
    else:
        return False
    
n_iterations = 10000

crossing = 0
for iteration in range(n_iterations):
    if(simulate()):
        crossing += 1
    
prob = crossing/n_iterations

print("Probability of stick crossing the lines is {}".format(prob))