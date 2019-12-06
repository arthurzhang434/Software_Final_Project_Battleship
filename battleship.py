#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:12:41 2019

@author: huaizhong
"""

import pygame
#initialize the pygame
pygame.init()

#Set up the game screen size
screen = pygame.display.set_mode((648,400))
dim = 25
gap = 3

#Title and Icon
pygame.display.set_caption("Arthur's Battleship")
Icon = pygame.image.load("battleship.png")
pygame.display.set_icon(Icon)

#Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (100, 100, 100)
ORANGE = (255, 165, 0)
DARKBLUE = (0, 0, 128)

COLORS = {0: BLUE,1: RED,2: GREEN,3: ORANGE,4: DARKBLUE,5: GREY,6: BLACK,7: WHITE}

#Set up the game board
grid1 = [[0 for i in range(10)] for i in range(10)]
grid2 = [[0 for i in range(10)] for i in range(10)]

def draw_board():
    screen.fill(COLORS[6])#single_player.screen = pygame.display.set_mode(dimension)
    for row in range(len(grid1)):
        for column in range(len(grid1[row])):
            pygame.draw.rect(screen,COLORS[7],[(gap+dim)*column+gap,(gap+dim)*row+gap,dim,dim])
    for row in range(len(grid2)):
        for column in range(len(grid2[row])):
            pygame.draw.rect(screen,COLORS[7],[(gap+dim)*(column+13)+gap,(gap+dim)*row+gap,dim,dim])
            
def draw_put_ships_board(width, height):
    draw_board()
    pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen,COLORS[4],[pos[0] - dim/2,pos[1] - dim/2,width*(dim+gap),height*(dim+gap)])
    pygame.display.update()
    
def place_ship():
    ships = [2, 3, 3, 4, 5]
    direction = 0
    while ships != []:
        ship_size = [ships[-1], 1]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                direction = 1 - direction
            draw_put_ships_board(ship_size[direction], ship_size[1-direction])
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    
if __name__ == "__main__":
    #game running loop
    running = True
    while running:
        draw_board()
        #pygame.display.update()
        place_ship()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            

        