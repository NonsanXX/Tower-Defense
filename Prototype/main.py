import pygame
import config as c
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import os

# Initialize pygame game
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1920,1080), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("WOTD")

# game variable
is_fast_forward = False
current_fast_forward_type = 1
game_over = False
game_outcome = 0 # -1 lost and 1 is win
level_started = False
last_enemy_spawn = pygame.time.get_ticks()
placing_turret = False
selected_turret = False
buttoning = False

# load image
map_image = pygame.image.load(os.path.join("Prototype", "levels", "map.png"))
cancel_turret_image = pygame.transform.scale(pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "cancel.png")), (99, 99))
upgrade_turret_image = pygame.transform.scale(pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "upgrade_turret.png")), (250, 250))
begin_image = pygame.transform.scale(pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "begin.png")), (250, 250))
restart_image = pygame.transform.scale(pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "restart.png")), (250, 250))
fast_forward_cancel_image = pygame.transform.scale(pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "FFW_cancel.png")), (99, 99))
fast_forward_x3_image = pygame.transform.scale(pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "FFW_X3.png")), (99, 99))
fast_forward_x5_image = pygame.transform.scale(pygame.image.load(os.path.join("Prototype", "assets", "images", "buttons", "FFW_X5.png")), (99, 99))

# load gui
coin_gui = pygame.transform.scale(pygame.image.load(os.path.join("Prototype", "assets", "images", "gui", "coin.png")), (120, 120))
coin_gui_up = pygame.transform.scale(pygame.image.load(os.path.join("Prototype", "assets", "images", "gui", "coin.png")), (99, 99))
heart_gui = pygame.transform.scale(pygame.image.load(os.path.join("Prototype", "assets", "images", "gui", "heart.png")), (120, 120))
logo_gui = pygame.image.load(os.path.join("Prototype", "assets", "images", "gui", "logo.png"))

#load sound
shot_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "elf", "yorn.wav"))
shot_fx.set_volume(0.5)
arrow_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "elf", "Arrow01.wav"))
arrow_fx.set_volume(0.5)
coss_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "elf", "crossbow02.wav"))
coss_fx.set_volume(0.5)
knight1_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "knight", "1.wav"))
knight1_fx.set_volume(0.5)
knight2_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "knight", "2.wav"))
knight2_fx.set_volume(0.5)
knight3_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "knight", "3.wav"))
knight3_fx.set_volume(0.5)
witch1_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "witch", "1.wav"))
witch1_fx.set_volume(0.5)
witch2_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "witch", "2.wav"))
witch2_fx.set_volume(0.25)
witch3_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "witch", "3.wav"))
witch3_fx.set_volume(0.5)
click_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "button.wav"))
button_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "turret.wav"))
backg_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "bg.wav"))
backg_fx.set_volume(0.05)
upgrade_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "upgrade.wav"))
cancel_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "cancel.wav"))
start_fx = pygame.mixer.Sound(os.path.join("Prototype", "assets", "audio", "start.wav"))
# enemy
enemy_images = {
    "weak" : pygame.image.load(os.path.join("Prototype", "assets", "images", "enemies", "enemy_1.png")),
    "medium" : pygame.image.load(os.path.join("Prototype", "assets", "images", "enemies", "enemy_2.png")),
    "strong" : pygame.image.load(os.path.join("Prototype", "assets", "images", "enemies", "enemy_3.png")),
    "elite" : pygame.image.load(os.path.join("Prototype", "assets", "images", "enemies", "enemy_4.png"))
}

witch_frame = lambda x: len(list(os.scandir(os.path.join("Prototype", "assets", "images", "turrets", "Witch", "Lv%d"%x))))
knight_frame = lambda x: len(list(os.scandir(os.path.join("Prototype", "assets", "images", "turrets", "Knight", "Lv%d"%x))))
elf_frame = lambda x: len(list(os.scandir(os.path.join("Prototype", "assets", "images", "turrets", "Elf", "Lv%d"%x))))

# witch tower
witch_spreadsheet = [[pygame.image.load(os.path.join("Prototype", "assets", "images", "turrets", "Witch", "Lv%d"%level, "Witch%d-%d.png"%(level, frame))) for frame in range(1, witch_frame(level)+1)] for level in range(1, 4)]

