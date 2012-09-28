#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

__author__ = "Kyle Gordon"
__copyright__ = "Copyright (C) Kyle Gordon"

import os
import csv
import logging
import signal
import time
import socket

import mosquitto
import ConfigParser

# Read the config file
config = ConfigParser.RawConfigParser()
config.read("/etc/mqtt-republisher/mqtt-republisher.cfg")

#Use ConfigParser to pick out the settings
DEBUG = config.getboolean("global", "debug")
LOGFILE = config.get("global", "logfile")
MAPFILE = config.get("global", "mapfile")
MQTT_HOST = config.get("global", "mqtt_host")
MQTT_PORT = config.getint("global", "mqtt_port")
MQTT_TOPIC = config.get("global", "mqtt_topic")

client_id = "Republisher_%d" % os.getpid()
mqttc = mosquitto.Mosquitto(client_id)

if DEBUG:
    logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)
else:
    logging.basicConfig(filename=LOGFILE, level=logging.INFO)

logging.info("Starting mqtt-republisher")
logging.info("INFO MODE")
logging.debug("DEBUG MODE")

def cleanup(signum, frame):
     """
     Signal handler to ensure we disconnect cleanly 
     in the event of a SIGTERM or SIGINT.
     """
     logging.info("Disconnecting from broker")
     mqttc.publish("/status/" + socket.getfqdn(), "Offline")
     mqttc.disconnect()
     logging.info("Exiting on signal %d", signum)

def connect():
    """
    Connect to the broker, define the callbacks, and subscribe
    """
    mqttc.connect(MQTT_HOST, MQTT_PORT, 60, True)

    #define the callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect

    mqttc.subscribe(MQTT_TOPIC, 2)

def on_connect(result_code):
     """
     Handle connections (or failures) to the broker.
     """
     ## FIXME - needs fleshing out http://mosquitto.org/documentation/python/
     if result_code == 0:
        logging.info("Connected to broker")
        mqttc.publish("/status/" + socket.getfqdn(), "Online")
     else:
        logging.warning("Something went wrong")
        cleanup()

def on_disconnect(result_code):
     """
     Handle disconnections from the broker
     """
     if result_code == 0:
        logging.info("Clean disconnection")
     else:
        logging.info("Unexpected disconnection! Reconnecting in 5 seconds")
        logging.debug("Result code: %s", result_code)
        time.sleep(5)
        connect()
        main_loop()

class RepublishingMap:
    """
    Read the named mapfile into a dictionary for internal lookups
    """
    with open(MAPFILE, mode="r") as inputfile:
        reader = csv.reader(inputfile)
        mapdict = dict((rows[0],rows[1]) for rows in reader)

#On recipt of a message print it
def on_message(msg):
    """
    What to do when the client recieves a message from the broker
    """
    logging.debug("Received: %s", msg.topic)
    if msg.topic in RepublishingMap.mapdict:
        ## Found an item. Replace it with one from the dictionary
        mqttc.publish(RepublishingMap.mapdict[msg.topic], msg.payload)
        logging.info("Republishing: %s -> %s", msg.topic, RepublishingMap.mapdict[msg.topic])
    else:
        # Received something with a /raw/ topic, but it didn't match. Push it out with /unsorted/ prepended
        mqttc.publish("/unsorted" + msg.topic, msg.payload)
        logging.info("Unknown: %s", msg.topic)

def main_loop():
        """
        The main loop in which we stay connected to the broker
        """
        while mqttc.loop() == 0:
                logging.debug("Looping")


# Use the signal module to handle signals
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

#connect to broker
connect()

main_loop()
