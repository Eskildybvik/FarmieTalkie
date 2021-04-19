import stmpy

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
		self.transitions = []
        
        # States done, check src/FarmieTalkieStates.py
		self.states = FarmieTalkieStates.get_states()

		# auto-generate similar transitions
		states_with_disconnects = [
			"initial", "main", "select_channel", "sending_message", "recording_message", 
			"select_channel", "add_channel", "manage_channels"
		]
		for st in states_with_disconnects:
			self.transitions.append(generate_disconnect_transition(st))
		
        states_that_allow_recording = ["main", "select_channel"]
        for st in states_that_allow_recording:
            self.transitions.append(generate_record_button_transition(st))

		states_with_back_button_to_main = [
			"play_message", "select_channel", "view_log", "manage_channels"
		]
		for st in states_with_back_button_to_main:
			self.transitions.append(generate_back_button_transistion(st))

		self.transitions.append(generate_back_button_transistion("replay_message", "view_log"))
		self.transitions.append(generate_back_button_transistion("add_channel", "manage_channels"))

        states_with_playback_finished = [
            ("play_message", "main"), ("replay_message", "view_log")
        ]
        for st in states_with_playback_finished:
            self.transitions.append(generate_playback_finished(source=st[0], target=st[1))

		# Other, more specialized transitions
		self.transitions.append({
			"source": "disconnected",
			"target": "main",
			"trigger": "connected",
			"effect": "subscribe_stored_channels"
		})
		self.transitions.append({
			"source": "main",
			"target": "select_channel",
			"trigger": "select_button"
		})
		self.transitions.append({
			"source": "recording_message",
			"target": "sending_message",
			"trigger": "record_button_release"
		})
		self.transitions.append({
			"source": "sending_message",
			"target": "main",
			"trigger": "message_sent",
			"effect": "play_confirmation_sound"
		})
		self.transitions.append({
			"source": "main",
			"target": "manage_channels",
			"trigger": "manage_button"
		})
		self.transitions.append({
			"source": "manage_channels",
			"target": "add_channel",
			"trigger": "add_button"
		})
		self.transitions.append({
			"source": "add_channel",
			"target": "manage_channels",
			"trigger": "confirm_button",
			"effect": "subscribe(channel)" # TODO: unsure of syntax
		})
		self.transitions.append({
			"source": "main",
			"target": "view_log",
			"trigger": "view_log_button"
		})
		self.transitions.append({
			"source": "view_log",
			"target": "replay_message",
			"trigger": "message_clicked"
		})
		self.transitions.append({
			"source": "replay_message",
			"target": "view_log",
			"trigger": "playback_finished"
		})
		self.transitions.append({
			"source": "replay_message",
			"target": "view_log",
			"trigger": "back_button"
		})
		


stm_driver = stmpy.Driver()
farmietalkie_machine = FarmieTalkie()
stmpy.Machine(
	"FarmieTalkie", 
	farmietalkie_machine, 
	farmietalkie_machine.transitions
	states=farmietalkie_machine.states
)