# This script passes the outputs of three2four.py to DLC 1.0 and
# Cleans up unncessesary files later
import os
array = os.listdir()
array1 = []
for i in array:
    if((os.path.isdir(i)) and (i.startswith('Fly0'))):
        array1.append(i)
# All Folders in array1
print(array1)
for i in array1:
    print('cp -r ' + i + ' data-flying/' + i)
    os.system('cp -r ' + i + ' data-flying/' + i)
    # Getting h5 files for each folder
    os.system('python Step2_ConvertingLabels2DataFrame.py')
    for j in os.listdir('data-flying/' + i):
        if(j.endswith('.csv')):
            os.system('rm ' + 'data-flying/' + i + '/' + j)
    # Cleaning up for easier processing later
    os.system('cp data-flying/CollectedData_Aditya.csv data-flying/' \
    + i +'/CollectedData_Aditya.csv')
    os.system('cp data-flying/CollectedData_Aditya.h5 data-flying/' + \
    i +'/CollectedData_Aditya.h5')
    os.system('rm data-flying/CollectedData_Aditya.csv')
    os.system('rm data-flying/CollectedData_Aditya.h5')
    print('cp -r data-flying/' + i + ' ' + i)
    os.system('rm -r ' + i)
    os.system('cp -r data-flying/' + i + ' .')
    os.system('rm -r data-flying/' + i)
