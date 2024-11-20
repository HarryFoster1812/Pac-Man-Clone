# this should house all of the back end logic for the game eg the ghost route planning, all of the entities and perform collision checking and see if the game is over
# house the game files
# create different pac man layouts based off a text file   
from src.objects.ghosts.ghost_state import GhostState 
from src.objects.pacman import Pacman
from src.objects.ghosts import Blinky, Inky, Clyde, Ghost, Pinky
from src.settings import Settings
from src.maze import Maze
from src.player import Player

class Game:

    def __init__(self, settings: Settings, player: Player) -> None:
        self.isPaused = True # this is when the user pauses the game
        self.info_pause = False # this is when the game is paused to show the score or when pac man is dead
        self.maze = Maze("src/levels/main.txt")
        
        self.frightened_mode = False

        self.dotsCounter = 0
        self.settings = settings
        self.level_info = self.maze.get_level_info(0)
        self.mode_pointer = 0
        self.pacman_frame_halt = 0
        self.saved_frame_counter = 0 # when ever we switch to fright mode the frame counter is overridden so we need to store the frame count elsewhere
        self.frame_counter = 0
        
        self.pacman = Pacman([416,816], self.maze)
        self.pacman.speed_modifier = self.level_info["pacmanSpeed"]
        self.ghosts = [
            Blinky.Blinky([416, 436], self.maze, self.pacman), 
            Pinky.Pinky  ([416, 528], self.maze, self.pacman), 
            None, # we set this to none since for inky we need blinky to be created 
            Clyde.Clyde  ([480, 528], self.maze, self.pacman)
                       ]
        self.ghosts[2] = Inky.Inky([352, 528], self.maze, self.pacman, self.ghosts[0])

        self.ghosts[2].setDotLimit(30)
        self.ghosts[3].setDotLimit(60)

        self.player = player

        self.ghost_eaten_multiplier = 1 # if pac man eats a ghost in succession he multiplies its wirth by 2* as many ghosts eaten 

        self.next_ghost_to_release = 1
        self.level = 0
        self.lives = 3

        

    def next_level(self):
        self.maze.reset()
        self.level += 1
        self.dotsCounter = 0
        self.level_info = self.maze.get_level_info(self.level)
        self.pacman.reset(self.level, self.maze)
        # set ghost dot limit
        ghost_startpos = [[416, 436],
                          [416, 528],
                          [352, 528],
                          [480, 528]
                          ]
        for i, ghost in enumerate(self.ghosts):
            ghost.reset(self.level, self.maze, ghost_startpos[i])
        

    def check_fright_mode(self):
        if self.frame_counter == self.level_info["frightFlashStart"]:
            for ghost in self.ghosts:
                if ghost.is_frightened:
                    ghost.image.switchFrameSet(ghost.white_frightened_image.frames)
        elif self.frame_counter == self.level_info["frightFrames"]:
            #restore frame counter
            self.frame_counter = self.saved_frame_counter
            # disable fright mode
            self.change_all_ghost_state(self.level_info["modes"][self.mode_pointer][0])
            # change pac man speed
            self.pacman.speed_modifier = self.level_info["pacmanSpeed"]
            self.frightened_mode = False
            
    def check_mode_switch(self):
        frame_target = self.level_info["modes"][self.mode_pointer][1]
        if self.frame_counter >= frame_target:
            self.mode_pointer += 1
            self.change_all_ghost_state(self.level_info["modes"][self.mode_pointer][0])

    def tick(self):
        
        self.frame_counter += 1
        if self.frightened_mode: # check is frightened mode should end
            self.check_fright_mode()
        else:
            self.check_mode_switch()

        if self.pacman_frame_halt > 0: # if pac man eats a dot he is then halted for one frame
            self.pacman_frame_halt -= 1

        else:
            self.pacman.tick()


        for ghost in self.ghosts:
            ghost.tick()


        self.checkCollisions()

    def toggleGame(self):
        # set all of the entities speed modifier to 0
        # stop the animate threads
        if self.isPaused:
            # unpause
            self.isPaused =  not self.isPaused
        else:
            self.isPaused = True

    def checkForGhostHouseRelease(self):
        if self.next_ghost_to_release > 3:
            return
        
        self.ghosts[self.next_ghost_to_release].incrementDotCounter()

        if self.ghosts[self.next_ghost_to_release].state != Ghost.GhostState.IN_GHOST_HOUSE:
            self.next_ghost_to_release += 1

    def checkCollisions(self):
        
        
        pacman_cell_loc = self.pacman.current_cell
        pacman_cell_loc = [int(index) for index in pacman_cell_loc]
        pacman_cell = self.maze.maze[pacman_cell_loc[1]][pacman_cell_loc[0]]

        if pacman_cell.has_dot:
            self.player.score += pacman_cell.points
            pacman_cell.removeImage()

            self.dotsCounter += 1            
            self.checkForGhostHouseRelease()
            self.pacman_frame_halt = 1

        elif pacman_cell.is_powerup:
            #change states of the ghosts
            self.player.score += pacman_cell.points
            self.dotsCounter += 1       
            
            self.ghost_eaten_multiplier = 1   
            self.saved_frame_counter = self.frame_counter
            self.frame_counter = 0
            self.frightened_mode = True

            self.change_all_ghost_state(GhostState.FRIGHTENED)

            pacman_cell.removeImage()
            self.pacman_frame_halt = 3

        for ghost in self.ghosts: 
            if ghost.current_cell == self.pacman.current_cell:
                
                if ghost.is_frightened:
                    self.ghostDead(ghost)
                else:
                    match(ghost.state):
                        case Ghost.GhostState.FRIGHTENED: self.ghostDead(ghost) # frightend
                        case Ghost.GhostState.DEAD: pass
                        case Ghost.GhostState.MOVING_INTO_GHOST_HOUSE: pass
                        case _: self.deadPacMan()    

    def deadPacMan(self):
        # game pauses
        self.info_pause = True
        print("PACMAN DEAD")
        # pacman changes to dead animation
        # disable controllers


    def dead_reset(self): # just pac man and the ghosts reset
        self.pacman.reset(self.level, self.maze)
        self.ghost_reset()
        

    def ghost_reset(self):
        ghost_startpos = [[416, 436],
                          [416, 528],
                          [352, 528],
                          [480, 528]
                          ]
        for i, ghost in enumerate(self.ghosts):
            ghost.reset(self.level, self.maze, ghost_startpos[i])

    def ghostDead(self, ghost:Ghost.Ghost):
        print("GHOST DEAD")
        # change ghost to dead state
        ghost.changeState(Ghost.GhostState.DEAD)
        # add points
        self.player.score += 200 * self.ghost_eaten_multiplier
        self.ghost_eaten_multiplier *= 2

    def change_all_ghost_state(self, state):
        if state == GhostState.FRIGHTENED:
            self.pacman.speed_modifier = self.level_info["frightPacManSpeed"]
            for ghost in self.ghosts:
                if ghost.state == GhostState.CHASE or ghost.state == GhostState.SCATTER:
                    ghost.changeState(state)
                
                elif ghost.state == GhostState.DEAD:
                    pass
                
                else:
                    ghost.enableFrightened()

        else:
            for ghost in self.ghosts:
                match(ghost.state):
                    case GhostState.FRIGHTENED:
                        ghost.changeState(state)
                        ghost.disableFrightened()
                    
                    case GhostState.CHASE:
                        ghost.changeState(state)
                    
                    case GhostState.SCATTER:
                        ghost.changeState(state)
                    
                    case GhostState.DEAD:
                        pass

                    case _:
                        ghost.disableFrightened()

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

        elif event.keysym_num in self.settings.cheat_keys:
            pass

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


DONE (From the list being created way too late in the project)
Fix dead ghosts not moving back to ghost house DONE
Add ghost moving back into ghost house
Add teleport squares
NEED TO ADD A PAUSE SCREEN
Add game timer to allow the switching of States
Add level based values (speed modifiers)

TO DO:

Add save / load game
Add death
Add reset level / redraw after death
Add game over / save score
Populate the boss screen
Make it look nicer
Add consumeables

Need to add cheat codes
add another life
reset the ghosts
release all of the ghosts
"""