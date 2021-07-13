from MDP_generation import *
import copy
import numpy as np
import matplotlib.pyplot as plt

numStates = len(list(stateToId.keys()))
#Initial Value Function for each State i.e v_0
values = np.zeros(numStates)
#Initial Policies for each state i.e pi(s)
policy = np.zeros(numStates)
n_iter = 10

#Number of iterations of the Value Iteration Algorithm
for i in range(n_iter):
    #Value functions for each state, given the old deterministic policy
    prev_values = copy.deepcopy(values)
    #Iterating over all states s
    for state_id in range(numStates):
        isTerminal = allValidStates[state_id]["isTerminal"]

        if(not isTerminal):
            #List of all actions 'a' possible for the given NON TERMINAL STATE
            actions = MDP[state_id]["actions"]
            numActions = len(list(actions.keys()))
            action_values = np.zeros(numActions)

            #Policy Evaluation Begins
            #Iterating over all the possible actions 'a' for the given NON TERMINAL STATE
            for action_id in actions.keys():
                action_val = 0.0
                #All possible new states s' for the given action
                transitions = MDP[state_id]["actions"][action_id]
                numTransitions = len(transitions)

                # Iterating over all possible new states s', given a and s
                for transition_id in range(numTransitions):
                    prob = transitions[transition_id]["prob"]
                    reward = transitions[transition_id]["reward"]
                    nextState = transitions[transition_id]["nextState"]
                    action_val += prob*(reward+prev_values[nextState])

                action_values[action_id]=action_val

            #Value Iteration Step
            values[state_id] = np.max(action_values)

            #Policy Improvement Step
            policy[state_id] = np.argmax(action_values)

    #To understand the convergence
    eps = np.max(values - prev_values)
    print(eps, i, np.mean(prev_values))


