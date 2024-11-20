# Okinawa AI Beach Robot Python Interface

## Initial setup
[It is recommended](https://realpython.com/python-virtual-environments-a-primer/#why-do-you-need-virtual-environments) to use virtual environments. Start by creating a virtual environment then installing the beachbot package without dependencies in edit mode (allows you to make use of any recent changes without reinstalling). This will avoid installing any conflicting packages with jetpack on the jetson or otherwise.
```
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

So for standard production installations this would just mean `pip install beachbot`

## Troubleshooting
Assuming you follow the guide above for installing on the Jetson, this should not be necessary, but in the event you see any errors, the information below may be of use:

On jetson, python-opencv is installed by nvidia and could be hidden by the pip version.
The pip-version does not support the jetson camera, thus, we have to uninstall all opencv pip versions from the jetson after reinstall of our package:
```
pip uninstall opencv-python
```
