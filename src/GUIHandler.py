from appJar import gui
import stmpy
import logging
from enum import IntEnum
from MQTTClient import MQTTClient


class Frame(IntEnum):
	"""Used to make it simple to change "scene" in the GUI"""

	MAIN = 0
	SELECT_CHANNEL = 1
	RECORDING_MESSAGE = 2
	SENDING_MESSAGE = 3
	MANAGE_CHANNELS = 4
	ADD_CHANNEL = 5
	VIEW_LOG = 6
	PLAYING_MESSAGE = 7
	DISCONNECTED = 8


class GUIHandler():
	"""Class for creating and running the graphical user interface.
	
	Fields
	------
	log_filenames : List[str]
		Filenames to display in the log
	"""

	def __press(self, button: str):
		self.__logger.debug(f"Button pressed: {button}")
		if button == "RECORD":
			self.__stm.send("record_button_press")
		elif button == "BACK":
			self.__stm.send("back_button_press")
		elif button == "STOP_RECORD":
			self.__stm.send("record_button_release")

	def __init__(self, stm: stmpy.Machine, mqtt: MQTTClient):
		"""
		Parameters
		----------
		stm : stmpy.Machine
			A reference to the state machine this belongs to
		mqtt : MQTTClient
			A reference to the MQTT client of the program
		"""

		self.__logger = logging.getLogger(__name__)
		self.__stm = stm
		self.__mqtt = mqtt
		self.__app = gui("FarmieTalkie", "320x480")
		self.__app.startFrameStack("DISPLAY", start=Frame.MAIN)
		self.log_filenames = []
		self.__frame_init()
		self.__app.stopFrameStack()

		# "Hardware" buttons
		self.__app.startFrame("HARDWARE", row=1)
		self.__app.addButtons(["RECORD", "STOP_RECORD", "BACK"], lambda btn: self.__press(btn))
		self.__app.stopFrame()
	
	def start(self):
		"""Start the GUI"""

		self.__app.go()
		self.__logger.debug("GUI Started")
	
	def destroy(self):
		"""Destructor of the GUI. Closes the program"""

		self.__app.stop()
		self.__logger.debug("GUI Stopped")
	
	def view_frame(self, frame: Frame):
		"""Go to a specific "scene" of the GUI"""

		if frame == Frame.MANAGE_CHANNELS:
			self.__app.updateListBox("Subscribed channels", self.__mqtt.subscribed_channels)
		if frame == Frame.VIEW_LOG:
			self.__app.updateListBox("Message log", self.log_filenames)
		self.__app.selectFrame("DISPLAY", frame)
		self.__logger.debug(f"Switched to frame {frame.name}")
	
	def __frame_init(self):
		self.__create_main_frame()
		self.__create_select_channel_frame()
		self.__create_recording_frame()
		self.__create_sending_message_frame()
		self.__create_manage_channels_frame()
		self.__create_add_channel_frame()
		self.__create_view_log_frame()
		self.__create_playing_message_frame()
		self.__create_disconnected_frame()


	def __create_main_frame(self):
		self.__app.startFrame("BUTTONS", row=5, column=0)
		self.__app.addLabel(Frame.MAIN.name, text="Listening for incoming messages")
		self.__app.addButton("Select channel", lambda btn: self.__stm.send("select_button"))
		self.__app.addButton("Manage channels", lambda btn: self.__stm.send("manage_button"))
		self.__app.addButton("View log", lambda btn: self.__stm.send("view_log_button"))
		self.__app.stopFrame()

	def __create_select_channel_frame(self):
		entryTitle = "Selected channel name"
		self.__app.startFrame()
		self.__app.addLabel(Frame.SELECT_CHANNEL.name, text="Select channel to send messages to")
		self.__app.addLabelEntry(entryTitle)
		def select_channel_callback(btn: str):
			self.__mqtt.selected_channel = self.__app.getEntry(entryTitle)
			self.__stm.send("back_button_press")
		self.__app.addButton("Confirm channel", select_channel_callback)
		self.__app.stopFrame()

	def __create_recording_frame(self):
		self.__app.startFrame()
		self.__app.addLabel(Frame.RECORDING_MESSAGE.name, text="Recording...")
		self.__app.stopFrame()

	def __create_sending_message_frame(self):
		self.__app.startFrame()
		self.__app.addLabel(Frame.SENDING_MESSAGE.name, text="Sending...")
		self.__app.stopFrame()

	def __create_manage_channels_frame(self):
		self.__app.startFrame()
		self.__app.addLabel(Frame.MANAGE_CHANNELS.name, text="Manage subscribed channels")
		self.__app.addListBox("Subscribed channels", self.__mqtt.subscribed_channels)
		def manage_channel_buttons(btn: str):
			if btn == "Add channel":
				self.__stm.send("add_button")
			elif btn == "Delete selected":
				self.__stm.send("delete", args=[self.__app.getListBox("Subscribed channels")])
		self.__app.addButtons(["Add channel", "Delete selected"], manage_channel_buttons)
		self.__app.stopFrame()

	def __create_add_channel_frame(self):
		self.__app.startFrame()
		self.__app.addLabel(Frame.ADD_CHANNEL.name, text="Add new channel")
		entryTitle = "Add channel"
		self.__app.addLabelEntry(entryTitle)
		def select_channel_callback(btn: str):
			self.__mqtt.add_channel(self.__app.getEntry(entryTitle))
			self.__stm.send("confirm_button")
		self.__app.addButton("Confirm channel to add", select_channel_callback)
		self.__app.stopFrame()

	def __create_view_log_frame(self):
		self.__app.startFrame()
		self.__app.addLabel(Frame.VIEW_LOG.name, text="Message log")
		self.__app.addListBox("Message log", self.log_filenames)
		def replay_callback(stm: str):
			selected = self.__app.getListBox("Message log")
			if len(selected) < 1:
				return
			self.__stm.send("select_message", args=[selected[0]])
		self.__app.addButton("Replay message", replay_callback)
		self.__app.stopFrame()

	def __create_playing_message_frame(self):
		self.__app.startFrame()
		self.__app.addLabel(Frame.PLAYING_MESSAGE.name, text="Playing message...")
		self.__app.stopFrame()

	def __create_disconnected_frame(self):
		self.__app.startFrame()
		self.__app.addLabel(Frame.DISCONNECTED.name, text="Not connected to broker")
		self.__app.addButton("Reconnect", lambda btn: self.__stm.send("reconnect_button"))
		self.__app.stopFrame()
