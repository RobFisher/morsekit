import os
from Tkinter import *
import koch
import play

class MkGui:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        r=0
        self.speedVar = IntVar()
        self.speedLabel = Label(frame, text="Speed");
        self.speedLabel.grid(column=0, row=r)
        self.speedBox = Spinbox(frame, from_=5, to=40, increment=1, textvariable=self.speedVar)
        self.speedBox.grid(column=1, row=r)
        r = r + 1
        self.farnsworthVar = IntVar()
        self.farnsworthLabel = Label(frame, text="Farnsworth")
        self.farnsworthLabel.grid(column=0, row=r)
        self.farnsworthBox = Spinbox(frame, from_=5, to=40, increment=1, textvariable=self.farnsworthVar)
        self.farnsworthBox.grid(column=1, row=r)
        r = r +1
        self.lettersVar = IntVar()
        self.lettersLabel = Label(frame, text="Letters")
        self.lettersLabel.grid(column=0, row=r)
        self.lettersBox = Spinbox(frame, from_=2, to=koch.maxLetters(), increment=1, textvariable=self.lettersVar)
        self.lettersBox.grid(column=1, row=r)
        r = r + 1
        self.button = Button(frame, text="Start", command=self.start)
        self.button.grid(column=1, row=r)

        self.speedVar.set(15)
        self.farnsworthVar.set(20)
        self.lettersVar.set(2)       

    def start(self):
        self.letters = koch.getLetters(self.lettersVar.get())
        self.words = koch.generateKochWords(1, self.letters)
        play.setSpeed(self.speedVar.get(), self.farnsworthVar.get())
        play.play(self.words)

root = Tk()
app = MkGui(root)
root.mainloop()
