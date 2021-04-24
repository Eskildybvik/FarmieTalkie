import stmpy
import FarmieTalkieStates
import logging
from signal import signal, SIGINT
from GUIHandler import GUIHandler, Frame
from MQTTClient import MQTTClient
# from AudioManager import AudioManager
from RecordingManager import RecordingManager
from PlaybackManager import PlaybackManager
import sounddevice as sd
import soundfile as sf
import wave

class FarmieTalkie:
	def __init__(self):
		self._logger = logging.getLogger(__name__)
		# Will be set in the main function
		self.gui = None
		self.mqtt = None
		self.stm = None

		# self.audio_manager = AudioManager()
		self.recording_manager = RecordingManager()
		
		# transitions done, check src/FarmieTalkieStates.py
		self.transitions = FarmieTalkieStates.get_transitions()
		
		# States done, check src/FarmieTalkieStates.py
		self.states = FarmieTalkieStates.get_states()

		self.notification_player = PlaybackManager("./assets/notification.wav")
		self.confirmation_player = PlaybackManager("./assets/confirmation.wav")
	
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
		player.on_finish = lambda: self.stm.send("playback_finished")
		player.play()
		
		# with sf.read(self.recording_manager.get_recording()) as wave:
			# sa.play_buffer()
		# data, fs = sf.read(self.recording_manager.get_recording())
		# sd.play(data, fs)

	
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
		self.audio_manager.destroy()
		

		
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
	farmietalkie_machine.stm = stm
	stm_driver.add_machine(stm)
	# self._logger.debug('Component initialization finished')
	mqtt = MQTTClient(stm)
	farmietalkie_machine.mqtt = mqtt
	gui = GUIHandler(stm, mqtt)
	farmietalkie_machine.gui = gui
	stm_driver.start(keep_active=True)
	gui.start()


if __name__ == "__main__":
	main()