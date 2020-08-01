'''
Name:       gameplay_UI.py
Purpose:    Classes for GUI elements outside of the game board itself. Pass button, text instructions etc;
Author:     Aaron Taube
Created:    7/21/2020
TODO:       Add visual feedback for pass button clicked
            Add tutorial window
            Add menu button
Notes:
'''
import pygame

#Allows player to skip certain actions
class Pass_Button:
    '''Pass_Button class for handling GUI behavior of the Pass Button'''
    def __init__(self, screen):
        self.buttonImg = pygame.image.load('Images\\Buttons\\Pass.png')
        self.screen = screen
    def show_button(self):
        self.screen.blit(self.buttonImg, (0, 0))
    def check_collision(self, pos):
        posX, posY = pos
        if posX < 64  and posX > 0:
            if posY < 128 and posY > 0:
                return True
        return False
#Instructive text at the bottom of the screen, such as telling whose turn it is
class Instruction:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('PressStart2P-Regular.ttf', 36)
        self.yellow = (255,255,0)
        self.text = self.font.render("Game Start", True, self.yellow)
    def show_instructions(self):
        self.screen.blit(self.text, (64, 586))
    def set_instructions(self, text):
        self.text = self.font.render(text, True, self.yellow)
class Tutorial:
    def __init__(self, screen):
        self.screen = screen
        self.tutorialImg = pygame.image.load('Images\\Buttons\\Tutorial.png')
    def render_tutorial(self):
        self.screen.blit(self.tutorialImg, (0, 0))
