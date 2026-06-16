import pygame
from player import Player

pygame.init()

clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = int(3/4 * WIDTH)
GROUND_Y = HEIGHT - 100 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Samurai Game")

player = Player(200, GROUND_Y - 40, 'player', 5, 1, 1.25, floor_y=GROUND_Y) 
enemy = Player(200, GROUND_Y - 40, 'Samurai', 5, 1, 1.25, floor_y=GROUND_Y) 

def main():

    moving_right = False
    moving_left = False
    
    player2_move_right = False
    player2_move_left = False

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_a:
                    moving_left = True
                    player.run = True
                if event.key == pygame.K_d:
                    moving_right = True
                    player.run = True
                if event.key == pygame.K_SPACE:
                    player.jump = True
                if event.key == pygame.K_z:
                    player.attack_1 = True
                if event.key == pygame.K_x:
                    player.attack_2 = True
                if event.key == pygame.K_c:
                    player.attack_3 = True 
                
        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                    player.run = False
                if event.key == pygame.K_d:
                    moving_right = False
                    player.run = False
            
        
            
        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (255, 0, 0), (0, GROUND_Y), (WIDTH, GROUND_Y))
        player.move(moving_right, moving_left)
        player.draw()
        player.update()
        
        
        enemy.draw()
        enemy.update()
    
    
    
    
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
