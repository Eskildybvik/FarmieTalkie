from appJar import gui
import stmpy
import logging
from enum import IntEnum
from MQTTClient import MQTTClient

class Frame(IntEnum):
	MAIN = 0
	SELECT_CHANNEL = 1
	RECORDING_MESSAGE = 2
	SENDING_MESSAGE = 3
	MANAGE_CHANNELS = 4
	ADD_CHANNEL = 5
	VIEW_LOG = 6
	PLAYING_MESSAGE = 7


class GUIHandler():
	def press(self, button):
		self._logger.debug(f"Button pressed: {button}")
		if button == "RECORD":
			self.stm.send("record_button_press")
		elif button == "BACK":
			self.stm.send("back_button_press")
		elif button == "STOP_RECORD":
			self.stm.send("record_button_release")

	def __init__(self, stm: stmpy.Machine, mqtt: MQTTClient):
		self._logger = logging.getLogger(__name__)
		self.stm = stm
		self.mqtt = mqtt
		self.app = gui("FarmieTalkie", "320x480")
		self.app.startFrameStack("DISPLAY", start=Frame.MAIN)
		self.frame_init()
		self.app.stopFrameStack()
		self.app.startFrame("HARDWARE", row=1)
		self.app.addButtons(["RECORD", "BACK", "STOP_RECORD"], lambda btn: self.press(btn))
		self.app.stopFrame()
	
	def start(self):
		self.app.go()
	
	def destroy(self):
		self.app.stop()
	
	def view_frame(self, frame: Frame):
		if frame == Frame.MANAGE_CHANNELS:
			self.app.updateListBox("Subscribed channels", self.mqtt.subscribed_channels)
		self.app.selectFrame("DISPLAY", frame)
	
	def frame_init(self):
		self.create_main_frame()
		self.create_select_channel_frame()
		self.create_recording_frame()
		self.create_sending_message_frame()
		self.create_manage_channels_frame()
		self.create_add_channel_frame()
		self.create_view_log_frame()
		self.create_playing_message_frame()


	def create_main_frame(self):
		self.app.startFrame("BUTTONS", row=5, column=0)
		self.app.addLabel(Frame.MAIN.name)
		self.app.addButton("Select channel", lambda btn: self.stm.send("select_button"))
		self.app.addButton("Manage channels", lambda btn: self.stm.send("manage_button"))
		self.app.addButton("View log", lambda btn: self.stm.send("view_log_button"))
		self.app.stopFrame()

	def create_select_channel_frame(self):
		entryTitle = "Selected channel name"
		self.app.startFrame()
		self.app.addLabel(Frame.SELECT_CHANNEL.name)
		self.app.addLabelEntry(entryTitle)
		def select_channel_callback(btn: str):
			self.mqtt.selected_channel = self.app.getEntry(entryTitle)
			self.stm.send("back_button_press")
		self.app.addButton("Confirm channel", select_channel_callback)
		self.app.stopFrame()

	def create_recording_frame(self):
		self.app.startFrame()
		self.app.addLabel(Frame.RECORDING_MESSAGE.name)
		self.app.stopFrame()

	def create_sending_message_frame(self):
		self.app.startFrame()
		self.app.addLabel(Frame.SENDING_MESSAGE.name)
		self.app.stopFrame()

	def create_manage_channels_frame(self):
		self.app.startFrame()
		self.app.addLabel(Frame.MANAGE_CHANNELS.name)
		self.app.addListBox("Subscribed channels", self.mqtt.subscribed_channels)
		# self.app.addLabelEntry("Channel Name")
		self.app.addButton("Add channel", lambda btn: self.stm.send("add_button"))
		self.app.stopFrame()

	def create_add_channel_frame(self):
		self.app.startFrame()
		self.app.addLabel(Frame.ADD_CHANNEL.name)
		entryTitle = "Add channel"
		self.app.addLabelEntry(entryTitle)
		def select_channel_callback(btn: str):
			self.mqtt.add_channel(self.app.getEntry(entryTitle))
			self.stm.send("confirm_button")
		self.app.addButton("Confirm channel to add", select_channel_callback)
		self.app.stopFrame()

	# TODO: Missing showing recordings
	def create_view_log_frame(self):
		self.app.startFrame()
		self.app.addLabel(Frame.VIEW_LOG.name)
		self.app.stopFrame()

	def create_playing_message_frame(self):
		self.app.startFrame()
		self.app.addLabel(Frame.PLAYING_MESSAGE.name)
		self.app.stopFrame()


