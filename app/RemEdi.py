#!/usr/bin/env python3
import tkinter as tk
import tkinter.font as tkfont
from tkinter import PhotoImage
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import json
import time
import math
from datetime import datetime
import os

import sys
sys.path.insert(0, '../modules/imaging')
import compressor

sys.path.insert(1, '../modules/sms_to_students')
import twilio_transcript
import twilio_invitation

HEIGHT=1080
WIDTH=1920

OPTIONS_RELY=0.15
TOPIC_RELY=0.44
TOPLOGO_RELY=0
BEGINCLASS_RELY=0.75

#ALL GLOBAL VARABLES
students_register={}
topic_name=""
diagram_filename=""
recording_enabled=False

with open('../saved_data/students_register/students_register.json') as json_stud_dict:
     students_register=json.load(json_stud_dict)

students_list=list(students_register)

now = datetime.now()

#initialising root
root=tk.Tk()

#giving appa title
root.title('RemEdi')
root.iconphoto(False, tk.PhotoImage(file='../design/assets/logo_stack_icon.png'))

canvas=tk.Canvas(root, height=HEIGHT, width=WIDTH) #placeholder
canvas.pack()

#---------------------------------------------------------------ENTER SEND DIAGRAM PAGE---------------------------------------------------------------
def send_diagram():

    def choose_file():
        global diagram_filename
        root.filename=filedialog.askopenfilename(initialdir="/home", title="Select Diagram",
        filetypes=(("png files", "*.png"),("jpg files", "*.jpg"), ("All Files", "*.*")))
        diagram_filename=root.filename
        print("Selected diagram", diagram_filename)
        send_diagram_entry_text_label=tk.Label(send_diagram_frame, bg="white", text=diagram_filename, font="Arial 16", foreground="#7F7F7F", justify="left")
        send_diagram_entry_text_label.place(relx=0.425, rely=0.4875, relwidth=0.525, relheight=0.065, anchor="center")

    def send_diagram_execute():
        global now
        global diagram_filename
        now = datetime.now()
        if diagram_filename is "":
            print("Select valid type")
        else:
            compressor.compress(diagram_filename, topic_name, now)
        diagram_filename=""

    def go_back():
        send_diagram_frame.place_forget()

    #frame ofr send diagram page
    send_diagram_frame=tk.Frame(frame, bg="#D4BAEC")
    send_diagram_frame.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.7, anchor="center")

    #sned diagram page title
    send_diagram_title_image=ImageTk.PhotoImage(Image.open("../design/assets/send_diagram_page_text.png"))
    send_diagram_title_label=tk.Label(send_diagram_frame, image=send_diagram_title_image, bg="#D4BAEC")
    send_diagram_title_label.image = send_diagram_title_image
    send_diagram_title_label.place(relx=0, rely=0.2, anchor="w")

    #send diagram page entry
    diagram_filename=""
    send_diagram_entry_working_image=Image.open('../design/assets/generic_page_entry.png')
    send_diagram_entry_working_image=send_diagram_entry_working_image.resize((704, 74), Image.ANTIALIAS)
    send_diagram_entry_image=ImageTk.PhotoImage(send_diagram_entry_working_image)
    send_diagram_entry_label=tk.Label(send_diagram_frame, image=send_diagram_entry_image, bg="#D4BAEC")
    send_diagram_entry_label.image = send_diagram_entry_image
    send_diagram_entry_label.place(relx=0.425, rely=0.5, anchor="center")

    #send diagram choose file
    send_diagram_choose_file_working_image=Image.open("../design/assets/generic_choose_file_button.png")
    send_diagram_choose_file_working_image=send_diagram_choose_file_working_image.resize((184, 74), Image.ANTIALIAS)
    send_diagram_choose_file_image=ImageTk.PhotoImage(send_diagram_choose_file_working_image)
    send_diagram_choose_file_button=tk.Button(send_diagram_frame, image=send_diagram_choose_file_image, bg="#D4BAEC",
    borderwidth=0, activebackground="#D4BAEC", command=choose_file)
    send_diagram_choose_file_button.image=send_diagram_choose_file_image
    send_diagram_choose_file_button.place(relx=0.775, rely=0.5, anchor="center")

    #send diagram page send diagram button
    send_diagram_send_diagram_working_image=Image.open('../design/assets/send_diagram_page_send_diagram.png')
    send_diagram_send_diagram_working_image=send_diagram_send_diagram_working_image.resize((263, 112), Image.ANTIALIAS)
    send_diagram_send_diagram_image=ImageTk.PhotoImage(send_diagram_send_diagram_working_image)
    send_diagram_send_diagram_button=tk.Button(send_diagram_frame, image=send_diagram_send_diagram_image, bg="#D4BAEC",
    borderwidth=0, activebackground="#D4BAEC", command=send_diagram_execute)
    send_diagram_send_diagram_button.image=send_diagram_send_diagram_image
    send_diagram_send_diagram_button.place(relx=0.8, rely=0.8, anchor='center')

    #send diagrame page back button
    send_diagram_back_image=ImageTk.PhotoImage(Image.open("../design/assets/generic_back_button.png"))
    send_diagram_back_button=tk.Button(send_diagram_frame, image=send_diagram_back_image, bg="#D4BAEC", borderwidth=0,
    activebackground="#D4BAEC", command=go_back)
    send_diagram_back_button.image=send_diagram_back_image
    send_diagram_back_button.place(relx=0.1, rely=0.8, anchor="center")
    return
