from src.animate import Animate

class Character:
    """
    This is the abstract class which defines a moving character eg. a ghost or pacman
    
    """

    def __init__(self, image_source: str) -> None:
        self.image = Animate(fileLoc=image_source)
        
    def tick(self):
        pass

    def toggleAnimation(self):
        self.image.toggleAnimation()