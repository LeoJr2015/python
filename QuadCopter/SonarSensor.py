import math

class SonarAltimeter:
    def __init__(self):
        self.pitch = 0.0
        self.roll = 0.0

    def set_attitude(self,attitude):
        self.pitch, self.roll = attitude
        self.pitch = math.radians(self.pitch)
        self.roll = math.radians(self.roll)

    def print_attitude(self):
        print (math.degrees(self.pitch),math.degrees(self.roll))

    def set_range(self,sonar_range):
        self.range = sonar_range

    def get_altitude(self):
        return math.cos(self.pitch)*math.cos(self.roll)*self.range


if __name__ == "__main__":
    import pylab
    from numpy import *
    altitude1 = []
    altitude2 = []

    a = SonarAltimeter()
    a.set_range(10.0)

    for angle in range(0,90):
        a.set_attitude((angle,0.0))
        #a.print_attitude()
        altitude1.append(a.get_altitude())

    a.set_range(11.0)

    for angle in range(0,90):
        a.set_attitude((angle,0.0))
        #a.print_attitude()
        altitude2.append(a.get_altitude())

    alt = array(altitude1)
    alt2 = array(altitude2)
    diff = alt2 - alt
    pylab.plot(alt,'b*-')
    pylab.plot(alt2,'g*-')
    pylab.plot(diff,'r-')
    pylab.show()
