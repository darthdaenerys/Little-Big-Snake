import pygame,os
from apple import Apple
from snake import Snake

class Game:
    def __init__(self,settings):
        self.settings=settings
        self.snake=Snake(settings)
        self.apple=Apple(settings,self.snake.bodies)
        self.score=0
        self.flag=1
        self.difficulty=8
        self.font=pygame.font.SysFont('subatomic.ttf',50,bold=True)
        self.eat_sound=pygame.mixer.Sound(os.path.join('sfx','sip-short-soft-soup.wav'))
        self.game_over_sound=pygame.mixer.Sound(os.path.join('sfx','game-over-arcade.wav'))

    def draw(self,display_surface):
        display_surface.fill(self.settings['bg_primary'])
        pixels=self.settings['pixels']
        for row in range(self.settings['window_height']//pixels):
            for col in range(self.settings['window_width']//pixels):
                if (row+col)%2==0:
                    pygame.draw.rect(display_surface,self.settings['bg_secondary'],(col*pixels,row*pixels,pixels,pixels))
    
    def render_font(self,display_surface):
        font_surface=self.font.render(f'Score: {self.score}',True,(255,255,255))
        display_surface.blit(font_surface,(10,10))
    
    def game_over(self,display_surface):
        font_surface=self.font.render(f'GAME OVER',True,(255,255,255))
        font_rect=font_surface.get_rect()
        font_rect.center=(self.settings['window_width']//2,self.settings['window_height']//2)
        display_surface.blit(font_surface,font_rect)
        pygame.display.update()
        self.game_over_sound.play()
        pygame.time.delay(1000)
        self.__init__(self.settings)
    
    def run(self,display_surface):
        self.draw(display_surface)
        self.snake.update(display_surface)
        if self.snake.direction!='None':
            if self.snake.wall_collision() or self.snake.snake_collision():
                self.game_over(display_surface)
            if self.snake.apple_collision(self.apple):
                self.snake.add_body()
                self.apple.spawn(self.snake.bodies)
                self.score+=1
                self.eat_sound.play()
                self.flag=1
        self.apple.update(display_surface,self.snake)
        self.render_font(display_surface)