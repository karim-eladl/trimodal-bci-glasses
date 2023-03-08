import os
import threading
import tkinter as tk
import time
import sys
import re
import datetime
from datetime import datetime
import csv
import imageio
import click
from PIL import Image, ImageTk
from collect_data_attU_files import count_lines
from collect_data_attU_files import start_connection
from collect_data_attU_files import run_streamer
import asyncio
import json
from Connection import Connection
from Utils import write_arr
from datetime import date
import time
from playsound import playsound
from references import convert_to_task
from references import conv_arr_file
from references import gettask
import pandas as pd
import numpy as np
from multiprocessing import Process
import threading
from threading import Thread




ROOT = "./data"

try:
    os.mkdir(f"{ROOT}")
except FileExistsError:
    pass


timestamp = date.today()
start_time = datetime.now()
today = date.today()




class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class tkvideo():
    def __init__(self, path, label, size = (640,360), next = None):
        self.path = path
        self.label = label
        self.size = size
        self.next = next
    
    def load(self, path, label):
        frame_data = imageio.get_reader(path)

        # TODO: play this using time sequence (as in frames per second), and not iterating over frames!
        for image in frame_data.iter_data():
            image = Image.fromarray(image)

            
            (width, height) = image.size
            ratio = width / height

            # maintain aspect ratio
            new_height = self.size[1]
            new_width = int(ratio * new_height)
            
            resized = image.resize((new_width, new_height), Image.ANTIALIAS)
            frame_image = ImageTk.PhotoImage(resized)
            label.config(image=frame_image)
            label.image = frame_image

        self.next()

    def play(self):
        thread = threading.Thread(target=self.load, args=(self.path, self.label))
        thread.daemon = 1
        thread.start()

#////////////////////////////////////////

def get_image_path(dir_name, image_name):
    return dir_name + image_name

