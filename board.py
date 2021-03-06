'''
Name:       board.py
Purpose:    Class and subclasses for displaying the map and accounting for gameplay mechanics such as terrain generation, 
            and combat, animation
Author:     Aaron Taube
Created:    6/14/2020
TODO:       Fix the pathfinding for finding valid unit placement
            Reduce rate of water tiles for now
            Add smarter programming to make sure there is plenty of paths and spaces for units to cross map
Notes:
'''
import tile
import random
import numpy
import pygame


class Map:
    ''''Positioning data for tiles of the map'''
    #create grid
    column_count = 13
    row_count = 9
    #position grid
    mapX = 64
    mapY = 0

    
    def __init__(self):
        '''Creates and stores an array of tiles that make up the playspace'''
        self.tiles = numpy.empty([0,Map.column_count])
        self.movedImg = pygame.image.load('Images\\Tiles\\moved_mask.png')
        self.valid_moveImg = pygame.image.load('Images\\Tiles\\movement_selection.png')
        self.valid_attackImg = pygame.image.load('Images\\Tiles\\attack_selection.png')
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
        '''Go through the entire map matrix and call the tiles' show_tile function'''
        for j in range(Map.column_count):
            for i in range(Map.row_count):
                self.tiles[i, j].show_tile(screen)
    
    def render_units(self, screen):
        '''Go through the entire map matrix and call the tiles' show_group function'''
        for j in range(Map.column_count):
            for i in range(Map.row_count):
                self.tiles[i, j].show_group(screen)
    
    def render_gray(self, screen):
        '''Puts a gray mask over tile containing a unit that can't be moved'''
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                if self.tiles[j,i].units["moved"] == True:
                    screen.blit(self.movedImg, (64+ 64*i, 64*j))

    def clear_round(self):
        '''Clears all gray tiles from moved units'''
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                self.tiles[i, j].units["moved"] = False
    
    def clear_moves(self):
        '''Clear all tiles currently marked as valid moves'''
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                self.tiles[j,i].movement["range"] = False

    def render_moves(self, screen):
        '''Render mask for tiles that are valid moves'''
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                if self.tiles[j,i].movement["range"] == True:
                    screen.blit(self.valid_moveImg, (64+ 64*i, 64*j))

    def player1_valid_placement(self, unit_type):
        '''Set valid placement tiles for player 1'''
        for j in range(Map.row_count):
            for i in range(2):
                #Set true for placeable tiles that aren't water tiles
                if self.tiles[j,i].tile_info["blocker"] == False:
                    self.tiles[j,i].movement["range"] = True
                if self.tiles[j,i].units["count"] >= 9:
                    self.tiles[j,i].tile_info["range"] = False
                if self.tiles[j,i].units["count"] > 0:
                    if self.tiles[j,i].units["unit_type"] != unit_type:
                        self.tiles[j,i].tile_info["range"] = False

    def player2_valid_placement(self, unit_type):
        '''Set valid placement tiles for player 2'''
        for j in range(Map.row_count):
            for i in range(Map.column_count - 2, Map.column_count):
                #Set true for placeable tiles that aren't water tiles
                if self.tiles[j,i].tile_info["blocker"] == False:
                    self.tiles[j,i].movement["range"] = True
                if self.tiles[j,i].units["count"] >= 9:
                    self.tiles[j,i].tile_info["range"] = False
                if self.tiles[j,i].units["count"] > 0:
                    if self.tiles[j,i].units["unit_type"] != unit_type:
                        self.tiles[j,i].tile_info["range"] = False

    def set_move_options(self, row, column):
        '''Set valid move options up to 3 tiles out from a given index'''
        #set straight movements and movements 2 out and one over, cause easiest this way
        for i in range(3):
            current_row = row + 1 + i
            if current_row <= Map.row_count - 1:
                if self.tiles[current_row, column].tile_info["blocker"]:
                    break
                self.tiles[current_row, column].movement["range"] = True
                if i == 1:
                    if column + 1 <= Map.column_count - 1:
                        if not self.tiles[current_row, column + 1].tile_info["blocker"]:
                            self.tiles[current_row, column + 1].movement["range"] = True
                    if column - 1 >= 0:
                        if not self.tiles[current_row, column - 1].tile_info["blocker"]:
                            self.tiles[current_row, column - 1].movement["range"] = True
        for i in range(3):
            current_row = row - 1 - i
            if current_row >= 0:
                if self.tiles[current_row, column].tile_info["blocker"]:
                    break
                self.tiles[current_row, column].movement["range"] = True
                if i == 1:
                    if column + 1 <= Map.column_count - 1:
                        if not self.tiles[current_row, column + 1].tile_info["blocker"]:
                            self.tiles[current_row, column + 1].movement["range"] = True
                    if column - 1 >= 0:
                        if not self.tiles[current_row, column - 1].tile_info["blocker"]:
                            self.tiles[current_row, column - 1].movement["range"] = True
        for i in range(3):
            current_column = column + 1 + i
            if current_column <= Map.column_count - 1:
                if self.tiles[row, current_column].tile_info["blocker"]:
                    break
                self.tiles[row, current_column].movement["range"] = True
                if i == 1:
                    if row + 1 <= Map.row_count - 1:
                        if not self.tiles[row + 1, current_column].tile_info["blocker"]:
                            self.tiles[row + 1, current_column].movement["range"] = True
                    if row - 1 >= 0:
                        if not self.tiles[row - 1, current_column].tile_info["blocker"]:
                            self.tiles[row - 1, current_column].movement["range"] = True
        for i in range(3):
            current_column = column - 1 - i
            if current_column >= 0:
                if self.tiles[row, current_column].tile_info["blocker"]:
                    break
                self.tiles[row, current_column].movement["range"] = True
                if i == 1:
                    if row + 1 <= Map.row_count - 1:
                        if not self.tiles[row + 1, current_column].tile_info["blocker"]:
                            self.tiles[row + 1, current_column].movement["range"] = True
                    if row - 1 >= 0:
                        if not self.tiles[row - 1, current_column].tile_info["blocker"]:
                            self.tiles[row - 1, current_column].movement["range"] = True
        #Set Other moves, be sure to cover all possible options, some redundancy necessary
        #   up to 2 row moves
        for i in range(2):
            current_row = row + 1 + i
            if current_row <= Map.row_count - 1 and column + 1 <= Map.column_count - 1:
                if self.tiles[current_row, column + 1].tile_info["blocker"]:
                    break
                self.tiles[current_row, column + 1].movement["range"] = True
        for i in range(2):
            current_row = row + 1 + i
            if current_row <= Map.row_count - 1 and column - 1 >= 0:
                if self.tiles[current_row, column - 1].tile_info["blocker"]:
                    break
                self.tiles[current_row, column - 1].movement["range"] = True
        for i in range(2):
            current_row = row - 1 - i
            if current_row >= 0 and column + 1 <= Map.column_count - 1:
                if self.tiles[current_row, column + 1].tile_info["blocker"]:
                    break
                self.tiles[current_row, column + 1].movement["range"] = True
        for i in range(2):
            current_row = row - 1 - i
            if current_row >= 0 and column - 1 >= 0:
                if self.tiles[current_row, column - 1].tile_info["blocker"]:
                    break
                self.tiles[current_row, column - 1].movement["range"] = True
        #   up to 2 Column moves
        for i in range(2):
            current_column = column + 1 + i
            if current_column <= Map.column_count - 1 and row + 1 <= Map.row_count - 1:
                if self.tiles[row + 1, current_column].tile_info["blocker"]:
                    break
                self.tiles[row + 1, current_column].movement["range"] = True
        for i in range(2):
            current_column = column - 1 - i
            if current_column >= 0 and row + 1 <= Map.row_count -1:
                if self.tiles[row + 1, current_column].tile_info["blocker"]:
                    break
                self.tiles[row + 1, current_column].movement["range"] = True
        for i in range(2):
            current_column = column + 1 + i
            if current_column <= Map.column_count - 1 and row - 1 >= 0:
                if self.tiles[row - 1, current_column].tile_info["blocker"]:
                    break
                self.tiles[row - 1, current_column].movement["range"] = True
        for i in range(2):
            current_column = column - 1 - i
            if current_column >= 0 and row - 1 >= 0:
                if self.tiles[row - 1, current_column].tile_info["blocker"]:
                    break
                self.tiles[row - 1, current_column].movement["range"] = True
        #clean out spaces where units already exist
        #   Technically not the most efficient way, but should only be called once per click,
        #    and easier to read and manage
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                if self.tiles[j, i].units["count"] > 0:
                    self.tiles[j, i].movement["range"] = False

    def render_attacks(self, screen):
        '''Render mask for tiles that are valid attacks'''
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                if self.tiles[j,i].movement["reach"] == True:
                    screen.blit(self.valid_attackImg, (64+ 64*i, 64*j))

    def clear_attacks(self):
        '''Clear all tiles currently marked as valid attacks'''
        for j in range(Map.row_count):
            for i in range(Map.column_count):
                self.tiles[j,i].movement["reach"] = False

    def set_attack_options(self, origin):
        '''Set valid attack options from a given index'''
        originX, originY = origin
        if originX + 1 <= Map.row_count - 1:
            self.tiles[originX + 1, originY].movement["reach"] = True
        if originX - 1 >= 0:
            self.tiles[originX - 1, originY].movement["reach"] = True
        if originY + 1 <= Map.column_count - 1:
            self.tiles[originX, originY + 1].movement["reach"] = True
        if originY - 1 >= 0:
            self.tiles[originX, originY - 1].movement["reach"] = True

