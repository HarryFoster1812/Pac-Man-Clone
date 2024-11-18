from src.objects.ghosts.Ghost import Ghost, GhostState
from src.gameImage import GameImage

# Cyan
class Inky(Ghost):
    def __init__(self, start_pos, maze, pacman):
        super(Inky, self).__init__(start_pos, maze, pacman)
        self.image = GameImage("assets/Ghosts/Cyan/Cyan", load_ghost_variations=True)
        self.scatter_cell = [27,35]
        self.colour = "cyan"
        self.direction = [0, 0]
        self.next_direction = [0,-1]
        self.calculateCurrentCell()
        self.next_cell = self.current_cell
        self.is_in_house = True

    def calculateTarget(self):
        match(self.state):
            case GhostState.CHASE:
                self.target = self.pacman.current_cell
                
            case GhostState.SCATTER:
                self.target = self.scatter_cell
            case GhostState.FRIGHTENED:
                self.target = self.current_cell