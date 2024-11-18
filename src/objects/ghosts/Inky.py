from src.objects.ghosts.Ghost import Ghost
from src.gameImage import GameImage

# Cyan
class Inky(Ghost):
    def __init__(self, start_pos, maze, pacman):
        super(Inky, self).__init__(start_pos, maze, pacman)
        self.image = GameImage("assets/Ghosts/Cyan/Cyan", load_ghost_variations=True)
        self.scatter_cell = [27,35]
        self.colour = "cyan"

        