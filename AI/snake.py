import pygame,random,os

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
        self.direction=random.choice(['left','right','up','down'])
        self.bodies=[]
        self.speed=settings['pixels']
        self.delta=settings['skin_gradient_roughness']
        self.settings=settings
        self.xhead=random.randrange(0,settings['window_width'],settings['pixels'])
        self.yhead=random.randrange(0,settings['window_height'],settings['pixels'])
        self.body_colour=random.choice(settings['skin_colour'])
        self.eat_sound=pygame.mixer.Sound(os.path.join('sfx','sip-short-soft-soup.wav'))
        self.game_over_sound=pygame.mixer.Sound(os.path.join('sfx','game-over-arcade.wav'))

    def update_direction(self,action):
        if self.direction=='left':
            if action=='left':
                self.direction='down'
            elif action=='right':
                self.direction='up'
        elif self.direction=='up':
            if action=='left':
                self.direction='left'
            elif action=='right':
                self.direction='right'
        elif self.direction=='right':
            if action=='left':
                self.direction='up'
            elif action=='right':
                self.direction='down'
        else:
            if action=='left':
                self.direction='left'
            elif action=='right':
                self.direction='right'
    
    def move_head(self):
        if self.direction=='up':
            self.yhead-=self.speed
        elif self.direction=='down':
            self.yhead+=self.speed
        elif self.direction=='right':
            self.xhead+=self.speed
        elif self.direction=='left':
            self.xhead-=self.speed
    
    def move_body(self):
        for body_idx in range(len(self.bodies)-1,-1,-1):
            if body_idx==0:
                self.bodies[body_idx].xpos=self.xhead
                self.bodies[body_idx].ypos=self.yhead
            else:
                self.bodies[body_idx].xpos=self.bodies[body_idx-1].xpos
                self.bodies[body_idx].ypos=self.bodies[body_idx-1].ypos
    
    def add_body(self):
        body=SnakeBody(self.settings['pixels'],self.xhead,self.yhead,self.body_colour)
        self.bodies.append(body)
        self.body_colour=self.body_colour+self.delta
        self.delta=-self.delta if self.body_colour==255 else self.delta
    
    def apple_collision(self,apple):
        if self.xhead==apple.xpos and self.yhead==apple.ypos:
            self.eat_sound.play()
            return True
        return False
    
    def wall_collision(self,xhead,yhead):
        return xhead<0 or xhead>=self.settings['window_width'] or yhead<0 or yhead>=self.settings['window_height']
    
    def body_collision(self,xhead,yhead):
        for body in self.bodies:
            if body.xpos==xhead and body.ypos==yhead:
                return True
        return False

    def draw(self,display_surface):
        rect=pygame.rect.Rect(self.xhead,self.yhead,self.settings['pixels'],self.settings['pixels'])
        rect=rect.inflate(6,6)
        pygame.draw.rect(display_surface,self.body_colour,rect)
        for body in self.bodies:
            body.draw(display_surface)

    def update(self,display_surface,action):
        self.update_direction(action)
        self.move_body()
        self.move_head()
        self.draw(display_surface)