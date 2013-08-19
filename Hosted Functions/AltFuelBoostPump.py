class AltFuelBoostPump:
    def __init__(self):
        self.inputs = []
        self.inputs.append(HF_DiscreteIO('l_alt_pump_selected','On','Off','Off'))
        self.inputs.append(HF_DiscreteIO('l_alt_pump_valid','Valid','Invalid','Invalid'))
        self.outputs = {'ALT FUEL PUMP L Command':'Open'}
        
    def getSSPCState(self):
        if ((self.inputs[0].getState()=="On") and (self.inputs[1].getState()=="Invalid")):
            self.outputs['ALT FUEL PUMP L Command'] = "Close"
        else:
            self.outputs['ALT FUEL PUMP L Command'] = "Open"
        return self.outputs['ALT FUEL PUMP L Command']

class HF_DiscreteIO:
    def __init__(self,ID,ActiveState=True,InactiveState=False,DefaultState=False):
        self.input_name = ID
        self.ActiveState = ActiveState
        self.InactiveState = InactiveState
        self.CurrentState = DefaultState
    def __str__(self):
        return self.input_name+" : "+self.CurrentState
    def setInput(self,State):
        if isinstance(State,basestring):
            if (State == self.ActiveState):
                self.CurrentState = State
            if (State == self.InactiveState):
                self.CurrentState = State
        else:
            if (State):
                self.CurrentState = self.ActiveState
            else:
                self.CurrentState = self.InactiveState
    def getState(self):
        return self.CurrentState

if __name__ == '__main__':
    HF1 = AltFuelBoostPump()
    for i in HF1.inputs:
        print i
    HF1.inputs[0]

    
