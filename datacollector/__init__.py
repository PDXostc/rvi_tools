"""
Copyright (C) 2014, Jaguar Land Rover

This program is licensed under the terms and conditions of the
Mozilla Public License, version 2.0.  The full text of the 
Mozilla Public License is at https://www.mozilla.org/MPL/2.0/

Maintainer: Rudolf Streif (rstreif@jaguarlandrover.com) 
"""

"""
Initialize tools package.
"""

import sys, os, logging
import logging.config
import settings


# setup logging
logging.config.dictConfig(settings.LOGGING)
# use tools logger for general logging
__TOOLS_LOGGER__ = logging.getLogger('tools')


