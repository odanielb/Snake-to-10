#-------------------------------------------------------------------------------
# File: snake_classes.py
# Name: Bridget O'Daniel
# Username: odanielb
#
# Assignment: FP Final Project
# Purpose: To work with and edit something I've created this year and think about object-oriented program and make improvements.
#
# Acknowledgements: The exit method here: http://docs.python.org/2/library/sys.html#sys.exit
# Also, I did not invent the idea of the game Snake: http://conversations.nokia.com/2010/11/25/the-evolution-of-snake/
#
# Errors: Displays an error when you quit by pressing q. Only does so because the program moves by timer, rather than waiting for key presses,
# meaning that once the user presses quit, it will sometimes have already done something that is impossible once the window closes. I could find
# no way to correct this problem, but all other ways of quitting (by running into something or winning) quit cleanly. Also, speed could not increase
# steadily because processing time slowed down the snake with each added tail, meaning the later tails are closer to the beginning tail in speed.
#
#-------------------------------------------------------------------------------

import turtle
import random
import Tkinter
import sys
import time

##### CLASSES ##################################################################

class Game():
    """A class to create a game of snake using the class Snake. This class can be used to give a Snake an environment to be in
    (500x500 window) and prompt user interactivity. Includes Game controls, instructions for a Game of snake and methods to
    monitor score, food, speed, and when the Game is won or lost."""

    def __init__(self):

        turtle.setup(500,500)                                                   #Change screensize for easy reference
        self.wn = turtle.Screen()                                               #Sets up Game's screen
        self.wn.bgcolor("black")

        self.on = False                                                         #Game has not yet started
        self.score = 0                                                          #Game score

        self.snake = Snake()                                                    #Creates the Snake that Game will use

        self.food = turtle.Turtle()                                             #Game creates its food turtle
        self.initialize_food()                                                  #And initializes its values

        self.display = turtle.Turtle()                                          #Game creates a turtle for written instructions, scores, etc.
        self.display.hideturtle()
        self.display.up()

        #Links keys to their designated functions
        self.wn.onkey(self.up, "Up")                                            #Game sets controls
        self.wn.onkey(self.down, "Down")
        self.wn.onkey(self.left, "Left")
        self.wn.onkey(self.right, "Right")
        self.wn.onkey(self.lose, "q")
        self.wn.onkey(self.start, " ")

        self.wn.listen()                                                        #Game's window listens for key presses

    def start(self):
        """Game changes its state to on from the initial intro screen (off)."""
        self.on = True

    def play(self):
        """The Game plays. This method controls what should happen each turn: checks if the Snake has hit anything, if it's eaten the food,
        moves the Snake forward, and checks if the Game is over or not. If Game isn't over, the Game calls this method again for the next turn."""
        is_game_over = self.snake.is_hit()                                      #Checks if Snake has hit walls/itself, stores in is_game_over
        self.check_food()                                                       #Checks if Snake has eaten food; makes necessary changes if so, including new food and new tails
        self.snake.forward()                                                    #Moves the Snake forward
        if is_game_over == True:                                                    #If the Snake did hit something...
            self.lose()                                                                 #Game over
        elif self.score >= 10:                                                      #If the Snake has eaten 10 food items...
            self.win()                                                                  #Game won!
        else:                                                                       #Otherwise...
            self.wn.ontimer(self.play(), 1)                                             #On the timer, Game calls play again

    ##### FOOD AND SPEED MONITORING METHODS ####################################

    def initialize_food(self):
        """The Game resets its food turtle to a new random location, thereby creating a new food item for the Snake to get."""
        self.food.ht()                                                          #Hides food
        self.food.up()
        self.food.shape("square")                                               #Food is for squares
        self.food.color("light green")
        self.food.setpos(random.randrange(-230,230), random.randrange(-230,230))#Puts food in a random location on the screen
        self.food.st()


    def check_food(self):
        """If the Game's Snake has eaten food, adds it to total food eaten, adds a tail to the Snake, and resets the food turtle to a new location."""
        if self.snake.has_eaten_food(self.food) == True:                        #If the game's Snake has eaten food,
            self.score += 1                                                         #Add it to the amount eaten
            self.display.clear()                                                    #Clears display
            self.display_score()                                                    #Displays new total
            self.snake.add_tail()                                                   #Adds new tail to Snake
            self.update_Snake_speed()                                               #Makes the Snake faster
            self.initialize_food()                                                  #Puts food in new location


    def update_Snake_speed(self):
        """Sets the Game's Snake to the appropriate speed based on the current score."""
        foodvsSpeed = {0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8, 8:9, 9:10, 10:0} #Each # of food paired with appropriate speed, so that they can be matched below.
        self.snake.speed = foodvsSpeed[self.score]

    ##### GAME CONTROLS / KEY PRESS METHODS ####################################

    def up(self):
        """Changes Snake direction to up."""
        self.snake.head.setheading(90)

    def down(self):
        """Changes Snake direction to down."""
        self.snake.head.setheading(270)

    def left(self):
        """Changes Snake direction to left."""
        self.snake.head.setheading(180)

    def right(self):
        """Changes Snake direction to right."""
        self.snake.head.setheading(0)

    def Quit(self):
        """Quits the program by closing window and then exiting using sys."""
        self.wn.bye()
        sys.exit()

    ########### GAME DISPLAY METHODS ###########################################

    def display_instructions(self):
        """The Game displays the instructions on screen."""
        self.display.color("white")
        self.display.setpos(0,170)
        self.display.write("Play snake!",move=False,align='center',font=("Arial",30,("bold","normal")))
        self.display.setpos(0,140)
        self.display.write("Collect food and don't hit walls or your tail.",move=False,align='center',font=("Arial",12,("bold","normal")))
        self.display.setpos(0,100)
        self.display.write("Get 10 food items to win!",move=False,align='center',font=("Arial",12,("bold","normal")))
        self.display.setpos(0,-100)
        self.display.write('Press the space bar to begin!',move=False,align='center',font=("Arial",12,("bold","normal")))
        self.display.setpos(0,-140)
        self.display.write('Use arrow keys to change direction, press "q" to quit.',move=False,align='center',font=("Arial",10,("bold","normal")))

    def display_score(self):
        """The Game displays the amount of food eaten in the window."""
        self.display.setpos(-230,-230)
        self.display.write('Food eaten: '+str(self.score),move=False,align='left',font=("Arial",12,("bold","normal")))

    def display_lose(self):
        """The Game displays GAME OVER."""
        self.display.clear()
        self.display.setpos(0,0)
        self.display.write('GAME OVER',move=False,align='center',font=("Arial",50,("bold","normal")))

    def display_win(self):
        """The Game displays YOU WIN!"""
        self.display.clear()
        self.display.setpos(0,0)
        self.display.write('YOU WIN!',move=False,align='center',font=("Arial",50,("bold","normal")))

    ######### WIN OR LOSE METHODS ##############################################

    def win(self):
        """Game won! Displays game won and quits."""
        self.display_win()
        time.sleep(2)
        self.Quit()

    def lose(self):
        """Game over! Displays game over and quits."""
        self.display_lose()
        time.sleep(2)
        self.Quit()


