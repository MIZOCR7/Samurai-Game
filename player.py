import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, charachter, speed, direction, scale, floor_y=500):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.character = charachter 
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(x, y, 60, 40)
        self.color = (255, 0, 0)
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
        self.displacement = 0
        
        
        
        if self.character == 'player':
            for index, animation_name in enumerate(self.animation_types):
                sheet = pygame.image.load(f"assets/img/{charachter}/{animation_name}/{animation_name}.png").convert_alpha()
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
        
        if self.character == 'Samurai':
            for index, animation_name in enumerate(self.animation_types):
                sheet = pygame.image.load(f"assets/img/{charachter}/{animation_name}/{animation_name}.png").convert_alpha()
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
            
            player_hitbox = pygame.Rect(self.rect.x + 50, self.rect.y + 50, self.rect.width - 90, player.rect.height - 50) 
            pygame.draw.rect(screen, (255,0,0), player_hitbox) 
            
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
            self.rect.y += self.vel_y 

            if self.rect.y >= self.floor_y - self.rect.height:
                self.rect.y = self.floor_y - self.rect.height 
                self.vel_y = 0
                self.in_air = False 
        
        
    def player2_move(self, moving_right, moving_left, screen, player):
        if self.alive:
            dx = 0
            
            my_collide_box = pygame.Rect(self.rect.x + 50, self.rect.y + 50, self.rect.width - 90, player.rect.height - 50) 
            
            target_collide_box = pygame.Rect(self.rect.x + 50, self.rect.y + 50, self.rect.width - 90, player.rect.height - 50) 
            
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
                self.vel_y = -17
                self.jump = False
                self.in_air = True
            
            self.vel_y += self.gravity
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed
            
            self.rect.x += dx
            my_collide_box.x += dx
            if my_collide_box.colliderect(target_collide_box) and abs(my_collide_box.bottom - target_collide_box.bottom) < 20:
                self.rect.x -= dx
            
            
            self.rect.y += self.vel_y 
            
            if self.rect.y >= self.floor_y - self.rect.height:
                self.rect.y = self.floor_y - self.rect.height
                self.vel_y = 0
                self.in_air = False
            
            
            
            
            
                
    def attack(self, screen, player):
        player_hitbox = pygame.Rect(0, 0, 60, player.rect.height)
        player_hitbox.center = player.rect.center
        
        if not self.shield: 
            if self.character == 'player' or (self.character == 'Samurai' and not self.attack_3):
                if (self.attack_1 or self.attack_2 or self.attack_3):
                    
                    box_x = self.rect.right - 90 if self.direction == 1 else (self.rect.left + 40) 
                    
                    attack_box = pygame.Rect(box_x, self.rect.y + 60, 50, self.rect.height - 60) 
                    
                    pygame.draw.rect(screen, (255,0,0), attack_box)
                    if attack_box.colliderect(player_hitbox): 
                        if player.shield:
                            player.rect.x += player.direction * 20
                        else:
                            player.hurt = True 
                        
            elif (self.character == 'Samurai' and self.attack_3): 
                if self.direction == 1:
                    attack_box = pygame.Rect((self.rect.x + 70), self.rect.y  + 70, (self.rect.width - 80) * self.direction, self.rect.height - 70) 
                elif self.direction == -1:
                    attack_box = pygame.Rect((self.rect.left), self.rect.y + 70, (self.rect.width - 60), self.rect.height - 70)
                
                pygame.draw.rect(screen, (255,0,0), attack_box)
                if attack_box.colliderect(player_hitbox): 
                    if player.shield:
                        player.rect.x += self.direction * 20 
                    else:
                        player.hurt = True
                            
        
    
    
    def update(self):
        self.update_action()
        self.update_animation()
    
