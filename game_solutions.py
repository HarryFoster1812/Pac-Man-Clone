from tkinter import *
from PIL import Image, ImageTk
from src.animate import Animate

class App():

    def __init__(self, root) -> None:
        self.mainCanvas = Canvas(root, bg="#000", highlightthickness=0)
        self.mainCanvas.pack(fill="both", expand="true")
        self.mainMenu()

        self.cleanUp = [] # add a list of attributes that need to be collected when switching to another screen
        pass

    def mainMenu(self):

        titleLabel = Label(self.mainCanvas, image="", bg="#000")
        titleLabel.pack()

        forLegalLabel = Label(self.mainCanvas, image="", bg="#000")
        forLegalLabel.pack()

        self.title = Animate("assets/title/title.gif", titleLabel)
        self.forLegal = Animate("assets/title/forLegal.gif", forLegalLabel)

        # add current arrow

        # play button

        # options

        # leaderboard

        # exit

        pass

    def nameScreen(self):

        # add current highest score 

        # add input box for the user name

        # add validation

        # add submit button

        # switch to game screen

        # back button at the top

    def gameScreen():
        raise NotImplementedError()

if __name__ == "__main__":
    root = Tk()
    root.geometry("960x540")
    root.title = "Woka Woka"
    app = App(root)
    root.mainloop()