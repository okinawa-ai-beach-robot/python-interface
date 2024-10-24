# Okinawa AI Beach Robot Python Interface

## Installation
The pyproject.toml implements dependency-groups as per [PEP735](https://peps.python.org/pep-0735/#copyright)

As this is not currently implemented into [pip](https://github.com/pypa/pip/issues/12963), we are currently using the PEP735 author's workaround pip package [dependency-groups](https://pypi.org/project/dependency-groups/). Assuming adoption to pip in the future, the installation will be updated accordingly.

### Initial setup
[It is recommended](https://realpython.com/python-virtual-environments-a-primer/#why-do-you-need-virtual-environments) to use virtual environments. Start by creating a virtual environment then installing the beachbot package without dependencies in edit mode (allows you to make use of any recent changes without reinstalling). This will avoid installing any conflicting packages with jetpack on the jetson or otherwise.
```
python3 -m venv .venv
. .venv/bin/activate
pip install --no-deps -e .
```

So for standard production installations this would just mean `pip install beachbot`

The dependency groups define two alternative dependency groups that are not meant for production, but for development.

`pip list` should only show beachbot, setuptools, and pip itself.

### Jetson
The jetson group contains all the same strict dependencies from the default production ones, but removes packages that are already installed via jetpack such that these optimized packages (e.g. opencv, torch, etc.) are used instead of the standard ones on pip.

```
pip install dependency-groups
pip-install-dependency-groups jetson
```

### Dev
The dev group contains the same dependencies as the default production ones, except allows for a much broader range of versions such that one of the developers can keep using the existing dependencies from their system-wide pip. (not recommended as development using undefined dependencies will lead to instances of code working for the developer and not for others who do not share the same dependencies)

## Troubleshooting
Assuming you follow the guide above for installing on the Jetson, this should not be necessary, but in the event you see any errors, the information below may be of use:

On jetson, python-opencv is installed by nvidia and could be hidden by the pip version.
The pip-version does not support the jetson camera, thus, we have to uninstall all opencv pip versions from the jetson after reinstall of our package:
```
pip uninstall opencv-python
```
