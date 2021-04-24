import logging
import queue
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

		self._logger = logging.getLogger()
		self._filename = filename
		self._stream = None
		self._current_frame = 0
		self._q = queue.Queue()
		self.on_finish = on_finish
		self._data, self._fs = sf.read(self._filename, always_2d=True)
	
	def play(self):
		"""Start the playback at the default output device"""

		self._stream = sd.OutputStream(
			callback=self._callback, samplerate=self._fs, channels=self._data.shape[1],
			finished_callback=self._on_finish_internal
		)
		self._stream.start()
	
	def reset(self):
		"""Reset the player (for re-using the audio file)"""

		if not self._stream:
			return
		self._current_frame = 0

	def _callback(self, outdata: numpy.ndarray, frames: int, time, status: sd.CallbackFlags):
		if status:
			self._logger.warning(status)
		chunksize = min(len(self._data) - self._current_frame, frames)
		outdata[:chunksize] = self._data[self._current_frame:(self._current_frame + chunksize)]
		if chunksize < frames:
			outdata[chunksize:] = 0
			raise sd.CallbackStop()
		self._current_frame += chunksize
	
	def _on_finish_internal(self):
		self._stream.stop()
		self._stream.close()
		if self.on_finish:
			self.on_finish()
