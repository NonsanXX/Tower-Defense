import pygame
from pygame.math import Vector2
from enemy_data import ENEMY_DATA
import math
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, waypoint, images):
        pygame.sprite.Sprite.__init__(self)
        self.waypoint = waypoint
        self.pos = Vector2(self.waypoint[0])
        self.target_waypoint = 1

        self.health = ENEMY_DATA[enemy_type]["health"]
        self.speed = ENEMY_DATA[enemy_type]["speed"]
        self.reward = ENEMY_DATA[enemy_type]["reward"]

        self.angle = 0
        self.original_image = pygame.transform.scale(images[enemy_type], (180, 180))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)
    
    def move(self, world):
        # define a target waypoint
        if self.target_waypoint >= len(self.waypoint):
            # if enemy reach the end of the path
            self.kill()
            world.health -= self.health
            world.money += self.reward
            world.missed_enemy += 1            
            return
        self.target = Vector2(self.waypoint[self.target_waypoint])
        self.movement = self.target - self.pos

        #calc distance
        dist = self.movement.length()
        if dist <= self.speed * world.game_speed:
            self.target_waypoint += 1
        
        self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        self.rect.center = self.pos

    def rotate(self):
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def check_alive(self, world):
        if self.health <= 0:
            world.money += self.reward
            world.killed_enemy += 1
            self.kill()