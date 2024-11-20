from enum import Enum

class GhostState(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2
    DEAD = 3
    IN_GHOST_HOUSE = 4
    MOVING_INTO_GHOST_HOUSE = 5
    MOVING_OUT_OF_GHOST_HOUSE = 6