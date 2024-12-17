from tkinter import Frame, Tk, Canvas, Event, Button, Label, Entry, messagebox, filedialog, Scrollbar, Text, END
from tkinter import ttk
import threading
import json
from src.animate import Animate
from src.leaderboard import Leaderboard
from src.game import Game
from src.settings import Settings
from src.player import Player

DEBUG = False


class App():

    # mainCanvas = None
    # currentScreen = 0 # 0 - main menu, 1 - game screen, 2 - settings, 3 - leaderboard, 4 - boss screen, 5 - name screen, 6 - intermediate
    # previousScreen = [] it is essentially a stack

    screenNums = {
        "MainMenu": 0,
        "NameScreen": 1,
        "LevelScreen": 2,
        "GameScreen": 3,
        "LeaderboardScreen": 4,
        "OptionScreen": 5,
        "BossScreen": 6
    }

    def __init__(self, root: Tk) -> None:
        # self.mainCanvas = Canvas(root, bg="#000", )
        self.root = root
        # bind the canvas so when a key is pressed it runs onKeyPress
        self.root.bind("<Key>", self.onKeyPress)

        # set up the main menu screen
        self.main_frame = Frame(self.root, highlightthickness=0)
        self.main_frame.pack(side="top", fill="both", expand=True)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.loading_thread = None
        self.load_game = False
        self.load_data = None

        self.current_screen_no = 0
        self.previous_screen_stack = []

        self.settings = Settings()
        self.leaderboard = Leaderboard()

        self.player = Player()

        self.frames = []

        # i copied the level screen twice so that if the boss key is pressed it
        # will still have the correct index
        for F in (
                MainMenu,
                NameScreen,
                LevelScreen,
                LevelScreen,
                LeaderboardScreen,
                OptionScreen,
                BossScreen):
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
        #print("THREAD STARTED")
        frame = GameScreen(self.main_frame, self)
        #print("FRAME LOADED")
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[3] = frame
        #print("FRAME INSERTED")
        # switch to game screen
        if self.load_game:
            self.load_game = False
            self.frames[3].game.parse(self.load_data)
            self.load_data = None

        self.switchFrame(App.screenNums["GameScreen"])

    def onKeyPress(self, event: Event):
        # check if the boss key is pressed
        if event.keysym_num == self.settings.getKey("boss_key"):
            self.toggleBoss()

        else:
            # pass it to the approprate frame
            self.current_frame.EventHandler(event)

    def switchFrame(self, frameNo):

        # if we are on a screen with threads then we need to pause them
        # the only screen with threads are MainMenu, LevelScreen and GameScreen
        # if we switch to a different screen then pause the threads
        if self.current_screen_no == App.screenNums["MainMenu"]:
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
                self.current_frame.game.isPaused = True  # pause the game
                #print("PAUSING GAME AND SWITCHING TO BOSS SCREEN")
                self.current_frame.pause_update_thread()

            self.switchFrame(App.screenNums["BossScreen"])

    def handle_load_save_game(self, fileLoc):
        with open(fileLoc, "r") as json_file:
            data = json.load(json_file)

        self.load_game = True
        self.load_data = data
        self.switchFrame(App.screenNums["LevelScreen"])


