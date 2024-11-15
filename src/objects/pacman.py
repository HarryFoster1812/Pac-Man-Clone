from src.animate import Animate

class Pacman:
    def __init__(self, start_pos: list) -> None:
        self.canvas_position = start_pos # the x and y co-ordinates of pacman
        self.current_cell = [] # the co-ordinates of pacman in the cell
        self.direction = -1 # the current direction that pacman is travelling
        self.next_direction = 0 # this will be via user input 
        self.speed = 10
        self.speed_modifier = 0.1 # float 0-1
        self.image = Animate("assets/PacManRight.gif") # need to fill this out

    def tick():
        # update the direction (is possible)
        # update position
        # update frame (based on current direction)
        # calculate next direction
        # 
        pass

    def place(self, x:int, y:int):
        self.speed_modifier = 0 # set it to 0 so that pac man does not move
        self.canvas_position = [x, y]