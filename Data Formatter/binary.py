"""binary"""
import binascii

data = "235b34125623"
s = "235b"
a = []

for i in range(len(s)/2):
    print i, " - ", s[i:i+2]

print data

for i in range(len(data)):
    print data[i]

print binascii.unhexlify(data)

print map(ord, data)
