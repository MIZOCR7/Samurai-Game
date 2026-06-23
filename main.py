import pygame
import os
import sys
from player import Player
from pygame import mixer


pygame.init()
pygame.joystick.init()
pygame.mixer.init()

clock = pygame.time.Clock()

WIDTH = 800 
HEIGHT = int(3/4 * WIDTH)
GROUND_Y = HEIGHT - 50 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Samurai Game")


def draw_text(surface, text, size, x, y, color=(255,255,255)):
    font = pygame.font.Font(None, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    surface.blit(text_surf, text_rect)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_connected_joysticks():
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        if not joystick.get_init():
            joystick.init()
        joysticks.append(joystick)
    return joysticks


def _joy_get_id(joystick):
    try:
        return joystick.get_instance_id()
    except Exception:
        try:
            return joystick.get_id()
        except Exception:
            return None


def _event_joy_id(event):
    return getattr(event, 'instance_id', getattr(event, 'joy', None))


def assign_joysticks(joysticks):
    enemy_joystick = joysticks[0] if len(joysticks) >= 1 else None
    player_joystick = joysticks[1] if len(joysticks) >= 2 else None
    return enemy_joystick, player_joystick


def reset_game():
    player = Player(100, GROUND_Y - 40, 'player', 5, 1, 1.25, floor_y=GROUND_Y)
    enemy = Player(550, GROUND_Y - 40, 'Samurai', 5, 1, 1.25, floor_y=GROUND_Y)
    return player, enemy


def main():
    
    background_img = pygame.image.load(resource_path("assets/background.png")).convert()
    background_img = pygame.transform.scale(background_img, (800, 600))
    
    countdown = 3
    last_count_update = pygame.time.get_ticks()
    
    hit1 = pygame.mixer.Sound(resource_path("assets/music/hit1.wav"))
    hit1.set_volume(0.4)
    
    punch = pygame.mixer.Sound(resource_path("assets/music/punch.mp3"))
    punch.set_volume(0.5)
    
    shield = pygame.mixer.Sound(resource_path('assets/music/shield.wav'))
    shield.set_volume(0.4)
    
    jump_fx = pygame.mixer.Sound(resource_path('assets/music/jump.wav'))
    jump_fx.set_volume(0.3)
    
    win_fx = pygame.mixer.Sound(resource_path("assets/music/win.mp3"))
    win_fx.set_volume(0.4)
    
    main_fx = pygame.mixer.Sound(resource_path('assets/music/background.mp3'))
    main_fx.set_volume(0.2)
    main_fx.play()
    
    go_fx = pygame.mixer.Sound(resource_path('assets/music/go.mp3'))
    go_fx.set_volume(0.4)
    
    count_fx = pygame.mixer.Sound(resource_path("assets/music/count.mp3"))
    count_fx.set_volume(0.4)
    
    moving_right = False
    moving_left = False
    player2_move_right = False
    player2_move_left = False

    player, enemy = reset_game()

    joysticks = get_connected_joysticks()
    enemy_joystick, player_joystick = assign_joysticks(joysticks)
    joystick_axis_threshold = 0.5

    game_state = 'menu'
    death_time = None
    dead_name = None

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                if game_state == 'menu':
                    if event.key == pygame.K_RETURN:
                        player, enemy = reset_game()
                        game_state = 'countdown'
                        countdown = 3
                        last_count_update = pygame.time.get_ticks()
                        count_fx.play()
                    continue

                if game_state == 'game_over':
                    if event.key == pygame.K_RETURN:
                        game_state = 'menu'
                    continue

                if game_state == 'countdown':
                    continue

                if event.key == pygame.K_a:
                    moving_left = True
                    player.run = True
                if event.key == pygame.K_d:
                    moving_right = True
                    player.run = True
                if event.key == pygame.K_SPACE:
                    player.jump = True
                    jump_fx.play()

                if player.alive: 
                    if event.key == pygame.K_z:
                        player.attack_1 = True
                        hit1.play()
                    if event.key == pygame.K_x:
                        player.attack_2 = True
                        hit1.play()
                    if event.key == pygame.K_c:
                        player.attack_3 = True
                        hit1.play() 
                    if event.key == pygame.K_q:
                        player.shield = True

                if event.key == pygame.K_k:
                    player2_move_right = True
                if event.key == pygame.K_h:
                    player2_move_left = True
                if event.key == pygame.K_u:
                    enemy.jump = True
                    jump_fx.play()

                if enemy.alive:
                    if event.key == pygame.K_b:
                        enemy.attack_1 = True
                        hit1.play() 
                    if event.key == pygame.K_n:
                        enemy.attack_2 = True
                        hit1.play()
                    if event.key == pygame.K_m:
                        enemy.attack_3 = True
                        hit1.play()
                    if event.key == pygame.K_y:
                        enemy.shield = True

            elif event.type == pygame.JOYBUTTONDOWN:
                if game_state != 'playing':
                    continue

                ejid = _event_joy_id(event)
                if enemy_joystick is not None and ejid is not None and ejid == _joy_get_id(enemy_joystick):
                    if event.button == 0:
                        enemy.attack_1 = True
                        hit1.play()
                    if event.button == 1:
                        enemy.attack_2 = True
                        hit1.play()
                    if event.button == 2:
                        enemy.attack_3 = True
                        hit1.play()
                    if event.button == 3:
                        enemy.shield = True
                    if event.button == 4:
                        enemy.jump = True
                        jump_fx.play()
                    if event.button == 5:
                        enemy.shoot_fireball = True
                elif player_joystick is not None and ejid is not None and ejid == _joy_get_id(player_joystick):
                    if event.button == 0:
                        player.attack_1 = True
                        hit1.play()
                    if event.button == 1:
                        player.attack_2 = True
                        hit1.play()
                    if event.button == 2:
                        player.attack_3 = True
                        hit1.play()
                    if event.button == 3:
                        player.shield = True
                    if event.button == 4:
                        player.jump = True
                        jump_fx.play()
                    if event.button == 5:
                        player.shoot_fireball = True

            elif event.type == pygame.JOYBUTTONUP:
                if game_state != 'playing':
                    continue

                ejid = _event_joy_id(event)
                if enemy_joystick is not None and ejid is not None and ejid == _joy_get_id(enemy_joystick):
                    if event.button == 3:
                        enemy.shield = False
                    if event.button == 4:
                        enemy.jump = False
                    if event.button == 5:
                        enemy.shoot_fireball = False
                elif player_joystick is not None and ejid is not None and ejid == _joy_get_id(player_joystick):
                    if event.button == 3:
                        player.shield = False
                    if event.button == 4:
                        player.jump = False
                    if event.button == 5:
                        player.shoot_fireball = False

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

            elif event.type == pygame.JOYDEVICEADDED or event.type == pygame.JOYDEVICEREMOVED:
                joysticks = get_connected_joysticks()
                enemy_joystick, player_joystick = assign_joysticks(joysticks)

        screen.blit(background_img, (0, 0))

        if game_state == 'menu':
            draw_text(screen, "Samurai Game", 64, WIDTH//2, HEIGHT//4)
            draw_text(screen, "Instructions:", 36, WIDTH//2, HEIGHT//4 + 70)
            draw_text(screen, "Player: A/D move, SPACE jump, Z/X/C attacks, Q shield", 24, WIDTH//2, HEIGHT//4 + 110)
            draw_text(screen, "Enemy: H/K move, U jump, B/N/M attacks, Y shield", 24, WIDTH//2, HEIGHT//4 + 140)
            draw_text(screen, "Press ENTER to start", 28, WIDTH//2, HEIGHT - 120)
        elif game_state == 'countdown':
            pygame.draw.line(screen, (76, 85, 91), (0, GROUND_Y), (WIDTH, GROUND_Y))
            
           
            player.bars(screen, enemy)

            
            current_time = pygame.time.get_ticks()
            if current_time - last_count_update >= 1000:
                countdown -= 1
                last_count_update = current_time
                
                if countdown < 0:
                    game_state = 'playing'

            
            if countdown > 0:
                draw_text(screen, str(countdown), 100, WIDTH // 2, HEIGHT // 2, (255, 215, 0))
            elif countdown == 0:
                draw_text(screen, "GO!", 120, WIDTH // 2, HEIGHT // 2, (0, 255, 0))

        elif game_state == 'playing':
            pygame.draw.line(screen, (76, 85, 91), (0, GROUND_Y), (WIDTH, GROUND_Y))

            
            if player_joystick is None:
                player_move_right = moving_right
                player_move_left = moving_left
                if enemy_joystick is None:
                    enemy_move_right = player2_move_right
                    enemy_move_left = player2_move_left
                else:
                    axis_x = enemy_joystick.get_axis(0)
                    enemy_move_right = axis_x > joystick_axis_threshold
                    enemy_move_left = axis_x < -joystick_axis_threshold
            else:
                axis_x = player_joystick.get_axis(0)
                player_move_right = axis_x > joystick_axis_threshold
                player_move_left = axis_x < -joystick_axis_threshold
                enemy_move_right = player2_move_right
                enemy_move_left = player2_move_left

            
            if enemy_joystick is not None and player_joystick is None:
                axis_x = enemy_joystick.get_axis(0)
                enemy_move_right = axis_x > joystick_axis_threshold
                enemy_move_left = axis_x < -joystick_axis_threshold

            player.move(player_move_right, player_move_left, screen, enemy)
            player.bars(screen, enemy)
            player.health_tiles(screen, enemy)
            player.fireballs(enemy)
            player.attack(screen, enemy, punch, shield)
            player.draw(screen)
            player.update() 
            enemy.player2_move(enemy_move_right, enemy_move_left, screen, player)
            enemy.attack(screen, player, punch, shield)
            enemy.fireballs(player)
            enemy.draw(screen) 
            enemy.update()

            if (not player.alive or not enemy.alive) and death_time is None:
                death_time = pygame.time.get_ticks()
                if not player.alive:
                    dead_name = "Ninja"
                else:
                    dead_name = "Samurai"

            if death_time is not None:
                if pygame.time.get_ticks() - death_time >= 5000:
                    game_state = 'game_over'

        elif game_state == 'game_over':
            if dead_name is None: 
                draw_text(screen, "Game Over", 48, WIDTH//2, HEIGHT//2)
            else:
                draw_text(screen, f"{dead_name} died", 48, WIDTH//2, HEIGHT//2 - 20)
                draw_text(screen, "Press ENTER to return to menu", 28, WIDTH//2, HEIGHT//2 + 40)
                win_fx.play()
            
            death_time = None
            dead_name = None

        pygame.display.update()
    pygame.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
