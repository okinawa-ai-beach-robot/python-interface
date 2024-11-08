from __future__ import annotations
from importlib.metadata import version as _version, PackageNotFoundError
import logging
import os
import sys
from . import manipulators
from . import sensors
from . import ai
from . import utils

try:
    __version__ = _version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["manipulators", "sensors", "ai", "utils"]  # "sensors", "platforms"

def get_base_path():
    if "BEACHBOT_HOME" in os.environ:
        return os.environ.get("BEACHBOT_HOME")
    else:
        logger.warning(
            "BEACHBOT_HOME environment variable not specified, fall back to home path "
            + os.environ["HOME"]
        )
        return os.environ["HOME"]

def get_model_path():
    return get_base_path() + os.path.sep + "Models"


def get_dataset_path():
    return get_base_path() + os.path.sep + "Datasets"


def get_data_path():
    return get_base_path() + os.path.sep + "Data"
