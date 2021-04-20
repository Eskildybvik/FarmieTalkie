from appJar import gui
import stmpy
import logging


class GUIHandler():
	def press(self, button):
		self._logger.debug(f"Button pressed: {button}")
		if button == "RECORD":
			self.stm.send("record_button_press")
		elif button == "BACK":
			self.stm.send("back_button_press")

	def __init__(self, stm: stmpy.Machine):
		self._logger = logging.getLogger(__name__)
		self.stm = stm
		self.app = gui("FarmieTalkie")
		self.app.addButtons(["RECORD", "BACK"], lambda btn: self.press(btn))
		self.app.go()

# http://appjar.info/simpleAppJar/
# app.addButtons(["Submit", "Cancel"], press)