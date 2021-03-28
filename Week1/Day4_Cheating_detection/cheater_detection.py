import numpy as np
import random

def cheater_detector(testcase):
    #Edit the code below
    #Randomly pick a player to be the cheater
    return random.randint(0,testcase.shape[0]-1)