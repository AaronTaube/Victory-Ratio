import pygame
import random
'''
Name:       tile.py
Purpose:    Class and subclasses for displaying the map tiles and accounting for gameplay mechanics such as terrain advantages,
            combat, animation at the more granular level
Author:     Aaron Taube
Created:    6/14/2020
TODO:       Animation for moving units
            Playing sound for animations
Notes:
'''
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
            "reach" : False
        }
        
        self.tile_info = {
            "tile_type" : None,
            "strength" : 0,
            "blocker" : False
        }
        self.strengths = {
            "spear" : "sword",
            "sword" : "axe",
            "axe" : "spear"
        }
        #values needed for running simple animation
        self.animateX = 0
        self.animateY = 0
    def show_tile(self, screen):
        screen.blit(self.tileImg, (self.tileX, self.tileY))
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
            self.clear_units()
    def clear_units(self):
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
                self.unitImg = pygame.image.load('Images\\Soldiers\\RedSwordIdle.png')
            if self.units["unit_type"] == "spear":
                self.unitImg = pygame.image.load('Images\\Soldiers\\RedSpearIdle.png')
    def show_group(self, screen):
        #if no units present, skip
        if self.units["count"] <= 0:
            return
        
        unitX = 0
        unitY = 0
        #place units based off the number of units in the slot
        for x in range(0, self.units["count"]):
            if x == 0:
                unitX = 12 + self.tileX + self.animateX
                unitY = 32 + self.tileY + self.animateY
            if x == 1:
                unitX = 0 + self.tileX + self.animateX
                unitY = 24 + self.tileY + self.animateY
            if x == 2:
                unitX = 24 + self.tileX + self.animateX
                unitY = 24 + self.tileY + self.animateY
            if x == 3:
                unitX = 12 + self.tileX  + self.animateX
                unitY = 16 + self.tileY + self.animateY
            if x == 4:
                unitX = 0 + self.tileX + self.animateX
                unitY = 8  + self.tileY + self.animateY
            if x == 5:
                unitX = 24 + self.tileX + self.animateX
                unitY = 8 + self.tileY + self.animateY
            if x == 6:
                unitX = 12 + self.tileX + self.animateX
                unitY = 0 + self.tileY + self.animateY
            if x == 7:
                unitX = 0 + self.tileX + self.animateX
                unitY = -8 + self.tileY + self.animateY
            if x == 8:
                unitX = 24 + self.tileX + self.animateX
                unitY = -8 + self.tileY + self.animateY
            if x == 9:
                unitX = 12 + self.tileX + self.animateX
                unitY = -24 + self.tileY + self.animateY
            screen.blit(self.unitImg, (unitX, unitY))
    def attack(self, defender):
        #if a unit was cleared in combat, it's type can land as None. If either is gone, skip
        if self.units["unit_type"] == None or defender.units["unit_type"] == None:
            return
        attacker_strength = 100
        defender_strength = 100
        #Check if a unit has advantage, and give it a 50% strength increase
        if self.strengths[self.units["unit_type"]] == defender.units["unit_type"]:
            attacker_strength += 50
        if defender.strengths[defender.units["unit_type"]] == self.units["unit_type"]:
            defender_strength += 50
        #Add defensive terrain bonus to defender strength
        defender_strength += defender.tile_info["strength"]
        #give each attacker one chance at killing an enemy unit
        for i in range (self.units["count"]):
            #but only if units remain
            if defender.units["count"] > 0:
                #generate random number between zero and the total of attacker and defender strength
                attack = random.randint(0, attacker_strength + defender_strength)
                #a high attacker strength has a higher chance of success
                #if the number generated is under the attack strength, kill a unit
                if attack < attacker_strength:
                    defender.subtract_unit()
    def slide_units(self, x, y):
        self.animateX = self.animateX + x
        self.animateY = self.animateY + y

        

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
        self.tile_info["tile_type"] = "forest"
        self.tile_info["strength"] = 25
        #Forest image
        self.tileImg = pygame.image.load('Images\\Tiles\\forest_tile.png')
#may cancel this
'''class Selection(Tile):
    #Grid tile for unit pool
    def __init__(self, x, y):
        Tile.__init__(self,x,y)
        self.tileImg = pygame.image.load('Images\\Tiles\\outline_pool2.png')'''