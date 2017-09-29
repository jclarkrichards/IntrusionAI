from Tkinter import *
from window import WindowABC, VerticalScrollFrame

class MainWindow(object):
    def __init__(self, root):
        self.root = root
        self.root.minsize(width=400, height=200)
        self.root.maxsize(width=600, height=500)
        self.win = WindowABC()
        self.mainFrame = VerticalScrollFrame(root) #self.win.newScrollFrame(root)
        #self.mainFrame = self.win.newFrame(root)
        for i in range(10):
            self.win.newButton(self.mainFrame.interior, text="Testing "+str(i), row=i)
        self.mainFrame.pack()


        
if __name__ == "__main__":
    root = Tk()
    win = MainWindow(root)
    root.mainloop()
