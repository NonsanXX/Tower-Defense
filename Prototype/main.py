import pygame
import constant as c
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import os

# Initialize pygame game
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("WOTD")

# game variable
is_fast_forward = False
game_over = False
game_outcome = 0 # -1 lost and 1 is win
level_started = False
last_enemy_spawn = pygame.time.get_ticks()
placing_turret = False
selected_turret = False

# load image
map_image = pygame.image.load(os.path.join("Prototype", "levels", "level.png"))
cursor_turret = pygame.image.load(os.path.join("Prototype", "assets", "images", "turrets", "cursor_turret.png"))
buy_turret_image = pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "buy_turret.png"))
cancel_turret_image = pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "cancel.png"))
upgrade_turret_image = pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "upgrade_turret.png"))
begin_image = pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "begin.png"))
restart_image = pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "restart.png"))
fast_forward_image = pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "fast_forward.png"))
# load gui
coin_gui = pygame.image.load(os.path.join("Prototype", "assets", "images", "gui", "coin.png"))
heart_gui = pygame.image.load(os.path.join("Prototype", "assets", "images", "gui", "heart.png"))
logo_gui = pygame.image.load(os.path.join("Prototype", "assets", "images", "gui", "logo.png"))
#load sound
shot_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "shot.wav"))
shot_fx.set_volume(0.5)

# enemy
enemy_images = {
    "weak" : pygame.image.load(os.path.join("Prototype", "assets", "images", "enemies", "enemy_1.png")),
    "medium" : pygame.image.load(os.path.join("Prototype", "assets", "images", "enemies", "enemy_2.png")),
    "strong" : pygame.image.load(os.path.join("Prototype", "assets", "images", "enemies", "enemy_3.png")),
    "elite" : pygame.image.load(os.path.join("Prototype", "assets", "images", "enemies", "enemy_4.png"))
}

# turret sprite sheet # turret animation
turret_spreadsheet = []
for x in range(1, c.TURRET_LEVEL+1):
    turret_sheet = pygame.image.load(os.path.join("Prototype", "assets", "images", "turrets", "turret_%d.png"%x))
    turret_spreadsheet.append(turret_sheet)

# load json data
with open(os.path.join("Prototype", "levels", "level.tmj")) as file:
    world_data = json.load(file)

# load font for displaing text in screen
text_font = pygame.font.SysFont("Consolas", 24, bold = True)
large_font = pygame.font.SysFont("Consolas", 36)

# function for text on screen
def draw_text(text, font, color, coor):
    img = font.render(text, True, color)
    screen.blit(img, coor)

def display_data():
    # draw panel
    pygame.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
    pygame.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 2)
    screen.blit(logo_gui, (c.SCREEN_WIDTH, 400))

    #display data
    draw_text("LEVEL: %d"%world.level, text_font, "grey100", (c.SCREEN_WIDTH + 10, 10))
    screen.blit(heart_gui, (c.SCREEN_WIDTH + 10, 35))
    draw_text(str(world.health), text_font, "grey100", (c.SCREEN_WIDTH + 50, 40))
    screen.blit(coin_gui, (c.SCREEN_WIDTH + 10, 65))
    draw_text(str(world.money), text_font, "grey100", (c.SCREEN_WIDTH + 50, 70))
    


def create_turret(pos):
    mouse_tile_x = pos[0] // c.TILE_SIZE
    mouse_tile_y = pos[1] // c.TILE_SIZE
    # calculate sequence in json tile_map
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 7:
        # check if already placed
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free:
            new_turret = Turret(turret_spreadsheet, mouse_tile_x, mouse_tile_y, shot_fx)
            turret_group.add(new_turret)

            # losing money
            world.money -= c.BUY_COST

def select_turret(pos):
    mouse_tile_x = pos[0] // c.TILE_SIZE
    mouse_tile_y = pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret
        
def deselect_turret():
    for turret in turret_group:
        turret.selected = False

#create group
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

#create world
world = World(world_data, map_image)
world.process_data()
world.process_enemy()


waypoint = world.waypoint

# create button
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_turret_image, True)
upgrade_button = Button(c.SCREEN_HEIGHT + 5, 180, upgrade_turret_image, True)
begin_button = Button(c.SCREEN_HEIGHT + 60, 300, begin_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_forward_button = Button(c.SCREEN_HEIGHT + 60, 300, fast_forward_image, True)

run = True

while run:
    clock.tick(c.FPS)

    #####################
    # UPDATING SECTION
    #####################
    if is_fast_forward:
        world.game_speed = 2
    else:
        world.game_speed = 1
    if not game_over:
        # check if player is lost
        if world.health <= 0:
            game_over = True
            game_outcome = -1 # lost
        # check if player is win
        if world.level > c.TOTAL_LEVEL:
            game_over = True
            game_outcome = 1 # win

        enemy_group.update(world)
        turret_group.update(enemy_group, world)

        # Highlight selected turret
        if selected_turret:
            selected_turret.selected = True

    #####################
    # DRAW SECTION
    #####################
    world.draw(screen)

    # draw group of enemies
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    display_data()

    if not game_over:
        # check if level started
        if not level_started:
            time_begin = pygame.time.get_ticks()
            if begin_button.draw(screen):
                level_started = True
        else:
            # Fast forward option
            if pygame.time.get_ticks() - time_begin > 100:
                if fast_forward_button.draw(screen):
                    is_fast_forward = not is_fast_forward
            # Spawn enemies
            if pygame.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN / world.game_speed:
                if world.spawned_enemy < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemy]
                    enemy = Enemy(enemy_type, waypoint, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemy += 1
                    last_enemy_spawn = pygame.time.get_ticks()

        # check if complete wave
        if world.check_level_complete():
            world.money += c.LEVEL_COMPLETE_REWARD
            world.level += 1
            level_started = False
            last_enemy_spawn = pygame.time.get_ticks()
            world.reset_level()
            world.process_enemy()

        # draw button
        # for turret button show cost
        draw_text(str(c.BUY_COST), text_font, "grey100", (c.SCREEN_WIDTH + 215, 135))
        screen.blit(coin_gui, (c.SCREEN_WIDTH + 260, 130))
        if turret_button.draw(screen):
            placing_turret = True

        if placing_turret:
            # show cursor
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pygame.mouse.get_pos()
            cursor_rect.center = cursor_pos
            screen.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(screen):
                placing_turret = False
        # show upgrade if turret is selected
        if selected_turret:
            # check if turret can be upgraded
            if selected_turret.upgrade_level < c.TURRET_LEVEL:
                # show cost of an upgrade button
                draw_text(str(c.UPGRADE_COST), text_font, "grey100", (c.SCREEN_WIDTH + 215, 195))
                screen.blit(coin_gui, (c.SCREEN_WIDTH + 260, 190))
                if upgrade_button.draw(screen):
                    if world.money >= c.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= c.UPGRADE_COST
    else:
        pygame.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "grey0", (310, 230))
        if game_outcome == 1:
            draw_text("YOU WIN!", large_font, "grey0", (315, 230))
        
        # restart level
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            placing_turret = False
            selected_turret = None
            last_enemy_spawn = pygame.time.get_ticks()
            
            #reset world
            world = World(world_data, map_image)
            world.process_data()
            world.process_enemy()

            #empty group
            enemy_group.empty()
            turret_group.empty()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            #check if mouse in screen
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                selected_turret = None
                deselect_turret()
                if placing_turret:
                    # if have enough money
                    if world.money >= c.BUY_COST:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)
    pygame.display.update()
pygame.quit()