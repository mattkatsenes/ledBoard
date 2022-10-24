'''
@author Olivia

This is a file for you to put use to build functions on our LED library. Did this work?
'''
import led
#it has an issue with import serial in led
import cv2 
import random
import time

def halfScreen(aboard):
    for led in aboard.stringOfLights:
        if(led.x > aboard.width/2):
            led.setColor(200,0,0)
        else:
            led.setColor(100,0,100)

def line(aboard, b, m, topColor, botColor):
    for led in aboard.stringOfLights:
        if led.x > (((-1 * m) * led.y) + b):
            led.setColorArr(topColor)
            print("top")
        else:
            led.setColorArr(botColor)
            print("bottom")

def spiral(aboard, topColor, botColor, frames):
    setLedPosition(aboard)
    for i in range(frames):
        b = (aboard.height/2)+i*(aboard.height/frames)*4
        line(aboard,b,2*b/aboard.width,topColor,botColor)
        displayImage(aboard)
        wave = cv2.imread('../assets/wavy-stripes-2.jpg')

def setLedPosition(aboard):
    for led in aboard.stringOfLights:
        led.setPosition(random.randrange(aboard.height), random.randrange(aboard.width))

def displayImage(aboard):
    for index, led in enumerate(aboard.stringOfLights):
        cv2.circle(wave,led.getPosition(), 10, led.getColorBGR(),-1)

# wave = cv2.imread('../assets/wavy-stripes-2.jpg')
# myBoard = led.LedBoard(200, wave.shape[0], wave.shape[1])
# spiral(myBoard, [0,200,0], [0,0,200], 48)
# cv2.imshow('test', wave)
# k = cv2.waitKey(0)
# if k ==27 or k == ord('q'):
#     cv2.destroyAllWindows()
