import os
import sys

project = sys.argv[1]

# Change config.yaml
# Change pose_config.yaml
# Change pose_config.yaml
def change_names(project_name = project):
    file1 = open(project_name + "/config.yaml", 'r')
    lines = file1.readlines()
    file1.close()
    file2 = open(project_name + "/config.yaml", 'w')
    task = ""
    date = ""
    for i in lines:
        if(i.startswith('project_path')):
            file2.write('project_path: ' + '/home/sane/adityaiyer/' + project_name + '\n')
            continue
        else:
            file2.write(i)
        if(i.startswith('Task')):
            task = i.split(' ')[1]
        if(i.startswith('date')):
            date = i.split(' ')[1]
    task = task[:-1]
    date = date[:-1]
    file2.close()
    folder = project_name + "/dlc-models/iteration-0/" + task + date + "-trainset95shuffle1/"
    file3 = open(folder + "train/pose_cfg.yaml", 'r')
    lines = file3.readlines()
    file3.close()
    file4 = open(folder + "train/pose_cfg.yaml", 'w')
    # Change init_weights, and project_path
    for i in lines:
        if(i.startswith('project_path')):
            file4.write('project_path: ' + '/home/sane/adityaiyer/' + project_name + '\n')
            continue
        elif(i.startswith('init_weights')):
            file4.write('init_weights: ' + 'home/sane/adityaiyer/deeplabcut/pose_estimation_tensorflow/models/pretrained/resnet_v1_50.ckpt\n')
        else:
            file4.write(i)
    file4.close()


    file5 = open(folder + "test/pose_cfg.yaml", 'r')
    lines = file5.readlines()
    file5.close()
    file6 = open(folder + "test/pose_cfg.yaml", 'w')
    # Change init_weights, and project_path
    for i in lines:
        if(i.startswith('init_weights')):
            file6.write('init_weights: ' + 'home/sane/adityaiyer/deeplabcut/pose_estimation_tensorflow/models/pretrained/resnet_v1_50.ckpt\n')
        else:
            file6.write(i)
    file6.close()
    print("Changed config.yaml and the 2 pose_cfg.yaml files")

if __name__ == "__main__":
    change_names()
