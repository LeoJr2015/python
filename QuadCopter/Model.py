if __name__ == "__main__":
    print "Starting"
    ##motor_test()
    ##PID_Test()
    print "Done"

class Motor():
    def __init__(self,ID):
        self.ID = ID
        self.power = int(0.0)
    def set_power(self,power):
        self.power = int(power)
    def get_thrust(self):
        if self.power < 1000:
            thrust = 0
        else:
            thrust = (float(self.power)-1000.0) / 1000.0
        return thrust


class Quadcopter():
    """
    Model of a Quadcopter in the Z-axis.

    Example Usage:
    quad = Quadcopter("Model 1",1.0)
    quad.set_motors(1300)
    quad.update_all(delta_time)
    height = quad.height
    """
    def __init__(self,ID,weight,num_motors=4):
        self.ID = ID
        self.weight = float(weight)
        self.climb_rate = 0.0
        self.height = 0.0
        self.motors = []
        self.thrust = 0.0
        for i in range(0, num_motors):
            self.motors.append(Motor(i))
        self.last_update = -1.0
    def set_motors(self,power):
        """
        Set the power of all motors in the system
        """
        for i in range(len(self.motors)):
            self.motors[i].power = power
            #print "Motor %i: %d" % (i, self.motors[i].power)
    def update_thrust(self):
        self.thrust = 0.0
        for i in range(len(self.motors)):
            thrust = self.motors[i].get_thrust()
            self.thrust += thrust
            #print "Motor %i Thrust: %f" % (i,self.thrust)
    def update_climb_rate(self):
        ##acceleration = Force / mass
        rate = ((self.thrust*10) - (self.weight*9.81)) / self.weight
        self.climb_rate = rate
        #print self.climb_rate
    def update_height(self,delta_t):
        delta_h = self.climb_rate * delta_t
        self.height += delta_h
        if self.height <= 0.0:
            self.height = 0.0
        #print "Height: ",self.height
    def update_all(self,delta_t):
        """
        Updates the thrust, climb rate and height of the QuadCopter
        model.
        """
        self.update_thrust()
        self.update_climb_rate()
        self.update_height(delta_t)

def PID_Test():
    import pylab
    from numpy import array
    from PID import PID
    height = []

    quad = Quadcopter("001","1.0")
    height_pid = PID(40.0,0.5,0.0)
    height_pid.set_point = 5.0
##    loop = 0
##    while (loop < 500):
##        control = height_pid.update(quad.height)
##        quad.set_motors(1000+control)
##        quad.update_all(0.02)
##        print control,quad.height
##        loop += 1

    quad.set_motors(1000)
    quad.update_all(1)
    #print quad.height
    #quad.set_motors(1500)
    #quad.update_all(1)
    #print quad.height
    for i in range(0,1000):
        quad.set_motors(height_pid.update(quad.height)+1000)
        quad.update_all(0.01)
        #print quad.height
        height.append(quad.height)

        if i == 500:
            height_pid.set_point = 2.0

    Aheight = array(height)
    pylab.plot(Aheight)
    pylab.show()

def motor_test():
    import pylab
    from numpy import array
    quad = Quadcopter("001","1.0")
    quad.set_motors(1300)

    for i in range(0,500):
        quad.update_all(0.01)
        height.append(quad.height)

    Aheight = array(height)
    pylab.plot(Aheight)
    pylab.show()