################################################################################


class Snake():
    """The class Snake is designed for use with the class Game and creates a Snake that is a collection of Turtles
    that follow each other in a line. Each Snake starts with only a "head" Turtle and may have "tail" Turtles
    added to its attribute tails (a list). Has functionality to test whether Snake has run into its tails, eaten
    food, or escaped the bounds of the window. The Snake is designed to move forward 20 pixels
    at a time in a 500x500 Turtle window."""

    def __init__(self):

        self.head = turtle.Turtle()
        self.head.shapesize(2,1,1)                                              #Makes it a bit wider than a normal arrow shape
        self.head.color("hot pink")                                             #Snake head is hot pink, also leaves a fun hot pink trail
        self.speed = 1
        self.head.speed(self.speed)

        self.tails = []

    ##### COLLISION METHODS ####################################################

    def is_hit(self):
        """Checks if Snake has hit anything that would result in game over. Returns True or False."""
        hit = self.has_hit_edges()                                              #Calls to see if Snake has hit edges
        if hit == False:                                                        #If not...
            hit = self.has_hit_tail()                                               #Has it hit its tails?
        return hit                                                              #Returns whether it has hit anything or not


    def has_hit_edges(self):
        """Checks if Snake has hit the edges of the window/gone offscreen. Returns True or False."""
        if self.head.xcor() >= 250 or self.head.xcor() <=-250:      #If Snake's x coordinates show it's offscreen
            return True                                                 #Return True
        elif self.head.ycor() >= 250 or self.head.ycor() <=-250:    #If Snake's y coordinates show it's offscreen
            return True                                                 #Return True
        else:
            return False                                            #Otherwise, return False


    def has_hit_tail(self):
        """Checks if snake has hit any of its tails. Returns True or False."""
        xdistance = 0
        ydistance = 0
        for t in self.tails:                                             #For each of Snake's tails...
            xdistance = self.head.xcor() - t.xcor()                         #Find the distance between the head and the tail
            ydistance = self.head.ycor() - t.ycor()
            if abs(xdistance) <= 15 and abs(ydistance) <= 15:           #If the distance is too close (touching)
                return True                                                 #Return True
        return False                                                    #Else return False


    def has_eaten_food(self, food):
        """Checks if the game's Snake and the food turtle have overlapped--meaning that the snake ate the food. Returns True or False."""
        xdistance = self.head.xcor() - food.xcor()                                      #Finds distance between the X values of the snake and the food
        ydistance = self.head.ycor() - food.ycor()                                      #Finds the distance between the Y values of the snake and the food
        if abs(xdistance) <= 20 and abs(ydistance) <= 20:                           #If those distances are less than 20 pixels in either direction...
            return True                                                                 #It has been eaten, return True
        else:
            return False                                                                #Otherwise, it has not been eaten, return False


    ##### UPDATING/CHANGING SNAKE: POSITION OR SIZE METHODS ####################

    def add_tail(self):
        """Adds a tail (a Turtle object) to the Snake."""
        tail = turtle.Turtle()
        tail.up()
        tail.color("plum")
        tail.shape("circle")
        tX = 0                  #Stores x of new tail
        tY = 0                  #Stores y of new tail

        #Set of if statements tells where to place the new tail relative to the position of the last tail (so that they are lined up)
        if len(self.tails) == 0:            #If the Snake has previously not had any tails
            if self.head.heading() == 90:       #If the Snake's head was facing up...
                tX = self.head.xcor()               #Give the new tail the same x coordinate
                tY = self.head.ycor() - 20          #But put it 20 spaces below it
            if self.head.heading() == 270:      #(And so on)
                tX = self.head.xcor()
                tY = self.head.ycor() + 20
            if self.head.heading() == 180:
                tX = self.head.xcor() + 20
                tY = self.head.ycor()
            if self.head.heading() == 0:
                tX = self.head.xcor() - 20
                tY = self.head.ycor()
        else:                                                   #If the snake has at least one tail already
            if self.tails[len(self.tails)-1].heading() == 90:       #If the tail before the new one was facing up...
                tX = self.tails[len(self.tails)-1].xcor()               #Give the new tail the same x coordinate
                tY = self.tails[len(self.tails)-1].ycor() - 20          #But put it 20 spaces below it
            if self.tails[len(self.tails)-1].heading() == 270:      #(And so on)
                tX = self.tails[len(self.tails)-1].xcor()
                tY = self.tails[len(self.tails)-1].ycor() + 20
            if self.tails[len(self.tails)-1].heading() == 180:
                tX = self.tails[len(self.tails)-1].xcor() + 20
                tY = self.tails[len(self.tails)-1].ycor()
            if self.tails[len(self.tails)-1].heading() == 0:
                tX = self.tails[len(self.tails)-1].xcor() - 20
                tY = self.tails[len(self.tails)-1].ycor()

        tail.setpos(tX,tY)  #Set this as the position of the tail
        self.tails.append(tail)  #Add it to the list


    def forward(self):
        """Moves the entire Snake forward by 20."""
        headX = self.head.xcor()                                       #Saves Snake's x coordinate before it moves
        headY = self.head.ycor()                                       #Saves Snake's y coordinate before it moves
        self.head.speed = self.speed
        self.head.forward(20)                                           #Moves Snake forward
        self.update_tails(headX, headY)                                 #Moves Snake's tails forward


    def update_tails(self, headX, headY):
        """Moves each tail forward to the position the tail in front of it last had. Provided coordinates are used to move the first tail."""
        new_posList = []                            #Stores updated set of positions for each tail
        tX = 0                                      #Stores current tail's new x coordinate
        tY = 0                                      #Stores current tail's new y coordinate
        if len(self.tails) != 0:                          #If the snake has a tail...

            for t in range(len(self.tails)):               #For each of the Snake's tails...
                if t == 0:                                  #If it's the first tail,
                    (tX, tY) = (headX, headY)                                #Make its coordinates the same as the snake head's old ones
                else:                                       #Otherwise,
                    tX = self.tails[t-1].xcor()                        #Make its coordinates the same as the tail in front of its old ones
                    tY = self.tails[t-1].ycor()
                new_posList.append( (tX, tY) )            #Adds the new set of coordinates to a list

            for t in range(len(self.tails)):               #For each of the Snake's tails...
                self.tails[t].setpos(new_posList[t])           #Set its position to the corresponding updated position in new_posList
                self.tails[t].speed(self.speed)                 #Set its speed to the current speed of the Snake

    #End of classes

