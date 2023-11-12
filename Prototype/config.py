from random import shuffle

ROWS = 16
COLS = 30
TILE_SIZE = 64
SCREEN_WIDTH = COLS*TILE_SIZE
SCREEN_HEIGHT = ROWS*TILE_SIZE
FPS = 60
HEALTH = 100
MONEY = 400
TOTAL_LEVEL = 15
SCORE_FILE = "highscore.txt"

# Enemy const
SPAWN_COOLDOWN = 1200

# Turret const
TURRET_LEVEL = 3
BUY_COST = 100
UPGRADE_COST = 250
LEVEL_COMPLETE_REWARD = 0
ANIMATION_STEP = 8
ANIMATION_DELAY = 15

#CHEERUP

CHEERUP_TEXT = [
    "ตั้งใจเล่นยังอะเรา?",
    "เล่นแบบนี้ เกมผมกากหรือคุณกาก?",
    "เม้าพังรึเปล่า?",
    "...?",
    "I am the storm that is approaching!"
]