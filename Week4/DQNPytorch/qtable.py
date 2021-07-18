import torch
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
        X1 = X1.view(-1,1024)
        X2 = X2.view(-1, 1152)
        X3 = X3.view(-1, 1152)
        X4 = X4.view(-1, 1024)

        X1 = torch.concat([X1,X2,X3,X4], dim=1) # Used X1 to save space (batch_size, -1)
        X1 = self.nn1(X1)
        X1 = torch.nn.ReLU(X1)
        X1 = self.nn2(X1)
        X1 = torch.nn.ReLU(X1) # (batch_size, 4) and since Q(s,a) is always positive!
        
        return X1 # Neural Network Returns Q(s,a) for all the actions 'a'



class qtable:
    def __init__(self):
        # Initializing the Neural Network
        self.model = DQN()
        self.model.to(device)
        self.loss_criterion = torch.nn.SmoothL1Loss()
        self.opt = torch.optim.AdamW(self.model.parameters(), lr = 0.001)
        self.epochs = 5

         # Converting the Board into its Feature Vector Representation - One Hot Encoded Tensor
    def preprocessing(state):
        # A Cell in 2048 can have a max value of 2^16 and the game board is 4x4
        state_feature_tensor = np.zeros(shape=(4,4,16), dtype=np.float32)
        
        # Iterating over Rows
        for i in range(4):
            # Iterating over Columns
            for j in range(4):
                if(state[i][j]!='_'):
                    k = int(np.log(X[i][j],2))-1
                    state_feature_tensor[i][j][k] = 1.0
        
        return state_feature_tensor
    
    # Returns Q(s,a) for all actions 'a'
    def qvalues(self,state):
        bitmap = np.array([self.preprocessing(state)])
        bitmap = torch.tensor(bitmap, dtype = torch.float32, device = device)
        model.eval()
        with torch.no_grad():
            qvals = self.model.predict(bitmap)
            qvals = qvals.detach().numpy()
        model.train()
        return qvals.reshape([-1])

    # Given an Episode - Generate a Batch of transitions = (s,a,r)
    def get_batch(self, episode):
        # Get the list of States, Actions and Rewards for each transition in the Episode
        states = episode["States"]
        actions = episode["Actions"]
        rewards = episode["Rewards"]
        
        Xs = []
        ys = []
        
        # Iterating over all transitions
        num_steps = len(actions)
        for i in range(num_steps):
            qval_s1 = self.qvalues(states[i]) # Gives Q(s_t, a) for all actions 'a'
            qval_s2 = self.qvalues(states[i+1]) # Gives Q(s_t+1, a) for all actions 'a'
            qval_s1[actions[i]] = rewards[i]+np.max(qval_s2) # Gives R_t + max Q(s',a'); gamma = 1
            
            Xs.append(self.preprocessing(states[i])) # Appending the State Bitmap for each transition
            ys.append(qval_s1)
        X = np.stack(Xs,axis=0)
        y = np.stack(ys,axis=0)
        return X,y
    
    # Given an Epoch (10 Episodes in an Epoch) - Generate A Dataset to train on
    def get_dataset(self,episodes):
        X_batches = []
        y_batches = []
        
        # Iterate through all episodes
        for episode in episodes:
            # Generate a Mini Bath for a given episode
            X,y = self.get_batch(episode)
            X_batches.append(X)
            y_batches.append(y)
        
        # Return Transition Batches comprising all the 10 episodes
        return np.concatenate(X_batches,axis=0),np.concatenate(y_batches,axis=0)

    def update(self,episodes):
        X,y = self.get_dataset(episodes)
        X = torch.tensor(X, dtype = torch.float32, device = device)
        y = torch.tensor(y, dtype = torch.float32, device = device)
 
        self.model.train() # Setting Model in Train Mode
        for i in range(self.epochs):
            self.opt.zero_grad()
            y_pred = self.model(X)
            loss = self.loss_criterion(y_pred, y)
            loss.backward()
            self.opt.step()
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
