from src.animate import Animate
from src.objects.map_objects.wall import Wall 
from src.objects.map_objects.moveable import Moveable 
from src.objects.map_objects.powerup import Powerup 
import copy

class Maze:

    # define the objects that should be created for the maze
    # anything that is 0 represents somewhere that any character can not move to 
    maze_dict =  {
        "X": None,  # Out side the bounds of the game
        ".": Moveable,  # dot
        "+": Moveable,  # junction 
        "p": Powerup,  # power-up
        "-": Moveable,  # tile with nothing
        "d": Moveable,  # junction without a dot
        "U": Moveable,  # junction where ghost can not turn up and does not have a dot
        "u": Moveable,  # junction where ghost can not turn up and has a dot
        "0": Wall,  # double corner
        "1": Wall,  # double wall
        "2": Wall,  # single corner
        "3": Wall,  # single wall
        "4": Wall,  # Ghost house corner
        "5": Wall,  # ghost house wall
        "=": Wall,  # ghost house trapdoor, this is 4 since the ghosts need to be able to move out of it
        "6": Wall,  # double short corner 
        "7": Wall,  # narrow double corner left
        "8": Wall,  # narrow double corner right
        "9": Wall,  # something to do with the walls
        "n": Moveable   # teleport square
    }

    # any image path is created as follows "path {frameNo} {rotation} {flip}"
    maze_image_dict = {
        "X": None,                                   # No image to display
        ".": "Dot.png",                              # dot
        "+": "Dot.png",                              # junction 
        "p": "PowerUp.png",                        # power-up
        "-": None,                                   # tile with nothing
        "d": "Dot.png",                                   # junction without a dot
        "U": None,                                   # junction where ghost can not turn up and does not have a dot
        "u": "Dot.png",                              # junction where ghost can not turn up and has a dot
        "0": "Apple.png", #"DoubleCorner.gif 1 0 0",               # double corner
        "1": "Apple.png", #"DoubleWall.gif 1 0 0",                 # double wall
        "2": "Apple.png", #"SingleCorner.gif 1 0 0",               # single corner
        "3": "Apple.png", #"SingleWall.gif 1 0 0",                 # single wall
        "4": "GhostHouse/GhostHouseCorner.gif 1 0 0",           # Ghost house corner
        "5": "Apple.png", #"GhostHouseWall.gif 1 0 0",             # ghost house wall
        "=": "GhostHouse/GhostHouseTrapdoor.png", #"GhostHouseTrapDoor.gif 1 0 0",         # ghost house trapdoor
        "6": "Apple.png", #"DoubleShortCorner.gif 1 0 0",          # double short corner 
        "7": "Apple.png", #"NarrowDoubleCornerRight.gif 1 0 0",    # narrow double corner
        "8": "Apple.png", #"NarrowDoubleCornerLeft.gif 1 0 0",     # narrow double corner 
        "9": "Apple.png",                                    # something to do with the walls
        "n": None
    }

    def __init__(self, file_location: str):
        with open(file_location, "r") as maze_file:
            maze_file = [line.rstrip("\n") for line in maze_file.readlines()]

        self.maze = []
        self.mazeImages = []
        self.staticImages = [] # all of the walls, and the dots
        self.animatedImages = [] # powerUps

        assetsPath = "assets/"

        # parse each line
        for line in maze_file:
            
            tempType = []
            imageTemp = []

            line = line.split(" ")

            for element in line:
                
                typeOfCell = Maze.maze_dict[element]
                if typeOfCell != None:

                    typeOfCell = typeOfCell()
                tempType.append(typeOfCell)
                
                imagePath = Maze.maze_image_dict[element]
                if (imagePath == None):
                    imageTemp.append(None)
                
                elif (len(imagePath.split(" ")) == 1): # check if it has any parameters
                    image = Animate(assetsPath + imagePath)
                    self.staticImages.append(image)
                    imageTemp.append(image)
                
                else: # it has parameters so we need to split them and then pass them through
                    #path {frameNo} {rotation} {flip}
                    imageTemp.append(None)
                    """
                    param_image_path = imagePath.split(" ")[0]
                    param_frame      = int(imagePath.split(" ")[1])
                    param_rotation   = int(imagePath.split(" ")[2])
                    param_flip       = int(imagePath.split(" ")[3])

                    image = Animate(assetsPath + param_image_path, frame=param_frame, flip=param_flip, rotation=param_rotation) 
                    imageTemp.append(image)
                    """
            self.maze.append(tempType)
            self.mazeImages.append(imageTemp)

    def reset(self):
        self.__init__()

    def removeObject(self, x, y):
        obj = self.maze[y][x]
        self.maze[y][x] = None
        del obj

