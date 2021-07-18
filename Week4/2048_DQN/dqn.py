from tensorflow import keras
import numpy as np
import math

N = 4

class dqn():
    def __init__(self):
        inputs = keras.layers.Input(shape=(4,4,16))
        x1 = keras.layers.Conv2D(filters=64,kernel_size=(2,1),padding="same",activation='relu')(inputs)
        y1 = keras.layers.Conv2D(filters=64,kernel_size=(2,1),padding="same",activation='relu')(x1)
        y2 = keras.layers.Conv2D(filters=64,kernel_size=(1,2),padding="same",activation='relu')(x1)

        x2 = keras.layers.Conv2D(filters=64,kernel_size=(1,2),padding="same",activation='relu')(inputs)
        y3 = keras.layers.Conv2D(filters=64,kernel_size=(2,1),padding="same",activation='relu')(x2)
        y4 = keras.layers.Conv2D(filters=64,kernel_size=(1,2),padding="same",activation='relu')(x2)

        z = keras.layers.concatenate([x1,x2,y1,y2,y3,y4],axis=3)
        z = keras.layers.Flatten()(z)

        outputs = keras.layers.Dense(units=4,activation='relu')(z)

        self.model = keras.Model(inputs=inputs,outputs=outputs)

        self.model.compile(optimizer="adam",loss="mse",metrics=["mae"])

        self.model.summary()

    def preprocessing(self,state):
        bitmap = np.zeros(shape=(4,4,16))
        for i in range(N):
            for j in range(N):
                if(state[i][j]!='_'):
                    k = int(math.log2(state[i][j]))-1
                    bitmap[i][j][k] = 1
        return bitmap

    def qvalues(self,state):
        bitmap = np.array([self.preprocessing(state)])
        qvals = self.model.predict(bitmap)
        return qvals.reshape([-1])

    def generate_minibatch(self,episode):
        states = episode["States"]
        actions = episode["Actions"]
        rewards = episode["Rewards"]
        Xs = []
        ys = []
        num_steps = len(actions)
        for i in range(num_steps):
            qvals1 = self.qvalues(states[i])
            qvals2 = self.qvalues(states[i+1])
            qvals1[actions[i]] = rewards[i]+np.max(qvals2)
            Xs.append(self.preprocessing(states[i]))
            ys.append(qvals1)
        X = np.stack(Xs,axis=0)
        y = np.stack(ys,axis=0)
        return X,y

    def generate_dataset(self,episodes):
        minibatches_X = []
        minibatches_y = []
        for episode in episodes:
            X,y = self.generate_minibatch(episode)
            minibatches_X.append(X)
            minibatches_y.append(y)
        return np.concatenate(minibatches_X,axis=0),np.concatenate(minibatches_y,axis=0)

    def update(self,episodes):
        X,y = self.generate_dataset(episodes)
        self.model.fit(x=X,y=y,epochs=10)