import pygame
import os
import sys
import random

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, charachter, speed, direction, scale, floor_y=500):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.character = charachter 
        self.speed = speed 
        self.direction = direction
        self.rect = pygame.Rect(x, y, 60, 40) 
        self.flip = False
        self.jump = False
        self.in_air = False
        self.vel_y = 0
        self.scale = scale
        self.gravity = 0.75
        self.max_fall_speed = 10
        self.floor_y = floor_y
        self.animation_list = []
        self.animation_types = ['idle', 'run', 'jump', 'attack1', 'attack2', 'attack3', 'shield', 'death', 'hurt']
        self.player2_no_frames = [6, 8, 12, 6, 4, 3, 2, 3, 2] 
        self.number_of_frames_list = [6, 8, 10, 4, 3, 4, 2, 3, 3] 
        self.counter = 0
        self.frame_index = 0 
        self.run = False
        self.alive = True 
        self.hurt = False 
        self.action = 0
        self.idle = True
        self.run = False 
        self.attack_1 = False
        self.attack_2 = False
        self.attack_3 = False
        self.hurt = False  
        self.shield = False 
        self.health = 100 
        self.max_health = self.health
        self.attack_cooldown = False
        self.font = pygame.font.Font(None, 28) 
        self.special_power = 0
        self.max_power = 100
        self.displacement = 20
        self.tile_image = pygame.image.load('assets/img/img.png').convert_alpha()
        self.tile_rect = None
        self.spawn_cooldown = 5000
        self.next_spawn_time = pygame.time.get_ticks()

        if self.character == 'player':
            for index, animation_name in enumerate(self.animation_types):
                sheet = pygame.image.load(resource_path(f"assets/img/{charachter}/{animation_name}/{animation_name}.png")).convert_alpha()
                temp_list = []
                num_of_frames = self.number_of_frames_list[index] 
                frame_width = int(sheet.get_width() / num_of_frames)
                frame_height = sheet.get_height() 
                for i in range(num_of_frames):
                    x_coor = i * frame_width 
                    slice_rect = pygame.Rect(x_coor, 0, frame_width, frame_height)
                    self.frame_image = sheet.subsurface(slice_rect)
                    
                    new_width = int(frame_width * self.scale)
                    new_height = int(frame_height * self.scale)
                    
                    self.frame_image = pygame.transform.scale(self.frame_image, (new_width, new_height))
                    
                    temp_list.append(self.frame_image)
                
                self.animation_list.append(temp_list)
            self.action = 0 
            self.frame_index = 0
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.rect.bottom = self.floor_y
        
        if self.character == 'Samurai':
            for index, animation_name in enumerate(self.animation_types):
                sheet = pygame.image.load(resource_path(f"assets/img/{charachter}/{animation_name}/{animation_name}.png")).convert_alpha()
                temp_list = []
                num_of_frames = self.player2_no_frames[index] 
                frame_width = int(sheet.get_width() / num_of_frames)
                frame_height = sheet.get_height() 
                for i in range(num_of_frames):
                    x_coor = i * frame_width 
                    slice_rect = pygame.Rect(x_coor, 0, frame_width, frame_height)
                    frame_image = sheet.subsurface(slice_rect)
                    
                    new_width = int(frame_width * self.scale)
                    new_height = int(frame_height * self.scale)
                    
                    frame_image = pygame.transform.scale(frame_image, (new_width, new_height))
                    
                    temp_list.append(frame_image)
                
                self.animation_list.append(temp_list)
            self.action = 0 
            self.frame_index = 0
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.rect.bottom = self.floor_y

    def update_action(self): 
        new_action = 0
        if self.run:
           new_action = 1
           self.shield = False
        if self.in_air:
            new_action = 2
        
        if not self.alive:
           new_action = 7
        
        if self.hurt:
            new_action = 8 
        
        if self.attack_1:
            new_action = 3 
        elif self.attack_2:
            new_action = 4
        elif self.attack_3:
            new_action = 5
        elif self.shield:
            new_action = 6 
                    


        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
        
        
    def update_animation(self):
        animation_cooldown = 5 
        
        if self.in_air:
            animation_cooldown = 3
        
        self.counter += 1
        if self.counter >= animation_cooldown:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                self.attack_1 = False
                self.attack_2 = False 
                self.attack_3 = False
                self.hurt = False
                self.attack_cooldown = False
                
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1 
                
        
        current_frame = self.animation_list[self.action][self.frame_index]
        self.image = pygame.transform.flip(current_frame, self.flip, False) 
        
    def draw(self):
        surface = pygame.display.get_surface()
        if surface:
            surface.blit(self.image, self.rect) 
        

    def move(self, moving_right, moving_left, screen, player):
        if self.alive: 
            dx = 0 
            global my_collide_box
            global target_collide_box
            
            my_collide_box = pygame.Rect(self.rect.x + 45, self.rect.y + 50, self.rect.width - 100, self.rect.height - 50)
            target_collide_box = pygame.Rect(player.rect.x + 50, player.rect.y + 50, player.rect.width - 100, player.rect.height - 50)


            if (self.attack_1 or self.attack_2 or self.attack_3) and not self.in_air:
                moving_right = False
                moving_left = False
                self.run = False

            if moving_right:
                self.direction = 1
                self.flip = False
                self.run = True
                dx = self.speed
            elif moving_left:
                self.direction = -1
                self.flip = True
                self.run = True
                dx = -self.speed
            else:
                self.run = False

            if self.jump and not self.in_air:
                self.vel_y = -14
                self.jump = False
                self.in_air = True

            self.vel_y += self.gravity
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed

            self.rect.x += dx 
            my_collide_box.x += dx
            if player.alive: 
                if my_collide_box.x <= 0: 
                    self.rect.x -= dx
                    self.displacement = 0
                if my_collide_box.right >= 800:
                    self.rect.x -= dx
                    self.displacement = 0
                if my_collide_box.colliderect(target_collide_box):
                    if my_collide_box.bottom > target_collide_box.top + 10:
                        self.rect.x -= dx
                        my_collide_box.x -= dx

            self.rect.y += self.vel_y
            my_collide_box.y += self.vel_y
            if player.alive:
                if my_collide_box.colliderect(target_collide_box):
                    if self.vel_y > 0 and (my_collide_box.bottom - self.vel_y <= target_collide_box.top + 10):
                        sink_offset = my_collide_box.bottom - target_collide_box.top
                        self.rect.y -= sink_offset
                        self.vel_y = 0
                        self.in_air = False

            if self.rect.y >= self.floor_y - self.rect.height:
                self.rect.y = self.floor_y - self.rect.height
                self.vel_y = 0
                self.in_air = False
        
        
        
    def player2_move(self, moving_right, moving_left, screen, player):
        if self.alive:
            dx = 0
            my_collide_box = pygame.Rect(self.rect.x + 45, self.rect.y + 50, self.rect.width - 100, self.rect.height - 50)
            target_collide_box = pygame.Rect(player.rect.x + 50, player.rect.y + 50, player.rect.width - 100, player.rect.height - 50)

            if moving_right:
                self.direction = 1
                self.flip = False
                self.run = True
                dx = self.speed
            elif moving_left:
                self.direction = -1
                self.flip = True
                self.run = True
                dx = -self.speed
            else:
                self.run = False

            if self.jump and not self.in_air:
                self.vel_y = -14
                self.jump = False
                self.in_air = True

            self.vel_y += self.gravity
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed

            self.rect.x += dx
            my_collide_box.x += dx 
            if player.alive:
                if my_collide_box.x <= 0: 
                    self.rect.x -= dx
                    self.displacement = 0
                if my_collide_box.right >= 800:
                    self.rect.x -= dx
                    self.displacement = 0
                if my_collide_box.colliderect(target_collide_box):
                    if my_collide_box.bottom > target_collide_box.top + 10:
                        self.rect.x -= dx 

            self.rect.y += self.vel_y
            my_collide_box.y += self.vel_y
            if player.alive: 
                if my_collide_box.colliderect(target_collide_box):
                    if self.vel_y > 0 and (my_collide_box.bottom - self.vel_y <= target_collide_box.top + 10):
                        sink_offset = my_collide_box.bottom - target_collide_box.top
                        self.rect.y -= sink_offset
                        self.vel_y = 0
                        self.in_air = False

            if self.rect.y >= self.floor_y - self.rect.height:
                self.rect.y = self.floor_y - self.rect.height
                self.vel_y = 0
                self.in_air = False
            
  
      
            
            
                
    def attack(self, screen, player, punch_fx, shield_fx):
        player_hitbox = pygame.Rect(self.rect.x + 45, self.rect.y + 50, self.rect.width - 100, self.rect.height - 50)
        player_hitbox.center = player.rect.center 
        
        
        if player.alive:
            if not self.shield: 
                if self.character == 'player' or (self.character == 'Samurai' and not self.attack_3):
                    if (self.attack_1 or self.attack_2 or self.attack_3):
                        
                        box_x = self.rect.right - 90 if self.direction == 1 else (self.rect.left + 40) 
                        
                        attack_box = pygame.Rect(box_x, self.rect.y + 60, 50, self.rect.height - 60) 
                        
                        
                        if attack_box.colliderect(player_hitbox): 
                            if player.shield: 
                                target_x = player.rect.x + (self.direction * self.displacement)
                                if target_x + 45 >= 0 and target_x + (player.rect.width - 55) <= 800:
                                    player.rect.x = target_x
                                shield_fx.play()
                            else:
                                player.hurt = True
                                if not self.attack_cooldown:
                                    player.health -= 10
                                    self.special_power = min(self.max_power, self.special_power + 10)
                                    punch_fx.play()
                                    self.attack_cooldown = True
                                    if player.health <= 0:
                                        player.alive = False
                                        player.health = 0
                                        
                
                
                elif (self.character == 'Samurai' and self.attack_3): 
                    if self.direction == 1:
                        attack_box = pygame.Rect((self.rect.x + 70), self.rect.y  + 70, (self.rect.width - 80) * self.direction, self.rect.height - 70) 
                    elif self.direction == -1:
                        attack_box = pygame.Rect((self.rect.left), self.rect.y + 70, (self.rect.width - 60), self.rect.height - 70)
    
                    
                    if attack_box.colliderect(player_hitbox): 
                        if player.shield:
                            target_x = player.rect.x + (self.direction * self.displacement)
                            if target_x + 45 >= 0 and target_x + (player.rect.width - 55) <= 800:
                                player.rect.x = target_x 
                            shield_fx.play()
                        else:
                            player.hurt = True
                            if not self.attack_cooldown:
                                    player.health -= 10
                                    self.special_power = min(self.max_power, self.special_power + 10)
                                    self.attack_cooldown = True
                                    punch_fx.play()
                                    if player.health <= 0:
                                        player.alive = False 
                                        player.health = 0
        
    
    def bars(self, screen, enemy):
        
        health_bar = pygame.Rect(50, 50, self.max_health * 2, 20)
        pygame.draw.rect(screen, (0, 0, 0), (45, 45, (self.max_health + 5) * 2, 30))
        pygame.draw.rect(screen, (255,0,0), health_bar)
        health_bar = pygame.Rect(50, 50, self.health * 2, 20)
        pygame.draw.rect(screen, (0,255,0), health_bar)
        p1_text = self.font.render("Ninja", True, (255, 255, 255))
        screen.blit(p1_text, (50, 25))
        

        screen.blit(pygame.Surface((200, 10), pygame.SRCALPHA), (50, 80)) 
        fill_width = int(( self.special_power / self.max_power) * 200)
        power_surface = pygame.Surface((200, 10), pygame.SRCALPHA) 
        pygame.draw.rect(power_surface, (255, 215, 0, 100), (0, 0, 200, 10), width=2, border_radius=5)
        if fill_width > 0:
            pygame.draw.rect(power_surface, (255, 215, 0, 220), (0, 0, fill_width, 10), border_radius=5)
        
        screen.blit(power_surface, (50,80))
        
        
        health_bar = pygame.Rect(550, 50, enemy.max_health * 2, 20)
        pygame.draw.rect(screen, (0, 0, 0), (545, 45, (self.max_health + 5) * 2, 30))
        pygame.draw.rect(screen, (255,0,0), health_bar)
        health_bar = pygame.Rect(550, 50, enemy.health * 2, 20)
        pygame.draw.rect(screen, (0,255,0), health_bar)
        p2_text = self.font.render("Samurai", True, (255, 255, 255))
        screen.blit(p2_text, (672, 25)) 
        
        screen.blit(pygame.Surface((200, 10), pygame.SRCALPHA), (550, 80))
        fill_width = int(( enemy.special_power / self.max_power) * 200)
        power_surface = pygame.Surface((200, 10), pygame.SRCALPHA) 
        pygame.draw.rect(power_surface, (255, 215, 0, 100), (0, 0, 200, 10), width=2, border_radius=5)
        if fill_width > 0:
            pygame.draw.rect(power_surface, (255, 215, 0, 220), (0, 0, fill_width, 10), border_radius=5)
        
        screen.blit(power_surface, (550,80)) 
        
        
    def health_tiles(self,screen, enemy, floor_y=500):
        current_time = pygame.time.get_ticks()
        if self.tile_rect is None and current_time >= self.next_spawn_time:
            rand_x = random.randint(50,750)
            rand_y = floor_y - self.tile_image.get_height()
            self.tile_rect = pygame.Rect(rand_x, rand_y, self.tile_image.get_width(), self.tile_image.get_height())
        
        if self.tile_rect is not None:
                my_hitbox = pygame.Rect(self.rect.x + 45, self.rect.y + 50, self.rect.width - 100, self.rect.height - 50)
                enemy_hitbox = pygame.Rect(enemy.rect.x + 45, enemy.rect.y + 50, enemy.rect.width - 100, enemy.rect.height - 50)
                
                if my_hitbox.colliderect(self.tile_rect):
                    self.health = min(self.max_health, self.health + 20)
                    self.tile_rect = None
                    self.next_spawn_time = current_time + self.spawn_cooldown 
                    enemy.next_spawn_time = self.next_spawn_time
                
                elif self.tile_rect is not None and enemy_hitbox.colliderect(self.tile_rect):
                    enemy.health = min(self.max_health, self.health + 20)
                    self.tile_rect = None
                    self.next_spawn_time = current_time + self.spawn_cooldown
                    enemy.next_spawn_time = self.next_spawn_time 
            
        if self.tile_rect is not None:
                screen.blit(self.tile_image, self.tile_rect)
        
    
    
    
    def update(self):
        self.update_action()
        self.update_animation()
