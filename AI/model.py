import tensorflow as tf,os
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

class NeuralNet(Model):
    def __init__(self,learning_rate,gamma,input_size,hidden_layer,output_size,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.gamma=gamma
        self.learning_rate=learning_rate
        self.loss=tf.keras.losses.MSE
        self.model=self._create(input_size,hidden_layer,output_size)

    def _create(self,input_size,hidden_layer,output_size):
        model=Sequential()
        model.add(Dense(hidden_layer,activation='relu',input_shape=(input_size,)))
        model.add(Dense(output_size,activation='softmax'))
        return model
    
    def compile(self,optimizer,loss,*args,**kwargs):
        super().compile(*args,**kwargs)
        if loss=='mse':
            self.loss=tf.keras.losses.MSE
        else:
            self.loss=tf.keras.losses.MAE
        if optimizer=='adam':
            self.optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        else:
            self.optimizer=tf.keras.optimizers.RMSprop(learning_rate=self.learning_rate)
    
    def train_step(self,state,action,reward,next_state,game_over):
        state=np.array(state,dtype=np.float32)
        action=np.array(action,dtype=np.float32)
        reward=np.array(reward,dtype=np.float32)
        next_state=np.array(next_state,dtype=np.float32)
        if len(state.shape)==1:
            state=np.expand_dims(state,axis=0)
            action=np.expand_dims(action,axis=0)
            reward=np.expand_dims(reward,axis=0)
            next_state=np.expand_dims(next_state,axis=0)
            game_over=np.expand_dims(game_over,axis=0)
        
        with tf.GradientTape() as tape:
            pred=self.model(state,training=True)
            target=np.copy(pred)

            for idx in range(len(game_over)):
                Q_new=reward[idx]
                if not game_over[idx]:
                    Q_new=reward[idx]+self.gamma*np.max(self.model(np.expand_dims(next_state[idx],axis=0),training=True))
                target[idx][np.argmax(action[idx]).item()] = Q_new
            loss = self.loss(target, pred)

        grad = tape.gradient(loss, self.model.trainable_variables) 
        self.optimizer.apply_gradients(zip(grad, self.model.trainable_variables))

    def save_model(self):
        if not os.path.exists('models'):
            os.mkdir('models')
        tf.keras.models.save_model(model=self.model,filepath=os.path.join('models','snakeAi.h5'))