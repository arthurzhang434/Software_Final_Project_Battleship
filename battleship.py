#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:12:41 2019

@author: huaizhong
"""

import pygame
import random
from itertools import permutations
from copy import deepcopy

class Field:
    def __init__(self, *content):
        if content == ():
            #print(content)
            self.content = None
        else:
            #print(content[0])
            if isinstance(content[0], Part_of_ship):
                self.content = content[0]
            else:
                raise TypeError
        self.is_open = False
    def open(self):
        self.is_open = True

class Part_of_ship:
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
            if sea.is_valid_coord(*coords) is False:
                raise IndexError
            if isinstance(sea[coords].content, Part_of_ship) is True:
                raise PlacementError
        for coords in self.location:
            sea[coords] = Field(Part_of_ship(self))
    def is_sunk(self):
        return all([self.sea[coords].is_open for coords in self.location])

class Sea:#玩家和电脑各自的老家
    def __init__(self, size=10):
        self.size = size
        self.grid = [[Field() for i in range(size)] for i in range(size)]
        #[[Field() for i in range(10)] for i in range(10)], content = None
        #生成空的10*10的list o list

    def __getitem__(self, index):#make 'Sea' object is subscriptable
        if index[0] < 0 or index[0] >= self.size:
            raise IndexError
        if index[1] < 0 or index[1] >= self.size:
            raise IndexError
        return self.grid[index[0]][index[1]]
    def __setitem__(self, index, value):#make 'Sea' object is subscriptable
        if index[0] < 0 or index[0] >= self.size:
            raise IndexError
        if index[1] < 0 or index[1] >= self.size:
            raise IndexError
        self.grid[index[0]][index[1]] = value  
    def represent(self):
        rep = ""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j].is_open:
                    if isinstance(self.grid[i][j].content, Part_of_ship):
                        rep += "Y "
                    else:
                        rep += "N "
                else:
                    rep += "X "
            rep += "\n"
        return rep

    def is_valid_coord(self, row, column):
        return 0 <= row < self.size and 0 <= column < self.size

class Player:#Player(10,5)
    def __init__(self, size, ships_count):
        self.sea = Sea(size)#sea = class variable; Sea = class object, Sea(10)
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
    #print('board is drawing')
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
    
def player_put_one_ship(new_player, position, shipsize, direction, grid1):
    #print(shipsize)
    column = position[0] // (dim + gap)# // 相除取整数
    row = position[1] // (dim + gap)
    if column < 10 and row < 10:
        try:
            new_player.put_ship(shipsize, [row, column], direction)
            for coords in new_player.ships[-1].location:
                grid1[coords[0]][coords[1]] = 5
            return True
        except IndexError:
            print("You are out of your own sea, please stay inside")
            return False
        except PlacementError:
            print("This place is already filled")
            return False
    else:
        try:
            new_player.put_ship(shipsize, [row, column], direction)
            for coords in new_player.ships[-1].location:
                grid1[coords[0]][coords[1]] = 5
            return True
        except IndexError:
            print("You are out of your own sea, please stay inside")
            return False
    
def player_place_ship(player):
    print('player is placing')
    ship_sizes = [2, 3, 3, 4, 5]
    direction = 0
    while ship_sizes != []:
        ship_size = [ship_sizes[-1], 1]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                direction = 1 - direction
            draw_put_ships_board(ship_size[direction], ship_size[1-direction])
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if player_put_one_ship(player1, position, ship_sizes[-1], direction, grid1) is True:
                    ship_sizes.pop()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def find_valid_place(position, ship_size, direction, sea2):#电脑检查是否可以放船

    if direction == 0:
        for i in range(ship_size):
            if position[1] + i > 9:
                return False
            else:
                if sea2[[position[0], position[1] + i]].content:# if = 1, already placed
                    return False
        return True
    else:#if direction = 1
        for i in range(ship_size):
            if position[0] + i > 9:
                return False
            else:
                if sea2[[position[0] + i, position[1]]].content:# if = 1, already placed
                    return False
        return True

def computer_place_ship(computer):#电脑放船， 一次性放所有船
    print('computer is placing')
    ship_sizes = [2,3,3,4,5]

    for ship_size in ship_sizes:
        possible_positions = []
        for row in range(10):
            for column in range(10):
                if find_valid_place([row, column], ship_size, 0, computer.sea) is True:
                    possible_positions.append((ship_size, [row, column], 0))
                if find_valid_place([row, column], ship_size, 1, computer.sea) is True:
                    possible_positions.append((ship_size, [row, column], 1))
        position = random.choice(possible_positions)
        print(position)
        computer.put_ship(position[0], position[1], position[2])
    

def player_make_move(position, sea2, grid2, grid1, player_turn):#玩家炸船
    #player_turn = True
    column = position[0] // (dim + gap) - 13
    row = position[1] // (dim + gap)
    if 0 <= column < 10 and 0 <= row < 10:
        sea2[[row, column]].open()
        if isinstance(sea2[row, column].content, Part_of_ship):
            grid2[row][column] = 1
        else:
            grid2[row][column] = 2
        #draw_board(grid1, grid2)
        draw_board()
        pygame.display.update()
        if grid2[row][column] == 1:
            print('You hitted!')
            player_turn = False
        if grid2[row][column] == 2:
            print('You missed!')
            player_turn = False
        #if sea2[[row, column]].content.is_part_of_sunk_ship():
            #print("You burned the ship !")
        #else:
            #print("you hitted!")
        #player_turn = False

    return player_turn                    

def generate_positions(x,y):
    size = range(x,y)
    position = permutations(size, 2)
    positions = []
    for p in position:
        pos = list(p)
        positions.append(pos)
    for i in range(10):
        positions.append([i,i])
    return positions

def intersection_list_of_list(list1, list2):
    list3 = [sublist for sublist in list1 if sublist in list2]
    return list3

def subtract_hitted_position(positions, ship_hitted):
    print(positions)
    print(ship_hitted[-1])
    new_positions = []
    for i in range(len(positions)):
        #print(positions[i])
        if positions[i] != ship_hitted[-1]:
            new_positions.append(positions[i])
    return new_positions
            

def find_valid_neighbor(positions, ship_hitted):
    valid_neighbor = []
    if len(ship_hitted) == 0:
        valid_neighbor = []
    if len(ship_hitted) != 0:
        neighbor = [[ship_hitted[-1][0] - 1, ship_hitted[-1][1]],
         [ship_hitted[-1][0] + 1, ship_hitted[-1][1]],
        [ship_hitted[-1][0], ship_hitted[-1][1] - 1],
        [ship_hitted[-1][0], ship_hitted[-1][1] + 1]]
        valid_neighbor = intersection_list_of_list(positions, neighbor)
        print(valid_neighbor)
    return valid_neighbor
    


def computer_turn(player1, sea1, grid1, grid2, positions, ship_hitted):
    ship_missed = []
    valid_neighbor = find_valid_neighbor(positions, ship_hitted)
    
    if len(valid_neighbor) == 0:
        position = random.choice(positions)
        row = position[0]
        column = position[1]
        sea1[[row, column]].open()
        if isinstance(sea1[row, column].content, Part_of_ship):
            grid1[row][column] = 1
        else:
            grid1[row][column] = 2
        draw_board()
        pygame.display.update()
        if grid1[row][column] == 1:
            print('Computer hitted!')
            ship_hitted.append([row, column])
            print("1")
            print(ship_hitted)
            positions = deepcopy(subtract_hitted_position(positions, ship_hitted))
        if grid1[row][column] == 2:
            print('Computer missed!')
            ship_missed.append([row, column])
            positions = deepcopy(subtract_hitted_position(positions, ship_missed))
        return [ship_hitted, positions]
            
    if len(valid_neighbor) != 0:
        position = random.choice(valid_neighbor)
        row = position[0]
        column = position[1]
        sea1[[row, column]].open()
        if isinstance(sea1[row, column].content, Part_of_ship):
            grid1[row][column] = 1
        else:
            grid1[row][column] = 2
        draw_board()
        pygame.display.update()
        if grid1[row][column] == 1:
            print('Computer hitted!')
            #print([row,column])
            ship_hitted.append([row, column])
            print('2')
            print(ship_hitted)
            positions = deepcopy(subtract_hitted_position(positions, ship_hitted))
        if grid1[row][column] == 2:
            print('Computer missed!')
            ship_missed.append([row, column])
            positions = deepcopy(subtract_hitted_position(positions, ship_missed))
        return [ship_hitted, positions]
        
    
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
    computer = Player(10,5)
    sea2 = computer.sea
    
    positions = generate_positions(0,9)
    #print(positions)
    ship_hitted = []
    
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
    
    player_place_ship(player1)
    draw_board()
    #print(grid1)
    pygame.display.update()
    computer_place_ship(computer)
    pygame.display.update()

    #game running loop
    running = True
    player_turn = True
    while running:
        while player_turn is True:
            #print('player turn')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    player_turn = player_make_move(position, sea2, grid2, grid1, player_turn)
                    #draw_board()
        while player_turn is False:
            #print('computer turn')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #running = False
                    pygame.quit()
                    exit()
                [ship_hitted, positions] = deepcopy(computer_turn(player1, sea1, grid1, grid2, positions, ship_hitted))
                player_turn = True
                #player_turn = computer_turn(player1, sea1, grid1, grid2, positions)
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            

        