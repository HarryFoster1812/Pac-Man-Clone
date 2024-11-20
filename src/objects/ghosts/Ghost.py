import random
import math
from enum import Enum
from src.objects.pacman import Pacman
from src.gameImage import GameImage
from src.objects.map_objects.moveable import Moveable
from src.objects.map_objects.wall import Wall

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
        self.state = GhostState.SCATTER # the current state of the ghost, 0 = default, 1 = scatter, 2 = fright, 3 = dead
        self.target = [] # the target square that the ghost its trying to get to
        self.direction = [] # [x, y] eg [1, 0] will be right, [0, -1] will be down
        self.next_direction = [] # the next square the ghost will move to
        self.is_dead = False
        self.is_frightened = False
        self.speed = 5.05050508333 # the base pixel movement speed of the ghost  
        self.speed_modifier = 0.5 # this is applied during the different ghost modes
        self.ghost_house_target = []
        self.ouside_ghost_house = [14,14]

        self.pacman = pacman
        self.dot_counter = 0
        self.dot_limit = 0
        self.colour = ""

        self.canvas_position = [start_pos[0], start_pos[1]] # the x and y co-ordinates of pacman
        self.target_position = []
        self.current_cell = [] # the co-ordinates of pacman in the cell
        self.next_cell = [0,0]

        self.tick_count = 0

        self.image=None

        self.dead_image = GameImage("assets/Ghosts/GhostEyes.gif")
        self.frightened_image = GameImage("assets/Ghosts/FrightendGhost.gif")
        self.white_frightened_image = GameImage("assets/Ghosts/WhiteFrightendGhost.gif")

        self.maze = maze

        self.level_info = self.maze.get_level_info(0)

    def tick(self):
        
        if self.state == GhostState.IN_GHOST_HOUSE:
            self.canvas_position [0] += self.direction[0]*self.speed*self.speed_modifier
            self.canvas_position [1] += self.direction[1]*self.speed*self.speed_modifier

            self.calculateCurrentCell()    
            # calculate target position
            self.calculateTargetPos()
            self.calculateNextCell()
        
            next_cell = self.maze.maze[int(self.next_cell[1])][int(self.next_cell[0])]

            if isinstance(next_cell, Wall):
                # snap ghost to the correct placement next to the wall
                self.direction = [component*-1 for component in self.direction]
                self.checkFrameSwitch(True)

            return
        
        elif self.state == GhostState.MOVING_OUT_OF_GHOST_HOUSE:
            #wait until ghost hits wall from in house state
            print("TRYING TO MOVE OUT", self.colour)
            self.calculateCurrentCell()
            self.calculateNextCell()
            next_cell = self.maze.maze[int(self.next_cell[1])][int(self.next_cell[0])]

            if isinstance(next_cell, Wall) and self.canvas_position[0] != 416:
                # calculate which direction will get the ghost to 416
                if (416 - self.canvas_position[0]) > 0:
                    self.direction = [1, 0] # we need to move right
                else:
                    self.direction = [-1, 0] # we need to move left
                self.checkFrameSwitch(True)

            if self.direction == [0, 1] and  self.canvas_position[0] == 416:
                self.direction = [0, -1]

            # move to correct x
            #check if moved to 416 or past (based on direction)
            if self.checkMovedPassed(416, self.direction[0], self.canvas_position[0]):
                self.canvas_position[0] = 416
                self.direction = [0, -1]
                self.checkFrameSwitch(True)

            
            # move to correct y
            if self.direction == [0,-1] and self.checkMovedPassed(436, self.direction[1], self.canvas_position[1]):
                if self.is_frightened:
                    self.changeState(GhostState.FRIGHTENED)
                else:
                    self.changeState(GhostState.CHASE)
                self.direction = [-1, 0]
                self.next_direction = [-1, 0]
                self.canvas_position[1] = 436
                self.checkFrameSwitch(True)
                self.calculateNextCell()

                return
            
            #move ghost
            print("SPEED:", self.speed_modifier)
            print("SPEED:", self.speed)
            self.canvas_position [0] += self.direction[0]*self.speed*self.speed_modifier
            self.canvas_position [1] += self.direction[1]*self.speed*self.speed_modifier
            return
        
        elif self.state == GhostState.MOVING_INTO_GHOST_HOUSE:
            #wait until ghost hits wall from in house state
            self.calculateCurrentCell()
            self.calculateNextCell()
            print("DIRECTION: ",self.direction)
            # move to correct x
            #check if moved to 416 or past (based on direction)
            if self.checkMovedPassed(self.ghost_house_target[1], 1, self.canvas_position[1]):
                print("HAS MOVED PASSED Y",self.canvas_position)
                self.canvas_position[1] = self.ghost_house_target[1]
                # set direction to move x
                if (self.ghost_house_target[0] - self.canvas_position[0]) > 0:
                    self.direction = [1, 0] # we need to move right
                else:
                    self.direction = [-1, 0] # we need to move left
                self.checkFrameSwitch(True)

            
            # move to correct y
            if self.direction[0] != 0 and self.checkMovedPassed(self.ghost_house_target[0], self.direction[0], self.canvas_position[0]):
                print("REACHED TARGET SWITCHING TO MOVING OUT",self.canvas_position)
                self.changeState(GhostState.MOVING_OUT_OF_GHOST_HOUSE)
                self.direction = [0, 1]
                self.next_direction = [0, 1]
                self.checkFrameSwitch(True)
                self.calculateNextCell()
            
            #move ghost
            self.canvas_position [0] += self.direction[0]*self.speed*self.speed_modifier
            self.canvas_position [1] += self.direction[1]*self.speed*self.speed_modifier
            return
        
        if self.state == GhostState.DEAD and self.current_cell == self.target:
            self.changeState(GhostState.MOVING_INTO_GHOST_HOUSE)
            self.direction = [0, 1] # make the ghost move down
            self.canvas_position = [416, 436]
            return

        direction_has_changed = False
        
        self.calculateTarget()
        
        # calculate current cell
        self.calculateCurrentCell()

        # check if current cell is next cell
        if self.current_cell == self.next_cell:
            # assign direction to next_direction
            if self.direction != self.next_direction:
                self.direction = self.next_direction
                direction_has_changed = True
            
            # get out current cell
            temp_current_cell = self.maze.maze[int(self.current_cell[1])][int(self.current_cell[0])]

            # check if we have hit a teleport square
            if isinstance(temp_current_cell, Moveable) and temp_current_cell.is_teleport:
                # get the index of the other teleport square
                index_other_cell = self.maze.getOtherTeleportSquareLocation(temp_current_cell)
                # change co-ordinates
                index_next_square_after_teleport = [index_other_cell[0] + self.next_direction[0], index_other_cell[1]+self.next_direction[1]]  
                self.canvas_position[0] = index_next_square_after_teleport[0]*32 -16
                self.canvas_position[1] = index_next_square_after_teleport[1]*32 -16
                self.calculateCurrentCell()
                self.calculateNextCell()
            
            else:
                self.calculateNextCell()
                temp_next_cell = self.maze.maze[int(self.next_cell[1])][int(self.next_cell[0])]
                # check if next cell is junction
                if isinstance(temp_next_cell, Moveable) and temp_next_cell.is_juction:
                        self.calculateNextDirection(temp_next_cell)
            
        
        #print("GHOST Direction:", self.direction)

        # move ghost in direction
        self.canvas_position [0] += self.direction[0]*self.speed*self.speed_modifier
        self.canvas_position [1] += self.direction[1]*self.speed*self.speed_modifier
        
        #print("GHOST Current position:", self.canvas_position)
        self.calculateCurrentCell()    
        #print("GHOST Current cell:", self.current_cell)
        # calculate target position
        
        self.calculateTargetPos()
        #print("Target Position:", self.target_position)
        #print("Target cell:", self.next_cell, end="\n\n")
        
        next_cell = self.maze.maze[int(self.next_cell[1])][int(self.next_cell[0])]
        
        if isinstance(next_cell, Wall):
            # snap ghost to the correct placement next to the wall
            self.next_cell = self.current_cell
            self.calculateTargetPos()
            self.canvas_position = self.target_position

        else:
            # snap ghost to correct placement
            self.snapPosition()

        # update frame (based on current direction)
        self.checkFrameSwitch(direction_has_changed)

    def setDotLimit(self, limit):
        self.dot_limit = limit

    def incrementDotCounter(self):
        self.dot_counter += 1
        if self.dot_counter >= self.dot_limit:
            self.changeState(GhostState.MOVING_OUT_OF_GHOST_HOUSE)

    def changeState(self, new_state):
        self.state = new_state
        self.next_direction = [component*-1 for component in self.direction]
        match (new_state):
            case GhostState.CHASE: 
                self.speed_modifier = 0.6
                
            case GhostState.SCATTER: 
                self.speed_modifier = 0.6

            case GhostState.FRIGHTENED: 
                self.enableFrightened()
                self.speed_modifier = 0.4
                self.image.switchFrameSet(self.frightened_image.frames)
            
            case GhostState.DEAD:
                self.speed_modifier = 1
                self.disableFrightened()
                self.enableDead()

            case GhostState.MOVING_OUT_OF_GHOST_HOUSE:
                self.disableDead()
    
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

    def checkFrameSwitch(self, direction_has_changed):
        if direction_has_changed:
            if self.is_dead:
                match(self.direction):
                    case [0,1] : 
                        self.updateFrame(self.dead_image.frames)
                        self.image.setFrameStatic(0)
                    case [0,-1]: 
                        self.updateFrame(self.dead_image.frames)
                        self.image.setFrameStatic(1)
                    case [1,0] : 
                        self.updateFrame(self.dead_image.frames)
                        self.image.setFrameStatic(2)
                    case [-1,0]: 
                        self.updateFrame(self.dead_image.frames)
                        self.image.setFrameStatic(3)
                            
            elif self.is_frightened:
                self.updateFrame(self.frightened_image.frames)
            else:
                match(self.direction):
                    case [0,1] : self.updateFrame(self.image.down)
                    case [0,-1]: self.updateFrame(self.image.up)
                    case [1,0] : self.updateFrame(self.image.right)
                    case [-1,0]: self.updateFrame(self.image.left)
                                    
        else:
            self.updateFrame()

    def updateFrame(self, change_frame_set = None):
        self.tick_count += 1
        self.tick_count %= 5
        if change_frame_set is not None:
            self.image.switchFrameSet(change_frame_set)
        
        if self.tick_count == 0:
            self.image.nextFrame()

    def checkMovedPassed(self, target_pos: int, direction: int, current_pos) -> bool:
        
        if current_pos == target_pos:
            return False
        # is is not equal so check if component positive and the target position is behind it
        elif direction > 0 and target_pos < current_pos:
            return True
        
        elif direction < 0 and target_pos > current_pos:
            return True
        
        return False

    def calculateNextDirection(self, junction_cell):
        # if it is then calculate next direction
        decisions = self.calculateValidDecisions(junction_cell, self.state, self.direction)
        
        # in fright mode the ghost make decisions randomly 
        if self.state == GhostState.FRIGHTENED:
            self.next_direction = random.choice(decisions)
        elif len(decisions) > 1: 
            distances = []
            for direction in decisions:
                junction_cell_plus_direction = self.next_cell[:]
                junction_cell_plus_direction[0] += direction[0]
                junction_cell_plus_direction[1] += direction[1]
                distance = self.pythagoras(self.target, junction_cell_plus_direction)
                distances.append(distance)
            # find the shortest one
            shortest_distance = min(distances)
            # chose the index
            decision_index = distances.index(shortest_distance)
            self.next_direction = decisions[decision_index]
        else:
            self.next_direction = decisions[0]

    def calculateValidDecisions(self, junction_cell: Moveable, ghost_state: int, current_direction: list):
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
        for direction in possible_copy:
            # copy next cell
            junction_location = self.next_cell[:]

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
      
    def enableDead(self):
        self.is_dead = True
        self.checkFrameSwitch(True)
        # set target square to outside ghostHouse
        self.target = self.ouside_ghost_house

    def disableDead(self):
        self.is_dead = False
        # change ghost image
        self.checkFrameSwitch(True) # this will change the frame

    def enableFrightened(self):
        self.is_frightened = True
        self.checkFrameSwitch(True)
        # set target square to outside ghostHouse

    def disableFrightened(self):
        self.is_frightened = False
        # change ghost image
        self.checkFrameSwitch(True) # this will change the frame
        # set target square

    def calculateTarget(self): # this is a virtual method
        pass

    def pythagoras(self, pos1: list, pos2:list) -> float:
        a = (pos1[0] - pos2[0])**2
        b = (pos1[1] - pos2[1])**2
        return math.sqrt(a + b) 
    
    def reset(self, level, maze,startpos):
        self.canvas_position = startpos
        self.level_info = self.maze.get_level_info(level)
        self.is_dead = False
        self.is_frightened = False

        if self.dot_counter >= self.dot_limit:
            self.state = GhostState.MOVING_OUT_OF_GHOST_HOUSE
        else:
            self.state = GhostState.IN_GHOST_HOUSE        

        if self.colour == "red": # this is needed since blinky does not have a dot limit
            self.state = GhostState.CHASE


