from src.gameImage import GameImage
from src.objects.map_objects.moveable import Moveable 

class Powerup(Moveable):
    def __init__(self):
        self.image = GameImage("assets/PowerUp.png")
        self.has_dot = True

    def __del__(self):
        # change game state to powerup
        pass