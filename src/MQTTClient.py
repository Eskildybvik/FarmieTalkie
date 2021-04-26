import paho.mqtt.client as mqtt
import stmpy
import logging



class MQTTClient:
	"""Class used for all MQTT related methods.
	
	Keeps track of subscribed channels (prefixed MQTT topics), handles 
	the broker connection, and automatically resubscribes on reconnect. 
	Also keeps track of the channel which messages should be sent to.

	Attributes
	----------
	subscribed_channels : List[str]
		List of channels the client is subscribed to
	selected_channel : str
		The channel messages should be sent to
	"""

	MQTT_BROKER = 'vps.esdy.io'
	MQTT_PORT = 16805
	MQTT_CHANNEL_PREFIX = "farmietalkie/message/"
	BROADCAST_CHANNEL = "broadcast"

	def __init__(self, stm: stmpy.Machine):
		"""
		Parameters
		----------
		stm: stmpy.Machine
			A reference to the state machine that includes this MQTTClient
		"""
		
		self.__logger = logging.getLogger(__name__)
		self.subscribed_channels = [self.BROADCAST_CHANNEL]
		self.selected_channel = ""

		self.__stm = stm
		# create a new MQTT client
		self.__logger.debug(f'Connecting to MQTT broker {self.MQTT_BROKER} at port {self.MQTT_PORT}')
		self.mqtt_client = mqtt.Client()
		# callback methods
		self.mqtt_client.on_connect = self.on_connect
		self.mqtt_client.on_message = self.on_message
		self.mqtt_client.on_disconnect = self.on_disconnect

		self.mqtt_client.connect(self.MQTT_BROKER, self.MQTT_PORT)
		self.mqtt_client.loop_start()

	# subscribe_stored_channels in diagram
	def on_connect(self, client: mqtt.Client, userdata, flags, rc):
		self.__logger.debug("Connected to broker")
		self.__stm.send("connect")
		for channel in self.subscribed_channels:
			self.mqtt_client.subscribe(self.MQTT_CHANNEL_PREFIX + channel)
			
	def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
		payload = msg.payload
		self.__logger.debug(f"Received message on channel {msg.topic}")
		if (msg.topic.startswith(self.MQTT_CHANNEL_PREFIX)):
			self.__stm.send("message", args=[payload])
		
		self.__logger.debug(f"length of message: {len(payload)}")

	def on_disconnect(self, client: mqtt.Client, userdata, rc):
		self.__stm.send("disconnect")

	def add_channel(self, channel: str):
		"""Subscribe to a channel."""

		if channel in self.subscribed_channels:
			return
		self.subscribed_channels.append(channel)
		self.mqtt_client.subscribe(self.MQTT_CHANNEL_PREFIX + channel)
		self.subscribed_channels.sort()

	def remove_channel(self, channel: str):
		"""Unsubscribe from a channel."""

		if channel == self.BROADCAST_CHANNEL:
			return # Cannot unsubscribe from the broadcast channel

		if channel in self.subscribed_channels:
			self.subscribed_channels.remove(channel)
			self.mqtt_client.unsubscribe(self.MQTT_CHANNEL_PREFIX + channel)
	
	def send_message(self, message: bytearray):
		"""Send a message to selected_channel
		
		Parameters
		----------
		message : bytearray
			A wav file from open(path, "rb").read()
		"""

		self.__logger.debug(f"Sending message to channel {self.selected_channel}...")
		sent_message = self.mqtt_client.publish(self.MQTT_CHANNEL_PREFIX + self.selected_channel, payload=message, qos=2)
		sent_message.wait_for_publish()
		self.__logger.debug("Message sent")
		self.__stm.send("message_sent")

	def destroy(self):
		"""Destructor for this class. Disconnects from MQTT"""

		self.mqtt_client.disconnect()
		self.__logger.debug("MQTT disconnected and destroyed")
