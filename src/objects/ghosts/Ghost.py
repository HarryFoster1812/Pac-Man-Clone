import math
from src.objects.pacman import Pacman
from src.gameImage import GameImage
from src.objects.map_objects.moveable import Moveable
from src.objects.map_objects.wall import Wall
from enum import Enum
import random

class GhostState(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2
    DEAD = 3
    IN_GHOST_HOUSE = 4
    MOVING_INTO_GHOST_HOUSE = 5
    MOVING_OUT_OF_GHOST_HOUSE = 6

class Ghost:


    def __init__(self, start_pos, maze, pacman: Pacman) -> None:
        self.state = GhostState.CHASE # the current state of the ghost, 0 = default, 1 = scatter, 2 = fright, 3 = dead
        self.target = [] # the target square that the ghost its trying to get to
        self.direction = [] # [x, y] eg [1, 0] will be right, [0, -1] will be down
        self.next_direction = [] # the next square the ghost will move to
        self.is_in_house = True # this is applicable when the ghost is eaten or is in the ghost house
        self.leaving_house = False
        self.is_dead = False
        self.speed = 5.05050508333 # the base pixel movement speed of the ghost  
        self.speed_modifier = 0.3 # this is applied during the different ghost modes

        self.pacman = pacman

        self.canvas_position = [start_pos[0], start_pos[1]] # the x and y co-ordinates of pacman
        self.target_position = []
        self.current_cell = [] # the co-ordinates of pacman in the cell
        self.next_cell = [0,0]
        
        self.tick_count = 0

        self.dead_image = GameImage("assets/Ghosts/GhostEyes.gif")
        self.frightend_image = GameImage("assets/Ghosts/FrightendGhost.gif")
        self.white_frightend_image = GameImage("assets/Ghosts/WhiteFrightendGhost.gif")

        self.maze = maze

    def tick(self):
        direction_has_changed = False
        
        self.calculateTarget()
        
        # calculate current cell
        self.calculateCurrentCell()    

        # check if current cell is next cell and center is past cell center (based on direction)
        if self.current_cell == self.next_cell:
            # assign direction to next_direction
            direction_has_changed = True if self.direction != self.next_direction else False 
            self.direction = self.next_direction
            # if it is then recalculate next cell
            self.calculateNextCell()
            temp_next_cell = self.maze.maze[int(self.next_cell[1])][int(self.next_cell[0])]
           
            # check if next cell is junction
            if isinstance(temp_next_cell, Moveable) and temp_next_cell.is_juction:
                    self.calculateNextDirection(temp_next_cell)
        
        print("Direction:", self.direction)

        # move ghost in direction
        self.canvas_position [0] += self.direction[0]*self.speed*self.speed_modifier
        self.canvas_position [1] += self.direction[1]*self.speed*self.speed_modifier
        # snap ghost to correct placement

        
        print("BLINKY Current position:", self.canvas_position)
        self.calculateCurrentCell()    
        print("BLINKY Current cell:", self.current_cell)
        # calcualte target position
        
        self.calculateTargetPos()
        print("Target Position:", self.target_position)
        print("Target cell:", self.next_cell, end="\n\n")
        
        next_cell = self.maze.maze[int(self.next_cell[1])][int(self.next_cell[0])]
        
        if isinstance(next_cell, Wall):
            self.next_cell = self.current_cell
            self.calculateTargetPos()
            self.canvas_position = self.target_position

        else:
            self.snapPosition()

        # check if we can change the direction of the ghost
        direction_has_changed = self.checkChangeDirection()

        # update frame (based on current direction)
        self.checkFrameSwitch(direction_has_changed)


    def changeState(self, new_state):

        self.next_direction = [component*-1 for component in self.direction]
        match (new_state):
            case GhostState.CHASE: 
                self.speed_modifier = 0.6
                
            case GhostState.SCATTER: 
                self.speed_modifier = 0.6

            case GhostState.FRIGHTENED: 
                self.speed_modifier = 0.4

    
    def calculateNextCell(self):
        self.next_cell[0] = self.current_cell[0]
        self.next_cell[1] = self.current_cell[1]

        self.next_cell[0] += self.direction[0]
        self.next_cell[1] += self.direction[1]

    def calculateTargetPos(self):
        x = self.next_cell[0]*32 -16
        y = self.next_cell[1]*32 -16
        self.target_position = [x,y]

    def snapPosition(self):
        next_position = [
                self.canvas_position[0] + self.speed * self.speed_modifier * self.direction[0],
                self.canvas_position[1] + self.speed * self.speed_modifier * self.direction[1]
            ]
        
        match(self.direction):
            case [0,1]:  next_position[0] = self.target_position[0] # moving in the y direction so snap to the middle of the x cell
            case [0,-1]: next_position[0] = self.target_position[0] # moving in the y direction so snap to the middle of the x cell
            case [1,0]:  next_position[1] = self.target_position[1] # moving in the x direction so snap to the middle of the y cell
            case [-1,0]: next_position[1] = self.target_position[1] # moving in the x direction so snap to the middle of the y cell
        
        if self.direction != [0, 0]:  # Only snap if we're moving
            self.canvas_position = next_position

    def checkChangeDirection(self) -> bool:
        if self.direction != self.next_direction:
            # check if we can change direction 
            current_cell_x = self.current_cell[0]
            current_cell_y = self.current_cell[1]

            current_cell_x += self.next_direction[0]
            current_cell_y += self.next_direction[1]

            next_cell = self.maze.maze[int(current_cell_y)][int(current_cell_x)]

            if isinstance(next_cell, Wall):
                return False
                    
        # the user has not entered a new direction to travel in
        else:
            return False

    def checkFrameSwitch(self, direction_has_changed):
        if direction_has_changed:
            match(self.is_dead):
                case False :
                    match(self.direction):
                        case [0,1] : self.updateFrame(self.image.down)
                        case [0,-1]: self.updateFrame(self.image.up)
                        case [1,0] : self.updateFrame(self.image.right)
                        case [-1,0]: self.updateFrame(self.image.left)
                
                case True:
                    match(self.direction):
                        case [0,1] : self.updateFrame(self.dead_image.frames)
                        case [0,-1]: self.updateFrame(self.dead_image.frames)
                        case [1,0] : self.updateFrame(self.dead_image.frames)
                        case [-1,0]: self.image.setFrameStatic()
        else:
            self.updateFrame()

    def updateFrame(self, change_frame_set = None):
        self.tick_count += 1
        self.tick_count %= 5
        if change_frame_set != None:
            self.image.switchFrameSet(change_frame_set)
        
        if self.tick_count == 0:
            self.image.nextFrame()

    def calculateNextDirection(self, juction_cell):
        # if it is then calcualte next direction
        decisions = self.calcualteValidDecisions(juction_cell, self.state, self.direction)
        
        # in fright mode the ghost make decisions randomly 
        if self.state == GhostState.FRIGHTENED:
            self.next_direction = random.choice(decisions)
        elif len(decisions) > 1: 
            distances = []
            for direction in decisions:
                junction_cell_plus_direction = self.next_cell[:]
                junction_cell_plus_direction[0] += direction[0]
                junction_cell_plus_direction[1] += direction[1]
                distance = Ghost.pythagoras(self.target, junction_cell_plus_direction)
                distances.append(distance)
            # find the shortest one
            shortest_distance = min(distances)
            # chose the index
            decision_index = distances.index(shortest_distance)
            self.next_direction = decisions[decision_index]
        else:
            self.next_direction = decisions[0]

    def calcualteValidDecisions(self, junction_cell: Moveable, ghost_state: int, current_direction: list):
        possible = [[1,0], [-1, 0], [0, 1], [0, -1]]
        opposite_direction = [direction*-1 for direction in current_direction]
        possible.remove(opposite_direction) # the ghost can not move in the opposite direction 
        
        # check if the juction allows ghost to move up
        # if it doesnt the only exception to this is if the ghost is in frightend mode
        #is we are moving down then we have already removed the possibility from the list
        if not junction_cell.can_move_up and ghost_state != GhostState.FRIGHTENED and current_direction != [0,1]: 
            possible.remove([0,-1]) # the ghost can not move up

        # copy the array as we are removing things from the original so it will mess up indexes
        possible_copy = possible[:]

        # loop over each direction get the cell and check if its traversable
        for i in range(len(possible_copy)):
            
            # copy next cell
            junction_location = self.next_cell[:]
            
            direction = possible_copy[i]

            junction_location[0] += direction[0]
            junction_location[1] += direction[1]
            # convert them to ints so we can use them as indicies
            junction_location[0] = int(junction_location[0])
            junction_location[1] = int(junction_location[1])

            # get the cell from the maze
            cell_next_to_juction = self.maze.maze[junction_location[1]][junction_location[0]]
            
            # check if is not traversable
            if not isinstance(cell_next_to_juction, Moveable):
                possible.remove(direction)

        return possible

    def calculateCurrentCell(self):
        x = (self.canvas_position[0] + 32)//32
        y = (self.canvas_position[1] + 32)//32
        
        self.current_cell = [x,y]

    def toggleDead(self):
        if self.is_dead:
            self.is_dead = False
            # change ghost image
            self.checkFrameSwitch(True) # this will change the frame
            # set target square

        else:
            self.is_dead = True
            self.state = 3
            self.checkFrameSwitch(True)
            # set target square to outside ghostHouse

    def calculateTarget(self):
        pass

    def pythagoras(pos1: list, pos2:list) -> float:
        a = (pos1[0] - pos2[0])**2
        b = (pos1[1] - pos2[1])**2
        return math.sqrt(a + b) 