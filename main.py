import pygame
from player import Player

pygame.init()

clock = pygame.time.Clock()

WIDTH = 800 
HEIGHT = int(3/4 * WIDTH)
GROUND_Y = HEIGHT - 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Samurai Game")

player = Player(500, GROUND_Y - 40, 'player', 5, 1, 1.25, floor_y=GROUND_Y)
enemy = Player(340, GROUND_Y - 40, 'Samurai', 5, 1, 1.25, floor_y=GROUND_Y)

def main():
    
    background_img = pygame.image.load("assets/background.png").convert()
    background_img = pygame.transform.scale(background_img, (800, 600))
     
    
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
                
                if player.alive:
                    if event.key == pygame.K_z:
                        player.attack_1 = True
                    if event.key == pygame.K_x:
                        player.attack_2 = True
                    if event.key == pygame.K_c:
                        player.attack_3 = True 
                    if event.key == pygame.K_q:
                        player.shield = True
                
                if event.key == pygame.K_t:
                    player.alive = False 
                    enemy.alive = False 
                
                if event.key == pygame.K_k:
                    player2_move_right = True
                if event.key == pygame.K_h:
                    player2_move_left = True
                if event.key == pygame.K_u:
                    enemy.jump = True
                
                if enemy.alive: 
                    if event.key == pygame.K_b:
                        enemy.attack_1 = True
                    if event.key == pygame.K_n:
                        enemy.attack_2 = True
                    if event.key == pygame.K_m:
                        enemy.attack_3 = True 
                    if event.key == pygame.K_y:
                        enemy.shield = True
        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                    player.run = False
                if event.key == pygame.K_d:
                    moving_right = False
                    player.run = False
                if event.key == pygame.K_q:
                    player.shield = False
   
                if event.key == pygame.K_k:
                    player2_move_right = False
                if event.key == pygame.K_h:
                    player2_move_left = False
                if event.key == pygame.K_u:
                    enemy.jump = False
                if event.key == pygame.K_y:
                    enemy.shield = False 
                    
            
        screen.blit(background_img, (0, 0))
        
        
        pygame.draw.line(screen, (76, 85, 91), (0, GROUND_Y), (WIDTH, GROUND_Y))
        player.move(moving_right, moving_left, screen, enemy) 
        player.bars(screen, enemy) 
        player.attack(screen, enemy) 
        player.draw() 
        player.update() 
        enemy.player2_move(player2_move_right, player2_move_left, screen, player)
        enemy.attack(screen, player)
        enemy.draw() 
        enemy.update() 
        
        
        
        
    
    
    
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
