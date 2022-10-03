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
        self.setColor(int(colorArr[0]) ,int(colorArr[1]), int(colorArr[2]))
        
    
    def getColor(self):
        return (self.r,self.g,self.b)
    
    def getColorBGR(self):
        return (self.b,self.g,self.r)
    
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
        
        '''
        This instance variable is a one-dimensional array to 
        match the stringOfLights array.  It contains a radius
        particular to each LED.  The radius is half the distance
        to the nearest other LED OR to the edge of the picture.
        '''
        self.radii = np.zeros(numLights,np.uint16)
    
    def buildRadiusArray(self):
        #I think i can do this with linear algebra...
        
        # build a complex array of your cells
        z = np.array([[complex(led.x, led.y) for led in self.stringOfLights]])
        out = abs(z.T-z)
        
        for index, row in enumerate(out):
            
            #convenience
            x, y = self.stringOfLights[index].getPosition()
        
            #find min distance to edge
            edgeDist = min(x,y,self.height-x,self.width-y)
            
            self.radii[index] =  min(min(i for i in row if i > 0)/2,edgeDist)
            #print("min radius for light ", index,": ",self.radii[index])
            #print("\tedge distance was: ",edgeDist)
        
            
    def setLedColorsStrict(self):
        '''
        Grabs the color from the pixel EXACTLY at the point where each LED
        resides.  Sets the color for each LED in the string. 
        '''
        for led in self.stringOfLights:
            x, y = led.getPosition()
            led.setColorArr(self.img[x][y])
    
    def setLedColorsCircleDynamic(self):
        self.buildRadiusArray()
        for i in range(self.numLights):
            self.setLedColorCircle(i, self.radii[i])
    
    def setLedColorsCircle(self,radius):
        '''
        Sets all led colors in the string based on a fixed radius.
        '''
        for i in range(self.numLights):
            self.setLedColorCircle(i,radius)
            
    def setLedColorCircle(self,ledNumber,radius):
        '''
        Sets the color of an individual LED to the average of the colors
        in img based on a box of given size
        '''
        #convenience code
        led = self.stringOfLights[ledNumber]
        x, y = led.getPosition()
        
        #CIRCLE TIME:
        #create a mask - all black image, white circle on top
        circle_img = np.zeros(self.img.shape[:2], np.uint8)
        cv2.circle(circle_img,(x,y),radius,(255,255,255), -1)
        
        #not sure why this produces a 4-item array, but we only need the first three.
        #perhaps the 4th is the alpha channel?        
        rgb_avg = cv2.mean(self.img,mask=circle_img)[0:3]
        #print("led position x: ",x,", y: ",y)
        #print("average rgb: ",rgb_avg)
        
        led.setColorArr(rgb_avg)
        
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
  