class MainMenu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        # create the title label
        title_label = Label(self, image="", background="#000")
        title_label.pack()

        # create the for legal label
        for_legal_label = Label(self, image="", background="#000")
        for_legal_label.pack()

        # load the title image and animate it
        self.title_image = Animate(
            "assets/title/title.gif", title_label, scale=1.1)
        self.for_legal_image = Animate(
            "assets/title/forLegal.gif",
            for_legal_label,
            scale=1.1)

        arrow_start_y = 340
        #print(arrow_start_y)

        # add current arrow
        self.selection = 0  # will determine where the arrow will be

        self.arrow = Label(self, image="", background="#000")
        self.arrow.place(x=100, y=arrow_start_y)

        self.arrow_image = Animate(
            fileLoc="assets/pacman-right/1.png",
            parent=self.arrow,
            scale=2.5)

        # Utility function for buttons
        def create_button(text, command):
            return Button(
                self,
                text=text,
                bg="#444",
                fg="#FFF",
                font=(
                    'Liberation Mono',
                    20,
                    "bold"),
                activebackground="#666",
                activeforeground="#FFF",
                pady=10,
                padx=20,
                bd=2,
                relief="raised",
                command=command)

        # Play button
        play_button = create_button(
            "New Game", lambda: controller.switchFrame(
                App.screenNums["NameScreen"]))
        play_button.pack(pady=10)

        self.buttonHeight = play_button.winfo_reqheight()

        # Load Game button
        load_button = create_button("Load Game", self.open_file_explorer)
        load_button.pack(pady=10)

        # Options button
        options_button = create_button(
            "Options", lambda: controller.switchFrame(
                App.screenNums["OptionScreen"]))
        options_button.pack(pady=10)

        # Leaderboard button
        leaderboard_button = create_button(
            "Leaderboard", lambda: controller.switchFrame(
                App.screenNums["LeaderboardScreen"]))
        leaderboard_button.pack(pady=10)

        # Exit button
        exit_button = create_button(
            "Exit", lambda: self.controller.root.quit())
        exit_button.pack(pady=10)

    # direction False: up, True: down
    def changeArrowSelection(self, direction: bool):
        if (direction and self.selection < 4):
            self.selection += 1

        elif (not direction and self.selection > 0):
            self.selection -= 1

        self.arrow.place(
            x=100, y=((self.buttonHeight + 20) * (self.selection) + 340))

    def open_file_explorer(self):
        filename = filedialog.askopenfilename(title="Select a File",
                                              filetypes=(("JSON files",
                                                          "*.json*"),
                                                         ("all files",
                                                          "*.*")))

        # Change label contents
        self.controller.handle_load_save_game(filename)

    def EventHandler(self, event: Event):
        if event.keysym_num == 65364:  # down arrow
            self.changeArrowSelection(True)

        elif event.keysym_num == 65362:  # up arrow
            self.changeArrowSelection(False)

        elif event.keysym_num == 65293:  # enter key
            match(self.selection):
                # name screen
                case 0: self.controller.switchFrame(App.screenNums["NameScreen"])
                case 1: self.open_file_explorer()
                # options
                case 2: self.controller.switchFrame(App.screenNums["OptionScreen"])
                # leaderboard
                case 3: self.controller.switchFrame(App.screenNums["LeaderboardScreen"])
                case 4: self.controller.root.quit()  # exit

    def toggleThreads(self):
        self.title_image.toggleAnimation()
        self.for_legal_image.toggleAnimation()

    def tkraise(self, aboveThis=None):
        self.toggleThreads()
        return super().tkraise(aboveThis)


class NameScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        self.current_player = controller.player

        # Center everything in a Frame
        self.center_frame = Frame(self, bg="#000")
        self.center_frame.pack(
            expand=True,
            fill="both",
            padx=40,
            pady=40)  # Expand to fill the screen

        self.title_label = Label(
            self.center_frame,
            text="Enter Your Name",
            font=(
                'Liberation Mono',
                24,
                "bold"),
            bg="#000",
            fg="#FFD700",
            pady=20)
        self.title_label.pack()

        # Input box for the user name
        self.name_entry = Entry(
            self.center_frame,
            font=(
                'Liberation Mono',
                16),
            bg="#FFF",
            fg="#000",
            bd=2,
            relief="solid")
        self.name_entry.pack(
            pady=20,
            ipadx=10,
            ipady=10,
            fill="x",
            expand=True)

        # Play Button (Centered)
        self.play_button = Button(
            self.center_frame,
            text="Play!",
            bg="#3A3",
            fg="#FFF",
            font=(
                'Liberation Mono',
                16,
                "bold"),
            activebackground="#5A5",
            activeforeground="#FFF",
            bd=2,
            relief="raised",
            command=lambda: self.nameButtonSubmit(
                self.name_entry.get()))
        self.play_button.pack(pady=20)

        # Back Button (Centered)
        self.back_button = Button(
            self.center_frame,
            text="Back",
            bg="#444",
            fg="#FFF",
            font=(
                'Liberation Mono',
                14),
            activebackground="#666",
            activeforeground="#FFF",
            bd=2,
            relief="raised",
            command=lambda: self.controller.goToPreviousScreen())
        self.back_button.pack(pady=10)

    def nameButtonSubmit(self, text_entered):
        if text_entered.strip() != "":

            self.current_player.name = text_entered.strip()
            self.current_player.score = 0

            self.controller.switchFrame(App.screenNums["LevelScreen"])
        else:
            messagebox.showinfo("INFO", "You need to enter a name")

    def EventHandler(self, event: Event):
        pass


