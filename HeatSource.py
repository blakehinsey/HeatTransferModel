# -*- coding: utf-8 -*-
import numpy as np
class HeatSource:
    'Heat source for heat transfer model'

    def __init__(self,rate):
        #This is the init, init
        self.rH = 0
        self.rHLast = 0
        self.tOffset = 0
        self.rate = rate
        self.BHeatLast = 0
        self.state = 0 # 0: 0ff, 1: rising, 2: high, 3: falling


    def update(self,t,BHeat):
        if BHeat > self.BHeatLast:
            self.tOffset = t # hold the start time
            self.state = 1

        elif BHeat < self.BHeatLast:
            # at the falling edge, take the time and set direction -1
            self.tOffset = t #if the last state was saturated set the time to 0
            self.state = 3

#Next steps:
# If the ratio is rising or falling, and the next state is the opposite state (going from rising to falling etc)
# set an additional time parameter to shift the waveform to 1 period
# may need to rewrite the cos function to make this easier to shift between rising and falling
# may also need to define a tShift paramter which is included in the trig function and added to the rate in the conditions
# to ensure when the time reaches the end of the period it goes to zeros
# it really woud help to draw this on paper.....

        if self.state == 1:
            if (t - self.tOffset) < self.rate:
                self.rH = (1 - np.cos((np.pi * (t+self.tOffset)) / self.rate)) / 2
            else:
                self.rH = 1
                self.state = 2

        elif self.state == 3:
            if (t - self.tOffset) < self.rate:
                self.rH = (1 + np.cos((t - self.tOffset) * np.pi / self.rate)) / 2 #Still need to revise this line
            else:
                self.rH = 0
                self.state = 0


        self.BHeatLast = BHeat
        self.tLast = t

        return self.rH
