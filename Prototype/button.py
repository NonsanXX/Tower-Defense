import pygame
import config as c

class Button():
    def __init__(self, x, y, image, single_click, click_fx, button_fx, upgrade_fx, cancel_fx, start_fx):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click
        self.click_fx = click_fx
        self.button_fx = button_fx
        self.upgrade_fx = upgrade_fx
        self.cancel_fx = cancel_fx
        self.start_fx = start_fx

    def draw(self, surface):
        # get mouse posi
        action = False
        pos = pygame.mouse.get_pos()
        # check mouse over clicked condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                # if was a single_click type
                if self.rect.topleft == (c.SCREEN_WIDTH/2-250, c.SCREEN_HEIGHT-100):
                    self.clicked = True
                    self.cancel_fx.play()
                elif self.rect.topleft == (c.SCREEN_WIDTH - 250, -30):
                    self.clicked = True
                    self.start_fx.play()
                elif self.rect.topleft == (c.SCREEN_WIDTH - 300, c.SCREEN_HEIGHT-200):
                    self.clicked = True
                    self.upgrade_fx.play()
                elif self.single_click:
                    self.clicked = True
                    self.click_fx.play()

        if not pygame.mouse.get_pressed()[0] and self.clicked:
            self.clicked = False
        # draw button on screen
        surface.blit(self.image, self.rect)

        return action