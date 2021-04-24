import logging
import queue
import threading
import sounddevice as sd
import soundfile as sf
import numpy # Needs to be loaded for sounddevice to work correctly
assert numpy # Prevents "not used" warning


class RecordingManager:
	"""Helper class for recording audio files.
	
	The recording process is ran in a separate thread.
	Saves the recording to a fixed file, whose path can be retrieved using 
	get_recording()
	"""

	SAMPLE_RATE = 44100
	TEMP_FILE_NAME = "recording_temp.ogg"

	def __init__(self):
		self.__logger = logging.getLogger(__name__)
		self.__buffer = queue.Queue()

	def start_recording(self):
		"""Begin recording audio from the default microphone"""

		self.recording = True
		recording_thread = threading.Thread(target=self.__thread_function)
		recording_thread.start()
	
	def __thread_function(self):
		with sf.SoundFile(self.TEMP_FILE_NAME, mode="w", 
				samplerate=self.SAMPLE_RATE, channels=1) as file:
			with sd.InputStream(samplerate=self.SAMPLE_RATE, 
					channels=1, callback=self.__callback):
				self.__logger.debug("Recording started")
				while self.recording:
					file.write(self.__buffer.get())
		self.__logger.debug("Recording finished")
	
	def stop_recording(self):
		"""Stop recording. Does nothing if no recording is in progress"""

		self.recording = False

	def get_recording(self) -> str:
		"""Get path of the recorded wav file"""
		
		return self.TEMP_FILE_NAME

	def __callback(self, indata: numpy.ndarray, frames: int, time, status: sd.CallbackFlags):
		if status:
			self.__logger.error(f"Audio recording error: {status}")
		self.__buffer.put(indata.copy())
