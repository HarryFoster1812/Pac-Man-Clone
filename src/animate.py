from tkinter import *
from PIL import Image, ImageTk
import threading

class Animate:
    
    def __init__(self, fileLoc="", parent: Label | Canvas = None, x=None, y=None, scale:float = 1) -> None:
        
        self.fames = Animate.getFrames(fileLoc, scale)
        self.parent = parent
        self.currentFrame = 0
        self.delayMS = 1000//len(self.fames)

        # add the image to the parent
        if(type(self.parent) == Label): 
            self.parent.configure(image=self.fames[self.currentFrame])

        else:
            self.parent.create_image(x, y, image=self.fames[self.currentFrame], anchor="ne")
        

        # check if the gif/image has more than one frame
        if (len(self.fames) > 1):
            self.loop =  self.parent.after(self.delayMS, self.update)

    def update(self):
        self.currentFrame += 1 # increment the frame
        self.currentFrame %= len(self.fames) # prevent a index error
        
        if(type(self.parent) == Label): 
            self.parent.configure(image=self.fames[self.currentFrame])

        self.loop = self.parent.after(self.delayMS, self.update) # recall the loop
        
        

    def getFrames(fileLoc, scale) -> list:
        # Open the image with PIL and convert to RGBA to preserve transparency
        info = Image.open(fileLoc)
        framesNo = info.n_frames
        # Extract frames and keep references
        frames = [] # i spent so long just to find out that this needs to be a local attribute since python was marking it for garbage collection so no image was displaying
        for i in range(framesNo):
            info.seek(i)  # Move to the i-th frame
            frame = info.copy().convert("RGBA")

            # resize the image
            newHeight = int( info.size[1] * scale )  # convert to int since the PIL resize will only accept int
            newWidth = int( info.size[0] * scale )

            frame = frame.resize((newWidth, newHeight), Image.LANCZOS)

            # Convert to ImageTk.PhotoImage to preserve transparency
            obj = ImageTk.PhotoImage(frame)
            frames.append(obj)

        return frames
        

    def __del__(self) -> None:
        self.parent.after_cancel(self.loop)
