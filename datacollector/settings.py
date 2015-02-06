"""
Copyright (C) 2014, Jaguar Land Rover

This program is licensed under the terms and conditions of the
Mozilla Public License, version 2.0.  The full text of the 
Mozilla Public License is at https://www.mozilla.org/MPL/2.0/

Maintainer: Rudolf Streif (rstreif@jaguarlandrover.com) 
"""

"""
Tools settings for rvi project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)



# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
             'level': 'DEBUG',
             'class': 'logging.StreamHandler',
             'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'rvitools.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'tools': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


# VIN
# not all data sources provide a VIN, this is the default if not provided
VIN_DEFAULT = "rvivin"

# GPS Source
# Enable/Disable the GPS Source
TRACKING_GPS_ENABLE = False
# Polling Interval for the GPS Source
TRACKING_GPS_INTERVAL = 5

# File Source
# Enable/Disable the File Source
TRACKING_FILE_ENABLE = True
# Polling Interval for the File Source
TRACKING_FILE_INTERVAL = 1
# Path to data files, can have wildcards for multiple files
# For each file an independent File Source will be spawned
TRACKING_FILE_NAME = '../../testdata/cabspottingdata/new_aj*'

# Database Sink
# Enable/Disable the Database Sink
RVI_TRACKING_DB_PUBLISH = True
# Name of the SQLite database file
RVI_TRACKING_DB_NAME = "rvidata.db"

# RVI Sink
# Enable/Disbale the RVI Sink
TRACKING_RVI_PUBLISH = True
# RVI Node to connect to (can be local or remote)
TRACKING_RVI_NODE_URL = 'http://127.0.0.1:8801'
# RVI Node to send data to
TRACKING_RVI_BACKEND_ID = 'jlr.com/backend'

# Message Queue Sink
# Enable/Disable Message Queue Sink
TRACKING_MQ_PUBLISH = True
# Kafka URL (can be local or remote)
TRACKING_MQ_URL = "localhost:9092"
# Kafka topic to publish messages to
TRACKING_MQ_TOPIC = "rvi"

