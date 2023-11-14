import pygame
import os
import config as c

class SFX:
    _instance = None  # Class variable to store the instance

    def __init__(self):
        self.select_turret_fx = pygame.mixer.Sound(os.path.join("Main_Game", "assets", "audio", "select_turret.wav"))
        self.button_fx = pygame.mixer.Sound(os.path.join("Main_Game", "assets", "audio", "button_click.wav"))
        self.upgrade_fx = pygame.mixer.Sound(os.path.join("Main_Game", "assets", "audio", "upgrade.wav"))
        self.cancel_fx = pygame.mixer.Sound(os.path.join("Main_Game", "assets", "audio", "cancel.wav"))
        self.start_fx = pygame.mixer.Sound(os.path.join("Main_Game", "assets", "audio", "start.wav"))
        self.menu_select = pygame.mixer.Sound(os.path.join("Main_Game", "assets", "audio", "menu_select.wav"))
        self.menu_enter = pygame.mixer.Sound(os.path.join("Main_Game", "assets", "audio", "menu_enter.wav"))
        self.denied = pygame.mixer.Sound(os.path.join("Main_Game", "assets", "audio", "denied.wav"))
        self.kill_fx = pygame.mixer.Sound(os.path.join("Main_Game", "assets", "audio", "kill.wav"))
        self.volume_control = pygame.mixer.Sound(os.path.join("Main_Game", "assets", "audio", "volumecontrol.wav"))

    @classmethod
    def play_fx(cls, select, volume):
        if cls._instance is None:
            cls._instance = cls()
        sound_effect = getattr(cls._instance, select, None)
        if sound_effect:
            sound_effect.set_volume(volume)
            sound_effect.play()
        else:
            print("Sound effect not found")
