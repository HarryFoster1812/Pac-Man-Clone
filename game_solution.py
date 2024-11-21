from tkinter import Frame, Tk, Canvas, Event, Button, Label, Entry, messagebox, filedialog
import threading
import pickle, json
from src.animate import Animate
from src.leaderboard import Leaderboard
from src.game import Game
from src.settings import Settings
from src.player import Player

DEBUG = False

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

        # i copied the level screen twice so that if the boss key is pressed it will still have the correct index
        for F in (MainMenu, NameScreen, LevelScreen, LevelScreen, LeaderboardScreen, OptionScreen, BossScreen):
            frame = F(self.main_frame, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames.append(frame)

        self.current_frame = self.frames[0]
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame.tkraise()

    def goToPreviousScreen(self):
        last_screen = self.previous_screen_stack.pop()
        self.switchFrame(last_screen)

    def instantiate_game_screen(self):
        print("THREAD STARTED")
        frame = GameScreen(self.main_frame, self)
        print("FRAME LOADED")
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[3] = frame
        print("FRAME INSERTED")
        # switch to game screen
        self.switchFrame(App.screenNums["GameScreen"])

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

    def replace_game_screen(self):
        self.frames[3] = LevelScreen(self.main_frame, self)

    def toggleBoss(self):
        if self.current_screen_no == App.screenNums["BossScreen"]:
            self.goToPreviousScreen()

        else:
            if isinstance(self.current_frame, GameScreen):
                self.current_frame.game.isPaused = True # pause the game
                print("PAUSING GAME AND SWITCHING TO BOSS SCREEN")
                self.current_frame.pause_update_thread()

            self.switchFrame( App.screenNums["BossScreen"] )

    def handle_load_save_game(self, fileLoc):
        file =  json.load(fileLoc)
        self.switchFrame(App.screenNums["GameScreen"])
        self.frames[3].game = file

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
            
            self.controller.switchFrame(App.screenNums["LevelScreen"])
        else:
            messagebox.showinfo("INFO", "You need to enter a name")
    
    def EventHandler(self, event: Event):
        pass

class LevelScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        title_label = Label(self, text="LOADING LEVEL", background="#000", fg="#FFF", font=("Ariel", 20)) # create the title label
        title_label.pack(anchor="center") 

    def check_game_screen(self):
        # check if game screen is instanciated in app
        if isinstance(self.controller.frames[3], GameScreen):
            # load new level
            self.controller.loading_thread = threading.Thread(target=self.controller.frames[3].next_level())
        else:
            self.controller.loading_thread = threading.Thread(target=self.controller.instantiate_game_screen())

    def tkraise(self, aboveThis = None):
        self.after(10, self.check_game_screen)
        return super().tkraise(aboveThis)

    def EventHandler(self, event: Event):
        pass

class GameScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller
        self.pause_menu_active = True
        self.thread_id = ""

        title_label = Label(self, image="", background="#000") # create the title label
        title_label.pack()

        self.game_canvas = Canvas(self, background="#000")
        self.game_canvas.pack(fill="both", expand = True)


        self.current_player = controller.player
        self.game = Game(controller.settings, controller.player)

        self.high_score = self.controller.leaderboard.get_high_score()

        self.lives_images = []

        self.player_score_label = None
        self.high_score_label = None
        self.level_label = None

        self.game_canvas.update()
        self.ms_delay = 17 #17

    def drawGame(self):
        # player Name label
        self.game_canvas.delete("all")

        self.lives_images.clear()

        Label(self.game_canvas, text=self.current_player.name, font=('Arial', 25), bg="#000", fg="#FFF").place(x=3*32, y=10)
        self.player_score_label = Label(self.game_canvas, text=self.current_player.score, font=('Arial', 25), bg="#000", fg="#FFF")
        self.player_score_label.place(x=3*32, y=42)

        Label(self.game_canvas, text="High Score", bg="#000", fg="#FFF", font=('Arial', 25)).place(relx=0.5, y=10, anchor="c")
        self.high_score_label = Label(self.game_canvas, text=self.high_score, bg="#000", fg="#FFF", font=('Arial', 25))
        self.high_score_label.place(relx=0.5, y=42, anchor="c")

        Label(self.game_canvas, text="Level", bg="#000", fg="#FFF", font=('Arial', 90)).place(x=23*32, y=10)
        self.level_label = Label(self.game_canvas, text=self.game.level, bg="#000", fg="#FFF", font=('Arial', 25))
        self.level_label.place(x=23*32, y=42)

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
        
        self.add_image_parents()
        for i in range(self.game.lives):
            temp = Label(self, image="", bg="#000")
            temp.place(x=(i*64+5),y=(35*32-16))
            temp_image = Animate("assets/PacManRight.gif", frame=1)
            temp_image.addParent(temp)
            self.lives_images.append([temp, temp_image])



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

    def create_pause_menu(self):
        self.pause_frame = PauseMenu(self.game_canvas, self)
        self.pause_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.pause_menu_active = True
    
    def destroy_pause_menu(self):
        self.pause_frame.destroy()
        self.pause_menu_active = False
    # 60 fps
    def update(self):
        print(self.tk.call("after", "info"))
        if self.game.isPaused:
            self.create_pause_menu()
            return
        else:
            lives_before = self.game.lives
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
            if self.game.dotsCounter == 250:
                # reset the game
                self.game.isPaused = True
                self.controller.switchFrame(App.screenNums["LevelScreen"])

            if self.game.lives == 0:
                # add game over message
                Label(self.game_canvas, text="GAME OVER", bg="#000", fg="#FFF").place(relx=.5, rely=.5, anchor="c")
                pacman_life = self.lives_images[-1]
                self.lives_images.remove(pacman_life)
                self.after(3000, self.game_over)  
                return
            
            elif self.game.lives < lives_before:
                pacman_life = self.lives_images[-1]
                self.lives_images.remove(pacman_life)
            
            elif self.game.lives > lives_before:
                temp = Label(self, image="", bg="#000")
                i = len(self.lives_images)
                temp.place(x=(i*64+5),y=(35*32-16))
                temp_image = Animate("assets/PacManRight.gif", frame=1)
                temp_image.addParent(temp)
                self.lives_images.append([temp, temp_image])
                
        
        self.thread_id = self.after(self.ms_delay, self.update)

    def add_image_parents(self):
        for i, row in enumerate(self.game.maze.maze):
            for j, cell in enumerate(row):
                if cell != None and hasattr(cell, "image"):
                    cell.image.addParent(self.game_canvas, x=((j)*32), y=(i*32))
        
        Pacman_pos = self.game.pacman.canvas_position
        self.game.pacman.image.addParent(self.game_canvas, x=Pacman_pos[0], y=Pacman_pos[1])
        
        for ghost in self.game.ghosts:
            ghost_pos = ghost.canvas_position
            ghost.image.addParent(self.game_canvas, x=ghost_pos[0], y=ghost_pos[1])
        
        self.game_canvas.tag_raise(self.game.pacman.image.id)

    def remove_image_parents(self):
        for i, row in enumerate(self.game.maze.maze):
            for j, cell in enumerate(row):
                if cell != None and hasattr(cell, "image"):
                    del cell.image
        
        del self.game.pacman.image
        
        for ghost in self.game.ghosts:
            del ghost.image


    def load_game(self, game):
        self.game = game
        # add parents to all of the images

    def game_over(self):
        self.controller.leaderboard.add_new_score(self.current_player)
        # switch to main menu
        self.controller.switchFrame(App.screenNums["MainMenu"])
        self.controller.replace_game_screen()
        # destroy its self
        self.destroy()

    def manual_unpause(self):
        self.destroy_pause_menu()
        self.game.isPaused = False
        self.thread_id = self.after(self.ms_delay, self.update)

    def pause_update_thread(self):
        self.after_cancel(self.thread_id)
        if hasattr(self, "pause_frame"):
            self.pause_frame.destroy()

    def next_level(self):
        self.pause_update_thread()
        self.game.next_level()
        self.level_label.configure(text=self.game.level)
        self.controller.switchFrame(App.screenNums["GameScreen"])

    def save_game(self):
        name = filedialog.asksaveasfilename(defaultextension=".pickle")


        with open(name, 'wb') as handle:
            for object in dir(self.game):
                pickle.dump(object, handle)

        self.add_image_parents()


    def tkraise(self, aboveThis = None):
        self.drawGame()
        self.thread_id = self.after(self.ms_delay, self.update)
        return super().tkraise(aboveThis)

    def EventHandler(self, event: Event):
        self.game.EventHandler(event)
        if not self.game.isPaused and self.pause_menu_active:
            self.destroy_pause_menu()
            self.thread_id = self.after(self.ms_delay, self.update)

class PauseMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#FFF", )

        self.controller = controller
        Label(self, text="GAME PAUSED", font=("Arial", 25), fg="#FFF", bg='#3F3').pack(anchor="center")
        # resume button
        self.resume_button = Button(self, text="Resume", command=lambda: self.controller.manual_unpause())
        self.resume_button.pack(anchor="center")
        # save button
        self.save_button = Button(self, text="Save", command=self.save_button_event)
        self.save_button.pack(anchor="center")
        # settings ?
        self.settings_button =Button(self, text="Settings", command=self.settings_button_event)
        self.settings_button.pack(anchor="center")
        # quit button
        Button(self, text="Quit", command=self.quit_button_event).pack(anchor="center")

    def save_button_event(self):
        self.controller.save_game()

    def settings_button_event(self):
        # save leaderboard Score
        self.controller.controller.switchFrame(App.screenNums["OptionScreen"])
        self.destroy()

    def quit_button_event(self):
        # save leaderboard Score
        self.controller.game_over()

    def EventHandler(self, event: Event):
        pass

class LeaderboardScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        title_label = Label(self, image="", background="#000") # create the title label
        title_label.pack() 

        self.leaderboard = controller.leaderboard

    def populate(self):
        
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="Leaderboard").pack()

        # iterate through the scores and display them
        for score in self.leaderboard.scores:
            Label(self, text=f"{score[0]}: {score[1]}", bg="#000", fg="#fff").pack()

        Button(self, text="Back", command=lambda: self.controller.goToPreviousScreen()).pack() # lambda is used because otherwise it doesnt work (i dont know why)


    def EventHandler(self, event: Event):
        if event.keysym_num == 65293: # enter key
            self.controller.goToPreviousScreen()

    def tkraise(self, aboveThis = None) -> None:
        self.populate()
        return super().tkraise(aboveThis)

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

        for i, option in enumerate(self.settings.getKeyValues()):
            option_name = option[0]
            option_info = option[1]
            Label(self, text=option_name).pack()

            self.buttons.append( Button(self, 
                                        text = f"{option_info[1]}: {option_info[0]}", 
                                        command=lambda opt=option_name, idx=i: self.buttonPress(opt, idx))
                                        )
            
            self.buttons[i].pack()
        
        Button(self, text="back", command = lambda: self.controller.goToPreviousScreen()).pack()

    def buttonPress(self, setting_name: str, clicked_button_index: int) -> None:
        self.listen = True
        self.to_change = setting_name
        self.clicked_button = clicked_button_index

    def EventHandler(self, event: Event):
        if self.listen:
            self.listen = False
            key_num = event.keysym_num
            key_name = event.keysym

            #check if key is already set
            if self.settings.key_exists(key_num):
                #display message to the user
                messagebox.showinfo("INFO", "Key entered already in use")

            else:
                self.settings.setKey(self.to_change, key_num, key_name)
                self.buttons[self.clicked_button].configure(text=f"{key_name}: {key_num}")

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
    