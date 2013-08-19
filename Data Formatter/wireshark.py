import csv

def WireSharkData(file):
    reader = csv.reader(file,delimiter=' ')
    data = []

    for row in reader:
        if row != []:
            for item in row[2:18]:
                if item != '':
                    data.append(item)
    
    output = ''.join(data)
    return output

if __name__ == "__main__":
    print WireSharkData(open('output.txt'))
    
