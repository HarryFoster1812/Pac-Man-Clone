from enum import Enum


class GhostState(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2
    DEAD = 3
    IN_GHOST_HOUSE = 4
    MOVING_INTO_GHOST_HOUSE = 5
    MOVING_OUT_OF_GHOST_HOUSE = 6

    def get_state_by_value(value):
        match (value):
            case 0: return GhostState.CHASE
            case 1: return GhostState.SCATTER
            case 2: return GhostState.FRIGHTENED
            case 3: return GhostState.DEAD
            case 4: return GhostState.IN_GHOST_HOUSE
            case 5: return GhostState.MOVING_INTO_GHOST_HOUSE
            case 6: return GhostState.MOVING_OUT_OF_GHOST_HOUSE
            case _: return False
