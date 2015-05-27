"""
Copyright (C) 2014, Jaguar Land Rover

This program is licensed under the terms and conditions of the
Mozilla Public License, version 2.0.  The full text of the 
Mozilla Public License is at https://www.mozilla.org/MPL/2.0/

Maintainer: Rudolf Streif (rstreif@jaguarlandrover.com) 
"""

"""
Data Collector

Source for file data
"""

import os
import time
import datetime
import pytz
import threading
import glob


fieldnames = ['timestamp', 'longitude' , 'latitude', 'altitude', 'vin']

class FileSource(threading.Thread):
    """
    Get data samples from a file
    """
    
    def __init__(self, conf, logger, queue, filepath):
        threading.Thread.__init__(self)
        self.conf = conf
        self.logger = logger
        self.queue = queue
        self.filepath = filepath
        
    def shutdown(self):
        self._Thread__stop()
        
    def process_file(self):
        try:
            f = open(self.filepath, 'r')
        except IOError as e:
            self.logger.info("%s: Cannot open file: %s", self.__class__.__name__, self.filepath)
            return False
            
        filename = os.path.basename(self.filepath).split('.')[0]
        columns = self.conf['TRACKING_FILE_COLUMNS'].split(self.conf['TRACKING_FILE_DELIMITER'])
            
        for line in iter(f):
            time.sleep(self.conf['TRACKING_FILE_INTERVAL'])
            fields = line.split()
            report = {
                u'timestamp' : pytz.utc.localize(datetime.datetime.fromtimestamp(float(fields[3]))).isoformat(),
                u'vin' : filename,
                u'data' : [
                        { 'channel' : 'location', 'value' : {'lat' : fields[0], 'lon' : fields[1], 'alt' : 0} },
                        { 'channel' : 'occupancy', 'value' : fields[2] },
                    ]
                }
            self.queue.put(report)
            
        return False
            
        
    def run(self):
        run = True
        while run:
            run = self.process_file()
            
            
class FileSources(object):
    """
    Get data samples from multiple files using FileSource
    """
    
    def __init__(self, conf, logger, queue):
        self.conf = conf
        self.logger = logger
        self.queue = queue
        self.filepath = conf['TRACKING_FILE_NAME']
        self.sources = {}

    def start(self):
        files = glob.glob(self.filepath)
        for f in files:
            source = FileSource(self.conf, self.logger, self.queue, f)
            self.sources[f] = source
            source.start()
            
    def shutdown(self):
        for key, value in self.sources.iteritems():
            value.shutdown()
        
            
