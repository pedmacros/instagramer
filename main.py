import tkinter as tk
import numpy as np
from skimage import io,img_as_ubyte
from tkinter import filedialog, Text
from PIL import Image, ImageTk
import os

root = tk.Tk()

def AddFile():
    global filename #it is set as global because it is needed in other functions
    filename = filedialog.askopenfilename(initialdir="/", title = "Select File",
                                            filetypes = (("images","*.jpg"),("all files","*.*"))) #gets file directory and name
    showInput(filename) 

def showInput(filename): #shows the image selected
    load = Image.open(filename) #opens the image
    load.thumbnail((frame_l.winfo_width(),frame_l.winfo_height())) #rescales the image to fit in the screen
    
    render = ImageTk.PhotoImage(load) #creaters the PhotoImage object
    img = tk.Label(frame_l,image = render, bg = "#222222") #sets it in the left frame with gray background
    
    img.image = render
    img.place(relheight = 1, relwidth = 1)

def transformTop():
    inp = io.imread(filename) #loads image file

    rows,columns,x = inp.shape #get dimensions of the image

    if columns > rows: #it checks if the image is long or wide
        new_rows = columns
        new_columns = columns
    else:
        new_columns = rows
        new_rows = rows
        
    global out #this variable is also needed in the save function
    
    out = np.ones((new_rows,new_columns,x)) #we create a new black square image to fit the original one inside it
    
    out[:,:,:] = (255,255,255) #the new image is painted white

    for i in range(0,rows): #the original image is placed on the top region of the white one
        for j in range(columns):
            out[i,j,:] = inp[i,j,:]

    out = out/256 #the final image is rescaled to fit the save function
    out = img_as_ubyte(out) #the data type is changed to fit the save function
    
    io.imsave("preview.jpg",out) #a preview is saved
    preview() #the preview is shown

    os.remove("preview.jpg") #the preview file is deleted


def transformMid():
    inp = io.imread(filename)

    rows,columns,x = inp.shape

    if columns > rows:
        new_rows = columns
        new_columns = columns
    else:
        new_columns = rows
        new_rows = rows
        
    global out
    
    out = np.ones((new_rows,new_columns,x))
    
    out[:,:,:] = (255,255,255)

    for i in range((new_rows//2-rows//2),(new_rows//2)+(rows//2)): #the original image is placed on the middle region of the white one
        for j in range(columns):
            out[i,j,:] = inp[i-(new_rows//2-rows//2),j,:]

    out = out/256
    out = img_as_ubyte(out)
    
    io.imsave("preview.jpg",out)
    preview()

    os.remove("preview.jpg")

def transformBot():
    inp = io.imread(filename)

    rows,columns,x = inp.shape

    if columns > rows:
        new_rows = columns
        new_columns = columns
    else:
        new_columns = rows
        new_rows = rows
        
    global out
    
    out = np.ones((new_rows,new_columns,x))
    
    out[:,:,:] = (255,255,255)

    for i in range(new_rows-rows,new_rows): #the original image is placed on the bottom region of the white one
        for j in range(columns):
            out[i,j,:] = inp[i-(new_rows-rows),j,:]

    out = out/256
    out = img_as_ubyte(out)
    
    io.imsave("preview.jpg",out)
    preview()

    os.remove("preview.jpg")

def preview():
    load = Image.open("preview.jpg")
    load.thumbnail((frame_r.winfo_width(),frame_r.winfo_height()))
    
    render = ImageTk.PhotoImage(load)
    img = tk.Label(frame_r,image = render, bg = "#222222")

    img.image = render
    img.place(relheight = 1, relwidth = 1)



def saveImg():
    f_name = filedialog.asksaveasfilename(initialdir="/", title = "Save File",filetypes = (("images","*.jpg"),("all files","*.*")))
    io.imsave(f_name,out)



canvas = tk.Canvas(root,height=500, width=800) #sets the default size of the window
canvas.pack()

#now the window is split in the areas, one on top and the other two side by side
frame_t = tk.Frame(root,bg = "#222222")
frame_t.place(relwidth=1,relheight=0.1,relx = 0, rely = 0)

frame_l = tk.Frame(root,bg = "#222222")
frame_l.place(relwidth=0.5,relheight=0.9,relx = 0, rely = 0.1)

frame_r = tk.Frame(root,bg = "#222222")
frame_r.place(relwidth=0.5,relheight=0.9,relx = 0.5, rely = 0.1)

#now the buttons are placed and their functions are assigned
openFile = tk.Button(frame_t, text = "Open File", padx = 10, pady = 5, 
                            fg = "white", bg = "#2E3973",command = AddFile)
openFile.pack(side = "left")

transformTop = tk.Button(frame_t, text = "Transform Top", padx = 10, pady = 5, fg = "white", bg = "#2E3973",
                         command = transformTop)
transformTop.pack(side = "left")

transformMid = tk.Button(frame_t, text = "Transform Mid", padx = 10, pady = 5, fg = "white", bg = "#2E3973",
                         command = transformMid)
transformMid.pack(side = "left")

transformBot = tk.Button(frame_t, text = "Transform Bot", padx = 10, pady = 5, fg = "white", bg = "#2E3973",
                         command = transformBot)
transformBot.pack(side = "left")

saveImg = tk.Button(frame_t, text = "Save Image", padx = 10, pady = 5, fg = "white", bg = "#2E3973",
                    command = saveImg)
saveImg.pack(side = "left")


root.mainloop() #the main loop begins
