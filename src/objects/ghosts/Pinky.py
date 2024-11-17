from src.objects.ghosts.Ghost import Ghost
from src.gameImage import GameImage

# Pink
class Pinky(Ghost):
    def __init__(self, start_pos, maze):
        super(Pinky, self).__init__(start_pos, maze)
        self.image = GameImage("assets/Ghosts/Pink/Pink", load_ghost_variations=True) # need to fill this out
        