#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:12:41 2019

@author: huaizhong
"""

import pygame

class Field:
    def __init__(self, *content):
        if content == ():
            self.content = None
        else:
            if isinstance(content[0], ShipPart):
                self.content = content[0]
            else:
                raise TypeError
        self.is_open = False
    def open(self):
        self.is_open = True

class ShipPart:
    def __init__(self, ship):
        self.ship = ship

    def is_part_of_sunk_ship(self):
        return self.ship.is_sunk()

class Ship:
    def __init__(self, size, sea, start, direction):
        self.size = size
        self.sea = sea
        if direction:# if direction = 1
            self.location = [[start[0] + x, start[1]] for x in range(size)]
        else:#if direction = 0
            self.location = [[start[0], start[1] + x] for x in range(size)]
        for coords in self.location:
            if not sea.is_valid_coord(*coords):
                raise IndexError
            if isinstance(sea[coords].content, ShipPart):
                raise PlacementError
        for coords in self.location:
            sea[coords] = Field(ShipPart(self))
    def is_sunk(self):
        return all([self.sea[coords].is_open for coords in self.location])

class Sea:#gameboard
    def __init__(self, size=10):
        self.size = size
        self.board = [[Field() for i in range(size)] for i in range(size)]
    def __getitem__(self, index):
        if index[0] < 0 or index[0] >= self.size:
            raise IndexError
        if index[1] < 0 or index[1] >= self.size:
            raise IndexError
        return self.board[index[0]][index[1]]
    def __setitem__(self, index, value):
        if index[0] < 0 or index[0] >= self.size:
            raise IndexError
        if index[1] < 0 or index[1] >= self.size:
            raise IndexError
        self.board[index[0]][index[1]] = value
    def is_valid_coord(self, row, column):
        return 0 <= row < self.size and 0 <= column < self.size
    def represent(self):
        rep = ""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].is_open:
                    if isinstance(self.board[i][j].content, ShipPart):
                        rep += "Y "
                    else:
                        rep += "N "
                else:
                    rep += "X "
            rep += "\n"
        return rep

class Player:
    def __init__(self, size, ships_count):
        self.sea = Sea(size)#sea = class variable; Sea = class object
        self.ships = []
        self.ready = False
        self.ships_count = ships_count
    def put_ship(self, size, coords, direction):
        ship = Ship(size, self.sea, coords, direction)
        self.ships.append(ship)
        if len(self.ships) == self.ships_count:
            self.ready = True
    def check_ships(self):
        for ship in self.ships:
            if not ship.is_sunk():
                return False
        return True

class PlacementError(Exception):
    pass

def draw_board():
    screen.fill(COLORS[6])#single_player.screen = pygame.display.set_mode(dimension)
    for row in range(len(grid1)):
        for column in range(len(grid1[row])):
            pygame.draw.rect(screen,COLORS[grid1[row][column]],[(gap+dim)*column+gap,(gap+dim)*row+gap,dim,dim])
    for row in range(len(grid2)):
        for column in range(len(grid2[row])):
            pygame.draw.rect(screen,COLORS[grid2[row][column]],[(gap+dim)*(column+13)+gap,(gap+dim)*row+gap,dim,dim])
            
def draw_put_ships_board(width, height):
    draw_board()
    pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen,COLORS[5],[pos[0] - dim/2,pos[1] - dim/2,width*(dim+gap),height*(dim+gap)])
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if put_one_ship(player1, position, ships[-1], direction, grid1):
                    ships.pop()
                    
def put_one_ship(new_player, position, ship, direction, grid1):
    column = position[0] // (dim + gap)# // 相除取整数
    row = position[1] // (dim + gap)
    if column < 10 and row < 10:
        try:
            new_player.put_ship(ship, [row, column], direction)
            for coords in new_player.ships[-1].location:
                grid1[coords[0]][coords[1]] = 5
            return True
        except IndexError:
            print("You are out of the sea , please stay inside")
            return False
        except PlacementError:
            print("This place is already filled")
            return False
    else:
        try:
            new_player.put_ship(ship, [row, column], direction)
            for coords in new_player.ships[-1].location:
                grid1[coords[0]][coords[1]] = 5
            return True
        except IndexError:
            print("You are out of the sea, please stay inside")

    
if __name__ == "__main__":
    #Set up the colors    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (100, 100, 100)
    ORANGE = (255, 165, 0)
    DARKBLUE = (0, 0, 128)

    COLORS = {0: WHITE,1: RED,2: GREEN,3: ORANGE,4: DARKBLUE,5: GREY,6: BLACK,7: BLUE}
    #set up the information for player1 and computer
    player1 = Player(10, 5)#size = 10, shipscount = 5, class object
    sea1 = player1.sea#set up the sea (home) for player1, class object
    
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

    #Set up the game board
    grid1 = [[0 for i in range(10)] for i in range(10)]
    grid2 = [[0 for i in range(10)] for i in range(10)]
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
            

        