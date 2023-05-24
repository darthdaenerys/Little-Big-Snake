import pygame,json,sys,os
from AI.apple import Apple
from AI.snake import Snake
import pandas as pd

class Environment:
    def __init__(self,display_surface,settings):
        self.settings=settings
        self.display_surface=display_surface
        self.clock=pygame.time.Clock()
        self.frame_iteration=0
        self.apple=Apple(self.settings)
        self.snake=Snake(self.settings)
        self.score=0
        self.font=pygame.font.SysFont('subatomic.ttf',50,bold=True)

    def reset(self):
        self.__init__(self.display_surface,self.settings)

    def draw(self):
        self.display_surface.fill(self.settings['bg_primary'])
        pixels=self.settings['pixels']
        for row in range(self.settings['window_height']//pixels):
            for col in range(self.settings['window_width']//pixels):
                if (row+col)%2==0:
                    pygame.draw.rect(self.display_surface,self.settings['bg_secondary'],(col*pixels,row*pixels,pixels,pixels))

    def render_stats(self,game_num,score,best_score):
        label=self.font.render(f'Game: {game_num}',True,(0,0,0))
        self.display_surface.blit(label,(10,10))
        label=self.font.render(f'Score: {score}',True,(0,0,0))
        self.display_surface.blit(label,(10,45))
        label=self.font.render(f'Best score: {best_score}',True,(0,0,0))
        self.display_surface.blit(label,(10,80))

    def step(self,action,agent,games,neuralnetwork):
        game_over=False
        reward=0
        self.frame_iteration+=1
        self.clock.tick(120)
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_q):
                self.settings['games']=games
                dataframe=None
                if self.settings['load_pretrained']:
                    if os.path.exists(os.path.join('AI','data.csv')):
                        dataframe=pd.read_csv(os.path.join('AI','data.csv'))
                        dataframe=pd.concat([dataframe,pd.DataFrame(agent.score_dataframe)],axis=0)
                        self.settings['best_score']=max(agent.best_score,self.settings['best_score'])
                else:
                    dataframe=pd.DataFrame(agent.score_dataframe)
                    self.settings['best_score']=agent.best_score
                dataframe.to_csv(os.path.join('AI','data.csv'),index=False)
                neuralnetwork.save_model()
                obj=json.dumps(self.settings,indent=4)
                with open(os.path.join('AI','settings.json'),'w') as f:
                    f.write(obj)
                    f.close()
                pygame.quit()
                sys.exit()

        self.draw()
        self.snake.update(self.display_surface,action)
        if (self.snake.wall_collision(self.snake.xhead,self.snake.yhead) or self.snake.body_collision(self.snake.xhead,self.snake.yhead) or agent.iterations>10*len(self.snake.bodies)+200):
            reward=-10
            game_over=True
            self.snake.game_over_sound.play()
            self.render_stats(agent.games,self.score,agent.best_score)
            return game_over,reward,self.score
        if self.snake.apple_collision(self.apple):
            self.snake.add_body()
            self.apple.spawn()
            agent.iterations=0
            self.score+=1
            reward=10
        self.apple.update(self.display_surface)
        self.render_stats(agent.games,self.score,agent.best_score)
        return game_over,reward,self.score