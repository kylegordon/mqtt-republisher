#!/usr/bin/env python

import mosquitto
import os
import time

MQTT_HOST="localhost"
MQTT_PORT=1883
MQTT_TOPIC="/test/raw/#"

mypid = os.getpid()
client_uniq = "Republisher_"+str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)

#define what happens after connection
def on_connect(rc):
        print "Connected"

#On recipt of a message print it
def on_message(msg):
	print "Received", msg.topic, msg.payload
	print "performing lookup magic"
	mqttc.publish("/test/sorted/foo/bar", msg.payload)

#connect to broker
mqttc.connect(MQTT_HOST, MQTT_PORT, 60, True)

#define the callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect

mqttc.subscribe(MQTT_TOPIC, 2)

#remain connected and publish
while mqttc.loop() == 0:
    pass

