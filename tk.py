from tkinter import *
from PIL import ImageTk
def say_hi():
    print("hello ~ !")
 
root = Tk()
root.geometry('400x300')
 
root.title("tkinter frame")
 
cv = Canvas(root,bg = 'white')
# 创建一个矩形，坐标为(10,10,110,110)
# cv.create_rectangle(10,10,110,110)

filename = ImageTk.PhotoImage(file = "./image/apple.jpg")
image = cv.create_image(100,2, anchor=NE, image=filename)
cv.pack()
root.mainloop()