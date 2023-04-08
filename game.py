import pygame

class Game:
    def __init__(self,settings):
        self.settings=settings

    def draw(self,display_surface):
        display_surface.fill(self.settings['bg_primary'])
    
    def run(self,display_surface):
        self.draw(display_surface)