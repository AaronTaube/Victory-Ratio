import pygame
class Tile:
    #contains needed information for instantiating individual tiles on grid
    tileX = 0
    tileY = 0
    tileImg = None

    tile_bonus = 0
    def __init__(self, x, y):
        self.tileX = x
        self.tileY = y
    def showTile(self,screen):
        screen.blit(self.tileImg, (self.tileX, self.tileY))
        print("show")


class Plane(Tile):
    #Plane style of tile
    #Plane image
    tileImg = pygame.image.load('Images\\Tiles\\grass_tile.png')

class Water(Tile):
    #Water style of tile
    #Water image
    tileImg = pygame.image.load('Images\\Tiles\\water_tile.png')

class Forest(Tile):
    #Forest style of tile
    #Forest image
    tileImg = pygame.image.load('Images\\Tiles\\forest_tile.png')
    tile_bonus = .25
    