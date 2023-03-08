import time
import random
import signal
from tkinter import *
import subprocess
import sys
from gtts import gTTS
from playsound import playsound


def handler(signum, frame):
    raise Exception("")


signal.signal(signal.SIGALRM, handler)
rounds = 1
round_time = 5 * 60
math_per_round = 3
reps_per_math = 10

rep_time = 3
math_time = reps_per_math * rep_time
break_time = 120

userid = sys.argv[1]
runname = sys.argv[2]

blueberry1 = '3E8847D9-3D52-7A2F-B913-2FBD9F63ECF3'
blueberry2 = 'CAC8BEEB-CDC7-ED2F-04D7-48A3A88C2614'
blueberry3 = '737E96F8-345B-0B18-66D0-B72FF7301397'

# sets = int(input("How many sets?"))
stimulus = "visual"
# stimulus = input("Which stimulus type? (visual, auditory, mental)   ")


if stimulus != 'mental':
    # create random problems` and .mp3 files if auditory
    problems = [[ ['']*reps_per_math for i in range(math_per_round)] for j in range(rounds)]
    for i in range(rounds):
        for j in range(math_per_round):
            for k in range(reps_per_math):
                # a = random.randint(100,999)
                # b = random.randint(100,999)
                a1 = 0
                b1 = 0
                while (a1+b1<10):
                    a1 = random.randint(1,9)
                    b1 = random.randint(1,9)
                a = random.randint(1,9)*10+a1
                b = random.randint(1,9)*10+b1
                problems[i][j][k] = str(a) + ' + ' + str(b)

                if stimulus == 'auditory':
                    audio = gTTS(text=problems[i][j][k], lang='en', slow=False)
                    audio.save('audio_files/' + str(i) + '_' + str(j) + '_' + str(k) + '.mp3')



# randomly choose math period start times
math_start = [[0 for i in range(math_per_round)] for j in range(rounds)]
rest_start = [[0 for i in range(math_per_round)] for j in range(rounds)]

for i in range(rounds):
    valid = False
    while not valid:
        start_times = random.sample(range(270), math_per_round*2)
        start_times_sorted = sorted(start_times)

        for t in range(math_per_round*2-1):
            if start_times_sorted[t+1] - start_times_sorted[t] < 40:
                valid = False
                break
            valid = True
    
    math_start[i] = sorted(start_times[:math_per_round])
    rest_start[i] = sorted(start_times[math_per_round:])    
    



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


def non_math(duration:int, type:str, countdown:bool):
    for s in range(duration,0,-1):
            signal.alarm(1)
            try:
                if countdown:
                    display_text(str(s) + 's ' + type)
                else:
                    display_text(type)
            except Exception:
                pass


def visual():
    non_math(10, 'Rest', False)

    for i in range(rounds): # 1 round = sets x (math + rest)
        non_math(math_start[i][0], 'Rest', False)
        for j in range(math_per_round): # sets = how many math / rest repetitions
            for k in range(reps_per_math): # reps = how many problems per math block
                signal.alarm(rep_time)
                try:
                    display_text(problems[i][j][k])
                except Exception:
                    pass
            
            if j != math_per_round-1:
                rest_time = math_start[i][j+1] - (math_start[i][j] + math_time)
            else:
                rest_time = round_time - (math_start[i][j] + math_time)
            non_math(rest_time, 'Rest', False)

        if i != rounds-1:
            non_math(break_time, 'Break', True)


def auditory():
    non_math(10, 'Rest', False)

    for i in range(rounds): 
        non_math(math_start[i][0], 'Rest', False)
        for j in range(math_per_round): 
            label.config(text='Math')
            win.update()
            for k in range(reps_per_math): 
                signal.alarm(rep_time)
                try:
                    playsound('audio_files/' + str(i) + '_' + str(j) + '_' + str(k) + '.mp3')
                    time.sleep(60)
                except Exception:
                    pass
            
            if j != math_per_round-1:
                rest_time = math_start[i][j+1] - (math_start[i][j] + math_time)
            else:
                rest_time = round_time - (math_start[i][j] + math_time)
            non_math(rest_time, 'Rest', False)

        if i != rounds-1:
            non_math(break_time, 'Break', True)


def mental():
    non_math(10, 'Rest', False)

    for i in range(rounds): 
        non_math(math_start[i][0], 'Rest', False)
        for j in range(math_per_round): 
            signal.alarm(math_time)

            try:
                display_text('Mental Math')
            except Exception:
                pass
            
            if j != math_per_round-1:
                rest_time = math_start[i][j+1] - (math_start[i][j] + math_time)
            else:
                rest_time = round_time - (math_start[i][j] + math_time)
            non_math(rest_time, 'Rest', False)

        if i != rounds-1:
            non_math(break_time, 'Break', True)


try:
    p1 = subprocess.Popen('python3 blueberry_scripts/blueberry_connect_save_data.py -a ' + blueberry1 + ' -u '  + userid + ' -r ' + str(runname), shell= True)
    p2 = subprocess.Popen('python3 blueberry_scripts/blueberry_connect_save_data.py -a ' + blueberry2 + ' -u '  + userid + ' -r ' + str(runname), shell= True)
    p3 = subprocess.Popen('python3 blueberry_scripts/blueberry_connect_save_data.py -a ' + blueberry3 + ' -u '  + userid + ' -r ' + str(runname), shell= True)
    time.sleep(10)
except KeyboardInterrupt:
    print("User stopped program.")


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
p3.kill()

print('start:', start)
# print('end:', end)

# print('start time:', start_time)
# print('end time:', end_time)

print('math start:', math_start[0])
print('rest start:', rest_start[0])

if stimulus != 'mental':
    print('problems:', problems)








    