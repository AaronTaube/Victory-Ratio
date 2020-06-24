import pygame
import board
#Initialize the pygame
pygame.init()

#handle Screen
screen = pygame.display.set_mode((960, 640))
#Currently can store a 13x10 grid, allowing for a small amount of space on sides
game_map = board.Map()
play_grid = board.Grid()
#Boolean handlers
running = True
while running:
    #black backdrop
    screen.fill((0,0,0))
    game_map.render_map(screen)
    play_grid.render_units(screen)
    #allows the game to be exited by clicking the 'x' in the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()