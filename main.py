import random
import pygame
import math
import time

clock = pygame.time.Clock()
res = (800,500)
screen = pygame.display.set_mode(res)

pygame.mouse.set_visible(False)

def rectangles_overlap(rect1, rect2):
    x1, y1, width1, height1 = rect1
    x2, y2, width2, height2 = rect2
    rect1_left = x1
    rect1_right = x1 + width1
    rect1_top = y1
    rect1_bottom = y1 + height1

    rect2_left = x2
    rect2_right = x2 + width2
    rect2_top = y2
    rect2_bottom = y2 + height2
    
    return (rect1_left < rect2_right and
        rect1_right > rect2_left and
        rect1_top < rect2_bottom and
        rect1_bottom > rect2_top)

class Player:
    def __init__(self, pos):
        self.pos = [pos[0], pos[1]]
        self.speed = 3
        self.animation_frames = 5
        self.animation_timer = 0
        self.animation_speed = 2
        self.images = [pygame.transform.scale(pygame.image.load("assets/player_frames/player_frame" + str(n+1)+ ".png"),(48,96)) \
                       for n in range(self.animation_frames)]
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.collider_height = 20
        self.collider_width = 30
        self.collider_offset = 20
        self.rect = self.generate_rect()
        self.gun = None

    def set_gun(self, gun):
        self.gun = gun

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
        self.rect = self.generate_rect()

        if any([rectangles_overlap(self.rect, wall_tile.rect) for wall_tile in wall_tiles]):
            self.pos[0] -= x_move * self.speed
            
        self.pos[1] += y_move * self.speed
        self.rect = self.generate_rect()

        if any([rectangles_overlap(self.rect, wall_tile.rect) for wall_tile in wall_tiles]):
            self.pos[1] -= y_move * self.speed

        self.moving = x_move or y_move
        if self.moving:
            self.animation_timer += dt
        else:
            self.animation_timer = 0
            
    def generate_rect(self):
        return (self.pos[0] - self.collider_width//2, self.pos[1] - self.collider_height//2 + self.collider_offset, self.collider_width, self.collider_height)

class Enemy:
    def __init__(self,pos):
        self.pos = [pos[0], pos[1]]
        self.speed = 3
        self.animation_frames = 5
        self.animation_timer = 0
        self.animation_speed = 2
        self.images = [pygame.transform.scale(pygame.image.load("assets/enemy_frames/enemy_walk_frame" + str(n+1)+ ".png"),(64,128)) \
                       for n in range(self.animation_frames)]
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.rect = self.generate_rect()
    def move(self):
        x_move = 0
        y_move = 0
        target = player.get_pos()

        self.animation_timer += dt
            
    def generate_rect(self):
        return (self.pos[0] - self.width//2, self.pos[1] - self.height//2, self.width, self.height)

class Gun:
    def __init__(self, owner):
        self.owner = owner
        self.unrotated_image = pygame.transform.scale(pygame.image.load("assets/gun.png"),(48,48))
        self.image = self.unrotated_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.ry = 20
        self.rx = 30
        self.direction = 0
        self.bullet_speed = 10

    def update(self, target_pos):
        angle = math.atan2(target_pos[1] - self.owner.pos[1], target_pos[0] - self.owner.pos[0])
        self.pos = [self.owner.pos[0] + self.rx * math.cos(angle), self.owner.pos[1] + self.ry * math.sin(angle)]
        self.direction = angle
        deg_angle = math.degrees(angle)
        if deg_angle % 360 > 270 or deg_angle % 360 <= 90:
            self.image = pygame.transform.rotate(self.unrotated_image, -deg_angle)
        else:
            self.image = pygame.transform.rotate(pygame.transform.flip(self.unrotated_image, False, True), -deg_angle)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def shoot(self):
        bullet = Bullet(self.pos, self.direction, self.bullet_speed)
        bullets.append(bullet)

class Bullet:
    def __init__(self, pos, direction, speed):
        self.image = pygame.image.load("assets/bullet.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pos = [pos[0], pos[1]]
        self.direction = direction
        self.speed = speed
        
    def update(self):
        self.pos[0] += self.speed * math.cos(self.direction)
        self.pos[1] += self.speed * math.sin(self.direction)
        
        

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
        self.rect = self.generate_rect()

    def generate_rect(self):
        return (self.pos[0] - self.width//2, self.pos[1] - self.height//2, self.width, self.height)

    
        

player = Player((100,100))

num_enemies = random.randint(0,6)
enemy_coords = [(random.randint(50,450),random.randint(50,450)) for x in range(1,6)]
enemies = [Enemy((enemy_coords[x-1])) for x in range(1,num_enemies)]

player.set_gun(Gun(player))
bullets = []

floor_tiles = []
for i in range(res[0]//32):
    for j in range(res[1]//32):
        floor_tiles.append(FloorTile((16 + 32*i ,16 + 32*j),pygame.image.load("assets/carpet1.png")))

wall_tiles = []
wall_tiles.append(WallTile((200,200),pygame.image.load("assets/wall1.png")))

w_pressed = False
a_pressed = False
s_pressed = False
d_pressed = False
dt = 0

while True:
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            if event.key == pygame.K_w: w_pressed = True
            elif event.key == pygame.K_a: a_pressed = True
            elif event.key == pygame.K_s: s_pressed = True
            elif event.key == pygame.K_d: d_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w: w_pressed = False
            elif event.key == pygame.K_a: a_pressed = False
            elif event.key == pygame.K_s: s_pressed = False
            elif event.key == pygame.K_d: d_pressed = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.gun.shoot()

    player.move()

    for bullet in bullets:
        bullet.update()

    screen.fill("black")
    
    for floor_tile in floor_tiles:
        screen.blit(floor_tile.image, (floor_tile.pos[0] - floor_tile.width//2, floor_tile.pos[1] - floor_tile.height//2))

    for wall_tile in wall_tiles:
        screen.blit(wall_tile.image, (wall_tile.pos[0] - wall_tile.width//2, wall_tile.pos[1] - wall_tile.height//2))

    screen.blit(player.images[int(player.animation_timer * player.animation_speed * player.animation_frames) % player.animation_frames], \
                (player.pos[0] - player.width//2, player.pos[1] - player.height//2))

    for bullet in bullets:
        screen.blit(bullet.image, (bullet.pos[0] - bullet.width//2, bullet.pos[1] - bullet.height//2))


    for enemy in enemies:
        screen.blit(enemy.images[int(enemy.animation_timer * enemy.animation_speed * enemy.animation_frames)% enemy.animation_frames], \
            (enemy.pos[0] - enemy.width//2, enemy.pos[1] - enemy.height//2))
        
    mouse_pos = pygame.mouse.get_pos()
    player.gun.update(mouse_pos)
    screen.blit(player.gun.image, (player.gun.pos[0] - player.gun.width//2, player.gun.pos[1] - player.gun.height//2))
    
    pygame.display.update()
    dt = clock.tick(60)/1000
