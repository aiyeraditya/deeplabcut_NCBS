# Convert dlc files to dltdv
import os
import numpy as np

# This Function Reads the csv file having DLC labeled points for all frames
def get_data(file, mm):
    # mm is the camera ID
    # t contains the Y pixel resolution for each camera
    t = [0, 800, 1080, 800]
    lines = file.readlines()
    file.close()
    xypts = []
    for i in range(3, len(lines)):
        count = 0
        data = lines[i].split(',');
        data1 = [0 for i in range(12)];
        for j in range(1,len(data), 3):
            x = data[j]
            y = data[j + 1]
            likelihood = float(data[j + 2])
            # Choose points only if likelihood is high
            if(likelihood <= 0.5):
                data1[count] = 'NaN'
                data1[count + 1] = 'NaN'
            else:
                data1[count] = x;
                data1[count + 1] = str(t[mm] - float(y));
                # This is because DLT has origin at bottom left and OpenCV has
                # origin at top left
            count = count + 2
        xypts.append(data1)
    return xypts

# This function reads an array of coordinates of
# all points labeled in a frame and returns appropriate x,y coordinates
def func(i,j, View):
    x1 = View[j][i]
    y1 = View[j][i + 1]
    return x1, y1


# This function outputs two things; x,y,z coordinates and the dlt residual
def get_dlt(cam_pts_str, dlt):
    cam_pts = [[0,0] for j in range(len(cam_pts_str))]
    for i in range(len(cam_pts_str)):
        for j in [0,1]:
            cam_pts[i][j] = float(cam_pts_str[i][j])
    n1 = len(dlt) # n1 Number of Cameras
    Y = [0 for i in range(2*n1)]
    for i in range(n1):
        Y[2*i] = cam_pts[i][0] - dlt[i][3]
        Y[2*i + 1] = cam_pts[i][1] - dlt[i][7]
    # Creating the matrix Y in Y = AX
    Y = np.transpose(Y)
    A = [[0,0,0] for i in range(2*n1)]
    for i in range(n1):
        for j in range(3):
            A[2*i][j] = dlt[i][j] - cam_pts[i][0]*dlt[i][8+j]
            A[2*i + 1][j] = dlt[i][j + 4] - cam_pts[i][1]*dlt[i][8+j]
    # Creating the Matrix A in Y = AX
    # Solving for Y = AX
    solve = np.linalg.lstsq(A, Y, rcond=-1)
    xyz = solve[0]
    residual = 0
    # DLTDV7 uses a different definition of residual than the one output by
    # the matrix. This definition is more suited for image based systems
    for i in range(n1):
        # This is from Kwon3D and DLTdv7.m from Ty Hedrick Lab
        u = (xyz[0]*dlt[i][0]  + xyz[1]*dlt[i][1] + xyz[2]*dlt[i][2] + \
        dlt[i][3])/(xyz[0]*dlt[i][8]  + xyz[1]*dlt[i][9] + xyz[2]*dlt[i][10] \
        + 1)
        v = (xyz[0]*dlt[i][4]  + xyz[1]*dlt[i][5] + xyz[2]*dlt[i][6] + \
        dlt[i][7])/(xyz[0]*dlt[i][8]  + xyz[1]*dlt[i][9] + xyz[2]*dlt[i][10] \
        + 1)
        delu2 = (u - cam_pts[i][0])**2
        delv2 = (v - cam_pts[i][1])**2
        sd = (delu2 + delv2)
        residual = residual + sd
        residual = np.sqrt(residual)/np.sqrt(2*n1 - 3)
        # The degrees of freedom with n cameras is given by 2n - 3
    return xyz, residual

# This function gets DLT coefficients from a csv file
def get_coeff(filename):
    file = open(filename);
    lines = file.readlines()
    file.close()
    coeff = []
    for i in range(0, len(lines)):
        k = lines[i].split(',')
        c = [0 for l in range(len(k))]
        for j in range(len(k)):
            c[j] = float(k[j])
        coeff.append(c)
    coeff = np.transpose(coeff)
    return coeff

