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
game_on_phase = False
game_end_phase = False
#Selection phase
unit_selection_phase = True
player1_selection_phase = True
player2_selection_phase = False
units_to_place = 9
chosen_unit = None

#Movement and combat phases
player1_move_phase = False
player2_move_phase = False
combat_phase = False
chosen_group = None
chosen_destination = None
chosen_attack = None
#Unit Placement Handlers
def check_for_selection(pos):
    #Check for pool selection if it's that phase
    if unit_selection_phase:
        handle_selection_phase(pos)
    return

def handle_selection_phase(pos):
    #grab needed globals
    global chosen_unit
    global units_to_place
    global player1_selection_phase
    global player2_selection_phase
    global unit_selection_phase
    global player1_move_phase
    global game_on_phase
    #filter which player is selecting

    #confirm which unit is being selected
    if player1_selection_phase:
        for cell in player1_pool.options:
            if cell.check_collision(pos):
                player1_pool.clear_selection()
                
                if cell.count > 0:
                    cell.set_selected()
        #highlight tiles that units can be placed in
        if player1_pool.unit_selected():
            chosen_unit = player1_pool.get_selected()
            movement_grid.clear()
            movement_grid.player1_valid_placement(game_map.tiles, play_grid.units, chosen_unit.unit_type)
    elif player2_selection_phase:
        #confirm which unit is being selected
        for cell in player2_pool.options:
            if cell.check_collision(pos):
                player2_pool.clear_selection()
                cell.set_selected()
        #highlight tiles that units can be placed in
        if player2_pool.unit_selected():
            chosen_unit = player2_pool.get_selected()
            movement_grid.player2_valid_placement(game_map.tiles, play_grid.units, chosen_unit.unit_type)
    #if no unit selected, exit to minimize work
    if chosen_unit == None:
        return
    #place units
    for row in game_map.tiles:
        for cell in row:
            if cell.check_collision(pos):
                if movement_grid.choices[cell.indexX, cell.indexY]:
                    place_unit(cell.indexX, cell.indexY)
                    units_to_place = units_to_place - 1
                    chosen_unit.reduce_count()
                    if chosen_unit.count <= 0:
                        player1_pool.clear_selection()
                        player2_pool.clear_selection()
                        chosen_unit = None
                    #play_grid.units[cell.indexX, cell.indexY].add_unit(unit.Sword())
    #Handle swapping of player phase
    if units_to_place <= 0:
        player1_selection_phase = not player1_selection_phase
        player2_selection_phase = not player2_selection_phase
        units_to_place = 9
        chosen_unit = None
        player1_pool.clear_selection()
        player2_pool.clear_selection()
        movement_grid.clear()
        if player1_pool.get_count() <= 0 and player2_pool.get_count() <= 0:
            player1_selection_phase = False
            player2_selection_phase = False
            unit_selection_phase = False
            game_on_phase = True
            player1_move_phase = True

def place_unit(x, y):
    unit_type = chosen_unit.unit_type
    if player1_selection_phase:
        if unit_type == 'axe':
            play_grid.units[x, y].add_unit(unit.Axe())
        if unit_type == 'sword':
            play_grid.units[x, y].add_unit(unit.Sword())
        if unit_type == 'spear':
            play_grid.units[x, y].add_unit(unit.Spear())

    if player2_selection_phase:
        if unit_type == 'axe':
            play_grid.units[x, y].add_unit(unit.Axe(2))
        if unit_type == 'sword':
            play_grid.units[x, y].add_unit(unit.Sword(2))
        if unit_type == 'spear':
            play_grid.units[x, y].add_unit(unit.Spear(2))
#Gameplay Handlers
def check_for_gameplay(pos):
    if game_on_phase:
        gameplay_phase(pos)
def gameplay_phase(pos):
    #Grab GLobals
    global game_on_phase
    global player1_move_phase
    global player2_move_phase
    global combat_phase
    global chosen_group
    global chosen_destination
    global chosen_attack
    #Select unit
    if combat_phase == False: #and chosen_group == None:
        for row in game_map.tiles:
            for cell in row:
                if cell.check_collision(pos):
                    if len(play_grid.units[cell.indexX, cell.indexY].units) > 0:
                        #confirm unit selected is selectable by active player
                        if play_grid.units[cell.indexX, cell.indexY].units[0].player == 1 and player1_move_phase:
                            chosen_group = play_grid.units[cell.indexX, cell.indexY]
                        elif play_grid.units[cell.indexX, cell.indexY].units[0].player == 2 and player2_move_phase:
                            chosen_group = play_grid.units[cell.indexX, cell.indexY]
                        #if choice valid, set movement options
                        if chosen_group != None:
                            movement_grid.clear()
                            movement_grid.set_move_options(cell.indexX, cell.indexY, game_map.tiles, play_grid.units)
                        return #Done for this click

    if chosen_group != None and combat_phase == False:
        for row in game_map.tiles:
            for cell in row:
                if cell.check_collision(pos):
                    if(movement_grid.choices[cell.indexX, cell.indexY]):
                        print(cell.indexX, cell.indexY, "made it", player1_move_phase, player2_move_phase)
                        unit_type = chosen_group.unit_type
                        play_grid.units[cell.indexX, cell.indexY].units = chosen_group.units
                        play_grid.units[cell.indexX, cell.indexY].count = chosen_group.count
                        chosen_group.units = []
                        chosen_group.count = 0
                        movement_grid.clear()
                        #for i in chosen_group.units:
                         #   soldier = i.remove_unit()

                            #play_grid.units[cell.indexX, cell.indexY].units.add_unit()
                    '''if player1_move_phase:
                        if unit_type == 'axe':
                            play_grid.units[cell.indexX, cell.indexY].add_unit(unit.Axe())
                        if unit_type == 'sword':
                            play_grid.units[cell.indexX, cell.indexY].add_unit(unit.Sword())
                        if unit_type == 'spear':
                            play_grid.units[cell.indexX, cell.indexY].add_unit(unit.Spear())

                    if player2_move_phase:
                        if unit_type == 'axe':
                            play_grid.units[cell.indexX, cell.indexY].add_unit(unit.Axe(2))
                        if unit_type == 'sword':
                            play_grid.units[cell.indexX, cell.indexY].add_unit(unit.Sword(2))
                        if unit_type == 'spear':
                            play_grid.units[cell.indexX, cell.indexY].add_unit(unit.Spear(2))
                    chosen_group.subtract_unit()'''
                            #play_grid.units[cell.indexX, cell.indexY] = chosen_group
                    '''if movement_grid.choices[cell.indexX, cell.indexY]:
                        place_unit(cell.indexX, cell.indexY)
                        units_to_place = units_to_place - 1
                        chosen_unit.reduce_count()
                        if chosen_unit.count <= 0:
                            player1_pool.clear_selection()
                            player2_pool.clear_selection()
                            chosen_unit = None'''
    return


#Gameplay Loop
#Boolean handlers
running = True
while running:
    #black backdrop
    screen.fill((0,0,0))
    #Render all interface by layer
    game_map.render_map(screen)
    movement_grid.render_moves(screen)
    play_grid.render_units(screen)
    if unit_selection_phase:
        player1_pool.render_pool(screen)
        player2_pool.render_pool(screen)
    #allows the game to be exited by clicking the 'x' in the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            check_for_selection(pos)
            check_for_gameplay(pos)
    pygame.display.update()

