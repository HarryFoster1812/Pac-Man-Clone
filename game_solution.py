from tkinter import *
#from tkinter.ttk import * # add styles ?
from PIL import Image, ImageTk
from src.animate import Animate
from src.leaderboard import Leaderboard


###################################
# reformat so each page is its own frame and the app serves as the controller just allowing the individual frames to be switched


class App():

    #mainCanvas = None
    #currentScreen = 0 # 0 - main menu, 1 - game screen, 2 - settings, 3 - leaderboard, 4 - boss screen, 5 - name screen, 6 - intermediate
    #previousScreen = [] it is essentially a stack

    screenNums = {
        "MainMenu"         : 0,
        "NameScreen"       : 1, 
        "LevelScreen"      : 2, 
        "GameScreen"       : 3, 
        "LeaderboardScreen": 4, 
        "OptionScreen"     : 5, 
        "BossScreen"       : 6
    }


    def __init__(self, root: Tk) -> None:
        #self.mainCanvas = Canvas(root, bg="#000", highlightthickness=0)
        #self.mainCanvas.pack(fill="both", expand="true", ) 
        root.bind("<Key>", self.onKeyPress) # bind the canvas so when a key is pressed it runs onKeyPress 

        # set up the main menu screen
        self.main_frame = Frame(root)
        self.main_frame.pack(side="top", fill="both", expand = True)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.currentScreenNo = 0
        self.previousScreenStack = []

        self.frames = []

        for F in (MainMenu, NameScreen, LevelScreen, GameScreen, LeaderboardScreen, OptionScreen, BossScreen):
            frame = F(self.main_frame, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames.append(frame)

        self.currentFrame = self.frames[0]
        self.currentFrame.grid(row=0, column=0, sticky="nsew")
        self.currentFrame.tkraise()
    
    def updateGame(self):
        pass
        # self.game.tick()
        # loop over each entity and update positions
        # check the last interaction and remove the appropriate dots?
        # have a 2d array of the dots for the board ? 

    def goToPreviousScreen(self):
        last_screen = self.previousScreenStack.pop()
        self.currentScreenNo = last_screen

        self.currentFrame = self.frames[last_screen]
        self.currentFrame.tkraise()

    def onKeyPress(self, event: Event):
        #check if the boss key is pressed
        if event.keysym_num == 'boss key not implemented':  
            self.toggleBoss()
            # when the frame approach is implemented change the frame to the bossFrame

        else:
            # pass it to the approprate frame
            self.currentFrame.EventHandler(event)

    def switchFrame(self, frameNo):
        self.previousScreenStack.append(self.currentScreenNo)
        self.currentScreenNo = frameNo
        self.currentFrame = self.frames[frameNo]
        self.currentFrame.tkraise()

    def toggleBoss(self):
        if self.currentScreen == 4:
            self.goToPreviousScreen()

        else:
            self.previousScreenStack.append(self.currentScreen)
            self.switchFrame("")

class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        titleLabel = Label(self, image="", background="#000") # create the title label
        titleLabel.pack()

        forLegalLabel = Label(self, image="", background="#000") # create the for legal label
        forLegalLabel.pack()

        # load the title image and animate it
        self.title = Animate("assets/title/title.gif", titleLabel)
        self.forLegal = Animate("assets/title/forLegal.gif", forLegalLabel)

        # add current arrow
        self.selection = 0 # this is where the arrow will be

        self.arrow = Label(self, image="", background="#000")
        self.arrow.place(x=100, y=(90*self.selection +300))

        self.arrowImage = Animate(fileLoc="assets/pacman-right/1.png", parent=self.arrow, scale=2.5)

        # play button
        playButton = Button(self, text="Play", background="#000", fg="#FFF", command=lambda: controller.switchFrame(App.screenNums["NameScreen"]))
        playButton.pack()

        self.buttonHeight = playButton.winfo_reqheight()
        # options
        Button(self, text="Options", background="#000", fg="#FFF", command=lambda: controller.switchFrame(App.screenNums["OptionScreen"])).pack()
        # leaderboard
        Button(self, text="Leaderboard", background="#000", fg="#FFF", command=lambda: controller.switchFrame(App.screenNums["LeaderboardScreen"])).pack()
        # exit
        Button(self, text="Exit", background="#000", fg="#FFF", command=lambda: root.quit()).pack()

    def changeArrowSelection(self, direction: bool):  # direction False: up, True: down
        if(direction and self.selection < 3):
            self.selection += 1
            self.arrow.place(x=100, y=(self.buttonHeight * self.selection +300))

        elif(not direction and self.selection > 0):
            self.selection -= 1
            self.arrow.place(x=100, y=(self.buttonHeight * self.selection +300))     

    def EventHandler(self, event: Event):
        if event.keysym_num == 65364: # down arrow
            self.changeArrowSelection(True)
        
        elif event.keysym_num == 65362: # up arrow
            self.changeArrowSelection(False)
        
        elif event.keysym_num == 65293: # enter key
            match(self.selection):
                case 0: self.controller.switchFrame(App.screenNums["NameScreen"]) # name screen
                case 1: self.controller.switchFrame(App.screenNums["OptionScreen"]) # options
                case 2: self.controller.switchFrame(App.screenNums["LeaderboardScreen"]) # leaderboard
                case 3: root.quit() # exit

class NameScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        titleLabel = Label(self, image="", background="#000") # create the title label
        titleLabel.pack()
        
        Button(self, text="Back",command=lambda: controller.goToPreviousScreen()).pack()
        # add current highest score 
        
        Label(self, text="Enter Name").pack()
        # add input box for the user name
        name_entry = Entry(self, font="Helvetica 11 bold",bg="white")
        name_entry.place(x=0, y=0)
        # add submit button
        Button(self, text="Play!",command=lambda: self.nameButtonSubmit(name_entry.get())).pack()

        # back button at the top
  
    def nameButtonSubmit(self, textEntered):
        if textEntered.strip() != "":
            # add new entry to scores
            # add name to entry
            self.controller.switchFrame(App.screenNums["LevelScreen"])
        else:
            Message(root, text="You need to enter a name").pack()
    
    def EventHandler(self, event: Event):
        pass

class LevelScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        titleLabel = Label(self, image="", background="#000") # create the title label
        titleLabel.pack()
        pass 

    def EventHandler(self, event: Event):
        pass

class GameScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        titleLabel = Label(self, image="", background="#000") # create the title label
        titleLabel.pack()
        pass 

    def EventHandler(self, event: Event):
        pass

class LeaderboardScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        titleLabel = Label(self, image="", background="#000") # create the title label
        titleLabel.pack()

        self.leaderboard = Leaderboard()

        Label(self, text="Leaderboard").pack()

        # iterate through the scores and display them
        for score in self.leaderboard.scores:
            Label(self, text=f"{score[0]}: {score[1]}", bg="#000").pack()

        Button(self, text="Back", command=lambda: controller.goToPreviousScreen()).pack() # lambda is used because otherwise it doesnt work (i dont know why)

    def EventHandler(self, event: Event):
        if event.keysym_num == 65293: # enter key
            self.controller.goToPreviousScreen()

class OptionScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        titleLabel = Label(self, image="", background="#000") # create the title label
        titleLabel.pack()
        pass 

    def EventHandler(self, event: Event):
        pass

class BossScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        titleLabel = Label(self, image="", background="#000") # create the title label
        titleLabel.pack()
        pass 

    def EventHandler(self, event: Event):
        pass

if __name__ == "__main__":
    root = Tk()
    root.geometry("960x540")
    root.title = "Woka Woka"
    app = App(root)
    root.mainloop()