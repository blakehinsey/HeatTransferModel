def TempControl(t,T,TTarget):
    global BStateLast;
    
    TError = TTarget-T;
    
    if TError > 0:
        BState = 1;

    if (BState - BStateLast) > 0:
        tOn = t;
        
    if TError < 0:
        BState = 0;
    
    if (BState - BStateLast < 0):
        #Falling edge, need to change the sign of the rControl shape
        print("State has gone low at", t, "seconds")
    rControl = (1-sp.exp(-(t-tOn)/500))
        
        
    BStateLast = BState;
    return rControl
        #rKQin= (1-sp.exp(-t/tauQin))