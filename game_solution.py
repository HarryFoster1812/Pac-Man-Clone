from tkinter import *
#from tkinter.ttk import * # add styles ?
from PIL import Image, ImageTk
from src.animate import Animate
from src.leaderboard import Leaderboard
from src.game import Game
from src.settings import Settings

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
        #self.mainCanvas = Canvas(root, bg="#000", )
        root.bind("<Key>", self.onKeyPress) # bind the canvas so when a key is pressed it runs onKeyPress 

        # set up the main menu screen
        self.main_frame = Frame(root, highlightthickness=0)
        self.main_frame.pack(side="top", fill="both", expand = True)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.current_screen_no = 0
        self.previous_screen_stack = []

        self.settings = Settings()
        self.leaderboard = Leaderboard()

        self.frames = []

        for F in (MainMenu, NameScreen, LevelScreen, GameScreen, LeaderboardScreen, OptionScreen, BossScreen):
            frame = F(self.main_frame, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames.append(frame)

        self.current_frame = self.frames[0]
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame.tkraise()
    
    def updateGame(self):
        pass
        # self.game.tick()
        # loop over each entity and update positions
        # check the last interaction and remove the appropriate dots?
        # have a 2d array of the dots for the board ? 

    def goToPreviousScreen(self):
        last_screen = self.previous_screen_stack.pop()
        self.switchFrame(last_screen)

    def onKeyPress(self, event: Event):
        #check if the boss key is pressed
        if event.keysym_num == self.settings.getKey("boss_key"):  
            self.toggleBoss()

        else:
            # pass it to the approprate frame
            self.current_frame.EventHandler(event)

    def switchFrame(self, frameNo):

        # if we are on a screen with threads then we need to pause them
        # the only screen with threads are MainMenu, LevelScreen and GameScreen
        if self.current_screen_no == App.screenNums["MainMenu"]: # if we switch to a different screen then pause the threads
            self.frames[App.screenNums["MainMenu"]].toggleThreads()

        if self.current_screen_no != App.screenNums["BossScreen"]:
            self.previous_screen_stack.append(self.current_screen_no)
        self.current_screen_no = frameNo
        self.current_frame = self.frames[frameNo]
        self.current_frame.tkraise()


    def toggleBoss(self):
        if self.current_screen_no == App.screenNums["BossScreen"]:
            self.goToPreviousScreen()

        else:
            self.switchFrame( App.screenNums["BossScreen"] )

class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        title_label = Label(self, image="", background="#000") # create the title label
        title_label.pack()

        for_legal_label = Label(self, image="", background="#000") # create the for legal label
        for_legal_label.pack()

        # load the title image and animate it
        self.title_image = Animate("assets/title/title.gif", title_label, scale=1.1)
        self.for_legal_image = Animate("assets/title/forLegal.gif", for_legal_label, scale=1.1)

        arrow_start_y = for_legal_label.winfo_pointery() + for_legal_label.winfo_reqheight()
        print(arrow_start_y)

        
        # add current arrow
        self.selection = 0 # will determine where the arrow will be

        self.arrow = Label(self, image="", background="#000")
        self.arrow.place(x=100, y=(90*self.selection + arrow_start_y))

        self.arrowImage = Animate(fileLoc="assets/pacman-right/1.png", parent=self.arrow, scale=2.5)

        # play button
        play_button = Button(self, text="Play", background="#000", fg="#FFF", command=lambda: controller.switchFrame(App.screenNums["NameScreen"]))
        play_button.pack()

        self.buttonHeight = play_button.winfo_reqheight()
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

    def toggleThreads(self):
        self.title_image.toggleAnimation()
        self.for_legal_image.toggleAnimation()

    def tkraise(self, aboveThis = None):
        self.toggleThreads()
        return super().tkraise(aboveThis)
    

class NameScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        title_label = Label(self, image="", background="#000") # create the title label
        title_label.pack()
        
        Button(self, text="Back",command=lambda: controller.goToPreviousScreen()).pack()
        # add current highest score 
        
        Label(self, text="Enter Name").pack()
        # add input box for the user name
        name_entry = Entry(self, font="Helvetica 11 bold",bg="white")
        name_entry.place(x=0, y=0)
        # add submit button
        Button(self, text="Play!",command=lambda: self.nameButtonSubmit(name_entry.get())).pack()

        # back button at the top
  
    def nameButtonSubmit(self, text_entered):
        if text_entered.strip() != "":
            # add new entry to scores
            # add name to entry
            self.controller.switchFrame(App.screenNums["GameScreen"])
        else:
            Message(self, text="You need to enter a name").pack()
    
    def EventHandler(self, event: Event):
        pass

class LevelScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        title_label = Label(self, image="", background="#000") # create the title label
        title_label.pack()
        pass 

    def EventHandler(self, event: Event):
        pass

class GameScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        title_label = Label(self, image="", background="#000") # create the title label
        title_label.pack()

        self.game_canvas = Canvas(self, background="#000")
        self.game_canvas.pack()

        self.game = Game(self.game_canvas, controller.settings)

        self.drawGame()

    def drawGame(self):
        Button(self.game_canvas, text = "test").grid(row=35, column=28)
        # top level 
        #1up       HIGHSCORE
        #PLAYER      SCORE
        #
        #
        #
        #
        #
        #LIVES                      AVAILIBLE POWERUPS

        # 28 x 36 total grid. 3 at the top, 2 at the bottom

        pass 

    def EventHandler(self, event: Event):
        pass

class LeaderboardScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        title_label = Label(self, image="", background="#000") # create the title label
        title_label.pack()

        self.leaderboard = controller.leaderboard

        Label(self, text="Leaderboard").pack()

        # iterate through the scores and display them
        for score in self.leaderboard.scores:
            Label(self, text=f"{score[0]}: {score[1]}", bg="#000", fg="#fff").pack()

        Button(self, text="Back", command=lambda: controller.goToPreviousScreen()).pack() # lambda is used because otherwise it doesnt work (i dont know why)

    def EventHandler(self, event: Event):
        if event.keysym_num == 65293: # enter key
            self.controller.goToPreviousScreen()

class OptionScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        self.settings =  controller.settings

        self.listen = False # will become true when a button is clicked 
        self.to_change = "" # the setting key to change
        self.clicked_button = None

        title_label = Label(self, image="", background="#000") # create the title label
        title_label.pack()

        self.buttons = []

        for option in enumerate(self.settings.getKeyValues()):
            button_index = option[0]
            Label(self, text=option[1][0]).pack()
            self.buttons.append( Button(self, text = option[1][1], command=lambda opt=option[1][0], idx=button_index: self.buttonPress(opt, idx)))
            self.buttons[button_index].pack()
        
        Button(self, text="back", command = lambda: self.controller.goToPreviousScreen()).pack()

    def buttonPress(self, setting_name: str, clicked_button_index: int) -> None:
        self.listen = True
        self.to_change = setting_name
        self.clicked_button = clicked_button_index

    def EventHandler(self, event: Event):
        if self.listen:
            self.listen = False
            key_num = event.keysym_num
            self.settings.setKey(self.to_change, key_num)
            self.buttons[self.clicked_button].configure(text=key_num)

class BossScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        title_label = Label(self, image="", background="#000") # create the title label
        title_label.pack()
        pass 

    def EventHandler(self, event: Event):
        pass

if __name__ == "__main__":
    root = Tk()
    root.geometry("896x1152")
    root.title = "Woka Woka"
    root.resizable(width=False, height=False)
    app = App(root)
    root.mainloop()