#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

__author__ = "Kyle Gordon"
__copyright__ = "Copyright (C) Kyle Gordon"

import os
import csv
import logging
import signal

import mosquitto

MQTT_HOST = "10.8.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "/raw/#"
MAPFILE = "/etc/mqtt-republisher/map.csv"
LOGFILE = "/var/log/mqtt-republisher.log"
DEBUG = False

client_id = "Republisher_%d" % os.getpid()
mqttc = mosquitto.Mosquitto(client_id)

if DEBUG:
    logging.basicConfig(filename=LOGFILE, level=logging.INFO)
else:
	 logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)

logging.info("Starting mqtt-republisher")
logging.info("INFO MODE")
logging.debug("DEBUG MODE")

def cleanup(signum, frame):
	 """
	 Signal handler to ensure we disconnect cleanly 
	 in the event of a SIGTERM or SIGINT.
	 """
	 logging.info("Disconnecting from broker")
	 mqttc.disconnect()
	 logging.info("Exiting on signal %d", signum)

# Turn the mapping file into a dictionary for internal use
with open(MAPFILE, mode="r") as inputfile:
	 """
	 Read the named mapfile into a dictionary for internal lookups
	 """
	 reader = csv.reader(inputfile)
    mydict = dict((rows[0],rows[1]) for rows in reader)

#define what happens after connection
def on_connect(rc):
	logging.info("Connected to broker")

#On recipt of a message print it
def on_message(msg):
	logging.debug("Received: " + msg.topic)
	if msg.topic in mydict:
		## Found an item. Replace it with one from the dictionary
		mqttc.publish(mydict[msg.topic], msg.payload)
		logging.debug("Republishing: " + msg.topic + " -> " + mydict[msg.topic])
	else:
		# Recieved something with a /raw/ topic, but it didn't match. Push it out with /unsorted/ prepended
		mqttc.publish("/unsorted" + msg.topic, msg.payload)
		logging.debug("Unknown: " + msg.topic)

# Use the signal module to handle signals
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

#connect to broker
mqttc.connect(MQTT_HOST, MQTT_PORT, 60, True)

#define the callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect

mqttc.subscribe(MQTT_TOPIC, 2)

#remain connected and publish
while mqttc.loop() == 0:
	logging.debug("Looping")
