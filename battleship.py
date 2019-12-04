#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:12:41 2019

@author: huaizhong
"""

import pygame
#initialize the pygame
pygame.init()

screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Arthur's Battleship")
Icon = pygame.image.load("battleship.png")
pygame.display.set_icon(Icon)
 
#game running loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        