from Tkinter import *
from tkMessageBox import *
import os
#import subprocess
from subprocess import PIPE, Popen
#import numpy as np
from window import WindowABC, VerticalScrollFrame
from records import MachineRecord


class LocalSettings(object):
    def __init__(self, root, main):
        self.name = "local"
        self.root = root
        self.main = main
        #self.info = info
        self.root.minsize(width=root.winfo_width(), height=500)#height=root.winfo_height())
        self.win = WindowABC()
        self.setGlobalSettings()
        self.machines = []
        self.numMachines = 0
        self.addButton = None
        self.clearButton = None
        self.createWindow()
        #self.layout = self

    def destroy(self):
        #print "Destroy"
        self.mainFrame.pack_forget()
        self.mainFrame.grid_forget()
        self.scrollFrame.pack_forget()
        self.scrollFrame.grid_forget()
        self.mainFrame.destroy()
        self.scrollFrame.destroy()
        
    def createWindow(self):
        '''Create initial window with one machine'''
        #self.mainFrame = self.win.newFrame(self.root, 20, 20)
        self.scrollFrame = VerticalScrollFrame(self.root)
        self.mainFrame = self.scrollFrame.interior
        self.win.newLabel(self.mainFrame, "Local")
        if len(self.names) > 0:
            for i in range(len(self.names)):
                self.addNewMachine(self.UIDS[i], self.names[i],
                                   self.ips[i], self.paths[i])
        else:
            self.addNewMachine()
        self.scrollFrame.pack()
        #self.mainFrame.pack()

    def refreshWindow(self):
        self.destroy()
        self.setGlobalSettings()
        self.machines = []
        self.numMachines = 0
        self.createWindow()

    def addNewMachine(self, uid="", name="", ip="", paths=[]):
        '''Add a new machine below last machine added.'''
        if self.addButton is not None:
            self.addButton.destroy()
        if self.clearButton is not None:
            self.clearButton.destroy()
        
        num = self.numMachines
        frameSub = self.win.newFrame(self.mainFrame, row=num, padx=5, pady=5)
        self.machines.append(MachineRecord(frameSub, self.keywords, uid, name,
                                           ip, paths, self.savepath, self.email))
        self.numMachines += 1

        self.addButton = self.win.newButton(self.mainFrame, text="Add Machine...", row=num+2)
        self.clearButton = self.win.newButton(self.mainFrame, text="Clear All Machines", row=num+3)
        self.clearButton.config(command=self.clearMachines)
        self.addButton.config(command=self.addNewMachine)

        self.machines = [m for m in self.machines if not m.destroyed]

    def clearMachines(self):
        #self.info["UIDS"] = []
        #self.info["names"] = []
        #self.info["ips"] = []
        #self.info["paths"] = []
        self.refreshWindow()

    def setGlobalSettings(self):
        '''Fill in boxes if there is info in the info dictionary'''
        self.UIDS = []
        self.names = []
        self.ips = []
        self.paths = []
        #self.savepath = self.info["path"]
        #self.daterange = self.info["date"]
        #self.keywords = self.info["keywords"]
        #self.email = self.info["email"]

        #if len(self.info["names"]) > 0:
        #    self.UIDS = self.info["UIDS"]
        #    self.names = self.info["names"]
        #    self.ips = self.info["ips"]
        #    self.paths = self.info["paths"]

    def getSettings(self):
        #print self.info
        #return self.info
        pass
        



