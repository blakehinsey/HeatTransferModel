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
Ta = 15+273; #ambient temperature [K]
T0 = 15+273; #initial water temperature

# First order differential equation
# T'(t) = 1/(ms*CP) * Qin + (U*A)/(ms*Cp)*Ta - (U*A)/(ms*CP)*Ts

KQin = Qin / (ms * Cp);
tauQin = 500;
KTa = (U * A) / (ms * Cp);
KTs = -(U * A) / (ms *Cp);
#dT'(t) = KQin * Qin + KTa * Ta + KTs * T(t);

def heatTrans(T, t, KQin, KTa, KTs,tauQin):
    #KQin function of T 1-sp.exp(-t/5) - to simulate response of heater
    #measuring the contact temperature of heater can indicate response of heater
 
    rKQin= (1-sp.exp(-t/tauQin)); #Time function for Qin
    dTdt = (KQin * rKQin) + KTa*Ta + KTs*T
    
    return dTdt

t = np.arange(0,60*60,10);
    

from scipy.integrate import odeint
sol = odeint(heatTrans,T0,t,args=(KQin,KTa,KTs,tauQin))-273;
TModelOut = np.reshape(sol,len(sol))

TTarget = 22*np.ones(len(t))
TError = (TModelOut - TTarget)
iMin = np.argmin(TError)

plt.figure()
plt.subplot(211).plot(t,sol,t,TTarget)
axes = plt.gca()
axes.set_ylim([10,30])
plt.subplot(212).plot(t,TError,t,np.zeros(len(t)))

