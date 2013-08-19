import csv
import sys

#input = "RIU_CT_AIWS433.cmd"
if len(sys.argv)==1:
    input = "RIU_CT_AIWS.cmd"
else:
    input = sys.argv[1]
    
list = []

in_file = open(input)
reader = csv.reader(in_file,delimiter='"')

for row in reader:
    if "AIWS " in row:
        file = row[1]
        #print file
        file_name = file[0:(file.find(';'))]
        file_rev = file[(file.find(';')+1):len(file)]
        #print "%s , %s" % (file_name,file_rev)
        list.append([file_name,file_rev])

output_file = input + ".csv"

out_file = open(output_file,'wb')
writer = csv.writer(out_file,delimiter=',')

for row in list:
    writer.writerow([row[0],row[1]])

out_file.close()

        
