import subprocess
import time
import sys
import os


#runname and userid are the first 2 arguments passed into the terminal command
runname = sys.argv[1]
userid = sys.argv[2]

#number of distinct tasks that will be included in the stream    
numtasks = input("How many tasks?")
totaltasks = {}
counter = 1

#collect task names and durations
for i in range(int(numtasks)):
    name = input("What do you want to call task " + str(counter) + "?")
    
    dur = input("Duration of task " + str(counter) + "?")
    while True:
        try:
            int(dur)
            break
        except:
            print("Enter an integer number for duration: ")
            dur = input("Duration of task " + str(counter) + "?")
    
    totaltasks[name] = dur
    counter += 1


newstr = ''
for item in totaltasks:
    newstr += item + '.png, '

print('Make sure that ' + newstr + ' are all in users folder.')

#list of strings that represent all the image files that will be used in stream
imagefiles = []
for item in totaltasks:
    imagefiles.append(str(item[0]) + '.png')

newpath = './study/' + str(userid) + '/images/'


#########################
#allow user to create sequence of tasks
finished = False
procedure = []
order = []
counter = 1
while not finished:
    new = input('Enter task ' + str(counter) + ': ')
    
    #adding task
    if new in totaltasks.keys():
        procedure.append(int(totaltasks[new]))
        order.append(new)
        command = 'cp ./' + new + '.png' + ' ' + newpath
        os.system(command)
        old = newpath + new + '.png'
        new1 = newpath + str(counter) + new + '.png'
        
        #creation of command, running command
        command = 'mv ' + old + ' ' + new1
        os.system(command)
    
        counter += 1
    
    #sequence is over
    elif new == 'quit':
        finished = True
        continue
    
    #case of typo
    while new != 'quit' and new not in totaltasks:
        print("Typo. Try again.")
        new = input('Enter task ' + str(counter) + ': ')
        
    
    #repeating same task consecutively
    repprev = input('Do you want to repeat previous task? Answer yes or no')
    
    while repprev != 'yes' and repprev != 'no':
        
        print("Typo, try again.")
        repprev = input('Do you want to repeat previous task? Answer yes or no')
        
    if repprev == 'yes':
        
        howman = input('How many times?')
        
        while True:
            try:
                int(howman)
                break
            except:
                print("Typo. Try again.")
                howman = input('How many times?')
            
        for i in range(int(howman)-1):
            procedure.append(int(totaltasks[new]))
            order.append(new)
            command = 'cp ./' + new + '.png' + ' ' + newpath
            os.system(command)
            old = newpath + new + '.png'
            new1 = newpath + str(counter) + new + '.png'
            command = 'mv ' + old + ' ' + new1
            os.system(command)
            
            counter += 1
            
    #repeating same sequence of tasks consecutively
    else:
        repseq = input('Do you want to repeat previous sequence? Answer yes or no')
        
        while repseq != 'yes' and repseq != 'no':
                
            print("Typo. Try again.")
            repseq = input('Do you want to repeat previous sequence? Answer yes or no')
            
        if repseq == 'yes':
            
            howman2 = input('How many items in sequence?')
            seqnum = input('How many times?')
            end = len(procedure)
            sequence = order[end-int(howman2):]
            print('sequence = ' + str(sequence))
            for i in range(int(seqnum)-1):
                for item in sequence:
                    if item in totaltasks.keys():
                        procedure.append(int(totaltasks[item]))
                        order.append(item)
                        command = 'cp ./' + item + '.png' + ' ' + newpath
                        os.system(command)
                        old = newpath + item + '.png'
                        new1 = newpath + str(counter) + item + '.png'
                        command = 'mv ' + old + ' ' + new1
                        os.system(command)
                    counter += 1
                
        else:
            continue
    

#address of blueberry which is needed as an argument to be passed in for bby_stream.py
address = input("Enter blueberry address: ")
    
    
#calculating totaldur
totaldur = sum(procedure)

print('Num tasks: ' + str(len(procedure)))
print("Total duration: " + str(totaldur))

#playing all files as images
initialize = str('python3 initialize.py start ' + str(userid) + ' ' + str(runname))
for item in totaltasks.items():
    initialize += ' ' + str(item[0]) + ' ' + str(item[1])

#refining all of the data, arguments to be passed in for refine.py
refine = str('python3 refine.py ' + str(userid) + ' ' + str(runname))
for item in totaltasks.items():
    refine += ' ' + str(item[0]) + ' ' + str(item[1])
    


try:

    subprocess.Popen('python3 bby_stream.py -a ' + str(address) + ' -d -u '  + str(userid) + ' -r ' + str(runname) + ' -o ' + str(totaldur), shell= True)
    time.sleep(5)
    subprocess.Popen(str(initialize), shell= True)
    time.sleep(totaldur + 20)
    subprocess.Popen(str(refine), shell= True)
except KeyboardInterrupt:
    print()
    print("User stopped program.")
    


