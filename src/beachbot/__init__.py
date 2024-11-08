from __future__ import annotations
from importlib.metadata import version as _version, PackageNotFoundError
from . import manipulators
from . import sensors
from . import ai
from . import utils

try:
    __version__ = _version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["manipulators", "sensors", "ai", "utils"]  # "sensors", "platforms"
