#!/usr/bin/env python

import mosquitto
import os
import time
import csv

MQTT_HOST="localhost"
MQTT_PORT=1883
MQTT_TOPIC="/raw/#"

mapfile='map.csv'

mypid = os.getpid()
client_uniq = "Republisher_"+str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)

def cleanup():
    print "Disconnecting"
    mqttc.disconnect()

# Turn the mapping file into a dictionary for internal use
# Valid from Python 2.7.1 onwards
with open(mapfile, mode='r') as inputfile:
    reader = csv.reader(inputfile)
    mydict = dict((rows[0],rows[1]) for rows in reader)

#define what happens after connection
def on_connect(rc):
        print "Connected"

#On recipt of a message print it
def on_message(msg):
	# print "Received", msg.topic, msg.payload
	if msg.topic in mydict:
		## Found an item. Replace it with one from the dictionary
		# print "Replacing " + msg.topic + " with " + mydict[msg.topic]
		mqttc.publish(mydict[msg.topic], msg.payload)
	else:
		# Recieved something with a /raw/ topic, but it didn't match. Push it out with /unsorted/ prepended
		mqttc.publish("/unsorted" + msg.topic, msg.payload)

try:
	#connect to broker
	mqttc.connect(MQTT_HOST, MQTT_PORT, 60, True)

	#define the callbacks
	mqttc.on_message = on_message
	mqttc.on_connect = on_connect

	mqttc.subscribe(MQTT_TOPIC, 2)

	#remain connected and publish
	while mqttc.loop() == 0:
		pass

except (KeyboardInterrupt):
    print "Keyboard interrupt received."
    cleanup()
except (RuntimeError):
    print "Crashed for some reason."
    cleanup()
