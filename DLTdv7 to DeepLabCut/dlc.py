import cv2
import os
def extract_data(file_name, array):
    # "Fly01_F1xypts.csv"
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    data = [0 for i in range(len(array))]
    count = 0;
    index = 0
    for i in lines:
        if(count == array[index]):
            data[index] = i
            index = index + 1
        if(index == len(array)):
            break
        count = count + 1
    return data
#
# I now have data containing all the requried data

def get_frames(video_name, array, offset):
    # This Function Extracts and crops the frame to the right size
    #video_name = 'Fly001_F01_V01.avi'
    cap = cv2.VideoCapture(video_name)
    number = 1
    count = 0
    ret = 1
    os.makedirs(video_name[:-4], exist_ok = True)
    os.chdir(video_name[:-4])
    while ret:
        ret, frame = cap.read()
        #os.makedirs("Images" + str(offset), exist_ok = True)
        if (number in array):
            cv2.imwrite("img"  + str(number) + ".png", frame)
            print("/img" + str(number) + ".png")
        number = number + 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            continue
    cap.release()
    cv2.destroyAllWindows() #Extracts  Images from Video and puts in folder
    print('Extracted Apprpriate Frames')# Make the change to os command here
# Appropriate frames have been extracted

def write_data(data, array, offset):
    # Offset as (0,0) are at different points for OpenCV and DLTdv7
    if(offset == 2):
        off = 1080
    else:
        off = 800
    x_max = [1200, 0, 1920, 0, 1200]
    y_max = [800, 0, 1080, 0, 800]
    file = open("View1.csv", 'w')
    file.write("X,Y,Slice\n") # Format for Step2_ConvertingLabels2DataFrame.py
    count = 0
    for i in data:
        dat = i.split(",")
        x = []
        y = []
        ar_index = []
        for i in range(6):
            ar_index.append(i*6 + offset)
            ar_index.append(i*6 + 1 + offset)
        for j in ar_index:
            if(dat[j] == 'NaN'):
                dat[j] = -1;
            if(j % 2 == 0):
                x.append(float(dat[j]))
            else:
                y.append(float(dat[j]))
        x1 = [k for k in x if k != -1]
        y1 = [k for k in y if k != -1]
        max_x = round(max(x1)) + 20
        if(max_x > x_max[offset]):
            max_x = x_max[offset]
        max_y = off - (round(max(y1)) + 40)
        if(max_y < 0):
            max_y = 0
        min_x = round(min(x1)) - 20
        if(min_x < 0):
            min_x = 0
        min_y = off - (round(min(y1)) - 40)
        if(min_y > offset):
            min_y = offset
        print("Images/image" + str(array[count]) + ".png")
        # make a folder Of Images Offset
        image = cv2.imread("img" + str(array[count]) + ".png")
        try:
            if(count != 0):
                im2 = image[max_y:min_y, min_x:max_x]
            else:
                im2 = image
        except:
            print("Error")
            continue
        cv2.imwrite("img" + str(array[count]) + ".png", im2)
        for i in range(6):
            if(count == 0):
                if(x[i] != -1):
                    file.write(str(round(x[i])) + "," + str(round(off - y[i]))\
                     + "," + str(count+1) + "\n")
                else:
                    file.write('0,0,' + str(count+1) +'\n')
            else:
                if(x[i] != -1):
                    file.write(str(round(x[i] - min_x)) + "," + \
                    str(round(off - y[i] - max_y)) + "," + str(count+1) + "\n")
                else:
                    file.write('0,0,' + str(count+1) +'\n')
        count = count + 1
    file.close()
# The XY file has been written

def initiate(array, filename, current):
    data = extract_data(filename + "xypts.csv", array)
    print(filename + "xypts.csv")
    for i in [0,2,4]:
        c = str(round(i/2 + 1));
        get_frames("View" + c + "/" + filename + '_V' + c + '.avi', array, i)
        write_data(data, array, i)
        os.chdir(current)

current = os.getcwd()
# Pass the Array and the FileName

array = [110,  115,  128,  163,  173,  197,  316,  387,  447,  575, 676,  744,\
 791,  794,  796,  920,  927,  955,  978, 1006]
initiate(array, 'Fly01_Control_F02', current)

array = [19,  64,  96, 138, 217, 294, 311, 329, 333, 362, 387, 436, 527, 562,\
 598, 615, 648, 653, 713, 767, 772]
initiate(array, 'Fly02_NoHaltere_F03', current)

array = [ 34, 108, 118, 169, 228, 302, 344, 400, 444, 492, 507, 509, 527, 565,\
 575, 630, 713, 747, 774, 806, 826]
initiate(array, 'Fly05_Right_F03', current)

array = [43, 139, 170, 176, 189, 192, 197, 224, 271, 279, 282, 345, 350, 427,\
 476, 481, 525, 534, 586, 600, 620]
