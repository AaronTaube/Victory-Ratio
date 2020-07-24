import pygame
import board
import math
import Units.unit as unit
import gameplay_buttons as gb
#Initialize the pygame
pygame.init()

#handle Screen
screen = pygame.display.set_mode((960, 640))
#Currently can store a 13x10 grid, allowing for a small amount of space on sides
game_map = board.Map()
#play_grid = board.Grid()
#movement_grid = board.Valid_Moves()
#attack_grid = board.Valid_Attacks()
player1_pool = board.Pool(1)
player2_pool = board.Pool(2)
pass_button = gb.Pass_Button(screen)
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
#chosen_group = None
chosen_destination = None
chosen_attack = None
chosen_cell = None
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
            #game_map.clear_moves()
            game_map.player1_valid_placement(chosen_unit.unit_type)
    elif player2_selection_phase:
        #confirm which unit is being selected
        for cell in player2_pool.options:
            if cell.check_collision(pos):
                player2_pool.clear_selection()
                if cell.count > 0:
                    cell.set_selected()
        #highlight tiles that units can be placed in
        if player2_pool.unit_selected():
            chosen_unit = player2_pool.get_selected()
            game_map.player2_valid_placement(chosen_unit.unit_type)
    #if no unit selected, exit to minimize work
    if chosen_unit == None:
        return
    #place units
    for row in game_map.tiles:
        for cell in row:
            if cell.check_collision(pos):
                if cell.movement["range"]:
                    place_unit(cell)
                    units_to_place = units_to_place - 1
                    chosen_unit.reduce_count()
                    if(chosen_unit.count <= 0):
                        player1_pool.clear_selection()
                        player2_pool.clear_selection()
                        chosen_unit = None
                '''if movement_grid.choices[cell.indexX, cell.indexY]:
                    place_unit(cell.indexX, cell.indexY)
                    units_to_place = units_to_place - 1
                    chosen_unit.reduce_count()
                    if chosen_unit.count <= 0:
                        player1_pool.clear_selection()
                        player2_pool.clear_selection()
                        chosen_unit = None'''
                    #play_grid.units[cell.indexX, cell.indexY].add_unit(unit.Sword())
    #Handle swapping of player phase
    if units_to_place <= 0:
        player1_selection_phase = not player1_selection_phase
        player2_selection_phase = not player2_selection_phase
        units_to_place = 9
        chosen_unit = None
        player1_pool.clear_selection()
        player2_pool.clear_selection()
        game_map.clear_moves()
        if player1_pool.get_count() <= 0 and player2_pool.get_count() <= 0:
            player1_selection_phase = False
            player2_selection_phase = False
            unit_selection_phase = False
            game_on_phase = True
            player1_move_phase = True
    '''#confirm which unit is being selected
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
            player1_move_phase = True'''

def place_unit(cell):
    unit_type = chosen_unit.unit_type
    if player1_selection_phase:
        cell.add_unit(unit_type)
    if player2_selection_phase:
        cell.add_unit(unit_type, 2)
    '''if player1_selection_phase:
        game_map.tiles[x, y].add_unit(unit_type)
    if player2_selection_phase:
        game_map.tiles[x, y].add_unit(unit_type, 2)'''
#Gameplay Handlers
def check_for_gameplay(pos):
    if game_on_phase:
        gameplay_phase(pos)