class LevelScreen(Frame):
    def __init__(self, parent, controller):
        # Dark background for consistency
        Frame.__init__(self, parent, bg="#222")
        self.controller = controller

        self.load = False
        self.data = None

        self.inner_frame = Frame(self, bg="#000")
        self.inner_frame.pack(expand=True, fill="both")

        self.title_label = Label(
            self.inner_frame,
            text="Loading Level...",
            font=(
                'Liberation Mono',
                24,
                "bold"),
            bg="#000",
            fg="#FFD700",
            pady=20)  # Golden color for emphasis
        self.title_label.pack(pady=50)

        # Animated Loading Icon (Centered)
        self.loading_label = Label(self.inner_frame, bg="#000")
        self.loading_label.pack(pady=20)
        self.loading_animation = Animate(
            "assets/loading.gif", self.loading_label, scale=1.5)

        # Subtext Instruction (Centered)
        self.instruction_label = Label(
            self.inner_frame,
            text="Please wait while the next level is prepared.",
            font=(
                'Liberation Mono',
                12,
                "italic"),
            bg="#000",
            fg="#AAA",
            pady=10)
        self.instruction_label.pack(pady=20)

    def check_game_screen(self):
        """Checks if the game screen is ready and initiates the loading process."""
        if isinstance(self.controller.frames[3], GameScreen):
            # If the game screen exists, prepare for the next level
            self.controller.loading_thread = threading.Thread(
                target=self.controller.frames[3].next_level)
            self.controller.loading_thread.start()
        else:
            # Instantiate a new game screen
            self.controller.loading_thread = threading.Thread(
                target=self.controller.instantiate_game_screen)
            self.controller.loading_thread.start()

    def update_loading_animation(self):
        """Ensures the loading animation continues while the background thread works."""
        self.loading_animation.toggleAnimation()  # Toggle animation state
        # Recheck the thread every 100ms
        self.after(100, self.check_loading_thread)

    def check_loading_thread(self):
        """Checks if the loading thread has finished, and updates accordingly."""
        if self.controller.loading_thread.is_alive():
            self.update_loading_animation()  # Keep updating if thread is still alive
        else:
            # Once the thread is done, stop the animation and switch the screen
            self.loading_animation.toggleAnimation()

    def tkraise(self, aboveThis=None):
        """Refreshes the screen and starts the loading process."""
        self.after(5, self.check_game_screen)
        self.update_loading_animation()  # Start the animation update
        return super().tkraise(aboveThis)

    def EventHandler(self, event: Event):
        pass


class GameScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000", bd=0)

        self.controller = controller
        self.pause_menu_active = True
        self.thread_id = ""

        self.game_canvas = Canvas(
            self, background="#000", highlightthickness=0)
        self.game_canvas.pack(fill="both", expand=True)

        self.current_player = controller.player
        self.game = Game(controller.settings, controller.player)

        self.high_score = self.controller.leaderboard.get_high_score()

        self.lives_images = []

        self.player_score_label = None
        self.high_score_label = None
        self.level_label = None

        self.game_canvas.update()
        self.ms_delay = 17  # 17

    def drawGame(self):
        # player Name label
        self.game_canvas.delete("all")

        self.lives_images.clear()

        # Modern font and colors for the labels
        label_font = ("Liberation Mono", 16, "bold")
        label_fg = "#FFF"  # White text for visibility
        label_bg = "#000"

        # Player Name Label (Left side)
        self.player_name_label = Label(
            self.game_canvas,
            text=self.current_player.name,
            font=label_font,
            fg=label_fg,
            bg=label_bg,
            padx=15,
            pady=10,
            relief="solid")
        self.player_name_label.place(x=2 * 32, y=10, anchor="w")

        # Player Score Label (Left side, below player name)
        self.player_score_label = Label(
            self.game_canvas,
            text=self.current_player.score,
            font=label_font,
            fg=label_fg,
            bg=label_bg,
            padx=15,
            pady=10,
            relief="solid")
        self.player_score_label.place(x=3 * 32, y=70, anchor="center")

        # High Score Label (Centered in the middle of the screen)
        self.high_score_label = Label(
            self.game_canvas,
            text="High Score",
            font=label_font,
            fg=label_fg,
            bg=label_bg,
            padx=15,
            pady=10,
            relief="solid")
        self.high_score_label.place(
            relx=0.5, y=17, anchor="center")  # Centering the label

        # High Score Value (Below the High Score label, centered)
        self.high_score_value_label = Label(
            self.game_canvas,
            text=f"{self.high_score}",
            font=label_font,
            fg=label_fg,
            bg=label_bg,
            padx=15,
            pady=10,
            relief="solid")
        self.high_score_value_label.place(
            relx=0.5, y=70, anchor="center")  # Below the High Score label

        # Level Label (Right side)
        self.level_label = Label(
            self.game_canvas,
            text="Level",
            font=label_font,
            fg=label_fg,
            bg=label_bg,
            padx=15,
            pady=10,
            relief="solid")
        # Right side of the screen
        self.level_label.place(x=26 * 32, y=17, anchor="center")
        self.level_label = Label(
            self.game_canvas,
            text=self.game.level,
            font=label_font,
            fg=label_fg,
            bg=label_bg,
            padx=15,
            pady=10,
            relief="solid")
        # Right side of the screen
        self.level_label.place(x=26 * 32, y=70, anchor="center")

        if (DEBUG):
            for i in range(36):
                for j in range(28):
                    x_0 = j * 32
                    y_0 = i * 32
                    x_1 = (j + 1) * 32
                    y_1 = (i + 1) * 32
                    self.game_canvas.create_rectangle(
                        (x_0, y_0), (x_1, y_1), fill="#000", outline='#FFF')

            rectanglex = self.game.pacman.canvas_position[0]
            rectangley = self.game.pacman.canvas_position[1]
            self.pacman_rectangle = self.game_canvas.create_rectangle(
                (rectanglex, rectangley), (rectanglex + 32, rectangley + 32), fill="green")

            for ghost in self.game.ghosts:
                ghost_temp_rectangle_x = ghost.scatter_cell[0] * 32
                ghost_temp_rectangle_y = ghost.scatter_cell[1] * 32
                self.game_canvas.create_rectangle(
                    (ghost_temp_rectangle_x,
                     ghost_temp_rectangle_y),
                    (ghost_temp_rectangle_x + 32,
                     ghost_temp_rectangle_y + 32),
                    fill=ghost.colour)

        self.add_image_parents()
        for i in range(self.game.lives):
            temp = Label(self, image="", bg="#000")
            temp.place(x=(i * 64 + 5), y=(35 * 32 - 16))
            temp_image = Animate("assets/PacManRight.gif", frame=1)
            temp_image.addParent(temp)
            self.lives_images.append([temp, temp_image])

        # top level
        # PLAYERNAME       HIGHSCORE     LEVEL
        # SCORE              SCORE         NO
        #
        #
        #
        #
        #
        # LIVES

        # 28 x 36 total grid. 3 at the top, 2 at the bottom

    def create_pause_menu(self):
        self.pause_frame = PauseMenu(self.game_canvas, self)
        self.pause_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.pause_menu_active = True
        self.after_cancel(self.thread_id)

    def destroy_pause_menu(self):
        self.pause_frame.destroy()
        self.pause_menu_active = False
    # 60 fps

    def update(self):
        #print(self.tk.call("after", "info"))
        if self.game.isPaused:
            self.create_pause_menu()
            return
        else:
            lives_before = self.game.lives
            self.game.tick()
            # draw pac man
            pacman_pos = self.game.pacman.canvas_position
            pacman_image_id = self.game.pacman.image.id
            self.game_canvas.moveto(
                pacman_image_id, pacman_pos[0], pacman_pos[1])

            # draw ghost
            for ghost in self.game.ghosts:
                self.game_canvas.moveto(
                    ghost.image.id,
                    ghost.canvas_position[0],
                    ghost.canvas_position[1])

            if DEBUG:
                rectanglex = self.game.pacman.current_cell[0] * 32
                rectangley = self.game.pacman.current_cell[1] * 32
                self.game_canvas.moveto(
                    self.pacman_rectangle, rectanglex, rectangley)

            # check for win
            if self.current_player.score > self.high_score:
                self.high_score = self.current_player.score

            self.high_score_value_label.configure(text=self.high_score)
            self.player_score_label.configure(text=self.current_player.score)
            # if win then reset and change to level frame
            if self.game.dotsCounter == 250:
                # reset the game
                self.game.isPaused = True
                self.controller.switchFrame(App.screenNums["LevelScreen"])

            if self.game.lives == 0:
                # add game over message
                Label(
                    self.game_canvas,
                    text="GAME OVER",
                    bg="#000",
                    fg="#FFF",
                    font=(
                        'liberation mono',
                        30)).place(
                    relx=.5,
                    rely=.48,
                    anchor="c")
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
                temp.place(x=(i * 64 + 5), y=(35 * 32 - 16))
                temp_image = Animate("assets/PacManRight.gif", frame=1)
                temp_image.addParent(temp)
                self.lives_images.append([temp, temp_image])

        self.thread_id = self.after(self.ms_delay, self.update)

    def add_image_parents(self):
        for i, row in enumerate(self.game.maze.maze):
            for j, cell in enumerate(row):
                if cell is not None and hasattr(cell, "image"):
                    cell.image.addParent(
                        self.game_canvas, x=((j) * 32), y=(i * 32))

        Pacman_pos = self.game.pacman.canvas_position
        self.game.pacman.image.addParent(
            self.game_canvas, x=Pacman_pos[0], y=Pacman_pos[1])

        for ghost in self.game.ghosts:
            ghost_pos = ghost.canvas_position
            ghost.image.addParent(
                self.game_canvas,
                x=ghost_pos[0],
                y=ghost_pos[1])

        self.game_canvas.tag_raise(self.game.pacman.image.id)

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
        name = filedialog.asksaveasfilename(defaultextension=".json")

        json_data = self.game.serialise()

        with open(name, 'w') as file:
            json.dump(json_data, file)

    def tkraise(self, aboveThis=None):
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
        Frame.__init__(self, parent, bg="#000", )

        self.controller = controller

        # Create a semi-transparent frame to hold the content
        self.pause_frame = Frame(self, bg="#333", bd=2, relief="solid")
        self.pause_frame.pack(expand=True, fill="both")

        # GAME PAUSED TITLE
        self.title_label = Label(
            self.pause_frame,
            text="Game Paused",
            font=(
                'Liberation Mono',
                24,
                "bold"),
            fg="#FFD700",
            bg="#333")
        self.title_label.pack(pady=20)

        # Resume Button
        self.resume_button = Button(
            self.pause_frame,
            text="Resume",
            bg="#3A3",
            fg="#FFF",
            font=(
                'Liberation Mono',
                16,
                "bold"),
            activebackground="#5A5",
            activeforeground="#FFF",
            bd=2,
            relief="raised",
            command=lambda: self.controller.manual_unpause())
        self.resume_button.pack(pady=15, fill="x")

        # Save Button
        self.save_button = Button(
            self.pause_frame,
            text="Save",
            bg="#444",
            fg="#FFF",
            font=(
                'Liberation Mono',
                16),
            activebackground="#666",
            activeforeground="#FFF",
            bd=2,
            relief="raised",
            command=self.save_button_event)
        self.save_button.pack(pady=15, fill="x")

        # Settings Button
        self.settings_button = Button(
            self.pause_frame,
            text="Settings",
            bg="#555",
            fg="#FFF",
            font=(
                'Liberation Mono',
                16),
            activebackground="#777",
            activeforeground="#FFF",
            bd=2,
            relief="raised",
            command=self.settings_button_event)
        self.settings_button.pack(pady=15, fill="x")

        # Quit Button
        self.quit_button = Button(
            self.pause_frame,
            text="Quit",
            bg="#D9534F",
            fg="#FFF",
            font=(
                'Liberation Mono',
                16),
            activebackground="#E57373",
            activeforeground="#FFF",
            bd=2,
            relief="raised",
            command=self.quit_button_event)
        self.quit_button.pack(pady=15, fill="x")

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
        # Dark background for a modern look
        Frame.__init__(self, parent, bg="#222")

        self.controller = controller
        self.leaderboard = controller.leaderboard

        # Title Label
        title_label = Label(
            self,
            text="Leaderboard",
            font=(
                'Liberation Mono',
                24,
                "bold"),
            bg="#222",
            fg="#FFD700",
            pady=20)  # Golden color for emphasis
        title_label.pack()

        # Instruction Label
        instruction_label = Label(self, text="Top scores are listed below.", font=(
            'Liberation Mono', 12, "italic"), bg="#222", fg="#AAA", pady=10)
        instruction_label.pack()

        # Frame for Leaderboard Entries
        self.leaderboard_frame = Frame(self, bg="#222")
        self.leaderboard_frame.pack(pady=20, padx=20)

        self.max_entries = 10

        # Back Button
        back_button = Button(
            self,
            text="Back",
            bg="#444",
            fg="#FFF",
            font=(
                'Liberation Mono',
                14,
                "bold"),
            activebackground="#666",
            activeforeground="#FFF",
            bd=2,
            relief="raised",
            command=lambda: self.controller.goToPreviousScreen())
        back_button.pack(pady=20)

    def populate(self):
        """Populates the leaderboard with the current scores."""
        # Clear any existing widgets in the leaderboard frame
        for widget in self.leaderboard_frame.winfo_children():
            widget.destroy()

        # Add leaderboard entries
        if not self.leaderboard.scores:
            Label(
                self.leaderboard_frame,
                text="No scores available.",
                font=(
                    'Liberation Mono',
                    14),
                bg="#222",
                fg="#FFF").pack(
                pady=10)
        else:

            scores = self.leaderboard.scores[:self.max_entries]

            for idx, score in enumerate(scores):
                rank_label = Label(
                    self.leaderboard_frame,
                    text=f"{idx + 1}.",
                    font=(
                        'Liberation Mono',
                        14,
                        "bold"),
                    bg="#222",
                    fg="#FFD700",
                    width=3,
                    anchor="e")
                rank_label.grid(row=idx, column=0, padx=10, pady=5)

                name_label = Label(self.leaderboard_frame, text=f"{score[0]}", font=(
                    'Liberation Mono', 14), bg="#222", fg="#FFF", width=20, anchor="w")
                name_label.grid(row=idx, column=1, padx=10, pady=5)

                score_label = Label(
                    self.leaderboard_frame,
                    text=f"{score[1]}",
                    font=(
                        'Liberation Mono',
                        14,
                        "bold"),
                    bg="#222",
                    fg="#FFD700",
                    width=10,
                    anchor="e")
                score_label.grid(row=idx, column=2, padx=10, pady=5)

    def tkraise(self, aboveThis=None):
        """Refreshes the leaderboard when the screen is raised."""
        self.populate()
        return super().tkraise(aboveThis)

    def EventHandler(self, event: Event):
        if event.keysym_num == 65293:  # enter key
            self.controller.goToPreviousScreen()


