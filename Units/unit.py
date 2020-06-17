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