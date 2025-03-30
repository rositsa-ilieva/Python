import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'flame': pygame.mixer.Sound('images/audio/heal.wav'),
            'heal':  pygame.mixer.Sound('images/audio/flame.wav')
        }
        
        self.sounds['heal'].set_volume(0.8)
        self.sounds['heal'].set_volume(0.4)

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.info['health']:
                player.health = player.info['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center, groups)


    def flame(self, player, cost, groups):
        if player.energy >= cost:
            self.sounds['flame'].play()
            player.energy -= cost

            if player.status.split('_')[0] == 'right':
                dir= pygame.math.Vector2(1,0)
            if player.status.split('_')[0] == 'left':
                dir= pygame.math.Vector2(-1,0)
            if player.status.split('_')[0] == 'up':
                dir= pygame.math.Vector2(0,-1)
            if player.status.split('_')[0] == 'down':
                dir= pygame.math.Vector2(0,1)

            for i in range(1,6):
                if dir.x:
                    offset_x = (dir.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE//3, TILESIZE//3)
                    y = player.rect.centery + randint(-TILESIZE//3, TILESIZE//3)
                    self.animation_player.create_particles('flame', (x,y), groups)
                else:
                    offset_y = (dir.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE//3, TILESIZE//3)
                    y = player.rect.centery + offset_y  + randint(-TILESIZE//3, TILESIZE//3)
                    self.animation_player.create_particles('flame', (x,y), groups)