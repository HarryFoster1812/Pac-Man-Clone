from src.gameImage import GameImage 

class Moveable:
    def __init__(self, has_dot, is_junction, can_move_up, is_powerup):
        if has_dot:
            self.image = GameImage("assets/Dot.png")
        
        elif is_powerup:
            self.image = GameImage("assets/PowerUp.png")

        self.has_dot = has_dot
        self.is_juction = is_junction
        self.can_move_up = can_move_up # this is only used for the ghosts since on specific tiles they can not move up

    def removeDot(self):
        self.has_dot = False
        del self.image
