import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, charachter, speed, direction, scale=1, floor_y=500):
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
        self.gravity = 0.75
        self.max_fall_speed = 10
        self.floor_y = floor_y
        self.animation_list = []
        self.counter = 0
        self.frame_index = 0
        self.spritesheet = pygame.image.load(f"assets/img/{charachter}/idle/idle.png").convert_alpha() 
        self.run = False
        self.alive = True 
        self.hurt = False 
        self.action = 0
        self.idle = True
        self.run = False
        self.num_of_frames = 6
        self.frame_width = int(self.spritesheet.get_width() / self.num_of_frames)
        self.frame_height = self.spritesheet.get_height()

        for i in range(self.num_of_frames):
            x_coor = i * self.frame_width
            slice_rect = pygame.Rect(x_coor, 0, self.frame_width, self.frame_height)
            frame_image = self.spritesheet.subsurface(slice_rect)
            self.animation_list.append(frame_image)
        self.frame_index = 0
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
            
        
    def animation(self):
        if self.idle and not self.in_air:
            num_of_frames = 6 
        
        
            
            
        
    def draw(self):
        surface = pygame.display.get_surface()
        if surface:
            surface.blit(self.image, self.rect)
        

    def move(self, moving_right, moving_left):
        dx = 0

        if moving_right:
            self.direction = 1
            self.flip = False
            dx = self.speed
            if self.rect.right - dx >= 850:
                self.rect.right = 850
                
        elif moving_left:
            self.direction = -1
            self.flip = True
            dx = -self.speed
            if self.rect.left <= -40:
                self.rect.left = -40

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
       
    def update_animation(self):
        animation_cooldown = 0.15
        
        self.frame_index += animation_cooldown
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            
        self.image = self.animation_list[int(self.frame_index)]
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.transform.flip(self.image, False, False)
    
    def update(self):
        self.update_animation()
        
