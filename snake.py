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
        self.previous_direction=None
        self.xhead=random.randrange(0,settings['window_width'],settings['pixels'])
        self.yhead=random.randrange(0,settings['window_height'],settings['pixels'])
        self.body_colour=random.choice(settings['skin_colour'])

    def input(self):
        keys=pygame.key.get_pressed()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not self.direction=='left' and self.previous_direction!='left':
            self.direction='right'
            self.previous_direction='None'
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not self.direction=='right' and self.previous_direction!='right':
            self.direction='left'
            self.previous_direction='None'
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and not self.direction=='down' and self.previous_direction!='down':
            self.direction='up'
            self.previous_direction='None'
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not self.direction=='up' and self.previous_direction!='up':
            self.direction='down'
            self.previous_direction='None'
        elif keys[pygame.K_p] and self.previous_direction=='None':
            self.previous_direction=self.direction
            self.direction='None'

    def move_head(self):
        if self.direction=='up':
            self.yhead-=self.speed
        elif self.direction=='down':
            self.yhead+=self.speed
        elif self.direction=='right':
            self.xhead+=self.speed
        elif self.direction=='left':
            self.xhead-=self.speed

    def draw(self,display_surface):
        rect=pygame.rect.Rect(self.xhead,self.yhead,self.settings['pixels'],self.settings['pixels'])
        rect=rect.inflate(6,6)
        pygame.draw.rect(display_surface,self.body_colour,rect)

    def update(self,display_surface):
        self.draw(display_surface)