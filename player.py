import pygame


moving_right = False
moving_left = False


class Player:
    def __init__(self, x, y, charachter, speed, direction, scale=1):
        self.x = x
        self.y = y
        self.character = charachter
        self.path = f"assets/img/{charachter}/"
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(x, y, 60, 40)
        self.color = (255, 0, 0)
        self.flip = False
        self.jump = False
        self.in_air = True

    def draw(self):
        surface = pygame.display.get_surface()
        if surface:
            pygame.draw.rect(surface, self.color, self.rect)

    def move(self, moving_right, moving_left):
        dx = 0
        dy = 0

        if moving_right:
            self.direction = 1
            self.flip = False
            dx = self.speed
        elif moving_left: 
            self.direction *= -1
        elif moving_left:
            self.direction = -1
            self.flip = True
            dx = -self.speed
        if self.jump == True and self.in_air == False:
            self.y -= -14
            self.jump = False
            self.in_air = True 
            

    def update(self):
        pygame.display.update()
