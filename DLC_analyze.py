import os
import deeplabcut

current = os.getcwd()

str = '/media/Aditya_Backup/CINE_FILES/Set10_27-28Feb/28Feb/AVI_DLC/View1/'
list = os.listdir('/media/Aditya_Backup/CINE_FILES/Set10_27-28Feb/28Feb/AVI_DLC/View1/')
videos = []
for i in list:
    videos.append(str + i)

# Now videos has path for all
config = 'flying_View1...../config.yaml'
deeplabcut.analyze_videos(config, videos, save_as_csv = True)
os.chdir(current)
deeplabcut.create_labeled_videos(config, videos)
os.chdir(current)

str = '/media/Aditya_Backup/CINE_FILES/Set10_27-28Feb/28Feb/AVI_DLC/View2/'
list = os.listdir('/media/Aditya_Backup/CINE_FILES/Set10_27-28Feb/28Feb/AVI_DLC/View2/')
videos = []
for i in list:
    videos.append(str + i)

# Now videos has path for all
config = 'flying_View2...../config.yaml'
deeplabcut.analyze_videos(config, videos, save_as_csv = True)
os.chdir(current)
deeplabcut.create_labeled_videos(config, videos)
os.chdir(current)

str = '/media/Aditya_Backup/CINE_FILES/Set10_27-28Feb/28Feb/AVI_DLC/View3/'
list = os.listdir('/media/Aditya_Backup/CINE_FILES/Set10_27-28Feb/28Feb/AVI_DLC/View3/')
videos = []
for i in list:
    videos.append(str + i)

# Now videos has path for all
config = 'flying_View3...../config.yaml'
deeplabcut.analyze_videos(config, videos, save_as_csv = True)
os.chdir(current)
deeplabcut.create_labeled_videos(config, videos)
os.chdir(current)
