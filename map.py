import tile

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
        for i in range(Map.column_count):
            Map.tiles.append([])
            for j in range(Map.row_count):
                x = i * 64 + Map.mapX
                y = j * 64 + Map.mapY
                self.tiles[i].append(tile.Plane(x, y))
                print("x=",x,"y=",y)

    def render_map(self,screen):
        for i in range(Map.column_count):
            for j in range(Map.row_count):
                self.tiles[i][j].showTile(screen)