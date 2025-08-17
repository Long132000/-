import pygame
import sys

pygame.init()
win = pygame.display.set_mode((1000, 1000)) # размеры X и Y
pygame.display.set_caption("Игра говно")

run = True
while(run):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False

black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

    
pygame.quit()
