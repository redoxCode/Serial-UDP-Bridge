import serial
import fcntl
import os
import socket
from serial.tools import list_ports
import time

#UDP socket settings
socketPort = 5000

#serial communication settings
baudrate = 500000

   
print("          \'x|`\r\n        \'|xx| `          \'|x|\r\n`   \'    |xx|    `   \'    |x|`\r\n         |xx|             |x|\r\n============|===============|===--\r\n~~~~~~~~~|xx|~~~~~~~~~~~~~|x|~~~~~~\n        UDP <--------> Serial\n")


def bytesToStr(inp):
    return inp.decode().rstrip()
def strToBytes(inp):
    inp+="\n"
    return inp.encode()

print("searching serial devices")
ports = list(serial.tools.list_ports.comports())
connections={}
for p in ports:
    port = (str(p).split(" ")[0])
    connection = serial.Serial(port, baudrate, timeout=2)
    if connection.is_open:
        while(connection.read()):
            pass
        connection.write(b'I?\n')
        uid = int(bytesToStr(connection.readline()))
        print("Found valid device with id " + str(uid) + " at " + str(port))
        connections[uid]=connection
    else:
        print("Found unknown device at " + str(port))
        connection.close()
print("found " + str(len(connections)) + " valid devices")


print("starting UDP socket at Port "+str(socketPort))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost', socketPort))
fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)

print("listening...")
addr=""
while 1:
    try:
        data, addr = s.recvfrom(1024)
        data = bytesToStr(data)
        uid = int(data[:data.find(':')])
        connections[uid].write(strToBytes(data[data.find(':')+1:]))
        print(strToBytes(data[data.find(':')+1:]))
    except:
        pass

    for uid in connections:
        if(connections[uid].in_waiting):
            ret = strToBytes(str(uid)+":"+bytesToStr(connections[uid].readline()))
            s.sendto(ret, addr)

