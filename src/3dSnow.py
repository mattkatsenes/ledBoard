
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
    
    # testing (make sure it is loading data correctly from file) 
    # print("number of pixels: " + str(PIXEL_COUNT))
    # for coord in coords:
    #     print(coord)
    
    
    pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False)
    
    #maybe i can use this to catch a problem and stop the script?
    run = 1
    
    snowflakes = [] #initialize a list of snowflakes
    flakesToRemove = [] #at end of animating step remove these snowflakes.. can't remove them while iterating over the list, I suspect
    gravity = [0,0,-6] #change z value to get gravity feeling correct.
    wind = [1,2,0] #initial wind direction
    RADIUS = 20 #snowflake light-up radius
    FREQ = 10 #every FREQ frames, generate a new snowflake.
    
    snowLevel = -250 #snowlevel in pixels on z axis.
    
    #frame count for generating new snowflakes.
    frame = 0
    
    #convenience for color setting
    white = [50,50,50]
    black = [0,0,0]
    
    #set initial snow level
    for i, pixel in enumerate(pixels):
            if(coords[i][2] <= snowLevel):
                pixel = white
    
    while run == 1:
        
        
        #generate new snowflakes occasionally
        if(frame % FREQ == 0):
            #new snowflake
            flake = [random.randint(-200,200),random.randint(-200,200),500]
            snowflakes.append(flake)
        
        #up frame count
        frame += 1
        
        #perturb wind (maybe do this only every so many frames)
        wind[0] = wind[0] + random.randint(-1,1)
        wind[1] = wind[1] + random.randint(-1,1)
        

        
        
        #each frame, iterate through snowflakes
        for i, flake in enumerate(snowflakes):
            if(flake[2]<= snowLevel):
                #if it's hit the ground...
                flakesToRemove.append(i)
            else:
                #move flake
                flake += gravity
                flake += wind
        
        for removeIndex in flakesToRemove:
            snowflakes.pop(removeIndex)
        
        #reset flakes to remove
        flakesToRemove = []
        
        for i, pixel in enumerate(pixels):
            #turn all off pixels off except those below snow level
            if coords[i][2] > snowLevel:
                pixel = black
            #check if there's a flake nearby and turn on.
            for flake in snowflakes:
                if(math.dist(flake,coords[i]) < RADIUS):
                    pixel = white
            
        pixels.show()
        
    
    
    
    
# auto-run the code
xmaslight()    