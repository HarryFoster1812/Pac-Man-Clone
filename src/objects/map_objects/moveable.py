from src.gameImage import GameImage 

class Moveable:
    def __init__(self, has_dot, is_junction, can_move_up, is_powerup, is_teleport):
        if has_dot:
            self.image = GameImage("assets/Dot.png")
            self.points = 10
        
        elif is_powerup:
            self.image = GameImage("assets/PowerUp.png")
            self.points = 50
        
        else:
            self.points = 0

        self.has_dot = has_dot
        self.is_juction = is_junction
        self.can_move_up = can_move_up # this is only used for the ghosts since on specific tiles they can not move up
        self.is_powerup = is_powerup
        self.is_teleport = is_teleport

    def removeImage(self):
        self.has_dot = False
        self.is_powerup = False
        self.points = 0
        del self.image

    def serialise(self):
        return {
            "has_dot":self.has_dot, 
            "is_junction":self.is_juction, 
            "can_move_up":self.can_move_up, 
            "is_poweup":self.is_powerup, 
            "is_teleport":self.is_teleport
            }
