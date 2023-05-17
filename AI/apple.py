import pygame,random,os

class Apple:
    def __init__(self,settings):
        self.settings=settings
        self.surface=pygame.image.load(os.path.join('graphics','apple.png')).convert_alpha()
        self.surface=pygame.transform.scale(self.surface,(self.settings['pixels'],self.settings['pixels']))
        self.rect=self.surface.get_rect()
        self.spawn()
    
    def spawn(self):
        self.xpos=random.randrange(0,self.settings['window_width'],self.settings['pixels'])
        self.ypos=random.randrange(0,self.settings['window_height'],self.settings['pixels'])
        self.rect.topleft=(self.xpos,self.ypos)

    def draw(self,display_surface:pygame.Surface):
        display_surface.blit(self.surface,self.rect)
    
    def update(self,display_surface):
        self.draw(display_surface)