# This function cretes the csv files that can be read by
def write_data(filename, date, coeff_file):
    # DLC files are seperate for each cameras. The following reads all of them
    file = open(date + '/View1/' + filename + '_V1DeepCut_resnet50_flying_V1\
    Mar3shuffle1_1030000.csv');
    View1 = get_data(file, 1)
    file = open(date + '/View2/' + filename + '_V2DeepCut_resnet50_flying_V2\
    Mar3shuffle1_1030000.csv');
    View2 = get_data(file, 2)
    file = open(date + '/View3/' + filename + '_V3DeepCut_resnet50_flying_V3\
    Mar3shuffle1_1030000.csv');
    View3 = get_data(file, 3)
    l = len(View1)
    os.system('mkdir ' + filename);
    dlt_coeff = get_coeff(coeff_file)
    # dlt1 is the DLT coefficients for first and third camera
    dlt1 = []
    dlt1.append(dlt_coeff[0])
    dlt1.append(dlt_coeff[2])
    # DLTdv needs 4 files. Xypoints, offsets, xyzpoints and xyzres
    f = open(filename + '/' + filename + 'xypts.csv', 'w')
    count = 0
    # First Line
    f.write('pt1_cam1_X,pt1_cam1_Y,pt1_cam2_X,pt1_cam2_Y,pt1_cam3_X,pt1_cam3_Y,\
    pt2_cam1_X,pt2_cam1_Y,pt2_cam2_X,pt2_cam2_Y,pt2_cam3_X,pt2_cam3_Y,\
    pt3_cam1_X, pt3_cam1_Y,pt3_cam2_X,pt3_cam2_Y,pt3_cam3_X,pt3_cam3_Y,\
    pt4_cam1_X,pt4_cam1_Y, pt4_cam2_X,pt4_cam2_Y,pt4_cam3_X,pt4_cam3_Y,\
    pt5_cam1_X,pt5_cam1_Y,pt5_cam2_X,pt5_cam2_Y,pt5_cam3_X,pt5_cam3_Y,\
    pt6_cam1_X,pt6_cam1_Y,pt6_cam2_X,pt6_cam2_Y,pt6_cam3_X,pt6_cam3_Y')
    for i in range(l):
        count = 0
        for j in range(6):
            [x1, y1] = func(2*j,i,View1)
            [x2, y2] = func(2*j,i,View2)
            [x3, y3] = func(2*j,i, View3)
            c = 0
            for k in [x1, x2, x3]:
                if k == 'NaN':
                    # To find if there is no label for some points
                    c += 1
            if(c == 0):
                # If all points are labeled
                xyz_a, residual_a = get_dlt([[x1, y1], [x2, y2], [x3, y3]],
                dlt_coeff)
                xyz = []
                residue = []
                # Choose the 2 points with least residual if DLT residual of
                # All three points is greater than 2.00
                if(residual_a > 2.00):
                    xyz1, residual1 = get_dlt([[x1, y1],[x2, y2]],\
                    dlt_coeff[0:2])
                    xyz.append(xyz1)
                    residue.append(residual1)
                    xyz1, residual1 = get_dlt([[x1, y1], [x3, y3]], dlt1)
                    xyz.append(xyz1)
                    residue.append(residual1)
                    xyz1, residual1 = get_dlt([[x2, y2], [x3, y3]],\
                    dlt_coeff[1:3])
                    xyz.append(xyz1)
                    residue.append(residual1)
                    min_index = np.argmin(residue)
                    if(min_index == 0):
                        x3 = 'NaN'
                        y3 = 'NaN'
                    elif(min_index == 1):
                        x2 = 'NaN'
                        y2 = 'NaN'
                    else:
                        x1 = 'NaN'
                        y1 = 'NaN'
            if(count != 0):
                # End of Only one point. Still on the same frame
                f.write(',')
            else:
                # End Of Line
                f.write('\n')
            f.write(x1 + ',' + y1 + ',' + x2 + ',' + y2 + ',' + x3 + ',' + y3)
            count = count + 1
    f.close()

    # Writing Other Files with Default Values
    f = open(filename + '/' +filename +'offsets.csv', 'w')
    f.write('Cam1_offset, Cam2_offset, Cam3_offset\n')
    for i in range(l):
        f.write('0.0,0.0,0.0\n')
    f.close()

    f = open(filename + '/' +filename + 'xyzres.csv', 'w')
    f.write('pt1_dltres,pt2_dltres,pt3_dltres,pt4_dltres,pt5_dltres, \
    pt6_dltres\n')
    for i in range(l):
        f.write('NaN,NaN,NaN,NaN,NaN,NaN\n')
    f.close()

    f = open(filename + '/' + filename + 'xyzpts.csv', 'w')
    f.write('pt1_X,pt1_Y,pt1_Z,pt2_X,pt2_Y,pt2_Z,pt3_X,pt3_Y,pt3_Z,pt4_X,\
    pt4_Y,pt4_Z,pt5_X,pt5_Y,pt5_Z,pt6_X,pt6_Y,pt6_Z\n')
    for i in range(l):
        f.write('NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,NaN,\
        NaN,NaN,NaN,NaN\n')
    f.close()

# This function reads the csv files that are available and converts those files
def get_filename(date, coeff_file):
    files = os.listdir(date + '/View1')
    files = [i for i in files if i.endswith('.csv')]
    #files now has all the csv files
    for i in range(len(files)):
        filenames = files[i].split('_V')
        # Filenames are like Fly01_F01_V1. Splitting at _V gives
        # The string 'Fly01_V1'
        write_data(filenames[0], date, coeff_file)
        print(filenames[0])

# Initiates the Program
get_filename('08-09JanAnalysed/AVI_09Jan', 'IC_dltCoefs09Jan.csv')
