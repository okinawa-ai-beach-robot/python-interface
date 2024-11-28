# Okinawa AI Beach Robot Python Interface

## Initial setup
[It is recommended](https://realpython.com/python-virtual-environments-a-primer/#why-do-you-need-virtual-environments) to use virtual environments. Start by creating a virtual environment then installing the beachbot package without dependencies in edit mode (allows you to make use of any recent changes without reinstalling). This will avoid installing any conflicting packages with jetpack on the jetson or otherwise.
```
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

Alternatively, if desired to reuse pip packages installed system-wide, the following can be used:
```
python3 -m venv --system-site-packages .venv
. .venv/bin/activate
pip install -e .
```

So for standard production installations this would just mean `pip install beachbot`


### Configuration of Data Folders
Current configuration can be inspecte by:
```
import beachbot
print(beachbot.config)
```

Example for setup of path variables in `.bashrc`, e.g. ubuntu setup for local development folder in /home/[username]/src/OIST_BC/`:
```
export BEACHBOT_HOME=${HOME}/src/OIST_BC/
export BEACHBOT_CACHE=${BEACHBOT_HOME}/Cache
export BEACHBOT_CONFIG=${BEACHBOT_HOME}/Config
export BEACHBOT_LOGS=${BEACHBOT_HOME}/Logs
export BEACHBOT_MODELS=${BEACHBOT_HOME}/Models
export BEACHBOT_MODELS=${BEACHBOT_HOME}/Datasets

```




### System Dependencies
The following commands need to be exeuted to install required software dependencies.
Video IO and codecs:
```
sudo apt install v4l-utils
sudo apt-get install ffmpeg x264 libx264-dev
```

## Troubleshooting
Assuming you follow the guide above for installing on the Jetson, this should not be necessary, but in the event you see any errors, the information below may be of use:

On jetson, python-opencv is installed by nvidia and could be hidden by the pip version.
The pip-version does not support the jetson camera, thus, we have to uninstall all opencv pip versions from the jetson after reinstall of our package:
```
pip uninstall opencv-python
```
