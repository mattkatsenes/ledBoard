
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
    
    #Set a start time and a duration for running (scripts will alternate)s
    startTime = time.time()  #start the stopwatch
    DURATION = 300 #end after this many seconds
    
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
    pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False)
    
    #maybe i can use this to catch a problem and stop the script?
    run = 1
    
    snowflakes = [] #initialize a list of snowflakes
    flakesToRemove = [] #at end of animating step remove these snowflakes.. can't remove them while iterating over the list, I suspect
    gravity = [0,0,-6] #change z value to get gravity feeling correct.
    wind = [1,2,0] #initial wind direction
    windMAX = 20 #otherwise it get's up to hurricane force.
    RADIUS = 50 #snowflake light-up radius
    BOUNDING_BOX = 400 #box around tree to start snowflakes.  If it's not bigger than tree, flakes may all blow away!
    FREQ = 10 #every FREQ frames, generate a new snowflake.
    INITIAL_SNOW_LEVEL = -250 #sets the initial "ground level"
    MAX_SNOW_LEVEL = 0 #reset when snow gets here.
    
    snowLevel = INITIAL_SNOW_LEVEL #snowlevel in pixels on z axis.
    
    #frame count for generating new snowflakes.
    frame = 0
    
    #convenience for color setting
    white = [50,50,50]
    black = [0,0,0]
    
    #set initial snow level
    for i in range(len(pixels)):
            if(coords[i][2] <= snowLevel):
                pixels[i] = white
    
    while run == 1:
        
        #stop if time has elapsed
        if(time.time() - startTime > DURATION):
            run = 0
        
        if(snowLevel > MAX_SNOW_LEVEL):
            snowLevel = INITIAL_SNOW_LEVEL
        
        #generate new snowflakes occasionally
        if(frame % FREQ == 0):
            #new snowflake & raise snow-level by 1 pixel
            flake = [random.randint(-1*BOUNDING_BOX,BOUNDING_BOX),random.randint(-1*BOUNDING_BOX,BOUNDING_BOX),500]
            snowflakes.append(flake)
            snowLevel += 1
        
        #up frame count
        frame += 1
        
        #perturb wind (maybe do this only every so many frames)
        wind[0] = wind[0] + random.randint(-1,1)
        wind[1] = wind[1] + random.randint(-1,1)
        
        #cap the wind speed, if necessary.
        if(abs(wind[0]) > windMAX):
            wind[0] = int(windMAX * wind[0]/abs(wind[0]))

        if(abs(wind[1]) > windMAX):
            wind[1] = int(windMAX * wind[1]/abs(wind[1]))

        
        #each frame, iterate through snowflakes
        for i, flake in enumerate(snowflakes):
            if(flake[2]<= snowLevel):
                #if it's hit the ground, mark for removal.
                flakesToRemove.append(i)
            else:
                #move flake
                flake = [sum(x) for x in zip(flake, gravity)]
                flake = [sum(x) for x in zip(flake, wind)]
                
                #messing with flake isn't persistent, unless...
                snowflakes[i] = flake
        
        #remove snowflakes that have landed (can't do it in previous loop because we're iterating over them)
        for removeIndex in flakesToRemove:
            snowflakes.pop(removeIndex)
        
        #reset flakes to remove
        flakesToRemove = []
        
        for i in range(len(pixels)):
            #turn all off pixels off except those below snow level
            if coords[i][2] > snowLevel:
                pixels[i] = black
            else:
                pixels[i] = white
            #check if there's a flake nearby and turn on.
            for flake in snowflakes:
                if(math.dist(flake,coords[i]) < RADIUS):
                    pixels[i] = white
        
        #update the lights
        pixels.show() 
        
        '''
        #testing code        
        countOn = 0
        for i, light in enumerate(pixels):
            if light != [0,0,0]:
                countOn += 1
    
    
        print("iteration: ",frame)
        print("numFlakes: ",len(snowflakes))
        print("lights on: ",countOn)
        '''
    
# auto-run the code
xmaslight()    