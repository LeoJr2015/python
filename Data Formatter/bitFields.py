import csv

def splitBinary(hex,size=8):
    lst = []
    #Round the size up to a multiple of 8
    if (size % 8):
        size = size + (8 - size % 8)
    binary = bin(int(hex,16))[2:]
    for char in binary:
        lst.append(char)
    while (len(lst)<size):
        lst = ['0'] + lst
    return lst

class bitField:
    def __init__(self,type):
        self.bits = []
        self.bits = type
        self.data = []
    def get_r(self):
        for i in range(len(self.bits)):
            print "%10s | %5s" % (self.bits[i],self.data[i])
    def add_data(self,data):
        #The size of the bitfield should be 4x the length of hex characters
        #For example 0xA (1 character) is 0b1010 (4 characters)
        #0xAA (2 characters) is 0b10101010 (8 Characters)
        size = (len(data)*4)
        #print int(size)
        self.data = splitBinary(data,size)
        while (len(self.bits)<len(self.data)):
            self.bits = ['#'] + self.bits

if __name__ == "__main__":
    field = bitField(['Bit 7','Bit 6','Bit 5','Bit 4','Bit 3','Bit 2','Bit 1','Bit 0'])
    field.add_data('00AA')
    field.get_r()

    #print splitBinary("00AA")

    
