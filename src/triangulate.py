import re
import math
import numpy as np
from numpy import dtype

files = ["../boardMaps/blah1.map","../boardMaps/blah2.map","../boardMaps/blah.map"]

#manually find the vertical axis in the picture or this is NOT going to work.
xCenter = 700

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
    
    coord_array.append(coords)
    
print(coord_array)

# build arrays of all corresponding x/y/z values for each light.
xNp = np.empty((2,len(coord_array)),dtype=int)
yNp = np.empty((2,len(coord_array)),dtype=int)
#zNp = np.empty((2,len(coord_array)),dtype=int)

print(xNp)

for i, coord in enumerate(coord_array):
    for j, point in enumerate(coord):
        print(j,i)
        xNp[j][i] = point[0]-xCenter
        yNp[j][i] = point[1]
        
        print(xNp)
        

coords = []

print(xNp.shape)

#iterate as many times as we have coordinates
for i in range(xNp.shape[0]):
    maxX_brightness = 0
    maxZ_brightness = 0
    
    x = 0
    y = int(np.mean(yNp,axis=1)[i]) #assumes we got all good pictures of Y
    z = 0
    
    # print("i: ",i)
    #for x & z, choose to take the data from whichever is brighter:
    for j in range(xNp.shape[1]):
        # print(j, coord_array[j][i][2]) #this is the brightness level of light i in photo j
        if(j%2 == 0): #zero or pi rotation - use for x coordinate
            if(coord_array[j][i][2] > maxX_brightness):
                maxX_brightness = coord_array[j][i][2]
                x = xNp[i][j]
        else: #rotation 1 or 3 (use for z-coordinate)
            if(coord_array[j][i][2] > maxZ_brightness):
                maxZ_brightness = coord_array[j][i][2]
                z = xNp[i][j]
                
    
    coords.append([x, y, z])
    
print(coords)

FILE = "../boardMaps/coords.txt"
with open(FILE, "w") as output:
        
    for coord in coords:
        output.write('[')
        output.write(', '.join(str(x) for x in coord))
        output.write(']')
        output.write("\n")