from Tkinter import *
import tkFont
import ttk
from tkMessageBox import *
import os
from subprocess import PIPE, Popen
from tkFileDialog import askopenfilename #, asksaveasfilename
from window import WindowABC
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
#import time
from constants import *
import platform

class Grapher(object):
    def __init__(self, root, main, info={}):
        self.name = "graph"
        self.root = root
        self.main = main
        self.info = info
        self.olddir = os.getcwd()
        self.tree_header = ["Name", "Time", "Date"]
        #print self.info
        #print "DATA WINDOW INFO"
        #print self.root.winfo_width(), self.root.winfo_height()
        
        #self.root.minsize(width=root.winfo_width(), height=271)
        self.win = WindowABC()
        self.createWindow()
        #self.setSettings()

    def destroy(self):
        print "Destroy the grapher settings"
        #print os.getcwd()
        os.chdir(self.olddir)
        #print os.getcwd()
        self.mainFrame.pack_forget()
        self.mainFrame.grid_forget()
        self.mainFrame.destroy()

    def createWindow(self):
        '''Create initial window with one machine'''
        self.mainFrame = self.win.newFrame(self.root, 20, 20)
        self.win.newLabel(self.mainFrame, "Data Analysis", colspan=3)
        #self.reportBox = self.win.newListbox(self.mainFrame, mode=SINGLE, width=50, row=1, colspan=3, yscroll=True)
        self.tree = self.win.newMultiColumnListBox(self.mainFrame, self.tree_header, row=1, colspan=2, height=15)
        self.readButton = self.win.newButton(self.mainFrame, "Read", row=3, width=20, sticky=W)
        self.graphButton = self.win.newButton(self.mainFrame, "Graph", row=3, col=1, width=20, sticky=E)
        #self.pathButton = self.win.newButton(self.mainFrame, text="Report Path", row=3, fg=TEXTCOLOR, bg=BUTTONCOLOR)
        #self.pathBox = self.win.newEntry(self.mainFrame, width=40, row=3, col=1, colspan=2, sticky=W+E)
        #self.generateButton = self.win.newButton(self.mainFrame, text="Generate Graph", row=4, fg=TEXTCOLOR, bg=BUTTONCOLOR)
        #self.win.newLabel(self.mainFrame, "Bins", row=4, col=1, sticky=E)
        #self.binBox = self.win.newEntry(self.mainFrame, width=5, row=4, col=2, sticky=W)
        #self.pathButton.config(command=self.openSaveDirectory)
        self.graphButton.config(command=self.generateGraph)
        self.readButton.config(command=self.readReport)
        self.fillListBox()
        self.mainFrame.pack()

    #def openSaveDirectory(self):
    #    folder = askopenfilename(parent=self.root, title="Save Folder")
    #    self.pathBox.delete(0, END)
    #    self.pathBox.insert(0, folder)

    def getEndDates(self, filename):
        data = open(filename, "r").read()
        data_lines = data.split("\n")
        return data_lines[1][:16], data_lines[-2][:16]

    def getGraphPoints(self, filename, binsize=10):
        try:
            binsize = int(binsize)
        except ValueError:
            return []
        else:
            if binsize <= 0:
                return []

        #binsize = test
        binsize *= 60
        times = []
        pctype = filename.split("/")[-1].split("-")[0]
        #print pctype
        if pctype == "Windows":
            with open(filename) as f:
                for line in f:
                    if "Event Date/Time:" in line:
                        datetime = line.split("Event Date/Time:")[1]
                        #print datetime
                        datetime = datetime.strip()
                        date = datetime.split(" ")[0]
                        time = datetime.split(" ")[1]
                        #print date, time
                        month, day, year = date.split("/")
                        hour, minute, second = time.split(":")
                        seconds = int(second) + 60 *(int(minute)+60*(int(hour)+24*(int(day)+30*int(month))))
                        times.append(seconds)
            times.reverse()
                        
                
        else:
            data = open(filename, "r").read()
            data_lines = data.split("\n")

            for i in range(1, len(data_lines)):
                if len(data_lines[i]) > 0:
                    datetime = data_lines[i][:15].split(":")
                    if len(datetime) == 3:
                        date = datetime[0].split(" ")
                        month = date[0].lower()
                        day = int(date[-2])
                        hour = int(date[-1])
                        minute = int(datetime[-2])
                        second = int(datetime[-1])
                        monthDict = {"jan":1, "feb":2, "mar":3, "apr":4, "may":5, "jun":6, 
                                     "jul":7, "aug":8, "sep":9, "oct":10, "nov":11, "dec":12}
                        month = monthDict[month]
                        seconds = second + 60 * (minute + 60 * (hour + 24 * (day + 30 * month)))
                        times.append(seconds)

        print len(times)
        print times[0:10]
        print binsize
        times = np.array(times) - times[0]
        print times[0:10]
        bins = []
        num = 0
        for i in range(len(times)):
            if times[i] <= binsize:
                num += 1
            else:
                bins.append(num)
                num = 1
                times -= times[i]
        print bins
        return bins

    def fillListBox(self):
        '''Find the reports this machine generated.  We know this by the UID and server'''
        #self.olddir = os.getcwd()
        #print self.info #Dictionary of actual machine clicked on
        os.chdir("Records")
        allreports = os.listdir(os.getcwd())
        monthDict = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",
                     7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        self.reportDict = {}
        for r in allreports:
            name, date, time = r.split("_")
            year, month, day = date.split("-")
            hour = time.split(".")[0][:2]
            minute = time.split(".")[0][2:]
            values = [year, month, day, hour, minute, name]
            self.reportDict[r] = values
        #print "REPORT DICTIONARY"
        #print self.reportDict
        orderedList = self.sortDateTimes(self.reportDict)
        #print "ORDERED LIST"
        #print orderedList
        self.lookupReport = {}
        
        names = []
        dates = []
        times = []
        for el in orderedList:
            year, month, day, hour, minute, name = el
            date = str(monthDict[int(month)])+" "+str(day)+", "+str(year)
            time = str(hour)+":"+str(minute)
            names.append(name)
            dates.append(date)
            times.append(time)

        treeList = []
        for i in range(len(names)):
            treeList.append((names[i], times[i], dates[i]))

        #print "TREE LIST"
        #print treeList
        #print ""
        for item in treeList:
            self.tree.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.tree_header[ix], width=None)<col_w:
                    self.tree.column(self.tree_header[ix], width=col_w)
            
        #names = self.tabify(names)
        #dates = self.tabify(dates)
        #times = self.tabify(times)
        #val = self.tabify(str(monthDict[int(month)])+" "+str(day)+", "+str(year))+time
        #print len(orderedList), len(treeList)
        #print ""
        #print ""
        for i, el in enumerate(orderedList):
            #val = names[i]+dates[i]+times[i]
            #print val
            #val = names[i]+", "+ times[i]+", "+ dates[i]
            val = (names[i], times[i], dates[i])
            #self.reportBox.insert(END, val)
            for filename in self.reportDict.keys():
                if self.reportDict[filename] == el:
                    self.lookupReport[val] = filename
        #print "LOOKUP REPORT"
        #print self.lookupReport

    def sortDateTimes(self, d):
        '''Sort the date and time from past to present.'''
        values = d.values()
        values.sort()
        return values

    def getFilenameFromTable(self):
        '''Get the filename that has the focus in the tree'''
        currentItem = self.tree.focus()
        item = self.tree.item(currentItem)
        return self.lookupReport[tuple(item['values'])]
    
    def readReport(self):
        '''Get the selected item in the listbox and then open up a new window to read the contents'''
        #selected = self.reportBox.get(ACTIVE)
        #print "Selected in TREE"
        #print selected
        selected = self.getFilenameFromTable()
        #currentItem = self.tree.focus()
        #print currentItem
        #itemDict = self.tree.item(currentItem)
        #print itemDict['values']
        #print "LOOKUP THE VALUE IN THE DICTIONARY"
        #print self.lookupReport[tuple(itemDict['values'])]
        #selected = self.lookupReport[tuple(itemDict['values'])]
        #print help(self.tree.selection)
        #print self.tree.selection()
        contents = open(selected).readlines()

        root = Tk()
        root.wm_title(selected)
        mainframe = self.win.newFrame(root, 10, 10)
        listbox = self.win.newListbox(mainframe, xscroll=True, yscroll=True, width=120, height=40)
        for line in contents:
            linemod = line.split('\n')[0]
            listbox.insert(END, linemod)
        root.mainloop()

    def generateGraph(self):
        '''Open up a new Window and have the graphing controls on new window'''
        #selected = self.reportBox.get(ACTIVE)
        selected = self.getFilenameFromTable()
        filename = os.getcwd()+"/"+selected
        root = Tk()
        root.wm_title(selected)
        self.graphframe = self.win.newFrame(root, 10, 10)
        self.win.newLabel(self.graphframe, "Bins", sticky=W)
        self.binBox = self.win.newEntry(self.graphframe, width=5, col=1, sticky=W)
        self.binBox.insert(END, '10')
        graphUpdateButton = self.win.newButton(self.graphframe, "Update", col=2, sticky=W)
        graphUpdateButton.config(command=self.updateGraph)
        self.graphframe.pack()
        self.canvas = self.win.newCanvas(self.graphframe, row=1, colspan=3, yscroll=False)
        #f = Figure(figsize=(5,5))
        #a = f.add_subplot(111)
        self.drawGraph(filename)
        """
        values = self.getGraphPoints(filename, self.binBox.get())
        if len(values) > 0:
            start, end = self.getEndDates(filename)
            xvalues = range(len(values))
            a.plot(xvalues, values)
            a.set_title(start + "  " + end)
            a.set_ylabel("Number of Entries")
            a.set_xlabel("Time per unit = " + str(self.binBox.get()) + " minutes")
            canvas2 = FigureCanvasTkAgg(f, canvas)
            canvas2.get_tk_widget().pack()
            canvas2.show()
        else:
            showinfo("Error Value", "Need to use integer values!")
        """
        root.mainloop()

    def updateGraph(self):
        '''Redraw the graph on the canvas'''
        #selected = self.reportBox.get(ACTIVE)
        selected = self.getFilenameFromTable()
        filename = os.getcwd()+"/"+selected
        self.canvas.destroy()
        self.canvas = self.win.newCanvas(self.graphframe, row=1, colspan=3, yscroll=False)
        self.drawGraph(filename)

    def drawGraph(self, filename):
        f = Figure(figsize=(5,5))
        a = f.add_subplot(111)
        values = self.getGraphPoints(filename, self.binBox.get())
        if len(values) > 0:
            start, end = self.getEndDates(filename)
            xvalues = range(len(values))
            a.plot(xvalues, values)
            a.set_title(start + "  " + end)
            a.set_ylabel("Number of Entries")
            a.set_xlabel("Time per unit = " + str(self.binBox.get()) + " minutes")
            canvas2 = FigureCanvasTkAgg(f, self.canvas)
            canvas2.get_tk_widget().pack()
            canvas2.show()
        else:
            showinfo("Error Value", "Need to use integer values!")


        



