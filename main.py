import pygame
import math
import time

clock = pygame.time.Clock()
res = (800,500)
screen = pygame.display.set_mode(res)

class Player:
    def __init__(self, pos):
        self.pos = [pos[0], pos[1]]
        self.speed = 3
        self.animation_frames = 5
        self.animation_timer = 0
        self.animation_speed = 2
        self.images = [pygame.transform.scale(pygame.image.load("assets/player_frames/player_frame" + str(n+1)+ ".png"),(48,96)) for n in range(self.animation_frames)]
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()

    def move(self):
        x_move = 0
        y_move = 0
        if w_pressed: y_move -= 1
        if a_pressed: x_move -= 1
        if s_pressed: y_move += 1
        if d_pressed: x_move += 1
            
        if x_move: y_move *= 1/(math.sqrt(2))
        if y_move: x_move *= 1/(math.sqrt(2))

        self.pos[0] += x_move * self.speed
        self.pos[1] += y_move * self.speed

        self.moving = x_move or y_move
        if self.moving:
            self.animation_timer += dt
        else:
            self.animation_timer = 0

class FloorTile:
    def __init__(self, pos, image):
        self.pos = [pos[0], pos[1]]
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

class WallTile:
    def __init__(self, pos, image):
        self.pos = [pos[0], pos[1]]
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

player = Player((100,100))

floor_tiles = []
for i in range(res[0]//32):
    for j in range(res[1]//32):
        floor_tiles.append(FloorTile((16 + 32*i ,16 + 32*j),pygame.image.load("assets/carpet1.png")))

wall_layout = [[],[],[],[],[],[],[],[],[]]

w_pressed = False
a_pressed = False
s_pressed = False
d_pressed = False
dt = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: w_pressed = True
            elif event.key == pygame.K_a: a_pressed = True
            elif event.key == pygame.K_s: s_pressed = True
            elif event.key == pygame.K_d: d_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w: w_pressed = False
            elif event.key == pygame.K_a: a_pressed = False
            elif event.key == pygame.K_s: s_pressed = False
            elif event.key == pygame.K_d: d_pressed = False

    player.move()

    screen.fill("black")
    
    for floor_tile in floor_tiles:
        screen.blit(floor_tile.image, (floor_tile.pos[0] - floor_tile.width//2, floor_tile.pos[1] - floor_tile.height//2))
    screen.blit(player.images[int(player.animation_timer * player.animation_speed * player.animation_frames)%player.animation_frames], \
                (player.pos[0] - player.width//2, player.pos[1] - player.height//2))
    pygame.display.update()
    dt = clock.tick(60)/1000
