from src.gameImage import GameImage
from src.maze import Maze
from src.objects.map_objects.wall import Wall
from src.objects.map_objects.moveable import Moveable

class Pacman:
    def __init__(self, start_pos: list, maze: Maze) -> None:
        self.canvas_position = [start_pos[0], start_pos[1]] # the x and y co-ordinates of pacman
        self.target_position = []
        self.current_cell = [] # the co-ordinates of pacman in the cell
        self.next_cell = [0,0]
        self.direction = [0,0] # the current direction that pacman is travelling
        self.next_direction = [0,0] # this will be via user input 
        self.speed = 5.05050508333 # pixels this is from 
        self.speed_modifier = 0.9 # float 0-1
        
        self.image = GameImage("assets/PacManRight.gif", calculate_rotations=True) # need to fill this out
        self.tick_count = 0

        self.maze = maze

    def tick(self):
        direction_has_changed = False

        print("Current position:", self.canvas_position)
        self.calculateCurrentCell()    
        print("Current cell:", self.current_cell)
        # calcualte target position
        # if target position is reached then check if direction can be changed
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
            self.direction = [0,0]
            self.enableIdle()

        else:
            self.snapPosition()

        # check if we can change the direction of pacman
        direction_has_changed = self.checkChangeDirection()

        # update frame (based on current direction)
        if direction_has_changed:
            match(self.direction):
                case [0,1] : self.updateFrame(self.image.down)
                case [0,-1]: self.updateFrame(self.image.up)
                case [1,0] : self.updateFrame(self.image.right)
                case [-1,0]: self.updateFrame(self.image.left)
        else:
            self.updateFrame()

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

            else:
                self.direction = self.next_direction
                self.disableIdle()
                return True
        
        # the user has not entered a new direction to travel in
        else:
            return False

    def updateFrame(self, change_frame_set = None):
        self.tick_count += 1
        self.tick_count %= 5
        if change_frame_set != None:
            self.image.switchFrameSet(change_frame_set)
        
        if self.tick_count == 0:
            self.image.nextFrame()

    def calculateCurrentCell(self):
        x = (self.canvas_position[0] + 32)//32
        y = (self.canvas_position[1] + 32)//32
        
        self.current_cell = [x,y]

    def enableIdle(self):
        self.image.enableIdle()

    def disableIdle(self):
        self.image.disableIdle()
