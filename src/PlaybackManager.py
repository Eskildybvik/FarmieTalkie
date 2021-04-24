import logging
import queue
import threading
import sounddevice as sd
import soundfile as sf
import numpy
assert numpy

class PlaybackManager:
	def __init__(self, filename: str, on_finish: callable = None):
		self._logger = logging.getLogger()
		self.filename = filename
		self._stream = None
		self._current_frame = 0
		self._q = queue.Queue()
		self.on_finish = on_finish
		self.data, self.fs = sf.read(self.filename, always_2d=True)
	
	def play(self):
		self._stream = sd.OutputStream(
			callback=self._callback, samplerate=self.fs, channels=self.data.shape[1],
			finished_callback=self._on_finish_internal
		)
		self._stream.start()
	
	def reset(self):
		if not self._stream:
			return
		self._current_frame = 0

	def _callback(self, outdata, frames, time, status):
		if status:
			self._logger.warning(status)
		chunksize = min(len(self.data) - self._current_frame, frames)
		outdata[:chunksize] = self.data[self._current_frame:(self._current_frame + chunksize)]
		if chunksize < frames:
			outdata[chunksize:] = 0
			raise sd.CallbackStop()
		self._current_frame += chunksize
	
	def _on_finish_internal(self):
		self._stream.stop()
		self._stream.close()
		if self.on_finish:
			self.on_finish()
