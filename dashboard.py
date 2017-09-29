from Tkinter import *
from tkMessageBox import *
import os
from subprocess import PIPE, Popen
from tkFileDialog import askdirectory #askopenfilename, asksaveasfilename
from window import WindowABC, VerticalScrollFrame
from PIL import Image, ImageTk
from machinetemplate import Machine
import json
from constants import *
import platform
from copy import deepcopy
#from connections import *
from connections import Connections
from grapher import Grapher


class Dashboard(object):
    def __init__(self, root, main):
        self.name = "dashboard"
        self.root = root
        self.main = main
        #print "DASHBOARD WINDOW INFO"
        #print dir(root)
        #print root.winfo_width(), root.winfo_height(), root.winfo_x(), root.winfo_y()
        #self.root.minsize(width=root.winfo_width(), height=500)
        self.win = WindowABC()
        #self.reloadWindow()
        # Handles the various buttons each machine will have 
        self.status = []
        self.machineButtons = [] #Holds the buttons for editing the machines
        self.deleteButtons = [] #Hold the buttons to delete the machines
        self.runButtons = []
        self.rerunButtons = []
        self.graphButtons = []
        self.machineLogos = []
        self.copyButtons = []
        #self.machines = {"edit":[], "delete":[], "server":[], "generate":[], "analyze":[], "schedule":[]}
        self.createWindow()

    def reloadWindow(self):
        '''Reload this window'''
        self.destroy()
        self.status = []
        self.machineButtons = [] #Holds the buttons for editing the machines
        self.deleteButtons = [] #Hold the buttons to delete the machines
        self.runButtons = []
        self.rerunButtons = []
        self.graphButtons = []
        self.machineLogos = []
        self.copyButtons = []
        self.createWindow()
        
    def destroy(self):
        #self.mainFrame.pack_forget()
        #self.mainFrame.destroy()
        self.mainFrame.pack_forget()
        self.mainFrame.grid_forget()
        self.scrollFrame.pack_forget()
        self.scrollFrame.grid_forget()
        self.mainFrame.destroy()
        self.scrollFrame.destroy()


    def saveDatafile(self):
        '''Save whatever is in self.data into the data file'''
        with open(JSONFILE, "w") as datafile:
            json.dump(self.data, datafile)

    def readDatafile(self):
        '''See if data.json exists.  If it does then pull data from it and return the data'''
        try:
            open(JSONFILE)
        except IOError:
            return {}
        else:
            with open(JSONFILE) as datafile:
                data = json.load(datafile)
            return data

    def createWindow(self):
        '''Create initial window with one machine'''
        self.data = self.readDatafile()
        im_ai = self.formatImage(AILOGO)
        im_x = self.formatImage(CANCELSMALL)
        im_run = self.formatImage(RUNONCELOGO)
        im_rerun = self.formatImage(SCHEDULELOGO)
        im_graph = self.formatImage(GRAPHLOGO)
        im_win = self.formatImage(WINLOGO)
        im_linux = self.formatImage(LINUXLOGO)
        im_copy = self.formatImage(COPYLOGO)
        im_good = self.formatImage(STATUSGOOD)

        self.scrollFrame = VerticalScrollFrame(self.root)
        self.mainFrame = self.scrollFrame.interior
        #self.mainFrame = self.win.newFrame(self.root, 20, 20, bg="#e3f7eb")
        self.win.newLabel(self.mainFrame, text="Intrusion", fg="black", bg="#e3f7eb", 
                          font=("Helvetica", 30, "bold"))
        self.win.newLabel(self.mainFrame, text="AI", col=2, fg="black", bg="#e3f7eb", 
                          font=("Helvetica", 30, "bold"))
        self.win.newLabel(self.mainFrame, image=im_ai, col=1, bg="#e3f7eb")
        self.subFrame = self.win.newFrame(self.mainFrame, 20, 20, bg="#c6d1ca", row=1, colspan=3)

        rowval = 1
        if len(self.data) > 0:
            for i in range(len(self.data["machine"])):
                self.status.append(self.win.newLabel(self.subFrame, image=im_good, sticky=EW, row=rowval, bg="#c6d1ca")) 
                self.machineButtons.append(self.win.newButton(self.subFrame, text=self.data["machine"][i]["name"], row=rowval, col=1))
                #self.machineButtons[-1].bind("<Enter>", self.machineButtonHoverEnter)
                #self.machineButtons[-1].bind("<Leave>", self.machineButtonHoverLeave)

                if self.data["machine"][i]["local"]:
                    if platform.system() == "Windows":
                        self.machineLogos.append(self.win.newLabel(self.subFrame, row=rowval, col=2, 
                                                                   sticky=EW, image=im_win, bg="#c6d1ca"))
                    else:
                        self.machineLogos.append(self.win.newLabel(self.subFrame, row=rowval, col=2, 
                                                                   sticky=EW, image=im_linux, bg="#c6d1ca"))
                else:
                    if self.data["machine"][i]["remote"] == "Windows":
                        self.machineLogos.append(self.win.newLabel(self.subFrame, row=rowval, col=2, 
                                                                   sticky=EW, image=im_win, bg="#c6d1ca"))
                    else:
                        self.machineLogos.append(self.win.newLabel(self.subFrame, row=rowval, col=2, 
                                                                   sticky=EW, image=im_linux, bg="#c6d1ca"))


                self.copyButtons.append(self.win.newButton(self.subFrame, row=rowval, col=3, sticky=EW, image=im_copy))
                self.runButtons.append(self.win.newButton(self.subFrame, row=rowval, col=4, sticky=EW, image=im_run))
                self.rerunButtons.append(self.win.newButton(self.subFrame, row=rowval, col=5, sticky=EW, image=im_rerun))
                self.graphButtons.append(self.win.newButton(self.subFrame, row=rowval, col=6, sticky=EW, image=im_graph))
                self.deleteButtons.append(self.win.newButton(self.subFrame, row=rowval, col=7, sticky=EW, image=im_x))

                self.machineButtons[-1].config(command=lambda m=len(self.machineButtons): self.editMachine(m))
                self.copyButtons[-1].config(command=lambda m=len(self.copyButtons): self.copyMachine(m))
                self.deleteButtons[-1].config(command=lambda m=len(self.deleteButtons): self.removeMachine(m))
                self.runButtons[-1].config(command=lambda m=len(self.runButtons): self.runLogReporter(m))
                self.rerunButtons[-1].config(command=lambda m=len(self.rerunButtons): self.rerunLogReporter(m))
                self.graphButtons[-1].config(command=lambda m=len(self.graphButtons): self.graphReport(m))


                rowval += 1
        print "ROWVAL = " + str(rowval)
        newButton = self.win.newButton(self.mainFrame, text="New", row=2)
        newButton.config(command=self.createNewMachine)

        #print type(self.mainFrame)
        #print dir(self.mainFrame)
        self.subFrame.grid_columnconfigure(0, weight=1)
        self.subFrame.grid_columnconfigure(1, weight=1)
        self.subFrame.grid_columnconfigure(2, weight=1)
        self.subFrame.grid_columnconfigure(3, weight=1)
        self.subFrame.grid_columnconfigure(4, weight=1)
        self.subFrame.grid_columnconfigure(5, weight=1)
        self.subFrame.grid_columnconfigure(6, weight=1)
        self.subFrame.grid_columnconfigure(7, weight=1)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.mainFrame.grid_columnconfigure(1, weight=1)
        self.mainFrame.grid_columnconfigure(2, weight=1)
    #def machineButtonHoverEnter(self, event):
    #    self.machineButtons[0].configure(text="Hello")
    #    #print "hello"

    #def machineButtonHoverLeave(self, enter):
        #index -= 1
        #print "bye"
   #     self.machineButtons[0].configure(text="Bye")

    def createNewMachine(self):
        '''Go to the machine template window to add the required information'''
        self.destroy()
        self.main.layout = Machine(self.root, self.main)

    def removeMachine(self, index):
        '''Remove a machine from the JSON file'''
        index -= 1
        junk = self.data["machine"].pop(index)
        self.saveDatafile()
        self.reloadWindow()

    def copyMachine(self, index):
        '''Copy this machine and all of its data.  We just copy this entry and add it to the JSON file'''
        index -= 1
        entry = deepcopy(self.data["machine"][index])
        entry["UID"] = self.getNextID()
        self.data["machine"].append(entry)
        self.saveDatafile()
        self.reloadWindow()

    def editMachine(self, index):
        '''Send data at this index to the template and fill the template with this data'''
        index -= 1
        #print "Edit " + str(index) + " machine"
        self.destroy()
        self.main.layout = Machine(self.root, self.main, self.data["machine"][index]["UID"])

    def runLogReporter(self, index):
        '''When clicked a small window pops up allowing you to enter your password for this server if it is not a local machine'''
        index -= 1
        print "running log reporter"
        if not self.data["machine"][index]["local"]:
            self.miniroot = Tk()
            self.miniroot.wm_title("Enter Server Password")
            miniframe = self.win.newFrame(self.miniroot, 10, 10)
            s = self.data["machine"][index]["server"]
            self.win.newLabel(miniframe, "Server:", sticky=W)
            self.win.newLabel(miniframe, s, col=1, sticky=W)
            self.win.newLabel(miniframe, "Password:", row=1, sticky=W)
            self.password = self.win.newEntry(miniframe, show="*", row=1, col=1)
            button = self.win.newButton(miniframe, "Enter", row=1, col=2)
            button.config(command=lambda:self.runServerOnce(index))
            self.miniroot.mainloop()
            #showinfo("Run", "Running the report")
        else:
            showinfo("Run", "Running report")
            self.runServerOnce(index)

    def runServerOnce(self, index):
        '''Open the server and get the logs based on the info in self.data'''
        #print self.data["machine"][index]
        print "running server once"
        try:
            password = self.password.get()
        except AttributeError:
            password = None
        
        if password is not None:
            self.miniroot.destroy()
            del self.password
        p2p = Connections()
        p2p.runLogReporter(self.data, index, password=password)

    def runServerPeriodically(self, index):
        #self.miniroot.destroy()
        print "Running Periodically"
        print self.frequencyBox.get()
        print self.dateBox.get()
        #print self.password.get()
        p2p = Connections(self.root)
        try:
            password = self.password.get()
        except AttributeError:
            self.miniroot.destroy()
            p2p.runLogReporter(self.data, index, freq=self.frequencyBox.get(),
                               date_filter=self.dateBox.get())
        else:
            self.miniroot.destroy()
            del self.password
            #print password
            p2p.runLogReporter(self.data, index, freq=self.frequencyBox.get(),
                               date_filter=self.dateBox.get(), password=password)
        showinfo("Running", "This just ran")

    def rerunLogReporter(self, index):
        '''Opens up a small window asking for additional info and/or a password'''
        index -= 1

        self.miniroot = Tk()
        self.miniroot.wm_title("Additional Info")
        miniframe = self.win.newFrame(self.miniroot, 10, 10)
        self.win.newLabel(miniframe, "Frequency", sticky=W)
        self.win.newLabel(miniframe, "Filter Date", sticky=W, row=1)
        self.frequencyBox = StringVar(miniframe)
        opt_freq = ["2 Min", "hourly", "Every 6 hours", "Every 12 hours", "daily", "weekly", "monthly", "None"]
        self.dateBox = StringVar(miniframe)
        opt_date = ["5 min", "1 hour", "12 hours", "1 day", "1 week", "1 month", "All"]
        self.win.newDropMenu(miniframe, self.frequencyBox, opt_freq, col=1)
        self.win.newDropMenu(miniframe, self.dateBox, opt_date, row=1, col=1)

        if not self.data["machine"][index]["local"]:
            #s = self.data["machine"][index]["server"]
            #self.win.newLabel(miniframe, "Server:", sticky=W)
            #self.win.newLabel(miniframe, s, col=1, sticky=W)
            self.win.newLabel(miniframe, "Password:", row=2, sticky=W)
            self.password = self.win.newEntry(miniframe, show="*", row=2, col=1)
            button = self.win.newButton(miniframe, "Enter", row=2, col=2)
            button.config(command=lambda:self.runServerPeriodically(index))
            #self.miniroot.mainloop()
            #showinfo("Run", "Running the report")
        else:
            #showinfo("Run", "Running report")
            button = self.win.newButton(miniframe, "Enter", row=2, col=2)
            button.config(command=lambda:self.runServerPeriodically(index))
            
        self.miniroot.mainloop()




    def graphReport(self, index):
        index -= 1
        #miniroot = Tk()
        #miniroot.wm_title("Reports")
        #miniframe = self.win.newFrame(miniroot, 10, 10)
        #self.win.newLabel(miniframe, "Name of Machine")
        #self.win.newListbox(miniframe, mode=SINGLE, yscroll=True, row=1)
        #self.miniroot.mainloop()
        self.destroy()
        self.main.layout = Grapher(self.root, self.main, self.data["machine"][index])


    def formatImage(self, image_path):
        '''Format JPG and PNG images to work with Tkinter nicely'''
        im = image_path
        image = Image.open(im)
        return ImageTk.PhotoImage(image)

    def getNextID(self):
        '''Find the max UID in the data and increment it, then return it'''
        ids = []
        for i in range(len(self.data["machine"])):
            ids.append(self.data["machine"][i]["UID"])
        return max(ids) + 1
        



