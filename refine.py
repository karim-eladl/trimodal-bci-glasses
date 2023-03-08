#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 15:55:00 2021

@author: mayaabiram
"""

import references
import os
from references import convert_to_task
import sys
import pandas as pd
import references
from references import conv_arr_file
import numpy as np
import bisect

ROOT = "./data"

ROOTEV = "."

try:
    os.mkdir(f"{ROOT}")
except FileExistsError:
    pass

# Make the root directory if it doesn't exist
try:
    os.mkdir(f"{ROOT}/muse/")
except FileExistsError:
    pass

try:
    os.mkdir(f"{ROOTEV}")
except FileExistsError:
    pass

try:
    os.mkdir(f"{ROOTEV}/study/")
except FileExistsError:
    pass

try:
    os.mkdir(f"{ROOT}/blueberry/")
except FileExistsError:
    pass



locationevents = f"{ROOTEV}/study/"

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect.bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError


def shorten(imagename):
        
    counter = 0
    while True:
        try:
            int(imagename[counter])
            counter += 1
        except:
            break
        
    return imagename[counter:len(imagename)-4]

def get_timestamps(file):
    
    timestamps = []
    
    with open(file) as e:
        df = pd.read_csv(e, header = None)
        arruse = df.values
        e.close()
    
    for row in arruse:
        timestamps.append(row[0])

    return timestamps

def get_order(totaltasks, file):
    
    
    
    order = []
    with open(file) as e:
        df = pd.read_csv(e, header = None)
        arruse = df.values
        e.close()
    
    for row in arruse[:-1]:
        
        order.append(shorten(row[1]))
           
    print('order: ' + str(order))
    return order


    
def refine_code_muse(userid, rno, totaltasks):
    
    try:
        os.mkdir(f"{ROOTEV}/study/{userid}")
    except FileExistsError:
        pass
    
    try:
        os.mkdir(f"{ROOTEV}/study/{userid}/{rno}")
    except FileExistsError:
        pass
    
    eventsfile = "./study/" + str(userid) + "/" + str(rno) + "/events.csv"
    order = get_order(totaltasks, eventsfile)
    
    timestamps = get_timestamps(eventsfile)


    filename2 = f'{ROOT}/muse/{userid}/{rno}/EEG.csv'

    sloc = f"{ROOT}/muse/{userid}/{rno}"
    
    
    #START WITH MUSE
    
    with open(filename2) as f:
        #f is a string representing name of .csv file 
        df = pd.read_csv(f)
        arruse = df.values
        f.close()
        
        arruse = [arruse]
        
    
    #create dict and order
    masterdict = {}
    ordering = []
    points = []
    
    timestampdict = {}
    orderedtime = []
    counter = 0
    
    dictofarrs = {}
    for item in totaltasks.items():
        dictofarrs[item[0]] = []
    
    
    #conv to right format
    for j in range(len(arruse)):
        for i in range(len(arruse[j])):
                
            temp = arruse[j][i]
            
            try:
                tempnext = arruse[j][i + 1]
                maxval = False
            except:
                maxval = True

            masterdict[temp[0]] = [temp[0], temp[1], temp[2], temp[3], temp[4]]
            ordering.append(temp[0]) 

    
    for item in timestamps:
        c = find_lt(ordering, item)
        orderedtime.append(c)
        points.append(ordering.index(c))
                  
    
    
    try:

        
        for i in range(0, len(points)-1):
                    
            for k in range(points[i], points[i+1]):
                cur = ordering[k]
                dictofarrs[order[i]].append(masterdict[cur])
                    
                        
    except:
        pass
    
    
    try:
        os.mkdir(sloc)
    except FileExistsError:
        pass
    
    for key in totaltasks:
        
        try:
            os.makedirs(sloc+ '/' + str(key) + '/')

        except:
            pass
    
    for key in totaltasks:
        conv_arr_file(dictofarrs[key], sloc+ '/' + str(key) + '/' + str(key) + '.csv')

def refine_code_blue(userid, rno, totaltasks):
    eventsfile = "./study/" + str(userid) + "/" + str(rno) + "/events.csv"
    order = get_order(totaltasks, eventsfile)
    
    timestamps = get_timestamps(eventsfile)
    
    try:
        os.mkdir(f"{ROOT}/blueberry/" + str(userid) + '/')
        os.mkdir(f"{ROOT}/blueberry/" + str(userid) + '/' + str(rno) + '/')
    except:
        pass
    
    filename1 = f"{ROOT}/blueberry/" + str(userid) + '/' + str(rno) + '/' + 'exg.csv'
    slocat = f"{ROOT}/blueberry/{userid}/{rno}"
    
    with open(filename1) as f:
        #f is a string representing name of .csv file 
        df = pd.read_csv(f)
        arruse = df.values
        f.close()
        
        arruse = [arruse]
        
    #create dict and order
    masterdict = {}
    ordering = []
    
    orderedtime = []

    dictofarrs = {}
    for item in totaltasks.items():
        dictofarrs[item[0]] = []
        
    points = []
    
    #conv to right format
    for j in range(len(arruse)):
        for i in range(len(arruse[j])):
                
            temp = arruse[j][i]
            
            try:
                tempnext = arruse[j][i + 1]
                tempnext = tempnext[0].split()
                maxval = False
            except:
                maxval = True

            masterdict[float(temp[0])] = [temp[0], temp[1], temp[2], temp[3]]
            ordering.append(float(temp[0]))
    
            
    for item in timestamps:
        try:
            c = find_lt(ordering, item)
            orderedtime.append(c)
            points.append(ordering.index(c))
        except:
            pass

        
    for i in range(0, len(points)-1):
        
        for k in range(points[i], points[i+1]):
            cur = ordering[k]
            dictofarrs[order[i]].append(masterdict[cur])
                
    
    
    try:
        os.mkdir(slocat)
    except FileExistsError:
        pass
    
    for key in totaltasks:
        
        try:
            os.makedirs(slocat+ '/' + str(key) + '/')

        except:
            pass
    
    for key in totaltasks:
        conv_arr_file(dictofarrs[key], slocat+ '/' + str(key) + '/' + str(key) + '.csv')
        
        
def refine_code(userid, rno, totaltasks):
    #refine_code_muse(userid, rno, totaltasks)
    refine_code_blue(userid, rno, totaltasks)
    

    
if __name__ == "__main__":
    
    uname = sys.argv[1]
    rno = sys.argv[2]
    
    i = 3
    totaltasks = {}
    try:
        while True:
            totaltasks[sys.argv[i]] = sys.argv[i + 1]
            i += 2
    except:
        pass
    
    print('totaltasks: ' + str(totaltasks))
                
    refine_code(uname, rno, totaltasks)
