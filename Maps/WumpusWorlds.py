import sys, pygame
pygame.init()

file = open("map1.txt", "r")

size = int(file.readline())
map = []
for i in file:
    temp = []
    for j in i:
        if j !='.':
            temp.append(j)
    map.append(temp)

print(size, map)

screensize = width, height = 500, 500

screen = pygame.display.set_mode(screensize)
screenrect = screen.get_rect()

pygame.display.set_caption("Wumpus World - The LadyBug")

icon = pygame.image.load("bug_up.png")
pygame.display.set_icon(icon)

background = pygame.Surface(screensize)

ground = pygame.image.load("bush.jpg")
groundrect = ground.get_rect()

for i in range(size):
    for j in range(size):
        screen.blit(ground, (j * 50, i * 50))

start = (0, 0)

groundstart = pygame.image.load("background.png")
groundstartrect = groundstart.get_rect()

groundstartrect[0], groundstartrect[1] = start

char = pygame.image.load("bug_down.png")
charrect = char.get_rect()

charrect[0], charrect[1] = start

screen.blit(groundstart, charrect)
screen.blit(char, charrect)

speed = [50, 0]

clock = pygame.time.Clock()
time = 0
deltatime = 0

flag_hold = True

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    time += deltatime
    if time >= 1:
        time = 0

        screen.blit(groundstart, charrect)
        
        ##if map[int(charrect[0]/50)][int(charrect[1]/50)] == '-':
        ##    groundstart = pygame.image.load("background.png")
        ##elif map[int(charrect[0]/50)][int(charrect[1]/50)] == "G":
        ##    groundstart = pygame.image.load("gold_bar.png")
        ##elif map[int(charrect[0]/50)][int(charrect[1]/50)] == "B":
        ##    groundstart = pygame.image.load("background-b.png")
        ##elif map[int(charrect[0]/50)][int(charrect[1]/50)] == "S":
        ##    groundstart = pygame.image.load("background-s.png")
        ##elif map[int(charrect[0]/50)][int(charrect[1]/50)] == "SB" or map[int(charrect[0]/50)][int(charrect[1]/50)] == "BS":
        ##    groundstart = pygame.image.load("background-bs.png")
        ##elif map[int(charrect[0]/50)][int(charrect[1]/50)] == "P":
        ##    groundstart = pygame.image.load("pit.png")
        ##elif map[int(charrect[0]/50)][int(charrect[1]/50)] == "PB" or map[int(charrect[0]/50)][int(charrect[1]/50)] == "PB":
        ##    groundstart = pygame.image.load("pit.png")
        ##elif map[int(charrect[0]/50)][int(charrect[1]/50)] == "W":
        ##    groundstart = pygame.image.load("monster.png")

        if flag_hold == True:
            if speed[0] < 0:
                char = pygame.image.load("bug_left.png")
            elif speed[0] > 0:
                char = pygame.image.load("bug_right.png")
            screen.blit(groundstart, charrect)
            screen.blit(char, charrect)
            flag_hold = False
            continue
        
        charrect.move_ip(speed)
        if charrect.right >= screen.get_rect().right:
            screen.blit(groundstart, charrect)
            screen.blit(char, charrect)
            flag_hold = True
            speed[0] = -speed[0]
            continue
        if charrect.left <= screen.get_rect().left:
            screen.blit(groundstart, charrect)
            screen.blit(char, charrect)
            flag_hold = True
            speed[0] = -speed[0]
            continue

        if speed[0] < 0:
            char = pygame.image.load("bug_left.png")
        elif speed[0] > 0:
            char = pygame.image.load("bug_right.png")
        
        screen.blit(groundstart, charrect)
        screen.blit(char, charrect)
    
    pygame.display.flip()
    deltatime = clock.tick(60) / 1000

