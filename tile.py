import pygame
class Tile:
    tile_width = 64
    tile_height = 64
    def __init__(self, x, y):
        self.tileX = x
        self.tileY = y
        self.tile_bonus = 0
        self.tileImg = pygame.image.load('Images\\Tiles\\unfound_tile.png')
    def show_tile(self, screen):
        screen.blit(self.tileImg, (self.tileX, self.tileY))
        #print("show")
    def assign_coordinate(self, x, y):
        self.indexX = x
        self.indexY = y
    def check_collision(self, pos):
        posX, posY = pos
        if posX < self.tileX + 64  and posX > self.tileX:
            if posY < self.tileY + 64 and posY > self.tileY:
                return True
        return False

class Plain(Tile):
    #Plain style of tile
    def __init__(self, x, y):
        Tile.__init__(self,x,y)
        #Plane image
        self.tileImg = pygame.image.load('Images\\Tiles\\grass_tile.png')

class Water(Tile):
    #Water style of tile
    def __init__(self, x, y):
        Tile.__init__(self,x,y)
        #Water image
        self.tileImg = pygame.image.load('Images\\Tiles\\water_tile.png')

class Forest(Tile):
    #Forest style of tile
    def __init__(self, x, y):
        Tile.__init__(self,x,y)
        #Forest image
        self.tileImg = pygame.image.load('Images\\Tiles\\forest_tile.png')
        self.tile_bonus = .25
class Selection(Tile):
    #Grid tile for unit pool
    def __init__(self, x, y):
        Tile.__init__(self,x,y)
        self.tileImg = pygame.image.load('Images\\Tiles\\outline_pool2.png')