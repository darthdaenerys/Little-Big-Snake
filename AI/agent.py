from AI.environment import Environment
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import pygame,json,random,numpy as np
from collections import deque
import tensorflow as tf
from AI.model import NeuralNet

class Agent:
    def __init__(self):
        pygame.init()
        f=open(os.path.join('AI','settings.json'))
        self.settings=json.load(f)
        f.close()
        self.display_surface=pygame.display.set_mode((self.settings['window_width'],self.settings['window_height']))
        pygame.display.set_caption('Snake AI - Reinforcement Learning')
        self.score_dataframe={
            'Score':[],
        }

        # agent hyperparameters
        if self.settings['load_pretrained']:
            self.best_score=self.settings['best_score']
            self.games=self.settings['games']
        else:
            self.best_score=0
            self.games=1
        self.epsilon=0  # controls randomness
        self.gamma=0    # discount rate
        self.max_memory=100_000
        self.memory=deque(maxlen=self.max_memory)
        self.batch_size=1000
        self.learning_rate=0.001
        self.iterations=0

        # agent variables
        self.env=Environment(self.display_surface,self.settings)
        self.neuralnetwork=NeuralNet(self.learning_rate,self.gamma,11,128,3)
        if self.settings['load_pretrained']:
            self.neuralnetwork.model=tf.keras.models.load_model(os.path.join('AI','models','snakeAi.h5'))
        # self.neuralnetwork.model.summary()
        self.neuralnetwork.compile(
            optimizer=self.settings['optimizer'],
            loss=self.settings['loss']
        )

    def get_state(self):
        '''
            returns 13 state values for the snake: [
            danger_left, danger_straight, danger_right,danger_straightright,danger_straightleft,
            direction_up, direction_right, direction_down, direction_left,
            food_up, food_right, food_down, food_left
        ]
        '''
        snake=self.env.snake
        apple=self.env.apple
        direction_up=snake.direction=='up'
        direction_down=snake.direction=='down'
        direction_right=snake.direction=='right'
        direction_left=snake.direction=='left'

        left_square_x=snake.xhead-self.settings['pixels']
        left_square_y=snake.yhead
        right_square_x=snake.xhead+self.settings['pixels']
        right_square_y=snake.yhead
        up_square_x=snake.xhead
        up_square_y=snake.yhead-self.settings['pixels']
        down_square_x=snake.xhead
        down_square_y=snake.yhead+self.settings['pixels']    

        danger_straight=(
            direction_left and (snake.wall_collision(left_square_x,left_square_y) or snake.body_collision(left_square_x,left_square_y)) or
            direction_up and (snake.wall_collision(up_square_x,up_square_y) or snake.body_collision(up_square_x,up_square_y)) or
            direction_right and (snake.wall_collision(right_square_x,right_square_y) or snake.body_collision(right_square_x,right_square_y)) or
            direction_down and (snake.wall_collision(down_square_x,down_square_y) or snake.body_collision(down_square_x,down_square_y))
        )
        danger_left=(
            direction_left and (snake.wall_collision(down_square_x,down_square_y) or snake.body_collision(down_square_x,down_square_y)) or
            direction_up and (snake.wall_collision(left_square_x,left_square_y) or snake.body_collision(left_square_x,left_square_y)) or
            direction_right and (snake.wall_collision(up_square_x,up_square_y) or snake.body_collision(up_square_x,up_square_y)) or
            direction_down and (snake.wall_collision(right_square_x,right_square_y) or snake.body_collision(right_square_x,right_square_y))
        )
        danger_right=(
            direction_left and (snake.wall_collision(up_square_x,up_square_y) or snake.body_collision(up_square_x,up_square_y)) or
            direction_up and (snake.wall_collision(right_square_x,right_square_y) or snake.body_collision(right_square_x,right_square_y)) or
            direction_right and (snake.wall_collision(down_square_x,down_square_y) or snake.body_collision(down_square_x,down_square_y)) or
            direction_down and (snake.wall_collision(left_square_x,left_square_y) or snake.body_collision(left_square_x,left_square_y))
        )

        food_left=apple.xpos<snake.xhead
        food_right=apple.xpos>snake.xhead
        food_up=apple.ypos<snake.yhead
        food_down=apple.ypos>snake.yhead

        return np.array([
            danger_left, danger_straight, danger_right,
            direction_up, direction_right, direction_down, direction_left,
            food_up, food_right, food_down, food_left
        ])

    # tradeoff: exploration / exploitation
    def get_action(self,state):
        self.epsilon=50-self.games
        move=[0,0,0]
        if random.randint(0,200)<self.epsilon:
            move[random.randint(0,2)]=1
        else:
            state=np.expand_dims(np.array(state,dtype=np.float32),0)
            pred=self.neuralnetwork.model.predict(state,verbose=0)[0]
            move[np.argmax(pred,axis=0)]=1
        return move

    def train_short_memory(self,state,action,reward,next_state,game_over):
        self.neuralnetwork.train_step(state,action,reward,next_state,game_over)

    def train_long_memory(self):
        if len(self.memory)>self.batch_size:
            batch=random.sample(self.memory,self.batch_size)
        else:
            batch=self.memory
        states, actions, rewards, next_states, game_overs = zip(*batch)
        self.neuralnetwork.train_step(states, actions, rewards, next_states, game_overs)
    
    def remember(self,state,action,reward,next_state,game_over):
        self.memory.append((state,action,reward,next_state,game_over))

    def get_command(self,action):
        if action[0]:
            return 'left'
        elif action[1]:
            return 'straight'
        else:
            return 'right'

    def record_statistics(self,scores_data):
        self.score_dataframe['Score'].append(scores_data)
    
    def update_model(self,score):
        if score>self.best_score:
            self.best_score=score
            self.neuralnetwork.save_model()