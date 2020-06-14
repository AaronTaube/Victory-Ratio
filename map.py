import numpy
import plane

class Map:
    #Positioning Data
    #create grid
    column_count = 13
    row_count = 10
    tiles = []
    #position grid
    mapX = 64
    mapY = 0

    #Creates and stores an array of tiles that make up the playspace
    def __init__(self, display):
        for i in range(self.column_count):
            self.tiles.append([])
            for j in range(self.row_count):
                x = i * 64 + self.mapX
                y = j * 64 + self.mapY
                self.tiles[i].append(plane.Plane(x, y, display))
                print("x=",x,"y=",y)

    def render_map(self,screen):
        for i in range(self.column_count):
            for j in range(self.row_count):
                self.tiles[i][j].showTile(screen)