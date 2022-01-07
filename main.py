import pygame, sys, math
from random import randint

from pygame.time import Clock

pygame.init()

HEIGHT = 720
WIDTH = 1280
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test noise")
clock = pygame.time.Clock()
SQUARE_SIZE = 32


run = True
fps = 60


def solidBlock():
    return pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))

def count_2d_list(nestedList:list):
    count = [0 for i in range(len(nestedList))]

    for i in range(len(nestedList)):
        for j in range(len(nestedList[i])):
            if nestedList[i][j] == 1:
                count[i] +=1
    return count


class Generator:
    def __init__(self) -> None:
        self.map = [[0 for x in range(20*10)] for y in range(12*2)]
        self.lenMap = len(self.map)

    def Generate(self):
        self.__init__()

        up = ((HEIGHT//2)//SQUARE_SIZE)+7
        down = self.lenMap-2

        spawn_threshold = 3

        sin_scale = 0
        sin_size = 2
        sin_offset = 0

        for line in range(len(self.map[0])):
            line_pose = int(math.sin(sin_scale+sin_offset)*sin_size)+sin_size+10
            self.map[line_pose][line] = 1
            for i in range(line_pose, self.lenMap-1):
                self.map[i][line] = 1
            sin_scale += .5


        for rowNum in range(len(self.map)):
            for tile in range(len(self.map[rowNum])):

                if rowNum >= up and rowNum <= down:
                    rand = randint(1,1+abs(rowNum-len(self.map)))
                    if rand <= spawn_threshold:
                        self.map[rowNum][tile] = 0

                if self.map[rowNum-1][tile] == 0 and self.map[rowNum][tile] != 0:
                    self.map[rowNum][tile] = 2







world = Generator()

class Rendering:
    def __init__(self) -> None:
        self.square = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE)).convert()

        self.scroll = [0,0]

    def calculate_scrolling(self):
        self.scroll[0] += (player.rect.x - self.scroll[0]-WIDTH//2)//5
        self.scroll[1] += (player.rect.y - self.scroll[1] - HEIGHT//2)//20
        
    def Draw_map(self):

        map_rect = list()
        posY = 0 
        rowNum = 0
        for row in world.map:
            posX = 0 
            for tile in row:
                if tile != 0:
                    map_rect.append(self.square.get_rect(topleft=(posX, posY)))
                if tile == 1:
                    self.square.fill(color=(217,97,0))
                    screen.blit(solidBlock(),(posX- self.scroll[0],posY-self.scroll[1]))
                elif tile == 2:
                    self.square.fill("green3")
                    screen.blit(self.square,(posX- self.scroll[0],posY-self.scroll[1]))

                posX += SQUARE_SIZE
            rowNum += 1
            posY += SQUARE_SIZE 
        return map_rect 
    
    def Draw_player(self):
        screen.blit(player.img, (player.rect.x - self.scroll[0], player.rect.y - self.scroll[1]))


renderer = Rendering()

class Player(pygame.sprite.Sprite):  # création du joueur
    def __init__(self):
        super().__init__()
        # stats
        self.SP = 4
        self.JUMP = 13
        # texture et animations
        self.img = pygame.Surface((SQUARE_SIZE-7, SQUARE_SIZE*2-7))
        self.img.fill("grey")
        self.rect = self.img.get_rect()
        # position et mouvement
        self.rect.x = 10
        self.rect.y = 10
        self.vel_y = 0
        self.SPAWN_X = 10
        self.SPAWN_Y = 10
        self.wall_jump = False
        self.cant_jump = -1
        self.width = self.rect.width
        self.height = self.rect.height

    def gravity(self, dy):
        self.vel_y += 1.60
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        return dy

    def move(self):
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        tile_list = renderer.Draw_map()

        if key[pygame.K_SPACE] and self.cant_jump <= 0 or key[pygame.K_UP] and self.cant_jump <= 0:
            self.cant_jump += 1
            self.vel_y = -self.JUMP
            dy += self.vel_y

        if key[pygame.K_LEFT]: #and self.rect.x > 0:
            dx -= self.SP

        if key[pygame.K_RIGHT]: #and self.rect.x + self.rect.width < WIDTH:
            dx += self.SP

        if self.wall_jump is False:
            dy = self.gravity(dy)

        for tile in tile_list:
            # collision x
            if tile.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # collision y
            if tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # au dessus ?
                if self.wall_jump and key[pygame.K_SPACE]:
                    dy -= self.JUMP
                    self.wall_jump = False

                elif self.wall_jump and key[pygame.K_SPACE]:
                    dy -= self.JUMP
                    self.wall_jump = False

                if self.vel_y < 0:
                    dy = tile.bottom - self.rect.top
                    self.vel_y = 0
                # en dessous ?
                elif self.vel_y >= 0:
                    dy = tile.top - self.rect.bottom
                    self.vel_y = 0
                    self.cant_jump = 0
        # update du déplacement du joueur
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.y > HEIGHT - self.rect.height:
            self.rect.x = self.SPAWN_X
            self.rect.y = self.SPAWN_Y

count = 0
world.Generate()
player = Player()
while run: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                world.Generate()

    screen.fill("white")
    #renderer.Draw_map()
    renderer.calculate_scrolling()
    player.move()
    renderer.Draw_player()
    
    pygame.display.update()
    clock.tick(fps)
