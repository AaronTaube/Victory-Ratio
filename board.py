import tile
import Units.unit as unit
import random
import numpy
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
        #Attempted to make numpy matrix play with my tiles, but it didn't play well with subclasses
        print(self.tiles)
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

class Pool:
    #Creates the Unit Pool for each player
    #Currently creates a set pool for each player
    def __init__(self, player):
        self.player = player
        self.groups = []
        self.populate_pool()

    def populate_pool(self):
        y = 0
        if self.player == 1:
            x = 0
        else:
            x = 64 * (Map.column_count + 1)
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
            i.show_group(screen)
        
        
        

        

