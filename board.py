import tile
import Units.unit as unit
import random
import numpy
import pygame


class Map:
    #Positioning Data
    #create grid
    column_count = 13
    row_count = 10
    #tiles = []
    #position grid
    mapX = 64
    mapY = 0

    #Creates and stores an array of tiles that make up the playspace
    def __init__(self):
        """self.tiles = []
        for i in range(Map.column_count):
            self.tiles.append([])
            for j in range(Map.row_count):
                x = i * 64 + Map.mapX
                y = j * 64 + Map.mapY
                #temp: creates just a random tile to come up with a temporary map
                number = random.random()
                if number < .2:
                    self.tiles[i].append(tile.Forest(x, y))
                elif number > .8:
                    self.tiles[i].append(tile.Water(x, y))
                else:
                    self.tiles[i].append(tile.Plain(x, y)) """
        self.tiles = numpy.empty([0,Map.column_count])
        temp = numpy.empty([0,Map.column_count])
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                x = i * 64 + Map.mapX
                y = j * 64 + Map.mapY
                number = random.random()
                if number < .2:
                    temp = numpy.append(temp, tile.Forest(x, y))
                elif number > .8:
                    temp = numpy.append(temp, tile.Water(x, y))
                else:
                    temp = numpy.append(temp, tile.Plain(x, y))
            self.tiles = numpy.vstack((self.tiles, temp)) 
            temp = numpy.empty([0,Map.column_count]) 
        #for ease, assign coordinate of each tile separately
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                self.tiles[j,i].assign_coordinate(j,i)
    def render_map(self,screen):
        for j in range(Map.column_count):
            for i in range(Map.row_count):
                self.tiles[i, j].show_tile(screen)

class Grid:
    #Creates a second grid of the same size as the map
    # to store units. 
    #Use size values from Map so that they always match
    column_count = Map.column_count
    row_count = Map.row_count


    #Creates and stores an array of empty space and units that are in play
    def __init__(self):
        """self.units = []
        for i in range(Grid.column_count):
            self.units.append([])
            for j in range(Grid.row_count):
                x = i * 64 + Map.mapX
                y = j * 64 + Map.mapY
                #temp: randomly assign units

                self.units[i].append(Units.unit.Group())"""
        self.units = numpy.empty([0, Map.column_count])
        temp = numpy.empty([0, Map.column_count])
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                x = i * 64 + Map.mapX
                y = j * 64 + Map.mapY
                number = random.random()
                temp = numpy.append(temp, unit.Group(x, y))
            self.units = numpy.vstack((self.units, temp)) 
            temp = numpy.empty([0,Map.column_count]) 
    
    def render_units(self, screen):
        for j in range(Map.column_count):
            for i in range(Map.row_count):
                self.units[i, j].show_group(screen)
class Valid_Moves:
    def __init__(self):
        self.choices = numpy.zeros((Map.row_count, Map.column_count), dtype = bool)
class Valid_Attacks:
    def __init__(self):
        self.choices = numpy.zeros((Map.row_count, Map.column_count), dtype = bool)

