import pygame
from AI.apple import Apple
from AI.snake import Snake

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