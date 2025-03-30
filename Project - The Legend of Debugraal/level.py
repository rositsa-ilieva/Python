import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.current_attack = None

        self.create_map()

        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layout={
            'trace': import_csv_file('csv_files/csv_trace.csv'),
            'obstacles': import_csv_file('csv_files/csvv_trees.csv'),
            'entities': import_csv_file('csv_files/csvvv_enemies.csv')
        }

        graphics = {
            'obstacles' : import_folder('images/obstacles/')
        }

        for style, layout in layout.items():
            for row_ind, row in enumerate(layout):
                for col_ind, col in enumerate(row):
                    if col != '-1':
                        x = col_ind * TILESIZE
                        y = row_ind * TILESIZE
                        if 0 <= x <= WIDTH and 0 <= y <= HEIGTH:
                            if style == 'trace':
                                Tile((x,y), [self.obstacles_sprites], 'invisible')
                            elif style == 'obstacles':
                                x = col_ind * 184
                                y = row_ind * 184
                                obstacle_index = int(col)
                                if 0 <= obstacle_index < len(graphics['obstacles']):
                                    surf = graphics['obstacles'][int(col)]
                                    Tile((x,y),[self.visible_sprites, self.obstacles_sprites], 'obstacles', surf)
                            elif style == 'entities':
                                x = col_ind * 184
                                y = row_ind * 184
                                if col == '4':
                                    self.player = Player((x,y),[self.visible_sprites], self.obstacles_sprites, self.create_attack, self.destroy_attack, self.create_magic)
                                else:
                                    if col == '0' : name = 'demons'
                                    elif col == '2': name = 'wraths'
                                    elif col == '1': name = 'beasts'
                                    Enemy(name, (x,y), [self.visible_sprites, self.attackable_sprites], self.obstacles_sprites, self.damage_player, self.trigger_death_particles, self.add_exp)
                         
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sp in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sp, self.attackable_sprites, False)
                if collision_sprites:
                    for target in collision_sprites:
                        target.get_damage(self.player, attack_sp.sprite_type)

    def damage_player(self, amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount

            if self.player.health <= 0:
                self.player.health = 0
                self.player_die()

            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def player_die(self):
        print("Game Over!")
        self.game_paused = True

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,[self.visible_sprites])

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def add_exp(self,amount):
	    self.player.exp += amount


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load('images/floor2.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
        

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = (self.floor_rect.x - self.offset.x, self.floor_rect.y - self.offset.y)
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
       
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for en in enemy_sprites:
            en.enemy_update(player)
