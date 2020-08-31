import pygame
from Code.Agent import Agent
from Code.AppData import SpritesData
from Code.EnvironmentSprites import EnvironmentSprite


class Player(EnvironmentSprite):
    def __init__(self, sprite_path, pos):
        EnvironmentSprite.__init__(self, sprite_path, pos)
        # self.image = pygame.image.load(sprite_path).convert()
        # self.rect = self.image.get_rect()
        self.agent = Agent()

    def get_next_move(self):
        return self.agent.calPoint()  # (move, next_step), self.point

    def get_pos(self):
        pos = self.agent.createAgent()[0]
        return pos

    def move_to(self, pos):
        x, y = pos[0] - self.rect[0], pos[1] - self.rect[1]
        image = None
        if x < 0:
            image = pygame.image.load(SpritesData.bug_left).convert()
        elif x > 0:
            image = pygame.image.load(SpritesData.bug_right).convert()
        if y < 0:
            image = pygame.image.load(SpritesData.bug_up).convert()
        elif y > 0:
            image = pygame.image.load(SpritesData.bug_down).convert()
        self.image = image
        self.rect = pos
