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
screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Arthur's Battleship")
Icon = pygame.image.load("battleship.png")
pygame.display.set_icon(Icon)

#Set up the colors
WHITE = (255, 255, 255)#Nothing
BLACK = (0, 0, 0)
RED = (255, 0, 0)#Hit
GREEN = (0, 255, 0)#Miss
BLUE = (0, 0, 255)#Ship

#
grid = []
for row in range(10):
    grid.append([])
    for column in range(10):
        grid[row].append(0)
        
upgrid = []
for row in range(10):
    upgrid.append([])
    for column in range(10):
        upgrid[row].append(10)
 
#game running loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
            

        