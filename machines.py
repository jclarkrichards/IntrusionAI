from Tkinter import *
from tkMessageBox import *
import os
from subprocess import PIPE, Popen
#from tkFileDialog import askdirectory #askopenfilename, asksaveasfilename
from window import WindowABC

class MachinePicker(object):
    def __init__(self, root, main):
        self.name = "machines"
        self.root = root
        self.main = main
        #self.info = info
        self.root.minsize(width=root.winfo_width(), height=271)
        self.baseDir = os.getcwd()
        self.win = WindowABC()
        self.createWindow()
        #self.layout = self

    def destroy(self):
        print "Destroy machine picker"
        self.mainFrame.destroy()

    def createWindow(self):
        '''Create initial window with one machine'''
        self.mainFrame = self.win.newFrame(self.root, 20, 20)
        self.listbox = self.win.newListbox(self.mainFrame, mode=MULTIPLE,
                                           yscroll=True, colspan=2, height=10)
        self.removeButton = self.win.newButton(self.mainFrame, text="Remove Entry", row=1)
        self.openButton = self.win.newButton(self.mainFrame, text="Open Machine", row=1, col=1)
        self.fillListBox()
        self.removeButton.config(command=self.removeMachine)
        self.openButton.config(command=self.openMachines)
        self.mainFrame.pack()

    def fillListBox(self):
        #print os.getcwd()
        f = self.openFile()
        if f is not None:
            f.close()
            with open("machines.txt") as f:
                for line in f:
                    name = line.split(",")[0]
                    self.listbox.insert(END, name)
            f.close()
        
    def removeMachine(self):
        selections = [self.listbox.get(i) for i in self.listbox.curselection()]
        if len(selections) > 0:
            lines = []
            names = []
            with open("machines.txt") as f:
                for line in f:
                    lines.append(line)
                    names.append(line.split(",")[0])

            for selection in selections:
                if selection in names:
                    i = names.index(selection)
                    line = lines[i]
                    lines.remove(line)
                    names.remove(selection)

            f.close()
            f = open("machines.txt", "w")
            s = ""
            for line in lines:
                s = s + line

            f.write(s)
            f.close()
            self.listbox.delete(0, END)
            self.fillListBox()

    def openMachines(self):
        #self.info["UIDS"] = []
        #self.info["names"] = []
        #self.info["ips"] = []
        #self.info["paths"] = []
        f = self.openFile()
        if f is not None:
            f.close()
            selections = [self.listbox.get(i) for i in self.listbox.curselection()]
            #print selections
            lines = []
            
            with open("machines.txt") as f:
                for line in f:
                    lines.append(line)
            f.close()
            for line in lines:
                line = line.split("\n")[0]
                parsed = line.split(",")
                uid = parsed[0].strip()
                name = parsed[1].strip()
                if uid in selections:
                    ip = parsed[2].strip()
                    paths = []
                    if len(parsed) > 3:
                        paths = [parsed[3].strip()]
                    if len(parsed) > 4:
                        for i in range(4, len(parsed)):
                            paths.append(parsed[i].strip())
                    #self.info["UIDS"].append(uid)
                    #self.info["names"].append(name)
                    #self.info["ips"].append(ip)
                    #self.info["paths"].append(paths)
        #print self.info
        showinfo("Loaded", "Go back to the Configure tab")

    def openFile(self):
        try:
            f = open("machines.txt")
        except IOError:
            pass
        else:
            return f
        return None

    def getSettings(self):
        '''Return the values of all of the options here'''
        #return self.info
        pass

        