# knight tower
knight_spreadsheet = [[pygame.image.load(os.path.join("Prototype", "assets", "images", "turrets", "Knight", "Lv%d"%level, "Knight%d-%d.png"%(level, frame))) for frame in range(1, knight_frame(level)+1)] for level in range(1, 4)]

# elf tower
elf_spreadsheet = [[pygame.image.load(os.path.join("Prototype", "assets", "images", "turrets", "Elf", "Lv%d"%level, "Elf%d-%d.png"%(level, frame))) for frame in range(1, elf_frame(level)+1)] for level in range(1, 4)]

selector = {
    "witch" : witch_spreadsheet,
    "knight" : knight_spreadsheet,
    "elf" : elf_spreadsheet
}

# load json data
with open(os.path.join("Prototype", "levels", "level.tmj")) as file:
    world_data = json.load(file)

# load font for displaing text in screen
text_font = pygame.font.Font("Prototype/assets/fonts/PixelAzureBonds-327Z.ttf", 50)
text_wave = pygame.font.Font("Prototype/assets/fonts/AncientModernTales-a7Po.ttf", 60)
text_win_or_lose = pygame.font.Font("Prototype/assets/fonts/AncientModernTales-a7Po.ttf", 80)

# function for text on screen
def draw_text(text, font, color, coor):
    img = font.render(text, True, color)
    screen.blit(img, coor)
def draw_center_text(text, font, color, eneble, coor):
    img = font.render(text, True, color)
    img_rect = img.get_rect(center=(c.SCREEN_WIDTH/2, c.SCREEN_HEIGHT/2))
    screen.blit(img, (img_rect.x*eneble[0]+coor[0], img_rect.y*eneble[1]+coor[1]))

def display_data():
    #display data
    screen.blit(heart_gui, (10, c.SCREEN_HEIGHT-115))
    draw_text(str(world.health), text_font, "grey100", (125, c.SCREEN_HEIGHT-80))
    screen.blit(coin_gui, (10, 10))
    draw_text(str(world.money), text_font, "grey100", (125, 40))

    draw_center_text("WAVE %s"%(world.level), text_wave, "grey100", (1, 0), (0, 30))

def create_turret(pos, choosing_turret, turret_name):
    mouse_tile_x = pos[0] // c.TILE_SIZE
    mouse_tile_y = pos[1] // c.TILE_SIZE
    # calculate sequence in json tile_map
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 92:
        # check if already placed
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free:
            new_turret = Turret(choosing_turret, mouse_tile_x, mouse_tile_y, shot_fx, turret_name, arrow_fx, coss_fx, knight1_fx,
                                knight2_fx, knight3_fx, witch1_fx, witch2_fx, witch3_fx)
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

def draw_slot(rect):
    pygame.draw.rect(screen, (217, 217, 217), rect, border_radius=25)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2, 25)

def nondeselect(ignore):
    mouse_pos = pygame.mouse.get_pos()
    for button in ignore:
        if button.rect.collidepoint(mouse_pos):
            return True

#create group
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

#create world
world = World(world_data, map_image, backg_fx)
world.process_data()
world.process_enemy()

waypoint = world.waypoint

# create button
cancel_button = Button(c.SCREEN_WIDTH/2-250, c.SCREEN_HEIGHT-100, cancel_turret_image, True, click_fx, button_fx, upgrade_fx, cancel_fx, start_fx)
upgrade_button = Button(c.SCREEN_WIDTH - 300, c.SCREEN_HEIGHT-200, upgrade_turret_image, True, click_fx, button_fx, upgrade_fx, cancel_fx, start_fx)
begin_button = Button(c.SCREEN_WIDTH - 250, -30, begin_image, True, click_fx, button_fx, upgrade_fx, cancel_fx, start_fx)
restart_button = Button(820, 500, restart_image, True, click_fx, button_fx, upgrade_fx, cancel_fx, start_fx)
fast_forward_cancel_button = Button(c.SCREEN_WIDTH/2+150, 10, fast_forward_cancel_image, True, click_fx, button_fx, upgrade_fx, cancel_fx, start_fx)
fast_forward_x3_button = Button(c.SCREEN_WIDTH/2+250, 10, fast_forward_x3_image, True, click_fx, button_fx, upgrade_fx, cancel_fx, start_fx)
fast_forward_x5_button = Button(c.SCREEN_WIDTH/2+350, 10, fast_forward_x5_image, True, click_fx, button_fx, upgrade_fx, cancel_fx, start_fx)

