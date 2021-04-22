import stmpy
import FarmieTalkieStates
import logging
from signal import signal, SIGINT
from GUIHandler import GUIHandler, Frame
from MQTTClient import MQTTClient
# from AudioManager import AudioManager
import simpleaudio as sa


class FarmieTalkie:
	def __init__(self):
		self._logger = logging.getLogger(__name__)
		# Will be set in the main function
		self.gui = None
		self.mqtt = None

		# self.audio_manager = AudioManager()
		
		# transitions done, check src/FarmieTalkieStates.py
		self.transitions = FarmieTalkieStates.get_transitions()
		
		# States done, check src/FarmieTalkieStates.py
		self.states = FarmieTalkieStates.get_states()
	
	# Media handling
	# Upon message play successful connection.
	def play_confirmation_sound(self):
		sa.WaveObject.from_wave_file("./assets/confirmation.wav").play()

	# Play a notification sound upon receiving a message.
	def play_notify_sound(self):
		sa.WaveObject.from_wave_file("./assets/notification.wav").play()
	
	# Play the enqueued message.
	def play(self, message: bytearray):
		with open("temp.wav", "wb") as temp:
			temp.write(message)
		sa.WaveObject.from_wave_file("temp.wav").play()
	
	def start_recording(self):
		pass
	
	# Message handling
	def send_message(self):
		pass
	
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