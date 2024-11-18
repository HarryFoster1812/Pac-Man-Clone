from src.objects.ghosts.Ghost import Ghost, GhostState
from src.gameImage import GameImage

# Red
class Blinky(Ghost):
    def __init__(self, start_pos, maze, pacman):
        super(Blinky, self).__init__(start_pos, maze, pacman)
        self.image = GameImage("assets/Ghosts/Red/Red", load_ghost_variations=True) # need to fill this out
        self.scatter_cell = [25,0]
        self.colour = "red"
        self.direction = [0, 0]
        self.next_direction = [-1,0]
        self.calculateCurrentCell()
        self.next_cell = self.current_cell

    def calculateTarget(self):
        match(self.state):
            case GhostState.CHASE:
                self.target = self.pacman.current_cell
            case GhostState.SCATTER:
                self.target = self.scatter_cell
            case GhostState.FRIGHTENED:
                self.target = self.current_cell