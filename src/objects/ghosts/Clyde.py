from src.objects.ghosts.Ghost import Ghost, GhostState
from src.gameImage import GameImage

# Orange
class Clyde(Ghost):
    def __init__(self, start_pos, maze, pacman):
        super(Clyde, self).__init__(start_pos, maze, pacman)
        self.image = GameImage("assets/Ghosts/Orange/Orange", load_ghost_variations=True) # need to fill this out
        self.scatter_cell = [0,35]
        self.colour = "orange"
        self.direction = [0, 0]
        self.next_direction = [0,1]
        self.calculateCurrentCell()
        self.next_cell = self.current_cell
        self.is_in_house = True

    def calculateTarget(self):
        match(self.state):
            case GhostState.CHASE:
                distance = Ghost.pythagoras(self.current_cell, self.pacman.current_cell)
                if distance < 5:
                    self.target = self.pacman.current_cell
                else:
                    self.target = self.scatter_cell

            case GhostState.SCATTER:
                self.target = self.scatter_cell
            case GhostState.FRIGHTENED:
                self.target = self.current_cell