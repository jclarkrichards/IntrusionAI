from Tkinter import *
from tkMessageBox import *
import os
from PIL import Image, ImageTk
from window import WindowABC, VerticalScrollFrame
from constants import *
import json
from copy import deepcopy
import platform

class Machine(object):
    def __init__(self, root, main, dataID=None):
        self.name = "template"
        self.root = root
        self.main = main
        self.UID = dataID
        #self.root.minsize(width=root.winfo_width(), height=500)
        self.pathBoxes = []
        self.pathrow = 2 #row to add next path box if added
        self.removePathButtons = []
        self.win = WindowABC()
        self.createWindow()
        self.addBelowPath()
        self.loadData()
        self.destroyed = False

    def destroy(self):
        self.mainFrame.pack_forget()
        self.mainFrame.grid_forget()
        self.scrollFrame.pack_forget()
        self.scrollFrame.grid_forget()
        self.mainFrame.destroy()
        self.scrollFrame.destroy()

    def createWindow(self):
        #self.mainFrame = self.win.newFrame(self.root, 20, 20, bg="#e3f7eb")
        self.scrollFrame = VerticalScrollFrame(self.root)
        self.mainFrame = self.scrollFrame.interior

        #======================================================================
        infoFrame = self.win.newFrame(self.mainFrame, 10, 10, colspan=3, bg="white")
        self.win.newLabel(infoFrame, "Machine Entry Form", font=("Helvetica", 30))
        self.win.newLabel(infoFrame, "Enter the information for the machine you want to generate a log report on and press the Save button at the bottom when finished in order to save this configuration onto the Dashboard.", width=20, wraplength=380, justify=LEFT, bg=LG, row=1)

        #======================================================================
        machineFrame = self.win.newFrame(self.mainFrame, 10, 10, row=1, colspan=3, bg=LG)
        self.win.newLabel(machineFrame, "Machine Name", bg=LG, justify=LEFT, sticky=W)
        self.nameBox = self.win.newEntry(machineFrame, col=1)

        self.win.newLabel(machineFrame, "Local Machine", row=1, bg=LG, justify=LEFT, sticky=W)
        self.yesno = IntVar()
        radios = self.win.newRadioButton(machineFrame, self.yesno, [("Yes", 1), ("No", 0)], 
                                         row=1, col=1, sticky=N+S+W, bg=LG)

        for radio in radios:
            radio.config(command=self.radioYesNo)
            
        machineFrame.grid_columnconfigure(0, weight=1)
        machineFrame.grid_columnconfigure(1, weight=3)

        #======================================================================            
        remoteFrame = self.win.newFrame(self.mainFrame, 10, 10, row=2, colspan=3, bg=LG)
        self.machineType = IntVar()
        self.win.newLabel(remoteFrame, "Remote Machine Type", bg=LG, justify=LEFT, sticky=W)
        self.radios = self.win.newRadioButton(remoteFrame, self.machineType, [("Linux", 1), ("Windows", 0)], 
                                              col=1, sticky=N+S+W, bg=LG)
        self.machineType.set(1)
        for radio in self.radios:
            radio.config(command=self.toggleRemoteMachine)

        self.win.newLabel(remoteFrame, "Server Name", row=2, bg=LG, justify=LEFT, sticky=W)
        self.serverBox = self.win.newEntry(remoteFrame, row=2, col=1, required=True)

        self.win.newLabel(remoteFrame, "IP Address", row=3, bg=LG, justify=LEFT, sticky=W)
        self.ipBox = self.win.newEntry(remoteFrame, row=3, col=1, required=True)

        self.win.newLabel(remoteFrame, "Port", row=4, bg=LG, justify=LEFT, sticky=W)
        self.portBox = self.win.newEntry(remoteFrame, row=4, col=1)

        #self.win.newLabel(self.mainFrame, "Password", row=9)
        #self.passwordBox = self.win.newEntry(self.mainFrame, show="*", row=9, col=1)
        self.pathBoxes = []
        self.keywordBoxes = []
        #self.winSystemKeywordsBox = []
        #self.winAppKeywordsBox = []
        #self.winSecurityKeywordsBox = []
        #self.windowsPathBoxes = []
        remoteFrame.grid_columnconfigure(0, weight=1)
        remoteFrame.grid_columnconfigure(1, weight=3)
        
        #======================================================================
        #if platform.system() == "Windows":
        #    self.addWindowsOptions()

            
            
        #======================================================================    
        self.pathsFrame = self.win.newFrame(self.mainFrame, 10, 10, row=4, colspan=3, bg=LG)
        self.win.newLabel(self.pathsFrame, "Path to Logs", bg=LG)
        self.win.newLabel(self.pathsFrame, "Keywords", col=1, bg=LG)

        #self.pathBoxes = []
        #self.keywordBoxes = []
        self.pathBoxes.append(self.win.newEntry(self.pathsFrame, row=self.pathrow))
        self.keywordBoxes.append(self.win.newEntry(self.pathsFrame, row=self.pathrow, col=1))
        self.pathrow += 1
        self.pathsFrame.grid_columnconfigure(0, weight=1)
        self.pathsFrame.grid_columnconfigure(1, weight=3)
        
    def addBelowPath(self):
        '''Add the rest of the entries below path boxes'''
        self.addPathButton = self.win.newButton(self.mainFrame, text="Add File Path", row=5, colspan=2, sticky=W)

        #======================================================================
        buttonsFrame = self.win.newFrame(self.mainFrame, 10, 10, row=6)
        self.saveButton = self.win.newButton(buttonsFrame, text="Save As New", sticky=E)
        self.updateButton = self.win.newButton(buttonsFrame, text="Update", col=1)
        self.cancelButton = self.win.newButton(buttonsFrame, text="Cancel", col=2)
        self.saveButton.config(command=self.saveInfo)
        self.updateButton.config(command=self.updateInfo)
        if self.UID is None:
            self.updateButton.configure(state="disabled")
        self.cancelButton.config(command=self.cancel)
        self.radioYesNo()
        self.addPathButton.config(command=self.addPath)

        #======================================================================

        
    def addPath(self):
        '''Add a path entry box below last one added'''
        self.addPathButton.destroy()
        self.saveButton.destroy()
        self.updateButton.destroy()
        self.cancelButton.destroy()
        self.pathBoxes.append(self.win.newEntry(self.pathsFrame, row=self.pathrow))
        self.keywordBoxes.append(self.win.newEntry(self.pathsFrame, row=self.pathrow, col=1))
        image = Image.open(CANCELSMALL)
        photo = ImageTk.PhotoImage(image)
        self.removePathButtons.append(self.win.newButton(self.pathsFrame, row=self.pathrow, col=2, sticky=W, image=photo))
        self.removePathButtons[-1].config(command=lambda m=len(self.removePathButtons): self.removePath(m))
        self.pathrow += 1
        self.addBelowPath()

    def removePath(self, m):
        '''Remove a path entry box'''
        #print "There are " + str(len(self.pathBoxes))
        #print "Removing items at index " + str(m)
        self.pathBoxes[m].destroy()
        self.keywordBoxes[m].destroy()
        #print "There are " + str(len(self.pathBoxes))
        junk = self.pathBoxes.pop(m)
        junk = self.keywordBoxes.pop(m)
        self.removePathButtons[m-1].destroy()
        junk = self.removePathButtons.pop(m-1)
        for i in range(len(self.removePathButtons)):
            self.removePathButtons[i].config(command=lambda m=len(self.removePathButtons): self.removePath(m))
            
    def addWindowsOptions(self):
        '''Add more Windows options if Windows is selected'''
        self.windowsPathsFrame = self.win.newFrame(self.mainFrame, 10, 10, row=3, colspan=3, bg=LG)
        self.win.newLabel(self.windowsPathsFrame, "Log Type", bg=LG)
        self.win.newLabel(self.windowsPathsFrame, "Keywords", col=1, bg=LG)
        self.systemCheck = IntVar(value=1)
        self.appCheck = IntVar(value=1)
        self.securityCheck = IntVar(value=1)
        check1 = self.win.newCheck(self.windowsPathsFrame, self.systemCheck, "System", row=1, bg=LG, sticky=W) 
        check2 = self.win.newCheck(self.windowsPathsFrame, self.appCheck, "Applications", row=2, bg=LG, sticky=W) 
        check3 = self.win.newCheck(self.windowsPathsFrame, self.securityCheck, "Security", row=3, bg=LG, sticky=W)
        self.winSystemKeywordsBox = self.win.newEntry(self.windowsPathsFrame, row=1, col=1)
        self.winAppKeywordsBox = self.win.newEntry(self.windowsPathsFrame, row=2, col=1)
        self.winSecurityKeywordsBox = self.win.newEntry(self.windowsPathsFrame, row=3, col=1)
        check1.config(command=self.toggleSystemCheck)
        check2.config(command=self.toggleAppCheck)
        check3.config(command=self.toggleSecurityCheck)
        self.windowsPathsFrame.grid_columnconfigure(0, weight=1)
        self.windowsPathsFrame.grid_columnconfigure(1, weight=3)
        
    def removeWindowsOptions(self):
        try:
            self.windowsPathsFrame.destroy()
        except:
            pass

    def toggleRemoteMachine(self):
        if self.machineType.get() == 0: #Windows as remote
            self.addWindowsOptions()
            #print "Windows is remote"
        else:
            self.removeWindowsOptions()
            #print "Linux is remote"

    def radioYesNo(self):
        '''When the Yes/No radio buttons are pressed'''
        if self.yesno.get() == 0:
            self.serverBox.configure(state="normal")
            self.ipBox.configure(state="normal")
            self.portBox.configure(state="normal")
            #self.passwordBox.configure(state="normal")
            self.radios[0].configure(state="normal")
            self.radios[1].configure(state="normal")
        else:
            self.serverBox.configure(state="disabled")
            self.ipBox.configure(state="disabled")
            self.portBox.configure(state="disabled")
            #self.passwordBox.configure(state="disabled")
            self.radios[0].configure(state="disabled")
            self.radios[1].configure(state="disabled")

    def cancel(self):
        '''No saving the info, just go back to the dashboard window'''
        if askyesno("Cancel", "Are you sure you want to cancel?"):
            self.main.dashboardWindow()

    def updateInfo(self):
        '''We do not create a new entry in the JSON file.  We just use self.UID to delete that entry and save this new entry'''
        if self.yesno.get() == 0 and (self.serverBox.get() == "" or self.ipBox.get() == ""):
            showerror("Error", "Need to fill in the Server and IP boxes")
        else:
            if askyesno("Updating Info", "Are you sure you want to update?  Previous info will be lost"):
                with open(JSONFILE) as datafile:
                    data = json.load(datafile)
        
                for i in range(len(data["machine"])):
                    if data["machine"][i]["UID"] == self.UID:
                        junk = data["machine"].pop(i)
                        break
        
                template = self.fillTemplate(self.UID)

                data["machine"].append(template)
                with open(JSONFILE, "w") as datafile:
                    json.dump(data, datafile)

                showinfo("Saved!", "Data has been updated")
                self.main.dashboardWindow()


    def saveInfo(self):
        '''Open up the JSON file, read it, append a TEMPLATE to it, and fill the template with the data entered, then save the data back to the JSON file.  After saving, display a success message and then go back to the Dashboard automatically.'''
        if self.yesno.get() == 0 and (self.serverBox.get() == "" or self.ipBox.get() == ""):
            showerror("Error", "Need to fill in the Server and IP boxes")
        else:
            try:
                open(JSONFILE)
            except IOError:
                data = BASE
                nextID = 0
            else:
                with open(JSONFILE) as datafile:
                    data = json.load(datafile)
                ids = []
                for i in range(len(data["machine"])):
                    ids.append(data["machine"][i]["UID"])
                nextID = max(ids) + 1
        
            template = self.fillTemplate(nextID)

            data["machine"].append(template)
            with open(JSONFILE, "w") as datafile:
                json.dump(data, datafile)

            showinfo("Saved!", "Data has been saved")
            self.main.dashboardWindow()
        
    def fillTemplate(self, UID):
        '''This creates a new instance of the template and fills it with the data entered.
        Gets called when saving or updating the templates information'''
        print "FILL TEMPLATE"
        template = deepcopy(TEMPLATE)
        template["UID"] = UID
        template["name"] = self.nameBox.get()
        if self.yesno.get():
            template["local"] = True
        else: #All this info only matters when False
            template["local"] = False

            if self.machineType.get():
                template["remote"] = "Linux"
            else:
                template["remote"] = "Windows"
            template["server"] = self.serverBox.get()
            template["ip"] = self.ipBox.get()
            template["port"] = self.portBox.get()
            #template["password"] = self.passwordBox.get()

        for i in range(len(self.pathBoxes)):
            template["logpaths"].append([self.pathBoxes[i].get()])
            template["keywords"].append([self.keywordBoxes[i].get()])

        if platform.system() == "Windows":
            #if "winSystemKeywords" in template.keys():
            template["winSystemKeywords"] = self.winSystemKeywordsBox.get()
            #if "winAppKeywords" in template.keys():
            template["winAppKeywords"] = self.winAppKeywordsBox.get()
            #if "winSecurityKeywords" in template.keys():
            template["winSecurityKeywords"] = self.winSecurityKeywordsBox.get()
            if self.systemCheck.get():
                template["systemcheck"] = True
            else:
                template["systemcheck"] = False
                
            if self.appCheck.get():
                template["appcheck"] = True
            else:
                template["appcheck"] = False
                
            if self.securityCheck.get():
                template["securitycheck"] = True
            else:
                template["securitycheck"] = False
                
        return template

    def loadData(self):
        '''If data is not empty, then load the data into the necessary boxes'''
        if self.UID is not None:
            entry = {}
            with open(JSONFILE) as datafile:
                data = json.load(datafile)
            for i in range(len(data["machine"])):
                if data["machine"][i]["UID"] == self.UID:
                    entry = data["machine"][i]
                else:
                    pass
                    #print "Entry not found?"
            if len(entry) > 0:
                self.nameBox.insert(0, entry["name"])
                self.serverBox.insert(0, entry["server"])
                self.ipBox.insert(0, entry["ip"])
                self.portBox.insert(0, entry["port"])
                if entry["local"]:
                    self.yesno.set(1)
                else:
                    self.yesno.set(0)

                if entry["remote"] == "Windows":
                    self.machineType.set(0)
                else:
                    self.machineType.set(1)

                #self.machineType.set(entry["remote"])
                self.radioYesNo()
                if len(entry["logpaths"]) > 1:
                    for i in range(1, len(entry["logpaths"])):
                        self.addPath()
                for i in range(len(entry["logpaths"])):
                    self.pathBoxes[i].insert(0, entry["logpaths"][i][0])
                    self.keywordBoxes[i].insert(0, entry["keywords"][i][0])
                    
                if platform.system() == "Windows":
                    print entry.keys()
                    if "winSystemKeywords" in entry.keys():
                        self.winSystemKeywordsBox.insert(0, entry["winSystemKeywords"])
                    if "winAppKeywords" in entry.keys():
                        self.winAppKeywordsBox.insert(0, entry["winAppKeywords"])
                    if "winSecurityKeywords" in entry.keys():
                        self.winSecurityKeywordsBox.insert(0, entry["winSecurityKeywords"])

    def toggleSystemCheck(self):
        '''Uses the self.systemCheck'''
        if self.systemCheck.get():
            self.winSystemKeywordsBox.configure(state='normal')
        else:
            self.winSystemKeywordsBox.configure(state='disabled')

    def toggleAppCheck(self):
        '''Uses the self.appCheck'''
        if self.appCheck.get():
            self.winAppKeywordsBox.configure(state='normal')
        else:
            self.winAppKeywordsBox.configure(state='disabled')


    def toggleSecurityCheck(self):
        if self.securityCheck.get():
            self.winSecurityKeywordsBox.configure(state='normal')
        else:
            self.winSecurityKeywordsBox.configure(state='disabled')

