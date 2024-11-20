from src.objects.map_objects.wall import Wall 
from src.objects.map_objects.moveable import Moveable 
from src.objects.ghosts.ghost_state import GhostState 
import math

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

        '.': [Moveable, [True,  False, True,  False, False]], # dot
        'p': [Moveable, [False, False, True,  True , False]], # powerup
        'P': [Moveable, [False, True,  True,  True , False]], # powerup that is junction
        '+': [Moveable, [True,  True,  True,  False, False]], # junction without a dot
        'd': [Moveable, [False, True,  True,  False, False]], # 
        'U': [Moveable, [False, True,  False, False, False]], # junction where ghost can not turn up and does not have a dot
        'u': [Moveable, [True,  True,  False, False, False]], # junction where ghost can not turn up and has a dot
        '-': [Moveable, [False, False, True,  False, False]], 
        'n': [Moveable, [False, False, False, False, True]], 
        'X': [None], 
    }

     # has dot, is junction, can move up, is powerup , is teleport

    level_info = [
        {
            "pacmanSpeed" : 0.8,
	    	"ghostSpeed" : 0.75,
	    	"frightPacManSpeed" : 0.9,
	    	"frightGhostSpeed" : 0.5,
	    	"frightFrames" : 6*60,
	    	"frightFlashStart" : 5*2*5,
	    	"modes" : [[GhostState.SCATTER, 7*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 7*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, math.inf]]
	    }, 
    
	    {
	    	"pacmanSpeed" : 0.9,
	    	"ghostSpeed" : 0.85,
	    	"frightPacManSpeed" : 0.95,
	    	"frightGhostSpeed" : 0.55,
	    	"frightFrames" : 5*60,
	    	"frightFlashStart" : 5*2*5,
	    	"modes" : [[GhostState.SCATTER, 7*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 7*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 1033*60], [GhostState.SCATTER, 1], [GhostState.CHASE, math.inf]]
	    }, 
    
	    {
	    	"pacmanSpeed" : 0.9,
	    	"ghostSpeed" : 0.85,
	    	"frightPacManSpeed" : 0.95,
	    	"frightGhostSpeed" : 0.55,
	    	"frightFrames" : 4*60,
	    	"frightFlashStart" : 5*2*5,
	    	"modes" : [[GhostState.SCATTER, 7*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 7*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 1033*60], [GhostState.SCATTER, 1], [GhostState.CHASE, math.inf]]
	    } ,
    
	    {
	    	"pacmanSpeed" : 0.9,
	    	"ghostSpeed" : 0.85,
	    	"frightPacManSpeed" : 0.95,
	    	"frightGhostSpeed" : 0.55,
	    	"frightFrames" : 3*60,
	    	"frightFlashStart" : 5*2*5,
	    	"modes" : [[GhostState.SCATTER, 7*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 7*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 1033*60], [GhostState.SCATTER, 1], [GhostState.CHASE, math.inf]]
	    },
    
    
	    {
	    	"pacmanSpeed" : 1,
	    	"ghostSpeed" : 0.95,
	    	"frightPacManSpeed" : 1,
	    	"frightGhostSpeed" : 0.6,
	    	"frightFrames" : 2*60,
	    	"frightFlash" : 5*2*5,
	    	"modes" : [[GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 1037*60], [GhostState.SCATTER, 1], [GhostState.CHASE, math.inf]]
	    },
    
	    {
	    	"pacmanSpeed" : 1,
	    	"ghostSpeed" : 0.95,
	    	"frightPacManSpeed" : 1,
	    	"frightGhostSpeed" : 0.6,
	    	"frightFrames" : 2*60,
	    	"frightFlash" : 5*2*5,
	    	"modes" : [[GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 1037*60], [GhostState.SCATTER, 1], [GhostState.CHASE, math.inf]]
	    },
    
	    {
	    	"pacmanSpeed" : 1,
	    	"ghostSpeed" : 0.95,
	    	"frightPacManSpeed" : 1,
	    	"frightGhostSpeed" : 0.6,
	    	"frightFrames" : 2*60,
	    	"frightFlash" : 5*2*5,
	    	"modes" : [[GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 1037*60], [GhostState.SCATTER, 1], [GhostState.CHASE, math.inf]]
	    },
    
	    {
	    	"pacmanSpeed" : 1,
	    	"ghostSpeed" : 0.95,
	    	"frightPacManSpeed" : 1,
	    	"frightGhostSpeed" : 0.6,
	    	"frightFrames" : 2*60,
	    	"frightFlash" : 5*2*5,
	    	"modes" : [[GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 1037], [GhostState.SCATTER, 1], [GhostState.CHASE, math.inf]]
	    },
    
	    {
	    	"pacmanSpeed" : 1,
	    	"ghostSpeed" : 0.95,
	    	"frightPacManSpeed" : 1,
	    	"frightGhostSpeed" : 0.6,
	    	"frightFrames" : 1*60,
	    	"frightFlash" : 5*2*3,
	    	"modes" : [[GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 1037], [GhostState.SCATTER, 1], [GhostState.CHASE, math.inf]]
	    },
    
	    {
	    	"pacmanSpeed" : 1,
	    	"ghostSpeed" : 0.95,
	    	"frightPacManSpeed" : 1,
	    	"frightGhostSpeed" : 0.6,
	    	"frightFrames" : 3*60,
	    	"frightFlash" : 5*2*5,
	    	"modes" : [[GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 20*60], [GhostState.SCATTER, 5*60], [GhostState.CHASE, 1037], [GhostState.SCATTER, 1], [GhostState.CHASE, math.inf]]
	    }
    ]

    def __init__(self, file_location: str):
        with open(file_location, "r") as maze_file:
            maze_file = [line.rstrip("\n") for line in maze_file.readlines()]

        self.maze = []
        self.teleport_squares = [] 

        self.file_loc = file_location 

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
                            obj = typeOfCell[0](arglist[0], arglist[1], arglist[2], arglist[3], arglist[4])

                else:
                    obj = None

                if isinstance(obj, Moveable) and obj.is_teleport:
                    self.teleport_squares.append(obj) 

                tempType.append(obj)
                
            self.maze.append(tempType)
            
    def reset(self):
        self.__init__(self.file_loc)

    def getOtherTeleportSquareLocation(self, square:Moveable):
        index_of_current_sqaure = self.teleport_squares.index(square)
        if index_of_current_sqaure == 0:
            other_sqaure = self.teleport_squares[1]
        else:
            other_sqaure = self.teleport_squares[0]

        for i, line in enumerate(self.maze):
            for j, cell in enumerate(line):
                if cell == other_sqaure:
                    return [j,i]

    def get_level_info(self, level):
        if level > 10:
            return Maze.level_info[10]
        
        return Maze.level_info[level]

    def removeObject(self, x, y):
        obj = self.maze[y][x]
        self.maze[y][x] = None
        del obj
