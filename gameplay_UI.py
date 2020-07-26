import pygame

class Pass_Button:
    def __init__(self, screen):
        self.buttonImg = pygame.image.load('Images\\Buttons\\Pass.png')
        self.screen = screen
    def show_button(self):
        self.screen.blit(self.buttonImg, (0, 0))
    def check_collision(self, pos):
        posX, posY = pos
        if posX < 64  and posX > 0:
            if posY < 128 and posY > 0:
                print('click')
                return True
        return False
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