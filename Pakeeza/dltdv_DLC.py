import numpy as np
import cv2
#import deeplabcut
import os
from datetime import datetime as dt

print("DeepLabCut Imported")

dltfilename = "datafiles/soldierfly02xypts.csv"
NumberOfParts = 8
crop_x = 0
crop_y = 0
image_size_x = 1200
image_size_y = 800
headers = ["right_antennae", "left_antennae", "antennae_base", "right_wing_base", "right_wing_tip", "left_wing_tip", "abdomen_tip", "right_haltere"]
project_name = "flying"
video_path = "datafiles/Flight2_V1.cine"
v_name = "Flight2_V1"
experimenter = 'Aditya'
image_start = 400
image_end = 995

date = dt.today()
month = date.strftime("%B")
day = date.day
d = str(month[0:3]+str(day))
date = dt.today().strftime('%Y-%m-%d')
folder = '{pn}-{exp}-{date}'.format(pn=project_name, exp=experimenter, date=date)
#folder = 'flying-Aditya-2019-01-03'

def edit_myconfig():
    file = open("myconfig.py", "r")
    lines = file.readlines()
    file.close()
    file = open("myconfig.py", "w")
    for i in lines:
        if (i.startswith("Task")):
            file.write("Task = '" + project_name + "'\n")
        elif (i.startswith("bodyparts")):
            file.write("bodyparts = [")
            for j in headers:
                if(headers[-1]==j):
                    file.write("'" + j + "']\n")
                else:
                    file.write("'" + j + "', ")
        elif (i.startswith("Scorers")):
            file.write("Scorers = ['" + experimenter + "']\n")
        else:
            file.write(i)
    file.close()


def create_csv():
    filenames = []
    file = open(dltfilename)
    f1 = file.readlines()
    count = 0
    colNo = NumberOfParts*2 + 1     #Number of Columns in the File from DeepLabCut
    for i in headers:               #Assuming that the headers match the
        filenames.append(i +".csv")
    f = []
    for i in f1:
        i = i[:-1] + ",\n"
        f.append(i)

    #Create The Above Files
    os.system("mkdir data-" + project_name)
    os.system("mkdir data-" +project_name + "/" + v_name)
    filedata = {filename: open("data-" + project_name + "/" + v_name + "/" + filename, 'w') for filename in filenames}

    for i in filenames:
        filedata[i].write("X,Y\n")  #Header for the exported files

    for i in f[1:]:         #Only Third Row Onwards Has Data
        values = i.split(",")
        count = 0
    # Read each row and write to each file. (Like Distributing Cards)
        for j in values:
            count+=1
            if(count==colNo):          #Last Column to Read. Go to next row
                break
            if(count%2 == 0):       #Y Value. DLTDV7 and DLC have different origins.
                if(float(j) == 0):
                    j = str(crop_y) # To prevent negative values for NA things
                filedata[filenames[int(count/2 - 1)]].write(str(image_size_y - crop_y - float(j)))
                filedata[filenames[int(count/2 - 1)]].write("\n")
            else:
                if(float(j) == 0):
                    j = str(crop_x)
                filedata[filenames[int((count-1)/2)]].write(str(float(j) - crop_x))
                filedata[filenames[int((count-1)/2)]].write(",")

    print("The Following Files have been created")
    for i in filenames:
        print(i)             #Check for Filenames to be printed

def extract_images(video_name, start, stop):
    cap = cv2.VideoCapture(video_name)
    number = 1
    count = 0
    ret = 1
    while ret:
        ret, frame = cap.read()
        if ((number >= start) and (number <= stop)):
            cv2.imwrite("data-" + project_name + "/" + v_name + "/img" + str(number) + ".png", frame)
            print("data-" + project_name + "/" + v_name + "/img" + str(number) + ".png")
        number = number + 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            continue
    cap.release()
    cv2.destroyAllWindows() #Extracts  Images from Video and puts in folder
    print('Extracted Apprpriate Frames')
    # Need to Add excpetion for last frame

#Generate DataFrame
def training_set():
    # confirm myconfig.py
    # do python code python Step2_ConvertingLabels2DataFrame.py
    os.system('python Step2_ConvertingLabels2DataFrame.py')
    # Move files to deeplabcut folder
    print("Training Set Has Been Generated")

