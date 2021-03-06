# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 07:17:09 2016

@author: blakehinsey
Model Type 4

Simple heat transfer model
A volume subject to ambient conditions and a heat source.
This version of the heat control is simply turn on heater if below threshold
or turn off when above threshold
There is an exponential ramp up/down of the heat source otherwise the solver will trip
Need to take into acount the derivative of the error... PID next.

"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from HeatSourceOld import HeatSource


# Constants
ms = 30 # water mass [kg]
Cp = 40 # heat capacity of water [J / (kg K)]
Qin = 25 # heat source input [W]
U = 9 # heat transfer coefficent of tank [W / (m^2 K)]
A = .4137 # area of tank [m^2]
Ta = 15+273 # ambient temperature [K]
T0 = 20+273 # initial water temperature

# Controller Input
TTarget = 21+273

# First order differential equation
# T'(t) = 1/(ms*CP) * Qin + (U*A)/(ms*Cp)*Ta - (U*A)/(ms*CP)*Ts
KQin = Qin / (ms * Cp)
tauQin = 500
KTa = (U * A) / (ms * Cp)
KTs = -(U * A) / (ms *Cp)
# dT'(t) = KQin * Qin + KTa * Ta + KTs * T(t);

MyHeatSource = HeatSource(TTarget) #initi heat source

def heatTrans(T, t, KQin, KTa, KTs,TTarget):
    rControl = MyHeatSource.update(t,T)
    """
    #Qin has a time function for turn on
    rKQin= (1-sp.exp(-t/tauQin)); #Time function for Qin
    dTdt = KQin * rKQin + KTa*Ta + KTs*T
    """
    dTdt = KQin*rControl + KTa*Ta + KTs*T
    return dTdt

t = np.arange(0,60*60,10);
TTargetArray = TTarget*np.ones(len(t))

sol = odeint(heatTrans,T0,t,args=(KQin,KTa,KTs,TTarget),hmin=0.1,hmax=.1);
TModelOut = np.reshape(sol,len(sol))
TError = (TModelOut - TTargetArray)

"""
Plotting and Data Analysis
"""

plt.figure()
plt.subplot(211).plot(t,TModelOut-273,t,TTargetArray-273,'--')
axes = plt.gca()
axes.set_ylim([15,25])
axes.set_ylabel("Temperature")
plt.subplot(212).plot(t,TError,t,np.zeros(len(t)),'--')
axes = plt.gca()
axes.set_ylim([-3,3])
axes.set_ylabel("TErrorControl")
plt.show()

Tmin = np.min(TModelOut)-273
Tmax = np.max(TModelOut)-273
Tmean = np.mean(TModelOut)-273
Tstdev = np.std(TModelOut)
print("Min: %0.1f" % Tmin, "Mean: %0.1f" % Tmean, "Max: %0.1f" % Tmax, "Stdev: %0.1f"% Tstdev)


"""
PID Controller Testing
"""

from PIDController import PIDController

MyPID = PIDController(1,0,1)
MyPID.set_SP(273+21)

PID_output = np.zeros(len(TModelOut))
PID_err = np.zeros(len(TModelOut))
PID_P = np.zeros(len(TModelOut))
PID_I = np.zeros(len(TModelOut))
PID_D = np.zeros(len(TModelOut))
 # return [PID_out, self.Err, self.P_val, self.D_val, self.I_val]

for i in range(len(TModelOut)):
    PID_output[i], PID_err[i], PID_P[i], PID_I[i], PID_D[i] = MyPID.update(TModelOut[i])

plt.figure()
plt.subplot(511).plot(PID_output)
axes = plt.gca()
axes.set_ylabel("PID")
plt.subplot(512).plot(PID_err)
axes = plt.gca()
axes.set_ylabel("Error")
plt.subplot(513).plot(PID_P)
axes = plt.gca()
axes.set_ylabel("P")
plt.subplot(514).plot(PID_I)
axes = plt.gca()
axes.set_ylabel("I")
plt.subplot(515).plot(PID_D)
axes = plt.gca()
axes.set_ylabel("D")

print("Qin:", Qin)

"""
Need to understand getting data from the class - what is returned when i MyPID.getSP and MyPID.SetSP
Search getting and setting information in class

Determine the difference in tModelOut and t - why factor of 10?
"""