#---------------------------------------------------------------END SEND DIAGRAM PAGE-----------------------------------------------------------------



#-----------------------------------------------------------------ENTER SEND TRANSCRIPT_--------------------------------------------------------------
def send_transcript():

    def go_back():
        send_transcript_frame.place_forget()

    def choose_file():
        root.filename=filedialog.askopenfilename(initialdir="/home", title="Select Diagram", filetypes=(("text files", "*.txt"), ("All Files", "*.*")))
        transcript_filename=root.filename
        print("Selected transcript:", transcript_filename)
        send_transcript_entry_text_label=tk.Label(send_transcript_frame, bg="white", text=transcript_filename, font="Arial 16",
        foreground="#7F7F7F", justify="left")
        send_transcript_entry_text_label.place(relx=0.425, rely=0.4875, relwidth=0.525, relheight=0.065, anchor="center")
        twilio_transcript.send_sms_transcript(transcript_filename)

    #frame ofr send transcript page
    send_transcript_frame=tk.Frame(frame, bg="#D4BAEC")
    send_transcript_frame.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.7, anchor="center")

    #sned transcript page title
    send_transcript_title_image=ImageTk.PhotoImage(Image.open("../design/assets/send_transcript_page_text.png"))
    send_transcript_title_label=tk.Label(send_transcript_frame, image=send_transcript_title_image, bg="#D4BAEC")
    send_transcript_title_label.image = send_transcript_title_image
    send_transcript_title_label.place(relx=0, rely=0.2, anchor="w")

    #send transcript page entry
    send_transcript_entry_working_image=Image.open('../design/assets/generic_page_entry.png')
    send_transcript_entry_working_image=send_transcript_entry_working_image.resize((704, 74), Image.ANTIALIAS)
    send_transcript_entry_image=ImageTk.PhotoImage(send_transcript_entry_working_image)
    send_transcript_entry_label=tk.Label(send_transcript_frame, image=send_transcript_entry_image, bg="#D4BAEC")
    send_transcript_entry_label.image = send_transcript_entry_image
    send_transcript_entry_label.place(relx=0.425, rely=0.5, anchor="center")

    #send transcript choose file
    send_transcript_choose_file_working_image=Image.open("../design/assets/generic_choose_file_button.png")
    send_transcript_choose_file_working_image=send_transcript_choose_file_working_image.resize((184, 74), Image.ANTIALIAS)
    send_transcript_choose_file_image=ImageTk.PhotoImage(send_transcript_choose_file_working_image)
    send_transcript_choose_file_button=tk.Button(send_transcript_frame, image=send_transcript_choose_file_image, bg="#D4BAEC",
    borderwidth=0, activebackground="#D4BAEC", command=choose_file)
    send_transcript_choose_file_button.image=send_transcript_choose_file_image
    send_transcript_choose_file_button.place(relx=0.775, rely=0.5, anchor="center")

    #send transcript page send transcript button
    send_transcript_send_transcript_working_image=Image.open('../design/assets/send_transcript_page_transcript.png')
    send_transcript_send_transcript_working_image=send_transcript_send_transcript_working_image.resize((263, 112), Image.ANTIALIAS)
    send_transcript_send_transcript_image=ImageTk.PhotoImage(send_transcript_send_transcript_working_image)
    send_transcript_send_transcript_button=tk.Button(send_transcript_frame, image=send_transcript_send_transcript_image, bg="#D4BAEC",
    borderwidth=0, activebackground="#D4BAEC")
    send_transcript_send_transcript_button.image=send_transcript_send_transcript_image
    send_transcript_send_transcript_button.place(relx=0.8, rely=0.8, anchor='center')

    #send transcripte page back button
    send_transcript_back_image=ImageTk.PhotoImage(Image.open("../design/assets/generic_back_button.png"))
    send_transcript_back_button=tk.Button(send_transcript_frame, image=send_transcript_back_image, bg="#D4BAEC", borderwidth=0,
    activebackground="#D4BAEC", command=go_back)
    send_transcript_back_button.image=send_transcript_back_image
    send_transcript_back_button.place(relx=0.1, rely=0.8, anchor="center")
    return
