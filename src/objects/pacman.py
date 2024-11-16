from src.gameImage import GameImage
from src.maze import Maze
from src.objects.map_objects.wall import Wall

class Pacman:
    def __init__(self, start_pos: list, maze: Maze) -> None:
        self.canvas_position = start_pos # the x and y co-ordinates of pacman
        self.current_cell = [] # the co-ordinates of pacman in the cell
        self.direction = -1 # the current direction that pacman is travelling
        self.next_direction = 0 # this will be via user input 
        self.speed = 5.05050508333 # pixels this is from 
        self.speed_modifier = 0.1 # float 0-1
        self.image = GameImage("assets/PacManRight.gif", calculateRotations=True) # need to fill this out
        self.maze = maze

    def tick(self):
        # check if we can update the direction 
        current_cell_x = self.current_cell.x
        current_cell_y = self.current_cell.y
        
        current_cell_x += self.next_direction[0]
        current_cell_y += self.next_direction[1]

        next_cell = self.maze[current_cell_y][current_cell_x]
        
        if isinstance(next_cell, Wall):
            #  can not move so
            pass

        self.canvas_position[0] += self.speed*self.speed_modifier
        # update the direction (is possible)
        # update position
        # update frame (based on current direction)
        # calculate next direction
        # 
        pass

    def updateFrame(self):
        pass

    def place(self, x:int, y:int):
        self.speed_modifier = 0 # set it to 0 so that pac man does not move
        self.canvas_position = [x, y]