import math
from src.animate import Animate

class Ghost:

    def __init__(self) -> None:
        self.pos = []  # contains the current position of the ghost
        self.current_tile = [] # the tile which the ghost corresponds to
        self.image = Animate() # the path/pillow image
        self.state = 0 # the current state of the ghost, 0 = default, 1 = scatter, 2 = fright
        self.target = [] # the target square that the ghost its trying to get to
        self.decision = [] # the next square the ghost will move to
        self.direction = [] # [x, y] eg [1, 0] will be right, [0, -1] will be down
        self.is_active = True # this is applicable when the ghost is eaten or is in the ghost house
        self.speed = 10 # the base pixel movement speed of the ghost  
        self.speed_modifier = 0.8 # this is applied during the different ghost modes

    def calculateTile() -> None:
        pass

    def calculateTarget() -> None:
        pass

    def makeNextDecision() -> None:
        pass

    def tick():
        pass

    def pythagoras(pos1, pos2) -> float:
        a = (pos1[0] - pos2[0])**2
        b = (pos1[1] - pos2[1])**2
        return math.sqrt(a + b) 