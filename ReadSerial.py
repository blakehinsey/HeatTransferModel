# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 21:55:21 2016

@author: blakehinsey
"""
import serial
import numpy as np
import matplotlib.pyplot as plt

#with serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=10) as ser:
#    ser.readline()   # read a '\n' terminated line


data = [] #contains the raw data
time = []
TAmb = []
T1 = []
T2 = []

with serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=6) as ser:
    for i in range(0,5):
        
        line_temp = ser.readline()   # read a '\n' terminated line
        str_temp = str(line_temp)
        #split_temp = str_temp.split("b'")[1].split("\\")[0].split(",") 
        data.append(str_temp.split("b'")[1].split("\\")[0].split(","))
        print(data[i])
        
        if i > 0:
            time.append(data[i][0])
            TAmb.append(data[i][1])
            T1.append(data[i][2])
            T2.append(data[i][3])
        plt.plot(time,TAmb)
        i = i+1
