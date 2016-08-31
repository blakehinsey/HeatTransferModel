# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 07:17:09 2016

@author: blakehinsey
Model3
Qin is a function of time - this allows modelling of heater response
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt


#first order differential equation

#Constants
ms = 30; #water mass [kg]
Cp = 40; #heat capacity of water [J / (kg K)]
Qin = 30; #heat source input [W]
U = 12; #heat transfer coefficent of tank [W / (m^2 K)]
A = .25; #area of tank [m^2]
Ta = 20+273; #ambient temperature [K]
T0 = 19+273; #initial water temperature

#Controller Input
TTarget = 21+273;

# First order differential equation
# T'(t) = 1/(ms*CP) * Qin + (U*A)/(ms*Cp)*Ta - (U*A)/(ms*CP)*Ts
KQin = Qin / (ms * Cp);
tauQin = 500;
KTa = (U * A) / (ms * Cp);
KTs = -(U * A) / (ms *Cp);
#dT'(t) = KQin * Qin + KTa * Ta + KTs * T(t);

global BHeatLast, tOn, BHeat
BHeatLast = 0;
BHeat= 0;
tOn = 0;

rControlOut=([])
tOut =([])
BHeatOut = ([])
TErrOut =([])

def heatTrans(T, t, KQin, KTa, KTs,TTarget):
    global BHeatLast
    global BHeat
    global tOn
    
    #Simple Control strategy
    TErrCont = TTarget-T;
    if TErrCont > .5:
        BHeat= 1;
    elif TErrCont < -.1:
        BHeat = 0;
        
    if (BHeat - BHeatLast) > 0:
        tOn = t;    
    elif (BHeat - BHeatLast < 0):
        tOn = t;

    BHeatLast = BHeat;
    
    if BHeat == 1:
        tHeat = t-tOn;
    if BHeat == 0:
        tHeat = np.max([200-(t-tOn),0])
        

        
    rControl = np.max([(1-sp.exp(-tHeat/50)),0])
    
    tOut.append(t)
    TErrOut.append(TErrCont)
    rControlOut.append(rControl)
    BHeatOut.append(BHeat)

    #print("BState", BState,"tOn",tOn,"rControl", rControl)
    
    #KQin function of T 1-sp.exp(-t/5)
    #BHeater controls heat input, on or off.
    
    """
    #Qin has a time function for turn on
    rKQin= (1-sp.exp(-t/tauQin)); #Time function for Qin
    dTdt = KQin * rKQin + KTa*Ta + KTs*T
    """
    dTdt = KQin*rControl + KTa*Ta + KTs*T
    return dTdt

t = np.arange(0,60*60,10);
    

from scipy.integrate import odeint
sol = odeint(heatTrans,T0,t,args=(KQin,KTa,KTs,TTarget),hmax=5);
TModelOut = np.reshape(sol,len(sol))

TTargetArray = TTarget*np.ones(len(t))
TError = (TModelOut - TTargetArray)

plt.figure()
plt.subplot(311).plot(t,sol-273,t,TTargetArray-273)
axes = plt.gca()
axes.set_ylim([15,25])
plt.subplot(312).plot(tOut,TErrOut,tOut,np.zeros(len(tOut)))
plt.subplot(313).plot(tOut,rControlOut,tOut,BHeatOut)
axes = plt.gca()
axes.set_ylim([0,2])


