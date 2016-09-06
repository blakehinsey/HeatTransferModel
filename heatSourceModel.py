# -*- coding: utf-8 -*-
class heatSource:
    'This is a PID controller'
    'Took the example from http://code.activestate.com/recipes/577231-discrete-pid-controller/'
    
    def __init__(self,magnitude,response,start_state):
        #This is the init
        self.t = 0;
        #code to check that start state is 1 or 0
        self.state = start_state
        self.rValue = start_state #ratio of peak signal
    
    def update(self,new_state,t):
        #just hack the example from heat trans model using a state change to trigger

    #dont forget to return something