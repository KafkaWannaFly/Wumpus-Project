import pygame
import sys
from Code.AppData import *
from Code.Game import Game
from Code.Player import Player


def test_the_agent():
    a = Agent()
    x, y = a.createAgent()
    print(x, end="\n")
    print(y, end="\n")

    while True:
        x, y = a.calPoint()
        if x != None:
            print(x, end="\n")
            print(y, end="\n")
            if x[0] == 2:
                for i in a.map:
                    print(i, end='\n')
        else:
            break


def main():
    pygame.init()

    # Caption & Icon
    pygame.display.set_caption("Wumpus World - The LadyBug")
    icon = pygame.image.load(SpritesData.bug_up)
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((ScreenData.Width, ScreenData.Height))
    screenrect = screen.get_rect()

    background = pygame.Surface((ScreenData.Width, ScreenData.Height))

    MapData.path = input()

    game = Game(screen)
    game.generate_env()

    clock = pygame.time.Clock()
    time = 0
    deltatime = 0

    while not game.is_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        time += deltatime
        if time >= 0.2:
            time = 0
            game.run()

        pygame.display.flip()
        deltatime = clock.tick(60) / 1000


if __name__ == '__main__':
    main()
