import logging
import queue
import threading
import sounddevice as sd
import soundfile as sf
import numpy # Needs to be loaded for sounddevice to work correctly
assert numpy # Prevents "not used" warning

class PlaybackManager:
	def __init__(self, filename: str, on_finish: callable = None):
		self._logger = logging.getLogger()
		self.filename = filename
		self._stream = None
		self._current_frame = 0
		self._q = queue.Queue()
		self.on_finish = on_finish
		self._data, self._fs = sf.read(self.filename, always_2d=True)
	
	def play(self):
		self._stream = sd.OutputStream(
			callback=self._callback, samplerate=self._fs, channels=self._data.shape[1],
			finished_callback=self._on_finish_internal
		)
		self._stream.start()
	
	def reset(self):
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
