# from ssl import _Cipher
import time
import random
import signal
from tkinter import *
import subprocess
import sys
import os
from gtts import gTTS
from playsound import playsound


def handler(signum, frame):
    raise Exception("")


signal.signal(signal.SIGALRM, handler)
rounds = 1
math_per_round = 5
reps_per_math = 10

rep_time = 3
rest_time = reps_per_math * rep_time
break_time = 120 

userid = sys.argv[1]
runname = sys.argv[2]

# runname = 1
# while os.path.isfile('./data/'+userid+'/'+str(runname)+'R.csv'):
#     runname += 1
# print("trial: " + str(runname))

blueberry1 = '3E8847D9-3D52-7A2F-B913-2FBD9F63ECF3'
blueberry2 = '737E96F8-345B-0B18-66D0-B72FF7301397'

# sets = int(input("How many sets?"))

stimulus = "visual"
# stimulus = input("Which stimulus type? (visual, auditory, mental)   ")


# create random problems and .mp3 files if auditory
if stimulus != 'mental':

# def generate_numbers():
    problems = [[ ['']*reps_per_math for i in range(math_per_round)] for j in range(rounds)]
    for i in range(rounds):
        for j in range(math_per_round):
            for k in range(reps_per_math):
                # a = random.randint(100,999)
                # b = random.randint(100,999)
                a1 = a2 = b1 = b2 = 0
                while a1+b1<10 and a2+b2<10:
                    a1 = random.randint(1,9)
                    a2 = random.randint(1,9)
                    b1 = random.randint(1,9)
                    b2 = random.randint(1,9)
                a = a1*10+a2
                b = b1*10+b2
                problems[i][j][k] = str(a) + ' + ' + str(b)

                if stimulus == 'auditory':
                    audio = gTTS(text=problems[i][j][k], lang='en', slow=False)
                    audio.save('audio_files/' + str(i) + '_' + str(j) + '_' + str(k) + '.mp3')

# setup tkinter
win = Tk()
win.configure(background='black')
win.attributes('-fullscreen',True)
label = Label(win, text='', font='none 100 bold', bg='black', fg='white')
label.pack(padx=100,pady=500)
win.update()

    
def display_text(text):
    label.config(text=text)
    win.update()
    time.sleep(60)


def countdown(duration, type):
    for s in range(duration,0,-1):
            signal.alarm(1)
            try:
                display_text(str(s) + 's ' + type)
            except Exception:
                pass


def visual():
    countdown(10, 'Rest')

    for i in range(rounds): # 1 round = sets x (math + rest)
        for j in range(math_per_round): # sets = how many math / rest repetitions
            for k in range(reps_per_math): # reps = how many problems per math block
                signal.alarm(rep_time)
                try:
                    display_text(problems[i][j][k])
                except Exception:
                    pass

            countdown(rest_time, 'Rest')

        if (i != rounds-1):
            countdown(break_time, 'Break')


def auditory():
    countdown(10, 'Rest')

    for i in range(rounds): # 1 round = sets x (math + rest)
        for j in range(math_per_round): # sets = how many math / rest repetitions
            # playsound('audio_files/' + str(i) + '_' + str(j) + '_' + str(0) + '.mp3')
            label.config(text='Math')
            win.update()
            for k in range(reps_per_math): # reps = how many problems per math block
                signal.alarm(rep_time)
                try:
                    playsound('audio_files/' + str(i) + '_' + str(j) + '_' + str(k) + '.mp3')
                    time.sleep(10)
                except Exception:
                    pass

            countdown(rest_time, 'Rest')

        if (i != rounds-1):
            countdown(break_time, 'Break')


def mental():
    countdown(10, 'Rest')

    for i in range(rounds): # 1 round = sets x (math + rest)
        for j in range(math_per_round): # sets = how many math / rest repetitions
            signal.alarm(rest_time)
            try:
                display_text('Mental Math')
            except Exception:
                pass

            countdown(rest_time, 'Rest')

        if (i != rounds-1):
            countdown(break_time, 'Break')

# start recieving data
try:
    p1 = subprocess.Popen('python3 2dev_record.py -a ' + blueberry1 + ' -u '  + userid + ' -r ' + str(runname), shell= True)
    p2 = subprocess.Popen('python3 2dev_record.py -a ' + blueberry2 + ' -u '  + userid + ' -r ' + str(runname), shell= True)

    # (output, err) = p.communicate()  

    # #This makes the wait possible
    # p_status = p.wait()

    time.sleep(10)
except KeyboardInterrupt:
    raise Exception("User stopped program.")


start = round(time.time(), 3) + 10
# start_time = time.strftime("%H:%M:%S", time.localtime())

if stimulus == 'visual':
    visual()
elif stimulus == 'auditory':
    auditory()
elif stimulus == 'mental':
    mental()
else:
    raise ValueError('Unknown stimulus type! Must be \'visual\', \'auditory\', or \'mental\'.')

end = round(time.time(), 3) # IN MS
# end_time = time.strftime("%H:%M:%S", time.localtime())

time.sleep(5)
p1.kill()
p2.kill()

print(start)
print(end)

# print("start time:", start_time)
# print("end time:", end_time)

if stimulus != 'mental':
    print(problems)






    