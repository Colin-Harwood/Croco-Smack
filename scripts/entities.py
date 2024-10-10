import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down':False, 'left': False, 'right': False}
        self.jump = 1

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('run')

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
    
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down':False, 'left': False, 'right': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        if self.collisions['down']:
            self.jump = 1

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        # surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'character', pos, size)
        self.air_time = 0
        self.attacking = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0

        if not self.attacking:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        else:
            self.set_action('attack')

        if self.attacking > 0:
            self.attacking = max(0, self.attacking - 1)

    def rect(self):
        if not self.attacking:
            return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        else:
            #update so that the hitbox starts further along the pplayer and so that the player back sword awing and above isnt counted as part of hihtbox
            #also player images need resized to be size of the biggest needed measurements so that the hitbox casn be a constant amount forward and down
            return pygame.Rect(self.pos[0], self.pos[1], self.size[0] + 8, self.size[1] + 5)

#attack lasts for a certain amount of time, but in that time the player can still move so play the animation for that certain amount of time and still let the player move.
#Also have the player only face one direction during the attack and increase the hitbox to the shovel length and let the player be in attack mode
    def attack(self):
        if not self.attacking:
            self.attacking += 30
