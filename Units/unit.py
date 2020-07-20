import pygame

class Unit:
    #Base class for soldiers
    def __init__(self, player = 1):
        self.unitX = 0
        self.unitY = 0
        self.unit_type = "unknown"
        self.unitImg = None
    def show_unit(self, x, y, screen):
        screen.blit(self.unitImg, (x + self.unitX, y + self.unitY))
        

class Axe(Unit):
    #subclass for Axe soldiers
    def __init__(self, player = 1):
        Unit.__init__(self)
        self.unit_type = "axe"
        #dict to show which units this soldier gets higher victory chances against
        self.strengths = {
            "axe": False,
            "spear": True,
            "sword": False,
            "bow": True
        }
        if player == 1:
            self.unitImg = pygame.image.load('Images\\Soldiers\\BlueAxeIdle.png')
        elif player == 2:
            self.unitImg = pygame.image.load('Images\\Soldiers\\RedAxeIdle.png')
        else:
            self.unitImg == pygame.image.load('Images\\Soldiers\\SoldierNotFound.png')

class Spear(Unit):
    #subclass for Spear soldiers
    def __init__(self, player = 1):
        Unit.__init__(self)
        self.unit_type = "spear"
        #dict to show which units this soldier gets higher victory chances against
        self.strengths = {
            "axe": False,
            "spear": False,
            "sword": True,
            "bow": True
        }
        if player == 1:
            self.unitImg = pygame.image.load('Images\\Soldiers\\BlueSpearIdle.png')
        elif player == 2:
            self.unitImg = pygame.image.load('Images\\Soldiers\\RedSpearIdle.png')
        else:
            self.unitImg == pygame.image.load('Images\\Soldiers\\SoldierNotFound.png')
class Sword(Unit):
    #subclass for Sword soldiers
    def __init__(self, player = 1):
        Unit.__init__(self)
        self.unit_type = "sword"
        #dict to show which units this soldier gets higher victory chances against
        self.strengths = {
            "axe": True,
            "spear": False,
            "sword": False,
            "bow": True
        }
        if player == 1:
            self.unitImg = pygame.image.load('Images\\Soldiers\\BlueSwordIdle.png')
        elif player == 2:
            self.unitImg = pygame.image.load('Images\\Soldiers\\RedSwordIdle.png')
        else:
            self.unitImg == pygame.image.load('Images\\Soldiers\\SoldierNotFound.png')

class Group:
    #collection of units located in a tile
    def __init__(self, x, y):
        self.units = []
        self.count = 0   
        self.groupX = x
        self.groupY = y 
    def add_unit(self, unit):
        if self.count < 9:
            self.count = self.count + 1
            self.units.append(unit)
    def subtract_unit(self, unit):
        self.units.pop()
        self.count = self.count - 1
    def show_group(self,screen):
        self.position_units()
        for unit in self.units:
            unit.show_unit(self.groupX, self.groupY, screen)
    def position_units(self):
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
    


