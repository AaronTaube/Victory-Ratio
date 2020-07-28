import pygame
import board
import math
import gameplay_UI as gUI

'''
Name:       main.py
Purpose:    Handles core gameplay loop and screen updates. 
Author:     Aaron Taube
Created:    6/13/2020
TODO:       Any needed changes for adding sound
            Any needed changes for compatibility with changes elsewhere
Notes:
'''
#Initialize the pygame
pygame.init()

#handle Screen
screen = pygame.display.set_mode((960, 640))
#Title and Icon
pygame.display.set_caption("Victory Ratio")
icon = pygame.image.load('Images\\Soldiers\\BlueAxeIdle.png')
pygame.display.set_icon(icon)
#Used just to lock framerate
clock = pygame.time.Clock()
keyframe_delay = 21
#Currently can store a 13x10 grid, allowing for a small amount of space on sides
game_map = board.Map()
player1_pool = board.Pool(1)
player2_pool = board.Pool(2)
pass_button = gUI.Pass_Button(screen)
instructions = gUI.Instruction(screen)
tutorial = gUI.Tutorial(screen)
#handle selections
selected_unit = None
selected_move = None
selected_attack = None

#Handle game states
#Begin and End Phase
initiation_phase = True
game_on_phase = False
game_end_setup = False
winner_text = ""
#Selection phase
tutorial_phase = True
unit_selection_phase = False
player1_selection_phase = False
player2_selection_phase = False
units_to_place = 9
chosen_unit = None

#Movement and combat phases
player1_move_phase = False
player2_move_phase = False
combat_phase = False
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
                    if player2_selection_phase:
                        instructions.set_instructions("Player 2 place " + str(units_to_place) + " units")
                    if player1_selection_phase:
                        instructions.set_instructions("Player 1 place " + str(units_to_place) + " units")
                
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
        #update instruction text
        if player2_selection_phase:
            instructions.set_instructions("Player 2 place " + str(units_to_place) + " units")
        if player1_selection_phase:
            instructions.set_instructions("Player 1 place " + str(units_to_place) + " units")
        if player1_pool.get_count() <= 0 and player2_pool.get_count() <= 0:
            player1_selection_phase = False
            player2_selection_phase = False
            unit_selection_phase = False
            game_on_phase = True
            player1_move_phase = True
            instructions.set_instructions("Player 1's turn!")
        
    

def place_unit(cell):
    unit_type = chosen_unit.unit_type
    if player1_selection_phase:
        cell.add_unit(unit_type)
    if player2_selection_phase:
        cell.add_unit(unit_type, 2)
    
#Gameplay Handlers
def check_for_gameplay(pos):
    if game_on_phase:
        gameplay_phase(pos)
        check_for_round()
def check_for_round():
    #if any unit has not been moved, continue round
    for row in game_map.tiles:
            for cell in row:
                if cell.units["moved"] == False and cell.units["count"] > 0:
                    return
    #else, new round
    new_round()
