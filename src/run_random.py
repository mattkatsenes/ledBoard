import os
import random
import subprocess
import time

#get current working directory
path = os.getcwd()
thisFileName = os.path.basename(__file__)

all_files = os.listdir(path)

executable_files = []

# Get .py files in this directory
for i in range(len(all_files)):
    if all_files[i].endswith('.py') and all_files[i] != thisFileName and not(all_files[i].startswith("BROKEN")):
        executable_files.append(all_files[i])


startTime = time.time()
DURATION = 20

onPi = False #if on pi, it runs forever and the python command is different.
      
run = True  
while run:
    #pick a random python file from this directory
    fileNum = random.randint(0,len(executable_files)-1)
    
    print("running this one: ",executable_files[fileNum])
    
    
    if(onPi):
        #run it [change python3 to python on the Pi]
        subprocess.run(["python",executable_files[fileNum]])
    
    else:
        if(time.time() - startTime > DURATION):
            run = False
            
        #run it [change python3 to python on the Pi]
        subprocess.run(["python3",executable_files[fileNum]])