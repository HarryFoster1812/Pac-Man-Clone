from src.objects.ghosts.Ghost import Ghost
from src.gameImage import GameImage
from src.objects.ghosts.ghost_state import GhostState


# Cyan
class Inky(Ghost):
    def __init__(self, start_pos, maze, pacman, blinky):
        super(Inky, self).__init__(start_pos, maze, pacman)
        self.image = GameImage("assets/Ghosts/Cyan/Cyan", load_ghost_variations=True)
        self.scatter_cell = [27,35]
        self.colour = "cyan"
        self.direction = [0, -1]
        self.next_direction = [0,-1]
        self.calculateCurrentCell()
        self.next_cell = self.current_cell
        self.state = GhostState.IN_GHOST_HOUSE
        self.ghost_house_target = start_pos
        self.blinky = blinky

    def reset(self, level, maze, startpos):
        super().reset(level, maze, startpos)
        
        parent = self.image.parent
        id = self.image.id
        self.image = GameImage("assets/Ghosts/Cyan/Cyan", load_ghost_variations=True)
        self.image.id = id
        self.image.parent = parent
        
        self.direction = [0, -1]
        self.next_direction = [0,-1]
        self.calculateCurrentCell()
        self.next_cell = self.current_cell

    def calculateTarget(self):
        match(self.state):
            case GhostState.CHASE:
                self.target = self.pacman.current_cell
                # need to do cell calulation based off pink
                
            case GhostState.SCATTER:
                self.target = self.scatter_cell
            case GhostState.FRIGHTENED:
                self.target = self.current_cell