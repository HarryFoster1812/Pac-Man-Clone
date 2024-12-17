from src.gameImage import GameImage


class Wall:
    def __init__(self, image_path, frame_no):
        self.image_path = image_path
        self.frame_no = frame_no
        self.image = GameImage(image_path, frame=frame_no)

    def serialise(self) -> dict:
        return {"image_path": self.image_path, "frame_no": self.frame_no}
