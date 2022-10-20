'''
@author: Matt Katsenes
Testing and experimentation with our LED library.
'''

import led
import cv2
import numpy as np
import random

from mary import stripes


import serial
import time


filepath = "../boardMaps/10_14_success.map"

myBoard = led.LedBoard(0, 0, 0)
myBoard.buildBoardFromFile(filepath)


stripes(myBoard, 200, 0, 0)

#grab a test image
#pic = cv2.imread('../assets/wavy-stripes-2.jpg')

#resize the image to match the board dimensions
# pic = cv2.resize(pic, (myBoard.img.shape[0],myBoard.img.shape[1]) )
# myBoard.img = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
# myBoard.setLedColorsCircleDynamic()

myBoard.serialOut()

stripes(myBoard, 0, 200, 0)

myBoard.serialOut()

stripes(myBoard, 0, 200, 0)
myBoard.serialOut()

myBoard.serialClose()    
    
    #arduino.write(bytes(str(index),'utf_8'))
    #arduino.write(bytes(str(light.getColor()),'utf_8'))
    

#myBoard.serialOut()
#myBoard.output("../boards/stripes.board")

# print("led list:")
# for led in myBoard.stringOfLights:
#     print(led)

#arduino.close()
           
# #testing code for individual LED
# myLed = Led()
# print(myLed)
#
# myLed.setColor(0, 0, 255)
# print(myLed.distanceTo(3, 4))
# print()
#
# #testing code for String of LEDS
# myString = LedString(2)
#
# myString.setColor(1,0,255,0)
# myString.stringOfLights[0].setColor(255,0,0)
#
# for light in myString.stringOfLights:
#     print(light)


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