from PyQt4.QtGui import QToolTip, QFont, QColor, QPalette
from PyQt4.QtCore import QPoint


class ToolTip(object):
	def __init__(self, iface):
		self.iface = iface
		self.canvas = iface.mapCanvas()		
   		   
	def show(self, text, toolTipPoint):
		QToolTip.showText(self.canvas.mapToGlobal(self.canvas.mouseLastXY()),str(text), self.canvas)		

   	def deactivate(self):
   		QToolTip.hideText()