#------------------------------------------------------------------END SEND  TRANSCRIPT---------------------------------------------------------------



#--------------------------------------------------------------------ENTER VOICE RECORDING------------------------------------------------------------
def voice_recording():
    global recording_enabled

    def go_back():
        voice_recording_frame.place_forget()

    def start_recording():
        global topic_name
        global recording_enabled
        if recording_enabled==False:
            print('Started recording')
            speech_to_text_command='gnome-terminal -- python3 ../modules/speech_to_text/speech-to-text.py'+' '+topic_name
            os.system(speech_to_text_command)
        else:
            print("Already recording")

    #view students Frame
    voice_recording_frame=tk.Frame(frame, bg="#D4BAEC")
    voice_recording_frame.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.7, anchor="center")

    #view students page title
    voice_recording_title_image=ImageTk.PhotoImage(Image.open("../design/assets/voice_recording_page_text.png"))
    voice_recording_title_label=tk.Label(voice_recording_frame, image=voice_recording_title_image, bg="#D4BAEC")
    voice_recording_title_label.image = voice_recording_title_image
    voice_recording_title_label.place(relx=0, rely=0.2, anchor="w")

    #voice recording start recording buttin
    voice_recording_start_recording_working_image=Image.open("../design/assets/voice_recording_page_start_recording.png")
    voice_recording_start_recording_working_image=voice_recording_start_recording_working_image.resize((276, 115), Image.ANTIALIAS)
    voice_recording_start_recording_image=ImageTk.PhotoImage(voice_recording_start_recording_working_image)
    voice_recording_start_recording_button=tk.Button(voice_recording_frame, image=voice_recording_start_recording_image, bg="#D4BAEC",
    borderwidth=0, activebackground="#D4BAEC", command=start_recording)
    voice_recording_start_recording_button.image=voice_recording_start_recording_image
    voice_recording_start_recording_button.place(relx=0.5, rely=0.5, anchor="center")

    # #voice recording stop recording buttin
    # voice_recording_stop_recording_working_image=Image.open("../design/assets/voice_recording_page_stop_recording.png")
    # voice_recording_stop_recording_working_image=voice_recording_stop_recording_working_image.resize((276, 115), Image.ANTIALIAS)
    # voice_recording_stop_recording_image=ImageTk.PhotoImage(voice_recording_stop_recording_working_image)
    # voice_recording_stop_recording_button=tk.Button(voice_recording_frame, image=voice_recording_stop_recording_image, bg="#D4BAEC",
    # borderwidth=0, activebackground="#D4BAEC", command=stop_recording)
    # voice_recording_stop_recording_button.image=voice_recording_stop_recording_image
    # voice_recording_stop_recording_button.place(relx=0.55, rely=0.5, anchor="w")

    #CODE TO START VOICE RECORDING
    #os.system('gnome-terminal -- python3 /home/raghav/RemEdi/modules/speech_to_text/speech-to-text.py')

    #voice recording page back button
    voice_recording_back_image=ImageTk.PhotoImage(Image.open("../design/assets/generic_back_button.png"))
    voice_recording_back_button=tk.Button(voice_recording_frame, image=voice_recording_back_image, bg="#D4BAEC", borderwidth=0,
    activebackground="#D4BAEC", command=go_back)
    voice_recording_back_button.image=voice_recording_back_image
    voice_recording_back_button.place(relx=0.1, rely=0.8, anchor="center")
