import pygame,json,sys
from game import Game

class Main:
    def __init__(self):
        pygame.init()
        f=open('settings.json')
        self.settings=json.load(f)
        f.close()

        self.display_surface=pygame.display.set_mode((self.settings['window_width'],self.settings['window_height']))
        pygame.display.set_caption('Snake')
        self.game=Game(self.settings)
        self.clock=pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(self.game.difficulty)
            
            self.game.run(self.display_surface)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.game.score%self.settings['difficulty_change_rate']==0 and self.game.flag:
                self.game.difficulty+=1
                self.game.flag=0

            # update surface
            pygame.display.update()

if __name__=='__main__':
    main=Main()
    main.run()