"""
Copyright (C) 2014, Jaguar Land Rover

This program is licensed under the terms and conditions of the
Mozilla Public License, version 2.0.  The full text of the 
Mozilla Public License is at https://www.mozilla.org/MPL/2.0/

Maintainer: Rudolf Streif (rstreif@jaguarlandrover.com) 
"""

"""
GPS Data Collector

Message Queue Sink that publishes messages to a Kafka message queue.
"""

import json
from kafka import KafkaClient, SimpleProducer

class MQSink(object):
    """
    Publish data report to message queue
    """
    kafka = None
    
    def __init__(self, conf, logger):
        self.conf = conf
        self.logger = logger
        
            
    def log(self, report):
        """
        Log the location record
        """
        # Connect to Kafka Message Queue Server
        if (not self.kafka):
            try:
                self.kafka = KafkaClient(self.conf['TRACKING_MQ_URL'])
            except:
                self.logger.error("%s: Kafka Message Queue Server unavailable: %s", self.__class__.__name__, self.conf['TRACKING_MQ_URL'])
                self.kafka = None
                return False
        
        producer = SimpleProducer(self.kafka)
        producer.send_messages(self.conf['TRACKING_MQ_TOPIC'], json.dumps(report))
        
        self.logger.info("%s: Report data published to message queue.", self.__class__.__name__)
        return True