class Pool:
    #Creates the Unit Pool for each player
    #Currently creates a set pool for each player
    '''def __init__(self, player):
        self.player = player
        self.groups = []
        self.populate_pool()
        self.x = 0 #have a separate self.x as is needed for other class
    def populate_pool(self):
        y = 0
        if self.player == 1:
            self.x = 0
            x = self.x
        else:
            self.x = 64 * (Map.column_count + 1)
            x = self.x
        for j in range (0, 3):
            unit_group = unit.Group(x,y)
            for i in range(0, 5):
                unit_group.add_unit(unit.Axe(self.player))
            self.groups.append(unit_group)
            y = y + 64
        for j in range (0, 3):
            unit_group = unit.Group(x,y)
            for i in range(0, 5):
                unit_group.add_unit(unit.Sword(self.player))
            self.groups.append(unit_group)
            y = y + 64
        for j in range (0, 3):
            unit_group = unit.Group(x,y)
            for i in range(0, 5):
                unit_group.add_unit(unit.Spear(self.player))
            self.groups.append(unit_group)
            y = y + 64

    def render_units(self, screen):
        for i in self.groups:
            i.show_group(screen)'''
    def __init__(self, player):
        self.player = player
        self.options = []
        if self.player == 1:
            self.x = 0
        else:
            self.x = (Map.column_count + 1) * 64
        self.axe_count = 15
        self.spear_count = 15
        self.sword_count = 15
        self.populate_pool()
        
    def populate_pool(self):
        '''y = 0
        if self.player == 1:
            self.x = 0
            x = self.x
            self.options.append(unit.Axe())
            self.options.append(unit.Sword())
            self.options.append(unit.Spear())
        else:
            self.x = 64 * (Map.column_count + 1)
            x = self.x
            self.options.append(unit.Axe(2))
            self.options.append(unit.Sword(2))
            self.options.append(unit.Spear(2))'''
        self.axe_option = Unit_Selection(self.player, "axe", self.axe_count, self.x, 0)
        self.sword_option = Unit_Selection(self.player, "sword", self.sword_count, self.x, 64)
        self.spear_option = Unit_Selection(self.player, "spear", self.spear_count, self.x, 128)
        self.options.append(self.axe_option)
        self.options.append(self.sword_option)
        self.options.append(self.spear_option)
        
    def render_pool(self, screen):
        '''tileY = 0
        unitY = 16
        unitX = self.x + 16
        for i in self.options:
            screen.blit(self.unitImg, (self.x + self.unitX, tileY + self.unitY))'''
        for i in self.options:
            i.render_selection(screen)
    def clear_selection(self):
        for cell in self.options:
            cell.is_selected = False

class Unit_Selection:
    def __init__(self, player, unit_type, count, x, y):
        self.player = player
        self.unit_type = unit_type
        self.x = x
        self.y = y
        self.is_selected = False
        self.count = count
        
        #set scale of unit sprite for selection
        scale = 2

        #Set outer border image
        self.outlineImg = pygame.image.load('Images\\Tiles\\outline_pool2.png')

        #set highlight image
        self.selectionImg = pygame.image.load('Images\\Tiles\\movement_selection.png')
        #set image for unit type of selection
        if unit_type == 'axe':
            if player == 1:
                self.unitImg = pygame.image.load('Images\\Soldiers\\BlueAxeIdle.png')
            elif player == 2:
                self.unitImg = pygame.image.load('Images\\Soldiers\\RedAxeIdle.png')

        if unit_type == 'sword':
            if player == 1:
                self.unitImg = pygame.image.load('Images\\Soldiers\\BlueSwordIdle.png')
            elif player == 2:
                self.unitImg = pygame.image.load('Images\\Soldiers\\RedSwordIdle.png')
        
        if unit_type == 'spear':
            if player == 1:
                self.unitImg = pygame.image.load('Images\\Soldiers\\BlueSpearIdle.png')
            elif player == 2:
                self.unitImg = pygame.image.load('Images\\Soldiers\\RedSpearIdle.png')
        self.unitImg = pygame.transform.rotozoom(self.unitImg, 0, scale)

        #Set the text for remaining units in selection
        font = pygame.font.Font('PressStart2P-Regular.ttf', 12)
        yellow = (255,255,0)
        self.text = font.render(str(self.count), True, yellow)

    def render_selection(self, screen):
        #Set offset for unit type and text
        unit_offsetX = -12
        unit_offsetY = -6
        text_offsetX = 38
        text_offsetY = 48
        #render selection outline first
        screen.blit(self.outlineImg, (self.x, self.y))

        #render the highlight if selected
        if self.is_selected:
            screen.blit(self.selectionImg, (self.x, self.y))

        #render unit type
        screen.blit(self.unitImg, (self.x + unit_offsetX, self.y + unit_offsetY))

        #render count
        screen.blit(self.text, (self.x + text_offsetX, self.y + text_offsetY))
    
    def check_collision(self, pos):
        posX, posY = pos
        if posX < self.x + 64  and posX > self.x:
            if posY < self.y + 64 and posY > self.y:
                return True
        return False
    
    def set_selected(self):
        self.is_selected = True
        
                

        

       
        
        

        

