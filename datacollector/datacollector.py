"""
Copyright (C) 2014, Jaguar Land Rover

This program is licensed under the terms and conditions of the
Mozilla Public License, version 2.0.  The full text of the 
Mozilla Public License is at https://www.mozilla.org/MPL/2.0/

Maintainer: Rudolf Streif (rstreif@jaguarlandrover.com) 
"""

"""
Data Collector

This tool collects data from the gpsd daemon and stores it in the RVI Backend
database using the Django ORM.
"""

import sys
import getopt
import os
import time
import logging

import django

from signal import *
from Queue import Queue

from daemon import Daemon
from utils import get_settings
from dbsink import DBSink
from mqsink import MQSink
from rvisink import RVISink
from gpssource import GPSSource
from filesource import FileSource, FileSources

import __init__
from __init__ import __TOOLS_LOGGER__ as logger




class DataCollector(Daemon):
    """
    """
    
    
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        super(DataCollector,self).__init__(pidfile, stdin, stdout, stderr)
        self.queue = Queue()
        self.gps_source = None
        self.file_source = None

    def run(self):
        # Execution starts here
        logger.info('%s: Starting...', self.__class__.__name__)

        # get configuration
        conf = get_settings()
        
        # setup gps source
        if conf['TRACKING_GPS_ENABLE'] == True:
            logger.info('%s: GPS Source enabled.', self.__class__.__name__)
            self.gps_source = GPSSource(conf, logger, self.queue)
            self.gps_source.start()
            
        # setup file source
        if conf['TRACKING_FILE_ENABLE'] == True:
            logger.info('%s: File Source enabled.', self.__class__.__name__)
            self.file_source = FileSources(conf, logger, self.queue, conf['TRACKING_FILE_NAME'])
            self.file_source.start()

        # setup database sink
        if conf['TRACKING_DB_PUBLISH'] == True:
            logger.info('%s: Publishing to database enabled.', self.__class__.__name__)
            db_sink = DBSink(conf, logger)
            
        # setup message queue sink
        if conf['TRACKING_MQ_PUBLISH'] == True:
            logger.info('%s: Publishing to message queue enabled.', self.__class__.__name__)
            mq_sink = MQSink(conf, logger)
            
        # setup RVI sink
        if conf['TRACKING_RVI_PUBLISH'] == True:
            logger.info('%s: Publishing to RVI enabled.', self.__class__.__name__)
            rvi_sink = RVISink(conf, logger)
            
        # catch signals for proper shutdown
        for sig in (SIGABRT, SIGTERM, SIGINT):
            signal(sig, self.cleanup)

        # main execution loop
        while True:
            try:
                
                # get data from queue
                try:
                    data = self.queue.get(True, 60)
                except Exception as e:
                    if isinstance(e, KeyboardInterrupt):
                        break
                    else:
                        logger.info("%s: Queue timeout", self.__class__.__name__)
                        continue
                    
                
                # vin is required but not all data sources may provide it
                if (not 'vin' in data):
                    data[u'vin'] = conf['VIN_DEFAULT']


                logger.info("%s: Got data: %s", self.__class__.__name__, data)

                if conf['TRACKING_DB_PUBLISH'] == True:
                    db_sink.log(data)

                if conf['TRACKING_MQ_PUBLISH'] == True:
                    mq_sink.log(data)

                if conf['TRACKING_RVI_PUBLISH'] == True:
                    rvi_sink.log(data)


            except KeyboardInterrupt:
                print ('\n')
                break

    def cleanup(self, *args):
        logger.info('%s: Caught signal: %d. Shutting down...', self.__class__.__name__, args[0])
        if self.gps_source:
            self.gps_source.shutdown()
        if self.file_source:
            self.file_source.shutdown()
        sys.exit(0)




def usage():
    print "Usage: %s foreground|start|stop|restart [-p <pidfile>]" % sys.argv[0]
        
if __name__ == "__main__":
    pid_file = '/var/run/' + os.path.splitext(__file__)[0] + '.pid'
    
    try:
        opts, args = getopt.getopt(sys.argv[2:], "hp:", ["help", "pidfile="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    # print opts
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif opt in ("-p", "--pidfile"):
            pid_file = arg

    data_collector = DataCollector(pid_file, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')

    if len(sys.argv) >= 2:
        if sys.argv[1] in ('foreground', 'fg'):
            data_collector.run()
        elif sys.argv[1] in ('start', 'st'):
            data_collector.start()
        elif sys.argv[1] in ('stop', 'sp'):
            data_collector.stop()
        elif sys.argv[1] in ('restart', 're'):
            data_collector.restart()
        else:
            print "%s: Unknown command." % sys.argv[0]
            usage()
            sys.exit(2)
    else:
        usage()
        sys.exit(2)
            

