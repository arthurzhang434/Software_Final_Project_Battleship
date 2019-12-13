#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:12:41 2019

@author: huaizhong

This code contains a game of battleship played by Graphical User Interface (GUI),
The part of user defined classes and objects (Object Oriented Programming) is 
cited from https://github.com/victoria92/battleship, and slight changes have been
made to adapt this code.


"""

import pygame
import random
from itertools import permutations
from copy import deepcopy

class Field:
    '''
    A Field object contains the information of each player's grids.
    '''
    def __init__(self, *content):
        if content == ():
            self.content = None
        else:
            if isinstance(content[0], Part_of_ship) is True:
                self.content = content[0]
            else:
                raise TypeError
        self.is_open = False
    def open(self):
        self.is_open = True

class Part_of_ship:
    '''
    A Part of ship object, latter being called to check whether a position 
    selected is a part of ship.
    
    **Parameters**
    
        None
        
    **Returns**

        None     
    '''
    def __init__(self, ship):
        self.ship = ship


class Ship:
    '''
    A Ship object has the property to check the valid grid when placing the
    ships and check if the ship is sunk.
    
    **Parameters**
    
        None
        
    **Returns**

        None     
    '''    
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

class Sea:
    '''
    A Field object contains the information of each player's grids on screen.
    '''
    def __init__(self, size=10):
        self.size = size
        self.grid = [[Field() for i in range(size)] for i in range(size)]
        #[[Field() for i in range(10)] for i in range(10)], content = None
        
    
    def __getitem__(self, index):#make 'Sea' object is subscriptable
        if index[0] < 0 or index[0] >= self.size:
            raise IndexError
        if index[1] < 0 or index[1] >= self.size:
            raise IndexError
        return self.grid[index[0]][index[1]]
    
    def __setitem__(self, index, value):#make 'Sea' object support item assignment
        if index[0] < 0 or index[0] >= self.size:
            raise IndexError
        if index[1] < 0 or index[1] >= self.size:
            raise IndexError
        self.grid[index[0]][index[1]] = value
    
    def is_valid_coord(self, row, column):
        return 0 <= row < self.size and 0 <= column < self.size

class Player:
    '''
    A Player object contains the information of each player's ships.
    Has the property to put the ship in a specific coordinate
    and check if the all ship is sunk or not.
    '''
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
    '''
    The function used to draw the main game screen.
    
    **Parameters**
    
        None
        
    **Returns**

        None     
    '''    
    screen.fill(COLORS[4])
    comment = pygame.image.load("comment.png")
    screen.blit(comment, (0, 324))
    #print(grid1)
    for row in range(10):
        for column in range(10):
            pygame.draw.rect(screen,COLORS[grid1[row][column]],[(gap+dim)*column+gap,(gap+dim)*row+gap,dim,dim])
    for row in range(10):
        for column in range(10):
            pygame.draw.rect(screen,COLORS[grid2[row][column]],[(gap+dim)*(column+13)+gap,(gap+dim)*row+gap,dim,dim])

    font = pygame.font.Font('freesansbold.ttf',16)
    player1_sea = font.render('Player1\'s Sea', True, (255,255,255))
    computer_sea = font.render('Computer\'s Sea', True, (255,255,255))
    screen.blit(player1_sea, (80,295))
    screen.blit(computer_sea, (440,295))
            
def draw_unput_ships(length, width):
    '''
    The function used to draw the ships on screen which dragged by mouse but 
    haven't placed down yet.
    
    **Parameters**
    
        length: the length of a ship
        width: the width of a ship
        
    **Returns**

        None     
    '''        
    draw_board()
    position = pygame.mouse.get_pos()
    pygame.draw.rect(screen,COLORS[3],[position[0] - dim/2,position[1] - dim/2,length*(dim+gap),width*(dim+gap)])
    pygame.display.update()
    
def player_put_one_ship(new_player, position, shipsize, direction, grid1):
    '''
    The function used to change the numbers (representing the colors) 
    in grid1 (10*10 list of lists). Also used to check wether the player
    placed the ship on a valid place.
    
    **Parameters**
    
        new_player: *player object*
        position: *list, int*, the position get from mouse.
        shipsize: *int*, the length of a ship
        direction: *int*, 0 = horizontal, 1 = vertical
        grid1: *list, list*
        
    **Returns**

        True of False 
    '''    
    #print(shipsize)
    column = position[0] // (dim + gap)# // 
    row = position[1] // (dim + gap)
    if column < 10 and row < 10:
        try:
            new_player.put_ship(shipsize, [row, column], direction)
            for coords in new_player.ships[-1].location:
                grid1[coords[0]][coords[1]] = 3
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
    '''
    The function used to draw the ships on screen which placed by clicking
    the mouse buttondown. The direction of a ship (horizontal or vertical)
    before placed could be changed by clicking any key on the key board.
    
    **Parameters**
    
        player: *Class object*, contains the information of player's ship.
        
    **Returns**

        None  
    '''    

    print('player is placing')
    ship_sizes = [2, 3, 3, 4, 5]
    direction = 0
    while ship_sizes != []:
        ship_size = [ship_sizes[-1], 1]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                direction = 1 - direction
            draw_unput_ships(ship_size[direction], ship_size[1-direction])
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if player_put_one_ship(player1, position, ship_sizes[-1], direction, grid1) is True:
                    ship_sizes.pop()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def find_valid_place(position, ship_size, direction, sea2):
    '''
    The function for computer check the valid grid to place the ships.
    
    **Parameters**
    
        position: *list, int*, row and column both in range(10)
        shipsize: *int*, the length of a ship
        direction: *int*, 0 = horizontal, 1 = vertical
        sea2: *Class object*, the board for computer.
        
    **Returns**

        True of False 
    '''    
    if direction == 0:
        for i in range(ship_size):
            if position[1] + i > 9:
                return False
            else:
                if sea2[[position[0], position[1] + i]].content:# if is True, already placed
                    return False
        return True
    else:#if direction = 1
        for i in range(ship_size):
            if position[0] + i > 9:
                return False
            else:
                if sea2[[position[0] + i, position[1]]].content:# if is True, already placed
                    return False
        return True

def computer_place_ship(computer):
    '''
    The function for computer to place the ships on the valid grids. 
    If there is currently no valid grid, computer will randomly choose a grid.
    
    **Parameters**
    
        computer: *Class object*, contains the information of computer's ship.
        
    **Returns**

        None
    '''  
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
    

def player_make_move(position, sea2, grid2):
    '''
    The function for player to choose a grid on computer's sea to blow up
    by clicking the mouse.
    
    **Parameters**
    
        position: *list, int*, the position get from mouse clicking.
        sea2: *class, obejct*, the board for computer.
        grid2: *list, list*, the grid for computer.
        
    **Returns**

        None
    '''    
    #player_turn = True
    column = position[0] // (dim + gap) - 13
    row = position[1] // (dim + gap)
    if 0 <= column < 10 and 0 <= row < 10:
        sea2[[row, column]].open()
        if isinstance(sea2[row, column].content, Part_of_ship):
            grid2[row][column] = 1
        else:
            grid2[row][column] = 2
        draw_board()
        pygame.display.update()
        if grid2[row][column] == 1:
            print('You hitted!')
        if grid2[row][column] == 2:
            print('You missed!')                 

def generate_positions(x,y):
    '''
    The function to generation all possible coordinates on player's sea
    for computer.
    
    **Parameters**
    
        x:*int*
        y:*int*
        
    **Returns**

        positions:*list, list*, list of lists of int contains all 
        possible coordinates.
    '''    
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
    '''
    The function to generation the intersection for two list.
    
    **Parameters**
    
        list1:*list*
        list2:*list*
        
    **Returns**

        list3:*list*
    '''    
    list3 = [sublist for sublist in list1 if sublist in list2]
    return list3

def subtract_hitted_position(positions, ship_hitted):
    '''
    The function to remove the position once chosen by computer.
    
    **Parameters**
    
        positions:*list*
        ship_hitted:*list*
        
    **Returns**

        new_positions:*list*
    '''    
    #print(positions)
    #print(ship_hitted[-1])
    new_positions = []
    for i in range(len(positions)):
        #print(positions[i])
        if positions[i] != ship_hitted[-1]:
            new_positions.append(positions[i])
    return new_positions
            

def find_valid_neighbor(positions, ship_hitted):
    '''
    The function for computer to find all possible valid neighbor
    based on the last hitted position.
    
    **Parameters**
    
        positions:*list*
        ship_hitted:*list*
        
    **Returns**

        valid_neighbor:*list*
    '''  
    valid_neighbor = []
    if len(ship_hitted) == 0:
        valid_neighbor = []
        
    if len(ship_hitted) == 1:
        neighbor = [[ship_hitted[-1][0] - 1, ship_hitted[-1][1]],
         [ship_hitted[-1][0] + 1, ship_hitted[-1][1]],
        [ship_hitted[-1][0], ship_hitted[-1][1] - 1],
        [ship_hitted[-1][0], ship_hitted[-1][1] + 1]]
        valid_neighbor = intersection_list_of_list(positions, neighbor)

    if len(ship_hitted) > 1:
        y_movement = ship_hitted[-1][0] - ship_hitted[-2][0]
        x_movement = ship_hitted[-1][1] - ship_hitted[-2][1]
        neighbor = [[ship_hitted[-1][0] + y_movement, ship_hitted[-1][1] + x_movement]]
        valid_neighbor = intersection_list_of_list(positions, neighbor)
        if len(valid_neighbor) == 0:
            ship_hitted.reverse()
            neighbor = [[ship_hitted[-1][0] - y_movement, ship_hitted[-1][1] - x_movement]]
            valid_neighbor = intersection_list_of_list(positions, neighbor)

    return valid_neighbor
    


def computer_turn(sea1, grid1, positions, ship_hitted):
    '''
    The function for computer to choose a grid on computer's sea to blow up.
    
    **Parameters**
    
        sea1:*class, obejct*, the board for player1.
        grid1:*list, list*, the grid for player1.
        positions:*list, list*
        ship_hitted:*list, list*
        
    **Returns**

        ship_hitted:*list, list*
        positions:*list, list*
    '''  
    ship_missed = []
    valid_neighbor = find_valid_neighbor(positions, ship_hitted)
    
    if len(valid_neighbor) == 0 and len(ship_hitted) == 0:
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
            positions = deepcopy(subtract_hitted_position(positions, ship_hitted))
        if grid1[row][column] == 2:
            print('Computer missed!')
            ship_missed.append([row, column])
            positions = deepcopy(subtract_hitted_position(positions, ship_missed))
        return [ship_hitted, positions]
            
    if len(valid_neighbor) != 0 and len(ship_hitted) != 0:
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
            ship_hitted.append([row, column])
            positions = deepcopy(subtract_hitted_position(positions, ship_hitted))
        if grid1[row][column] == 2:
            print('Computer missed!')
            ship_missed.append([row, column])
            positions = deepcopy(subtract_hitted_position(positions, ship_missed))
        return [ship_hitted, positions]
    
    if len(valid_neighbor) == 0 and len(ship_hitted) != 0:
        ship_hitted = []
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
            positions = deepcopy(subtract_hitted_position(positions, ship_hitted))
        if grid1[row][column] == 2:
            print('Computer missed!')
            ship_missed.append([row, column])
            positions = deepcopy(subtract_hitted_position(positions, ship_missed))
        return [ship_hitted, positions] 
    
    
    
def game_result(winner):
    '''
    The function to show the game result when game is finish.
    
    **Parameters**
    
        winner:*class object*, 
        player1 or computer who first blow up all the ships.
        
    **Returns**

        None
    '''  
    
    if winner == player1:
        font = pygame.font.Font('freesansbold.ttf',16)
        result = font.render('Congratulations! You beat my artificial idiot!', True, (255,255,255))
        screen.blit(result, (285,325))
        pygame.display.update()
        
    if winner == computer:
        font = pygame.font.Font('freesansbold.ttf',16)
        result = font.render('Sorry, hope you will win next time.', True, (255,255,255))
        screen.blit(result, (350,350))
        pygame.display.update()        

if __name__ == "__main__":
    
    #Set up the colors used in this game   
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)   
    GREY = (100, 100, 100)
    BLACK = (0, 0, 0)    
    COLORS = {0: WHITE,1: RED,2: GREEN,3: GREY,4: BLACK}
    
    #set up the informations for player1 and computer
    player1 = Player(10, 5)#size = 10, shipscount = 5, class object
    sea1 = player1.sea#set up the sea for player1, class object
    computer = Player(10,5)
    sea2 = computer.sea
    
    #generate the list of positions and ship_hitted for computer to use.
    positions = generate_positions(0,10)
    ship_hitted = []
    
    #initialize the pygame
    pygame.init()

    #Set up the game screen size and other parameters
    screen = pygame.display.set_mode((648, 648))
    dim = 25
    gap = 3

    #Set up the title and Icon for this game
    pygame.display.set_caption("Arthur's Battleship")
    Icon = pygame.image.load("battleship.png")
    pygame.display.set_icon(Icon)

    #Set up the game board
    grid1 = [[0 for i in range(10)] for i in range(10)]
    grid2 = [[0 for i in range(10)] for i in range(10)]
    
    player_place_ship(player1)
    #print(grid1)
    draw_board()
    pygame.display.update()
    computer_place_ship(computer)
    pygame.display.update()

    #game running infinite loop
    running = True#variable for game running
    player_turn = True#variable for switching the turn between player and computer
    while running:
        #print(grid1)
        while player_turn is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    player_make_move(position, sea2, grid2)
                    if computer.check_ships():
                        game_result(player1)
                        break
                    player_turn = False
        while player_turn is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                [ship_hitted, positions] = deepcopy(computer_turn(sea1, grid1, positions, ship_hitted))
                if player1.check_ships():
                    game_result(computer)
                player_turn = True
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            

        