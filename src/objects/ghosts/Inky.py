from src.objects.ghosts.Ghost import Ghost
from src.gameImage import GameImage

# Cyan
class Inky(Ghost):
    def __init__(self, start_pos, maze):
        super(Inky, self).__init__(start_pos, maze)
        self.image = GameImage("assets/Ghosts/Cyan/Cyan", load_ghost_variations=True) # need to fill this out
        