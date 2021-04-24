import logging
import queue
import threading
import sounddevice as sd
import soundfile as sf
import numpy
assert numpy


class RecordingManager:
	SAMPLE_RATE = 44100
	TEMP_FILE_NAME = "recording_temp.wav"

	def __init__(self):
		self._logger = logging.getLogger(__name__)
		self._buffer = queue.Queue()

	def start_recording(self):
		self.recording = True
		recording_thread = threading.Thread(target=self._thread_function)
		recording_thread.start()
	
	def _thread_function(self):
		with sf.SoundFile(self.TEMP_FILE_NAME, mode="w", 
				samplerate=self.SAMPLE_RATE, channels=1) as file:
			with sd.InputStream(samplerate=self.SAMPLE_RATE, 
					channels=1, callback=self.callback):
				self._logger.debug("Recording started")
				while self.recording:
					file.write(self._buffer.get())
		self._logger.debug("Recording finished")
	
	def stop_recording(self):
		self.recording = False

	def get_recording(self):
		return self.TEMP_FILE_NAME

	def callback(self, indata, frames, time, status):
		if status:
			self._logger.error(f"Audio recording error: {status}")
		self._buffer.put(indata.copy())
