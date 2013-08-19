import re
import os
import csv
from time import localtime,strftime

FTI_FILE_HEADER= \
""";FTI Report
;Interfaces   Internal/External
;Author       Author
;Version      Version
;Date         %s \n\n""" % (strftime("%d %b %Y %H:%M:%S", localtime()))


def Process(File_Name,Symbols):
    file = open(File_Name)
    fields = []
    entries = 0

    for line in file:
        current_line = line.strip()+"\n",

        if (current_line[0][0]=="_"):
            if (current_line[0].find(".")<0):

                #print current_line[0]
                csv = current_line[0].replace('\t',',').replace(' ',',').replace('\n','')
                field = csv.split(',')
                if field[0] in Symbols:
                    fields.append(field)
                    entries += 1
                #break
    print entries, " Symbols Found"
    return fields

def outputCSV(outputfile,data):
    exportfile = open(outputfile,'w')
    count = 0

    exportfile.write(FTI_FILE_HEADER)
    
    for row in data:
        #print row,
        #print len(row)
        if len(row) == 3:
            size = int(row[2],16)
            #print row[0],size
            csv_entry = "%-40s, %10s, %5s, %8s \n" % (row[0],row[1]+"00000000","32","FFFFFFFF")
            #csv_entry = row[0]+",\t"+row[1]+",\t"+row[2]+"\n"
            exportfile.write(csv_entry)
            count += 1
    exportfile.close()
    print count, " Entries added"

def loadSymbols(datafile):
    symbolfile = open(datafile)
    symbols = []

    for row in symbolfile:
        symbols.append(row.strip())

    return symbols
        

if __name__ == '__main__':
    symbols = loadSymbols("symbols.txt")


    infile = "SMC00-0000-0000.map"
    outputfile = infile+".csv"
    data = Process(infile,symbols)
    outputCSV(outputfile,data)
    
