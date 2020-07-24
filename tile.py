import pygame
class Tile:
    tile_width = 64
    tile_height = 64
    def __init__(self, x, y):
        self.tileX = x
        self.tileY = y
        self.tile_bonus = 0
        self.tileImg = pygame.image.load('Images\\Tiles\\unfound_tile.png')
        self.unitImg = None
        self.is_blocker = False
        self.units = {
            "unit_type" : None,
            "count" : 0,
            "player" : 0,
            "moved" : False
        }
        self.movement = {
            "range" : False,
            "player" : 0,
            "reach" : False
        }
        self.placement = {
            "player" : 0
        }
        self.tile_info = {
            "tile_type" : None,
            "strength" : 0,
            "blocker" : False
        }
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
    #Unit management
    def add_unit(self, unit_type, player = 1):
        if self.units["unit_type"] == None:
            self.units["unit_type"] = unit_type
        if self.units["player"] == 0:
            self.units["player"] = player
        self.units["count"] = self.units["count"] + 1
        self.set_unitImg()
    def subtract_unit(self):
        self.units["count"] = self.units["count"] - 1
        if self.units["count"] == 0:
            clear_unit()
    def clear_unit(self):
        self.units["count"] = 0
        self.units["unit_type"] = None
        self.units["player"] = 0
        self.units["moved"] = False
    def set_unitImg(self):
        if self.units["player"] == 1:
            if self.units["unit_type"] == "axe":
                self.unitImg = pygame.image.load('Images\\Soldiers\\BlueAxeIdle.png')
            if self.units["unit_type"] == "sword":
                self.unitImg = pygame.image.load('Images\\Soldiers\\BlueSwordIdle.png')
            if self.units["unit_type"] == "spear":
                self.unitImg = pygame.image.load('Images\\Soldiers\\BlueSpearIdle.png')

        elif self.units["player"] ==  2:
            if self.units["unit_type"] == "axe":
                self.unitImg = pygame.image.load('Images\\Soldiers\\RedAxeIdle.png')
            if self.units["unit_type"] == "sword":
                self.unitImg = pygame.image.load('Images\\Soldiers\\ReddIdle.png')
            if self.units["unit_type"] == "spear":
                self.unitImg = pygame.image.load('Images\\Soldiers\\RedSpearIdle.png')
    def show_group(self, screen):
        #if no units present, skip
        if self.units["count"] <= 0:
            return
        unitX = 0
        unitY = 0
        for x in range(0, self.units["count"]):
            if x == 0:
                unitX = 12 + self.tileX
                unitY = 32 + self.tileY
            if x == 1:
                unitX = 0 + self.tileX
                unitY = 24 + self.tileY
            if x == 2:
                unitX = 24 + self.tileX
                unitY = 24 + self.tileY
            if x == 3:
                unitX = 12 + self.tileX
                unitY = 16 + self.tileY
            if x == 4:
                unitX = 0 + self.tileX
                unitY = 8  + self.tileY
            if x == 5:
                unitX = 24 + self.tileX
                unitY = 8 + self.tileY
            if x == 6:
                unitX = 12 + self.tileX
                unitY = 0 + self.tileY
            if x == 7:
                unitX = 0 + self.tileX
                unitY = -8 + self.tileY
            if x == 8:
                unitX = 24 + self.tileX
                unitY = -8 + self.tileY
            if x == 9:
                unitX = 12 + self.tileX
                unitY = -24 + self.tileY
            screen.blit(self.unitImg, (unitX, unitY))
        '''
        #if no units present, skip
        if self.count <= 0:
            return
        #Set all possible positions within tile for unit
        for x in range(0, self.count):
            if x == 0:
                self.units[x].unitX = 12
                self.units[x].unitY = 32
            if x == 1:
                self.units[x].unitX = 0
                self.units[x].unitY = 24
            if x == 2:
                self.units[x].unitX = 24
                self.units[x].unitY = 24
            if x == 3:
                self.units[x].unitX = 12
                self.units[x].unitY = 16
            if x == 4:
                self.units[x].unitX = 0
                self.units[x].unitY = 8
            if x == 5:
                self.units[x].unitX = 24
                self.units[x].unitY = 8
            if x == 6:
                self.units[x].unitX = 12
                self.units[x].unitY = 0
            if x == 7:
                self.units[x].unitX = 0
                self.units[x].unitY = -8
            if x == 8:
                self.units[x].unitX = 24
                self.units[x].unitY = -8
            if x == 9:
                self.units[x].unitX = 12
                self.units[x].unitY = -24
'''

class Plain(Tile):
    #Plain style of tile
    def __init__(self, x, y):
        Tile.__init__(self,x,y)
        self.tile_info["tile_type"] = "plain"
        #Plane image
        self.tileImg = pygame.image.load('Images\\Tiles\\grass_tile.png')

class Water(Tile):
    #Water style of tile
    def __init__(self, x, y):
        Tile.__init__(self,x,y)
        self.tile_info["tile_type"] = "water"
        self.tile_info["blocker"] = True
        #Water image
        self.tileImg = pygame.image.load('Images\\Tiles\\water_tile.png')


class Forest(Tile):
    #Forest style of tile
    def __init__(self, x, y):
        Tile.__init__(self,x,y)
        self.tile_info["tile_type"] = "water"
        self.tile_info["strength"] = 25
        #Forest image
        self.tileImg = pygame.image.load('Images\\Tiles\\forest_tile.png')
#may cancel this
class Selection(Tile):
    #Grid tile for unit pool
    def __init__(self, x, y):
        Tile.__init__(self,x,y)
        self.tileImg = pygame.image.load('Images\\Tiles\\outline_pool2.png')