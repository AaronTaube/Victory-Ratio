import pygame

#Initialize the pygame
pygame.init()

#handle Screen
screen = pygame.display.set_mode((960, 640))

#Boolean handlers
running = True
while running:
    #black backdrop
    screen.fill((0,0,0))

    #allows the game to be exited by clicking the 'x' in the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False