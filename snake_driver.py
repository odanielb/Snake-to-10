#-------------------------------------------------------------------------------
# File: snake_driver.py
# Name: Bridget O'Daniel
# Username: odanielb
#
# Assignment: FP Final Project
# Purpose: To work with and edit something I've created this year and think about object-oriented program and make improvements.
#
# Acknowledgements: I did not invent the idea of the game Snake: http://conversations.nokia.com/2010/11/25/the-evolution-of-snake/
#
#-------------------------------------------------------------------------------

import Tkinter
import snake_game

game = snake_game.Game()                                                        #Create a Game

while game.on == False:                                                         #Wait until Game is turned on (see method start() and __init__; activated when user presses space bar)
    game.display_instructions()                                                     #Game displays the instructions
game.display.clear()                                                            #Game clears instructions
game.play()                                                                     #Game starts to play!

Tkinter.mainloop()                                                              #Hooray, main loop
