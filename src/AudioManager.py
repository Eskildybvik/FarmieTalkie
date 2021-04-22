import pyaudio
import wave
import time
import sys
import threading

class AudioManager:

	def __init__(self):
		self.p = pyaudio.PyAudio()
		self.notification_wave = wave.open("./assets/notification.wav", "rb")
		self.confirmation_wave = wave.open("./assets/confirmation.wav", "rb")

	def callback(self, wf, in_data, frame_count, time_info, status):
		data = wf.readframes(frame_count)
		return (data, pyaudio.paContinue)
	
	# Todo do something with sound.
	def create_stream(self, file_path:str, sound_data: bytearray = None):
		wf = wave.open(file_path, 'rb')
		stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
				channels=wf.getnchannels(),
				rate=wf.getframerate(),
				output=True,
				stream_callback=(lambda in_data, frame_count, time_info, status: self.callback(wf, in_data, frame_count, time_info, status)))
		
		return (wf, stream)

	
	def play_cached(self, wf):
		wf.setpos(0)
		stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
				channels=wf.getnchannels(),
				rate=wf.getframerate(),
				output=True,
				stream_callback=(lambda in_data, frame_count, time_info, status: self.callback(wf, in_data, frame_count, time_info, status)))
		
		stream.start_stream()

		# wait for stream to finish
		while stream.is_active():
			time.sleep(0.1)

		stream.stop_stream()
		stream.close()

	def play(self, file_path:str, sound_data: bytearray = None):
		(wf, stream) = self.create_stream(file_path)

		stream.start_stream()

		# wait for stream to finish
		while stream.is_active():
			time.sleep(0.1)

		stream.stop_stream()
		stream.close()
		wf.close()

	def play_notification(self):
		self.play_cached(self.notification_wave)

	def play_confirmation(self):
		self.play_cached(self.confirmation_wave)

	def destroy(self):
		self.notification_wave.close()
		self.confirmation_wave.close()
		self.p.terminate()
