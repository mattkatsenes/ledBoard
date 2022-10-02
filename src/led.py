import numpy as np
import cv2
import random

class Led(object):
    '''
    Represents one light on our string
    The light knows it's color and it's X,Y location
    '''
    
    def __init__(self):
        '''
        sets led to off (black) by default at position (0,0)
        '''
        self.r = 0
        self.g = 0
        self.b = 0
        
        self.x = 0
        self.y = 0
        
    def setColor(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b 
    
    def setColorArr(self,colorArr):
        self.r = colorArr[0]
        self.g = colorArr[1]
        self.b = colorArr[2]
    
    def getColor(self):
        return (self.r,self.g,self.b)
    
    def setPosition(self,x,y):
        self.x = x
        self.y = y

    def getPosition(self):
        return self.x, self.y
    
    #checks the distance from this LED to a given point
    def distanceTo(self,x,y):
        distance = pow(pow(self.x-x,2) + pow(self.y-y,2),.5)
        return distance
    
    #this overrides the default print behavior for the object
    def __str__(self):
        response = "light at "
        response = response + "x: " + str(self.x) + ", y: " + str(self.y)
        response = response + ", with color: (" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"
        return response
    
class LedString(object):
    '''
    Experimenting with inheritance, mostly.  
    This layer of abstraction models the string itself.
    It's just an array of LEDs.
    '''
    def __init__(self,numLights=0):
        self.numLights = numLights
        self.stringOfLights = []
        for num in range(self.numLights):
            led = Led()
            self.stringOfLights.append(led)
            
    
    def __str__(self):
        '''
        Not sure if this will help to print anything.  It doesn't.
        '''
        output = ""
        for led in stringOfLights:
            output = output + str(led) + "\n"
        return output
    
    #not sure if this is useful    
    def setColor(self,lightNum,r,g,b):
        self.stringOfLights[lightNum].setColor(r,g,b)
        

class LedBoard(LedString):
    '''
    This class is meant to represent an LED board.
    In our case, it is a board filled with LED lights on strings.
    Each light knows its own position in space.  This class should
    hold a theoretical representation of the image and contain methods
    for updating each LED on the board.
    
    width/height = theoretical pixel size of the image projected down
                   onto the board
    img = the theoretical image to be projected on board
    '''
    def __init__(self,numLights=0,height=300,width=400):
        super().__init__(numLights)
        self.width = width
        self.height = height
        
        '''
        This instance variable is a cv2 compliant array of three-tuples
        representing an image.  It will be used to mix down to the board
        lights.  Because OpenCV uses BGR, we'll have to switch that up,
        and because OpenCV places 0,0 at the top left of the image, any
        math-y stuff we do will have to take that into account.
        '''
        self.img = np.zeros((height,width,3), np.uint8)
    
    def setLedColorsStrict(self):
        '''
        Grabs the color from the pixel EXACTLY at the point where each LED
        resides.  Sets the color for each LED in the string. 
        '''
        for led in self.stringOfLights:
            x, y = led.getPosition()
            led.setColorArr(self.img[x][y])
            
        
    def output(self,filepath="../boards/output.board"):
        '''
        Writes a file with the LED color values in string order.
        Format rellies on led.getColor()
        newline delimited values
        '''
        with open(filepath, "w") as out:
            for led in self.stringOfLights:
                out.write(str(led.getColor()))
                out.write("\n")
                
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
    
myBoard = LedBoard(10,5,4)

#randomize pixel color:
myBoard.img = (np.random.rand(5,4,3) * 255).astype(np.uint8)

#print(myBoard.img)

#randomize positions of LEDs for testing
for led in myBoard.stringOfLights:
    led.setPosition(random.randrange(myBoard.height),random.randrange(myBoard.width))
    

myBoard.setLedColorsStrict()

for led in myBoard.stringOfLights:
    print(led)

# cv2.imshow('test',myBoard.img)
# k = cv2.waitKey(0)
# if k == 27 or k == ord('q'):
#     cv2.destroyAllWindows()

#myBoard.output("../boards/test.board")