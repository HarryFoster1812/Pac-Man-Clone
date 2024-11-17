from src.gameImage import GameImage 

class Moveable:
    def __init__(self, has_dot=True, is_junction=False, can_move_up=True):
        if has_dot:
            self.image = GameImage("assets/Dot.png")
        
        self.has_dot = has_dot
        self.is_juction = is_junction
        self.can_move_up = can_move_up # this is only used for the ghosts since on specific tiles they can not move up