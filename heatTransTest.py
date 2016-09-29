# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 17:45:08 2016

@author: blakehinsey
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

t = np.arange(0,100,1);

BHeat = np.zeros(len(t))
for i in range(len(BHeat)):
    if i > 20:
        BHeat[i] = 1
    if i > 60:
        BHeat[i] = 0
HOutTest = np.zeros(len(t))


from HeatSource import HeatSource
MySource = HeatSource(20)



for i in range(len(t)):
    HOutTest[i] = MySource.update(t[i],BHeat[i])
plt.plot(HOutTest)
plt.show()
