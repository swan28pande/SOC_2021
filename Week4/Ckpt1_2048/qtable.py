import torch
from tdqm import tdqm
import numpy as np
import random
import matplotlib.pyplot as plt

device = torch.device("cuda:0" if torch.cuda.is_available else "cpu")

# Defining the Deep Q Network Architecture
class DQN(torch.nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.setup_convolution_layers()
        self.setup_linear_layers()
    
    def setup_convolution_layers(self):
        self.conv1 = torch.nn.Conv2d(16,128,(1,2))
        self.conv2 = torch.nn.Conv2d(16,128,(2,1))

        self.conv1_1 = torch.nn.Conv2d(128,128,(1,2))
        self.conv1_2 = torch.nn.Conv2d(128,128,(2,1))

        self.conv2_1 = torch.nn.Conv2d(128,128,(1,2))
        self.conv2_2 = torch.nn.Conv2d(128,128,(2,1))
    
    def setup_linear_layers(self):
        self.nn1 = torch.nn.Linear(4352,256)
        self.nn2 = torch.nn.Linear(256,4)

    def forward(self, X):
        X1 = self.conv1(X); X1 = torch.nn.ReLU(X1)
        X1 = self.conv1_1(X1);  X1 = torch.nn.ReLU(X1)

        X2 = self.conv1(X); X2 = torch.nn.ReLU(X2)
        X2 = self.conv1_2(X2); X2 = torch.nn.ReLU(X2)

        X3 = self.conv2(X);  X3 = torch.nn.ReLU(X3)
        X3 = self.conv2_1(X3);  X3 = torch.nn.ReLU(X3)

        X4 = self.conv2(X);  X4 = torch.nn.ReLU(X4)
        X4 = self.conv2_2(X4);  X4 = torch.nn.ReLU(X4)

        # Flattening All the Outputs of the Convolution Layers and Feed it into the FCNN
        X1 = torch.flatten(X1)
        X2 = torch.flatten(X2)
        X3 = torch.flatten(X3)
        X4 = torch.flatten(X4)

        X1 = torch.concat([X1,X2,X3,X4]) # Used X1 to save space
        X1 = self.nn1(X1)
        X1 = torch.nn.ReLU(X1)
        X1 = self.nn2(X1)
        X1 = torch.nn.ReLU(X1)
        
        return X1 # Neural Network Returns Q(s,a) for all the actions 'a'



class qtable:
    def __init__(self):
        # Initializing the Neural Network
        self.model = DQN()
        self.model.to(device)

         # Converting the Board into its Feature Vector Representation - One Hot Encoded Tensor
    def bitmap_representation(state):
        # A Cell in 2048 can have a max value of 2^16 and the game board is 4x4
        state_feature_tensor = np.zeros(shape=(4,4,16), dtype=np.float32)
        
        # Iterating over Rows
        for i in range(4):
            # Iterating over Columns
            for j in range(4):
                if(state[i][j]=='_'):
                    state_feature_tensor[i][j][0] = 1.0
                else:
                    power_of_2 = int(np.log(X[i][j],2))
                    state_feature_tensor[i][j][power_of_2] = 1.0
        
        return state_feature_tensor
    
    # Returns Q(s,a) for all actions 'a'
    def forstate(self,state):
        state = self.bitmap_representation(state).to(device)
        # Putting Model in evaluation Mode
        model.eval()
        with torch.no_grad():
            action_value_functions = self.model(state) # Outputs Q(s,a) for all actions
            action_value_functions = action_value_function.detach().numpy()
        # Reverting Model Back to Train Mode
        model.train()
        return action_value_functions

    # Returns Q(s,a) given station 's' and action 'a'
    def values(self,state,action):
        action_dict = {0:'U', 1:'D', 2:'L', 3:'R'}
        Q_val = self.forstate(state)
        return Q_val[action]

    def update(self,episode):
        pass
