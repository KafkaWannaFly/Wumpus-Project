from Code.AppData import MapData, SpritesData
from Code.Player import *


class Game(object):
    def __init__(self, screen):
        self.read_map_data()
        self.enviroment = None
        self.screen = screen
        self.player = Player(SpritesData.bug_down)

        self.groundstart = pygame.image.load(SpritesData.background)
        self.groundstart_rect = self.groundstart.get_rect()

        self.speed = [50, 0]

        self.is_over = False
        self.flag_hold = True

    def read_map_data(self):
        file = open(MapData.path, "r")
        MapData.map2D = []
        for i in file:
            temp = []
            for j in i:
                if j != '.' and j != '\n':
                    temp.append(j)
            MapData.map2D.append(temp)

    def generate_env(self):
        ground = pygame.image.load(SpritesData.bush)
        groundrect = ground.get_rect()

        for i in range(MapData.size):
            for j in range(MapData.size):
                self.screen.blit(ground, (j * 50, i * 50))

        self.groundstart_rect[0], self.groundstart_rect[1] = (0, 0)

        self.screen.blit(self.groundstart, self.player.rect)
        self.screen.blit(self.player.sprite, self.player.rect)

    # Demo purpose
    def run_game(self):
        print(self.player.rect)
        self.screen.blit(self.groundstart, self.player.rect)

        if self.flag_hold:
            if self.speed[0] < 0:
                self.player.sprite = pygame.image.load(SpritesData.bug_left)
            elif self.speed[0] > 0:
                self.player.sprite = pygame.image.load(SpritesData.bug_right)
            self.screen.blit(self.groundstart, self.player.rect)
            self.screen.blit(self.player.sprite, self.player.rect)
            self.flag_hold = False
            return

        self.player.rect.move_ip(self.speed)
        if self.player.rect.right >= self.screen.get_rect().right:
            self.screen.blit(self.groundstart, self.player.rect)
            self.screen.blit(self.player.sprite, self.player.rect)
            self.flag_hold = True
            self.speed[0] = -self.speed[0]
            return

        if self.player.rect.left <= self.screen.get_rect().left:
            self.screen.blit(self.groundstart, self.player.rect)
            self.screen.blit(self.player.sprite, self.player.rect)
            self.flag_hold = True
            self.speed[0] = -self.speed[0]
            return

        if self.speed[0] < 0:
            self.player.sprite = pygame.image.load(SpritesData.bug_left)
        elif self.speed[0] > 0:
            self.player.sprite = pygame.image.load(SpritesData.bug_right)

        self.screen.blit(self.groundstart, self.player.rect)
        self.screen.blit(self.player.sprite, self.player.rect)
