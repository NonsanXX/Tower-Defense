import pygame
import config as c

class Button():
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):
        # get mouse posi
        action = False
        pos = pygame.mouse.get_pos()
        # check mouse over clicked condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                # if was a single_click type
                if self.single_click:
                    self.clicked = True

        if not pygame.mouse.get_pressed()[0] and self.clicked:
            self.clicked = False
        # draw button on screen
        surface.blit(self.image, self.rect)

        return action