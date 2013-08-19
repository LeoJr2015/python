import struct
message_types = [0,"Status","IMU-Pitch","Altitude"]

def main():
    f = open('C:\Python27\Projects\Binary Reader\data.bin','r')
    data = f.read()
    messages = []
    
    valid = True
    i = 0
    while (i < len(data)):
        message_id = message_types[ord(data[i])]
        message_size = ord(data[i+1])
        if message_size == 1:
            message_data = struct.unpack('b',data[i+2:i+2+message_size])[0]
        if message_size == 2:
            message_data = struct.unpack('>h',data[i+2:i+2+message_size])[0]
        if message_size == 4:
            message_data = struct.unpack('i',data[i+2:i+2+message_size])[0]
        i = i + 2 + message_size
        messages.append((message_id,message_size,message_data))
    process_messages(messages)


def process_messages(messages):
    for message in messages:
        id,size,data = message
        print id, size, data       


if __name__ == "__main__":
    main()
    raw_input("Press Enter to continue")
