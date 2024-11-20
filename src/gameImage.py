from PIL import Image, ImageTk
import copy
from tkinter import Canvas

class GameImage:
    def __init__(self, image_path:str, scale:float=1, rotation: int = 0, flip:int = 0, frame: int=-1, calculate_rotations:bool = False, load_ghost_variations = False):
        self.current_frame = 0
        self.isIdle = True

        if load_ghost_variations:
            directions = ["GhostDown.gif", "GhostLeft.gif", "GhostRight.gif", "GhostUp.gif"]
            self.down = self.getFrames(image_path+directions[0],scale)
            self.left = self.getFrames(image_path+directions[1],scale)
            self.right = self.getFrames(image_path+directions[2],scale)
            self.up = self.getFrames(image_path+directions[3],scale)
            self.frames = self.left[:]
        
        else:
            self.frames = self.getFrames(image_path,scale)            
            if frame != -1:
                self.current_frame = 0
                self.frames = [self.frames[frame]] # get rid of the other frames since we dont need them

            if calculate_rotations:
                self.right = copy.copy(self.frames)
                self.up = self.rotateFrames(self.frames, 90)
                self.left = self.rotateFrames(self.frames, 180)
                self.down = self.rotateFrames(self.frames, 270)

    def getFrames(self, fileLoc:str, scale:float) -> list:
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
    
    def nextFrame(self):
        if not self.isIdle:
            self.current_frame += 1
            self.current_frame %= len(self.frames)
            self.parent.itemconfigure(self.id, image=self.frames[self.current_frame])
            self.parent.update()

    def switchFrameSet(self, frameList: list):
        self.isIdle = False
        self.frames = frameList[:]
        self.nextFrame()
        pass

    def rotateFrames(self, frames:list, theta: int) -> list:
        temp = []
        for frame in frames:
            frame = ImageTk.getimage(frame)
            frame = frame.rotate(theta)
            frame = ImageTk.PhotoImage(frame)
            temp.append(frame)

        return temp
    
    def enableIdle(self):
        self.current_frame = -1
        self.nextFrame()
        self.isIdle = True

    def disableIdle(self):
        self.isIdle = False

    def addParent(self, parent: Canvas, x, y):
        self.parent = parent
        self.id = self.parent.create_image(x, y, image=self.frames[self.current_frame], anchor="nw")

    def remove_parent(self):
        self.parent = None
        self.id = None

    def setFrame(self, frame_index):
        self.current_frame = frame_index -1
        self.nextFrame()

    def setFrameStatic(self, frame_index):
        self.current_frame = frame_index -1
        self.nextFrame()
        self.isIdle = True