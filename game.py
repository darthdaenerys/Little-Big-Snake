import pygame

class Game:
    def __init__(self,settings):
        self.settings=settings
        self.score=0

    def draw(self,display_surface):
        display_surface.fill(self.settings['bg_primary'])
        pixels=self.settings['pixels']
        for row in range(self.settings['window_height']//pixels):
            for col in range(self.settings['window_width']//pixels):
                if (row+col)%2==0:
                    pygame.draw.rect(display_surface,self.settings['bg_secondary'],(col*pixels,row*pixels,pixels,pixels))
    
    def run(self,display_surface):
        self.draw(display_surface)