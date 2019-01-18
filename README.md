# deeplabcut_NCBS
#Using DeepLabCut @ NCBS

This document outlines the protocol to train DeepLabCut for using on the Pakeeza Cluster at NCBS

## Getting Started

# Installing Anaconda
Run the following to check if conda is installed on your system
```
conda info
```
If not, run the following on Terminal. This is for Ubuntu 16.04 LTS
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
The output for this should indicate that Python 3.6 is initialised


## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
