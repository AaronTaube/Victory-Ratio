import tile
import Units.unit as unit
import random
import numpy
import pygame


class Map:
    #Positioning Data
    #create grid
    column_count = 13
    row_count = 9
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
        self.tileImg = pygame.image.load('Images\\Tiles\\movement_selection.png')

    def player1_valid_placement(self, board, groups, unit_type):
        for j in range(Map.row_count):
            for i in range(2):
                #Set true for placeable tiles that aren't water tiles
                #TODO set false if tile is full or a different unit type
                if board[j,i].is_blocker == False:
                    self.choices[j,i] = True
                if len(groups[j,i].units) >= 9:
                    self.choices[j,i] = False
                if len(groups[j,i].units) > 0:
                    if groups[j,i].units[0].unit_type != unit_type:
                        self.choices[j,i] = False
    def player2_valid_placement(self, board, groups, unit_type):
        for j in range(Map.row_count):
            for i in range(Map.column_count - 2, Map.column_count):
                #Set true for placeable tiles that aren't water tiles
                #TODO set false if tile is full or a different unit type
                if board[j,i].is_blocker == False:
                    self.choices[j,i] = True
                if len(groups[j,i].units) >= 9:
                    self.choices[j,i] = False
                if len(groups[j,i].units) > 0:
                    if groups[j,i].units[0].unit_type != unit_type:
                        self.choices[j,i] = False
    def set_move_options(self, row, column, tiles, groups):
        #set straight movements
        for i in range(3):
            current_row = row + 1 + i
            if current_row <= Map.row_count - 1:
                if tiles[current_row, column].is_blocker:
                    break
                self.choices[current_row, column] = True
        for i in range(3):
            current_row = row - 1 - i
            if current_row >= 0:
                if tiles[current_row, column].is_blocker:
                    break
                self.choices[current_row, column] = True
        for i in range(3):
            current_column = column + 1 + i
            if current_column <= Map.column_count - 1:
                if tiles[row, current_column].is_blocker:
                    break
                self.choices[row, current_column] = True
        for i in range(3):
            current_column = column - 1 - i
            if current_column >= 0:
                if tiles[row, current_column].is_blocker:
                    break
                self.choices[row, current_column] = True
        #Set Other moves, be sure to cover all possible options, some redundancy necessary
        #   up to 2 row moves
        for i in range(2):
            current_row = row + 1 + i
            if current_row <= Map.row_count - 1 and column + 1 <= Map.column_count - 1:
                if tiles[current_row, column + 1].is_blocker:
                    break
                self.choices[current_row, column + 1] = True
        for i in range(2):
            current_row = row + 1 + i
            if current_row <= Map.row_count - 1 and column - 1 >= 0:
                if tiles[current_row, column - 1].is_blocker:
                    break
                self.choices[current_row, column - 1] = True
        for i in range(2):
            current_row = row - 1 - i
            if current_row >= 0 and column + 1 <= Map.column_count - 1:
                if tiles[current_row, column + 1].is_blocker:
                    break
                self.choices[current_row, column + 1] = True
        for i in range(2):
            current_row = row - 1 - i
            if current_row >= 0 and column - 1 >= 0:
                if tiles[current_row, column - 1].is_blocker:
                    break
                self.choices[current_row, column - 1] = True
        #   up to 2 Column moves
        for i in range(2):
            current_column = column + 1 + i
            if current_column <= Map.column_count - 1 and row + 1 <= Map.row_count - 1:
                if tiles[row + 1, current_column].is_blocker:
                    break
                self.choices[row + 1, current_column] = True
        for i in range(2):
            current_column = column - 1 - i
            if current_column >= 0 and row + 1 <= Map.row_count :
                if tiles[row + 1, current_column].is_blocker:
                    break
                self.choices[row + 1, current_column] = True
        for i in range(2):
            current_column = column + 1 + i
            if current_column <= Map.column_count - 1 and row - 1 >= 0:
                if tiles[row - 1, current_column].is_blocker:
                    break
                self.choices[row - 1, current_column] = True
        for i in range(2):
            current_column = column - 1 - i
            if current_column >= 0 and row - 1 >= 0:
                if tiles[row - 1, current_column].is_blocker:
                    break
                self.choices[row - 1, current_column] = True
        #clean out spaces where units already exist
        #   Technically not the most efficient way, but should only be called once per click,
        #    and easier to read and manage
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                if len(groups[j, i].units) > 0:
                    self.choices[j, i] = False
    def clear(self):
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                self.choices[j,i] = False
    def render_moves(self, screen):
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                if self.choices[j,i]:
                    screen.blit(self.tileImg, (64+ 64*i, 64*j))

class Valid_Attacks:
    def __init__(self):
        self.choices = numpy.zeros((Map.row_count, Map.column_count), dtype = bool)
        self.tileImg = pygame.image.load('Images\\Tiles\\attack_selection.png')
    def set_attack_options(self, origin):
        originX, originY = origin
        if originX + 1 <= Map.row_count - 1:
            self.choices[originX + 1, originY] = True
        if originX - 1 >= 0:
            self.choices[originX - 1, originY] = True
        if originY + 1 <= Map.column_count - 1:
            self.choices[originX, originY + 1] = True
        if originY - 1 >= 0:
            self.choices[originX, originY - 1] = True
    def render_attacks(self, screen):
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                if self.choices[j,i]:
                    screen.blit(self.tileImg, (64+ 64*i, 64*j))
    def clear(self):
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                self.choices[j,i] = False

class Pool:
    #Creates the Unit Pool for each player
    #Currently creates a set pool for each player
    
    def __init__(self, player):
        self.player = player
        self.options = []
        if self.player == 1:
            self.x = 0
        else:
            self.x = (Map.column_count + 1) * 64
        self.axe_count = 9
        self.spear_count = 0
        self.sword_count = 0
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
    
    def unit_selected(self):
        for cell in self.options:
            if cell.is_selected:
                return True
        return False
    def get_selected(self):
        for cell in self.options:
            if cell.is_selected:
                return cell
        return None
    def get_count(self):
        count = 0
        for cell in self.options:
            count = count + cell.count
        return count

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
        if unit_type == "axe":
            if player == 1:
                self.unitImg = pygame.image.load('Images\\Soldiers\\BlueAxeIdle.png')
            elif player == 2:
                self.unitImg = pygame.image.load('Images\\Soldiers\\RedAxeIdle.png')

        if unit_type == "sword":
            if player == 1:
                self.unitImg = pygame.image.load('Images\\Soldiers\\BlueSwordIdle.png')
            elif player == 2:
                self.unitImg = pygame.image.load('Images\\Soldiers\\RedSwordIdle.png')
        
        if unit_type == "spear":
            if player == 1:
                self.unitImg = pygame.image.load('Images\\Soldiers\\BlueSpearIdle.png')
            elif player == 2:
                self.unitImg = pygame.image.load('Images\\Soldiers\\RedSpearIdle.png')
        self.unitImg = pygame.transform.rotozoom(self.unitImg, 0, scale)

        #Set the text for remaining units in selection
        self.font = pygame.font.Font('PressStart2P-Regular.ttf', 12)
        self.yellow = (255,255,0)
        self.text = self.font.render(str(self.count), True, self.yellow)

    def reduce_count(self):
        self.count = self.count - 1
        self.text = self.font.render(str(self.count), True, self.yellow)

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
        
                

        

       
        
        

        