# Draw Slot for selector
witch_selector = Button(c.SCREEN_WIDTH/2-150, c.SCREEN_HEIGHT-100, pygame.transform.scale(witch_spreadsheet[0][0], (99, 99)), True, button_fx, button_fx, upgrade_fx, cancel_fx, start_fx)
knight_selector = Button(c.SCREEN_WIDTH/2-50, c.SCREEN_HEIGHT-100, pygame.transform.scale(knight_spreadsheet[0][0], (99, 99)), True, button_fx, button_fx, upgrade_fx, cancel_fx, start_fx)
elf_selector = Button(c.SCREEN_WIDTH/2+50, c.SCREEN_HEIGHT-100, pygame.transform.scale(elf_spreadsheet[0][0], (99, 99)), True, button_fx, button_fx, upgrade_fx, cancel_fx, start_fx)

# No other action done when mouse is hover over button
ignore = [cancel_button, upgrade_button, begin_button, fast_forward_cancel_button, fast_forward_x3_button, fast_forward_x5_button, witch_selector, knight_selector, elf_selector]

run = True

while run:
    clock.tick(c.FPS)

    #####################
    # UPDATING SECTION
    #####################
    world.game_speed = current_fast_forward_type
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
    pygame.Surface.fill(screen, "Black")
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
            if pygame.time.get_ticks() - time_begin > 100: # Check if delta time is greater than 100ms
                if fast_forward_cancel_button.draw(screen):
                    current_fast_forward_type = 1
                if fast_forward_x3_button.draw(screen):
                    current_fast_forward_type = 3
                if fast_forward_x5_button.draw(screen):
                    current_fast_forward_type = 5
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
        draw_slot(witch_selector)
        draw_slot(knight_selector)
        draw_slot(elf_selector)
        if witch_selector.draw(screen):
            placing_turret = True
            select = (selector["witch"], "witch")
        if knight_selector.draw(screen):
            placing_turret = True
            select = (selector["knight"], "knight")
        if elf_selector.draw(screen):
            placing_turret = True
            select = (selector["elf"], "elf")
        if placing_turret:
            # show cursor
            cursor_turret = pygame.transform.scale(select[0][0][0], (99, 99))
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pygame.mouse.get_pos()
            cursor_rect.center = (cursor_pos[0], cursor_pos[1]-30)
            screen.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(screen):
                placing_turret = False
        # show upgrade if turret is selected
        if selected_turret:
            # check if turret can be upgraded
            if selected_turret.upgrade_level < c.TURRET_LEVEL:
                # show cost of an upgrade button
                draw_text(str(c.UPGRADE_COST), text_font, "grey100", (c.SCREEN_WIDTH - 200, c.SCREEN_HEIGHT - 200))
                screen.blit(coin_gui_up, (c.SCREEN_WIDTH - 300, c.SCREEN_HEIGHT - 220))
                if upgrade_button.draw(screen):
                    if world.money >= c.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= c.UPGRADE_COST
    else:
        rect_width = 800
        rect_height = 400
        rect_x = (c.SCREEN_WIDTH - rect_width) // 2
        rect_y = (c.SCREEN_HEIGHT - rect_height) // 2

        pygame.draw.rect(screen, "black", (rect_x, rect_y, rect_width, rect_height), border_radius=30)
        if game_outcome == -1:
            #draw_text("GAME OVER", large_font, "grey0", (rect_x // 2, rect_y // 2))
            draw_center_text("GAME OVER", text_win_or_lose, "grey0", (1, 0), (0, rect_y + 100))
            #draw_center_text("WAVE %s"%(world.level), large_font, "grey100", (1, 0), (0, 10))
        if game_outcome == 1:
            draw_center_text("YOU WIN!", text_win_or_lose, "grey0", (1, 0), (0, rect_y + 100))
        
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
        if nondeselect(ignore):
            buttoning = True
        else:
            buttoning = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not buttoning:
            mouse_pos = pygame.mouse.get_pos()
            #check if mouse in screen
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                selected_turret = None
                deselect_turret()
                if placing_turret:
                    # if have enough money
                    if world.money >= c.BUY_COST and not buttoning:
                        create_turret(mouse_pos, select[0], select[1])
                else:
                    selected_turret = select_turret(mouse_pos)
    pygame.display.update()
pygame.quit()