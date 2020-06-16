import pygame
class Tile:
    #contains needed information for instantiating individual tiles on grid
    tileX = 0
    tileY = 0
    planeImg = None
    def __init__(self, x, y):
        self.tileX = x
        self.tileY = y
    def showTile(self,screen):
        screen.blit(self.planeImg, (self.tileX, self.tileY))
        print("show")


class Plane(Tile):
    #Plane style of tile

    #Plane image
    planeImg = pygame.image.load('Images\\grass_tile.png')
    tileX = 0
    tileY = 0
    