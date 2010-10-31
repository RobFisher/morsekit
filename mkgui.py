from Tkinter import *

class MkGui:
    def init(__self__, __master):
        frame = Frame(master)
        frame.pack()
        self.button = Button(frame, text="Start", command=self.start)
        self.button.pack(side=RIGHT)

    def start(self):
        os.system("./koch.py")

root = Tk()
app = MkGui(root)
root.mainloop()
