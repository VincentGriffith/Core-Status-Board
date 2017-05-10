from tkinter import *

#Config stuff
elementr = 15 #Fuel element display radius in pixels

#Resizing Canvas code from stack overflow
class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

#Create fullscreen, resizing window
root = Tk()
root.attributes("-fullscreen", True)
myframe = Frame(root)
myframe.pack(fill=BOTH, expand=YES)
mycanvas = ResizingCanvas(myframe,width=850, height=400, bg="#035096", highlightthickness=0)
mycanvas.pack(fill=BOTH, expand=YES)

scale = 20 #scaling down coordinates
elements = [] #should import from file eventually
selected1 = None
selected2 = None #Can select up to 2 positions at a time
selectmult = False #toggles selecting 1 or 2 positions
gridnameraw = [("B1",0,4.05384),("B2",3.51053,2.02692),("B3",3.51053,-2.02692),("B4",0,-4.05384),("B5",-3.51053,-2.02692),("B6",-3.51053,2.02692),("C1",0,7.98068),("C2",3.99034,6.91134),("C3",6.91134,3.99034),("C4",7.98068,0),("C5",6.91134,-3.99034),("C6",3.99034,-6.91134),("C7",0,-7.98068),("C8",-3.99034,-6.91134),("C9",-6.91134,-3.99034),("C10",-7.98068,0),("C11",-6.9113,3.9903),("C12",-3.9903,6.9113),("D1",0,11.9456),("D2",4.0853,11.2253),("D3",7.6787,9.1504),("D4",10.3449,5.9728),("D5",11.764,2.0737),("D6",11.764,-2.0737),("D7",10.3449,-5.9728),("D8",7.6787,-9.1504),("D9",4.0853,-11.2253),("D10",0,-11.9456),("D11",-4.0853,-11.2253),("D12",-7.6787,-9.1504),("D13",-10.3449,-5.9728),("D14",-11.764,-2.0737),("D15",-11.764,2.0737),("D16",-10.3449,5.9728),("D17",-7.6787,9.1504),("D18",-4.0853,11.2253),("E1",0,15.9156),("E2",4.1189,15.3728),("E3",7.9578,13.7828),("E4",11.254,11.254),("E5",13.8742,7.9578),("E6",15.3728,4.1189),("E7",15.9156,0),("E8",15.3728,-4.1189),("E9",13.8742,-7.9578),("E10",11.254,-11.254),("E11",7.9578,-13.7828),("E12",4.1189,-15.3728),("E13",0,-15.9156),("E14",-4.1189,-15.3728),("E15",-7.9578,-13.7828),("E16",-11.254,-11.254),("E17",-13.8742,-7.9578),("E18",-15.3728,-4.1189),("E19",-15.9156,0),("E20",-15.3728,4.1189),("E21",-13.8742,7.9578),("E22",-11.254,11.254),("E23",-7.9578,13.7828),("E24",-4.1189,15.3728),("F1",0,19.8882),("F2",4.134866,19.45259),("F3",8.08863,18.15786),("F4",11.69035,16.08963),("F5",14.77899,13.307314),("F6",17.223232,9.9441),("F7",18.915634,6.14553),("F8",19.777202,2.070608),("F9",19.777202,-2.070608),("F10",18.915634,-6.14553),("F11",17.223232,-9.9441),("F12",14.77899,-13.307314),("F13",11.69035,-16.08963),("F14",8.08863,-18.167858),("F15",4.134866,-19.45259),("F16",0,-19.8882),("F17",-4.134866,-19.45259),("F18",-8.08863,-18.167858),("F19",-11.69035,-16.08963),("F20",-14.77899,-13.307314),("F21",-17.223232,-9.9441),("F22",-18.915634,-6.14553),("F23",-19.777202,-2.070608),("F24",-19.777202,2.070608),("F25",-18.915634,6.14553),("F26",-17.223232,9.9441),("F27",-14.77899,13.307314),("F28",-11.69035,16.08963),("F29",-8.08863,18.167858),("F30",-4.134866,19.45259)] #Core grid positions in real coordinates

gridnamexy = [(raw[0],(raw[1]+50)*180,(raw[2]+22)*180) for raw in gridnameraw] #Translate into distance in pixels from upper left corner of screen

class Outside: #contains and draws elements not in other positions
    def __init__(self):
        self.outs = []
    def add(self,new):
        self.outs.append(new)
        self.draw()
    def draw(self):
        self.undraw()
        self.circles = []
        self.labels = []
        position = 20
        for element in self.outs:
            self.circles.append(mycanvas.create_circle(mycanvas,position,40,elementr,fill="#ff0000"))
            self.labels.append(mycanvas.create_text(position,40,text = str(element.serial)))
            position += 40
    def undraw(self):
        for element in self.outs:
            mycanvas.delete(element)


out = Outside()



#Circle code from stack overflow
def _create_circle(self,x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
mycanvas.create_circle = _create_circle

class Element:
    def __init__(self, model, SN):
        self.model = model
        self.serial = SN
        self.position = out
        out.add(self)
    def select(event):
        if selected1 == self:
            selected1 = None
            selected2 = None
        elif selected1 == None:
            selected1 = self
        elif selectmult and select2 == None:
            selected2 = self
        else:
            selected1 = None
            selected2 = None
    def insert(self, pos):
        self.position = pos
        pos.insert(self)
    def remove(self):
        pos.remove()
        self.insert(None)

class Position:
    def __init__(self,x,y,r,name):
        self.circle = mycanvas.create_circle(mycanvas,x,y,r,fill="#dcdccd")
        self.label = mycanvas.create_text(x,y-5,text=name)
        self.name = "name"
        self.contains = None
    def insert(self,element):
        self.contains = element
        mycanvas.itemconfig(self.label,text = name + "\n" + element.serial)
    def remove(self):
        self.insert(None)

def select(event):
    pass

class AddElement:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        Label(top, text="Serial Number").pack()
        self.sn = Entry(top)
        self.sn.pack(padx=5)

        Label(top,text = "Model").pack()
        self.md = Entry(top)
        self.md.pack(padx=5)

        okay = Button(top, text="Create", command=self.ok)
        cancel = Button(top, text="Cancel", command=self.cancel)
        okay.pack(pady=5,side=LEFT)
        cancel.pack(pady=5,side=LEFT)

    def ok(self):
        new = Element(self.md.get(),self.sn.get())
        elements.append(new)
        self.top.destroy()

    def cancel(self):
        self.top.destroy()

def add_element():
    add = AddElement(root)

def move_element():
    pass

def del_element():
    pass

def EmptyPoss(poss):
    return {x | x in poss and x.contains == None}

def makepositions(poslist,r):
    positions = []
    for namexy in poslist:
        positions.append(Position((namexy[1]/scale), (namexy[2]/scale), r, namexy[0]))
    return positions




#Menus
menubar = Menu(root)
elemenu = Menu(menubar,tearoff = 0)
elemenu.add_command(label = "Add", command = add_element)
elemenu.add_command(label = "Move", command = move_element)
elemenu.add_command(label = "Delete", command = del_element)
menubar.add_cascade(label = "Elements", menu = elemenu)

root.config(menu=menubar)

gridposs = makepositions(gridnamexy,elementr)


root.mainloop()
root.destroy()        