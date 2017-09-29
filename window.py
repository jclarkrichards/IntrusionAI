from Tkinter import *
from constants import *
import ttk
import tkFont

class WindowABC(object):
    def newFrame(self, root, padx=0, pady=0, row=0, col=0, rowspan=1, colspan=1, sticky=N+S+W+E, bwidth=0, r=FLAT, fg=None, bg=None, setWeights=True):
        frame = Frame(root, padx=padx, pady=pady, highlightcolor="red", borderwidth=bwidth, relief=r, fg=fg, bg=bg)
        #if setWeights:
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky, padx=10, pady=10)
        
        #self.addScrollbars(root, frame, yscroll, False, row=row, col=col, rowspan=rowspan, colspan=colspan)
        return frame

    def newLabel(self, root, text="", row=0, col=0, rowspan=1, colspan=1, justify=CENTER, 
                 sticky=N+S+W+E, width=0, fg=None, bg=None, image=None, font=None, wraplength=0):
        label = Label(root, text=text, width=width, fg=fg, bg=bg, image=image, font=font, wraplength=wraplength,
                      justify=justify)
        #label.grid_rowconfigure(0, weight=1)
        #label.grid_columnconfigure(0, weight=1)
        label.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky, padx=5, pady=5)
        if image is not None:
            label.image = image
        return label

    def newListbox(self, root, mode=BROWSE, width=20, height=20, yscroll=False, xscroll=False,
                   row=0, col=0, rowspan=1, colspan=1, sticky=N+S+W+E):
        lb = Listbox(root, selectmode=mode, height=height, width=width)
        self.addScrollbars(root, lb, yscroll, xscroll, row=row, col=col, rowspan=rowspan,
                           colspan=colspan)
        lb.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky)
        return lb

    def newCanvas(self, root, width=0, height=0, xscroll=False, yscroll=True,
                   row=0, col=0, rowspan=1, colspan=1, sticky=N+S+W+E):
        canvas = Canvas(root, width=width, height=height)
        self.addScrollbars(root, canvas, yscroll, xscroll, row=row, col=col, rowspan=rowspan, 
                           colspan=colspan)
        canvas.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky)
        return canvas

    def addScrollbars(self, root, widget, yscroll, xscroll, row=0, col=0, rowspan=1, colspan=1):
        if yscroll:
            yscrollbar = Scrollbar(root)
            yscrollbar.grid(row=row, column=colspan+col, rowspan=rowspan, sticky=N+S)
            widget.config(yscrollcommand=yscrollbar.set)
            yscrollbar.config(command=widget.yview)
        if xscroll:
            xscrollbar = Scrollbar(root, orient=HORIZONTAL)
            #print row, col, rowspan, colspan
            xscrollbar.grid(row=rowspan+row, column=col, columnspan=colspan, sticky=W+E)
            widget.config(xscrollcommand=xscrollbar.set)
            xscrollbar.config(command=widget.xview)
        
    def newButton(self, root, text="", row=0, col=0, rowspan=1, colspan=1, sticky=N+S+W+E, width=0,
                  height=0, fg=None, bg=None, image=None):
        if fg is not None and bg is not None:
            button = Button(root, text=text, width=width, height=height, fg=fg, bg=bg, 
                            activebackground=fg, activeforeground=bg, image=image)
        else:
            button = Button(root, text=text, width=width, image=image)
        
        if image is not None:
            button.image = image
            
        #button.grid_rowconfigure(0, weight=1)
        #button.grid_columnconfigure(0, weight=1)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky, padx=5, pady=5)
        return button

    def newEntry(self, root, show="", enabled=True, width=20, row=0, col=0, 
                 rowspan=1, colspan=1, sticky=N+S+W+E, fg=None, bg=None, required=False):
        if required:
            entry = Entry(root, show=show, width=width, highlightcolor="#556058", highlightthickness=3, fg=fg, bg=RC)
        else:
            entry = Entry(root, show=show, width=width, highlightcolor="#556058", highlightthickness=3, fg=fg, bg=bg)
        if not enabled:
            entry.configure(state='disabled')
        entry.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky, padx=2, pady=2)
        return entry

    def newDropMenu(self, root, var, options, width=20, row=0, col=0, rowspan=1, colspan=1, sticky=N+S+W+E):
        var.set(options[-1])
        drop = OptionMenu(root, var, *options)
        drop.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky)
        return drop

    def newCheck(self, root, var, text="", row=0, col=0, rowspan=1, colspan=1, sticky=N+S+W+E,
                 fg=None, bg=None):
        check = Checkbutton(root, text=text, variable=var, fg=fg, bg=bg)
        check.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky)
        return check

    def newRadioButton(self, root, var, choices=[], row=0, col=0, rowspan=1, colspan=1, sticky=N+S+W+E, 
                       fg=None, bg=None):
        radios = []
        for i, choice in enumerate(choices):
            radio = Radiobutton(root, text=choice[0], variable=var, value=choice[1], indicatoron=1, fg=fg, bg=bg)
            radio.grid(row=row+i, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky)
            radios.append(radio)
        return radios
            
    def newMultiColumnListBox(self, root, colList, row=0, col=0, height=10, rowspan=1, colspan=1, sticky=N+W+S+E):
        #print type(root)
        tree = ttk.Treeview(columns=colList, height=height, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky, in_=root)
        vsb.grid(row=row, column=col+colspan, rowspan=rowspan, columnspan=colspan, sticky=N+S, in_=root)
        hsb.grid(row=row+rowspan, column=col, rowspan=rowspan, columnspan=colspan, sticky=E+W, in_=root)
        for col in colList:
            tree.heading(col, text=col.title(), command=lambda c=col: self.sortby(tree, c, 0))
            tree.column(col, width=tkFont.Font().measure(col.title()))
        return tree
    
    def sortby(self, tree, col, descending):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, int(not descending)))
    
        
class VerticalScrollFrame(Frame):
    def __init__(self, root, *args, **kw):
        Frame.__init__(self, root, *args, **kw)
        win = WindowABC()
        self.vscrollbar = Scrollbar(root, orient=VERTICAL)
        self.vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(root, yscrollcommand=self.vscrollbar.set)
        #canvas = self.newCanvas(root, width=200, height=200, yscroll=True)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.vscrollbar.config(command=self.canvas.yview)
        #canvas.config(scrollregion=canvas.bbox(ALL))
        #interior = self.newFrame(canvas)
        self.interior = interior = win.newFrame(self.canvas, 30, 30, sticky=N+S)
        #self.interior = interior = Frame(self.canvas)
        interior_id = self.canvas.create_window(0,0,window=self.interior, anchor=NW)
        def _configure_interior(event):
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            #print size
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.config(width=self.interior.winfo_reqwidth())
        self.interior.bind('<Configure>', _configure_interior)
        
        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind('<Configure>', _configure_canvas)
        
        #return interior
    def destroy(self):
        self.vscrollbar.destroy()
        self.canvas.destroy()
        self.interior.destroy()
        








    
def organizeByRows(widgets=[]):
    row = 0
    if len(widgets) > 0:
        for i in range(len(widgets)):
            widgets.config(row=row)
            row += 1
