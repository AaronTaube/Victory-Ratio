# Victory Ratio User's Guide

Victory Ratio is a strategy game written in python. The following .py files are included:
**main.py -** contains the core gameplay loop and handles the state of the game. It is also the file that calls all the visual elements from other files and classes. This is the file that the user will run to play the game.
**board.py -** contains the Map class that renders the game itself, as well as the necessary classes for the unit selection pool in the beginning phase of the game.
**tiles.py -** contains the individual tile class and subclasses that store the information needed to play the game
**gameplay_UI.py -** contains the GUI elements and texts such as the instructional text and pass button.
 Additionally, folders containing all the necessary image files are included in source.
 
 ## Video Demonstration
 Recorded presentation of the game in action is available at the following link: https://youtu.be/bQQ6Z5LisTM.
 
 ## Requirements
 * python 3.7
 * pygame 1.9.6
 * numpy 1.19.1
 
 ## Installation
 To install victory ratio, the user must have an IDE and python 3.7 installed.
 Clone the repository to your computer, and then install the two necessary packages, pygame and numpy.
 * To install pygame use "pip install pygame"
 * To install numpy use "pip install numpy"
 
 ## Gameplay Breakdown
 Victory Ratio is intended to be played by two people at one computer.
 Once the game is launched, a brief tutorial is displayed. Click anywhere to move on.
 ![Tutorial Image](/Images/Buttons/Tutorial.png)
 ### Unit Selection phase begins
 1. Player one will click on a unit from their pool on the right side of the screen. They can then place 9 units of any quantity of each in tiles on their side of the field.
 2. Player two will then do the same.
 3. This continues until no units remain to place. 
 
 ### Player one will then have first move.
 1. A player can select any unit that has not been grayed out.
 2. They then can choose to move the unit to a space within 3 spaces of the unit, or click pass.
 3. After movement, the player can see red tiles indicating attack range. They can either attack an enemy unit in those tiles, or hit pass.
 4. If an attack is issued, the attacking unit will swing first. The remaining defending units will then attack back.
 5. After attacking or passing, a unit is grayed out until the end of the round.
 
 Then player two goes through the above.
 If one player has no units still available to move, then the player who still has units available will continue until all units have moved.
 When neither player has moves remaining, the round resets and all units may be moved again.
 This continues until one player has no units remaining on the field, and the still standing player is declared the victor.
  
 ### Terrain effects are at play in this game. 
 * Green tiles represent a plain. They have no impact on the player. 
 * Green and brown tiles indicate a forest, and a unit that is defending in this tile has a strength increase, so are less likely to die here. 
 * Blue tiles indicate water, and so they are not tiles that the player can move past or into.
 

 ### The game has a weapons triangle system. What this means is each soldier has a weapon they are strong against and a weapon they are weak against.
 Combat calculation is as follows.
 * All units have 100 Strength each.
 * If a unit has type advantage, they have +50 strength.
 * The type advantages are as follows:
 * Sword is strong against Axe
 * Axe is strong against Spear
 * Spear is strong against Sword
 * If a unit is defending in a forest tile, they have an additional 25 strength.
 * For each unit attacking in a group, their strength and the unit they are attacking's strength are added together. A number is then rolled between 0 and their combined strength.
 * If the number rolled is less than the attacker's strength, then that attacker has successfully destroyed one unit.
 * After being attacked, defenders then perform the attack calculation back against their attackers, but only with the number of units they have left.
 
 ## Known Issues:
 * Sometimes when there is an uneven number of unit groups between player 1 and 2, the turn order can pass incorrectly.
 * If the user changes units they are placing, such as from axe to spear, then tries to place the spear holder in a place with an axe unit, the spear count will decrease and additional axe units will be placed instead. The user should be blocked from placing a unit there.
 
