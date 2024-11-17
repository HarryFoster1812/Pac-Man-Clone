import math

class Ghost:

    def __init__(self, start_pos, maze) -> None:
        self.state = 0 # the current state of the ghost, 0 = default, 1 = scatter, 2 = fright, 3 = dead
        self.target = [] # the target square that the ghost its trying to get to
        self.decision = [] # the next square the ghost will move to
        self.direction = [] # [x, y] eg [1, 0] will be right, [0, -1] will be down
        self.is_active = True # this is applicable when the ghost is eaten or is in the ghost house
        self.speed = 5.05050508333 # the base pixel movement speed of the ghost  
        self.speed_modifier = 0.8 # this is applied during the different ghost modes


        self.canvas_position = [start_pos[0], start_pos[1]] # the x and y co-ordinates of pacman
        self.target_position = []
        self.current_cell = [] # the co-ordinates of pacman in the cell
        self.next_cell = [0,0]
        self.direction = [0,0] # the current direction that pacman is travelling
        self.next_direction = [0,0] # this will be via user input 
        self.speed = 5.05050508333 # pixels this is from 
        self.speed_modifier = 0.9 # float 0-1
        
        self.tick_count = 0

        self.maze = maze


    def calculateTile() -> None:
        pass

    def calculateTarget() -> None:
        pass

    def makeNextDecision() -> None:
        pass

    def tick(self):
        pass

    def changeState(self, new_state):
        match (new_state):
            case 0: self.calculateTarget()
            case 1: pass # go to the edge of the screen
            case 2: 
                self.direction *= -1
                self.speed_modifier = 0.4

    def pythagoras(pos1, pos2) -> float:
        a = (pos1[0] - pos2[0])**2
        b = (pos1[1] - pos2[1])**2
        return math.sqrt(a + b) 