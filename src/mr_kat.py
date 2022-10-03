'''
@author: Matt Katsenes
Testing and experimentation with our LED library.
'''

import led

              
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

#grab my green-blue stripe test image
#gb = cv2.imread('../assets/gb_vert.jpg')


#more complicated wavy image:
wave = cv2.imread('../assets/wavy-stripes-2.jpg')
print("original image shape: ",wave.shape)


myBoard = LedBoard(200,wave.shape[0],wave.shape[1])

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