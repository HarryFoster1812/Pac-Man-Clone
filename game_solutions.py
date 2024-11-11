from tkinter import *
from PIL import Image, ImageTk
import time

class App():

    def __init__(self, root) -> None:
        self.mainCanvas = Canvas(root, bg="#000", highlightthickness=0)
        self.mainCanvas.pack(fill="both", expand="true")
        self.mainMenu()
        pass

    def mainMenu(self):
        file = "assets/title/title.gif"
        # Open the image with PIL and convert to RGBA to preserve transparency
        info = Image.open(file)
        framesNo = info.n_frames
        # Extract frames and keep references
        self.photoimage_objects = [] # i spent so long just to find out that this needs to be a local attribute since python was marking it for garbage collection so no image was displaying
        for i in range(framesNo):
            info.seek(i)  # Move to the i-th frame
            frame = info.copy().convert("RGBA")
            # Convert to ImageTk.PhotoImage to preserve transparency
            obj = ImageTk.PhotoImage(frame)
            self.photoimage_objects.append(obj)

        imageTitle = Label(self.mainCanvas, image=self.photoimage_objects[0], bg="#000")
        imageTitle.pack()
        pass

    def gameScreen():
        pass

if __name__ == "__main__":
    root = Tk()
    root.geometry("960x540")
    root.title = "Woka Woka"
    app = App(root)
    root.mainloop()