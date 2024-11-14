# this should house all of the back end logic for the game eg the ghost route planning, all of the entities and perform collision checking and see if the game is over
# house the game files
# create different pac man layouts based off a text file   

from tkinter import *
from src.objects.ghosts import *
import src.objects.pacman 

class Game:
    def __init__(self, canvas) -> None:
        self.isPaused = True
        #self.pacman = Pacman()
        #self.ghosts = [Blinky() , Speedy(), Inky(), Clyde()]
        self.level = 0
        self.score = 0
        self.dotsCounter = 0
        
        pass

    def tick(self):
        pass

    def toggleGame(self):
        pass

    def EventHandler(self, event):
        pass

"""
# Notes while researching:
# Pac man is concidered to be in a tile when his centre point is in the tile. Tile being 8x8 pixels (redundant in tkinter

# ghosts have three modes: chase, scatter and frightened
# in scatter each ghost has a fixed target tile 
# in frightened they do not have a target tile but randomly move at junctions

#at the start of the game they alternate between chase and scatter on a timer
# frightened mode will pause the timer and the ghost will go back to its previous state

# Level 1: 
# Scatter for 7 seconds, then Chase for 20 seconds.
# Scatter for 7 seconds, then Chase for 20 seconds.
# Scatter for 5 seconds, then Chase for 20 seconds.
# Scatter for 5 seconds, then switch to Chase mode permanently

# Level 2-4: 
# Scatter for 7 seconds, then Chase for 20 seconds.
# Scatter for 7 seconds, then Chase for 20 seconds.
# Scatter for 5 seconds, then Chase for 1033 seconds.
# Scatter for 1/60 seconds, then switch to Chase mode permanently

# Level 5+: 
# Scatter for 5 seconds, then Chase for 20 seconds.
# Scatter for 5 seconds, then Chase for 20 seconds.
# Scatter for 5 seconds, then Chase for 1037 seconds.
# Scatter for 1/60 seconds, then switch to Chase mode permanently

# Ghost Algorithm
# Once they reach a new tile they will look ahead and make a decision on what to do next
# Ghost can never reverse their direction 
# The exeption is that when they change modes they are forced to reverse as soon as they enter the next tile
# And the exeption to this exeption is when they leave frightened mode
# Obviously they will pick the path that is the shortest straight line distance
# An exeption to the decision making is in the four center blocks where they can not go upwards (unless chosen randomly or on forced reversed)

# In scatter mode:
# Pink   - Top left
# Red    - Top right
# Yellow - Bottom Left
# Blue   - Bottom right

# Escape from the ghost house
# Red - Spawns ouside the ghost house
# Pink - immediately
# Blue - After 30 dots eaten
# over 1/3 of dots eaten

# In chase mode
# Red - Pac Man Square
# Pink - Four tiles ahead of pac man location (and orientation). Maybe implement the original bug as a feature? (when pac man is facing upwards the target would be 4 tiles up and 4 tiles to the left)
# Blue - Overly complex, Two tiles ahead of pac man then double the vector from Red to this target and that is the assigned tile
# Orange - Again overly complex, Has two active modes, if pac man is farther than 8 tiles away then his target is his scattered target otherwise it is the same as RED


# Need to add cheat codes

"""