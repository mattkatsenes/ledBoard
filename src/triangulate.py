import re
import math
import numpy as np


ERR = -9999

files = ["../boardMaps/test1.map","../boardMaps/test2.map","../boardMaps/test3.map","../boardMaps/test4.map"]

#manually find the vertical axis in the picture or this is NOT going to work.
#horizontal axis (x) center allows us to put the origin at the center of the tree.
yCenter = 363
xCenter = 380


#x dimension is vertical, increasing numbers move you down.
#y dimension is horizontal, increasing numbers move you right, I think.
#z dimension is toward camera (deduce from images 2/4).
#Let's declare positive-Z to be toward the camera, so zero is behind tree.
coord_array = []

for file in files:
    fin = open(file,'r')
    coords_raw = fin.readlines()
    
    coords_bits = [i.split(",") for i in coords_raw]

    coords = []

    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)
        #print(new_coord)
    
    coord_array.append(coords)
    
#print(coord_array)

# build arrays of all corresponding x/y/z values for each light.
xNp = np.zeros((len(coord_array),len(coord_array[0])),dtype=int)
yNp = np.zeros((len(coord_array),len(coord_array[0])),dtype=int)
#zNp = np.empty((2,len(coord_array[0])),dtype=int)

#test
#print(yNp)

for i, bigList in enumerate(coord_array):
    #print(i, bigList)
    for j, point in enumerate(bigList):
        #print(i,j)
        #print(point)
        if(point[2] == -1):
            xNp[i][j] = ERR
            yNp[i][j] = ERR
        else:
            xNp[i][j] = point[0]-xCenter
            yNp[i][j] = point[1]-yCenter

        #test
        #print(yNp)
        

coords = []

#test, should have 4 across (one from each file), numLights down.
print(xNp.shape)

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
        #print(image, coord_array[image][i][2]) #this is the brightness level of light i in photo image
        if(image%2 == 0):
            #do y stuff
            sign = image - 1 # something on the left is on the right when tree turned around.
            sign *= -1
            if(coord_array[image][i][2] > maxY_brightness):
                maxY_brightness = coord_array[image][j][2]
                y = yNp[image][i]*sign
        else:
            #figure out z
            sign = image - 2 # something on the left is on the right when tree turned around.
            if(coord_array[image][i][2] > maxZ_brightness):
                maxZ_brightness = coord_array[image][j][2]
                z = yNp[image][i]*sign
           
            
    

    '''

    maxY_brightness = 0
    maxZ_brightness = 0
    
    y = ERR
    z = ERR
    
    # print("i: ",i)
    #for y & z, choose to take the data from whichever is brighter:
    for j in range(xNp.shape[0]):
        # print(j, coord_array[j][i][2]) #this is the brightness level of light i in photo j
        if(j%2 == 0): #zero or pi rotation - use for y-coordinate
            if(coord_array[i][j][2] > maxY_brightness):
                maxY_brightness = coord_array[i][j][2]
                y = xNp[j][i]
        else: #rotation 1 or 3 (use for z-coordinate)
            if(coord_array[i][j][2] > maxZ_brightness):
                maxZ_brightness = coord_array[i][j][2]
                z = xNp[i][j]
                
    '''
    coords.append([x, y, z])
    
print(coords)

countErrors = 0
for point in coords:
    for val in point:
        if val == ERR:
            countErrors += 1

print("total number of errors: ",countErrors)

#find errors, work forwards and backwards in the string until you find a good ones, then interpolate correct-ish values.
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

