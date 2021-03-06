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
# Polling Interval for the File Source (in seconds, can be a fraction)
TRACKING_FILE_INTERVAL = 0.01
# Path to data files, can have wildcards for multiple files
# For each file an independent File Source will be spawned
TRACKING_FILE_NAME = '../../testdata/cabspottingdata/new_a*'

# Munic.box Source
# Enable/Disable the Munic.box Source
TRACKING_MUNICBOX_ENABLE = True
# URL to listen on <host>:<port>, use 0.0.0.0 for all interfaces
TRACKING_MUNICBOX_URL = '0.0.0.0:8080'

# Database Sink
# Enable/Disable the Database Sink
TRACKING_DB_PUBLISH = False
# Name of the SQLite database file
TRACKING_DB_NAME = "../rvidata.db"

# RVI Sink
# Enable/Disbale the RVI Sink
TRACKING_RVI_PUBLISH = True
# RVI Node to connect to (can be local or remote)
#TRACKING_RVI_NODE_URL = 'http://127.0.0.1:8801'
TRACKING_RVI_NODE_URL = 'http://127.0.0.1:8811'
# RVI Node to send data to
TRACKING_RVI_BACKEND_ID = 'jlr.com/backend'

# Message Queue Sink
# Enable/Disable Message Queue Sink
TRACKING_MQ_PUBLISH = False
# Kafka URL (can be local or remote)
# TRACKING_MQ_URL = "localhost:9092"
TRACKING_MQ_URL = "192.168.100.144:9092"
# Kafka topic to publish messages to
TRACKING_MQ_TOPIC = "rvi"

