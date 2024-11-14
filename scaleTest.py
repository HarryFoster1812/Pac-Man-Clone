import tkinter as tk
from src.animate import Animate

root = tk.Tk()

# Make a frame and having it fill the whole root window using pack
mainframe = tk.Frame(root)
mainframe.pack(fill=tk.BOTH, expand=1)

# Add four labels using the grid manager
# Each is stickied to all four sides so it will fill the entire grid cell
label_1 = tk.Label(mainframe, image="", bg='blue')
label_1.grid(row=0, column=0, sticky='nsew')
imageOne = Animate("assets/title/title.gif", label_1, scale=0.9)

# Add weights to the grid rows and columns
# Changing the weights will change the size of the rows/columns relative to each other
mainframe.grid_rowconfigure(0, weight=1)
mainframe.grid_rowconfigure(1, weight=1)
mainframe.grid_columnconfigure(0, weight=1)
mainframe.grid_columnconfigure(1, weight=1)

root.geometry("708x911")

root.mainloop()