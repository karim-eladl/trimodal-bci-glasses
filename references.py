#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 12:20:40 2021
"""


import pandas as pd
import csv
import os
from datetime import date
import numpy as np


#CREATION OF DATA FOLDER
ROOT = "./data"
today = date.today()

try:
    os.mkdir(f"{ROOT}")
except FileExistsError:
    pass

    
 

###############################
#THIS IS THE IMPORTANT FUNCTION
###############################

def conv_arr_file(arr, filename):
    #takes in a 2-D array and converts it to a .csv file
    

    with open(filename,"w+") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(arr)

    
    
    




