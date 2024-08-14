#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""Python Package Template"""
from __future__ import annotations
from importlib.metadata import version as _version, PackageNotFoundError
import logging
import os, sys


try:
    __version__ = _version(__name__)
except PackageNotFoundError:
    __version__="0.0.0"


__all__ = ["manipulators", "sensors", "ai"]  # "sensors", "platforms"



def get_base_path():
    if 'BEACHBOT_HOME' in os.environ:
        return os.environ.get('BEACHBOT_HOME')
    else:
        logger.warning("BEACHBOT_HOME environment variable not specified, fall back to home path " + os.environ['HOME'])
        return os.environ['HOME']
    
logger = logging.getLogger(__name__)
logging.basicConfig(filename=get_base_path() + os.path.sep+__name__+'.log', level=logging.INFO)

_handler = logging.StreamHandler(sys.stdout)
_handler.setLevel(logging.INFO)
_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_handler.setFormatter(_formatter)
logger.addHandler(_handler)


def get_model_path():
    return get_base_path() + os.path.sep + "Models"
def get_dataset_path():
    return get_base_path() + os.path.sep + "Datasets"
def get_data_path():
    return get_base_path() + os.path.sep + "Data"

from . import manipulators
from . import sensors
from . import ai

from . import utils
