from tkinter import Frame, Tk, Canvas, Event, Button, Label, Entry, Message, filedialog
import threading
import pickle
from src.animate import Animate
from src.leaderboard import Leaderboard
from src.game import Game
from src.settings import Settings
from src.player import Player

DEBUG = True

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
        self.root = root
        self.root.bind("<Key>", self.onKeyPress) # bind the canvas so when a key is pressed it runs onKeyPress

        # set up the main menu screen
        self.main_frame = Frame(self.root, highlightthickness=0)
        self.main_frame.pack(side="top", fill="both", expand = True)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.loading_thread = None

        self.current_screen_no = 0
        self.previous_screen_stack = []

        self.settings = Settings()
        self.leaderboard = Leaderboard()

        self.player = Player()

        self.frames = []

        for F in (MainMenu, NameScreen, LevelScreen, GameScreen, LeaderboardScreen, OptionScreen, BossScreen):
            
            if F is GameScreen:
                self.loading_thread = threading.Thread(target=self.instantiate_game_screen())
            else:
                frame = F(self.main_frame, self)
                frame.grid(row=0, column=0, sticky="nsew")
                self.frames.append(frame)

        self.current_frame = self.frames[0]
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame.tkraise()

        #self.current_frame = self.frames[0]
        #self.current_frame.grid(row=0, column=0, sticky="nsew")
        #self.current_frame.tkraise()

    def goToPreviousScreen(self):
        last_screen = self.previous_screen_stack.pop()
        self.switchFrame(last_screen)

    def instantiate_game_screen(self):
        print("THREAD STARTED")
        frame = GameScreen(self.main_frame, self)
        print("FRAME LOADED")
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames.insert(3,frame)
        print("FRAME INSERTED")

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

        # if we are on the boss screen then we dont add it to the stack
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

    def handle_load_save_game(self, fileLoc):
        file =  pickle.load(fileLoc)

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

        self.arrow_image = Animate(fileLoc="assets/pacman-right/1.png", parent=self.arrow, scale=2.5)

        # play button
        play_button = Button(self, text="New Game", background="#000", fg="#FFF", command=lambda: controller.switchFrame(App.screenNums["NameScreen"]))
        play_button.pack()

        self.buttonHeight = play_button.winfo_reqheight()
        # options

        Button(self, text="Load Game", background="#000", fg="#FFF", command=self.open_file_explorer).pack()

        Button(self, text="Options", background="#000", fg="#FFF", command=lambda: controller.switchFrame(App.screenNums["OptionScreen"])).pack()
        # leaderboard
        Button(self, text="Leaderboard", background="#000", fg="#FFF", command=lambda: controller.switchFrame(App.screenNums["LeaderboardScreen"])).pack()
        # exit
        Button(self, text="Exit", background="#000", fg="#FFF", command=lambda: self.controller.root.quit()).pack()

    def changeArrowSelection(self, direction: bool):  # direction False: up, True: down
        if(direction and self.selection < 3):
            self.selection += 1
            self.arrow.place(x=100, y=(self.buttonHeight * self.selection +300))

        elif(not direction and self.selection > 0):
            self.selection -= 1
            self.arrow.place(x=100, y=(self.buttonHeight * self.selection +300))

    def open_file_explorer(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
        # Change label contents
        self.controller.handle_load_save_game(filename) 

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
                case 3: self.controller.root.quit() # exit

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

        self.current_player = controller.player
        
        # add current highest score 
        Button(self, text="Back",command=lambda: controller.goToPreviousScreen()).pack()
        
        Label(self, text="Enter Name").pack()
        # add input box for the user name
        name_entry = Entry(self, font="Helvetica 11 bold",bg="white")
        name_entry.pack()
        # add submit button
        Button(self, text="Play!",command=lambda: self.nameButtonSubmit(name_entry.get())).pack()

        # back button at the top
  
    def nameButtonSubmit(self, text_entered):
        if text_entered.strip() != "":
            
            self.current_player.name = text_entered.strip() 
            
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
        self.game_canvas.pack(fill="both", expand = True)


        self.current_player = controller.player
        self.game = Game(self.game_canvas, controller.settings, controller.root, controller.player)

        self.high_score = self.controller.leaderboard.get_high_score()

        if (DEBUG):
            for i in range(36):
                for j in range(28):
                    x_0 = j*32
                    y_0 = i*32
                    x_1 = (j+1)*32
                    y_1 = (i+1)*32
                    self.game_canvas.create_rectangle((x_0, y_0), (x_1, y_1), fill="#000", outline='#FFF')

            rectanglex = self.game.pacman.canvas_position[0]
            rectangley = self.game.pacman.canvas_position[1]
            self.pacman_rectangle = self.game_canvas.create_rectangle((rectanglex,rectangley), (rectanglex+32,rectangley+32), fill="green")

            for ghost in self.game.ghosts:
                ghost_temp_rectangle_x = ghost.scatter_cell[0]*32
                ghost_temp_rectangle_y = ghost.scatter_cell[1]*32
                self.game_canvas.create_rectangle((ghost_temp_rectangle_x,ghost_temp_rectangle_y), (ghost_temp_rectangle_x+32,ghost_temp_rectangle_y+32), fill=ghost.colour)

        self.game_canvas.update()

        self.ms_delay = 17 #17


    def drawGame(self):
        self.game_canvas.children.clear()
        # player Name label
        Label(self.game_canvas, text=self.current_player.name).place(x=0, y=0)
        self.player_score_label = Label(self.game_canvas, text=self.current_player.score)
        self.player_score_label.place(x=0, y=32)

        Label(self.game_canvas, text="High Score").place(x=32, y=0)
        self.high_score_label = Label(self.game_canvas, text=self.high_score)
        self.high_score_label.place(x=32, y=32)

        Label(self.game_canvas, text="Level").place(x=32, y=0)
        self.high_score_label = Label(self.game_canvas, text=self.game.level)
        self.high_score_label.place(x=32, y=32)



        for i, row in enumerate(self.game.maze.maze):
            for j, cell in enumerate(row):
                if cell != None and hasattr(cell, "image"):
                    cell.image.addParent(self.game_canvas, x=((j)*32), y=(i*32))
        
        Pacman_pos = self.game.pacman.canvas_position
        self.game.pacman.image.addParent(self.game_canvas, x=Pacman_pos[0], y=Pacman_pos[1])
        
        for ghost in self.game.ghosts:
            ghost_pos = ghost.canvas_position
            ghost.image.addParent(self.game_canvas, x=ghost_pos[0], y=ghost_pos[1])
        
        # top level 
        #PLAYERNAME       HIGHSCORE     LEVEL
        #SCORE              SCORE         NO
        #
        #
        #
        #
        #
        #LIVES                      

        # 28 x 36 total grid. 3 at the top, 2 at the bottom
 

    # 60 fps
    def update(self):
        if self.game.isPaused:
            pass
        else:
            self.game.tick()
            # draw pac man
            pacman_pos = self.game.pacman.canvas_position
            pacman_image_id = self.game.pacman.image.id
            self.game_canvas.moveto(pacman_image_id, pacman_pos[0], pacman_pos[1])
            
            # draw ghost
            for ghost in self.game.ghosts:
                self.game_canvas.moveto(ghost.image.id, ghost.canvas_position[0], ghost.canvas_position[1])

            if DEBUG:
                rectanglex = self.game.pacman.current_cell[0]*32
                rectangley = self.game.pacman.current_cell[1]*32
                self.game_canvas.moveto(self.pacman_rectangle, rectanglex, rectangley)
            
            
            # check for win
            if self.current_player.score > self.high_score:
                self.high_score = self.current_player.score
            
            self.high_score_label.configure(text=self.high_score)
            self.player_score_label.configure(text=self.current_player.score)
            # if win then reset and change to level frame
            if self.game.dotsCounter == 244:
                # reset the game
                self.controller.switchFrame(App.screenNums["LoadingScreen"])
                
        
        self.after(self.ms_delay, self.update)
    
    def next_level(self):
        self.game.next_level()
        self.drawGame()

    def tkraise(self, aboveThis = None):
        self.drawGame()
        self.after(self.ms_delay, self.update)
        return super().tkraise(aboveThis)

    def EventHandler(self, event: Event):
        self.game.EventHandler(event)

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
         

    def EventHandler(self, event: Event):
        pass

if __name__ == "__main__":
    main = Tk()
    main.geometry("896x1170")
    main.title = "Woka Woka"
    main.resizable(width=False, height=False)
    app = App(main)
    main.mainloop()
    