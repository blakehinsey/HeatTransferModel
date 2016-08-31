# -*- coding: utf-8 -*-

def PIDControl(VIn,VTarget,KList):
    #Where...
    #VIn: input value
    #VTarget: target value
    #KList: constants list ([Kp,Ki,Kd])

    Kp, Ki,Kd = KList;
    
    try:
      ErrLast
    except NameError:
      ErrLast = 0;
            
    try:
      Derivative
    except NameError:
      Derivative  = 0;a
    
    
    
          
        
        
        
return PIDOut