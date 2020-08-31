from Code.Agent import Agent
from Code.AppData import MapData, SpritesData, Color, ScreenData, Font
from Code.Bush import Bush
from Code.EnvironmentSprites import EnvironmentSprite, G, BG, B, W, P
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

        self.score = pygame.font.Font(Font.consolas, 25)
        self.action = pygame.font.Font(Font.consolas, 20)
        self.text_action = None

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

                bush = Bush((j * 50, i * 50))
                self.bushes.add(bush)
        self.all_sprites.add(self.player)
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
        curPos = self.player.get_pos()
        if P in MapData.map2D[curPos[0]][curPos[1]] or W in MapData.map2D[curPos[0]][curPos[1]]:
            print('Game over!')
        curRect = (curPos[1] * 50, curPos[0] * 50)
        (action, next_step), point = self.player.get_next_move()
        myAction = ''
        if action == 0 or action is None:  # stop
            myAction = 'Done!'
            print(myAction)

            self.is_over = True
        elif action == 1:  # simple move
            myAction = 'Move to ' + str((next_step[0], next_step[1]))
            print(myAction)

            nextPos = (next_step[1] * 50, next_step[0] * 50)
            self.move_player(curRect, nextPos)
        elif action == 2:  # shoot wumpus
            myAction = 'Shoot Wumpus at ' + str(next_step)
            print(myAction)
            # next_step is wumpus position
            self.remove_wumpus(next_step)
        elif action == 3:  # pick gold
            myAction = 'Pick up gold'
            print(myAction)

            # next_step is gold position
            goldPos = next_step[1] * 50, next_step[0] * 50
            sprite = self.find_sprite(goldPos, SpritesData.gold)

            i, j = next_step[0], next_step[1]
            goldStr = MapData.map2D[i][j]
            goldStr = goldStr.replace('G', '')

            if goldStr == '':  # if there is nothing, replace with a background
                goldStr = '-'
                sprite.set_image(SpritesData.background)
            else:  # If there are somethings, just remove gold sprite
                self.all_sprites.clear(self.screen, sprite.image)
                sprite.kill()
            self.update_draw()

        self.update()
        self.text_action = self.action.render('', True, Color.BLUE_CORAL)
        self.text_action = self.action.render(myAction, True, Color.BLUE_CORAL)
        print('Point: ' + str(self.player.agent.point))
        self.display_score()

    def display_score(self):
        text_score = self.score.render("Score: " + str(self.player.agent.point), True, Color.BLUE_CORAL)
        self.screen.blit(text_score, (10, 10))
        self.screen.blit(self.text_action, (10, 35))

    def move_player(self, curPos, nextPos):
        self.remove_bush(nextPos)
        self.player.move_to(nextPos)

        self.all_sprites.draw(self.screen)
        self.bushes.draw(self.screen)

    def find_sprite(self, pos, spriteData=None):
        sprites = self.sprites()
        sprite = None
        for i in sprites:
            if i.rect == pos:
                if spriteData is None:
                    sprite = i
                    break
                else:
                    if i.imagePath == spriteData:
                        sprite = i
                        break
        return sprite

    def sprites(self):
        return self.all_sprites.sprites()

    def get_bushes_sprites(self):
        return self.bushes.sprites()

    def remove_wumpus(self, pos):
        # Remove wumpus itself
        i, j = pos[0], pos[1]
        wumpusStr = MapData.map2D[i][j]
        wumpusStr = wumpusStr.replace('W', '')
        wumpusSprite = self.find_sprite((j * 50, i * 50), SpritesData.wumpus)
        if wumpusStr == '':
            wumpusStr = '-'
            wumpusSprite.set_image(SpritesData.background)
        else:
            self.all_sprites.clear(self.screen, wumpusSprite.image)
            wumpusSprite.kill()

        # Remove its Stench from map data
        if i - 1 >= 0:
            near_i, near_j = i - 1, j
            stenchStr = MapData.map2D[near_i][near_j]
            stenchStr = stenchStr.replace('S', '')
            if stenchStr == '':
                stenchStr = '-'
                stenchSprite = self.find_sprite((near_j * 50, near_i * 50), SpritesData.background_s)
                stenchSprite.set_state(BG)
            elif stenchStr == 'B':
                stenchSprite = self.find_sprite((near_j * 50, near_i * 50), SpritesData.background_bs)
                stenchSprite.set_state(B)
        if i + 1 < MapData.size:
            near_i, near_j = i + 1, j
            stenchStr = MapData.map2D[near_i][near_j]
            stenchStr = stenchStr.replace('S', '')
            if stenchStr == '':
                stenchStr = '-'
                stenchSprite = self.find_sprite((near_j * 50, near_i * 50), SpritesData.background_s)
                stenchSprite.set_state(BG)
            elif stenchStr == 'B':
                stenchSprite = self.find_sprite((near_j * 50, near_i * 50), SpritesData.background_bs)
                stenchSprite.set_state(B)
        if j - 1 >= 0:
            near_i, near_j = i, j - 1
            stenchStr = MapData.map2D[near_i][near_j]
            stenchStr = stenchStr.replace('S', '')
            if stenchStr == '':
                stenchStr = '-'
                stenchSprite = self.find_sprite((near_j * 50, near_i * 50), SpritesData.background_s)
                stenchSprite.set_state(BG)
            elif stenchStr == 'B':
                stenchSprite = self.find_sprite((near_j * 50, near_i * 50), SpritesData.background_bs)
                stenchSprite.set_state(B)
        if j + 1 < MapData.size:
            near_i, near_j = i, j + 1
            stenchStr = MapData.map2D[near_i][near_j]
            stenchStr = stenchStr.replace('S', '')
            if stenchStr == '':
                stenchStr = '-'
                stenchSprite = self.find_sprite((near_j * 50, near_i * 50), SpritesData.background_s)
                stenchSprite.set_state(BG)
            elif stenchStr == 'B':
                stenchSprite = self.find_sprite((near_j * 50, near_i * 50), SpritesData.background_bs)
                stenchSprite.set_state(B)

    def remove_bush(self, pos):
        bushes = self.get_bushes_sprites()
        bush = None
        for i in bushes:
            if i.rect == pos:
                bush = i
                break
        if bush is not None:
            self.bushes.clear(self.screen, bush.image)
            bush.kill()

        self.all_sprites.draw(self.screen)
        self.bushes.draw(self.screen)

    def update(self):
        self.all_sprites.update()
        self.bushes.update()

    def update_draw(self):
        self.all_sprites.draw(self.screen)
        self.bushes.draw(self.screen)
