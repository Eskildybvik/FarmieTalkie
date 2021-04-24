import logging
import threading
import sounddevice as sd
import soundfile as sf
import numpy # Needs to be loaded for sounddevice to work correctly
assert numpy # Prevents "not used" warning


class PlaybackManager:
	"""Helper class for playing audio files asynchronously.
	
	Usage: 
	1. Select a sound file in the constructor
	2. Use the play method to play it at the systems default output device
	If re-using the same player multiple times, call reset() between each call of play()
	"""

	def __init__(self, filename: str, on_finish: callable = None):
		"""
		Parameters
		----------
		filename : str
			Path to the sound file to play
		on_finish : callable
			Callback for when audio is finished
		"""

		self.__logger = logging.getLogger()
		self.__filename = filename
		self.__stream = None
		self.__current_frame = 0
		self.on_finish = on_finish
		self.__data, self.__samplerate = sf.read(self.__filename, always_2d=True)
	
	def play(self):
		"""Start the playback at the default output device"""

		self.__stream = sd.OutputStream(
			callback=self.__callback, samplerate=self.__samplerate, channels=self.__data.shape[1],
			finished_callback=self.__on_finish_internal
		)
		self.__stream.start()
	
	def reset(self):
		"""Reset the player (for re-using the audio file)"""

		if not self.__stream:
			return
		self.__current_frame = 0

	def __callback(self, outdata: numpy.ndarray, frames: int, time, status: sd.CallbackFlags):
		if status:
			self.__logger.warning(status)
		chunksize = min(len(self.__data) - self.__current_frame, frames)
		outdata[:chunksize] = self.__data[self.__current_frame:(self.__current_frame + chunksize)]
		if chunksize < frames:
			outdata[chunksize:] = 0
			raise sd.CallbackStop()
		self.__current_frame += chunksize
	
	def __on_finish_internal(self):
		self.__stream.stop()
		self.__stream.close()
		if self.on_finish:
			self.on_finish()