#reset round at player 1 goes first
def new_round():
    for row in game_map.tiles:
        for cell in row:
            if cell.units["moved"] == True:
                cell.units["moved"] = False
    player1_move_phase = True
    player2_move_phase = False
    update_turn_text()

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
                            game_map.set_move_options(chosen_cell.indexX, chosen_cell.indexY)
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
                        return
                      
    if combat_phase:
        for row in game_map.tiles:
            for cell in row:
                if cell.check_collision(pos):
                    if cell.units["player"] != chosen_cell.units["player"] and cell.units["count"] > 0 and cell.movement["reach"]:
                        #attacking player deals damage first
                        if chosen_cell.indexY < cell.indexY:
                            animate_combat(chosen_cell, "up")
                        if chosen_cell.indexY > cell.indexY:
                            animate_combat(chosen_cell, "down")
                        if chosen_cell.indexX < cell.indexX:
                            animate_combat(chosen_cell, "right")
                        if chosen_cell.indexX > cell.indexX:
                            animate_combat(chosen_cell, "left")
                        chosen_cell.attack(cell)
                        #defending player deals damage after losing units
                        if cell.indexY < chosen_cell.indexY:
                            animate_combat(cell, "up")
                        if cell.indexY > chosen_cell.indexY:
                            animate_combat(cell, "down")
                        if cell.indexX < chosen_cell.indexX:
                            animate_combat(cell, "right")
                        if cell.indexX > chosen_cell.indexX:
                            animate_combat(cell, "left")
                        cell.attack(chosen_cell)
                    else:
                        return #not valid target, so no reaction
                    #swap the turn
                    swap_turn()
                    return #exit before triggering next loop
    #If player chooses to skip combat, change to next player's turn
    if combat_phase:
        if pass_button.check_collision(pos):
            swap_turn()
            return #exit before triggering next loop
    #If player chooses for the selected unit to stay in place, switch to combat phase
    if not combat_phase:
        if pass_button.check_collision(pos):
            if chosen_cell == None:
                return #skip if no unit being held
            game_map.clear_moves()
            combat_phase = True
            coordinate = chosen_cell.indexX, chosen_cell.indexY
            game_map.set_attack_options(coordinate)

def animate_combat(cell, direction):
    if direction == "left":
        #slide unit towards target
        for i in range(12):
            cell.slide_units(0, -2)
            #continue to animate all other aspects as normal
            screen.fill((0,0,0))
            game_map.render_map(screen) 
            game_map.render_units(screen)
            game_map.render_gray(screen)
            pass_button.show_button()
            instructions.show_instructions()
            pygame.time.delay(keyframe_delay)
            pygame.display.update()
        #slide unit back to start position
        for i in range(12):
            cell.slide_units(0, 2)
            #continue to animate all other aspects as normal
            screen.fill((0,0,0))
            game_map.render_map(screen) 
            game_map.render_units(screen)
            game_map.render_gray(screen)
            pass_button.show_button()
            instructions.show_instructions()
            pygame.time.delay(keyframe_delay)
            pygame.display.update()
    if direction == "right":
        #slide unit towards target
        for i in range(12):
            cell.slide_units(0, 2)
            #continue to animate all other aspects as normal
            screen.fill((0,0,0))
            game_map.render_map(screen) 
            game_map.render_units(screen)
            game_map.render_gray(screen)
            pass_button.show_button()
            instructions.show_instructions()
            pygame.time.delay(keyframe_delay)
            pygame.display.update()
        #slide unit back to start position
        for i in range(12):
            cell.slide_units(0, -2)
            #continue to animate all other aspects as normal
            screen.fill((0,0,0))
            game_map.render_map(screen) 
            game_map.render_units(screen)
            game_map.render_gray(screen)
            pass_button.show_button()
            instructions.show_instructions()
            pygame.time.delay(keyframe_delay)
            pygame.display.update()
    if direction == "up":
        #slide unit towards target
        for i in range(12):
            cell.slide_units(2,0)
            #continue to animate all other aspects as normal
            screen.fill((0,0,0))
            game_map.render_map(screen) 
            game_map.render_units(screen)
            game_map.render_gray(screen)
            pass_button.show_button()
            instructions.show_instructions()
            pygame.time.delay(keyframe_delay)
            pygame.display.update()
        #slide unit back to start position
        for i in range(12):
            cell.slide_units(-2, 0)
            #continue to animate all other aspects as normal
            screen.fill((0,0,0))
            game_map.render_map(screen) 
            game_map.render_units(screen)
            game_map.render_gray(screen)
            pass_button.show_button()
            instructions.show_instructions()
            pygame.time.delay(keyframe_delay)
            pygame.display.update()
    if direction == "down":
        #slide unit towards target
        for i in range(12):
            cell.slide_units(-2, 0)
            #continue to animate all other aspects as normal
            screen.fill((0,0,0))
            game_map.render_map(screen) 
            game_map.render_units(screen)
            game_map.render_gray(screen)
            pass_button.show_button()
            instructions.show_instructions()
            pygame.time.delay(keyframe_delay)
            pygame.display.update()
        #slide unit back to start position
        for i in range(12):
            cell.slide_units(2, 0)
            #continue to animate all other aspects as normal
            screen.fill((0,0,0))
            game_map.render_map(screen) 
            game_map.render_units(screen)
            game_map.render_gray(screen)
            pass_button.show_button()
            instructions.show_instructions()
            pygame.time.delay(keyframe_delay)
            pygame.display.update()
    
