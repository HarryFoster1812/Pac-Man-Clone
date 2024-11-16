from PIL import Image, ImageTk
import copy

class GameImage:
    def __init__(self, image_path:str, scale:float=1, rotation: int = 0, flip:int = 0, frame: int=-1, calculateRotations:bool = False):
        self.frames = GameImage.getFrames(image_path,scale)

        self.current_frame = 0

        if calculateRotations:
            self.frames0 = copy.deepcopy(self.frames)
            self.frames90 = GameImage.rotateFrames(self.frames, 90)
            self.frames180 = GameImage.rotateFrames(self.frames, 180)
            self.frames270 = GameImage.rotateFrames(self.frames, 270)

    def getFrames(fileLoc:str, scale:float) -> list:
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
        self.current_frame += 1
        self.current_frame %= len(self.frames)

    def switchFrameSet(self, frameList: list):
        self.frames = frameList
        pass

    def rotateFrames(frames:list, theta: int) -> list:
        temp = []
        for frame in frames:
            frame = ImageTk.getimage(frame)
            frame = frame.rotate(theta)
            frame = ImageTk.PhotoImage(frame)
            temp.append(frame)

        return temp