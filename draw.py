from tkinter import *
from tkinter import ttk, colorchooser, filedialog,messagebox
import PIL
from PIL import ImageTk, Image, ImageDraw
from PIL import ImageGrab
import os
import cv2


from tensorflow import keras
import h5py
import numpy as np

model = keras.models.load_model("model.h5")

width = 30
image = PIL.Image.new("RGB", (400, 400), (0, 0, 0))
draw = ImageDraw.Draw(image)

def paint(event) :
    color = 'white'
    x1,y1,x2,y2  = event.x-1 , event.y-1 , event.x+1 , event.y+1
    c.create_oval(x1 ,y1,x2,y2 ,width= width ,fill =  color ,outline = color)
    draw.line([x1, y1, x2, y2],fill="white",width= 20)

def clean():
    c.delete(ALL)
    image1 = PIL.Image.new("RGB", (400, 400), (0, 0, 0)) 
    image.paste(image1)

def saveImage():
    try:
        os.mkdir('YourDrawings')
    except:
        pass
    filename = "YourDrawings/recent_drawing.png"
    image.save(filename)
    imgtobesaved = image.resize((28,28))
    imgtobesaved.save("YourDrawings/recent_drawing_resized.png")

def changewidth(w):
    global width
    width = w

def guess():
    saveImage()
    img = cv2.imread("YourDrawings/recent_drawing_resized.png" , 0)
    if(np.sum(img)==0):
        messagebox.showinfo('Answer' , 'Please Draw a Number')
    else :
        img = img/255
        for row in range(28):
            for col in range(28):
                if img[row][col] != 0:
                    img[row][col] = 1
        pred = model.predict(img.reshape(-1,784))
        print(pred)
        print(np.argmax(pred))
        if(pred[np.argmax(pred)] > 0.001):
            messagebox.showinfo('Answer' , 'I think the Number is ' + str(np.argmax(pred)))
        else:
            messagebox.showinfo('Answer' , ' Unable to read Image try Again !' )
        clean()


root = Tk()
root.title('D I G I T   R E C O G N I Z E R')
root.geometry('400x470')

c = Canvas(root ,width = 400 , height = 400 , bg= 'black')
c.pack(side = TOP )
c.bind('<B1-Motion>' , paint)

btn_reset = Button(root, text="    C L E A R",bg = '#07B1CD' , font="Times 10 bold",command = clean)
btn_reset.place(x=200, y=420, height=30, width=80)
btn_guess = Button(root, text="G U E S S", bg = '#950aff' , fg ='white' , font="Times 10 bold",command = guess)
btn_guess.place(x=300, y=420, height=30, width=80)

controls = Frame(root,padx = 5,pady = 5)
Label(controls, text='Size : ',font="Times 15 bold").grid(row=0,column=0)
slider = ttk.Scale(controls,from_= 5, to = 50, command=changewidth,orient=HORIZONTAL)
slider.set(width)
slider.grid(row=0,column=1,ipadx=20)
controls.place(x=2, y=420,)

root.mainloop()