#---------------------------------------------------------------------END VOICE RECORDING-------------------------------------------------------------



#------------------------------------------------------------------ENTER VIEW STUDENTS-----------------------------------------------------------------
def view_students():

    global students_list

    #update student_list
    def update_students_register(student_name, student_number):
        global students_register
        global students_list

        #check for empty fields
        if student_name is '' or student_number is '':
            print("Enter valid name and number.")
            return

        students_register.update({student_name: student_number})

        with open('../saved_data/students_register/students_register.json', 'w') as json_write_file:
            json.dump(students_register, json_write_file)

        #updating the list
        students_list.append(student_name)
        #delete entry in name and umber entry
        view_students_add_number_entry.delete(0, tk.END)
        view_students_add_name_entry.delete(0, tk.END)
        print("update student register: ", students_register)
        print("Students list:", students_list)
        view_students_frame.place_forget()
        view_students()

    def go_back():
        view_students_frame.place_forget()

    #view students Frame
    view_students_frame=tk.Frame(frame, bg="#D4BAEC")
    view_students_frame.place(relx=0.5, rely=0.5, relheight=0.7, relwidth=0.7, anchor="center")

    #view students page title
    view_students_title_image=ImageTk.PhotoImage(Image.open("../design/assets/view_students_page_text.png"))
    view_students_title_label=tk.Label(view_students_frame, image=view_students_title_image, bg="#D4BAEC")
    view_students_title_label.image = view_students_title_image
    view_students_title_label.place(relx=0, rely=0.2, anchor="w")

    #view student enetr name
    view_students_add_name_entry_working_image=Image.open('../design/assets/view_students_name_entry.png')
    view_students_add_name_entry_working_image=view_students_add_name_entry_working_image.resize((580, 64), Image.ANTIALIAS)
    view_students_add_name_entry_image=ImageTk.PhotoImage(view_students_add_name_entry_working_image)
    view_students_add_name_entry_label=tk.Label(view_students_frame, image=view_students_add_name_entry_image, bg="#D4BAEC")
    view_students_add_name_entry_label.image = view_students_add_name_entry_image
    view_students_add_name_entry_label.place(relx=0.4, rely=0.4, anchor="center")

    #enter name Entry
    view_students_add_name_entry=tk.Entry(view_students_frame, bg="white", font="Arial 14", foreground="#7F7F7F", borderwidth=0, relief='flat')
    view_students_add_name_entry.place(relx=0.45, rely=0.39275, relwidth=0.3425, relheight=0.0625, anchor="center")

    #view student enetr number
    view_students_add_number_entry_working_image=Image.open('../design/assets/view_students_number_entry.png')
    view_students_add_number_entry_working_image=view_students_add_number_entry_working_image.resize((580, 64), Image.ANTIALIAS)
    view_students_add_number_entry_image=ImageTk.PhotoImage(view_students_add_number_entry_working_image)
    view_students_add_number_entry_label=tk.Label(view_students_frame, image=view_students_add_number_entry_image, bg="#D4BAEC")
    view_students_add_number_entry_label.image = view_students_add_number_entry_image
    view_students_add_number_entry_label.place(relx=0.4, rely=0.5, anchor="center")

    #enter number Entry
    view_students_add_number_entry=tk.Entry(view_students_frame, bg="white", font="Arial 14", foreground="#7F7F7F", borderwidth=0, relief='flat')
    view_students_add_number_entry.place(relx=0.45, rely=0.49275, relwidth=0.3425, relheight=0.0625, anchor="center")

    #view students page add students button
    view_students_add_students_working_image=Image.open('../design/assets/view_students_add_students.png')
    view_students_add_students_working_image=view_students_add_students_working_image.resize((263, 112), Image.ANTIALIAS)
    view_students_add_students_image=ImageTk.PhotoImage(view_students_add_students_working_image)
    view_students_add_students_button=tk.Button(view_students_frame, image=view_students_add_students_image, bg="#D4BAEC",
    borderwidth=0, activebackground="#D4BAEC",
    command=lambda: update_students_register(view_students_add_name_entry.get(), view_students_add_number_entry.get()))
    view_students_add_students_button.image=view_students_add_students_image
    view_students_add_students_button.place(relx=0.75, rely=0.45, anchor='center')

    #view students page back BUTTON
    view_students_back_image=ImageTk.PhotoImage(Image.open("../design/assets/generic_back_button.png"))
    view_students_back_button=tk.Button(view_students_frame, image=view_students_back_image, bg="#D4BAEC", borderwidth=0,
    activebackground="#D4BAEC", command=go_back)
    view_students_back_button.image=view_students_back_image
    view_students_back_button.place(relx=0.1, rely=0.8, anchor="center")
    #
    # #view students page remove student button
    # view_students_remove_student_working_image=Image.open('/home/raghav/RemEdi/design/assets/view_students_remove_student.png')
    # view_students_remove_student_working_image=view_students_remove_student_working_image.resize((263, 112), Image.ANTIALIAS)
    # view_students_remove_student_image=ImageTk.PhotoImage(view_students_remove_student_working_image)
    # view_students_remove_student_button=tk.Button(view_students_frame, image=view_students_remove_student_image, bg="#D4BAEC",
    # borderwidth=0, activebackground="#D4BAEC")
    # view_students_remove_student_button.image=view_students_remove_student_image
    # view_students_remove_student_button.place(relx=0.75, rely=0.75, anchor='center')
