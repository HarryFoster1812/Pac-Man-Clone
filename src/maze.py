class Maze:

    # define the objects that should be created for the maze
    maze_dic =  {
        "": 0,
        "": 0,
        "": 0,
        "": 0,
        "": 0,
        "": 0,
        "": 0,
    }

    def __init__(self, file_location: str):
        with open(file_location, "r") as maze_file:
            maze_file = [line.rstrip("\n") for line in maze_file.readlines()]
        
        maze_file