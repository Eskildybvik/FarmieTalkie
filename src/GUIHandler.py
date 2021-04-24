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
			self._stm.send("record_button_press")
		elif button == "BACK":
			self._stm.send("back_button_press")
		elif button == "STOP_RECORD":
			self._stm.send("record_button_release")

	def __init__(self, stm: stmpy.Machine, mqtt: MQTTClient):
		self._logger = logging.getLogger(__name__)
		self._stm = stm
		self._mqtt = mqtt
		self._app = gui("FarmieTalkie", "320x480")
		self._app.startFrameStack("DISPLAY", start=Frame.MAIN)
		self._frame_init()
		self._app.stopFrameStack()
		self._app.startFrame("HARDWARE", row=1)
		self._app.addButtons(["RECORD", "BACK", "STOP_RECORD"], lambda btn: self.press(btn))
		self._app.stopFrame()
	
	def start(self):
		self._app.go()
	
	def destroy(self):
		self._app.stop()
	
	def view_frame(self, frame: Frame):
		if frame == Frame.MANAGE_CHANNELS:
			self._app.updateListBox("Subscribed channels", self._mqtt.subscribed_channels)
		self._app.selectFrame("DISPLAY", frame)
	
	def _frame_init(self):
		self._create_main_frame()
		self._create_select_channel_frame()
		self._create_recording_frame()
		self._create_sending_message_frame()
		self._create_manage_channels_frame()
		self._create_add_channel_frame()
		self._create_view_log_frame()
		self._create_playing_message_frame()


	def _create_main_frame(self):
		self._app.startFrame("BUTTONS", row=5, column=0)
		self._app.addLabel(Frame.MAIN.name)
		self._app.addButton("Select channel", lambda btn: self._stm.send("select_button"))
		self._app.addButton("Manage channels", lambda btn: self._stm.send("manage_button"))
		self._app.addButton("View log", lambda btn: self._stm.send("view_log_button"))
		self._app.stopFrame()

	def _create_select_channel_frame(self):
		entryTitle = "Selected channel name"
		self._app.startFrame()
		self._app.addLabel(Frame.SELECT_CHANNEL.name)
		self._app.addLabelEntry(entryTitle)
		def select_channel_callback(btn: str):
			self._mqtt.selected_channel = self._app.getEntry(entryTitle)
			self._stm.send("back_button_press")
		self._app.addButton("Confirm channel", select_channel_callback)
		self._app.stopFrame()

	def _create_recording_frame(self):
		self._app.startFrame()
		self._app.addLabel(Frame.RECORDING_MESSAGE.name)
		self._app.stopFrame()

	def _create_sending_message_frame(self):
		self._app.startFrame()
		self._app.addLabel(Frame.SENDING_MESSAGE.name)
		self._app.stopFrame()

	def _create_manage_channels_frame(self):
		self._app.startFrame()
		self._app.addLabel(Frame.MANAGE_CHANNELS.name)
		self._app.addListBox("Subscribed channels", self._mqtt.subscribed_channels)
		self._app.addButton("Add channel", lambda btn: self._stm.send("add_button"))
		self._app.stopFrame()

	def _create_add_channel_frame(self):
		self._app.startFrame()
		self._app.addLabel(Frame.ADD_CHANNEL.name)
		entryTitle = "Add channel"
		self._app.addLabelEntry(entryTitle)
		def select_channel_callback(btn: str):
			self._mqtt.add_channel(self._app.getEntry(entryTitle))
			self._stm.send("confirm_button")
		self._app.addButton("Confirm channel to add", select_channel_callback)
		self._app.stopFrame()

	# TODO: Missing showing recordings
	def _create_view_log_frame(self):
		self._app.startFrame()
		self._app.addLabel(Frame.VIEW_LOG.name)
		self._app.stopFrame()

	def _create_playing_message_frame(self):
		self._app.startFrame()
		self._app.addLabel(Frame.PLAYING_MESSAGE.name, text="Playing incoming message...")
		self._app.stopFrame()


