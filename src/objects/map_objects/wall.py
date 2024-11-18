from src.gameImage import GameImage

class Wall:
    def __init__(self, image_path, frame_no):
        self.image = GameImage(image_path, frame=frame_no)