RVI TOOLS
=========

This document is an overview of the RVI Tools. RVI Tools is a set of 
applications that help getting started with the RVI middleware framework.

RVI Tools are a set of data collectors, simulators and other tools collect
and transmit data using RVI

For details on RVI consult the documentation in the
[RVI](https://github.com/PDXostc/rvi) respository.

Follow the links to the various RVI tools:

[Data Collector](https://github.com/PDXostc/rvitools/tree/master/datacollector)


### Docker Images

To make testing easier and self-contained there are Docker configuration files
available to create Docker images. There are Docker configuration files for

* Fedora
* Ubuntu

and a script to invoke the build process:

    $ createdocker <targetos>
    
where *targetos* is one of *fedora* or *ubuntu*. This will create a docker image
called *dc-rvitools-<targetos>* which you can launch in the foreground with

    $ docker run -ti --rm dc-rvitools-<targetos>
    
Currently, the image will launch the *datacollector* by default. You will see its
logging output scroll over the screen. If you want to launch the image with a
shell use

    $ docker run -ti --rm dc-rvitools-<targetos> bash
    
Now you get a shell to poke around.

If you want to run in the background launch the container with

    $ docker run --name rvitools -d dc-rvi-tools-<targetos>
    
The *datacollector* by default sends its log output to *stdout*. You can retrieve
the output from a container running in the background with

    $ docker logs rvitools

To stop the running container

    $ docker stop rvitools
    
You can restart it with

    $ docker start rvitools
    
and delete it with

    $ docker rm rvitools


### Configuration

The *datacollector* and other RVI Tools in the future use a *settings.py* file
for their configuration. You may want and need to adjust that file before
creating the Docker image. The file is copied to the image and then used by the
tool when it is starting.



