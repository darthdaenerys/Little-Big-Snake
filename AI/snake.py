import pygame,random,os

class SnakeBody:
    def __init__(self,pixels,xpos,ypos,colour):
        self.colour=colour
        self.xpos=xpos
        self.ypos=ypos
        self.pixels=pixels

    def draw(self,display_surface):
        pygame.draw.rect(display_surface,self.colour,(self.xpos,self.ypos,self.pixels,self.pixels))