initiate(array, 'Fly06_Left_F01', current)

array = [ 91, 121, 218, 248, 303, 345, 373, 469, 488, 509, 528, 539, 608, 622,\
 627, 632, 679, 764, 824, 832, 878]
initiate(array, "Fly01_F02", current)

array = [ 38,  92, 176, 177, 187, 365, 382, 388, 395, 464, 481, 504, 506, 538,\
 540, 603, 629, 641, 657, 663, 728]
initiate(array, "Fly02_F03", current)

array = [ 12,  55,  65, 114, 143, 159, 177, 226, 270, 344, 381, 398, 466, 491,\
 517, 568, 582, 602, 651]
initiate(array, "Fly03_F02", current)

array = [152, 189, 218, 250, 257, 268, 308, 339, 398, 471, 643, 736, 742, 752,\
 774, 843, 858, 868]
initiate(array, "Fly04_F01", current)

array = [2,  29, 119, 123, 191, 216, 226, 235, 269, 315, 372, 399, 413, 429,\
 433, 482, 506, 567, 634, 664]
initiate(array, "Fly05_F03", current)

array = [ 89, 117, 142, 211, 226, 261, 262, 297, 336, 412, 428, 435, 515,\
 535, 542, 626, 649, 676, 702, 716, 749]
initiate(array, "Fly06_F02", current)

array = [  8,  50,  76, 124, 129, 198, 210, 231, 278, 304, 306, 310, 349,\
 360, 398, 410, 437, 439, 502, 507]
initiate(array, "Fly07_F01", current)

array = [ 50,  69,  79,  82,  97, 110, 176, 179, 202, 221, 291, 319, 332,\
 379, 387, 432, 464, 468, 535, 577, 584]
initiate(array, "Fly08_F03", current)

array = [ 28,  33,  51,  61,  62,  94, 148, 155, 173, 198, 215, 229, 291,\
 323, 324, 378, 427, 428, 437]
initiate(array, "Fly10_F02", current)

# array = [2,  18,  70,  74, 109, 119, 223, 279, 311, 317, 410, 440, 463,\
# 471, 495, 520, 550, 578, 589, 597, 682];
# data = extract_data("Fly01_F1xypts.csv", array)


# array = [ 30,   46,  182,  200,  214, 224,  314,  387,  432,  442, 529,\
#  556,  674,  686,  751,  753,  845,  893,  935, 1000];
# data = extract_data("Fly01_F2xypts.csv", array)


# array =[ 50, 162, 178, 200, 216, 248, 262, 342, 360, 367, 376, 412, 425,\
# 489, 510, 557, 675, 810, 817, 864];
# data = extract_data("Fly01_F3xypts.csv", array)


# array = [ 34, 130, 140, 148, 250, 360, 406, 457, 508, 618, 621, 650, 677,\
# 684, 764, 768, 778, 810];
# data = extract_data("Fly02_F1xypts.csv", array)

# array = [10,  27,  78, 175, 285, 306, 397, 472, 499, 500, 507, 513, 687,\
# 704, 711, 718, 732, 779, 783, 867, 910];
# data = extract_data("Fly02_F2xypts.csv", array)


# array =[ 26, 130, 160, 166, 178, 192, 242, 310, 362, 393, 398];
# data = extract_data("Fly02_F3xypts.csv", array)



# array = [13,   42,   53,  190,  236,  439,  541,  582,  626,  654,  722,\
# 730,  844,  887,  900,  914,  962,  991, 1053, 1063, 1164];
# data = extract_data("Fly02_F01xypts.csv", array)


# array = [2,  33,  51,  61, 114, 130, 143, 178, 244, 349, 401, 403, 521];
# data = extract_data("Fly02_F02xypts.csv", array)


# array =[7, 103, 153, 223, 233, 264, 274, 294, 320, 338, 340, 350, 363, 414,\
# 435, 534, 551];
# data = extract_data("Fly02_F03xypts.csv", array)

# array =[ 53, 162, 225, 252, 268, 315, 319, 362, 423, 446, 468, 505, 507,\
# 519, 543];
# data = extract_data("Fly02_F04xypts.csv", array)


# array = [ 29, 101, 124, 134, 139, 170, 353, 386, 394, 400, 444, 477, 523,\
#529, 600, 776, 780, 835, 837, 907, 938];
# data = extract_data("Fly01_F1xypts.csv", array)

# array = [ 3,  32,  54,  92, 153, 186, 224, 258, 262, 267, 282, 306, 318, \
#329, 371, 393, 473, 531, 555, 612, 615];
# data = extract_data("Fly01_F2xypts.csv", array)


# array =[ 34, 140, 186, 333, 400, 422, 432, 462, 470, 500, 534, 580, 600,\
#605, 633, 640, 680, 750, 841, 930, 981];
# data = extract_data("Fly01_F3xypts.csv", array)
