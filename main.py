import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 3/4 * WIDTH

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Samurai Game")

run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        run = False
        
pygame.quit()
