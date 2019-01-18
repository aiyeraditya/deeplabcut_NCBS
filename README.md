# deeplabcut_NCBS
# Using DeepLabCut @ NCBS

This document outlines the protocol to train DeepLabCut for using on the Pakeeza Cluster at NCBS from a computer set up with Ubunutu 16.04

## Getting Started

# Installing Anaconda
Run the following to check if conda is installed on your system
```
conda info
```
If not, run the following on Terminal.
```
cd /tmp
curl -O https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
sha256sum Anaconda3-5.0.1-Linux-x86_64.sh
```
The sha256sum is simply for checking the integrity of the downloaded packages. Check the output against the hashes available at the [Anaconda with Python 3 on 64-bit Linux page](https://docs.continuum.io/anaconda/hashes/lin-3-64)

```
bash Anaconda3-5.0.1-Linux-x86_64.sh
```
Review the License Agreement and type 'yes' when prompted (/if you are cool with the contents of the license Agreement, that is/)

```
source ~/.bashrc
conda list
```

'conda list' is to confirm if conda has been installed properly.

#Create an environment

```
conda create deeplabcut py36 python=3.6 anaconda
```
Feel free to rename 'deeplabcut' from the above line to whatever you want to name your environment as. If you do so, replace 'deeplabcut' in the next line to the name of your environment

```
source activate deeplabcut
python --version
```
The output for this should indicate that Python 3.6 is initialised.

Now, let's install deeplabcut and its dependencies

# Installing deeplabcut, wxPython, and tensorflow

```
pip install deeplabcut --user
pip install https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04/wxPython-4.0.3-cp36-cp36m-linux_x86_64.whl --user
pip install --ignore-installed tensorflow==1.10 --user
```
I recommend the installation of the CPU version of Tensorflow. All the major training will be done on Pakeeza GPU clusters.

If you got this far, Great! Now you are set-up for creating your project and training

# Setting Up Training Set
If you want to use the DeepLabCut GUI, refer to the DeepLabCut UserOverViewGuide for creating the training set

If you have used DLT-DV (Ty Hedrick) to label the images, do the following:
```
MUST ADD STUFF HERE
```

Once that is set up, you are ready to use Pakeeza for training the network

# Setting Up Files on Pakeeza

Transfer the entire project folder to Pakeeza using this line on Terminal. Open Terminal from the parent directory of the projcet folder and run this.
```
scp -r <project-folder> adityaiyer@pakeeza:~/
```

For the password, please mail adityaiyer@ncbs.res.in or meet me in the lab

Run the following to confirm the files have been transfered:
```
ssh adityaiyer@pakeeza.ncbs.res.in
export http_proxy=http://proxy.ncbs.res.in:3128
export https_proxy=http://proxy.ncbs.res.in:3128
cd /home/sane/adityaiyer
ls
```
You should see your project-folder listed.

Now, project paths in the config files have to be changed to reflect their new location on the Pakeeza servers. To do this, the python script change_name.py will be used
```
python change_name.py <project-folder>
```

## Authors

* **Aditya Iyer**

## License


## Acknowledgments

* DeepLabCut
* DLT-DV
* Abin Ghosh
* Shivansh Dave
