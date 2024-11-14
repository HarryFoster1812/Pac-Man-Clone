class Maze:

    # define the objects that should be created for the maze
    maze_dic =  {
        "X": 0, # free cell
        ".": 0, # dot
        "+": 0, # junction 
        "p": 0, # powerup
        "0": 0, # double corner
        "1": 0, # double wall
        "2": 0, # single corner
        "3": 0, # single wall
        "4": 0, # Ghost house corner
        "5": 0, # ghost house wall
        "=": 0, # ghost house trapdoor
        "6": 0, 
        "7": 0,
        "8": 0,
        "9": 0
    }

    def __init__(self, file_location: str):
        with open(file_location, "r") as maze_file:
            maze_file = [line.rstrip("\n") for line in maze_file.readlines()]
        
        # gen images