import pygame
from Code import AppData
from Code.AppData import SpritesData

BG = 'BG'
S = 'S'
B = 'B'
BS = B + S
G = 'G'
P = 'P'
W = 'W'
A = 'A'


class EnvironmentSprite(pygame.sprite.Sprite):
    def __init__(self, imgPath, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imgPath).convert()
        self.rect = self.image.get_rect()
        self.rect = pos
        self.state = None

    # def update(self, *args):
    #     if self.state == BG:
    #         self.image = pygame.image.load(SpritesData.background).convert()
    #     elif self.state == B:
    #         self.image = pygame.image.load(SpritesData.background_b).convert()
    #     elif self.state == S:
    #         self.image = pygame.image.load(SpritesData.background_s).convert()
    #     elif self.state == BS:
    #         self.image = pygame.image.load(SpritesData.background_bs).convert()
    #     elif self.state == G:
    #         self.image = pygame.image.load(SpritesData.gold).convert()

    def set_image(self, imgPath):
        self.image = pygame.image.load(imgPath).convert()

    def set_state(self, state):
        self.state = state
