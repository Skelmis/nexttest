__version__ = "0.0.1"

import logging
import sys
from collections import namedtuple


logging.getLogger(__name__).addHandler(logging.NullHandler())
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=0, minor=0, micro=1, releaselevel="final", serial=0)


if sys.version_info[1] < 8:
    raise RuntimeError("This package requires python 3.8 or higher.")
