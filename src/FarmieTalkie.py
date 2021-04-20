import stmpy
import FarmieTalkieStates

def generate_disconnect_transition(source: str) -> dict:
    disconnect_transition = {
        "source": source,
        "target": "disconnected",
		"trigger": "disconnect"
    }
    return disconnect_transition
    
def generate_record_button_transition(source: str) -> dict:
    record_button_transition = {
        "source": source,
		"trigger": "record_button_press",
        "target": "recording_message"
    }
    return record_button_transition

def generate_back_button_transistion(source: str, target: str = "main") -> dict:
	back_button_transition = {
		"source": source,
		"trigger": "back_button_press",
		"target": target
	}
	return back_button_transition

def generate_playback_finished(source: str, target: str) -> dict:
    playback_finished_transition = {
        "source": source,
        "trigger": "playback_finished",
        "target": target,
    }
    return playback_finished_transition
    

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