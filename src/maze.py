from src.animate import Animate
from src.objects.map_objects.wall import Wall 
from src.objects.map_objects.moveable import Moveable 
from src.objects.map_objects.powerup import Powerup 
import copy

class Maze:

    # define the objects that should be created for the maze
    # each value is [Class, [args]]
    maze_dict = {
        '┅': [Wall, ["other/Wall.gif",                      0]], # Bottom outer wall
        '━': [Wall, ["other/Wall.gif",                      1]], # top outer wall 
        '┃': [Wall, ["other/Wall.gif",                      2]], # Left outer wall
        '┇': [Wall, ["other/Wall.gif",                      3]], # Right outer wall
        
        '╚': [Wall, ["other/DoubleCorner.gif",              0]], 
        '╔': [Wall, ["other/DoubleCorner.gif",              1]], # outer double corner
        '╝': [Wall, ["other/DoubleCorner.gif",              2]], 
        '╗': [Wall, ["other/DoubleCorner.gif",              3]], 
        
        '┄': [Wall, ["other/InnerWall.gif",                 0]], # bottom inner wall 
        '─': [Wall, ["other/InnerWall.gif",                 1]], # top inner wall
        '│': [Wall, ["other/InnerWall.gif",                 2]], 
        '┆': [Wall, ["other/InnerWall.gif",                 3]], 
        
        '┘': [Wall, ["other/InnerCorner.gif",               0]], 
        '┐': [Wall, ["other/InnerCorner.gif",               1]], 
        '└': [Wall, ["other/InnerCorner.gif",               2]], 
        '┌': [Wall, ["other/InnerCorner.gif",               3]], # short single corner
        
        '╮': [Wall, ["other/InnerLongCorner.gif",           0]], # long inner corner
        '╯': [Wall, ["other/InnerLongCorner.gif",           1]], 
        '╭': [Wall, ["other/InnerLongCorner.gif",           2]], 
        '╰': [Wall, ["other/InnerLongCorner.gif",           3]], 
        
        '╒': [Wall, ["GhostHouse/GhostHouseCorner.gif",     0]], 
        '╘': [Wall, ["GhostHouse/GhostHouseCorner.gif",     1]], 
        '╕': [Wall, ["GhostHouse/GhostHouseCorner.gif",     2]], 
        '╛': [Wall, ["GhostHouse/GhostHouseCorner.gif",     3]], 
        '=': [Wall, ["GhostHouse/GhostHouseTrapdoor.png",   0]], # trapdoor (ghost can move through only on exit)
        '╼': [Wall, ["GhostHouse/GhostHouseEnd.gif",        0]], 
        '╾': [Wall, ["GhostHouse/GhostHouseEnd.gif",        1]], 
        
        '┢': [Wall, ["other/DoubleLongCorner.gif",          0]], 
        '┡': [Wall, ["other/DoubleLongCorner.gif",          1]], # long outer corner
        '┪': [Wall, ["other/DoubleLongCorner.gif",          2]], 
        '┩': [Wall, ["other/DoubleLongCorner.gif",          3]], 
        '┲': [Wall, ["other/DoubleLongCorner.gif",          4]], 
        '┱': [Wall, ["other/DoubleLongCorner.gif",          5]], 

        '.': [Moveable, [True, False, True, False]], # dot
        'p': [Moveable, [False, False, True, True]], # powerup
        'P': [Moveable, [False, True, True, True]], # powerup that is junction
        '+': [Moveable, [True, True, True, False]], # junction without a dot
        'd': [Moveable, [False, True, True, False]], # 
        'U': [Moveable, [False, True, False, False]], # junction where ghost can not turn up and does not have a dot
        'u': [Moveable, [True, True, False, False]], # junction where ghost can not turn up and has a dot
        '-': [Moveable, [False, False, True, False]], 
        'n': [Moveable, [False, False, False, False]], 
        'X': [None], 
        }

        # has dot, is junction, can move up

    def __init__(self, file_location: str):
        with open(file_location, "r") as maze_file:
            maze_file = [line.rstrip("\n") for line in maze_file.readlines()]

        self.maze = []
        self.staticImages = [] # all of the walls, and the dots
        self.animatedImages = [] # powerUps

        assetsPath = "assets/"

        # parse each line
        for line in maze_file:
            
            tempType = []

            line = line.split(" ")

            for element in line:

                typeOfCell = Maze.maze_dict[element]

                if typeOfCell[0] != None:
                    # check if any args are given
                    if len(typeOfCell) == 1:

                        obj = typeOfCell[0]()

                    else: # args are given, need to extract args from [1]
                        if typeOfCell[0] is Wall:
                            arglist = typeOfCell[1]
                            obj = typeOfCell[0]( assetsPath + arglist[0], arglist[1])
                        
                        else:
                            arglist = typeOfCell[1]
                            obj = typeOfCell[0](arglist[0], arglist[1], arglist[2], arglist[3])
                        

                else:
                    obj = None

                tempType.append(obj)
                
            self.maze.append(tempType)
            
    def reset(self):
        self.__init__()

    def removeObject(self, x, y):
        obj = self.maze[y][x]
        self.maze[y][x] = None
        del obj

