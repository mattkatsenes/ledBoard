'''
@author Olivia

This is a file for you to put use to build functions on our LED library. Did this work? Hello!
'''
import led
#it has an issue with import serial in led
import cv2 
import random
import time
import math

def halfScreen(aboard):
    for led in aboard.stringOfLights:
        if(led.x > aboard.width/2):
            led.setColor(200,0,0)
        else:
            led.setColor(100,0,100)

#m and b are variables from y=mx+b 
#color variables should be arrays [r,g,b]
def line(aboard, b, m, topColor, botColor):
    for led in aboard.stringOfLights:
        if led.x > (((-1 * m) * led.y) + b):
            led.setColorArr(topColor)
        else:
            led.setColorArr(botColor)

#color variables should be arrays [r,g,b]
#frames are the amount of frames in the animation
def spiral(aboard, topColor, botColor, frames):
    for i in range(frames):
        m = i / (1-(i/50))
        b = (m*(0-1)*(aboard.width/2))+(aboard.height/2)
        line(aboard,b,m,topColor,botColor)
        aboard.show()

def distance(point1, point2):
    return math.sqrt(abs(((point2[0] - point1[0])**2) + ((point2[1] - point1[1])**2)))

#If this doesn't work, switch height and width
#point is [x,y], color is [r,g,b]
def spreadOutFrom(point, aboard, color, frames):
    if(point[0]>aboard.width/2):
        if(point[1]>aboard.height/2):
            max = distance([0,0],point)
        else:
            max = distance([0,aboard.height],point)
    else:
        if(point[1]>aboard.height/2):
            max = distance([aboard.width,0],point)
        else:
            max = distance([width,height],point)
    increment = max / frames
    dist = 0
    for i in range(frames):
        for led in aboard.stringOfLights:
            dist = dist + increment
            if(distance(point, [led.x,led.y]) < dist):
                led.setColorArr(color)
        aboard.show()
            
def snowfall(aboard):
    print()


# wave = cv2.imread('../assets/wavy-stripes-2.jpg')
# myBoard = led.LedBoard(200, wave.shape[0], wave.shape[1])
# spiral(myBoard, [0,200,0], [0,0,200], 48)
# cv2.imshow('test', wave)
# k = cv2.waitKey(0)
# if k ==27 or k == ord('q'):
#     cv2.destroyAllWindows()
