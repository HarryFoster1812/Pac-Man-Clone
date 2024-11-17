from src.objects.ghosts.Ghost import Ghost
from src.gameImage import GameImage

# Red
class Blinky(Ghost):
    def __init__(self, start_pos, maze):
        super(Blinky, self).__init__(start_pos, maze)
        self.image = GameImage("assets/Ghosts/Red/Red", load_ghost_variations=True) # need to fill this out