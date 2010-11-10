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
        self.wordsVar = IntVar()
        self.wordsLabel = Label(frame, text="# Words")
        self.wordsLabel.grid(column=0, row=r)
        self.wordsBox = Spinbox(frame, from_=1, to=1000, increment=1, textvariable=self.wordsVar)
        self.wordsBox.grid(column=1, row=r)
        r = r + 1
        self.entryLabel = Label(frame, text="Enter text here:")
        self.entryLabel.grid(column=0, row=r)
        r = r + 1
        self.entryFrame = Frame(frame, borderwidth=2, relief=SUNKEN)
        self.entryFrame.grid(column=0, columnspan=2, row=r, padx=20)
        self.entryScrollbar = Scrollbar(self.entryFrame, orient=VERTICAL)
        self.entryScrollbar.pack(side=RIGHT, fill=Y)
        self.entryText = Text(self.entryFrame, wrap=WORD, height=5, yscrollcommand=self.entryScrollbar.set)
        self.entryText.pack()
        self.entryScrollbar.config(command=self.entryText.yview)
        r = r + 1
        self.answerLabel = Label(frame, text="Answer:")
        self.answerLabel.grid(column=0, row=r)
        r = r + 1
        self.answerFrame = Frame(frame, borderwidth=2, relief=SUNKEN)
        self.answerFrame.grid(column=0, columnspan=2, row=r, padx=20)
        self.answerScrollbar = Scrollbar(self.answerFrame, orient=VERTICAL)
        self.answerScrollbar.pack(side=RIGHT, fill=Y)
        self.answerText = Text(self.answerFrame, wrap=WORD, height=5, yscrollcommand=self.answerScrollbar.set)
        self.answerText.pack()
        self.answerScrollbar.config(command=self.answerText.yview)
        r = r + 1
        self.button = Button(frame, text="Start", command=self.start)
        self.button.grid(column=1, row=r)

        self.speedVar.set(15)
        self.farnsworthVar.set(20)
        self.lettersVar.set(2)

    def start(self):
        self.letters = koch.getLetters(self.lettersVar.get())
        self.words = koch.generateKochWords(self.wordsVar.get(), self.letters)
        play.setSpeed(self.speedVar.get(), self.farnsworthVar.get())
        play.play(self.words, self.displayAnswer)

    def displayAnswer(self):
        self.answerText.delete("1.0", END)
        self.answerText.insert("1.0", self.words)

root = Tk()
app = MkGui(root)
root.mainloop()
