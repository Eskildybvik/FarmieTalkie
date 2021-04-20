import stmpy
import FarmieTalkieStates
import logging
from GUIHandler import GUIHandler, Frame
from MQTTClient import MQTTClient


class FarmieTalkie:
	def __init__(self):
		# Will be set in the main function
		self.gui = None
		self.mqtt = None
		
		# transitions done, check src/FarmieTalkieStates.py
		self.transitions = FarmieTalkieStates.get_transitions()
		
		# States done, check src/FarmieTalkieStates.py
		self.states = FarmieTalkieStates.get_states()
	
	# Media handling
	# Upon message play successful connection.
	def play_confirmation_sound(self):
		pass

	# Play a notification sound upon receiving a message.
	def play_notify_sound(self):
		pass
	
	# Play the enqueued message.
	def play(self):
		pass
	
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
	
	def show_main(self):
		self.gui.view_frame(Frame.MAIN)
	


		
def main():
	logging.basicConfig(level=logging.DEBUG)
	stm_driver = stmpy.Driver()
	farmietalkie_machine = FarmieTalkie()
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
	gui = GUIHandler(stm)
	farmietalkie_machine.gui = gui
	stm_driver.start(keep_active=True)
	gui.start()


if __name__ == "__main__":
	main()