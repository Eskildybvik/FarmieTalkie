import paho.mqtt.client as mqtt
import stmpy
import logging
from threading import Thread
import json


MQTT_BROKER = 'vps.esdy.io'
MQTT_PORT = 16805

MQTT_TOPIC_INPUT = 'ttm4115/team_1/command'
MQTT_TOPIC_OUTPUT = 'ttm4115/team_1/answer'


class MQTTClient:


	def on_connect(self, client, userdata, flags, rc):
		pass
	def on_message(self, client, userdata, msg: mqtt.MQTTMessage):
		pass
	def __init__(self):
		# create a new MQTT client
		self._logger.debug('Connecting to MQTT broker {} at port {}'.format(MQTT_BROKER, MQTT_PORT))
		self.mqtt_client = mqtt.Client()
		# callback methods
		self.mqtt_client.on_connect = self.on_connect
		self.mqtt_client.on_message = self.on_message

	def stop(self):
		pass
