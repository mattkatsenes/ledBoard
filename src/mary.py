'''
@author Mary

This is a file for you to put use to build functions on our LED library. 
'''
from led import *
import led
import random
import cv2
import time

def animateLine(aBoard, i, r, g, b):
    w = aBoard.width
    for led in aBoard.stringOfLights:
        x = led.x
        if x >= i / 100 *w and x <= (i+1) / 100 *w:
            led.setColor(r, g, b)
            #cv2.circle(wave,led.getPosition(),20,led.getColorBGR(),-1)    
            #cv2.imshow('test',wave)
            #k = cv2.waitKey(0)
            #if k == 27 or k == ord('q'):
             #   cv2.destroyAllWindows()

linuxPath = "../assets/"
marysPath = "c:/Users/maryc/OneDrive/Desktop/ledBoard/assets/"

def stripes(aBoard, r, g, b):
    for led in aBoard.stringOfLights:
        y = led.y
        h = aBoard.height
        if y <= 4/5*h and y>= 3/5*h or y <=2/5*h and y >= 1/5*h:
            led.setColor(r, g, b)
    #aBoard.output('../boards/stripes.board')

# wave = cv2.imread('c:/Users/maryc/OneDrive/Desktop/ledBoard/assets/wavy-stripes-2.jpg')
#
#
# myBoard = led.LedBoard(200,wave.shape[0],wave.shape[1])
# for led in myBoard.stringOfLights:
#     led.setPosition(random.randrange(myBoard.height),random.randrange(myBoard.width))
#
# for i in range(100):
#     animateLine(myBoard, i, 200, 0, 0)
#     wave = cv2.imread('c:/Users/maryc/OneDrive/Desktop/ledBoard/assets/wavy-stripes-2.jpg')
#     for led in myBoard.stringOfLights:
#         cv2.circle(wave,led.getPosition(),20,led.getColorBGR(),-1)    
#     cv2.imshow('test',wave)
#     time.sleep(.1)
#     k = cv2.waitKey(0)
#     if k == 27 or k == ord('q'):
#         cv2.destroyAllWindows()
