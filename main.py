import random
import pygame
import math
import time


clock = pygame.time.Clock()
res = (800,500)
screen = pygame.display.set_mode(res)
pygame.mouse.set_visible(False)
pygame.mixer.init()

gunshots = pygame.mixer.Sound("assets/music/gunshot.mp3")
pygame.mixer.Sound.set_volume(gunshots,0.3)

global game_state

def draw_start_menu():
    pygame.font.init()
    screen.fill((0,0,0))
    font = pygame.font.SysFont('arial',50)
    start_button = font.render('Click to Start',True,(255,255,255))
    screen.blit(pygame.image.load("assets/logo.png"),(250,100))
    screen.blit(start_button,(150,350))
    pygame.display.update() 

def draw_game_over():
    pygame.font.init()
    screen.fill((255,10,10))
    if player.went_home:
        font = pygame.font.SysFont('arial',70,True)
        dead = font.render("DEAD",(255,255,255))
    screen.blit(dead)
    pygame.display.update()
    
def main():
    game_state = "start_menu"
    
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
        def __init__(self, pos, health):
            self.pos = [pos[0], pos[1]]
            self.speed = 3
            self.animation_frames = 5
            self.animation_timer = 0
            self.animation_speed = 1

            self.death_animation_frames = 10
            self.death_animation_timer = 0
            self.death_animation_speed = 1
            self.images = [pygame.transform.scale(pygame.image.load("assets/player_frames/player_frame" + str(n+1)+ ".png"),(48,96)) \
                           for n in range(self.animation_frames)]

            self.death_images = [pygame.transform.scale(pygame.image.load("assets/player_death_frames/player_death" + str(n+1)+ ".png"),(48,96)) \
                           for n in range(self.death_animation_frames)]
            self.width = self.images[0].get_width()
            self.height = self.images[0].get_height()
            self.collider_height = 20
            self.collider_width = 20
            self.collider_offset = 20

            self.collider2_height = 50
            self.collider2_width = 25
            self.collider2_offset = 0
            
            self.rect = self.generate_rect()
            self.rect2 = self.generate_rect2()
            self.gun = None
            self.max_health = 1000
            if health:
                self.health = health
            else:
                self.health = self.max_health
            
            self.dead = False

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
            self.rect2 = self.generate_rect2()

            if any([rectangles_overlap(self.rect, prop.rect) for prop in props]):
                self.pos[0] -= x_move * self.speed

            for cash in cashes:
                if rectangles_overlap(self.rect, cash.rect):
                    cashes.remove(cash)
                
                
            self.pos[1] += y_move * self.speed
            self.rect = self.generate_rect()

            if any([rectangles_overlap(self.rect, prop.rect) for prop in props]):
                self.pos[1] -= y_move * self.speed

            for cash in cashes:
                if rectangles_overlap(self.rect, cash.rect):
                    cashes.remove(cash)

            self.moving = x_move or y_move
            if self.moving:
                self.animation_timer += dt
            else:
                self.animation_timer = 0

        def die(self):
            self.dead = True

        def update(self):
            if self.dead:
                self.death_animation_timer += dt
                if self.death_animation_timer * self.death_animation_speed > 1:
                    player = None
                    pygame.quit()
                    quit()
                
        def generate_rect(self):
            return (self.pos[0] - self.collider_width//2, self.pos[1] - self.collider_height//2 + self.collider_offset, self.collider_width, self.collider_height)

        def generate_rect2(self):
            return (self.pos[0] - self.collider2_width//2, self.pos[1] - self.collider2_height//2 + self.collider2_offset, self.collider2_width, self.collider2_height)
        
    class Enemy:
        def __init__(self,pos):
            self.pos = [pos[0], pos[1]]
            self.speed = 3
            self.animation_frames = 5
            self.animation_timer = 0
            self.animation_speed = 1

            self.death_animation_frames = 8
            self.death_animation_timer = 0
            self.death_animation_speed = 1
            colour = random.randint(1,2)
            if colour == 1:
                self.images = [pygame.transform.scale(pygame.image.load("assets/enemy1_frames/enemy_walk_frame" + str(n+1)+ ".png"),(64,128)) \
                               for n in range(self.animation_frames)]
            else:
                self.images = [pygame.transform.scale(pygame.image.load("assets/enemy2_frames/enemy2_walk_frame" + str(n+1)+ ".png"),(64,128)) \
                               for n in range(self.animation_frames)]

            if colour == 1:
                self.death_images = [pygame.transform.scale(pygame.image.load("assets/enemy1_death_frames/enemy1_death" + str(n+1)+ ".png"),(64,128)) \
                               for n in range(self.death_animation_frames)]
            else:
                self.death_images = [pygame.transform.scale(pygame.image.load("assets/enemy2_death_frames/enemy2_death" + str(n+1)+ ".png"),(64,128)) \
                               for n in range(self.death_animation_frames)]
                
            self.width = self.images[0].get_width()
            self.height = self.images[0].get_height()

            self.collider_height = 20
            self.collider_width = 20
            self.collider_offset = 20

            self.collider2_height = 50
            self.collider2_width = 25
            self.collider2_offset = 0
            
            self.rect = self.generate_rect()
            self.rect2 = self.generate_rect2()
            self.max_health = 100
            self.health = self.max_health
            self.dead = False
            

        def set_gun(self, gun):
            self.gun = gun
            
        def move(self):
            x_move = 0
            y_move = 0
            target = player.get_pos()

            self.animation_timer += dt

        def die(self):
            self.dead = True

        def update(self):
            if self.dead:
                self.death_animation_timer += dt
                if self.death_animation_timer * self.death_animation_speed > 1:
                    cashes.append(Cash(self.pos, random.randint(300,1000)))
                    enemies.remove(self)
                    del self
                
                
        def generate_rect(self):
            return (self.pos[0] - self.collider_width//2, self.pos[1] - self.collider_height//2 + self.collider_offset, self.collider_width, self.collider_height)

        def generate_rect2(self):
            return (self.pos[0] - self.collider2_width//2, self.pos[1] - self.collider2_height//2 + self.collider2_offset, self.collider2_width, self.collider2_height)

    class Gun:
        def __init__(self, owner):
            self.owner = owner
            self.pos = self.owner.pos
            self.unrotated_image = pygame.transform.scale(pygame.image.load("assets/gun.png"),(48,48))
            self.image = self.unrotated_image
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.ry = 20
            self.rx = 30
            self.direction = 0
            self.bullet_speed = 5
            self.fire_rate = 10
            self.fire_time = 1 / self.fire_rate
            self.fire_timer = 0
            self.innacuracy = 5
            self.bullet_damage = 10

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

            self.fire_timer -= dt
            if self.fire_timer < 0:
                self.fire_timer = 0

        def shoot(self):
            if self.fire_timer == 0:
                direction = self.direction + math.radians(random.gauss(0, self.innacuracy))
                bullet = Bullet(self, self.pos, direction, self.bullet_speed, self.bullet_damage)
                bullets.append(bullet)
                self.fire_timer = self.fire_time
                pygame.mixer.Sound.play(gunshots)
                

    class Bullet:
        def __init__(self, owner, pos, direction, speed, damage):
            self.owner = owner
            self.pos = [pos[0], pos[1]]
            self.direction = direction
            self.speed = speed
            self.damage = damage
            if self.owner.owner == player: self.image_unrotated = pygame.image.load("assets/friendly_bullet.png")
            else: self.image_unrotated = pygame.image.load("assets/bullet.png")
            
            self.image = pygame.transform.rotate(self.image_unrotated, -math.degrees(self.direction))
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.collider_height = 10
            self.collider_width = 10
            self.rect = self.generate_rect()
            
            
        def update(self):
            self.pos[0] += self.speed * math.cos(self.direction)
            self.pos[1] += self.speed * math.sin(self.direction)
            self.rect = self.generate_rect()
            x, y = self.pos
            
            dead = False
            for enemy in enemies:
                if not dead and rectangles_overlap(self.rect, enemy.rect2) and enemy != self.owner.owner:
                    enemy.health -= self.damage
                    bullets.remove(self)
                    del self
                    dead = True
                    break

            if not dead and rectangles_overlap(self.rect, player.rect2) and player != self.owner.owner:
                player.health -= self.damage
                bullets.remove(self)
                del self
                dead = True
                
            if not dead:
                for prop in props:
                    if rectangles_overlap(self.rect, prop.rect2):
                        bullets.remove(self)
                        del self
                        dead = True
                        break
            
            if not dead and (x <= 0 or y <= 0 or x > res[0] or y > res[1]):
                bullets.remove(self)
                del self
                dead = True
            
            
        def generate_rect(self):
            return (self.pos[0] - self.collider_width//2, self.pos[1] - self.collider_height//2, self.collider_width, self.collider_height)
            
            

    class FloorTile:
        def __init__(self, pos, image):
            self.pos = [pos[0], pos[1]]
            self.image = image
            self.width = self.image.get_width()
            self.height = self.image.get_height()

    class Cash:
        def __init__(self, pos, amount):
            self.image = pygame.image.load("assets/props/cash.png")
            self.pos = pos
            self.amount = amount
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

    class Prop:
        def __init__(self, pos, hp, id):
            self.pos = [pos[0], pos[1]]
            self.hp = hp
            self.id = id
            if id == 0:
                unscaled_image = pygame.image.load("assets/props/tree.png")
                self.image = pygame.transform.scale(unscaled_image, (unscaled_image.get_width()*1.5, unscaled_image.get_height()*1.5))
            elif id == 1:
                unscaled_image = pygame.image.load("assets/props/column.png")
                self.image = pygame.transform.scale(unscaled_image, (unscaled_image.get_width()*1.5, unscaled_image.get_height()*1.5))
            elif id == 2:
                self.image = pygame.image.load("assets/walls/back_wall.png")
            elif id == 3:
                self.image = pygame.transform.scale(pygame.image.load("assets/walls/side_wall.png"), (20,64))
            elif id == 4:
                self.image = pygame.image.load("assets/door_closed.png")
            elif id == 5:
                self.image = pygame.image.load("assets/props/slot_machine1.png")
            elif id == 6:
                self.image = pygame.image.load("assets/props/slot_machine2.png")
            elif id == 7:
                self.image = pygame.image.load("assets/props/table.png")
            else:
                self.image = pygame.transform.scale(pygame.image.load("assets/walls/front_wall.png"), (64,20))
            
            self.width = self.image.get_width()
            self.height = self.image.get_height()

            if id == 0: #tree
                self.collider_width = 30
                self.collider_height = 30
                self.collider_offset = 50

                self.collider2_width = self.image.get_width() - 20 
                self.collider2_height = self.image.get_height()
                self.collider2_offset = 0

            elif id == 1: #column
                self.collider_width = 40
                self.collider_height = 30
                self.collider_offset = 50

                self.collider2_width = self.image.get_width() - 10 
                self.collider2_height = self.image.get_height()
                self.collider2_offset = 0
                
            elif id in [2,4,5,6]: # back_wall
                self.collider_width = 20
                self.collider_height = 20
                self.collider_offset = 40

                self.collider2_width = self.image.get_width()
                self.collider2_height = self.image.get_height()
                self.collider2_offset = 0
                
            elif id == 3 or id == 8: # side_wall, front wall
                self.collider_width = self.image.get_width()
                self.collider_height = self.image.get_height()
                self.collider_offset = 0

                self.collider2_width = self.image.get_width()
                self.collider2_height = self.image.get_height()
                self.collider2_offset = 0

            else: # table
                self.collider_width = self.image.get_width()
                self.collider_height = self.image.get_height()
                self.collider_offset = 0

                self.collider2_width = self.image.get_width()
                self.collider2_height = self.image.get_height()
                self.collider2_offset = 0
                
                
                
            self.rect = self.generate_rect()
            self.rect2 = self.generate_rect2()
            
        def generate_rect(self):
            return (self.pos[0] - self.collider_width//2, self.pos[1] - self.collider_height//2 + self.collider_offset, self.collider_width, self.collider_height)

        def generate_rect2(self):
            return (self.pos[0] - self.collider2_width//2, self.pos[1] - self.collider2_height//2 + self.collider2_offset, self.collider2_width, self.collider2_height)

    player_x = 100
    player_health = None
    
    while True:

        if game_state == "start_menu":
            draw_start_menu()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "playing"
        else:
                        
            player = Player((player_x, res[1] - 50), player_health)
            player.set_gun(Gun(player))

            num_enemies = random.randint(1,6)
            enemy_coords = [(random.randint(150,res[0]-150),random.randint(250,res[1]-50)) for x in range(1,6)]
            enemies = [Enemy((enemy_coords[x - 1])) for x in range(num_enemies)]

            for enemy in enemies:
                enemy.set_gun(Gun(enemy))

            props = []
            cashes = []

            object_spawn_rect = (200,200, res[0]- 400, res[1] - 400)
            object_spawn_rate = 0.4
            
            while random.uniform(0,1) < 0.4:
                spawn_pos = (random.randint(object_spawn_rect[0], object_spawn_rect[0] + object_spawn_rect[2]),
                             random.randint(object_spawn_rect[1], object_spawn_rect[1] + object_spawn_rect[3]))
                props.append(Prop(spawn_pos,200,0))
                
            while random.uniform(0,1) < 0.4:
                spawn_pos = (random.randint(object_spawn_rect[0], object_spawn_rect[0] + object_spawn_rect[2]),
                             random.randint(object_spawn_rect[1], object_spawn_rect[1] + object_spawn_rect[3]))
                props.append(Prop(spawn_pos,50,1))
                
            while random.uniform(0,1) < 0.4:
                spawn_pos = (random.randint(object_spawn_rect[0], object_spawn_rect[0] + object_spawn_rect[2]),
                            random.randint(object_spawn_rect[1], object_spawn_rect[1] + object_spawn_rect[3]))
                props.append(Prop(spawn_pos,50,5))
                
            while random.uniform(0,1) < 0.4:
                spawn_pos = (random.randint(object_spawn_rect[0], object_spawn_rect[0] + object_spawn_rect[2]),
                             random.randint(object_spawn_rect[1], object_spawn_rect[1] + object_spawn_rect[3]))
                props.append(Prop(spawn_pos,50,6))
            
            while random.uniform(0,1) < 0.4:
                spawn_pos = (random.randint(object_spawn_rect[0], object_spawn_rect[0] + object_spawn_rect[2]),
                             random.randint(object_spawn_rect[1], object_spawn_rect[1] + object_spawn_rect[3]))
                props.append(Prop(spawn_pos,50,7))

            floor_tiles = []
            for i in range(res[0]//32 + 1):
                for j in range(res[1]//32 + 1):
                    floor_tiles.append(FloorTile((16 + 32*i ,16 + 32*j),pygame.image.load("assets/carpet2.png")))

            door1_location = random.randint(3,7)
            door2_location = random.randint(9,res[0]//32 -11)
            door1_open = False
            door2_open = False
            for i in range(res[0]//32):
                if i == door1_location:
                    door = Prop((16 + 32*i, 32), 1000, 4)
                    props.append(door)
                    door1_pos = (16 + 32*i, 32)
                    
                elif i == door2_location:
                    door2 = Prop((16 + 32*i, 32), 1000, 4)
                    props.append(door2)
                    door2_pos = (16 + 32*i, 32)
                else:
                    props.append(Prop((16 + 32*i, 32), 60, 2))

                props.append(Prop((16 + 32*i, res[1] - 10), 60, 8))

            for i in range(res[1]//64 + 1):
                props.append(Prop((10, 32 + 64*i), 60, 3))
                props.append(Prop((res[0] - 10, 32 + 64*i), 60, 3))

            bullets = []

            w_pressed = False
            a_pressed = False
            s_pressed = False
            d_pressed = False
            dt = 0

            unscaled_image = pygame.image.load("assets/health_bar.png")
            health_bar_image = pygame.transform.scale(unscaled_image, (unscaled_image.get_width()*0.5, unscaled_image.get_height()*0.5))

            def generate_health_bar(health_fraction):
                health_colour = (max(min(255-255*health_fraction,255),0),max(min(255*health_fraction,255),0),0)
                surface = pygame.Surface((int((28+195)*health_fraction), 30),pygame.SRCALPHA)
                pygame.draw.polygon(surface, health_colour, [(0,0),(30,0),(30,30)])
                pygame.draw.rect(surface, health_colour, [30,0,195,30])
                return surface

            def open_door(door1_open):
                reach = 100
                if not door1_open and len(enemies) == 0 and (player.pos[0] - door1_pos[0])**2 + (player.pos[1] - door1_pos[1])**2 < reach**2:
                    door1_open = True
                    props.remove(door)
                return door1_open

            def open_door2(door2_open):
                reach = 100
                if not door2_open and len(enemies) == 0 and (player.pos[0] - door2_pos[0])**2 + (player.pos[1] - door2_pos[1])**2 < reach**2:
                    door2_open = True
                    props.remove(door2)
                return door2_open
                    
            room_completed = False

            while not room_completed:
                pygame.event.set_grab(True)
                
                for event in pygame.event.get():

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.event.set_grab(False)
                            pygame.quit()
                            quit()

                        if event.key == pygame.K_w: w_pressed = True
                        elif event.key == pygame.K_a: a_pressed = True
                        elif event.key == pygame.K_s: s_pressed = True
                        elif event.key == pygame.K_d: d_pressed = True

                        elif event.key == pygame.K_e:
                            door1_open = open_door(door1_open)
                            door2_open = open_door2(door2_open)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w: w_pressed = False
                        elif event.key == pygame.K_a: a_pressed = False
                        elif event.key == pygame.K_s: s_pressed = False
                        elif event.key == pygame.K_d: d_pressed = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            player.gun.shoot()

                for enemy in enemies:
                    if random.randint(1,10) == 10: enemy.gun.shoot()

                player.move()

                if door1_open and player.pos[1] < 50:
                    room_completed = True
                    
                elif door2_open and player.pos[1] < 50:
                    room_completed = True
                    #####

                for bullet in bullets:
                    bullet.update()

                for enemy in enemies:
                    enemy.update()
                    if enemy.health <= 0 and not enemy.dead:
                        enemy.die()

                if player.health <= 0:
                    player.update()
                    player.die()

                # display

                screen.fill("black")
                
                for floor_tile in floor_tiles:
                    screen.blit(floor_tile.image, (floor_tile.pos[0] - floor_tile.width//2, floor_tile.pos[1] - floor_tile.height//2))

                if not player.dead:
                    screen.blit(player.images[int(player.animation_timer * player.animation_speed * player.animation_frames) % player.animation_frames], \
                                (player.pos[0] - player.width//2, player.pos[1] - player.height//2))
                else:
                    screen.blit(player.death_images[int(player.death_animation_timer * player.death_animation_speed * player.death_animation_frames) % player.death_animation_frames], \
                                    (player.pos[0] - player.width//2, player.pos[1] - player.height//2))
                    
                for enemy in enemies:
                    if not enemy.dead:
                        screen.blit(enemy.images[int(enemy.animation_timer * enemy.animation_speed * enemy.animation_frames)% enemy.animation_frames], \
                                    (enemy.pos[0] - enemy.width//2, enemy.pos[1] - enemy.height//2))
                    else:
                        screen.blit(enemy.death_images[int(enemy.death_animation_timer * enemy.death_animation_speed * enemy.death_animation_frames) % enemy.death_animation_frames], \
                                    (enemy.pos[0] - enemy.width//2, enemy.pos[1] - enemy.height//2))

                for prop in props:
                    screen.blit(prop.image, (prop.pos[0] - prop.width//2, prop.pos[1] - prop.height//2))

                for cash in cashes:
                    screen.blit(cash.image, (cash.pos[0] - cash.width//2, cash.pos[1] - cash.height//2))


                for bullet in bullets:
                    screen.blit(bullet.image, (bullet.pos[0] - bullet.width//2, bullet.pos[1] - bullet.height//2))
                
                    
                mouse_pos = pygame.mouse.get_pos()
                player.gun.update(mouse_pos)
                screen.blit(player.gun.image, (player.gun.pos[0] - player.gun.width//2, player.gun.pos[1] - player.gun.height//2))

                for enemy in enemies:
                    enemy.gun.update(player.pos)
                    screen.blit(enemy.gun.image, (enemy.gun.pos[0] - enemy.gun.width//2, enemy.gun.pos[1] - enemy.gun.height//2))

                #UI display
                health_bar_pos = (res[0]-140,40)
                screen.blit(health_bar_image, (health_bar_pos[0] - health_bar_image.get_width()//2, health_bar_pos[1] - health_bar_image.get_height()//2))
                health_fraction = max(min(player.health/player.max_health, 1), 0)
                screen.blit(generate_health_bar(health_fraction), (res[0] - 250,25))
                
                
                pygame.display.update()
                dt = clock.tick(60)/1000
            player_x = player.pos[0]
            player_health = player.health

if __name__ == "__main__":
    pygame.mixer.init()
    pygame.mixer.music.load("assets/music/TheWayForwarder.mp3")
    pygame.mixer.music.play(-1)
    main()
