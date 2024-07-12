Robot interface package template

Install in dev mode via `pip install -e .`
(Will create links to source files, so you can edit in-place, without reinstalling)

## Troubleshooting
On jetson, python-opencv is installed by nvidia and could be hidden by the pip version.
The pip-version does not support the jetson camera, thus, we have to uninstall all openvc pip versions from the jetson after resintall of our package:
```
pip uninstall opencv-python
```
