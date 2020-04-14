#!/usr/bin/env python3
import json
import numpy as np
from PIL import Image, ImageOps
import tkinter as tk
import tkinter.font as tkfont
from tkinter import PhotoImage
from tkinter import filedialog
from PIL import Image, ImageTk
import PIL
import os

HEIGHT=1080
WIDTH=1920
TOPLOGO_RELY=0

text_filename=""
text_file_dir=""
json_filename=""

def regenerate_image():
    global text_filename
    global text_file_dir
    global json_filename

    text_file_dir=text_filename
    text_filename=text_filename.replace("_to_text.txt", "")
    json_filename=text_filename
    json_filename=json_filename+"_specs.json"
    #load image specifications into a dict from json
    with open(json_filename) as json_read:
        image_specs = json.load(json_read)

    #store image specs in local variables
    width = image_specs["width"]
    height = image_specs["height"]

    #read contents of file and store in list
    TextFile=open(text_file_dir, "r")
    char_list=TextFile.read()

    #initialise flat image array list
    image_array_flat=[]

    #convert char list to flat image array
    for element in char_list:
        if ord(element)-65>25:
            image_array_flat.append(25)
        else:
            image_array_flat.append(ord(element)-65)

    #initiliase empty image array list
    image_array=np.zeros((width, height, 3), dtype=np.uint8)

    #convert flat image array into 3d array out of 25
    i=0
    x=0
    y=0
    while y<height:
        x=0
        while x<width:
            image_array[x][y]=[image_array_flat[i], image_array_flat[i+1], image_array_flat[i+2]]
            x+=1
            i+=3
        y+=1

    #regenerate image array (of 255) from array out of 25
    i=0
    j=0
    k=0
    while j<height:
        i=0
        while i<width:
            k=0
            while k<3:
                image_array[i, j, k]=round(image_array[i, j, k]*10)
                if image_array[i, j, k]>255:
                    image_array[i, j, k]=255
                k+=1
            i+=1
        j+=1

    #store image from array that has been reduced to 25 and then brought to out of 255 again
    result_image=Image.fromarray(image_array)
    #rotate image by 270 anticlockwise
    result_image = result_image.rotate(270, PIL.Image.NEAREST, expand = 1)
    #mirror the image
    result_image = ImageOps.mirror(result_image)
    result_image.show()
    text_filename=text_filename+".jpg"
    print(text_filename)
    text_filename=os.path.basename(text_filename)
    print(text_filename)
    result_image.save('../saved_data/regenerated_diagrams/'+text_filename)
    text_file_dir=""
    text_filename=""
    json_filename=""



#initialising root
root=tk.Tk()

#giving appa title
root.title('RemEdi')
root.iconphoto(False, tk.PhotoImage(file='../design/assets/logo_stack_icon.png'))

canvas=tk.Canvas(root, height=HEIGHT, width=WIDTH) #placeholder
canvas.pack()

#general Frame
frame=tk.Frame(root, bg="white")
frame.place(relwidth=1, relheight=1, relx=0.5, rely=0.5, anchor="center")

#frame for top logo
top_logo_frame=tk.Frame(frame, bg="white")
top_logo_frame.place(relx=0, rely=TOPLOGO_RELY, relheight=0.155, relwidth=1, anchor="nw")

#label for top logo
top_logo_image=ImageTk.PhotoImage(Image.open('../design/assets/logo_small.png'))
top_logo_label=tk.Label(top_logo_frame, image=top_logo_image, bg="white")
top_logo_label.place(relx=0.145, rely=0.5, anchor='center')

#frame ofr send diagram page
regenerate_diagram_frame=tk.Frame(root, bg="#D4BAEC")
regenerate_diagram_frame.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.7, anchor="center")

def choose_file():
    global text_filename
    root.filename=filedialog.askopenfilename(initialdir="/home", title="Text to Diagram",
    filetypes=(("text files", "*.txt"), ("All Files", "*.*")))
    text_filename=root.filename
    print("Selected diagram", text_filename)
    regenerate_diagram_entry_text_label=tk.Label(regenerate_diagram_frame, bg="white", text=text_filename, font="Arial 16", foreground="#7F7F7F", justify="left")
    regenerate_diagram_entry_text_label.place(relx=0.425, rely=0.4875, relwidth=0.525, relheight=0.065, anchor="center")

#sned diagram page title
regenerate_diagram_title_image=ImageTk.PhotoImage(Image.open("../design/assets/regenerate_diagram.png"))
regenerate_diagram_title_label=tk.Label(regenerate_diagram_frame, image=regenerate_diagram_title_image, bg="#D4BAEC")
regenerate_diagram_title_label.image = regenerate_diagram_title_image
regenerate_diagram_title_label.place(relx=0, rely=0.2, anchor="w")

#send diagram page entry
text_filename=""
regenerate_diagram_entry_working_image=Image.open('../design/assets/generic_page_entry.png')
regenerate_diagram_entry_working_image=regenerate_diagram_entry_working_image.resize((704, 74), Image.ANTIALIAS)
regenerate_diagram_entry_image=ImageTk.PhotoImage(regenerate_diagram_entry_working_image)
regenerate_diagram_entry_label=tk.Label(regenerate_diagram_frame, image=regenerate_diagram_entry_image, bg="#D4BAEC")
regenerate_diagram_entry_label.image = regenerate_diagram_entry_image
regenerate_diagram_entry_label.place(relx=0.425, rely=0.5, anchor="center")

#send diagram choose file
regenerate_diagram_choose_file_working_image=Image.open("../design/assets/generic_choose_file_button.png")
regenerate_diagram_choose_file_working_image=regenerate_diagram_choose_file_working_image.resize((184, 74), Image.ANTIALIAS)
regenerate_diagram_choose_file_image=ImageTk.PhotoImage(regenerate_diagram_choose_file_working_image)
regenerate_diagram_choose_file_button=tk.Button(regenerate_diagram_frame, image=regenerate_diagram_choose_file_image, bg="#D4BAEC",
borderwidth=0, activebackground="#D4BAEC", command=choose_file)
regenerate_diagram_choose_file_button.image=regenerate_diagram_choose_file_image
regenerate_diagram_choose_file_button.place(relx=0.775, rely=0.5, anchor="center")

#send diagram page send diagram button
regenerate_diagram_regenerate_diagram_working_image=Image.open('../design/assets/regenerate_button.png')
regenerate_diagram_regenerate_diagram_working_image=regenerate_diagram_regenerate_diagram_working_image.resize((263, 112), Image.ANTIALIAS)
regenerate_diagram_regenerate_diagram_image=ImageTk.PhotoImage(regenerate_diagram_regenerate_diagram_working_image)
regenerate_diagram_regenerate_diagram_button=tk.Button(regenerate_diagram_frame, image=regenerate_diagram_regenerate_diagram_image, bg="#D4BAEC",
borderwidth=0, activebackground="#D4BAEC", command=regenerate_image)
regenerate_diagram_regenerate_diagram_button.image=regenerate_diagram_regenerate_diagram_image
regenerate_diagram_regenerate_diagram_button.place(relx=0.8, rely=0.8, anchor='center')

root.mainloop()
