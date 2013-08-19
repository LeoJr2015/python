#!/usr/bin/env python
class TextStarSim:
    def __init__(self):
        self.screen = []
        self.line = 0
        self.col = 0
        self.window = 0
        for i in range(0,16):
            self.screen.append([])
            for j in range(0,16):
                self.screen[i].append(" ")
    def print_screen(self):
        print (self.line,self.col), "Screen:",self.window/2
        #print "#0123456789ABCDEF#"
        print "##################"
        print "#%s#" % "".join(self.screen[self.window]).ljust(16)
        print "#%s#" % "".join(self.screen[self.window+1]).ljust(16)
        print "##################"
    def write(self,data):
        #for i in range(len(data)):
        i = 0
        while i < len(data):
            #print self.line, self.col, data[i]
            if self.col >15:
                #print "New Line"
                self.col = 0
                self.line += 1
            elif self.line >= 15:
                self.col = 0
                self.line = 0
            
            if ord(data[i]) == 254:
                if ord(data[i+1]) == 80: #Position Cursor
                    self.setcursor(ord(data[i+2]),ord(data[i+3]))
                    i += 4
                elif ord(data[i+1]) == 83: #Clear Screen
                    for x in range(0,16):
                        for y in range(0,16):
                            self.screen[i][j] = " "
                    i += 1
                elif ord(data[i+1]) == 98: #BarGraph
                    width = ord(data[i+2])
                    percent = (ord(data[i+3]))
                    self.blocks = "*" * int(float(width)*(float(percent)/100))
                    self.write(self.blocks)
                    i += 4
                elif ord(data[i+1]) == 71: #GoToLine
                    self.line = ord(data[i+2])
                    self.col = 0
                    i += 3
                elif ord(data[i+1]) == 79: #ScrollWindow
                    direction = ord(data[i+2])
                    if direction == 1:
                        self.window += 2
                    else:
                        self.window -= 2
                    if self.window < 0:
                        self.window = 14
                    elif self.window > 14:
                        self.window = 14
                    i += 3
            elif data[i] == '\n': #new line
                self.line += 1
                self.col = 0
                i += 1
            else:
                #if self.col >= 16:
                #    print "New Line2"
                #    self.col = 0
                #   self.line += 1
                self.screen[self.line][self.col] = data[i]
                self.col += 1
                i += 1
            
    def setcursor(self,l,c):
        self.line = l
        self.col = c
                
                

        #self.screen[0] = data

if __name__ == "__main__":
    import struct
    
    tss = TextStarSim()
    tss.print_screen()
    tss.write("Screen 0\n")
    tss.write("Screen 0\n")
    tss.write("Screen 1\n")
    tss.write("Screen 1\n")
    tss.write("Screen 2\n")
    tss.write("Screen 2\n")
    tss.write("Screen 3\n")
    tss.print_screen()
    tss.setcursor(1,1)
    tss.write(struct.pack('BBBB',254,98,16,25))
    tss.write(struct.pack('BBB',254,79,1))#7
    tss.print_screen()
    tss.write(struct.pack('BBB',254,79,1))#6
    tss.print_screen()
    tss.write(struct.pack('BBB',254,79,1))#5
    tss.print_screen()
    tss.write(struct.pack('BBB',254,79,1))#4
    tss.write(struct.pack('BBB',254,79,0))#3
    tss.write(struct.pack('BBB',254,79,0))#2
    tss.write(struct.pack('BBB',254,79,0))#1
    tss.write(struct.pack('BBB',254,79,0))#0
    
    #tss.write(struct.pack('BBBB',254,80,0,0))
    tss.print_screen()
    #tss.write(struct.pack('BB',254,83))
    #tss.print_screen()
