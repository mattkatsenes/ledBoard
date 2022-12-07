import serial

bt = serial.Serial("/dev/tty.HC-05",9600,timeout=2)
print("bluetototh open on ",bt.name)
bt.write("testing-school".encode())

data = bt.readline()

print(data)

bt.close()
