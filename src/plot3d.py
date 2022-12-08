import matplotlib.pyplot as plt
import re
import numpy as np
from mpl_toolkits import mplot3d

# IMPORT THE COORDINATES - put correct filename in here.
coordfilename = "../boardMaps/treeCoords.txt"
#coordfilename = "../boardMaps/coords.txt"

fin = open(coordfilename,'r')
coords_raw = fin.readlines()

coords_bits = [i.split(",") for i in coords_raw]

coords = []

for slab in coords_bits:
    new_coord = []
    for i in slab:
        new_coord.append(int(re.sub(r'[^-\d]','', i)))
    coords.append(new_coord)


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for coord in coords:
    ax.scatter3D(coord[0],coord[1],coord[2],marker='o')




ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()