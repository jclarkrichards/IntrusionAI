from Tkinter import *
from tkMessageBox import *
from local import LocalSettings
from settings import GlobalSettings
from machines import MachinePicker
from grapher import Grapher
from dashboard import Dashboard
from constants import *

class MainWindow(object):
    def __init__(self, root):
        self.root = root
        self.root.wm_title("Image Classifier")
        #self.root.attributes('-zoomed', True)
        w = 500
        h = 600
        self.root.minsize(width=w, height=h)
        #self.root.maxsize(width=600, height=900)
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        #print "MAIN WINDOW INFO"
        #print ws, hs, x, y
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Exit", command=self.exitApp)
        self.menu.add_command(label="Dashboard", command=self.dashboardWindow)
        self.menu.add_command(label="Settings", command=self.globalWindow)
        #self.menu.add_command(label="Configure", command=self.localWindow)
        #self.menu.add_command(label="Machines", command=self.machinesWindow)
        #self.menu.add_command(label="Graph", command=self.graphWindow)
        self.layout = None
        self.dashboardWindow()

    def toggle_fullscreen(self, event=None):
        print "Toggle Fullscreen"
        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        print "End Fullscreen"
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"
    
    def dashboardWindow(self):
        if self.layout is not None:
            self.layout.destroy()
        self.layout = Dashboard(self.root, self)

    def localWindow(self):
        '''Define machines and run to get reports'''
        if self.layout is not None:
            self.layout.destroy()
        self.layout = LocalSettings(self.root, self)

    def globalWindow(self):
        '''Set the settings to use on all machines'''
        if self.layout is not None:
            self.layout.destroy()
        self.layout = GlobalSettings(self.root, self)

    def machinesWindow(self):
        '''This displays a list of the names of the machines used before.'''
        if self.layout is not None:
            self.layout.destroy()
        self.layout = MachinePicker(self.root, self)

    def graphWindow(self):
        if self.layout is not None:
            self.layout.destroy()
        self.layout = Grapher(self.root, self)

    def reloadWindow(self):
        if self.layout is not None:
            pass

    def exitApp(self):
        self.layout.destroy()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    win = MainWindow(root)
    root.mainloop()

    
