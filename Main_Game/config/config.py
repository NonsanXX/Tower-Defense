from random import shuffle

ROWS = 16
COLS = 30
TILE_SIZE = 64
SCREEN_WIDTH = COLS*TILE_SIZE
SCREEN_HEIGHT = ROWS*TILE_SIZE
FPS = 60
HEALTH = 100
MONEY = 40000
TOTAL_LEVEL = 15
SCORE_FILE = "Main_Game/highscore.txt"
MUSIC_VOLUME_FILE = "Main_Game/config/ms_volume.txt"
FX_VOLUME_FILE = "Main_Game/config/fx_volume.txt"

# Enemy const
SPAWN_COOLDOWN = 1200

# Turret const
TURRET_LEVEL = 3
BUY_COST = 100
UPGRADE_COST = 500
LEVEL_COMPLETE_REWARD = 0
ANIMATION_STEP = 8
ANIMATION_DELAY = 15
LIMIT = 24

#CHEERUP

CHEERUP_TEXT = [
    "ไม่เป็นไร เอาใหม่นะ",
    "ผมเข้าใจ เน็ต Ping ใช่มั้ยล่ะ?",
    "เม้าส์คุณพังรึเปล่า?",
    "...?",
    "I am the storm that is approaching!",
    "E-JUDGE is strongest foe.",
    "No Context.",
    "Por qué traducir?"
]