import pygame
import constant as c
from turret_data import TURRET_DATA
import math
class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheets, tile_x, tile_y, shot_fx):
        pygame.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level - 1]["range"]
        self.cooldown = TURRET_DATA[self.upgrade_level - 1]["cooldown"]
        self.damage = TURRET_DATA[self.upgrade_level - 1]["damage"]
        self.last_shot = pygame.time.get_ticks()
        self.shot_fx = shot_fx
        self.selected = False
        self.target = None

        # posi var
        self.tile_x = tile_x
        self.tile_y = tile_y
        # calc center coor
        self.x = (tile_x+0.5) * c.TILE_SIZE
        self.y = (tile_y+0.5) * c.TILE_SIZE

        # animation var
        self.sprite_sheets = sprite_sheets
        self.animaion_list = self.load_image(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Update img section
        self.angle = 90
        self.original_image = self.animaion_list[self.frame_index]
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # show range
        self.range_image = pygame.Surface((self.range*2, self.range*2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_image(self, sprite_sheet):
        # to extract image from spritesheet
        size = sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEP):
            temp_img = sprite_sheet.subsurface(x*size, 0, size, size)
            animation_list.append(temp_img)

        return animation_list
    
    def update(self, enemy_group, world):
        if self.target:
            self.play_animation()
        else:
            if pygame.time.get_ticks() - self.last_shot > self.cooldown / world.game_speed:
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        # find an enemy to target
        x_dist = 0
        y_dist = 0
        # check distance to each enemy to see if it in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist**2 + y_dist**2)
                if dist <= self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))

                    # Play sound
                    self.shot_fx.play()
                    
                    # Damage enemy
                    self.target.health -= self.damage
                    break

    def play_animation(self):
        # update
        self.original_image = self.animaion_list[self.frame_index]
        # check time
        if pygame.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animaion_list):
                self.frame_index = 0
                self.last_shot = pygame.time.get_ticks()
                self.target = None

    def upgrade(self):
        self.upgrade_level += 1
        self.range = TURRET_DATA[self.upgrade_level - 1]["range"]
        self.cooldown = TURRET_DATA[self.upgrade_level - 1]["cooldown"]
        self.damage = TURRET_DATA[self.upgrade_level - 1]["damage"]

        # update turret image
        self.animaion_list = self.load_image(self.sprite_sheets[self.upgrade_level - 1])
        self.original_image = self.animaion_list[self.frame_index]

        # update range circle
        self.range_image = pygame.Surface((self.range*2, self.range*2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        