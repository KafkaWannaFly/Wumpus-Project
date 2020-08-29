import pygame

from Code import AppData
from Code.AppData import SpritesData


class Bush(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(SpritesData.bush).convert()
        self.rect = self.image.get_rect()
        self.rect = pos
        self.IsActive = True

    def update(self, *args):
        if self.IsActive is False:
            self.kill()

    def set_active(self, active):
        self.IsActive = active
