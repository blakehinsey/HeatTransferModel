# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp

class HeatSource:
    'Heat source for heat transfer model. This heat source has its own simple control strategy.'

    def __init__(self,TTarget):
        self.TTarget = TTarget
        self.BHeat = 0
        self.BHeatLast = 0
        self.tOn = 0

    def update(self,t,T): #is update too generic name?
        # Simple Control strategy
        self.TErrCont = self.TTarget-T;
        if self.TErrCont > .5:
            self.BHeat= 1
        elif self.TErrCont < -.5:
            self.BHeat = 0;

        #should always use self. or okay to assign to self later?



        if (self.BHeat - self.BHeatLast) > 0:
            self.tOn = t;
        elif (self.BHeat - self.BHeatLast < 0):
            self.tOn = t;

        self.BHeatLast = self.BHeat;

        if self.BHeat == 1:
            tHeat = t-self.tOn;
        if self.BHeat == 0:
            tHeat = np.max([200-(t-self.tOn),0])

        self.rControl = np.max([(1-sp.exp(-tHeat/50)),0])

        return self.rControl

    def getErr(self):
        return self.TErrCont

    def getBHeat(self):
        return self.BHeat
