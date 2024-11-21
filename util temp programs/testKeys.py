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

def buttonClicked(buttonParam):
    atts = dir(buttonParam)
    for attr in atts:
        print(f"{attr}:  {getattr(buttonParam, attr)}")

    buttonParam.configure(text="Clicked")

root.bind("<Key>", keyPress)
my_button = Button(root, text = "hello")
my_button.configure(command=lambda: buttonClicked(my_button))
my_button.pack()
root.mainloop()
