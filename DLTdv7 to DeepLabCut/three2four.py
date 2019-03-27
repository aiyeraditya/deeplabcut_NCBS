
# Before running this code, ensure the following files are present:
# 1. two2three.py
# 2. dlc.py
# 3. Step2_ConvertingLabels2DataFrame.py
# 4. myconfig.py
# Change myconfig.py to have the label points we are interested in

import os
# Converts to seperate csv files for each camera
os.system('python dlc.py')
array = os.listdir()
array1 = []
current = os.getcwd()
for i in array:
    if(os.path.isdir(i)):
        array1.append(i)
# Gets all folders of Videos Labeled

for j in array1:
    os.system('cp two2three.py ' + j + "/") #Copying Relevant files
    os.system('cp myconfig.py ' + j + "/")
    os.system('cp Step2_ConvertingLabels2DataFrame.py ' + j + "/")
    os.makedirs(j + '/data-flying', exist_ok = True)
    os.chdir(j)
    os.system('python two2three.py') # Making h5 files for DLC
    os.chdir(current)
