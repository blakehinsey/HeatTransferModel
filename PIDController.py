# -*- coding: utf-8 -*-
class PIDController:
    'This is a PID controller'
    'Took the example from http://code.activestate.com/recipes/577231-discrete-pid-controller/'
    
    def __init__(self,Kp,Ki,Kd):
        #This is the init
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.SP = 0 #the setpoint
        self.Err = 0 #current error
        self.Int = 0 #current integral
        self.Der = 0 #current derivative
    
    def update(self,current_value):
        #Evaluate the PID
        self.Err = self.SP - current_value
        
        self.P_val = self.Kp * self.Err
        
        self.D_val = self.Kd * (self.Err - self.Der)
        self.Der = self.Err
        
        self.Int = self.Int + self.Err
        self.I_val = self.Int * self.Ki
        
        PID_out = self.P_val + self.I_val + self.D_val
        return [PID_out, self.Err, self.P_val, self.I_val, self.D_val]
    
    def set_SP(self,SP):
        #Reset the set point and reset rolling deriv and integral
        self.SP = SP 
        self.Der = 0
        self.Int = 0

    def getErr(self):
        return self.Err
    
    def getP_val(self):
        return self.P_val
        
    def getI_val(self):
        return self.I_val
        
    def getD_val(self):
        return self.I_val
        
    def getSP(self):
        return self.SP