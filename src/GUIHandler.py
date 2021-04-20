from appJar import gui
import stmpy
import logging
from enum import IntEnum

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

	def __init__(self, stm: stmpy.Machine):
		self._logger = logging.getLogger(__name__)
		self.stm = stm
		self.app = gui("FarmieTalkie", "320x480")
		self.app.startFrameStack("DISPLAY", start=Frame.MAIN)
		self.frame_init()
		self.app.stopFrameStack()
	
	def start(self):
		self.app.go()
	
	def view_frame(self, frame: Frame):
		self.app.selectFrame("DISPLAY", frame)
	
	def frame_init(self):
		self.create_main_frame()
		self.create_select_channel_frame()
		self.create_sending_message_frame()
		self.create_manage_channels_frame()
		self.create_add_channel_frame()
		self.create_view_log_frame()
		self.create_playing_message_frame()


	def create_main_frame(self):
		self.app.startFrame("BUTTONS", row=5, column=0)
		self.app.addButtons(["RECORD", "BACK"], lambda btn: self.press(btn))
		self.app.stopFrame()

	def create_select_channel_frame(self):
		self.app.startFrame()
		
		self.app.stopFrame()

	def create_sending_message_frame(self):
		self.app.startFrame()
		
		self.app.stopFrame()

	def create_manage_channels_frame(self):
		self.app.startFrame()
		
		self.app.stopFrame()

	def create_add_channel_frame(self):
		self.app.startFrame()
		
		self.app.stopFrame()

	def create_view_log_frame(self):
		self.app.startFrame()
		
		self.app.stopFrame()

	def create_playing_message_frame(self):
		self.app.startFrame()
		
		self.app.stopFrame()



# http://appjar.info/simpleAppJar/
# app.addButtons(["Submit", "Cancel"], press)