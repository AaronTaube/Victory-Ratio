import pygame
import board
import math
#Initialize the pygame
pygame.init()

#handle Screen
screen = pygame.display.set_mode((960, 640))
#Currently can store a 13x10 grid, allowing for a small amount of space on sides
game_map = board.Map()
play_grid = board.Grid()
movement_grid = board.Valid_Moves()
attack_grid = board.Valid_Attacks()
player1_pool = board.Pool(1)
player2_pool = board.Pool(2)

#handle selections
selected_unit = None
selected_move = None
selected_attack = None

#handle game states
game_begin_phase = False
game_end_phase = False
unit_selection_phase = True
player1_selection_phase = True
player2_selection_phase = False
player1_move_phase = False
player2_move_phase = False
combat_phase = False


def check_for_selection(pos):
    #Check for pool selection if it's that phase
    if unit_selection_phase:
        check_selection_phase(pos)
    return

def check_selection_phase(pos):
    #filter which player is selecting
    if player1_selection_phase:
        check_unit_selection(pos, player1_pool)
    elif player2_selection_phase:
        check_unit_selection(pos, player2_pool)

def check_unit_selection(pos, pool):
    #check for collision based on pool position
    x = pool.x
    y = 0
    posX, posY = pos
    groups = pool.groups
    for i in range(0, len(groups)):
        y = i * 64
        if isCollision(x, y, posX, posY):
            print("x",x, "y", y)
        print(i)
        
def isCollision(selectionX, selectionY, posX, posY):
    distance = math.sqrt(math.pow(selectionX - posX, 2) + math.pow(selectionY - posY, 2))
    if distance < 32:
        return True
    else:
        return False



#Boolean handlers
running = True
while running:
    #black backdrop
    screen.fill((0,0,0))
    #Render all interface by layer
    game_map.render_map(screen)
    play_grid.render_units(screen)
    player1_pool.render_units(screen)
    player2_pool.render_units(screen)
    #allows the game to be exited by clicking the 'x' in the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            check_for_selection(pos)
    pygame.display.update()

