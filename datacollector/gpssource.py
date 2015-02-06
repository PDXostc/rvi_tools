"""
Copyright (C) 2014, Jaguar Land Rover

This program is licensed under the terms and conditions of the
Mozilla Public License, version 2.0.  The full text of the 
Mozilla Public License is at https://www.mozilla.org/MPL/2.0/

Maintainer: Rudolf Streif (rstreif@jaguarlandrover.com) 
"""

"""
GPS Data Collector

Source for GPS data using gpsd
"""

import time
import threading
from gps import *


class GPSSource(threading.Thread):
    """
    Connect to GPSD and get data samples.
    """
    
    def __init__(self, conf, logger, queue):
        threading.Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE)
        self.conf = conf
        self.logger = logger
        self.queue = queue
        self.last_speed = 1.0
        self.nofix = False
        
    def shutdown(self):
        self._Thread__stop()
        
    def run(self):
        while True:

            time.sleep(self.conf['TRACKING_GPS_INTERVAL'])
            
            # get GPS data sample
            self.session.next()
            
            # process GPS data sample
            if (self.session.fix.mode == MODE_NO_FIX) and not self.nofix:
                self.logger.info("%s: Waiting for GPS to fix...", self.__class__.__name__)
                continue
            
            # check for valid GPS time    
            if not isnan(self.session.fix.time):
                # don't collect samples if vehicle is not in motion
                if (self.session.fix.speed < 0.1) and (self.last_speed < 0.1):
                    continue
                self.last_speed = self.session.fix.speed
                    
                altitude = 0
                if (self.session.fix.mode == MODE_3D):
                    altitude = self.session.fix.altitude

                report = {
                    u'timestamp' : self.session.utc,
                    u'data' : [
                        { 'channel' : 'speed', 'value' : self.session.fix.speed },
                        { 'channel' : 'location', 'value' : {'lat' : self.session.fix.latitude, 'lon' : self.session.fix.longitude, 'alt' : altitude} },
                        { 'channel' : 'climb', 'value' : self.session.fix.climb },
                        { 'channel' : 'track', 'value' : self.session.fix.track },
                    ]
                }
                
                # publish to queue
                self.queue.put(report)

            


