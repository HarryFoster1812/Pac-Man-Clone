from src.gameImage import GameImage
from src.maze import Maze
from src.objects.map_objects.wall import Wall
from src.objects.map_objects.moveable import Moveable

class Pacman:

    SPEED = 5.05050508333 # pixels this is from

    def __init__(self, start_pos: list, maze: Maze) -> None:
        self.canvas_position = [start_pos[0], start_pos[1]] # the x and y co-ordinates of pacman
        self.target_position = []
        self.calculateCurrentCell()
        self.current_cell = [] # the co-ordinates of pacman in the cell
        self.next_cell = [0,0]
        self.direction = [0,0] # the current direction that pacman is traveling
        self.next_direction = [0,0] # this will be via user input 
         
        self._maze_ = maze
        self.speed_modifier = 2 # float 0-1
        
        self._pacman_death_image_ = GameImage("assets/pacmanDeath.gif")

        self.image = GameImage("assets/PacManRight.gif", calculate_rotations=True) # need to fill this out
        self.tick_count = 0

        self.is_dead = False


    def tick(self):

        if self.is_dead:
            self.updateFrame()
            return

        direction_has_changed = False

        self.calculateCurrentCell()
        #print("Current position:", self.canvas_position)
        #print("Current cell:", self.current_cell)
        # calculate target position
        # if target position is reached then check if direction can be changed
        self.next_cell[0] = self.current_cell[0]
        self.next_cell[1] = self.current_cell[1]

        self.next_cell[0] += self.direction[0]
        self.next_cell[1] += self.direction[1]

        self.calculateTargetPos()
        current_cell = self._maze_.maze[int(self.current_cell[1])][int(self.current_cell[0])]
        #print("Target Position:", self.target_position)
        #print("Target cell:", self.next_cell, end="\n\n")
        #print("Direction:", self.direction, end="\n\n")
        #print("Next Direction:", self.next_direction, end="\n\n")
        try:
            next_cell = self._maze_.maze[int(self.next_cell[1])][int(self.next_cell[0])]

            if isinstance(next_cell, Wall):
                self.next_cell = self.current_cell
                self.calculateTargetPos()
                self.canvas_position = self.target_position
                self.direction = [0,0]
                self.enableIdle()

            elif isinstance(current_cell, Moveable) and current_cell.is_teleport:
                # find the other teleport square
                index_other_cell = self._maze_.getOtherTeleportSquareLocation(current_cell)
                # change co-ordinates
                index_next_square_after_teleport = [index_other_cell[0] + self.next_direction[0], index_other_cell[1]+self.next_direction[1]]  
                self.canvas_position[0] = index_next_square_after_teleport[0]*32 -16
                self.canvas_position[1] = index_next_square_after_teleport[1]*32 -16
                return

            else:
                self.snapPosition()
        
        except:
             # find the other teleport square
            index_other_cell = self._maze_.getOtherTeleportSquareLocation(current_cell)

            # change coordiantes
            index_next_square_after_teleport = [index_other_cell[0] + self.next_direction[0], index_other_cell[1]+self.next_direction[1]]  
            self.canvas_position[0] = index_next_square_after_teleport[0]*32 -16
            self.canvas_position[1] = index_next_square_after_teleport[1]*32 -16
            return

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

    def reset(self, level, maze):
        parent = self.image.parent
        id = self.image.id
        self.__init__([416,816], maze)
        self.image.parent = parent
        self.image.id = id
        self.calculateCurrentCell()
        self.is_dead = False
        self.updateFrame(self.image.right)

    def snapPosition(self):
        next_position = [
                self.canvas_position[0] + Pacman.SPEED * self.speed_modifier * self.direction[0],
                self.canvas_position[1] + Pacman.SPEED * self.speed_modifier * self.direction[1]
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

            next_cell = self._maze_.maze[int(current_cell_y)][int(current_cell_x)]

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

    def start_death(self):
        self.updateFrame(self._pacman_death_image_.frames)
        self.is_dead = True

    def serialise(self) -> dict:
        pass