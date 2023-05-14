import pygame,random,os

class Apple:
    def __init__(self,settings,bodies):
        self.settings=settings
        self.colour=self.settings['apple_colour']
        self.surface=pygame.image.load(os.path.join('graphics','apple.png')).convert_alpha()
        self.surface=pygame.transform.scale(self.surface,(self.settings['pixels'],self.settings['pixels']))
        self.rect=self.surface.get_rect()
        self.spawn(bodies)
    
    def spawn(self,bodies):
        while True:
            flag=True
            self.xpos=random.randrange(0,self.settings['window_width'],self.settings['pixels'])
            self.ypos=random.randrange(0,self.settings['window_height'],self.settings['pixels'])
            for body in bodies:
                if body.xpos==self.xpos and body.ypos==self.ypos:
                    flag=False
                    break
            if flag: break
        self.rect.topleft=(self.xpos,self.ypos)

    def draw(self,display_surface:pygame.Surface):
        display_surface.blit(self.surface,self.rect)
    
    def update(self,display_surface,snake):
        self.draw(display_surface)