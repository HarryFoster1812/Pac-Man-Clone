from src.objects.ghosts.Ghost import Ghost
from src.gameImage import GameImage
from src.objects.map_objects.wall import Wall
from src.objects.map_objects.moveable import Moveable
from src.maze import Maze
import random

# Red
class Blinky(Ghost):
    def __init__(self, start_pos, maze, pacman):
        super(Blinky, self).__init__(start_pos, maze, pacman)
        self.image = GameImage("assets/Ghosts/Red/Red", load_ghost_variations=True) # need to fill this out
        self.scatter_cell = [25,0]
        self.colour = "red"
        self.direction = [0, 0]
        self.next_direction = [-1,0]

    def tick(self):

        self.target = self.pacman.current_cell
        
        # calculate current cell
        self.calculateCurrentCell()    

        # check if current cell is next cell and center is past cell center (based on direction)
        if self.current_cell == self.next_cell:
            # assign direction to next_direction
            self.direction = self.next_direction
            # if it is then recalculate next cell
            self.calculateNextCell()
            temp_next_cell = self.maze.maze[int(self.next_cell[1])][int(self.next_cell[0])]
           
            # check if next cell is junction
            if temp_next_cell is Moveable and temp_next_cell.is_juction:
                    self.calculateNextDirection(temp_next_cell)
        
        # move ghost in direction
        # snap ghost to correct placement

        direction_has_changed = False
        print("BLINKY Current position:", self.canvas_position)
        self.calculateCurrentCell()    
        print("BLINKY Current cell:", self.current_cell)
        # calcualte target position
        self.next_cell[0] = self.current_cell[0]
        self.next_cell[1] = self.current_cell[1]

        self.next_cell[0] += self.direction[0]
        self.next_cell[1] += self.direction[1]

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

    def calculateNextCell(self):
        pass 
        

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
        decisions = self.calcualteValidDecisions(juction_cell, self.state)
        
        # in fright mode the ghost make decisions randomly 
        if self.state == 2:
            self.next_direction = random.choice(decisions)
        elif len(decisions > 1): 
            distances = []
            for direction in decisions:
                distance = Ghost.pythagoras(self.target, self.next_cell)
                distances.append(distance)
            # find the shortest one
            shortest_distance = min(distances)
            # chose the index
            decision_index = distances.index(shortest_distance)
            self.next_direction = decisions[decision_index]

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