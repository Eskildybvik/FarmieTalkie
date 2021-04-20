import stmpy
import FarmieTalkieStates
	
class FarmieTalkie:
	def __init__(self):
		self.transitions = FarmieTalkieStates.get_transitions()
		
		# States done, check src/FarmieTalkieStates.py
		self.states = FarmieTalkieStates.get_states()

		# auto-generate similar transitions
		
		


stm_driver = stmpy.Driver()
farmietalkie_machine = FarmieTalkie()
stmpy.Machine(
	"FarmieTalkie", 
	farmietalkie_machine, 
	farmietalkie_machine.transitions,
	states=farmietalkie_machine.states
)