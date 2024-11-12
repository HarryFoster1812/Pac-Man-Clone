from tkinter import *
#from tkinter.ttk import * # add styles ?
from PIL import Image, ImageTk
from src.animate import Animate
from src.leaderboard import Leaderboard

class App():

    #mainCanvas = None
    #currentScreen = 0 # 0 - main menu, 1 - game screen, 2 - settings, 3 - leaderboard, 4 - boss screen, 5 - name screen
    #previousScreen = 0

    def __init__(self, root) -> None:
        self.mainCanvas = Canvas(root, bg="#000", highlightthickness=0)
        self.mainCanvas.pack(fill="both", expand="true", ) 
        root.bind("<Key>", self.onKeyPress) # bind the canvas so when a key is pressed it runs onKeyPress 

        self.currentScreen = 0 # set the current screen to the main menu
        self.mainMenu() # set up the main menu screen


        #self.game = Game()
        # let the game have a leaderboard object and access it from there
        # let the game have a settings object and access it from there

        self.cleanUp = [] # add a list of attributes that need to be collected when switching to another screen
        pass

    def mainMenu(self):
        self.clearCanvas()
        self.currentScreen = 0
        titleLabel = Label(self.mainCanvas, image="", background="#000") # create the title label
        titleLabel.pack()

        forLegalLabel = Label(self.mainCanvas, image="", background="#000") # create the for legal label
        forLegalLabel.pack()

        # load the title image and animate it
        self.title = Animate("assets/title/title.gif", titleLabel) 
        self.forLegal = Animate("assets/title/forLegal.gif", forLegalLabel)  

        # add current arrow
        self.selection = 0 # this is where the arrow will be

        self.arrow = Label(self.mainCanvas, image="", background="#000")
        self.arrow.place(x=100, y=(90*self.selection +300))

        self.arrowImage = Animate(fileLoc="assets/pacman-right/1.png", parent=self.arrow, scale=2.5)

        self.buttonHeight = 0

        # play button
        playButton = Button(self.mainCanvas, text="Play", background="#000", fg="#FFF")
        playButton.pack()

        self.buttonHeight = playButton.winfo_reqheight()
        # options
        Button(self.mainCanvas, text="Options", background="#000", fg="#FFF").pack()
        # leaderboard
        Button(self.mainCanvas, text="Leaderboard", background="#000", fg="#FFF", command=self.leaderBoardScreen).pack()
        # exit
        Button(self.mainCanvas, text="Exit", background="#000", fg="#FFF", command=lambda: root.quit()).pack()

    def mainMenuEventHandler(self, event):
        if event.keysym_num == 65364: # down arrow
            self.changeArrowSelection(True)
        
        elif event.keysym_num == 65362: # up arrow
            self.changeArrowSelection(False)
        
        elif event.keysym_num == 65293: # enter key
            match(self.selection):
                case 0: pass # name screen
                case 1: pass # options
                case 2: self.leaderBoardScreen() # leaderboard
                case 3: root.quit() # exit

    def changeArrowSelection(self, direction: bool):  # direction False: up, True: down
        if(direction and self.selection < 3):
            self.selection += 1
            self.arrow.place(x=100, y=(self.buttonHeight * self.selection +300))

        elif(not direction and self.selection > 0):
            self.selection -= 1
            self.arrow.place(x=100, y=(self.buttonHeight * self.selection +300))     

    def nameScreen(self):
        pass
        # add current highest score 

        # add input box for the user name

        # add validation

        # add submit button

        # switch to game screen

        # back button at the top

    def leaderBoardScreen(self):
        self.clearCanvas()
        
        self.previousScreen = self.currentScreen
        self.currentScreen = 3

        self.leaderboard = Leaderboard()

        Label(self.mainCanvas, text="Leaderboard").pack()

        # iterate through the scores and display them
        for score in self.leaderboard.scores:
            Label(self.mainCanvas, text=f"{score[0]}: {score[1]}").pack()

        Button(self.mainCanvas, text="Exit", command=lambda: self.goToPreviousScreen()).pack() # lambda is used because otherwise it doesnt work (i dont know why)

    def leaderboardEventHandler(self, event):
        if event.keysym_num == 65293: # enter key
            self.goToPreviousScreen()

    def clearCanvas(self):
        for child in self.mainCanvas.winfo_children():
            child.destroy() # make sure to destroy it so the memory is freed

    def onKeyPress(self, event):
        #check if the boss key is pressed
        if event.keysym_num == 'boss key not implemented':  
            self.toggleBoss()

        else:
            match(self.currentScreen):
                case 0: self.mainMenuEventHandler(event)
                case 1: self.gameScreenEventHandler(event)
                case 2: self.settingsEventHandler(event)
                case 3: self.leaderboardEventHandler(event)
                case 4: self.bossEventHandler(event)
        
    def toggleBoss(self):
        if self.currentScreen == 4:
            self.currentScreen = self.previousScreen
            # add logic to switch back to the old screen (unpause game as well)

        else:
            self.previousScreen = self.currentScreen
            self.bossScreen()

    def gameScreen(self):
        raise NotImplementedError()
    
    def bossScreen(self):
        raise NotImplementedError()    
    
    def goToPreviousScreen(self):
        match (self.previousScreen):
            case 1: self.gameScreen()
            case 2: self.settingsScreen()
            case 3: self.leaderBoardScreen()
            case _: self.mainMenu() 

if __name__ == "__main__":
    root = Tk()
    root.geometry("960x540")
    root.title = "Woka Woka"
    app = App(root)
    root.mainloop()