def moving_files():
    # Move "Collected" files to project_name + "-" + experimenter + "-" + date
    file_list = os.listdir("data-" + project_name)
    file_list_labeled = os.listdir(folder + "/labeled-data/")
    os.system("rm -R " + folder + "/labeled-data/" + v_name + "_labeled")
    os.system("rm -R " + folder + "/labeled-data/" + v_name)
    print("Removed " +  folder + "/labeled-data/" + v_name)
    os.system("mkdir " + folder + "/labeled-data/" + v_name)
    for i in file_list:
        if i.startswith("C"):
            os.system("cp data-" + project_name + "/" + i + " " + folder + "/labeled-data/" + v_name + "/" + i)
    file_list = os.listdir("data-" + project_name + "/" + v_name)
    for i in file_list:
        if i.startswith("img"):
            os.system("cp data-" + project_name + "/" + v_name + "/" + i + " " + folder + "/labeled-data/" + v_name + "/" + i)
    print("Files Moved to Appropriate Places")

def change_yaml():
    f = open(folder + "/config.yaml", "r")
    f_lines = f.readlines()
    f.close()
    f = open(folder + "/config.yaml", "w")
    check = 0
    for i in f_lines:
        if(check == 0):
            f.write(i)
        if(check == 1):
            if(i.startswith("-") != True):
                check = 0
                f.write(i)
        if(i.startswith("bodyparts")):
            check = 1
            for j in headers:
                f.write("- " + j + "\n")
    f.close()

# Function to Remove the Bad Image from the list and the corresponding datafiles
# And Then Re-Run The Above Functions
def remove_bad_image(lost_images):
    count = 0
    for i in lost_images:
        l = len("data-" + project_name) + 1
        str = "data-" + project_name + i[l:]
        print(str)
        os.system("rm " + str) # Removed Image from datafile
        l += len(v_name) + 5    # 2 for '/' and 3 for 'img'
        number = int(i[l:-4])   # This is the index of the missing image
        print(number)
        row_number = number - image_start + 1 - count
        count = count + 1
        path1 = "data-" + project_name + "/" + v_name
        file_list = os.listdir(path1)
        for j in file_list:
            if (j.endswith(".csv") != True):
                continue
            file1 = open(path1 + "/" + j, "r")
            f = file1.readlines()
            file1.close()
            file1 = open(path1 + "/" + j, "w")
            print("Now Working on This File " + path1 + "/" + j, "w")
            c = 0
            for k in f:
                if (c == row_number):
                    c = c + 1
                    continue
                c = c + 1
                file1.write(k)  #Rewrites csv files
        file1.close()
        training_set()
        moving_files()

def edit_init():
    # Move The Project Folder and DeepLabCut to package folder
    # From DeepLabCut, do not move create, generate or refine
    # Also Move config.yaml
    file = open("package/deeplabcut/__init__.py", "r")
    lines = files.readlines()
    file.close()
    file = open("package/deeplabcut1/__init__.py", "w")
    for i in lines:
        if("generate_training_dataset" in i) or ("refine_training_dataset" in i):
            file.write("# ")
            file.write(i)
        else:
            file.write(i)
    file.close()
    file = open("package/" + folder + "/config.yaml")
    # Change the paths to Google Drive Paths
    file.close()


# edit_myconfig()
# create_csv()            # COnverts DLT-DV files to indivudual files for Step2.py
# extract_images('datafiles/Flight2_V1.cine', 400, 995)   #Takes Images from the video
# deeplabcut.create_new_project(project_name,experimenter, [video_path], working_directory='.',copy_videos=True)
# training_set()  # Generates Training Set
# moving_files()  # Moves files to appropriate folder
# change_yaml()   #Changes the config file
# lost_images = deeplabcut.check_labels(folder + '/config.yaml')  #Labels for Confirmation
# remove_bad_image(lost_images)   #Removes Corrupted Images that could not be labeled
# lost_images = deeplabcut.check_labels(folder + '/config.yaml')  #Reruns the labeling code
# proceed = raw_input("Are the Labeled Images fine? If yes, will proceed with creating training set 'Y' or 'N' ")
# if(proceed == 'Y'):
#      deeplabcut.create_training_dataset(folder + '/config.yaml', num_shuffles = 1)
#      edit_init()
# if(proceed == 'N'):
#     print("Will Figure Out What To Do Later")


# Change config.yaml to upload to Google Drive
