def xmaslight():
    # NOTE THE LEDS ARE GRB COLOUR (NOT RGB)
    
    # Here are the libraries I am currently using:
    import time
    import board
    import neopixel
    import re
    import math
    
    # You are welcome to add any of these:
    # import random
    # import numpy
    # import scipy
    # import sys
    
    # If you want to have user changable values, they need to be entered from the command line
    # so import sys sys and use sys.argv[0] etc
    # some_value = int(sys.argv[0])
    
    # IMPORT THE COORDINATES - put correct filename in here.
    coordfilename = "../boardMaps/test.map"
    
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
    
    stripeColor = [50,50,50] #white
    black = [0,0,0]
    
    while run == 1:
        y = 0
        
        
        for i in range(50):
            #move my stripe down (positive y direction)
            y+=10
            
            # set colors of pixels
            LED = 0
            while LED < len(coords):
                # if within 10 of y value, light up.
                if(abs(coords[LED][1] - y) < 10):
                    pixels[LED] = stripeColor
                else:
                    pixels[LED] = black
            
                LED += 1
            
            # show (use sparingly)
            pixels.show()
        
    
    

# auto-run the code
xmaslight()    