#-----------------------------------------------------------------END VIEW STUDENTS--------------------------------------------------------------------



#--------------------------------------------------------------_----ENTER BEGIN CLASS---------------------------------------------------------------
def begin_class():
    twilio_invitation.send_invitation(topic_name)
#-------------------------------------------------------------------END BEHIN CLASS-----------------------------------------------------------------



frame=tk.Frame(root, bg="white")
frame.place(relx=0, rely=0, relwidth=1, relheight=1)#relative to parent ie root here


#---------------------------------------------SET THE OPTIONS BUTTONS---------------------------------------------------------------------------------
options_frame=tk.Frame(frame, bg="white")
options_frame.place(relx=0, rely=OPTIONS_RELY, relheight=0.3, relwidth=1)

#send diagram button
send_diagram_image=ImageTk.PhotoImage(Image.open('../design/assets/send_diagram.png'))
send_diagram_button = tk.Button(options_frame, image=send_diagram_image, borderwidth=0, relief='flat', bg="white",
activebackground="white", command=send_diagram)
send_diagram_button.place(relx=0.1334375, rely=0, anchor="n")

#voice recording button
voice_recording_image=ImageTk.PhotoImage(Image.open('../design/assets/voice_recording.png'))
voice_recording_button = tk.Button(options_frame, image=voice_recording_image, borderwidth=0, relief='flat', bg="white",
activebackground="white", command=voice_recording)
voice_recording_button.place(relx=0.1334375+0.244375, rely=0, anchor="n")

