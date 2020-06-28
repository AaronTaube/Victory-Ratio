import pygame

class Unit:
    #Base class for soldiers
    def __init__(self):
        self.unitX = 0
        self.unitY = 0
        self.unit_type = "unknown"

class Axe(Unit):
    #subclass for Axe soldiers
    def __init__(self):
        Unit.__init__(self)
        self.unit_type = "axe"
        #dict to show which units this soldier gets higher victory chances against
        self.strengths = {
            "axe": False,
            "spear": True,
            "sword": False,
            "bow": True
        }


class Spear(Unit):
    #subclass for Spear soldiers
    def __init__(self):
        Unit.__init__(self)
        self.unit_type = "spear"
        #dict to show which units this soldier gets higher victory chances against
        self.strengths = {
            "axe": False,
            "spear": False,
            "sword": True,
            "bow": True
        }
class Sword(Unit):
    #subclass for Sword soldiers
    def __init__(self):
        Unit.__init__(self)
        self.unit_type = "sword"
        #dict to show which units this soldier gets higher victory chances against
        self.strengths = {
            "axe": True,
            "spear": False,
            "sword": False,
            "bow": True
        }
class Group:
    #collection of units located in a tile
    def __init__(self):
        self.units = []
        self.count = 0    
    def add_unit(self, unit):
        if self.count < 9:
            self.count = self.count + 1
            self.units.append(unit)
    def subtract_unit(self, unit):
        self.units.pop()
        self.count = self.count - 1
    def show_group(self,screen):
        print("made it")
