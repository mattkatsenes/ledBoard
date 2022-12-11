import matplotlib.pyplot as plt
import re
import numpy as np
from mpl_toolkits import mplot3d

# IMPORT THE COORDINATES - put correct filename in here.
#coordfilename = "../boardMaps/treeCoords.txt"
#coordfilename = "../boardMaps/treeCoords-try2.txt"
#coordfilename = "../boardMaps/parker_coords.txt"
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


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.view_init(elev=0, azim=30, roll=0)

xs = []
ys = []
zs = []

for coord in coords:
    ax.scatter3D(coord[0],coord[1],coord[2],marker='o')
    xs.append(coord[0])
    ys.append(coord[1])
    zs.append(coord[2])

ax.set_box_aspect((np.ptp(xs), np.ptp(ys), np.ptp(zs)))  # aspect ratio is 1:1:1 in data space



ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()