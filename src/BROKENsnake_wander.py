
def xmaslight():
    # NOTE THE LEDS ARE GRB COLOUR (NOT RGB)
    
    # Here are the libraries I am currently using:
    import time
    import board
    import neopixel
    import re
    import math
    
    # You are welcome to add any of these:
    import random
    # import numpy
    # import scipy
    # import sys
    
    # If you want to have user changable values, they need to be entered from the command line
    # so import sys sys and use sys.argv[0] etc
    # some_value = int(sys.argv[0])
    
    # IMPORT THE COORDINATES - put correct filename in here.
    coordfilename = "../boardMaps/treeCoords-zUp.txt"
    
    #Set a start time and a duration for running (scripts will alternate)s
    startTime = time.time()  #start the stopwatch
    DURATION = 300 #end after this many seconds
    
    fin = open(coordfilename,'r')
    coords_raw = fin.readlines()
    
    coords_bits = [i.split(",") for i in coords_raw]
    
    coords = []
    
    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)
    
    #set up the pixels (AKA 'LEDs')
    PIXEL_COUNT = len(coords) # this should be 500
    pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False)
    
    #maybe i can use this to catch a problem and stop the script?
    run = True
    
   
    
    #frame count for generating new snowflakes.
    frame = 0
    
    #convenience for color setting
    snakeColor = [80,0,0] 
    background = [0,0,0]
    
    radius = 20
    
    snakeHead = [0,0] #this list will contain the point where the snake's head is IN 2-space.

    
    DURATION = 3 #time (sec) for a light to stay on
    
    lightsOn = [] #list of indices of lights currently on
    timeStamps = [] #list of timestamps when lights were turned on
    
    #set everything to background color
    for i in range(len(pixels)):
        pixels[i] = background
    
    pixels.show()
    
    theta = 0
    increment = 10 #degrees between theta1 and theta2
    while run:
        
        #stop if time has elapsed
        if(time.time() - startTime > DURATION):
            run = False
            
        if(theta == 360): #so theta doesn't go to 10,000
            theta = 0
            
        #snakeHead[0] = cos(theta) # does theta need to go between 0 and 2pi or 0 and 360?
        #snakeHead[1] = sin(theta)
        for i in range(len(pixels)):
            #is the pixel between the lines created from theta and theta + increment
            if(pixels[i].y >= (sin(theta)/cos(theta))*pixels[i].x and pixels[i].y <= (sin(theta + increment)/cos(theta + increment))*pixels[i].x):
               pixels[i] = snakeColor
            # same as the other if but the < and > are swapped for if 90<theta<270
            if(pixels[i].y <= (sin(theta)/cos(theta))*pixels[i].x and pixels[i].y >= (sin(theta + increment)/cos(theta + increment))*pixels[i].x):
               pixels[i] = snakeColor
        # there are probably lots of bugs in this, sorry
        #    like if theta is 90, 270, 85, 265
        #    and it doesn't check if the light is in the right quadrant
        
        # we need to add z. probably just a variable that goes from 0 to whatever the height of the tree is 
        # and if the pixel is within 10ish units of that height and the other stuff in the if is true, then it lights up ?
        
        theta += 1
        frame +=1 #advance the frame count
        
        #update the lights
        pixels.show() 
         
# auto-run the code
xmaslight()    
