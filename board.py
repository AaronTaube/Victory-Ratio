import tile
import Units.unit
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
                temp = numpy.append(temp, Units.unit.Group(x, y))
            self.units = numpy.vstack((self.units, temp)) 
            temp = numpy.empty([0,Map.column_count]) 
    
    def render_units(self, screen):
        for j in range(Map.column_count):
            for i in range(Map.row_count):
                self.units[i, j].show_group(screen)