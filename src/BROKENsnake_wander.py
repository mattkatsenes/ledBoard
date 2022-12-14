
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
    
    snakeHead = [0,0] #this list will contain the point where the snake's head is IN 2-space.
    
    DURATION = 3 #time (sec) for a light to stay on
    
    lightsOn = [] #list of indices of lights currently on
    timeStamps = [] #list of timestamps when lights were turned on
    
    #set everything to background color
    for i in range(len(pixels)):
        pixels[i] = background
    
    pixels.show()
    
    while run:
        
        #stop if time has elapsed
        if(time.time() - startTime > DURATION):
            run = False
        
        
        frame +=1 #advance the frame count
        
        #update the lights
        pixels.show() 
         
# auto-run the code
xmaslight()    