import sys

import pygame
from scripts.util import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Croc
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Croco-smack')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
                        'background': load_image('background.png'),
                       'player': load_image('character/Soldier-Attack1.png'),
                       'character/run': Animation(load_images('character/walk'), img_dur=9),
                       'character/attack': Animation(load_images('character/attack'), img_dur=6),
                       'character/idle': Animation(load_images('character/idle'), img_dur=6),
                       'character/jump': Animation(load_images('character/jump'), img_dur=6),
                       'croc/run': Animation(load_images('croc/walk'), img_dur=8),
                       'croc/die': Animation(load_images('croc/die'), img_dur=6, loop=False),
                       'decor': load_images('tiles/decor'),
                        'grass': load_images('tiles/grass'),
                        'large_decor': load_images('tiles/large_decor'),
                        'stone': load_images('tiles/stone')
                        }
        
        self.player = Player(self, (0, 0), (13, 18))
        self.croc = Croc(self, (20, 0), (18, 14))

        self.tilemap = Tilemap(self, 16)

        self.scroll = [0, 0]

        self.enemies = []

        self.load_level()

    def load_level(self):
        self.tilemap.load('map.json')

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Croc(self, spawner['pos'], (18, 14)))

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            if not len(self.enemies):
                self.load_level()

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, render_scroll)

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap, (0, 0), self.player)
                enemy.render(self.display, offset=render_scroll)
                if enemy.animation.done:
                    self.enemies.remove(enemy)
                if enemy.killedPlayer:
                    self.load_level()

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP and self.player.jump > 0:
                        self.player.velocity[1] = -3
                        self.player.jump = 0
                    if event.key == pygame.K_c:
                        self.player.attack()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                        
                
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()