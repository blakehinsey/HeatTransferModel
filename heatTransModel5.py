# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 15:22:05 2016

@author: blakehinsey
Function based heat transfer model
Heat source is either on or off - use this to characterise the heat transfer coefficients for the model
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# Constants - high certainty
ms = 30 # water mass [kg]
A = .4137 # area of tank [m^2]
Cp = 40 # heat capacity of water [J / (kg K)] - need to verify this value

# Need to optimise these
U = 9 # heat transfer coefficient of tank [W / (m^2 K)]
Qin = 25 # heat source input [W] #relatively known, may need to adjust "efficiency"
tauQin = 500 # time constant of heating element

# States of the system - need to measure
Ta = 15+273 # ambient temperature [K]
T0 = 15+273 # initial water temperature


# First order differential equation
# T'(t) = 1/(ms*CP) * Qin + (U*A)/(ms*Cp)*Ta - (U*A)/(ms*CP)*Ts
KQin = Qin / (ms * Cp)
KTa = (U * A) / (ms * Cp)
KTs = -(U * A) / (ms *Cp)
# dT'(t) = KQin * Qin + KTa * Ta + KTs * T(t);

rInput=([])
tModelOut=([])
#the method above is a bit of a hack... using append to top up the lists

t = np.arange(0,60*60,10);

def heatTrans(T, t, KQin, KTa, KTs):
    # Qin has a time function for turn on
    rKQin= (1-sp.exp(-t/tauQin)); #Time function for Qin
    dTdt = KQin * rKQin + KTa*Ta + KTs*T

    rInput.append(rKQin)
    tModelOut.append(t)

    return dTdt

sol = odeint(heatTrans,T0,t,args=(KQin,KTa,KTs),hmin=0.1,hmax=.1);
TModelOut = np.reshape(sol,len(sol))


plt.figure()
plt.subplot(211).plot(t,sol-273)
axes = plt.gca()
axes.set_ylim([15,25])
axes.set_ylabel("Temperature")
plt.subplot(212).plot(tModelOut,rInput)
axes = plt.gca()
axes.set_ylim([0,1.2])
axes.set_ylabel("rHeater Control")

plt.show()
