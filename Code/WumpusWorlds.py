import pygame
import sys
from Code.AppData import *
from Code.Game import Game
from Code.Player import Player


def main():
    pygame.init()

    # Caption & Icon
    pygame.display.set_caption("Wumpus World - The LadyBug")
    icon = pygame.image.load(SpritesData.bug_up)
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((ScreenData.Width, ScreenData.Height))
    screenrect = screen.get_rect()

    background = pygame.Surface((ScreenData.Width, ScreenData.Height))

    game = Game(screen)
    game.generate_env()

    clock = pygame.time.Clock()
    time = 0
    deltatime = 0

    while not game.is_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        time += deltatime
        if time >= 1:
            time = 0
            game.run_game()

        pygame.display.flip()
        deltatime = clock.tick(60) / 1000


if __name__ == '__main__':
    main()
