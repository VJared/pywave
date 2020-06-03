#Jared Veerhoff
#06/03/2020


import tkinter as tk
#import time
import math
import random
from PIL import ImageTk, Image

#TODO: add slider for values
MIN_WIDTH = 700
MIN_HEIGHT = 700

#Correlates with frequency of the wave function
WAVE_CONST = 7
#Wave amplitude
WIGGLE = 5

#Where the slices should start
S_OFFSET = -100
#How wide the sliced area be
S_WIDTH = 100
#How wide the slices are
S_GAP = 20
#How far the slices move
S_INTENSITY = 20
#TODO: use this to keep slices in a "grid"
S_RANDSTEP = 1

#Split the image in two, side by side
def split(im):
    tm = Image.new(im.mode, im.size)
    for i in range(im.size[0] // 2):
        #Move odd colums of pixels all to the right side
        box1 = (i*2, 0, i*2+1, im.size[1])
        #Even stays on the left
        box2 = (i*2+1, 0, i*2+2, im.size[1])
        
        region1 = im.crop(box1)
        region2 = im.crop(box2)

        tm.paste(region1, (i, 0, i+1, im.size[1]))
        tm.paste(region2, (im.size[0]//2+i, 0, im.size[0]//2+i + 1, im.size[1]) )
    return tm

#Opposite as above, this essentially performs a "faro shuffle" on the columns
def unsplit(im):
    tm = Image.new(im.mode, im.size)
    i = 0
    while (i < im.size[0]):
        dest1 = (i*2, 0, i*2+1, im.size[1])
        curr1 = (i, 0, i+1, im.size[1])
        dest2 = (i*2 + 1, 0, i*2+2, im.size[1])
        curr2 = (im.size[0] // 2 + i, 0, im.size[0] // 2 + i + 1, im.size[1])

        region1 = im.crop(curr1)
        region2 = im.crop(curr2)

        tm.paste(region1, dest1)
        tm.paste(region2, dest2)
        i = i+1
    return tm

#Rotate, split, then fix
def splot(im):
    im = im.transpose(Image.ROTATE_90)
    tm = split(im)
    tm = tm.transpose(Image.ROTATE_270)
    return tm

def unsplot(im):
    im = im.transpose(Image.ROTATE_90)
    tm = unsplit(im)
    tm = tm.transpose(Image.ROTATE_270)
    return tm

#Applies a sin wave effect to the image
def wave(im):
    tm = Image.new(im.mode, im.size)
    for i in range(im.size[0]):
        
        offset = im.size[1] * math.sin(i*(WAVE_CONST/1000)) * (WIGGLE/100)
        #print(offset)
        offset = int(offset)
        if offset < 0:
            offset = im.size[1] + offset
            
        bottom = (i, offset, i+1, im.size[1])
        top = (i, 0, i+1, offset)
        
        region1 = im.crop(top)
        region2 = im.crop(bottom)

        #print((i, im.size[1] - offset , i+1, im.size[1]))
        tm.paste(region1, (i, im.size[1] - offset , i+1, im.size[1]))
        tm.paste(region2, (i, 0, i + 1, im.size[1] - offset) )
    return tm

#Cuts a section of the image into slices, offsets each slice by a random amount
def stagger(im):
    tm = im
    mid = im.size[0]//2 + S_OFFSET
    for i in range(mid - S_WIDTH // 2, mid + S_WIDTH // 2, S_GAP):
        offset = random.randrange(-S_INTENSITY, S_INTENSITY, S_RANDSTEP)
        if offset < 0:
            offset = im.size[1] + offset
        
        bottom = (i, offset, i+S_GAP, im.size[1])
        top = (i, 0, i+S_GAP, offset)
        
        region1 = im.crop(top)
        region2 = im.crop(bottom)

        #print((i, im.size[1] - offset , i+1, im.size[1]))
        tm.paste(region1, (i, im.size[1] - offset , i+S_GAP, im.size[1]))
        tm.paste(region2, (i, 0, i + S_GAP, im.size[1] - offset) )
    return tm

#Same as above, cuts horizontal slices however
def stogger(im):
    tm = im
    mid = im.size[1]//2 + S_OFFSET
    for i in range(mid - S_WIDTH // 2, mid + S_WIDTH // 2, S_GAP):
        offset = random.randrange(-S_INTENSITY, S_INTENSITY, S_RANDSTEP)
        if offset < 0:
           offset = im.size[0] + offset
            
        bottom = (offset, i, im.size[0], i+S_GAP)
        top = (0, i, offset, i+S_GAP)
        
        region1 = im.crop(top)
        region2 = im.crop(bottom)

        #print((i, im.size[1] - offset , i+1, im.size[1]))
        tm.paste(region1, (im.size[0] - offset, i, im.size[0], i+S_GAP))
        tm.paste(region2, (0, i, im.size[0] - offset, i + S_GAP) )
    return tm

def colorTest(im):
    # split the image into individual bands
    source = im.split()

    R, G, B = 0, 1, 2

    # select two regions depending on presence of green (basically darkness)
    maskG = source[G].point(lambda i: i <= 125 and 255)
    maskG2 = source[G].point(lambda i: i > 125 and 255)

    # reduce green and red bands
    outG = source[G].point(lambda i: i * .5) #magenta
    outR = source[R].point(lambda i: i * .5) #cyan
    
    # paste the processed bands back, magenta in light, cyan in dark
    source[G].paste(outG, None, maskG2)
    source[R].paste(outR, None, maskG)

    # build a new multiband image
    im = Image.merge(im.mode, source)
    
    return im

def randomize(im):
    #Select a random number of effects
    numSteps = random.randrange(5, 12)
    steps = []
    tm = im

    #apply random settings for wave and stagger
    WIGGLE = random.randrange(1, 30)
    WAVE_CONST = random.randrange(1, 400)

    S_GAP = random.randrange(1, 40)
    S_INTENSITY = random.randrange(1, 100)
    S_OFFSET = random.randrange(-100, 100)
    S_RANDSTEP = random.choice([1, S_GAP])
    S_WIDTH = random.randrange(0, 100)

    for i in range(numSteps):
        steps.append(random.randrange(0, 8))
    switcher = {
        0: split,
        1: splot,
        2: unsplit,
        3: unsplot,
        4: wave,
        5: stagger,
        6: stogger,
        7: colorTest
    }
    #Run through the random list, apply respective effects for each value
    for step in steps:
        func = switcher.get(step, lambda: "Error")
        tm = func(tm)
    return tm

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.img = Image.open("maxresdefault.jpg")
        if(self.img.size > (MIN_WIDTH, MIN_HEIGHT)):
            self.resize()            
        self.pimg = ImageTk.PhotoImage(self.img)
        self.last = self.img
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)                      
        self.undoB = tk.Button(self, text = "UNDO", fg = "yellow",
                              command=self.undo)
        self.undoB.pack(side="bottom")
        self.quit.pack(side="bottom")

        self.splitB = tk.Button(self, text="SPLIT", command=self.split)
        self.unsplitB = tk.Button(self, text="MERGE", command=self.unsplit)
        self.splotB = tk.Button(self, text="SPLOT", command=self.splot)
        self.unsplotB = tk.Button(self, text="MORGE", command=self.unsplot)
        
        self.waveB = tk.Button(self, text="WAVY", command=self.wave)
        self.stagB = tk.Button(self, text="STAG", command=self.stag)
        self.stogB = tk.Button(self, text="STOG", command=self.stog)
        self.colorB = tk.Button(self, text="COLOR", command=self.color)
        self.randB = tk.Button(self, text="RAND", command=self.rand)
        
        #TODO: switch to grid instead of pack 
        self.splitB.pack(side="left")
        self.unsplitB.pack(side="left")
        self.splotB.pack(side="left")
        self.unsplotB.pack(side="left")

        self.waveB.pack(side="left")
        self.stagB.pack(side="left")
        self.stogB.pack(side="left")
        self.colorB.pack(side="left")
        self.randB.pack(side="left")

        self.panel = tk.Label(self, image = self.pimg)
        self.panel.pack(side="top")
        
    def split(self):
        self.last = self.img
        self.img = split(self.img)
        self.updateImage()
    def unsplit(self):
        self.last = self.img
        self.img = unsplit(self.img)
        self.updateImage()
    def splot(self):
        self.last = self.img
        self.img = splot(self.img)
        self.updateImage()
    def unsplot(self):
        self.last = self.img
        self.img = unsplot(self.img)
        self.updateImage()

    def wave(self):
        self.last = self.img
        self.img = wave(self.img)
        self.updateImage()
    def stag(self):
        self.last = self.img
        self.img = stagger(self.img)
        self.updateImage()
    def stog(self):
        self.last = self.img
        self.img = stogger(self.img)
        self.updateImage()
    def color(self):
        self.last = self.img
        self.img = colorTest(self.img)
        self.updateImage()
    def rand(self):
        self.last = self.img
        self.img = randomize(self.img)
        self.updateImage()
    
    def updateImage(self):
        self.pimg = ImageTk.PhotoImage(self.img)
        self.panel.configure(image = self.pimg)
    
    def undo(self):
        self.img = self.last
        self.updateImage()

    #resize image to fit inside bounds, maintains aspect ratio
    def resize(self):
        over = (self.img.size[0] / MIN_WIDTH, self.img.size[1] / MIN_HEIGHT)
        if over[0] > over[1]:
            ratio = MIN_WIDTH / self.img.size[0]
            self.img = self.img.resize(tuple(int(ratio*x) for x in self.img.size))
            #print(self.img.size)
        else:
            ratio = MIN_HEIGHT / self.img.size[1]
            self.img = self.img.resize(tuple(int(ratio*x) for x in self.img.size))
            #print(self.img.size)
        
print("Using Pillow", Image.__version__)
root = tk.Tk()
app = Application(master=root)
app.mainloop()

#TODO: add commandline arguments