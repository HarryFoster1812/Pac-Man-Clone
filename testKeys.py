from tkinter import *
root = Tk()
keyLabel = Label(root, text="Key Pressed:")
keyLabel.pack()
print(dir(Button()))

def keyPress(event):
    keyLabel.configure(text=f"Key Pressed: {event.keycode}")
    atts = dir(event)
    for attr in atts:
        print(f"{attr}:  {getattr(event, attr)}")

root.bind("<Key>", keyPress)
root.mainloop()
