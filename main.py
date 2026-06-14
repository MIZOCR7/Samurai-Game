import pygame
import random
from player import *

pygame.init()

WIDTH = 800
HEIGHT = int(3/4 * WIDTH)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Samurai Game")


player = Player(200, 200, 'player', 3, 1)

def main():
  player.draw()
  player.update()
  
  
  
  
  run = True
  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          run = False
        if event.key == pygame.K_a:
          moving_left = True
        if event.key == pygame.K_d:
          moving_right = True
        if event.key == pygame.K_SPACE:
          player.jump = True
        
  pygame.quit()
  

if __name__ == "__main__":
  main()
