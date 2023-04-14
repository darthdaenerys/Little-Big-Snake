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
        self.settings=settings
        self.xhead=random.randrange(0,settings['window_width'],settings['pixels'])
        self.yhead=random.randrange(0,settings['window_height'],settings['pixels'])

    def draw(self,display_surface):
        rect=pygame.rect.Rect(self.xhead,self.yhead,self.settings['pixels'],self.settings['pixels'])