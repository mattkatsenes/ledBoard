import cv2
import numpy as np
import time
import sys
import serial


#call this script with arguments like this.. change filepath each time.
# python3 populate_board.py "../boardMaps/test.map"
# python3.11 populate_board.py "../boardMaps/test.map"
def main():
    #some constants
    NUM_LEDs = 50
    DELAY = 0.8 #delay between lighting LEDs [seconds]
    FILE = "../boardMaps/test.map"  #filepath to output LED positions
    THRESHOLD = 100 #value below this probably isn't a LED.
    SERIAL_PATH = "/dev/tty.HC-05-SPPDev"
    
    #grabbing command line argument for filepath
    args = sys.argv[1:]
    
    if(len(args) == 1):
        FILE = args[0]

    #to remind us to change this constant
    print("looking for " + str(NUM_LEDs) + " leds")

    #start up the bluetooth serial interface:
    bt = serial.Serial(SERIAL_PATH,9600,timeout=.5)
    print("serial initialized on ",bt.name)
    
    cap = cv2.VideoCapture(0)
    
    lightPositions = [] #list of x,y positions for lights.
    begun = False
    firstSeen = False
    
    while True:
        # cap.read() returns 2 values, boolean stored as ret, and frame (the image array)
        ret, frame = cap.read()

        # attempt to read light number from bluetooth serial
        lightOn = -1 #will store the number of thelight (transmitted in one byte or two if >255)
        
        #grab the information off the bluetooth device?
        if bt.in_waiting:
            bt_input = bt.readline()
            #print('raw: ',bt_input)
            #print('decoded: ',bt_input.decode())
            lightOn = int(bt_input.decode())
            #print("turning on: ",lightOn)
            #print("we already have: ",len(lightPositions))
            
                
        #mess with bounds here to manually crop to the right-ish size.
        #cropped = frame[10:600, 200:1000]
        
        #flip horizontal to deal with up/down issues when turning computer sideways 
        cropped = cv2.flip(frame,1)
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)  
        
        
        #the (41,41) defines the radius of the gaussian blur, the last one is a flag on how to treat borders
        blur = cv2.GaussianBlur(gray, (41, 41), cv2.BORDER_DEFAULT)

        #find the brightest spot (and least bright spot)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)
        
        if not begun:
            #draw BLUE circle around brightest spot for testing
            cv2.circle(cropped, maxLoc, 30, (255, 0, 0), 10)
            cv2.imshow('cropped', cropped)
            
            #useful for manual calibration with flashlight.
            print(maxLoc)
            
            if cv2.waitKey(1) == ord('a'):
                #start the process by pressing 'a'
                begun = True
                bt.write("start".encode())

        elif lightOn > -1:
            if(maxVal > THRESHOLD):
                #draw RED circle on brightest spot
                cv2.circle(cropped, maxLoc, 30, (0, 255, 0), 10)

                #send back the number of the light we think we're mapping...
                bt.write(str.encode(str(len(lightPositions))))

                #adding a brightness value to the x/y coordinates.  Helps decide which measurement to use.
                maxLoc = list(maxLoc)
                maxLoc.append(int(maxVal))
            
            
                
            else:
                # can't find a bright enough spot.  Declare failure.
                maxLoc = (0,0)
            
                bt.write("fail".encode())
                
                #draw WHITE circle around (0,0)
                cv2.circle(cropped, maxLoc, 30, (255, 255, 255), 10)

                maxLoc = [0,0,-1]


            # check we haven't missed a light somewhere
            assert(len(lightPositions) == lightOn)
        
            # add the data to our list of light positions
            lightPositions.append(maxLoc)
        
        cv2.imshow('cropped', cropped)
            
        '''    
        elif not firstSeen:
            if maxVal > THRESHOLD:
                firstSeen = True
                
                cv2.circle(cropped, maxLoc, 30, (0, 255, 0), 10)
                cv2.imshow('cropped', cropped)
            
                # this adds information about reliability
                # a bright light is likely in the right place
                # a dim light may be an error.
                # we will use the brightest lights for position data.
                maxLoc = list(maxLoc)
                maxLoc.append(int(maxVal))
                
                lightPositions.append(maxLoc)
                
                print (maxLoc)
                lastLedTime = time.time()
                
        elif begun and time.time()-lastLedTime >= DELAY and maxVal > THRESHOLD:
            
            #draw RED circle around brightest spot for testing
            cv2.circle(cropped, maxLoc, 30, (0, 0, 255), 10)
            cv2.imshow('cropped', cropped)
            
            
            # this adds information about reliability
            # a bright light is likely in the right place
            # a dim light may be an error.
            # we will use the brightest lights for position data.
            maxLoc = list(maxLoc)
            maxLoc.append(int(maxVal))
            
            lightPositions.append(maxLoc)
            
            print (maxLoc)
            
            #take snapshot
            lastLedTime = time.time()
            
            
        elif time.time()-lastLedTime >= DELAY*1.1:
            #time has elapsed and we have'nt found a light (it's on the other side of the tree)
            
            maxLoc = (0,0)
            #draw WHITE circle around brightest spot for testing
            cv2.circle(cropped, maxLoc, 30, (255, 255, 255), 10)
            cv2.imshow('cropped', cropped)
            
            maxLoc = [0,0,-1]
            
            lightPositions.append(maxLoc)
            
            print (maxLoc)
            lastLedTime = time.time()
        
        '''
        
            
        
        
        if cv2.waitKey(1) == ord('q') or len(lightPositions) == NUM_LEDs:
            #end process when we have the required number of LEDs or someone presses q
            break
    
    cap.release()
    
    print(lightPositions)
    
    #open a file and write the contents of lightPositions
    #to be used in led.py
    #BUG!!! somehow, this set the dimensions BACKWARDS in the first line, 
    #as compared with the rest of the lines.
    #Right now, you must fix manually 
    with open(FILE, "w") as output:
        # #puts the image dimensions at the beginning of the list.
        # output.write(','.join(str(x) for x in cropped.shape))
        # output.write("\n")
        
        for position in lightPositions:
            output.write('[')
            output.write(', '.join(str(x) for x in position))
            output.write(']')
            output.write("\n")
    
if __name__ == '__main__':
    main()
