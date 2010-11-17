import os
from Tkinter import *
import ConfigParser
import koch
import play
import score

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
        self.answerText = Text(self.answerFrame, wrap=WORD, height=5, takefocus=0, state=DISABLED,
                               yscrollcommand=self.answerScrollbar.set)
        self.answerText.pack()
        self.answerScrollbar.config(command=self.answerText.yview)
        r = r + 1
        self.analysisLabel = Label(frame, text="Analysis:")
        self.analysisLabel.grid(column=0, row=r)
        r = r + 1
        self.analysisFrame = Frame(frame, borderwidth=2, relief=SUNKEN)
        self.analysisFrame.grid(column=0, columnspan=2, row=r, padx=20)
        self.analysisScrollbar = Scrollbar(self.analysisFrame, orient=VERTICAL)
        self.analysisScrollbar.pack(side=RIGHT, fill=Y)
        self.analysisText = Text(self.analysisFrame, wrap=WORD, height=5, state=DISABLED,
                                 takefocus=0, yscrollcommand=self.analysisScrollbar.set)
        self.analysisText.pack()
        self.analysisScrollbar.config(command=self.analysisText.yview)
        r = r + 1
        self.resultVar = StringVar()
        self.resultLabel = Label(frame, textvariable=self.resultVar)
        self.resultLabel.grid(column=0, row=r, columnspan=2)
        r = r + 1
        self.button = Button(frame, text="Stop", command=self.stop)
        self.button.grid(column=0, row=r)
        self.button = Button(frame, text="Start", command=self.start)
        self.button.grid(column=1, row=r)

        self.speedVar.set(15)
        self.farnsworthVar.set(20)
        self.lettersVar.set(2)
        self.loadSettings()

    def start(self):
        self.saveSettings()
        self.entryText.delete("1.0", END)
        self.answerText.config(state=NORMAL)
        self.answerText.delete("1.0", END)
        self.answerText.config(state=DISABLED)
        self.analysisText.config(state=NORMAL)
        self.analysisText.delete("1.0", END)
        self.analysisText.config(state=DISABLED)
        self.resultVar.set("")
        self.letters = koch.getLetters(self.lettersVar.get())
        self.words = koch.generateKochWords(self.wordsVar.get(), self.letters)
        play.setSpeed(self.speedVar.get(), self.farnsworthVar.get())
        play.play(self.words, self.displayAnswer)

    def stop(self):
        play.stop()

    def displayAnswer(self):
        answerGiven = self.entryText.get("1.0", END)
        comparison = score.compare(self.words, answerGiven)
        self.answerText.config(state=NORMAL)
        self.answerText.insert("1.0", self.words)
        self.answerText.config(state=DISABLED)
        comparisonString = score.makeComparisonString(comparison)
        self.analysisText.config(state=NORMAL)
        self.analysisText.insert("1.0", comparisonString)
        self.analysisText.config(state=DISABLED)
        mistakes = score.countMistakes(comparisonString)
        characters = len(self.words)
        percentage = int((float(characters - mistakes)/float(characters))*100)
        self.resultVar.set("Characters: " + str(len(self.words)) + " Mistakes: "
                      + str(mistakes) + " Score: " + str(percentage) + "%")

    def saveSettings(self):
        config = ConfigParser.SafeConfigParser()
        config.add_section('morse')
        config.set('morse', 'speed', str(self.speedVar.get()))
        config.set('morse', 'farnsworth', str(self.farnsworthVar.get()))
        config.add_section('koch')
        config.set('koch', 'letters', str(self.lettersVar.get()))
        config.set('koch', 'words', str(self.wordsVar.get()))
        with open('mkgui.cfg', 'wb') as configFile:
            config.write(configFile)

    def loadSettings(self):
        config = ConfigParser.SafeConfigParser()
        config.read('mkgui.cfg')
        if config.has_option('morse', 'speed'):
            self.speedVar.set(config.getint('morse', 'speed'))
        if config.has_option('morse', 'farnsworth'):
            self.farnsworthVar.set(config.getint('morse', 'farnsworth'))
        if config.has_option('koch', 'letters'):
            self.lettersVar.set(config.getint('koch', 'letters'))
        if config.has_option('koch', 'words'):
            self.wordsVar.set(config.getint('koch', 'words'))
        
root = Tk()
app = MkGui(root)
root.mainloop()
