import pygame

class Unit:
    unitX = 0
    unitY = 0
    unit_type = "unknown"

class Axe(Unit):
    unit_type = "axe"


class Spear(Unit):
    unit_type = "spear"

class Sword(Unit):
    unit_type = "sword"

class Group:
    #collection of units located in a tile
    def __init__(self):
        self.units = []    
    def add_unit(self, unit):
        self.units.append(unit)
    def subtract_unit(self, unit):
        self.units.pop()
    def show_group(self,screen):
        print("made it")
