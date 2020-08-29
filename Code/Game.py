from Code.Agent import Agent
from Code.AppData import MapData, SpritesData
from Code.Bush import Bush
from Code.EnvironmentSprites import EnvironmentSprite, G
from Code.Player import *


class Game(object):
    def __init__(self, screen):
        self.read_map_data()
        self.screen = screen
        self.player = None

        self.groundstart = pygame.image.load(SpritesData.background)
        self.groundstart_rect = self.groundstart.get_rect()
        self.groundstart_rect[0], self.groundstart_rect[1] = (0, 0)

        self.speed = [50, 0]
        self.is_over = False
        self.flag_hold = True

        self.bushes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    def read_map_data(self):
        file = open(MapData.path, "r")
        MapData.map2D = []
        firstLine = 1
        for i in file:
            if firstLine:
                firstLine -= 1
                continue
            temp = i.strip().split('.')
            MapData.map2D.append(temp)

    def generate_env(self):
        for i in range(MapData.size):
            for j in range(MapData.size):
                tmp = None
                pos = (j * 50, i * 50)
                if '-' in MapData.map2D[i][j]:
                    env = EnvironmentSprite(SpritesData.background, pos)
                    self.all_sprites.add(env)
                if 'B' in MapData.map2D[i][j] and 'S' in MapData.map2D[i][j]:
                    env = EnvironmentSprite(SpritesData.background_bs, pos)
                    self.all_sprites.add(env)
                else:
                    if 'B' in MapData.map2D[i][j]:
                        env = EnvironmentSprite(SpritesData.background_b, pos)
                        self.all_sprites.add(env)
                    if 'S' in MapData.map2D[i][j]:
                        env = EnvironmentSprite(SpritesData.background_s, pos)
                        self.all_sprites.add(env)
                if 'G' in MapData.map2D[i][j]:
                    env = EnvironmentSprite(SpritesData.gold, pos)
                    self.all_sprites.add(env)
                    tmp = pygame.image.load(SpritesData.gold)
                if 'P' in MapData.map2D[i][j]:
                    pit = EnvironmentSprite(SpritesData.pit, pos)
                    self.all_sprites.add(pit)
                if 'W' in MapData.map2D[i][j]:
                    wumpus = EnvironmentSprite(SpritesData.wumpus, pos)
                    self.all_sprites.add(wumpus)
                if 'A' in MapData.map2D[i][j]:
                    agent = Player(SpritesData.bug_up, pos)
                    self.player = agent
                    self.all_sprites.add(agent)
                if tmp is not None:
                    self.screen.blit(tmp, (j * 50, i * 50))

                bush = Bush((j * 50, i * 50))
                self.bushes.add(bush)

        # self.screen.blit(self.groundstart, self.player.rect)
        # self.screen.blit(self.player.image, self.player.rect)

        # self.obstacles.draw(self.screen)
        # self.enviroment.draw(self.screen)

        self.all_sprites.draw(self.screen)
        self.bushes.draw(self.screen)
        self.remove_bush(self.player.rect)

    # Demo purpose
    def run_demo(self):
        print(self.player.rect)
        self.screen.blit(self.groundstart, self.player.rect)

        if self.flag_hold:
            if self.speed[0] < 0:
                self.player.image = pygame.image.load(SpritesData.bug_left)
            elif self.speed[0] > 0:
                self.player.image = pygame.image.load(SpritesData.bug_right)
            self.screen.blit(self.groundstart, self.player.rect)
            self.screen.blit(self.player.image, self.player.rect)
            self.flag_hold = False
            return

        self.player.rect.move_ip(self.speed)
        if self.player.rect.right >= self.screen.get_rect().right:
            self.screen.blit(self.groundstart, self.player.rect)
            self.screen.blit(self.player.image, self.player.rect)
            self.flag_hold = True
            self.speed[0] = -self.speed[0]
            return

        if self.player.rect.left <= self.screen.get_rect().left:
            self.screen.blit(self.groundstart, self.player.rect)
            self.screen.blit(self.player.image, self.player.rect)
            self.flag_hold = True
            self.speed[0] = -self.speed[0]
            return

        if self.speed[0] < 0:
            self.player.image = pygame.image.load(SpritesData.bug_left)
        elif self.speed[0] > 0:
            self.player.image = pygame.image.load(SpritesData.bug_right)

        self.screen.blit(self.groundstart, self.player.rect)
        self.screen.blit(self.player.image, self.player.rect)

    def run(self):
        (move, next_step), point = self.player.get_next_move()
        if move == 1:  # simple move
            pass
        elif move == 2:  # shoot wumpus
            pass
        elif move == 3:  # pick gold
            pass

    def sprites(self):
        return self.all_sprites.sprites()

    def bushes(self):
        return self.bushes

    def replace_sprite(self, pos, path, state=None):
        sprites = self.sprites()
        bushes = self.bushes
        sprite = None
        for i, j in zip(sprites, bushes):
            if i.rect == pos:
                sprite = i
            if j.rect == pos:
                self.bushes.clear(self.screen, j.image)
                j.kill()
        if sprite is not None:
            sprite.set_image(path)
            self.all_sprites.draw(self.screen)
            self.bushes.draw(self.screen)
        else:
            print('replace_sprite: null exception')
        if state is not None:
            sprite.set_state(state)

    def remove_bush(self, pos):
        sprites = self.sprites()
        bushes = self.bushes
        for sprite, bush in zip(sprites, bushes):
            if bush.rect == pos and sprite.rect == pos:
                self.bushes.clear(self.screen, bush.image)
                bush.kill()
        self.all_sprites.draw(self.screen)
        bushes.draw(self.screen)
