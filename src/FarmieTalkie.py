import stmpy
import logging
import sounddevice as sd
import soundfile as sf
from signal import signal, SIGINT

import FarmieTalkieStates
from GUIHandler import GUIHandler, Frame
from MQTTClient import MQTTClient
from RecordingManager import RecordingManager
from PlaybackManager import PlaybackManager


class FarmieTalkie:
	"""Main class of the FarmieTalkie system. Keeps everything together."""

	def __init__(self):
		self.__logger = logging.getLogger(__name__)
		self.__stm = None
		self.__message_player = None
		
		# Needs to be public to give the driver access
		self.transitions = FarmieTalkieStates.get_transitions()
		self.states = FarmieTalkieStates.get_states()

		self.recording_manager = RecordingManager()
		# Pre-load the two sound effects used
		self.notification_player = PlaybackManager("./assets/notification.wav")
		self.confirmation_player = PlaybackManager("./assets/confirmation.wav")
	
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
		with open("temp.ogg", "wb") as file:
			file.write(message)
		self.__message_player = PlaybackManager("temp.ogg")
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
		pass
	
	def subscribe(self):
		pass
	
	def unsubscribe(self):
		pass


	# GUI Handling
	def show_add_menu(self):
		self.gui.view_frame(Frame.ADD_CHANNEL)
	
	def show_manage_menu(self):
		self.gui.view_frame(Frame.MANAGE_CHANNELS)
	
	def show_log(self):
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