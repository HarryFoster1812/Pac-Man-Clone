class Maze:

    # define the objects that should be created for the maze
    maze_dic =  {
        "X": 0, # Out side the bounds of the game
        ".": 0, # dot
        "+": 0, # junction 
        "p": 0, # powerup
        "-": 0, # tile with nothing
        "d": 0, # junction without a dot
        "U": 0, # junction where ghost can not turn up and does not have a dot
        "u": 0, # junction where ghost can not turn up and has a dot
        "0": 0, # double corner
        "1": 0, # double wall
        "2": 0, # single corner
        "3": 0, # single wall
        "4": 0, # Ghost house corner
        "5": 0, # ghost house wall
        "=": 0, # ghost house trapdoor
        "6": 0, # double short corner 
        "7": 0, # narow double corner
        "8": 0, # narrow double corner 
        "9": 0 # something to do with the walls
    }

    def __init__(self, file_location: str):
        with open(file_location, "r") as maze_file:
            maze_file = [line.rstrip("\n") for line in maze_file.readlines()]
        
        # gen images