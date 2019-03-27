# Setting up DeepLabCut on Pakeeza

* Copy the DeepLabCut folder to your home directory

Open terminal from the folder containing deeplabcut folder as downloaded from github on your local computer and run the following
```
scp -r deeplabcut <username>@pakeeza:~/
```
# Get Anaconda Running On Pakeeza
* Login to your account on pakeeza
```
ssh <username>@pakeeza
[Enter Password]
```

Pakeeza runs CentOS 7. Let's install anaconda for CentOS.
```
export http_proxy=http://proxy.ncbs.res.in:3128
export https_proxy=http://proxy.ncbs.res.in:3128
curl -O https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh
sha256sum Anaconda3-5.3.1-Linux-x86_64.sh
```
The sha256sum is simply for checking the integrity of the downloaded packages. Check the output against the hashes available at the [Anaconda with Python 3 on 64-bit Linux page](https://docs.continuum.io/anaconda/hashes/lin-3-64)

```
bash Anaconda3-5.3.1-Linux-x86_64.sh
```
Review the License Agreement and type 'yes' when prompted (/if you are cool with the contents of the license Agreement, that is/)

```
source ~/.bashrc
conda list
```

'conda list' is to confirm if conda has been installed properly.

## Create an environment

```
conda create deeplabcut py36 python=3.6 anaconda
source activate deeplabcut
python --version
```
The output for this should indicate that Python 3.6 is initialised.

Install all dependencies for DeepLabCut

```
pip install deeplabcut
```

# Checking If DeepLabCut works

Run the following to confirm that DeepLabCut works fine.
```
source activate deeplabcut
python
>> import deeplabcut
```

If deeplabcut imports without any issues, you are good to go! Continue with README.md, changing adityaiyer to <username> wherever necessary

Good Luck!!
