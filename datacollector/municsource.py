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
import urlparse
import json
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from base64 import b64decode

class MunicSource(threading.Thread):
    """
    Launch HTTP server to receive data from Munic.box dongles.
    """
    
    def __init__(self, conf, logger, queue):
        threading.Thread.__init__(self)
        self.conf = conf
        self.logger = logger
        self.queue = queue
        self.host, self.port = self.conf['TRACKING_MUNICBOX_URL'].split(':')
        self.localServer = HTTPServer(logger, queue, (self.host, int(self.port)), HTTPMethodHandler)
        self.logger.info("%s: Server listening on: %s:%s", self.__class__.__name__, self.host, self.port)
        
    def shutdown(self):
        self._Thread__stop()
        
    def run(self):
        self.localServer.serve_forever()
        
    def shutdown(self):
        self.localServer.shutdown()

class HTTPServer(BaseHTTPServer.HTTPServer):
    def __init__(self, logger, queue, *args):
        self.logger = logger
        self.queue = queue
        BaseHTTPServer.HTTPServer.__init__(self, *args)

class HTTPMethodHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        self.server.logger.info("%s: " + format, self.__class__.__name__, *args)
        return
    
    def do_GET(self):
        self.server.logger.info("%s: HTTP GET from: %s (%s)", self.__class__.__name__, self.client_address, self.address_string())
        self.send_response(501)
        self.end_headers()
        return
        
    def do_POST(self):
        logger = self.server.logger
        queue = self.server.queue
        
        logger.info("%s: HTTP POST from: %s (%s)", self.__class__.__name__, self.client_address, self.address_string())

        # begin the response

        # process data
        ct = self.headers.getheader('content-type').split(';')[0]
        if ct == 'application/json':
            cl = int(self.headers.getheader('content-length'))
            self.send_response(200)
            self.end_headers()
            data = json.loads(self.rfile.read(cl))
            self.process_data(data, queue)
        else:
            self.send_response(415)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        
        return
        
    def process_data(self, data, queue):
        # data is an array of dictionaries
        for record in data:
            # we are only interested in a record that has a payload with
            # location data
            if 'payload' in record and 'loc' in record['payload']:
                report = {}
                report[u'data'] = []
                # parse payload
                payload = record['payload']
                report[u'timestamp'] = payload['recorded_at_ms']
                report[u'vin']       = payload['asset']
                # parse location
                loc = payload['loc']
                report['data'].append({ 'channel' : 'location', 'value' : {'lon' : loc[0], 'lat' : loc[1], 'alt' : 0} })
                # parse fields
                fields = payload['fields']
                if 'GPS_SPEED' in fields:
                    # Munic.Box measures GPS speed in 1/1000 knots (1 knot = 1.852 km/hr)
                    report['data'].append({ 'channel' : 'gps_speed', 'value' : Base64Decoder.decodeInteger(fields['GPS_SPEED']['b64_value']) * 0.001852})
                if 'MDI_OBD_SPEED' in fields:
                    # OBD speed
                    report['data'].append({ 'channel' : 'obd_speed', 'value' : Base64Decoder.decodeInteger(fields['MDI_OBD_SPEED']['b64_value'])})
                if 'MDI_OBD_RPM' in fields:
                    # OBD rpm
                    report['data'].append({ 'channel' : 'obd_rpm', 'value' : Base64Decoder.decodeInteger(fields['MDI_OBD_RPM']['b64_value'])})
                if 'MDI_OBD_VIN' in fields:
                    # OBD VIN (not all vehicles implements that)
                    report['data'].append({ 'channel' : 'obd_vin', 'value' : Base64Decoder.decodeString(fields['MDI_OBD_VIN']['b64_value'])})
                if 'GPS_DIR' in fields:
                    # Heading in 1/100 degrees
                    report['data'].append({ 'channel' : 'heading', 'value' : Base64Decoder.decodeInteger(fields['GPS_DIR']['b64_value']) * 0.01})
                if 'DIO_IGNITION' in fields:
                    # Ignition status
                    report['data'].append({ 'channel' : 'ignition', 'value' : Base64Decoder.decodeBoolean(fields['DIO_IGNITION']['b64_value'])})
                if 'ODO_FULL' in fields:
                    # GPS full odometer
                    report['data'].append({ 'channel' : 'gps_odometer', 'value' : Base64Decoder.decodeInteger(fields['ODO_FULL']['b64_value'])})
                if 'MDI_OBD_MILEAGE' in fields:
                    # OBD Mileage
                    report['data'].append({ 'channel' : 'obd_mileage_km', 'value' : Base64Decoder.decodeInteger(fields['MDI_OBD_MILEAGE']['b64_value'])})
                if 'MDI_OBD_MILEAGE_METERS' in fields:
                    # OBD Mileage
                    report['data'].append({ 'channel' : 'obd_mileage_m', 'value' : Base64Decoder.decodeInteger(fields['MDI_OBD_MILEAGE_METERS']['b64_value'])})
                if 'MDI_JOURNEY_TIME' in fields:
                    # Total journey time
                    report['data'].append({ 'channel' : 'journey_time_total', 'value' : Base64Decoder.decodeInteger(fields['MDI_JOURNEY_TIME']['b64_value'])})
                if 'MDI_IDLE_JOURNEY' in fields:
                    # Idle journey time
                    report['data'].append({ 'channel' : 'journey_time_idle', 'value' : Base64Decoder.decodeInteger(fields['MDI_IDLE_JOURNEY']['b64_value'])})
                if 'MDI_DRIVING_JOURNEY' in fields:
                    # Driving journey time
                    report['data'].append({ 'channel' : 'journey_time_driving', 'value' : Base64Decoder.decodeInteger(fields['MDI_DRIVING_JOURNEY']['b64_value'])})
                if 'MDI_ODO_JOURNEY' in fields:
                    # Trip odometer
                    report['data'].append({ 'channel' : 'journey_odometer', 'value' : Base64Decoder.decodeInteger(fields['MDI_ODO_JOURNEY']['b64_value'])})
                # publish to queue
                queue.put(report)
            
        return

class Base64Decoder(object):
    @classmethod
    def decodeInteger(self, b64value):
        result = 0
        for c in b64decode(b64value):
            result = result << 8
            result += ord(c)
        return result

    @classmethod
    def decodeBoolean(self, b64value):
        if ord(b64decode(b64value)) == 0x0:
            return False
        else:
            return True

    @classmethod
    def decodeString(self, b64value):
        return b64decode(b64value)
