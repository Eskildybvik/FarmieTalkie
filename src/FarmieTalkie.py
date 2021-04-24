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
	def __init__(self):
		self._logger = logging.getLogger(__name__)
		self._stm = None
		
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
		return self._stm
	
	@stm.setter
	def stm(self, stm: stmpy.Machine):
		self._stm = stm
		self.mqtt = MQTTClient(self._stm)
		self.gui = GUIHandler(self._stm, self.mqtt)

	def start(self):
		self.gui.start()
	
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
		with open("temp.wav", "wb") as file:
			file.write(message)
		player = PlaybackManager("temp.wav")
		player.on_finish = lambda: self._stm.send("playback_finished")
		player.play()

	
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