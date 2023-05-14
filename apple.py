import pygame,random,os

class Apple:
    def __init__(self,settings,bodies):
        self.settings=settings
        self.colour=self.settings['apple_colour']
        self.surface=pygame.image.load(os.path.join('graphics','apple.png')).convert_alpha()
        self.surface=pygame.transform.scale(self.surface,(self.settings['pixels'],self.settings['pixels']))
        self.rect=self.surface.get_rect()

    def draw(self,display_surface:pygame.Surface):
        display_surface.blit(self.surface,self.rect)
    
    def update(self,display_surface,snake):
        self.draw(display_surface)