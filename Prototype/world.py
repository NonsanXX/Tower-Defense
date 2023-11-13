import pygame
from enemy_data import ENEMY_SPAWN_DATA
from random import shuffle
import config as c
class World():
    def __init__(self, data, map_image, backg_fx):
        self.level = 1
        self.difficulty = 1
        self.game_speed = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.waypoint = []
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemy = 0
        self.killed_enemy = 0
        self.missed_enemy = 0
        self.backg_fx = backg_fx

    def process_data(self):
        #look though data to extract
        for layer in self.level_data["layers"]:
            self.backg_fx.play()
            if layer["name"] == "field":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    self.process_waypoint(obj["polyline"])

    def process_waypoint(self, data):
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoint.append((temp_x, temp_y))

    def check_level_complete(self):
        if self.killed_enemy + self.missed_enemy == len(self.enemy_list):
            if not self.level % c.TOTAL_LEVEL:
                self.difficulty += 0.5
            return True

    def reset_level(self):
        # reset enemy varible
        self.enemy_list = []
        self.spawned_enemy = 0
        self.killed_enemy = 0
        self.missed_enemy = 0

    def draw(self, surface):
        surface.blit(self.image, (0,0))

    def process_enemy(self):
        enemies = ENEMY_SPAWN_DATA[(self.level - 1)%c.TOTAL_LEVEL]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            self.enemy_list.extend([enemy_type]*enemies_to_spawn)            
        
        # shuffle list
        shuffle(self.enemy_list)
