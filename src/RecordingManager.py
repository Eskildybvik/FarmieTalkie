import logging
import queue
import threading
import sounddevice as sd
import soundfile as sf
import numpy
assert numpy


class RecordingManager:
	"""Helper class for recording audio files.
	
	The recording process is ran in a separate thread.
	Saves the recording to a fixed file, whose path can be retrieved using 
	get_recording()
	"""

	SAMPLE_RATE = 44100
	TEMP_FILE_NAME = "recording_temp.wav"

	def __init__(self):
		self._logger = logging.getLogger(__name__)
		self._buffer = queue.Queue()

	def start_recording(self):
		"""Begin recording audio from the default microphone"""
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
		"""Stop recording. Does nothing if no recording is in progress"""
		self.recording = False

	def get_recording(self) -> str:
		"""Get path of the recorded wav file"""
		return self.TEMP_FILE_NAME

	def callback(self, indata: numpy.ndarray, frames: int, time, status: sd.CallbackFlags):
		if status:
			self._logger.error(f"Audio recording error: {status}")
		self._buffer.put(indata.copy())