class Pool:
    '''Creates the Unit Pool for each player
    Currently creates a set pool for each player'''
    
    def __init__(self, player):
        '''Sets the rules for the player pool. If it is desired to change the number of units, only need to change the appropriate count here.'''
        self.player = player
        self.options = []
        if self.player == 1:
            self.x = 0
        else:
            self.x = (Map.column_count + 1) * 64
        self.axe_count = 9
        self.spear_count = 9
        self.sword_count = 9
        self.populate_pool()
        
    def populate_pool(self):
        '''Sets the defined pool parameters to the individual unit selection tiles'''
        self.axe_option = Unit_Selection(self.player, "axe", self.axe_count, self.x, 0)
        self.sword_option = Unit_Selection(self.player, "sword", self.sword_count, self.x, 64)
        self.spear_option = Unit_Selection(self.player, "spear", self.spear_count, self.x, 128)
        self.options.append(self.axe_option)
        self.options.append(self.sword_option)
        self.options.append(self.spear_option)
        
    def render_pool(self, screen):
        '''Display unit pool'''
        for i in self.options:
            i.render_selection(screen)

    def clear_selection(self):
        '''Make it so that no unit is currently selected in the pool'''
        for cell in self.options:
            cell.is_selected = False
    
    def unit_selected(self):
        '''set the selected'''
        for cell in self.options:
            if cell.is_selected:
                return True
        return False

    def get_selected(self):
        '''Find which unit in the pool is selected'''
        for cell in self.options:
            if cell.is_selected:
                return cell
        return None

    def get_count(self):
        '''Check the number of units remaining'''
        count = 0
        for cell in self.options:
            count = count + cell.count
        return count

class Unit_Selection:
    '''An individual unit selection tile of given player, type, number of units, and position of the selection tile'''
    def __init__(self, player, unit_type, count, x, y):
        '''Specify the player, type, count, and position of the selection tile, sets image of the tile accordingly'''
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
        '''Decrement number of this unit remaining in the pool'''
        self.count = self.count - 1
        self.text = self.font.render(str(self.count), True, self.yellow)

    def render_selection(self, screen):
        '''Show the unit, the outline of the selection tile, and highlight the tile if it is selected'''
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
        '''Confirm if the tile has been clicked'''
        posX, posY = pos
        if posX < self.x + 64  and posX > self.x:
            if posY < self.y + 64 and posY > self.y:
                return True
        return False
    
    def set_selected(self):
        '''Change self.is_selected to True'''
        self.is_selected = True
        
                

        

       
        
        

        

