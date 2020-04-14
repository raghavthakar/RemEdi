from PIL import Image, ImageTk
import numpy as np
import json
import time
import math
from datetime import datetime
import os

def compress(DIAGRAM_FILE_DIR, TOPIC, NOW):
    resized_height=450

    SAVE_PATH='../saved_data/saved_image_to_text_data/'

    DIAGRAM_FILENAME=os.path.basename(DIAGRAM_FILE_DIR)

    DATE_TIME = NOW.strftime("%d-%m-%Y-%H-%M-%S")
    print("Converted and saved: ", SAVE_PATH+DIAGRAM_FILE_DIR+TOPIC+DATE_TIME)

    #load image
    #sample_image=Image.open('../modules/imaging/himesh.jpg')
    sample_image=Image.open(DIAGRAM_FILE_DIR)
    working_image=sample_image

    #compress image
    width, height = working_image.size
    resize_factor=resized_height/height
    width=round(resize_factor*width)
    height=round(resize_factor*height)
    working_image=working_image.resize((width, height), Image.ANTIALIAS)

    #write the image specs into a dict
    image_specs={'width':width, 'height':height}
    #write image specs into JSON FILE
    with open(SAVE_PATH+TOPIC+DATE_TIME+'_specs.json', 'w') as json_write:
        json.dump(image_specs, json_write)

    #convert image into 3D array (2D matrix for pixel ID, 3rd dimension for vals of RGB)
    image_array=np.array(working_image)

    #reducing all colors to out of 25
    i=0
    j=0
    k=0
    while i<height:
        j=0
        while j<width:
            k=0
            while k<3:
                image_array[i, j, k]=round(image_array[i, j, k]/10)
                k+=1
            j+=1
        i+=1

    #flatten image_array and save a copy (convert 3d array into 1 long 1d array)
    image_array_flat=np.ndarray.flatten(image_array)

    #initialise a character list
    char_list=[]
    #convert flat image array into char char_array
    image_array_flat.tolist()
    for i in image_array_flat:
        if i+65>90:
            char_list.append(chr(90))
        else:
            char_list.append(chr(i+65))

    #save the char array into a .txt file
    TextFile=open(SAVE_PATH+TOPIC+DATE_TIME+'_to_text.txt','w')
    for element in char_list:
          TextFile.write(element)
    TextFile.close()
