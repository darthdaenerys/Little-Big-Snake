import pygame,random

class SnakeBody:
    def __init__(self,pixels,xpos,ypos,colour):
        self.colour=colour
        self.xpos=xpos
        self.ypos=ypos
        self.pixels=pixels

    def draw(self,display_surface):
        pygame.draw.rect(display_surface,self.colour,(self.xpos,self.ypos,self.pixels,self.pixels))

class Snake:
    def __init__(self,settings):
        self.direction='None'
        self.speed=settings['pixels']
        self.delta=settings['skin_gradient_roughness']
        self.settings=settings
        self.xhead=random.randrange(0,settings['window_width'],settings['pixels'])
        self.yhead=random.randrange(0,settings['window_height'],settings['pixels'])

    def input(self):
        keys=pygame.key.get_pressed()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not self.direction=='left' and self.previous_direction!='left':
            self.direction='right'
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not self.direction=='right' and self.previous_direction!='right':
            self.direction='left'
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and not self.direction=='down' and self.previous_direction!='down':
            self.direction='up'

    def draw(self,display_surface):
        rect=pygame.rect.Rect(self.xhead,self.yhead,self.settings['pixels'],self.settings['pixels'])