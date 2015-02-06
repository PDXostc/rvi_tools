"""
Copyright (C) 2014, Jaguar Land Rover

This program is licensed under the terms and conditions of the
Mozilla Public License, version 2.0.  The full text of the 
Mozilla Public License is at https://www.mozilla.org/MPL/2.0/

Maintainer: Rudolf Streif (rstreif@jaguarlandrover.com) 
"""

"""
GPS Data Collector

RVI Sink that sends data reports to RVI.
"""

import jsonrpclib
import time


class RVISink(object):
    """
    Send data report to RVI
    """
    
    def __init__(self, conf, logger):
        self.conf = conf
        self.logger = logger
        self.logger.info('%s: Setting up outbound connection to RVI Service Edge at %s', self.__class__.__name__, self.conf['TRACKING_RVI_NODE_URL'])
        self.rvi_service_edge = jsonrpclib.Server(conf['TRACKING_RVI_NODE_URL'])
        self.transaction_id = 1
        
            
    def log(self, report):
        """
        Log the location record
        """
        try:
            self.rvi_service_edge.message(calling_service = "/big_data",
                                          service_name = self.conf['TRACKING_RVI_BACKEND_ID'] + "/logging/report",
                                          transaction_id = self.transaction_id,
                                          timeout = int(time.time())+60,
                                          parameters = [report]
                                         )
        except Exception as e:
            self.logger.error("%s: Connection error: %s", self.__class__.__name__, e)
            return False
            
        self.transaction_id += 1
        
        self.logger.info("%s: Report data sent to RVI.", self.__class__.__name__)
        return True
