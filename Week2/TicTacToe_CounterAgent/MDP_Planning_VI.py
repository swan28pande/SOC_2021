from MDP_generation import *
import copy
import numpy as np
import matplotlib.pyplot as plt

numStates = len(list(stateToId.keys()))
values = np.zeros(numStates)
policy = np.zeros(numStates)
n_iter = 10

for i in range(n_iter):
    prev_values = copy.deepcopy(values)
    for state_id in range(numStates):
        isTerminal = allValidStates[state_id]["isTerminal"]
        if(not isTerminal):
            actions = MDP[state_id]["actions"]
            numActions = len(list(actions.keys()))
            action_values = np.zeros(numActions)
            for action_id in actions.keys():
                action_val = 0.0
                transitions = MDP[state_id]["actions"][action_id]
                numTransitions = len(transitions)
                for transition_id in range(numTransitions):
                    prob = transitions[transition_id]["prob"]
                    reward = transitions[transition_id]["reward"]
                    nextState = transitions[transition_id]["nextState"]
                    action_val += prob*(reward+prev_values[nextState])
                action_values[action_id]=action_val
            values[state_id] = np.max(action_values)
            policy[state_id] = np.argmax(action_values)
    eps = np.max(values - prev_values)
    print(eps, i, np.mean(prev_values))