#add students button
view_students_image=ImageTk.PhotoImage(Image.open('../design/assets/view_students.png'))
# button = tk.Button(frame, text="Choose Image", bg="#FDB927", activebackground='white', foreground="black", command=lambda: test_function(entry.get()))
view_students_button = tk.Button(options_frame, image=view_students_image, borderwidth=0, bg="white", relief='flat',
activebackground="white", command=view_students)
view_students_button.place(relx=0.1334375+0.244375+0.244375, rely=0, anchor="n")

#send transcript button
send_transcript_image=ImageTk.PhotoImage(Image.open('../design/assets/send_transcript.png'))
send_transcript_button = tk.Button(options_frame, image=send_transcript_image, borderwidth=0, bg="white", relief='flat',
activebackground="white", command=send_transcript)
send_transcript_button.place(relx=0.1334375+0.244375+0.244375+0.244375, rely=0, anchor="n")
#---------------------------------------------  END OF OPTIONS BUTTONS---------------------------------------------------------------------------------



#_______________________________________________ENTER TOPIC ENTRY_____________________________________________________________________________________
def update_topic(topic_entry_text):
    global topic_name
    topic_name=topic_entry_text
    print(topic_name)

#frame for topic
topic_frame=tk.Frame(frame, bg="white")
topic_frame.place(relx=0, rely=TOPIC_RELY, relheight=0.275, relwidth=1)

#open and resize topic image
topic_working_image=Image.open('../design/assets/todays_topic.png')
topic_working_image=topic_working_image.resize((1775, 274), Image.ANTIALIAS)
#image label for topic entry
topic_image=ImageTk.PhotoImage(topic_working_image)
topic_label=tk.Label(topic_frame, image=topic_image, bg="white")
topic_label.place(relx=0.5, rely=0.5, anchor='center')

#topic Entry
topic_entry=tk.Entry(topic_frame, bg="white", font="Arial 36", foreground="#7F7F7F", borderwidth=0, relief='flat')
topic_entry.place(relx=0.57, rely=0.45, relwidth=0.65, relheight=0.5, anchor="center")

#topic OK BUTTON
topic_entry_button=tk.Button(topic_frame, text="OK", font="Arial 24", foreground="white", activeforeground="white",
borderwidth=0, bg="#552582", relief='flat', activebackground="#552582",
command=lambda: update_topic(topic_entry.get()))
topic_entry_button.place(relx=0.935, rely=0.45, relwidth=0.05, relheight=0.2, anchor="center")
#_______________________________________________END TOPIC ENTRY_____________________________________________________________________________________



#-------------------------------------------ENTER TOP RIGHT LOGO-------------------------------------------------------------------------------------
#frame for top logo
top_logo_frame=tk.Frame(frame, bg="white")
top_logo_frame.place(relx=0, rely=TOPLOGO_RELY, relheight=0.155, relwidth=1, anchor="nw")

#label for top logo
top_logo_image=ImageTk.PhotoImage(Image.open('../design/assets/logo_small.png'))
top_logo_label=tk.Label(top_logo_frame, image=top_logo_image, bg="white")
top_logo_label.place(relx=0.145, rely=0.5, anchor='center')
#-------------------------------------------END TOP RIGHT LOGO-------------------------------------------------------------------------------------



#-------------------------------------------ENTER BEGIN CLASS BUTTON--------------------------------------------------------------------------------
#frame for begin class
begin_class_frame=tk.Frame(frame, bg='white')
begin_class_frame.place(relx=0, rely=BEGINCLASS_RELY, relwidth=1, relheight=0.2)

#begin class BUTTON
#send transcript button
begin_class_image=ImageTk.PhotoImage(Image.open('../design/assets/begin_class.png'))
begin_class_button = tk.Button(begin_class_frame, image=begin_class_image, borderwidth=0, bg="white", relief='flat', activebackground="white", command=begin_class)
begin_class_button.place(relx=0.86, rely=0.5, anchor="center")
#-------------------------------------------END BEGIN CLASS BUTTON----------------------------------------------------------------------------------

root.mainloop()
