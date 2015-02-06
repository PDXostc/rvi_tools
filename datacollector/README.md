Copyright (C) 2014, Jaguar Land Rover

This document is licensed under Creative Commons
Attribution-ShareAlike 4.0 International.


DATA COLLECTOR (DC)
===================

The DC is a simple Python application that can collect data such as location
from different data sources and publish them to different data sinks.

Data Sources
------------

Currently we have these data sources:

1. GPS Data Source

   Data source that reads location information from a GPS receiver via
   gpsd.
        
2. File Data Source
 
   Data source that reads location information from one or more files.
        
Data Sinks
----------
    
The data sinks are:

1. Database Sink

   Publishes data received from the data sources to a local SQLite database.
        
2. Message Queue Sink

   Publishes data received from the data sources to an Apache Kafka message
   queue which can be local or remote.
        
3. RVI Sink

   Publishes data received from the data sources to RVI.
        
Running
-------
        
The DC can be run interactively in the foreground or as a background process.

1. Foreground Invocation

        shell> python datacollector.py fg
        
2. Background Invocation

        shell> python datacollector.py start
        
   To stop a DC running in the background use
   
        shell> python datacollector.py stop
        
   To restart a DC running in the background use
    
        shell> python datacollcetor.py restart
        
   A DC running in the background uses a file that stores the processe's PID to
   be able find the running process in the process table of the system. The
   default PID file is /var/run/<name>.pid where name is basename of the
   application e.g. datacollector.
 
Configuration
------------- 
   
Configuration of the DC is accomplished by modifying the file settings.py.


TODO
----

1. Multiple Invocation

To enable multiple DC to be able to run with different configuration we
need to add to specify the settings module on the command line.)

2. Multi-threaded Sinks

Sources run in their own threads and the file source can even have multiple
threads on its own to publish to the internal message queue. However, only the
main thread currently reads from the internal message queue and publishes to the
various sinks. It should be possible to create multiple threads for sinks such
as the RVI sink to stress test the sink.
