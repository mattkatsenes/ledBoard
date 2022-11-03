'''
@author: Matt Katsenes
Testing and experimentation with our LED library.
'''

import led
import cv2
import numpy as np
import random

from mary import stripes, animateLine
from olivia import line


import serial
import time


def turnOff(board):
    for light in board.stringOfLights:
        light.setColor(0,0,0)

filepath = "../boardMaps/10_14_success.map"

myBoard = led.LedBoard(0, 0, 0)
myBoard.buildBoardFromFile(filepath)

steps = 20
for i in range(steps):
    for light in myBoard.stringOfLights:
        if(light.x < (i+1)/steps*myBoard.height and light.x >= i/steps*myBoard.height):
            light.setColor(0,200*(i+1)/steps,0)
        elif(light.getColor() != (0,0,0)):
            light.setColor(0,0,0)
    
    myBoard.serialOut()
    #time.sleep(1)
            
            
            
# line(myBoard,(myBoard.height/2)+(myBoard.height)*4 +5000,20,[0,100,0], [0,0,200])
# myBoard.serialOut()


# for i in range(100):
#     animateLine(myBoard, i, 200, 0, 0)
#     #wave = cv2.imread('../assets/wavy-stripes-2.jpg')
#     myBoard.serialOut()

#stripes(myBoard, 200, 0, 0)

# grab a test image
#pic = cv2.imread('../assets/gb_vert.jpg')
pic = cv2.imread('../assets/gb_vert.jpg')

#resize the image to match the board dimensions
pic = cv2.resize(pic, (myBoard.img.shape[0],myBoard.img.shape[1]) )
myBoard.img = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
myBoard.setLedColorsCircleDynamic()

cv2.imshow('pic',pic)

time.sleep(3)

#myBoard.serialOut()



#turnOff(myBoard)

#myBoard.serialOut()


# pic2 = cv2.resize(pic2, (myBoard.img.shape[0],myBoard.img.shape[1]) )
# myBoard.img = cv2.cvtColor(pic2, cv2.COLOR_BGR2RGB)
# myBoard.setLedColorsCircleDynamic()
#
# cv2.imshow('pic2',pic2)
#
# myBoard.serialOut()
#
# myBoard.serialClose()  
#
# k = cv2.waitKey(0)
# if k == 27 or k == ord('q'):
#     cv2.destroyAllWindows()  

    #arduino.write(bytes(str(index),'utf_8'))
    #arduino.write(bytes(str(light.getColor()),'utf_8'))
    

#myBoard.serialOut()
#myBoard.output("../boards/stripes.board")

# print("led list:")
# for led in myBoard.stringOfLights:
#     print(led)

#arduino.close()
           


#testing code for mixing down from an image:
'''
#grab my green-blue stripe test image
#gb = cv2.imread('../assets/gb_vert.jpg')


#more complicated wavy image:

wave = cv2.imread('../assets/wavy-stripes-2.jpg')


myBoard = led.LedBoard(200,wave.shape[0],wave.shape[1])

#converts cv2 default (BGR) to our format (RGB)
myBoard.img = cv2.cvtColor(wave, cv2.COLOR_BGR2RGB)



#randomize pixel color on image:
#myBoard.img = (np.random.rand(myBoard.height,myBoard.width,3) * 255).astype(np.uint8)

#randomize positions of LEDs for testing
for led in myBoard.stringOfLights:
    led.setPosition(random.randrange(myBoard.height),random.randrange(myBoard.width))

myBoard.setLedColorsCircleDynamic()


#myBoard.setLedColorCircle(0, 10)

#set all the LED colors.
#myBoard.setLedColorsCircle(10)


# #set the led colors to only what's on top of them    
# myBoard.setLedColorsStrict()

#draw a circle around the where the LEDs are  in the image
for index, led in enumerate(myBoard.stringOfLights):
    cv2.circle(wave,led.getPosition(),myBoard.radii[index],led.getColorBGR(),-1)    

cv2.imshow('test',wave)
k = cv2.waitKey(0)
if k == 27 or k == ord('q'):
    cv2.destroyAllWindows()

#myBoard.output("../boards/test.board")

'''