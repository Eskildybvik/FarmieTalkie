import stmpy
import logging
import sounddevice as sd
import soundfile as sf
from signal import signal, SIGINT
from typing import List

import FarmieTalkieStates
from GUIHandler import GUIHandler, Frame
from MQTTClient import MQTTClient
from RecordingManager import RecordingManager
from PlaybackManager import PlaybackManager
from MessageManager import MessageManager


class FarmieTalkie:
	"""Main class of the FarmieTalkie system. Keeps everything together."""

	def __init__(self):
		self.__logger = logging.getLogger(__name__)
		self.__stm = None
		self.__message_player = None
		self.__message_manager = MessageManager()
		self.__cached_messages = self.__message_manager.get_current_message_names()
		
		# Needs to be public to give the driver access
		self.transitions = FarmieTalkieStates.get_transitions()
		self.states = FarmieTalkieStates.get_states()

		self.recording_manager = RecordingManager()
		# Pre-load the two sound effects used
		self.notification_player = PlaybackManager("./assets/notification.ogg")
		self.confirmation_player = PlaybackManager("./assets/confirmation.ogg")
	
	# Needed for the setter to work
	@property
	def stm(self):
		return self.__stm
	
	@stm.setter
	def stm(self, stm: stmpy.Machine):
		self.__stm = stm
		self.mqtt = MQTTClient(self.__stm)
		self.gui = GUIHandler(self.__stm, self.mqtt)

	def start(self):
		self.gui.start()
		self.__logger.debug("FarmieTalkie has been started!")
	
	# Media handling
	# Upon message play successful connection.
	def play_confirmation_sound(self):
		self.confirmation_player.reset()
		self.confirmation_player.play()

	# Play a notification sound upon receiving a message.
	def play_notify_sound(self):
		self.notification_player.reset()
		self.notification_player.play()
	
	# Play the enqueued message.
	def play(self, message: bytearray):
		self.__logger.debug("Received voice message")
		self.__message_manager.new_message(message)
		self.__cached_messages = self.__message_manager.get_current_message_names()
		self.__message_player = PlaybackManager(self.__cached_messages[-1])
		self.__message_player.on_finish = lambda: self.__stm.send("playback_finished")
		self.__message_player.play()
	
	def replay(self, message: str):
		self.__logger.debug(f"Replaying {message}")
		self.__message_player = PlaybackManager(message)
		self.__message_player.on_finish = lambda: self.__stm.send("playback_finished")
		self.__message_player.play()

	def stop_playing(self):
		if self.__message_player:
			# Need to use stop_no_callback to prevent skipping the next message in the queue
			self.__message_player.stop_no_callback()

	
	def start_recording(self):
		self.recording_manager.start_recording()
	
	def stop_recording(self):
		self.recording_manager.stop_recording()
	

	# Message handling
	def send_message(self):
		with open(self.recording_manager.get_recording(), "rb") as recording_file:
			recording = bytearray(recording_file.read())
			self.mqtt.send_message(recording)

	def connect(self):
		self.mqtt.connect()
	
	def subscribe(self):
		pass
	
	def unsubscribe(self, channels: List[str]):
		for channel in channels:
			self.mqtt.remove_channel(channel)
		self.gui.view_frame(Frame.MANAGE_CHANNELS) # Refresh channels


	# GUI Handling
	def show_add_menu(self):
		self.gui.view_frame(Frame.ADD_CHANNEL)
	
	def show_manage_menu(self):
		self.gui.view_frame(Frame.MANAGE_CHANNELS)
	
	def show_log(self):
		self.gui.log_filenames = self.__cached_messages
		self.gui.view_frame(Frame.VIEW_LOG)

	def display_channel_set(self):
		self.gui.view_frame(Frame.SELECT_CHANNEL)
	
	def display_sending(self):
		self.gui.view_frame(Frame.SENDING_MESSAGE)

	def display_recording(self):
		self.gui.view_frame(Frame.RECORDING_MESSAGE)

	def show_main(self):
		self.gui.view_frame(Frame.MAIN)
	
	def show_playing(self):
		self.gui.view_frame(Frame.PLAYING_MESSAGE)
	
	def show_disconnected(self):
		self.gui.view_frame(Frame.DISCONNECTED)
	
	def destroy(self):
		self.mqtt.destroy()
		self.gui.destroy()
		


def main():
	logging.basicConfig(level=logging.DEBUG)
	stm_driver = stmpy.Driver()
	farmietalkie_machine = FarmieTalkie()
	signal(SIGINT, lambda a,b: farmietalkie_machine.destroy())
	stm = stmpy.Machine(
		"FarmieTalkie",
		farmietalkie_machine.transitions,
		farmietalkie_machine, 
		states=farmietalkie_machine.states
	)
	stm_driver.add_machine(stm)
	farmietalkie_machine.stm = stm
	stm_driver.start(keep_active=True)
	farmietalkie_machine.start()

if __name__ == "__main__":
	main()