import numpy as np

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
    '''
    def __init__(self,numLights=0,width=400,height=300):
        super().__init__(numLights)
        self.width = width
        self.height = height
        
        '''
        We will hard-define the origin at the center of the pixel matrix.
        It's going to take some playing around to get the scale to feel right.
        '''
        self.pixelArray = np.zeros((height,width,3), np.uint8)
        
    
#testing code for individual LED
myLed = Led()
print(myLed)

myLed.setColor(0, 0, 255)
print(myLed.distanceTo(3, 4))
print()

#testing code for String of LEDS
myString = LedString(2)

myString.setColor(1,0,255,0)
myString.stringOfLights[0].setColor(255,0,0)

for light in myString.stringOfLights:
    print(light)
    
myBoard = LedBoard(2,5,4)
print(myBoard.pixelArray)