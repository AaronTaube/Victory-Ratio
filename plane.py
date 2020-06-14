import pygame
class Plane:
    #Plane style of tile

    #Plane image
    planeImg = pygame.image.load('Images\\grass_tile.png')
    tileX = 0
    tileY = 0
    #Access gameplay screen
    #screen = None
    def __init__(self, x, y, display):
        self.tileX = x
        self.tileY = y
        #self.screen = display

    def showTile(self,screen):
        screen.blit(self.planeImg, (self.tileX, self.tileY))
        print("show")