def csort(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def atoi(text):
    return int(text) if text.isdigit() else text

#////////////////////////////////////////

class Sequencer():
    def __init__(self, user, rno, totaltasks):
        self.ptime = 10 # seconds

        self.user = user
        self.image_dir = "study/{}/images/".format(user)
        self.video_dir = "study/{}/videos/".format(user)
        self.rno = rno
        self.totaltasks = totaltasks

        self.events = []
        self.videos = []
        self.current_video = 0
        self.background = "gray"
        
        self.root = tk.Tk()
        self.root.title("AttentivU – Lexington – 2021")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.attributes('-fullscreen',True)
        self.root.configure(background=self.background)
        
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.minsize(self.width, self.height)

        self.label = tk.Label(text="")
        self.label.pack()
        self.label.place(x=self.width/2, y=self.height/2, anchor=tk.CENTER)
        self.label.configure(background=self.background)

        # self.update_clock()
        # self.render_image("study/bg_grey.jpg")

        # this is a deferred start call, 1 second after the init
        self.root.after(1000, self.start)
        self.root.mainloop()
        

    def shorten(self, imagename):
        #function that names a string imagename as "123example.png" and extracts the word "example"
        #extracts task name from a string name of a file that has an image for that task
        counter = 0
        while True:
            try:
                int(imagename[counter])
                counter += 1
            except:
                break
            
        return imagename[counter:len(imagename)-4]
            
    def callback(self):
        self.root.quit()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.root.after(1000, self.update_clock)

    def record_event(self, record):
        self.events.append([time.time(), record])

    def write_to_csv(self):
        t_stamp = int(time.time())
        try:
            os.mkdir("study/" + str(self.user) + "/" + str(self.rno) + "/")
        except:
            pass
        path = "study/" + str(self.user) + "/" + str(self.rno) + "/events.csv".format(self.user, t_stamp)
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.events)

        return path

    def render_image(self, path):
        load = Image.open(path)
        width, height = load.size
        ratio = width / height

        # maintain aspect ratio
        new_height = self.height
        new_width = int(ratio * new_height)

        resized = load.resize((new_width, new_height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(resized)

        self.label.configure(image = image)
        self.label.image = image

    # this is where the logic starts
    def start(self):
        self.iterate_images()

    def done(self):
        self.record_break()
        path = self.write_to_csv()
        print("saved data to", path)
        print('done')
        self.callback()

    def record_break(self):
        #self.render_image("study/bg_grey.jpg")
        self.record_event("break")
        time.sleep(self.ptime)

    def loop_image(self, image_dir, image_name, index, total):
        # print('loop_image', image_name, index, total)
        rawname = self.shorten(image_name)
        playsound(str(rawname) + '.mp3')
        path = get_image_path(self.image_dir, image_name)
        self.record_event(image_name)
        self.render_image(path)

    def iterate_images(self):
        #iterates through all images for the duration specified in wrapper.py
        imgs = os.listdir(self.image_dir)
        imgs.sort(key = csort)

        counter = 0
        total = 0
        index = 0

        for image_name in imgs:
            if not image_name.startswith('.'):
                total += 1

        for image_name in imgs:
            
            if not image_name.startswith('.'):
                
                self.root.after(counter * 1000, self.loop_image, self.image_dir, image_name, index, total)
                index += 1
                
                #if the task representing the image is in our list of eligible tasks
                rawname = self.shorten(image_name)
                
                if rawname in totaltasks.keys():
                    
                    #counter is increased by duration of the specific, current task
                    counter += int(totaltasks[rawname])
                
                    
                
                    

        self.root.after(counter * 1000, self.iterate_videos)

    def iterate_videos(self):
        vids = os.listdir(self.video_dir)
        vids.sort(key = csort)
        

        for video_name in vids:
            if not video_name.startswith('.'):
                self.videos.append(self.video_dir + video_name)

        self.play_videos()

    def play_videos(self):
        # print("play_videos", self.current_video)
        
        if self.current_video == len(self.videos):
            self.done()
        else:
            path = self.videos[self.current_video]
            video_name = path.split('/').pop()
            self.record_event(video_name)
            self.current_video = self.current_video + 1
            self.player = tkvideo(path, self.label, size = (self.width,self.height), next = self.play_videos)
            self.player.play()


def start_pipeline(user, rno, totaltasks):
    sequencer = Sequencer(user, rno, totaltasks)

def init_user(user):
    imdir = "study/{}/images/".format(user)
    vidir = "study/{}/videos/".format(user)
    if(os.path.isdir(imdir)==True or os.path.isdir(vidir)== True):
        raise OSError("User files already exist. Use 'start' command to start the pipeline.")
    os.makedirs(imdir)
    os.makedirs(vidir)
    print("User Initialized")

def remove_user(user):
    if(os.path.isdir("study/{}/".format(user))==False):
         raise OSError("User does not exist")
    shutil.rmtree("study/{}/".format(user))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(color.BOLD)
        print(         
"""            Welcome to AttentivU Study recorder Lexington 2021!"""
        )
        print(color.END)
        print(         
"""            Quick information on how to use this script:
            $ python3 study.py init <user_name>
            Creates <user_name> folder in the <study> folder.
            $ python3 study.py remove <user_name>
            Removes <user_name> folder in the <study> folder.
            $ python3 Streamer.py
            Starts recording for AttentivU glasses in the <data> folder.
            $ python3 study.py start <user_name>
            Starts the study for the <user_name> folder in the <study> folder. Please launch this one in a new terminal window.
            For more details please refer to README.md
            """
        )
    else:
        command = sys.argv[1]
        user = sys.argv[2]
        
        
        
        try:
            #not initializing user, starting stream of images
            if(command=='start'):
                rno = sys.argv[3]
                
                #create dictionary based on arguments passed in with command
                #dictionary where keys are task names and values are task durations
                i = 4
                totaltasks = {}
                try:
                    while True:
                        totaltasks[sys.argv[i]] = sys.argv[i + 1]
                        i += 2
                except:
                    pass
                start_pipeline(user, rno, totaltasks)
                             
                
            elif(command=='init'):
                init_user(user)
            elif(command=='remove'):
                remove_user(user)
            else:
                raise Exception("Invalid argument {}. Refer to readme for usage".format(command))
        except Exception as E:
            print(E)
