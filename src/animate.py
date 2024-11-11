from tkinter import *
from PIL import Image, ImageTk

class Animate:
    
    def __init__(self, fileLoc, parent) -> None:
        # Open the image with PIL and convert to RGBA to preserve transparency
        info = Image.open(fileLoc)
        framesNo = info.n_frames
        # Extract frames and keep references
        self.photoimage_objects = [] # i spent so long just to find out that this needs to be a local attribute since python was marking it for garbage collection so no image was displaying
        for i in range(framesNo):
            info.seek(i)  # Move to the i-th frame
            frame = info.copy().convert("RGBA")
            # Convert to ImageTk.PhotoImage to preserve transparency
            obj = ImageTk.PhotoImage(frame)
            self.photoimage_objects.append(obj)
        

    def __del__() -> None:
        pass