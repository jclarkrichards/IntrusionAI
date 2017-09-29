from Tkinter import *
from window import WindowABC
import numpy as np
import time

class StatusIndicator(object):
    def __init__(self, root):
        self.name = "status"
        self.root = root
        self.root.minsize(width=root.winfo_width(), height=271)
        self.win = WindowABC()
        self.createWindow()
        
    def destroy(self):
        print "Destroy the grapher settings"
        self.mainFrame.pack_forget()
        self.mainFrame.grid_forget()
        self.mainFrame.destroy()

    def createWindow(self):
        '''Create initial window with one machine'''
        self.mainFrame = self.win.newFrame(self.root, 20, 20)
        self.canvas = self.win.newCanvas(self.mainFrame, width=200, height=200, yscroll=False)
        self.mainFrame.pack()
        self.x, self.y, self.z = 100, 100, 100
        self.drawCube()

    def drawCube(self):
        self.canvas.delete(ALL)
                
        point1 = (self.x, self.y)
        point2 = (self.x+50, self.y+10)
        point3 = (self.x+50, self.y+70)
        point4 = (self.x, self.y+60)
        point5 = (self.x+40, self.y-20)
        point6 = (self.x+90, self.y-10)
        point7 = (self.x+90, self.y+50)
        point8 = (self.x+40, self.y+40)

        self.canvas.create_line(point1+point2)
        self.canvas.create_line(point2+point3)
        self.canvas.create_line(point3+point4)        
        self.canvas.create_line(point4+point1)

        self.canvas.create_line(point5+point6)
        self.canvas.create_line(point6+point7)
        self.canvas.create_line(point7+point8)
        self.canvas.create_line(point8+point5)

        self.canvas.create_line(point1+point5)
        self.canvas.create_line(point2+point6)
        self.canvas.create_line(point3+point7)
        self.canvas.create_line(point4+point8)
        #self.canvas.create_line(50,50,100,25, fill="red", dash=(4,4))
        self.x += 5
        self.root.after(100, self.drawCube) #100ms

        
if __name__ == "__main__":
    root = Tk()
    win = StatusIndicator(root)
    root.mainloop()







        



