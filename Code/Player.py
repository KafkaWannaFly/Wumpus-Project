import pygame
from Code.Agent import Agent
from Code.EnvironmentSprites import EnvironmentSprite


class Player(EnvironmentSprite):
    def __init__(self, sprite_path, pos):
        EnvironmentSprite.__init__(self, sprite_path, pos)
        # self.image = pygame.image.load(sprite_path).convert()
        # self.rect = self.image.get_rect()
        self.agent = Agent()

    def get_next_move(self):
        self.agent.calPoint()  # (move, next_step), self.point

    def get_pos(self):
        var = self.agent.createAgent()[0]
        return var[0]

    def shot_arrow(self, direction):
        pass
