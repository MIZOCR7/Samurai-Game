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
        self.animation_types = ['idle', 'run', 'jump', 'attack1', 'attack2', 'attack3']
        self.number_of_frames_list = [6, 8, 10, 4, 3, 4] 
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
        self.attack1_cooldown = 4 

        for index, animation_name in enumerate(self.animation_types):
            sheet = pygame.image.load(f"assets/img/{charachter}/{animation_name}/{animation_name}.png").convert_alpha()
            temp_list = []
            num_of_frames = self.number_of_frames_list[index] 
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
        if self.in_air:
            new_action = 2
            
            
        if self.attack_1:
            new_action = 3 
        elif self.attack_2:
            new_action = 4
        elif self.attack_3:
            new_action = 5
            
            
                 

        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
    
    def update_animation(self):
        animation_cooldown = 5 
        
        self.counter += 1
        if self.counter >= animation_cooldown:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                self.attack_1 = False
                self.attack_2 = False
                self.attack_3 = False
                
        
        current_frame = self.animation_list[self.action][self.frame_index]
        self.image = pygame.transform.flip(current_frame, self.flip, False)
        
    def draw(self):
        surface = pygame.display.get_surface()
        if surface:
            surface.blit(self.image, self.rect)
        

    def move(self, moving_right, moving_left):
        dx = 0
        
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
       
    
    def player2_move(moving_right, moving_left):
        pass 
    
    
    def update(self):
        self.update_action()
        self.update_animation()
        

