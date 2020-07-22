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