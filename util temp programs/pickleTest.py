from src.game import Game
from src.settings import Settings
from src.player import Player
import pickle
from tkinter import *

root =  Tk()

settings = Settings()
player = Player()
test = Game(settings, player)


with open("file.pickle", "wb") as my_file:
    pickle.dump(test, my_file)