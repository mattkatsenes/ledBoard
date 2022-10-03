#import led  
import cv2
import numpy as np
import time

NUM_LEDs = 5
DELAY = 1 #delay between lighting LEDs
FILE = "../boardMaps/test.map"  #filepath to output LED positions

cap = cv2.VideoCapture(0)

lightPositions = [] #list of x,y positions for lights.
begun = False

while True:
    # cap.read() returns 2 values, boolean stored as ret, and frame (the image array)
    ret, frame = cap.read()
    
    #mess with bounds here to manually crop to the right-ish size.
    cropped = frame[10:600, 200:1000]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)    
    
    height = int(cap.get(4))
    width = int(cap.get(3))
    
    blur = cv2.GaussianBlur(gray, (41, 41), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)
    
    if not begun:
        #draw BLUE circle around brightest spot for testing
        cv2.circle(cropped, maxLoc, 30, (255, 0, 0), 10)
        cv2.imshow('cropped', cropped)
        
        if cv2.waitKey(1) == ord('a'):
            #start the process by pressing 'a'
            begun = True
            lastLedTime = time.time()
        
    elif begun and time.time() - lastLedTime >= DELAY:
        #take snapshot
        lastLedTime = time.time()
        lightPositions.append(maxLoc)
        
        #draw RED circle around brightest spot for testing
        cv2.circle(cropped, maxLoc, 30, (0, 0, 255), 10)
        cv2.imshow('cropped', cropped)
        
        
    
    else:
        #process running, inbetween snapshots
        cv2.imshow('cropped', cropped)
        
    
    
    if cv2.waitKey(1) == ord('q') or len(lightPositions) == NUM_LEDs:
        #end process when we have the required number of LEDs or someone presses q
        break

cap.release()

print(lightPositions)

#open a file and write the contents of lightPositions
#to be used in led.py
with open(FILE, "w") as output:
    output.write(','.join(str(x) for x in cropped.shape))
    output.write("\n")
    for position in lightPositions:
        output.write(','.join(str(x) for x in position))
        output.write("\n")
    

#find the rectangle that is our board:
'''
#this is not going to work - we don't have a clean enough image
board_img = cv2.imread('../assets/board1.jpg')
board_gray = cv2.cvtColor(board_img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(board_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
cv2.imshow('board',board_img)
cv2.imshow('rectangle detection',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''





#paste bin
'''
img = cv2.imread('rectangle.jpg')

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for cnt in cnts:
    approx = cv2.contourArea(cnt)
    print(approx)

cv2.imshow('image', img)
cv2.imshow('Binary',thresh_img)
cv2.waitKey()
'''