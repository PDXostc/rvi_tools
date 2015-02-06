"""
Copyright (C) 2014, Jaguar Land Rover

This program is licensed under the terms and conditions of the
Mozilla Public License, version 2.0.  The full text of the 
Mozilla Public License is at https://www.mozilla.org/MPL/2.0/

Maintainer: Rudolf Streif (rstreif@jaguarlandrover.com) 
"""

"""
GPS Data Collector

Database Sink that stores reports to the database.
It uses the PeeWee ORM (pip install peewee) to create a local
SQLite database.
"""

import datetime
import pytz

from peewee import *

# placehoder for actual database which gets initialized when
# DBSink is initialized
db_proxy = Proxy()

class BaseModel(Model):
    """
    Base model class whose only purpose is to hold the database reference.
    """
    class Meta:
        database = db_proxy
        
class Location(BaseModel):
    """
    Location information
    """
    vin = CharField()
    time = DateTimeField(default=pytz.utc.localize(datetime.datetime.utcnow()).isoformat())
    latitude = FloatField()
    longitude = FloatField()
    altitude = FloatField(default=0)
    speed = FloatField(default=0)
    climb = FloatField(default=0)
    track = FloatField(default=0)
    odometer = FloatField(default=0)
 


class DBSink(object):
    """
    Write report data to database
    """
    
    def __init__(self, conf, logger):
        self.conf = conf
        self.logger = logger
        self.db = SqliteDatabase(self.conf['TRACKING_DB_NAME'], threadlocals=True)
        db_proxy.initialize(self.db)
        self.db.connect()
        self.db.create_tables([Location], True)
        
            
    def log(self, report):
        """
        Log the location record
        """

        location = Location(vin = report['vin'])
        if 'timestamp' in report:
            location.time = report['timestamp']
        for channel in report['data']:
            key = channel['channel']
            value = channel['value']
            if key == 'location':
                location.latitude = value['lat']
                location.longitude = value['lon']
                location.altitude = value['alt']
            elif key == 'speed':
                location.speed = float(value)
            elif key == 'odometer':
                location.odometer = float(value)
            elif key == 'climb':
                location.climb = float(value)
            elif key == 'track':
                location.track = float(value)
        location.save()
        
        self.logger.info("%s: Report data saved to database.", self.__class__.__name__)
        return True


