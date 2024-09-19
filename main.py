import sys

import pygame
from scripts.util import load_image

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Croco-smack')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {'background': load_image('background.png'),
                       'player': load_image('character/Soldier-Attack1.png')}

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))
            self.display.blit(self.assets['player'], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()