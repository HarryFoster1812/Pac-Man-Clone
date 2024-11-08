from tkinter import *
from PIL import *

class App():

    def __init__(self) -> None:
        #self.currentGame = Game();
        self.mainCanvas = Canvas(root, bg="#000", highlightthickness=0).pack(fill="both", expand="true")
        pass

    def mainMenu():

        pass

    def gameScreen():
        pass

if __name__ == "__main__":
    root = Tk()
    root.geometry("960x540")
    root.title = "Woka Woka"
    app = App()
    root.mainloop()