def gameplay_phase(pos):
    #Grab Globals
    global game_on_phase
    global player1_move_phase
    global player2_move_phase
    global combat_phase
    #global chosen_group
    global chosen_cell
    global chosen_destination
    global chosen_attack
    #Select unit
    if combat_phase == False: #and chosen_group == None:
        for row in game_map.tiles:
            for cell in row:
                if cell.check_collision(pos):
                    '''if len(play_grid.units[cell.indexX, cell.indexY].units) > 0 and play_grid.units[cell.indexX, cell.indexY].moved == False:
                        #confirm unit selected is selectable by active player
                        if play_grid.units[cell.indexX, cell.indexY].units[0].player == 1 and player1_move_phase:
                            chosen_group = play_grid.units[cell.indexX, cell.indexY]
                        elif play_grid.units[cell.indexX, cell.indexY].units[0].player == 2 and player2_move_phase:
                            chosen_group = play_grid.units[cell.indexX, cell.indexY]
                        #if choice valid, set movement options
                        if chosen_group != None:
                            movement_grid.clear()
                            movement_grid.set_move_options(cell.indexX, cell.indexY, game_map.tiles, play_grid.units)
                        chosen_cell = cell.indexX, cell.indexY
                        return #Done for this click'''
                    #determine if moveable unit in cell
                    if cell.units["count"] > 0 and cell.units["moved"] == False:
                        #confirm unit is selectable by active player
                        if cell.units["player"] == 1 and player1_move_phase:
                            chosen_cell = cell
                        elif cell.units["player"] == 2 and player2_move_phase:
                            chosen_cell = cell
                        #if choice valid, set movement options
                        if chosen_cell != None:
                            game_map.clear_moves()
                            game_map.set_move_options(cell.indexX, cell.indexY)
                        return #Done for this click
    if chosen_cell != None and combat_phase == False:
        for row in game_map.tiles:
            for cell in row:
                if cell.check_collision(pos):
                    if cell.movement["range"]:
                        move_unit(chosen_cell, cell)
                        chosen_cell = cell
                        game_map.clear_moves()
                        combat_phase = True
                        coordinate = chosen_cell.indexX, chosen_cell.indexY
                        game_map.set_attack_options(coordinate)
                        print("check")
                        return
                        '''chosen_cell = cell.indexX, cell.indexY
                        unit_type = chosen_group.unit_type
                        play_grid.units[chosen_cell].units = chosen_group.units
                        play_grid.units[chosen_cell].count = chosen_group.count
                        chosen_group.units = []
                        chosen_group.count = 0
                        chosen_group = play_grid.units[chosen_cell]
                        #prepare for combat phase
                        movement_grid.clear()
                        combat_phase = True
                        attack_grid.set_attack_options(chosen_cell)
                        return'''
    if combat_phase:
        for row in game_map.tiles:
            for cell in row:
                if cell.check_collision(pos):
                    print('TODO Combat Stuff')
                    #Insert code to calculate damage and trigger animations

                    #end code here
                    #swap the turn
                    '''player1_move_phase = not player1_move_phase
                    player2_move_phase = not player2_move_phase
                    combat_phase = False
                    chosen_group = None
                    chosen_cell = None
                    attack_grid.clear()'''
                    swap_turn()
                    return #exit before triggering next loop
    #If player chooses to skip combat, change to next player's turn
    if combat_phase:
        if pass_button.check_collision(pos):
            '''player1_move_phase = not player1_move_phase
            player2_move_phase = not player2_move_phase
            combat_phase = False
            chosen_group = None
            chosen_cell = None
            attack_grid.clear()'''
            swap_turn()
            return #exit before triggering next loop
    #If player chooses for the selected unit to stay in place, switch to combat phase
    if not combat_phase:
        if pass_button.check_collision(pos):
            game_map.clear_moves()
            combat_phase = True
            coordinate = chosen_cell.indexX, chosen_cell.indexY
            game_map.set_attack_options(coordinate)

def move_unit(start, end):
    end.units = start.units.copy()
    end.set_unitImg()
    start.clear_unit()
#code for ending player turn
def swap_turn():
    global player1_move_phase
    global player2_move_phase
    global combat_phase
    #global chosen_group
    global chosen_cell
    #play_grid.units[chosen_cell].moved = True
    chosen_cell.units["moved"] = True
    player1_move_phase = not player1_move_phase
    player2_move_phase = not player2_move_phase
    combat_phase = False
    #chosen_group = None
    chosen_cell = None
    game_map.clear_attacks()

def next_round():
    print('TODO')
        


#Gameplay Loop
#Boolean handlers
running = True
while running:
    #black backdrop
    screen.fill((0,0,0))
    #Render all interface by layer
    game_map.render_map(screen)
    game_map.render_moves(screen)   
    game_map.render_units(screen)

    '''movement_grid.render_moves(screen)
    attack_grid.render_attacks(screen)
    play_grid.render_units(screen)'''
    if unit_selection_phase:
        player1_pool.render_pool(screen)
        player2_pool.render_pool(screen)
    if game_on_phase:
        pass_button.show_button()
        game_map.render_gray(screen)
        if combat_phase:
            game_map.render_attacks(screen)
    #allows the game to be exited by clicking the 'x' in the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            check_for_selection(pos)
            check_for_gameplay(pos)
    pygame.display.update()

