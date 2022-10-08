'''
@author Mary

This is a file for you to put use to build functions on our LED library. 
'''
import led
import random
import cv2


def stripes(aBoard, r, g, b):
    for led in aBoard.stringOfLights:
        y = led.y
        h = aBoard.height
        if y <= 4/5*h and y>= 3/5*h or y <=2/5*h and y >= 1/5*h:
            led.setColor(r, g, b)
    #aBoard.output('../boards/stripes.board')

wave = cv2.imread('c:/Users/maryc/OneDrive/Desktop/ledBoard/assets/wavy-stripes-2.jpg')


myBoard = led.LedBoard(200,wave.shape[0],wave.shape[1])

for led in myBoard.stringOfLights:
    led.setPosition(random.randrange(myBoard.height),random.randrange(myBoard.width))

stripes(myBoard, 100, 100, 255)
for index, led in enumerate(myBoard.stringOfLights):
    cv2.circle(wave,led.getPosition(),20,led.getColorBGR(),-1)    
cv2.imshow('test',wave)
k = cv2.waitKey(0)
if k == 27 or k == ord('q'):
    cv2.destroyAllWindows()