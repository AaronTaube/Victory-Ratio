import pygame
import board
import math
import Units.unit as unit
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

#Handle game states
#Begin and End Phase
game_begin_phase = False
game_end_phase = False
#Selection phase
unit_selection_phase = True
player1_selection_phase = True
player2_selection_phase = False
placed_units = 0
chosen_unit = None
#Movement and combat phases
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

    #confirm which unit is being selected
    if player1_selection_phase:
        for cell in player1_pool.options:
            if cell.check_collision(pos):
                player1_pool.clear_selection()
                cell.set_selected()
        #highlight tiles that units can be placed in
        if player1_pool.unit_selected():
            chosen_unit = player1_pool.get_selected()
            movement_grid.player1_valid_placement(game_map.tiles, play_grid.units, chosen_unit)
    elif player2_selection_phase:
        #confirm which unit is being selected
        for cell in player2_pool.options:
            if cell.check_collision(pos):
                player2_pool.clear_selection()
                cell.set_selected()
        #highlight tiles that units can be placed in
        if player2_pool.unit_selected():
            chosen_unit = player2_pool.get_selected()
            movement_grid.player2_valid_placement(game_map.tiles, play_grid.units, chosen_unit)
    #if no unit selected, exit to minimize work
    if chosen_unit == None:
        return
    #place units
    for row in game_map.tiles:
        for cell in row:
            if cell.check_collision(pos):
                if movement_grid.choices[cell.indexX, cell.indexY]:
                    play_grid.units[cell.indexX, cell.indexY].add_unit(unit.Sword())

'''def check_unit_selection(pos, pool):
    #check for collision based on pool position
    x = pool.x
    y = 0
    posX, posY = pos
    options = pool.options
    for i in range(0, len(options)):
        y = i * 64
        if isCollision(x, y, posX, posY):
            print("x",x, "y", y)
        #print(i)'''
        
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
    movement_grid.render_moves(screen)
    play_grid.render_units(screen)
    #player1_pool.render_units(screen)
    #player2_pool.render_units(screen)
    player1_pool.render_pool(screen)
    player2_pool.render_pool(screen)
    #allows the game to be exited by clicking the 'x' in the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            check_for_selection(pos)
    pygame.display.update()

