scale = 0.1
max = 2000
min = 1000

def Motors(throttle,pitch):
    delta = (1500 - pitch) * scale
    motor1 = throttle + delta
    motor2 = throttle - delta
    print "(%04i,%04i)\n" % (motor1,motor2)



if __name__ == '__main__':
    Motors(1000,1500)
    Motors(1000,1400)
    Motors(1000,1600)
    Motors(1000,1000)
    Motors(1000,2000)
    
