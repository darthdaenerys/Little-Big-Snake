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