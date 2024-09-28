import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down':False, 'left': False, 'right': False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def update(self, movement=(0, 0)):
        entity_rect = self.rect()

        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        self.pos[0] += movement[0]
        self.pos[1] += self.velocity[1]

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))