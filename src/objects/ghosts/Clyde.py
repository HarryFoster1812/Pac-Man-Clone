from src.objects.ghosts.Ghost import Ghost
from src.gameImage import GameImage

# Orange
class Clyde(Ghost):
    def __init__(self, start_pos, maze):
        super(Clyde, self).__init__(start_pos, maze)
        self.image = GameImage("assets/Ghosts/Orange/Orange", load_ghost_variations=True) # need to fill this out
