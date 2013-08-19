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
    def __init__(self,file,type):
        self.bits = []
        self.reader = csv.reader(open(file))
        for row in self.reader:
            if row[0] == type:
                if type == "":
                    type = "Default"
                self.ID = type
                self.bits = row[1:]
        self.data = []
    def get_r(self):
        for i in range(len(self.bits)):
            print "%10s | %5s" % (self.bits[i],self.data[i])
    def add_data(self,data):
        size = (len(data)*2)
        if size < 8:
            size = 8
        self.data = splitBinary(data,(len(data)*2))
        while (len(self.bits)<len(self.data)):
            self.bits = ['#'] + self.bits

if __name__ == "__main__":
    field = bitField('bitFields.csv','Default')
    field.add_data('A')
    field.get_r()

    #print splitBinary("A")

    
