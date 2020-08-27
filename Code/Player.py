import pygame


class Player(object):
    def __init__(self, sprite_path):
        self.sprite = pygame.image.load(sprite_path)
        self.rect = self.sprite.get_rect()
        self.rect[0], self.rect[1] = (0, 0)

    def get_next_move(self):
        pass

    def move_to(self, direction):
        pass

    def shot_arrow(self, direction):
        pass
