from Tkinter import *
import os
from subprocess import PIPE, Popen
from tkFileDialog import askdirectory #askopenfilename, asksaveasfilename
from window import WindowABC
from constants import *
import json

class GlobalSettings(object):
    def __init__(self, root, main):
        self.name = "global"
        self.root = root
        self.main = main
        self.data = self.openDatafile()
        #self.info = info
        #print self.info["email"]
        #self.root.minsize(width=root.winfo_width(), height=271) #root.winfo_height())
        self.win = WindowABC()
        self.createWindow()
        self.setSettings()
        self.layout = self
        
    def destroy(self):
        #print "Destroy the global settings"
        self.mainFrame.destroy()

    def createWindow(self):
        '''Create initial window with one machine'''
        self.mainFrame = self.win.newFrame(self.root, 20, 20)
        self.win.newLabel(self.mainFrame, "Global", colspan=2)
        self.win.newLabel(self.mainFrame, "Frequency", row=2)
        self.win.newLabel(self.mainFrame, "Filter Date", row=3)
        self.win.newLabel(self.mainFrame, "Keywords", row=4)
        self.win.newLabel(self.mainFrame, "Email Report", row=5)
        self.win.newLabel(self.mainFrame, "Email", row=6)

        self.pathButton = self.win.newButton(self.mainFrame, text="Report Path", row=1)
        self.pathBox = self.win.newEntry(self.mainFrame, row=1, col=1, sticky=W+E)

        self.frequencyBox = StringVar(self.mainFrame)
        options2 = ["2 Min", "hourly", "Every 6 hours", "Every 12 hours",
                    "daily", "weekly", "monthly", "None"]
        drop2 = self.win.newDropMenu(self.mainFrame, self.frequencyBox, options2, row=2, col=1)

        self.dateBox = StringVar(self.mainFrame)
        options = ["5 min", "1 hour", "12 hours", "1 day", "1 week", "1 month", "All"]
        drop = self.win.newDropMenu(self.mainFrame, self.dateBox, options, row=3, col=1)

        self.keywordBox = self.win.newEntry(self.mainFrame, row=4, col=1)
        #Holds 0 for unchecked, and 1 for checked
        self.emailCheck = IntVar()
        self.check = self.win.newCheck(self.mainFrame, self.emailCheck, row=5, col=1, sticky=W)

        self.emailBox = self.win.newEntry(self.mainFrame, width=25, row=6, col=1, enabled=False)
        #data = self.openDatafile()
        self.email = self.data["email"]
        #self.emailBox.insert(0, data["email"])
        emailButton = self.win.newButton(self.mainFrame, "Save Email", row=7)
        emailButton.config(command=self.saveEmail)
        self.pathButton.config(command=self.openSaveDirectory)
        self.check.config(command=self.toggleEmailCheck)
        self.mainFrame.pack()

    def openDatafile(self):
        try:
            open(JSONFILE)
        except IOError:
            print "An error occurred"
            return {}
        else:
            with open(JSONFILE) as datafile:
                data = json.load(datafile)
        try:
            print data["sendemail"]
        except KeyError:
            data["sendemail"] = False
        return data

    def saveDatafile(self, data):
        with open(JSONFILE, "w") as datafile:
            json.dump(data, datafile)
        
        
    def openSaveDirectory(self):
        folder = askdirectory(parent=self.root, title="Save Folder")
        self.pathBox.insert(0, folder)

    def toggleEmailCheck(self):
        if self.emailCheck.get():
            self.data["sendemail"] = True
            self.saveDatafile(self.data)
            self.emailBox.configure(state='normal')
            self.emailBox.insert(0, self.email)
        else:
            self.data["sendemail"] = False
            self.saveDatafile(self.data)
            self.emailBox.delete(0, END)
            self.emailBox.configure(state='disabled')

    def saveEmail(self):
        '''Open JSON file and save this email address there'''
        print "Saving email"
        #try:
        #    open(JSONFILE)
        #except IOError:
        #    print "An error occurred"
        #else:
        #    with open(JSONFILE) as datafile:
        #        data = json.load(datafile)
        #print self.emailBox.get()
        self.data["email"] = self.emailBox.get()
        self.saveDatafile(self.data)
            #try:
            #    print data["email"]
            #except KeyError:
            #    data["email"
            #else:
            #    data["email"] = self.emailBox.get()
            #with open(JSONFILE, "w") as datafile:
            #    json.dump(data, datafile)

    def getSettings(self):
        '''Return the values of all of the options here'''
        #self.info["path"] = self.pathBox.get()
        #self.info["frequency"] = self.frequencyBox.get()
        #self.info["date"] = self.dateBox.get()
        #self.info["keywords"] = self.keywordBox.get()
        #self.info["email_check"] = self.emailCheck.get()
        #self.info["email"] = self.emailBox.get()
        #return self.info
        pass

    def setSettings(self):
        '''Set the settings based on the info dictionary'''
        #self.pathBox.insert(0, self.info["path"])
        #if self.info["date"] != "":
        #    self.dateBox.set(self.info["date"])
        #if self.info["frequency"] != "":
        #    self.frequencyBox.set(self.info["frequency"])
        #print self.info["email"]
        #self.emailBox.insert(0, self.info["email"])
        pass
        