def move_unit(start, end):
    end.units = start.units.copy()
    end.set_unitImg()
    start.clear_units()
#code for ending player turn
def swap_turn():
    global player1_move_phase
    global player2_move_phase
    global combat_phase
    #global chosen_group
    global chosen_cell
    #play_grid.units[chosen_cell].moved = True
    chosen_cell.units["moved"] = True
    if player1_move_phase:
        if not check_has_moves(2) and check_has_moves(1):
            chosen_cell = None
            combat_phase = False
            game_map.clear_attacks()
            return #if other player has no valid moves, stay on this players turn
    if player2_move_phase:
        if not check_has_moves(1) and check_has_moves(2):
            chosen_cell = None
            combat_phase = False
            game_map.clear_attacks()
            return #if other player has no valid moves, stay on this players turn
    player1_move_phase = not player1_move_phase
    player2_move_phase = not player2_move_phase
    combat_phase = False
    #chosen_group = None
    chosen_cell = None
    game_map.clear_attacks()
    update_turn_text()
    
def update_turn_text():
    if player1_move_phase:
        instructions.set_instructions("Player 1's turn!")
    if player2_move_phase:
        instructions.set_instructions("Player 2's turn!")

def check_has_moves(player):
    for row in game_map.tiles:
        for cell in row:
            if cell.units["player"] == player and cell.units["moved"] == False :
                return True
    return False
def check_game_over():
    global game_end_setup
    global game_on_phase
    global winner_text
    player1_alive = False
    player2_alive = False
    for row in game_map.tiles:
        for cell in row:
            if cell.units["player"] == 1 and cell.units["count"] > 0:
                player1_alive = True
            if cell.units["player"] == 2 and cell.units["count"] > 0:
                player2_alive = True
            if player1_alive and player2_alive:
                return
    if player1_alive and not player2_alive:
        #TODO player1 victory
        game_end_phase = True
        game_on_phase = False
        winner_text = "Player 1 Wins!"
        game_end_setup = True
    if player2_alive and not player1_alive:
        #TODO player2 victory
        game_end_phase = True
        game_on_phase = False
        winner_text = "Player 2 Wins!"
        game_end_setup = True
        


#Gameplay Loop
#Boolean handlers
running = True
while running:
    #black backdrop
    screen.fill((0,0,0))
    #Set text for player phase
    if initiation_phase:
        instructions.set_instructions("Player 1 place " + str(units_to_place) + " units")
        initiation_phase = False
    if game_end_setup:
        instructions.set_instructions(winner_text)
    #Render all interface by layer
    game_map.render_map(screen)
    game_map.render_moves(screen)   
    game_map.render_units(screen)
    instructions.show_instructions()
    if tutorial_phase:
        tutorial.render_tutorial()
    if unit_selection_phase:
        player1_pool.render_pool(screen)
        player2_pool.render_pool(screen)
    if game_on_phase:
        pass_button.show_button()
        game_map.render_gray(screen)
        if combat_phase:
            game_map.render_attacks(screen)
        check_game_over()
    #allows the game to be exited by clicking the 'x' in the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if tutorial_phase:
                tutorial_phase = False
                unit_selection_phase = True
                player1_selection_phase = True
                continue

            check_for_selection(pos)
            check_for_gameplay(pos)
    pygame.display.update()
    clock.tick(60)

