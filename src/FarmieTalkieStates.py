from typing import List

def get_states() -> List[dict]:
	states = [
			{
				"name": "disconnected",
				"entry": "connect"
			},
			{
				"name": "main",
				"entry": "show_main"
			},
			{
				"name": "select_channel",
				"entry": "display_channel_set",
				"message": "defer"
			},
			{
				"name": "recording_message",
				"entry": "start_recording; display_recording",
				"message": "defer"
			},
			{
				"name": "sending_message",
				"entry": "send_message; display_sending",
				"message": "defer"
			},
			{
				"name": "manage_channels",
				"entry": "show_manage_menu",
				"message": "defer"
			},
			{
				"name": "add_channel",
				"entry": "show_add_menu",
				"message": "defer"
			},
			{
				"name": "play_message",
				"entry": "play_notify_sound; show_playing",
				"exit": "stop_playing",
				"disconnect": "defer",
				"message": "defer"
			},
			{
				"name": "view_log",
				"entry": "show_log",
				"disconnect": "defer",
				"message": "defer"
			},
			{
				"name": "replay_message",
				"disconnect": "defer",
				"exit": "stop_playing",
				"message": "defer"
			}
		]
	return states

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

def get_transitions() -> List[dict]:
	transitions = []

	states_with_disconnects = [
			"initial", "main", "select_channel", "sending_message", "recording_message", 
			"select_channel", "add_channel", "manage_channels"
		]
		
	for st in states_with_disconnects:
		transitions.append(generate_disconnect_transition(st))
	
	states_that_allow_recording = ["main", "select_channel"]
	for st in states_that_allow_recording:
		transitions.append(generate_record_button_transition(st))

	states_with_back_button_to_main = [
		"play_message", "select_channel", "view_log", "manage_channels"
	]
	for st in states_with_back_button_to_main:
		transitions.append(generate_back_button_transistion(st))

	transitions.append(generate_back_button_transistion("replay_message", "view_log"))
	transitions.append(generate_back_button_transistion("add_channel", "manage_channels"))

	states_with_playback_finished = [
		("play_message", "main"), ("replay_message", "view_log")
	]
	for st in states_with_playback_finished:
		transitions.append(generate_playback_finished(source=st[0], target=st[1]))

	# Other, more specialized transitions
	transitions.append({
		"source": "disconnected",
		"target": "main",
		"trigger": "connect"
	})
	transitions.append({
		"source": "main",
		"target": "select_channel",
		"trigger": "select_button"
	})
	transitions.append({
		"source": "recording_message",
		"target": "sending_message",
		"effect": "stop_recording",
		"trigger": "record_button_release"
	})
	transitions.append({
		"source": "sending_message",
		"target": "main",
		"trigger": "message_sent",
		"effect": "play_confirmation_sound"
	})
	transitions.append({
		"source": "main",
		"target": "manage_channels",
		"trigger": "manage_button"
	})
	transitions.append({
		"source": "manage_channels",
		"target": "add_channel",
		"trigger": "add_button"
	})
	transitions.append({
		"source": "manage_channels",
		"target": "manage_channels",
		"trigger": "delete",
		"effect": "unsubscribe(*)"
	})
	transitions.append({
		"source": "add_channel",
		"target": "manage_channels",
		"trigger": "confirm_button"
	})
	transitions.append({
		"source": "main",
		"target": "view_log",
		"trigger": "view_log_button"
	})
	transitions.append({
		"source": "view_log",
		"target": "replay_message",
		"trigger": "select_message",
		"effect": "replay(*)"
	})
	transitions.append({
		"source": "replay_message",
		"target": "view_log",
		"trigger": "playback_finished"
	})
	transitions.append({
		"source": "replay_message",
		"target": "view_log",
		"trigger": "back_button"
	})
	transitions.append({
		"source": "main",
		"target": "play_message",
		"trigger": "message",
		"effect": "play(*)"
	})

	return transitions