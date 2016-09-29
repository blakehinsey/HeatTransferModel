# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 12:41:23 2016

@author: blakehinsey
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

t = []
TAmb = []
T1 = []
T2 = []
i = 0
with open('measurements/testdata.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        if i > 0:
            t.append(float(row[0]))
            TAmb.append(float(row[1]))
            T1.append(float(row[2]))
            T2.append(float(row[3]))
        i += 1

#plt.plot(t, TAmb, t, T1, t, T2)
#plt.show()


# Low pass filter all the things!
b, a = signal.butter(1, 0.005)
TAmbFilt = signal.filtfilt(b, a, TAmb)
b, a = signal.butter(1, 0.07)
T1Filt = signal.filtfilt(b, a, T1)
T2Filt = signal.filtfilt(b, a, T2)
plt.figure()
plt.plot(t, TAmbFilt, t, T1Filt, t, T2Filt)

TAmbMean = np.mean(TAmbFilt)

T2Max = np.max(T2Filt)
T2Max_i = np.argmax(T2)

T1Norm = np.divide(np.subtract(T1Filt,TAmbFilt),T2Filt)
T1Norm = T1Norm - T1Norm[0]
T1Norm = T1Norm / np.max(T1Norm)
T1NormMax_i = np.argmax(T1Norm)

tT1Peak = t[T1NormMax_i]
tT2Peak = t[T2Max_i]

print('Time for T1 normalised peak', tT1Peak, 'at sample ', T1NormMax_i)

"""
The code for the section above should end here - should only read the data and show some statistics about it

The next step would be to characterise rHeat from the normalised T1 above - some sine and exp function?
    It would be nice to have an optimisation to solve for the coefficients of the mixed function for rHeat

After that, need to pass it on to a function to optimise the heat transfer coefficients
    This will probably look like a function of heatTransModel5 - can pass variables in, initialise the heat source model

Speaking of the heat source model - it would be useful to have a simple heat source model (probably the function will do)
    as the one that is used below. It doesn't need to deal with off/on/off - only ON

Once those parameters are characterised above, then need a simulation of the controller for the temperature control...
bang-bang controller should do the trick considering the response time / inertia of the system
"""

pltrange = 300 # hack number of points to plot based on data

plt.figure()
plt.plot(t[0:pltrange], T1Norm[0:pltrange])
plt.hold(True)


def rHeatSource(t,rate):
    if t < rate:
        rHeat = (1 - np.cos((np.pi * (t)) / rate)) / 2
    else:
        rHeat = 1
    return rHeat

rHeatModel = []

rates_list = [400,500,600,700,800,900]
for rate in rates_list:
    rHeatModelTemp = []
    for time in t[:pltrange]:
        rHeatModelTemp.append(rHeatSource(time,rate))
    rHeatModel.append(rHeatModelTemp)
    plt.plot(t[0:pltrange], rHeatModelTemp, linestyle='dashed')
    del rHeatModelTemp


"""""
from HeatSource import HeatSource

def rHeat

rHeatOut = []
myHeatSource = HeatSource(700) # initialise heat source with x rate
for time in t[:pltrange]:
    rHeatOut.append(myHeatSource.update(time,1))
    print(time)

plt.plot(t[0:pltrange], rHeatOut)

"""
