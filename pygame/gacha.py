import pygame
import sys
import random


pygame.init()
screen = pygame.display.set_mode((800, 400))


img = pygame.image.load("doc/5_star/Columbina.png").convert_alpha()

running = True
x = 0 
clock = pygame.time.Clock()
delta_time = 0.1
while running:
    screen.fill((255, 255, 255))
    screen.blit(img, (x, 0))

    x += 50*delta_time
    
    
    
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            running = False
    pygame.display.flip()
    delta_time = clock.tick(60)/1000
    delta_time = min(delta_time, 0.05)

pygame.quit()