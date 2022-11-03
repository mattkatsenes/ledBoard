import serial
import time
from serial.tools import list_ports


SERIAL_PATH = "/dev/tty.HC-05"
#SERIAL_PATH = "/dev/cu.usbserial-14240"


print("Start")

bluetooth=serial.Serial(SERIAL_PATH, 9600)#Start communications with the bluetooth unit
bluetooth.timeout = 1
#time.sleep(10)

print("Connected")

#bluetooth.flushInput() #This gives the bluetooth a little kick

bluetooth.flush()

bluetooth.write("test".encode())

port = list(list_ports.comports())
for p in port:
    print(p)
    # if "Arduino" in p:
    #     SERIAL_PATH = p.device


for i in range(5): #send 5 groups of data to the bluetooth
    print("Ping " + str(i))
    
    bluetooth.write(b"BOOP "+str.encode(str(i)))#These need to be bytes not unicode, plus a number
    
    #print("wrote data")
    
    input_data=bluetooth.readline()#This reads the incoming data. In this particular example it will be the "Hello from Blue" line
    print(input_data.decode())#These are bytes coming in so a decode is needed
    
    time.sleep(0.1) #A pause between bursts

bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
print("Done")