import sys

import pygame
from scripts.util import load_image
from scripts.entities import PhysicsEntity

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Croco-smack')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {'background': load_image('background.png'),
                       'player': load_image('character/Soldier-Attack1.png')}
        
        self.player = PhysicsEntity(self, 'player', (0, 0), (15, 18))

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                        
                
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()