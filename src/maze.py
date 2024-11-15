from src.animate import Animate

class Maze:

    # define the objects that should be created for the maze
    # anything that is 0 represents somewhere that any character can not move to 
    maze_dict =  {
        "X": 0,  # Out side the bounds of the game
        ".": 1,  # dot
        "+": 2,  # junction 
        "p": 3,  # power-up
        "-": 4,  # tile with nothing
        "d": 5,  # junction without a dot
        "U": 6,  # junction where ghost can not turn up and does not have a dot
        "u": 6,  # junction where ghost can not turn up and has a dot
        "0": 0,  # double corner
        "1": 0,  # double wall
        "2": 0,  # single corner
        "3": 0,  # single wall
        "4": 0,  # Ghost house corner
        "5": 0,  # ghost house wall
        "=": 4,  # ghost house trapdoor, this is 4 since the ghosts need to be able to move out of it
        "6": 0,  # double short corner 
        "7": 0,  # narrow double corner left
        "8": 0,  # narrow double corner right
        "9": 0,  # something to do with the walls
        "n": 7   # teleport square
    }

    # any image path is created as follows "path {frameNo} {rotation} {flip}"
    maze_image_dict = {
        "X": None,                                   # No image to display
        ".": "Dot.png",                              # dot
        "+": "Dot.png",                              # junction 
        "p": "PowerUp.png 1",                        # power-up
        "-": None,                                   # tile with nothing
        "d": None,                                   # junction without a dot
        "U": None,                                   # junction where ghost can not turn up and does not have a dot
        "u": "Dot.png",                              # junction where ghost can not turn up and has a dot
        "0": "Apple.png", #"DoubleCorner.gif 1 0 0",               # double corner
        "1": "Apple.png", #"DoubleWall.gif 1 0 0",                 # double wall
        "2": "Apple.png", #"SingleCorner.gif 1 0 0",               # single corner
        "3": "Apple.png", #"SingleWall.gif 1 0 0",                 # single wall
        "4": "Apple.png", #"GhostHouseCorner.gif 1 0 0",           # Ghost house corner
        "5": "Apple.png", #"GhostHouseWall.gif 1 0 0",             # ghost house wall
        "=": "Apple.png", #"GhostHouseTrapDoor.gif 1 0 0",         # ghost house trapdoor
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