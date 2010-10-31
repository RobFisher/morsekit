import os
from Tkinter import *
import koch

class MkGui:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.button = Button(frame, text="Start", command=self.start)
        self.button.pack(side=RIGHT)

    def start(self):
        koch.startKoch(20)

root = Tk()
app = MkGui(root)
root.mainloop()
