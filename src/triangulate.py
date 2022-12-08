import re
import math
import numpy as np

NUM_LEDs = 500

ERR = -9999

files = ["../boardMaps/tree1_12_7.map","../boardMaps/tree2_12_7.map","../boardMaps/tree3_12_7.map","../boardMaps/tree4_12_7.map"]


#x dimension is vertical, increasing numbers move you down.
#y dimension is horizontal, increasing numbers move you right, I think.
#z dimension is toward camera (deduce from images 2/4).

#coord_array = []

# build arrays of all corresponding OBSERVED x/y values for each light.
xNp = np.zeros((len(files),NUM_LEDs),dtype=int)
yNp = np.zeros((len(files),NUM_LEDs),dtype=int)
brightness = np.zeros((len(files),NUM_LEDs),dtype=int)

for filenum, file in enumerate(files):
    fin = open(file,'r')
    coords_raw = fin.readlines()
    
    coords_bits = [i.split(",") for i in coords_raw]

    #coords = []

    for led, slab in enumerate(coords_bits):
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        #coords.append(new_coord)
        #print(new_coord)
        if(new_coord[2] == -1):
            xNp[filenum][led] = ERR
            yNp[filenum][led] = ERR
            brightness[filenum][led] = -1
        else:
            xNp[filenum][led] = new_coord[0]
            yNp[filenum][led] = new_coord[1]
            brightness[filenum][led] = new_coord[2]
    
    #coord_array.append(coords)
    
#print(coord_array)

#deduce the location of [0,0,0] by looking at good observations and guessing.

avgY = 0
countY = 0


for led in range(NUM_LEDs):
    if(yNp[0][led] > ERR and yNp[2][led] > ERR):
        avgY += (yNp[0][led] + yNp[2][led])/2
        countY += 1
    if(yNp[1][led] > ERR and yNp[3][led] > ERR):
        avgY += (yNp[1][led] + yNp[3][led])/2
        countY += 1


avgY /= countY

#guess the vertical middle to be half the distance to the 
avgX = np.max(xNp) / 2

print("average y value on good observations: ",avgX)
print("x midpoint: ",avgY)

#shift coordinates so the origin is at the middle of the tree
for led in range(NUM_LEDs):
    for f in range(len(files)):
        if(xNp[f][led] > ERR):
            xNp[f][led] -= avgX
            #flip x axis around zero, otherwise moving in the positive X direction makes you go down.
            xNp[f][led] *= -1 
            
        if(yNp[f][led] > ERR):
            yNp[f][led] -= avgY
            



#Initialize our final list for output. 
coords = []

#test, should have 4 across (one from each file), numLights down.
#print(xNp.shape)

#slicing practice
#print(xNp[:,1:2])
#print(xNp[1::2,1:2]) #odd, rows 1,3
#print(xNp[::2,1:2]) #even, rows 0,2

#iterate as many times as we have coordinates
for i in range(xNp.shape[1]):

    #derive the x value from an average of good observations
    total = 0
    num = 0

    for xVal in xNp[:,i:i+1]: #that is a slice vertically through the array
        if(xVal != ERR):
            total += xVal
            num += 1

    if(num>0):
        x = int(total/num)
    else:
        x = ERR

    maxY_brightness = 0
    maxZ_brightness = 0

    #set initial y,z values to our error marker
    y = ERR
    z = ERR

    for image, yVal in enumerate(yNp[:,i:i+1]):
        if(image%2 == 0):
            #do y stuff
            sign = image - 1 # something on the left is on the right when tree turned around.
            sign *= -1 #flip sign so first image is real tree position
            if(brightness[image][i] > maxY_brightness):
                maxY_brightness = brightness[image][i]
                y = yNp[image][i]*sign
        else:
            #figure out z
            sign = image - 2 # something on the left is on the right when tree turned around.
            if(brightness[image][i] > maxZ_brightness):
                maxZ_brightness = brightness[image][i]
                z = yNp[image][i]*sign




    coords.append([x, y, z])

#print(coords)


#error checking:
countErrors = 0
for point in coords:
    for val in point:
        if val == ERR:
            countErrors += 1

print("total number of errors: ",countErrors)

#find errors:
# work forwards and backwards in the string until you find a good ones, 
# then interpolate correct-ish values.

for dim in range(3):
    lastGoodIndex = -1
    for index in range(len(coords)):
        if coords[index][dim] != ERR:
            lastGoodIndex = index
        elif(lastGoodIndex != -1):
            #there's something good behind us...
            dist_back = index-lastGoodIndex

            nextGoodIndex = index+1 #maybe
            #find next good Index
            while(nextGoodIndex < len(coords) and coords[nextGoodIndex][dim] == ERR):
                nextGoodIndex+=1

            if(nextGoodIndex == len(coords)):
                #hit the end of the string without finding a good one.
                coords[index][dim] = coords[lastGoodIndex][dim]

            else:
                #we have good stuff behind us and in front of us on the string.
                dist_forward = nextGoodIndex - index

                coords[index][dim] = int((coords[nextGoodIndex][dim]-coords[lastGoodIndex][dim])*dist_back/(dist_back+dist_forward)+coords[lastGoodIndex][dim])

        else:
            #beginning of string
            nextGoodIndex = index+1 #maybe
            #find next good Index
            while(nextGoodIndex < len(coords) and coords[nextGoodIndex][dim] == ERR):
                nextGoodIndex+=1

            assert(nextGoodIndex < len(coords))
            coords[index][dim] = coords[nextGoodIndex][dim]

print(coords)

countErrors = 0
for point in coords:
    for val in point:
        if val == ERR:
            countErrors += 1
print("total number of errors: ",countErrors)



FILE = "../boardMaps/coords.txt"
with open(FILE, "w") as output:

    for coord in coords:
        output.write('[')
        output.write(', '.join(str(x) for x in coord))
        output.write(']')
        output.write("\n")

