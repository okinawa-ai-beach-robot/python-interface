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
    pass


__all__ = ["manipulators", "sensors", "ai"]  # "sensors", "platforms"


logger = logging.getLogger(__name__)
logging.basicConfig(filename=__name__+'.log', level=logging.INFO)

_handler = logging.StreamHandler(sys.stdout)
_handler.setLevel(logging.INFO)
_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_handler.setFormatter(_formatter)
logger.addHandler(_handler)

from . import manipulators
from . import sensors
from . import ai

from . import utils
