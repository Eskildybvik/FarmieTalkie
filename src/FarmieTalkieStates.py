def get_states():
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
				"entry": "start_recording",
				"message": "defer"
			},
			{
				"name": "sending_message",
				"entry": "send_message",
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
				"entry": "play_notify_sound; play(msg)", # TODO: Unsure about syntax
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
				"entry": "play(msg)", # TODO: Unsure about syntax
				"disconnect": "defer",
				"message": "defer"
			}
		]
    return states