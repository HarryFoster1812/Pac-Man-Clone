from tkinter import *
from PIL import Image, ImageTk
import threading

class Animate:
    
    def __init__(self, fileLoc="", parent: Label | Canvas = None, x=None, y=None, scale:float = 1, rotation: int = 0, flip:int = 0, frame: int=-1) -> None:

        """
        The constructor function for an animated image
        :param fileLoc: The file location of the image
        :param parent: The object that the image will be added to
        :param x: 
        :param y:
        :param scale:
        :param rotation:
        :param flip:  
        :param frame: -1 default, otherwise the frame is specified
        """

        self.fames = self.getFrames(fileLoc, scale)
        self.parent = parent
        self.currentFrame = 0
        self.delayMS = 1000//len(self.fames)

        self.is_enabled = False

        # check if the gif/image has more than one frame and it is intended to be used as a gif
        if (len(self.fames) > 1 and frame ==-1):
            self.loop =  None # set it to something

        elif(frame != -1): # we need to get a specific frame
            self.currentFrame = frame

    def update(self):
        self.currentFrame += 1 # increment the frame
        self.currentFrame %= len(self.fames) # prevent a index error
        
        if(type(self.parent) == Label): 
            self.parent.configure(image=self.fames[self.currentFrame])

        self.loop = self.parent.after(self.delayMS, self.update) # recall the loop


    def addParent(self, new_parent, x:int = 0, y:int = 0):
        # add the image to the parent
        self.parent = new_parent

        if(type(self.parent) == Label): 
            self.parent.configure(image=self.fames[self.currentFrame])

        elif (type(self.parent) == Canvas):
            self.id = self.parent.create_image(x, y, image=self.fames[self.currentFrame], anchor="ne")
        

    def getFrames(self, fileLoc, scale) -> list:
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

    def toggleAnimation(self):
        if hasattr(self, "loop"): # we need to check if the loop attribute is created as for a static image (1 frame) the loop will not be created
            if self.is_enabled:
                self.parent.after_cancel(self.loop) # cancel the loop
                self.is_enabled = False
            else:
                self.loop = self.parent.after(self.delayMS, self.update)
                self.is_enabled = True

    def __del__(self) -> None:
        if hasattr(self, "loop"): # we need to check if the loop attribute is created as for a static image (1 frame) the loop will not be created
            self.parent.after_cancel(self.loop) # cancel the loop
