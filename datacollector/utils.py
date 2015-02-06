"""
Copyright (C) 2014, Jaguar Land Rover

This program is licensed under the terms and conditions of the
Mozilla Public License, version 2.0.  The full text of the 
Mozilla Public License is at https://www.mozilla.org/MPL/2.0/

Maintainer: Rudolf Streif (rstreif@jaguarlandrover.com) 
"""

"""
GPS Data Collector

This tool collects data from the gpsd daemon and stores it in the RVI Backend
database using the Django ORM.
"""

import settings



def get_setting(name, default=None):
    try:
        value = getattr(settings, name, default)
    except AttributeError:
        rvi_logger.error('RVI Server: %s not defined. Check settings!', name)
        sys.exit(1)
    return value
        

def get_settings():
        # get settings from configuration
        # service edge url
        conf = {}
        
        conf['VIN_DEFAULT'] = get_setting("VIN_DEFAULT", "rvidefault")
        
        conf['TRACKING_GPS_ENABLE']   = get_setting("TRACKING_GPS_ENABLE", True)
        conf['TRACKING_GPS_INTERVAL'] = get_setting("TRACKING_GPS_INTERVAL", 5)

        conf['TRACKING_FILE_ENABLE']    = get_setting("TRACKING_FILE_ENABLE", True)
        conf['TRACKING_FILE_INTERVAL']  = get_setting("TRACKING_FILE_INTERVAL", 5)
        conf['TRACKING_FILE_NAME']      = get_setting("TRACKING_FILE_NAME")
        conf['TRACKING_FILE_COLUMNS']   = get_setting("TRACKING_FILE_COLUMNS", 'latitude longitude occupancy timestamp')
        conf['TRACKING_FILE_DELIMITER'] = get_setting("TRACKING_FILE_DELIMITER", ' ')


        conf['TRACKING_DB_PUBLISH']   = get_setting("TRACKING_DB_PUBLISH", False)
        conf['TRACKING_DB_NAME']      = get_setting("TRACKING_DB_NAME", "rvidata.db")

        conf['TRACKING_MQ_PUBLISH']   = get_setting("TRACKING_MQ_PUBLISH", False)
        conf['TRACKING_MQ_URL']       = get_setting("TRACKING_MQ_URL", "localhost:9092")
        conf['TRACKING_MQ_TOPIC']     = get_setting("TRACKING_MQ_TOPIC", "rvi")

        conf['TRACKING_RVI_PUBLISH']    = get_setting("TRACKING_RVI_PUBLISH", False)
        conf['TRACKING_RVI_NODE_URL']   = get_setting("TRACKING_RVI_NODE_URL")
        conf['TRACKING_RVI_BACKEND_ID'] = get_setting("TRACKING_RVI_BACKEND_ID")



        return conf
