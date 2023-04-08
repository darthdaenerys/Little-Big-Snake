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

if __name__=='__main__':
    main=Main()