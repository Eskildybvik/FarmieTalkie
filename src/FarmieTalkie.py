import stmpy
import FarmieTalkieStates
import logging
import MQTTClient



class FarmieTalkie:
	def __init__(self):
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
		pass
	
	def show_manage_menu(self):
		pass
	
	def show_log(self):
		pass

	def display_channel_set(self):
		pass
	
	def show_main(self):
		pass
	


		
def main():
	logging.basicConfig(level=logging.DEBUG)
	stm_driver = stmpy.Driver()
	farmietalkie_machine = FarmieTalkie()
	stm = stmpy.Machine(
		"FarmieTalkie", 
		farmietalkie_machine, 
		farmietalkie_machine.transitions,
		states=farmietalkie_machine.states
	)
	self._logger.debug('Component initialization finished')
	mqtt = MQTTClient(stm)
	farmietalkie_machine.mqtt = mqtt
	self.stm_driver.start(keep_active=True)


if __name__ == "__main__":
	main()