class OptionScreen(Frame):
    def __init__(self, parent, controller):
        # Use a darker background for contrast
        Frame.__init__(self, parent, bg="#222")

        self.controller = controller
        self.settings = controller.settings
        self.listen = False  # Becomes True when waiting for a key press
        self.to_change = ""  # Stores the setting key to change
        self.clicked_button = None  # Stores the index of the clicked button

        # Title Label
        title_label = Label(
            self,
            text="Options",
            font=(
                'Liberation Mono',
                24,
                "bold"),
            bg="#222",
            fg="#FFF",
            pady=20)
        title_label.pack()

        # Instruction Label
        instruction_label = Label(
            self,
            text="Click a setting to change the key binding, then press a new key.",
            font=(
                'Liberation Mono',
                12,
                "italic"),
            bg="#222",
            fg="#AAA",
            pady=10)
        instruction_label.pack()

        # Buttons for each setting
        self.buttons = []
        # Group buttons in a frame for alignment
        button_frame = Frame(self, bg="#222")
        button_frame.pack(pady=20)

        for i, option in enumerate(self.settings.getKeyValues()):
            option_name = option[0]
            option_info = option[1]

            # Label for setting name
            Label(
                button_frame,
                text=option_name,
                font=(
                    'Liberation Mono',
                    14),
                bg="#222",
                fg="#FFF").grid(
                row=i,
                column=0,
                padx=20,
                pady=10,
                sticky="w")

            # Button to display current key binding
            button = Button(
                button_frame,
                text=f"{option_info[1]}: {option_info[0]}",
                bg="#444",
                fg="#FFF",
                font=(
                    'Liberation Mono',
                    12,
                    "bold"),
                activebackground="#666",
                activeforeground="#FFF",
                bd=2,
                relief="raised",
                command=lambda opt=option_name,
                idx=i: self.buttonPress(
                    opt,
                    idx))
            button.grid(row=i, column=1, padx=20, pady=10, sticky="e")
            self.buttons.append(button)

        # Back Button
        back_button = Button(
            self,
            text="Back",
            bg="#444",
            fg="#FFF",
            font=(
                'Liberation Mono',
                14,
                "bold"),
            activebackground="#666",
            activeforeground="#FFF",
            bd=2,
            relief="raised",
            command=lambda: self.controller.goToPreviousScreen())
        back_button.pack(pady=20)

    def buttonPress(
            self,
            setting_name: str,
            clicked_button_index: int) -> None:
        self.listen = True
        self.to_change = setting_name
        self.clicked_button = clicked_button_index

    def EventHandler(self, event: Event):
        if self.listen:
            self.listen = False
            key_num = event.keysym_num
            key_name = event.keysym

            # check if key is already set
            if self.settings.key_exists(key_num):
                # display message to the user
                messagebox.showinfo("INFO", "Key entered already in use")

            else:
                self.settings.setKey(self.to_change, key_num, key_name)
                self.buttons[self.clicked_button].configure(
                    text=f"{key_name}: {key_num}")


class BossScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#000")

        self.controller = controller

        Label(
            self,
            text="Very productive work going on here",
            font=(
                'Liberation Mono',
                30),
            bg="#000",
            fg="#FFF").place(
            relx=0.5,
            rely=0.5,
            anchor="center")

    def EventHandler(self, event: Event):
        pass


if __name__ == "__main__":
    main = Tk()
    main.geometry("896x1170")
    main.title = "Woka Woka"
    main.resizable(width=False, height=False)
    app = App(main)
    main.mainloop()
