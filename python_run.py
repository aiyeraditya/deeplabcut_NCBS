import deeplabcut
print("DEEPLABCUT IMPORTED")
gputouse = 2
project_name = "YAY"
video_path = 'home/sane/adityaiyer/video.avi'
config_path = 'home/sane/adityaiyer/' + project_name + '/config.yaml'
deeplabcut.train_network(config_path, shuffle = 1, gputouse = 2, save_iters = 50000, displayiters = None)
deeplabcut.evaluate_network(config_path,Shuffles=[1], plotting=True)
deeplabcut.analyze_videos(config_path,[video_path],shuffle=1, save_as_csv=True)
deeplabcut.create_labeled_video(config_path, [video_path])
