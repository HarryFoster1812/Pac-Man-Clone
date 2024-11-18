# this should house all of the back end logic for the game eg the ghost route planning, all of the entities and perform collision checking and see if the game is over
# house the game files
# create different pac man layouts based off a text file   

from tkinter import *
from src.objects.ghosts import *
from src.objects.pacman import Pacman
from src.objects.ghosts import Blinky, Inky, Clyde, Ghost, Pinky
from src.settings import Settings
from src.maze import Maze

class Game:

    level_based_speed = {}

    def __init__(self, canvas: Canvas, settings: Settings) -> None:
        self.isPaused = True
        self.maze = Maze("src/levels/main.txt")
        self.pacman = Pacman([416,816], self.maze)
        self.ghosts = [
            Blinky.Blinky([418, 436], self.maze, self.pacman), 
            Pinky.Pinky  ([416, 528], self.maze, self.pacman), 
            Inky.Inky    ([352, 528], self.maze, self.pacman), 
            Clyde.Clyde  ([480, 528], self.maze, self.pacman)
                       ]
        
        self.next_ghost_to_release = 1
        self.level = 0
        self.reset = False
        self.score = 0
        self.lives = 3
        self.dotsCounter = 0 # after 70 dots bonus will display, and then after 170 another bonus will display
        self.settings = settings

        self.pacman_frame_halt = 0
        pass

    def tick(self):
        if self.pacman_frame_halt > 0: # if pac man eats a dot he is then halted for one frame
            self.pacman_frame_halt -= 1
        
        else:
            self.pacman.tick()
        
        for ghost in self.ghosts:
            ghost.tick()


        pacman_cell_loc = self.pacman.current_cell
        pacman_cell_loc = [int(index) for index in pacman_cell_loc]
        pacman_cell = self.maze.maze[pacman_cell_loc[1]][pacman_cell_loc[0]]
        if pacman_cell.has_dot:
            self.score += 1
            pacman_cell.removeImage()
            self.dotsCounter += 1
            self.ghosts[self.next_ghost_to_release].incrementDotCount
            self.pacman_frame_halt = 1
        
        elif pacman_cell.is_powerup:
            #change states of the ghosts
            # change other stuff
            # activate something else
            pacman_cell.removeImage()
            self.pacman_frame_halt = 3
            pass

    def toggleGame(self):
        # set all of the entities speed modifier to 0
        # stop the animate threads
        if self.isPaused:
            # unpause
            self.isPaused =  not self.isPaused
        else:
            self.isPaused = True
            pass

    def moveCharacters(self):
        pass

    def checkForGhostHouseRelease(self):
        if self.ghosts[self.next_ghost_to_release].state == Ghost.GhostState.IN_GHOST_HOUSE:
            pass

    def checkCollision(self):
        for ghost in self.ghosts: 
            if ghost.current_cell == self.pacman.current_cell:
                match(self.ghost.state):
                    case 0: self.deadPacMan() # default
                    case 1: self.deadPacMan() # scatter
                    case 2: self.ghostDead(ghost) # frightend

    def deadPacMan(self):
        # game pauses
        # pacman changes to dead animation
        # disable controllers
        pass

    def ghostDead(self, ghost:Ghost.Ghost):
        # change ghost to dead state
        # add points
        pass

    def EventHandler(self, event):
        if self.isPaused:
            self.toggleGame()
        
        if event.keysym_num == self.settings.getKey("up_key"): 
            self.pacman.next_direction = [0, -1]

        elif event.keysym_num == self.settings.getKey("down_key"):
            self.pacman.next_direction = [0, 1]
        
        elif event.keysym_num == self.settings.getKey("right_key"):
            self.pacman.next_direction = [1, 0]
        
        elif event.keysym_num == self.settings.getKey("left_key"):
            self.pacman.next_direction = [-1, 0]
        
        elif event.keysym_num == self.settings.getKey("pause_key"):
            self.toggleGame() # pause the game

"""
# Notes while researching:
# Pac man is considered to be in a tile when his centre point is in the tile. Tile being 8x8 pixels (for this the original dimensions are scaled by 4x so each tile is now 32x32

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
# The exception is that when they change modes they are forced to reverse as soon as they enter the next tile
# And the exception to this exception is when they leave frightened mode
# Obviously they will pick the path that is the shortest straight line distance

# In scatter mode:
# Pink   - Top left
# Red    - Top right
# Orange - Bottom Left
# Blue   - Bottom right

# Escape from the ghost house
# Red - Spawns outside the ghost house
# Pink - immediately
# Blue - After 30 dots eaten
# over 1/3 of dots eaten

# on a life lost the dot counter is set to global and reset as follows
# Pink   - 7
# Cyan - 17
# Orange - 32

# In chase mode
# Red - Pac Man Square
# Pink - Four tiles ahead of pac man location (and orientation). Maybe implement the original bug as a feature? (when pac man is facing upwards the target would be 4 tiles up and 4 tiles to the left)
# Blue - Overly complex, Two tiles ahead of pac man then double the vector from Red to this target and that is the assigned tile
# Orange - Again overly complex, Has two active modes, if pac man is farther than 8 tiles away then his target is his scattered target otherwise it is the same as RED


# This is for the ghost house force leave The game begins with an initial timer limit of four seconds, but lowers to it to three seconds starting with level five.

# Need to add cheat codes

"""