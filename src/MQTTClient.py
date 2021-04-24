import paho.mqtt.client as mqtt
import stmpy
import logging


MQTT_BROKER = 'vps.esdy.io'
MQTT_PORT = 16805

MQTT_CHANNEL_PREFIX = "farmietalkie/message/"


def generate_test_sound() -> bytearray: 
	f = open("assets/testsound.wav", "rb")
	test_file = f.read()
	f.close()
	byteArray = bytearray(test_file)
	return byteArray


class MQTTClient:

	def __init__(self, stm: stmpy.Machine):
		self._logger = logging.getLogger(__name__)
		self.test_sound = generate_test_sound()
		self.subscribed_channels = []
		self.selected_channel = ""

		self.stm = stm
		# create a new MQTT client
		self._logger.debug(f'Connecting to MQTT broker {MQTT_BROKER} at port {MQTT_PORT}')
		self.mqtt_client = mqtt.Client()
		# callback methods
		self.mqtt_client.on_connect = self.on_connect
		self.mqtt_client.on_message = self.on_message
		self.mqtt_client.on_disconnect = self.on_disconnect

		self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
		self.mqtt_client.loop_start()

	# subscribe_stored_channels in diagram
	def on_connect(self, client, userdata, flags, rc):
		self._logger.debug("Connected to broker")
		self.stm.send("connect")
		for channel in self.subscribed_channels:
			self.mqtt_client.subscribe(MQTT_CHANNEL_PREFIX + channel)
			
	def on_message(self, client, userdata, msg: mqtt.MQTTMessage):
		payload = msg.payload
		self._logger.debug(f"Received message on channel {msg.topic}")
		if (msg.topic.startswith(MQTT_CHANNEL_PREFIX)):
			self.stm.send("message", args=[payload])
		
		self._logger.debug(f"length of message: {len(payload)}")

	def on_disconnect(self, client, userdata, rc):
		self.stm.send("disconnect")

	def add_channel(self, channel: str):
		if channel in self.subscribed_channels:
			return
		self.subscribed_channels.append(channel)
		self.mqtt_client.subscribe(MQTT_CHANNEL_PREFIX + channel)
		self.subscribed_channels.sort()

	def remove_channel(self, channel: str):
		if channel in self.subscribed_channels:
			self.subscribed_channels.remove(channel)
			self.mqtt_client.unsubscribe(MQTT_CHANNEL_PREFIX + channel)
	
	# TODO: Decide what to send: bytesarray or base64 encoded bytesarray w/json. 
	def send_message(self, message: bytearray):
		self._logger.debug(f"Sending message to channel {self.selected_channel}...")
		sent_message = self.mqtt_client.publish(MQTT_CHANNEL_PREFIX + self.selected_channel, payload=message, qos=2)
		sent_message.wait_for_publish()
		self.stm.send("message_sent")

	def destroy(self):
		self.mqtt_client.disconnect()

	

		