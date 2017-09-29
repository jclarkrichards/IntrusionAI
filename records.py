from Tkinter import *
from tkMessageBox import *
import os
from subprocess import PIPE, Popen
#import numpy as np
#from scipy import ndimage
#import shutil
#from tkFileDialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
from window import WindowABC
import time
import platform
if platform.system() == "Windows":
    import logwin
import emailer

class MachineRecord(object):
    def __init__(self, root, keywords="", UID="", name="", ip="",
                 paths=[], savepath="", email=""):
        self.platform = platform.system()
        self.root = root
        self.trimdate = trimdate
        self.frequency = frequency
        self.frequencyVal = None
        self.email = email
        self.timer = None
        self.name = ""
        if savepath == "":
            savepath = os.getcwd()
        self.savepath = savepath
        self.paths=paths
        self.baseDirectory = os.getcwd()#"/home/jonathan/Documents/IPBlockApp"
        self.pathBoxes = []
        self.pathrow = 11 #row to add next path box if added
        self.removePathButtons = []
        self.win = WindowABC()
        self.col0Width = 15
        self.win.newLabel(self.root, "====================================================", colspan=3)
        self.win.newLabel(self.root, "Machine Name", width=25, row=1)
        self.win.newLabel(self.root, "Local Machine", width=25, row=2)
        self.win.newLabel(self.root, "Remote Machine Type", width=25, row=4)
        self.yesno = IntVar()
        radios = self.win.newRadioButton(self.root, self.yesno, [("Yes", 1), ("No", 0)], row=2, col=1, sticky=N+S+W) 
        for radio in radios:
            radio.config(command=self.radioYesNo)
        
        self.machineType = IntVar()
        self.radios = self.win.newRadioButton(self.root, self.machineType, [("Windows", 0), ("Linux", 1)], row=4, col=1, sticky=N+S+W)
        for radio in self.radios:
            radio.config(command=self.radioMachineType)

        self.win.newLabel(self.root, "Server Name", row=6)
        self.win.newLabel(self.root, "IP Address", row=7)
        self.win.newLabel(self.root, "Port", row=8)
        self.win.newLabel(self.root, "Password", row=9)
        if self.platform == "Linux" or self.platform == "Windows":
            self.win.newLabel(self.root, "Keywords", row=10, col=1)
            self.win.newLabel(self.root, "Path to Logs", row=10)
        #elif self.platform == "Windows":
        #    self.win.newLabel(self.root, "Keywords", row=4, colspan=2)

        self.nameBox = self.win.newEntry(self.root, row=1, col=1)
        if UID != []:
            self.nameBox.insert(0, UID)

        self.serverBox = self.win.newEntry(self.root, row=6, col=1)
        if name != []:
            self.serverBox.insert(0, name)

        self.ipBox = self.win.newEntry(self.root, row=7, col=1)
        if ip != []:
            self.ipBox.insert(0, ip)

        self.portBox = self.win.newEntry(self.root, row=8, col=1)
        self.passwordBox = self.win.newEntry(self.root, show="*", row=9, col=1)

        self.pathBoxes = []
        self.keywordBoxes = []
        if self.platform == "Linux" or self.platform =="Windows":
            if len(paths) > 0:
                for i, path in enumerate(paths):
                    self.pathBoxes.append(self.win.newEntry(self.root, row=self.pathrow))
                    self.pathBoxes[-1].insert(0, path)
                    self.keywordBoxes.append(self.win.newEntry(self.root, row=self.pathrow, col=1))
                    self.keywordBoxes[-1].insert(0, keywords)
                    self.removePathButtons.append(self.win.newButton(self.root, row=self.pathrow, col=2, sticky=W))
                    self.pathrow += 1
            else:
                self.pathBoxes.append(self.win.newEntry(self.root, row=self.pathrow))
                self.keywordBoxes.append(self.win.newEntry(self.root, row=self.pathrow, col=1))
                self.keywordBoxes[-1].insert(0, keywords)
                self.pathrow += 1
                
        #elif self.platform == "Windows":
        #    self.keywordBoxes.append(self.win.newEntry(self.root, row=self.pathrow, colspan=2))
        #    self.keywordBoxes[-1].insert(0, keywords)
            
        self.addBelowPath()
        self.destroyed = False

    def addBelowPath(self):
        '''Add the rest of the entries below path boxes'''
        if self.platform == "Linux" or self.platform == "Windows":
            self.addPathButton = self.win.newButton(self.root, text="Add File Path", row=self.pathrow, colspan=2)
        self.connectButton = self.win.newButton(self.root, text="Run Once", row=self.pathrow+2)
        self.scheduleButton = self.win.newButton(self.root, text="Run ", row=self.pathrow+2, col=1)
        self.stopButton = self.win.newButton(self.root, text="Stop Run", row=self.pathrow+2, col=2)
        self.removeButton = self.win.newButton(self.root, text="Remove Machine",
                                               row=self.pathrow+1, col=1)
        self.saveButton = self.win.newButton(self.root, text="Save Machine", row=self.pathrow+1)
        #self.divider = self.win.newLabel(self.root, "=======================================", row=self.pathrow+3, colspan=3)
        self.radioYesNo()
        #if self.platform == "Linux":
        #    self.connectButton.config(command=self.Linux2Linux)
        #elif self.platform == "Windows":
        #    self.connectButton.config(command=self.Windows2Linux)
            
        self.stopButton.config(command=self.stop)
        if self.platform == "Linux" or self.platform == "Windows":
            self.addPathButton.config(command=self.addPath)
        self.removeButton.config(command=self.selfDestruct)
        self.saveButton.config(command=self.saveMachine)
        self.scheduleButton.config(command=self.scheduleMachine)

    def addPath(self):
        '''Add a path entry box below last one added'''
        self.addPathButton.destroy()
        self.connectButton.destroy()
        self.stopButton.destroy()
        self.removeButton.destroy()
        self.saveButton.destroy()
        self.scheduleButton.destroy()
        #self.divider.destroy()
        self.pathBoxes.append(self.win.newEntry(self.root, row=self.pathrow))
        self.keywordBoxes.append(self.win.newEntry(self.root, row=self.pathrow, col=1))
        im = "/home/jonathan/Downloads/IPBlockApp/Images/x.png"
        image = Image.open(im)
        photo = ImageTk.PhotoImage(image)

        self.removePathButtons.append(self.win.newButton(self.root, text="R", row=self.pathrow, col=2, sticky=W, image=photo))
        self.removePathButtons[-1].config(command=lambda m=len(self.removePathButtons): self.removePath(m))
        #self.removePathButtons[-1].config(command=self.removePath)
        self.pathrow += 1
        self.addBelowPath()

    def removePath(self, m):
        '''Remove a path entry box'''
        self.pathBoxes[m].destroy()
        self.keywordBoxes[m].destroy()
        self.removePathButtons[m-1].destroy()
        

    def radioYesNo(self):
        '''When the Yes/No radio buttons are pressed'''
        if self.yesno.get() == 0:
            self.serverBox.configure(state="normal")
            self.ipBox.configure(state="normal")
            self.portBox.configure(state="normal")
            self.passwordBox.configure(state="normal")
            self.radios[0].configure(state="normal")
            self.radios[1].configure(state="normal")
            self.radioMachineType()

        else:
            self.serverBox.configure(state="disabled")
            self.ipBox.configure(state="disabled")
            self.portBox.configure(state="disabled")
            self.passwordBox.configure(state="disabled")
            self.radios[0].configure(state="disabled")
            self.radios[1].configure(state="disabled")
            if platform.system() == "Windows":
                self.connectButton.config(command=self.Windows2Self)
                print "Windows -> Self"
            else:
                self.connectButton.config(command=self.Linux2Self)
                print "Linux -> Self"

    def radioMachineType(self):
        if self.machineType.get() == 0:
            if platform.system() == "Windows":
                self.connectButton.config(command=self.Windows2Windows)
                print "Windows -> Windows"
            else:
                self.connectButton.config(command=self.Linux2Windows)
                print "Linux -> Windows"
        else:
            if platform.system() == "Windows":
                self.connectButton.config(command=self.Windows2Linux)
                print "Windows -> Linux"
            else:
                self.connectButton.config(command=self.Linux2Linux)
                print "Linux -> Linux"
            

    # Connecting Linux -> Self, Linux, Windows
    def Linux2Self(self):
        print "Connecting Linux to Self"
        paths = []
        for path in self.pathBoxes:
            p = path.get()
            if p != "":
                paths.append(p)
                
        result = []
        for path in paths:
            result += open(path, "r").readlines()
            print type(result)
            #print len(result)
            #print result[4]
            result[-1] += "\n\n" + path + "\n\n"
            
        reported = self.trimResults(result)
        #print type(reported)
        if reported:
            if self.frequencyVal is None:
                showinfo("Saved", "Report Saved at "+ self.savepath)
        else:
            showinfo("Empty", "Nothing to report")
        if self.frequencyVal is not None:
            self.timer = self.root.after(self.frequencyVal, self.Linux2Self)

    def Linux2Linux(self):
        '''Connect to server, read log file and return contents.  Ultimately want to loop through all machines'''
        print "Connecting Linux to Linux"
        name = self.serverBox.get()

        ipaddress = self.ipBox.get()
        password = self.passwordBox.get()

        paths = []
        for path in self.pathBoxes:
            paths.append(path.get())

        port = self.portBox.get()
        #path = self.pathBox.get()#+"/mail.log"
        #command = "cat"
        command = ""
        for path in paths:
            command = command + "echo " + "\""+path+"\"" +"; cat " + path + "; "
            #command = command + " " + path
        command = command + "echo"
        if port == "":
            cmd = ["sshpass", "-p", password, "ssh", "-X", name+"@"+ipaddress, command]
        else:
            cmd = ["sshpass", "-p", password, "ssh", "-X", name+"@"+ipaddress, "-p", port, command]
            
        ssh = Popen(cmd, stdout=PIPE, stderr=PIPE)
        result = ssh.stdout.readlines()
        if len(result) > 0:
            reported = self.trimResults(result)
            if reported:
                if self.frequencyVal is None:
                    showinfo("Saved", "Report Saved at "+ self.savepath)
            else:
                showinfo("Empty", "Nothing to report")
            if self.frequencyVal is not None:
                self.timer = self.root.after(self.frequencyVal, self.Linux2Linux)


    def Linux2Windows(self):
        print "Connecting Linux to Windows"
        
            

    # Connect Windows -> Self, Linux, Windows
    def Windows2Self(self):
        print "Connecting Windows to Self"
        server = None
        logTypes = ["System", "Application", "Security"]
        temp = self.keywordBoxes[0].get()
        keywords = temp.split(", ")
        savefolder = self.getSaveFolderWindows()
        logwin.getAllEvents(server, logTypes, savefolder, keywords, self.trimdate)

    def Windows2Linux(self):
        print "Connecting Windows to Linux"
        name = self.serverBox.get()
        ipaddress = self.ipBox.get()
        password = self.passwordBox.get()

        paths = []
        for path in self.pathBoxes:
            paths.append(path.get())

        command = ""
        for path in paths:
            command = command + "echo " + "\""+path+"\"" +"; cat " + path + "; "
        command = command + "echo"

        cmd = ["plink.exe", name+"@"+ipaddress, "-pw", password, "-C", command]
        #print cmd
        ssh = Popen(cmd, stdout=PIPE, stderr=PIPE)
        result = ssh.stdout.readlines()
        #print len(result)
        if len(result) > 0:
            reported = self.trimResults(result)
            if reported:
                if self.frequencyVal is None:
                    showinfo("Saved", "Windows Report Saved at "+ self.savepath)
            else:
                showinfo("Empty", "Nothing to report")
            if self.frequencyVal is not None:
                self.timer = self.root.after(self.frequencyVal, self.Windows2Linux)
        
    def Windows2Windows(self):
        print "Connecting Windows to Windows"
        '''Method for connecting to a server while on a Windows platform'''
        #Connect to server.  Testing on local machine.
        pass

    def getSaveFolderWindows(self):
        '''Get the folder we need to save the results in when on Windows platform'''
        if "Records" not in os.listdir(self.savepath):
            os.mkdir(self.savepath+"/Records")
        return self.savepath+"\Records"

    
    def trimResults(self, result):
        '''result is a list of strings.  We only want to keep the entries that contain any of the keywords'''
        paths = []
        for path in self.pathBoxes:
            paths.append(path.get()+"\n")
        keywordList = []
        for k in self.keywordBoxes:
            keywordList.append(k.get())
        print paths
        print len(result)
        #keywords = self.keywordBox.get()
        #keywords = keywords.split(",")
        report = []
        keywords = []
        currentTime = time.localtime()
        for i, line in enumerate(result):
            if line in paths:
                print line
                if i == 0:
                    report.append(line)
                else:
                    report.append("\n\n" + line)
                index = paths.index(line)
                keywords = keywordList[index]
                keywords = keywords.split(",")
                if len(keywords) == 1:
                    if keywords[0] == "":
                        keywords = []
                #print keywords
            else:
                if len(keywords) > 0:
                    for keyword in keywords:
                        #modify the case for this keyword; upper, lower, and first letter upper
                        keyMod1 = keyword.upper()
                        keyMod2 = keyword.lower()
                        keyMod3 = keyword[0].upper()+keyMod2[1:]
                        #print keyword, keyMod1, keyMod2, keyMod3
                        if keyword in line or keyMod1 in line or keyMod2 in line or keyMod3 in line:
                            if len(line) > 16:
                                writeToReport = self.filterViaTime(line, currentTime)
                                if writeToReport:
                                    report.append(line)
                else:
                    if len(line) > 16:
                        writeToReport = self.filterViaTime(line, currentTime)
                        if writeToReport:
                            report.append(line)
                    

        if len(report) > 0:
            name = self.generateFilename()
            if "Records" not in os.listdir(self.savepath):
                os.mkdir(self.savepath+"/Records")
            #if self.savepath != "":
            f = open(self.savepath+"/Records/"+name, "w+")
            #else:
            #    f = open(name, "w+")                
            for line in report:
                f.write(line)
            
            if self.email != "":
                print "Reading generated mesage"
                message = open(self.savepath+"/Records/"+name).read()
                emailer.sendEmail(message, self.email)
            return True
        else:
            return False
                
            
    def generateFilename(self):
        ct = time.localtime()
        name = self.serverBox.get()
        if name == "":
            #print platform.system == "Linux"
            name = platform.system()
            #print type(name)
        return name+"_"+str(ct.tm_year)+"-"+str(ct.tm_mon).zfill(2)+"-"+str(ct.tm_mday).zfill(2)+"_"+str(ct.tm_hour).zfill(2)+str(ct.tm_min).zfill(2)+".txt"
        
        
    def filterViaTime(self, line, current_time):
        '''Assuming all lines start with a time in the format of:  Mmm dd hh:mm:ss'''        
        month = line[:3]
        day = int(line[4:6])
        hour = int(line[7:9])
        minute = int(line[10:12])
        second = int(line[13:15])
        monthDict = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, 
                     "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
        month = monthDict[month]

        #print month, day, hour, minute, second
        #seconds = second + minute * 60 + hour * 3600 + day * 86400
        seconds = second + 60 * (minute + 60 * (hour + 24 * (day + 30 * month)))
        month_now = current_time.tm_mon
        day_now = current_time.tm_mday
        hour_now = current_time.tm_hour
        min_now = current_time.tm_min
        sec_now = current_time.tm_sec
        #seconds_now = sec_now + min_now * 60 + hour_now*3600 + day_now*86400
        seconds_now = sec_now + 60 * (min_now + 60 * (hour_now + 24 * (day_now + 30 * month_now)))
        time_dif = seconds_now - seconds
        time_check = 0
        #print "TRIM DATE"
        #print self.trimdate
        #print "END TRIM DATE"
        if self.trimdate == "5 min":
            time_check = 5*60
        elif self.trimdate == "10 min":
            time_check = 10*60
        elif self.trimdate == "30 min":
            time_check = 30*60
        elif self.trimdate == "1 hour":
            time_check = 60*60
        elif self.trimdate == "1 day":
            time_check = 24*60*60
        elif self.trimdate == "1 week":
            time_check = 7*24*60*60
        elif self.trimdate == "1 month":
            time_check = 30*24*60*60
        else:
            return True
        #print time_dif, time_check
        if time_dif <= time_check:
            return True
        return False

    def stop(self):
        #print self.timer
        self.root.after_cancel(self.timer)
        showinfo("Stopped!", "Scheduler has been stopped!")

    def test(self):
        print "hello there"
        #self.timer = self.root.after(2000, self.test)

    def scheduleMachine(self):
        #self.test()
        #needs to be in milliseconds
        if self.frequency == "2 Min":
            freq = 2*60*1000
        elif self.frequency == "hourly":
            freq = 60*60*1000
        elif self.frequency == "Every 6 hours":
            freq = 60*60*6*1000
        elif self.frequency == "Every 12 hours":
            freq = 60*60*12*1000
        elif self.frequency == "daily":
            freq = 60*60*24*1000
        elif self.frequency == "weekly":
            freq = 60*60*24*7*1000
        elif self.frequency == "monthly":
            freq = 60*60*24*30*1000
        else:
            freq = None

        self.frequencyVal = freq
        if self.platform == "Linux":
            self.Linux2Linux()
        elif self.platform == "Windows":
            self.Windows2Linux()
        #print self.frequency

    def update(self):
        pass

    def saveMachine(self):
        '''open up a file where we want to save this machine and add a new entry'''
        os.chdir(self.baseDirectory)
        try:
            f = open("machines.txt")
        except IOError:
            f = open("machines.txt", "w")
        finally:
            f.close()
            s = self.nameBox.get() + ", " + self.serverBox.get() + ", " + self.ipBox.get()
            for pathBox in self.pathBoxes:
                s = s + ", " + pathBox.get()
            s += "\n"
            lines = []
            uids = []
            with open("machines.txt") as f:
                for line in f:
                    lines.append(line)
                    uids.append(line.split(",")[0])
            #print lines
            #print names
            if self.nameBox.get() in uids:
                i = uids.index(self.nameBox.get())
                line = lines[i]
                newline = self.nameBox.get() + ", " + self.serverBox.get() + ", " + self.ipBox.get()
                for pathBox in self.pathBoxes:
                    newline = newline + ", " + pathBox.get()
                s += "\n"
                lines[i] = newline
            else:
                lines.append(s)
            f.close()
            s = ""
            for line in lines:
                s += line
            f = open("machines.txt", "w")
            f.write(s)
            f.close()
            showinfo("Saved", "Configuration has been saved")


    def selfDestruct(self):
        self.root.destroy()
        self.destroyed = True
        

