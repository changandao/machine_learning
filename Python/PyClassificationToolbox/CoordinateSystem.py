#    Copyright 2016 Stefan Steidl
#    Friedrich-Alexander-Universität Erlangen-Nürnberg
#    Lehrstuhl für Informatik 5 (Mustererkennung)
#    Martensstraße 3, 91058 Erlangen, GERMANY
#    stefan.steidl@fau.de


#    This file is part of the Python Classification Toolbox.
#
#    The Python Classification Toolbox is free software: 
#    you can redistribute it and/or modify it under the terms of the 
#    GNU General Public License as published by the Free Software Foundation, 
#    either version 3 of the License, or (at your option) any later version.
#
#    The Python Classification Toolbox is distributed in the hope that 
#    it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
#    See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with the Python Classification Toolbox.  
#    If not, see <http://www.gnu.org/licenses/>.


import math
from Operation import Operation
from PyQt4 import QtCore, QtGui


class CoordinateSystem(object):
	
	GRID = 1
	COORDINATE_SYSTEM = 2
	
	def __init__(self, featurespace, widget_width, widget_height, xmin = -5.0, xmax = 5.0, ymin = -5.0, ymax = 5.0, equalAxis = True):
		super(CoordinateSystem, self).__init__()

		self.featurespace = featurespace
		self.__showCoordinateSystem = True
		self.__showGrid = True

		self.__mouse_pressed = False
		self.__mouse_dragging = False

		self.__pen = QtGui.QPen()		
		self.__pen.setWidth(1)
		self.__pen.setStyle(QtCore.Qt.SolidLine)
		self.__pen.setBrush(QtCore.Qt.black)
		
		self.__gridPen = QtGui.QPen()
		self.__gridPen.setWidth(1)
		self.__gridPen.setStyle(QtCore.Qt.DashLine)
		self.__gridPen.setBrush(QtGui.QColor(240, 240, 240))

		self.__width = widget_width
		self.__height = widget_height
		self.setLimits(xmin, xmax, ymin, ymax, 0, 0, 0, equalAxis)		
		
			
	def __getColor(self):
		return self.__pen.color()
		
	def __setColor(self, col):
		self.__pen.setBrush(col)
				
		
	def __getGridColor(self):
		return self.__gridPen.color()
	
	def __setGridColor(self, col):
		self.__gridPen.setBrush(col)


	color = property(__getColor, __setColor)
	gridColor = property(__getGridColor, __setGridColor)


	def setLimits(self, xmin, xmax, ymin, ymax, dx = 0, dy = 0, zoom = 0, equalAxis = True):
		self.__equalAxis = equalAxis
		self.__dx, self.__dy = dx, dy
		self.__zoom = min(zoom, self.maxZoomValue(xmax - xmin, ymax - ymin))
		
		self.__preferred_xmin, self.__preferred_xmax = xmin, xmax
		self.__preferred_ymin, self.__preferred_ymax = ymin, ymax
		self.__xmin, self.__xmax = xmin + self.__zoom + dx, xmax - self.__zoom + dx
		self.__ymin, self.__ymax = ymin + self.__zoom + dy, ymax - self.__zoom + dy
		
		rx = self.__xmax - self.__xmin
		ry = self.__ymax - self.__ymin					 
		self.__pixelsXPerUnit = 1.0 * self.__width / rx		
		self.__pixelsYPerUnit = 1.0 * self.__height / ry
		
		if self.__equalAxis:
			self.__pixelsXPerUnit = self.__pixelsYPerUnit = min(self.__pixelsXPerUnit, self.__pixelsYPerUnit)
			
			rangeX = self.__width / self.__pixelsXPerUnit
			self.__xmin = self.__xmin * rangeX / rx
			self.__xmax = self.__xmin + rangeX
			
			rangeY = self.__height / self.__pixelsYPerUnit
			self.__ymin = self.__ymin * rangeY / ry
			self.__ymax = self.__ymin + rangeY
					
		# print("setLimits: [{0}:{1},{2}:{3}]".format(self.__xmin, self.__xmax, self.__ymin, self.__ymax))
		# print("pixels per unit in x: {0}".format(self.__pixelsXPerUnit))
		# print("pixels per unit in y: {0}".format(self.__pixelsYPerUnit))				 
			
		self.__cx, self.__cy = self.world2screen(0, 0)


	def getLimits(self):
		return (self.__xmin, self.__ymin, self.__xmax, self.__ymax)
	

	def getPixelsPerUnit(self):
		return (self.__pixelsXPerUnit, self.__pixelsYPerUnit)

	
	def maxZoomValue(self, rangeX, rangeY):
		return (max(int(rangeX), int(rangeY)) - 1) / 2.0
		# return int(math.ceil((max(int(rangeX), int(rangeY)) - 1) / 2.0))
		
	
	def setWidgetSize(self, width, height):
		self.__width = width
		self.__height = height		
		self.setLimits(self.__preferred_xmin, self.__preferred_xmax, 
									 self.__preferred_ymin, self.__preferred_ymax, 
									 self.__dx, self.__dy,
									 self.__zoom, 
									 self.__equalAxis)


	def world2screen(self, worldX, worldY):
		screenX = int((worldX - self.__xmin) * self.__width	/ (self.__xmax - self.__xmin))
		screenY = int((worldY - self.__ymin) * self.__height / (self.__ymax - self.__ymin))
		return screenX, self.__height - screenY


	def screen2world(self, screenX, screenY):
		screenY = self.__height - screenY
		worldX = (screenX - self.__cx) / self.__pixelsXPerUnit
		worldY = (screenY - self.__height + self.__cy) / self.__pixelsYPerUnit
		return worldX, worldY

	
	def getTicsRange(self, min_value, max_value):
		tics_min = int(min_value) if min_value < 0 else int(math.ceil(min_value))
		tics_max = int(max_value) if max_value > 0 else int(math.floor(max_value))
		tics = list(range(tics_min, tics_max))
		tics.append(tics_max)
		return tics

	
	def paint(self, qp, action):
		if action == self.COORDINATE_SYSTEM and self.__showCoordinateSystem:
			
			# draw both axes
			qp.setPen(self.__pen)
			qp.drawLine(0, self.__cy, self.__width, self.__cy)
			qp.drawLine(self.__cx, 0, self.__cx, self.__height)
						
			# draw xtics
			xtics = self.getTicsRange(self.__xmin, self.__xmax)
			ytics = self.getTicsRange(self.__ymin, self.__ymax)
		
			qp.setPen(self.__pen)
			for x in xtics:
				x, y = self.world2screen(x, 0)
				qp.drawLine(x, y, x, y + 5)

			# draw ytics
			for y in ytics:
				x, y = self.world2screen(0, y)
				qp.drawLine(x, y, x + 5, y)
				
			
		if action == self.GRID and self.__showCoordinateSystem:	

			# draw grid
			if self.__showGrid:
				qp.setPen(self.__gridPen)
				
				xtics = self.getTicsRange(self.__xmin, self.__xmax)
				ytics = self.getTicsRange(self.__ymin, self.__ymax)
				
				for x in xtics:
					if not x == 0:
						x, y = self.world2screen(x, 0)
						qp.drawLine(x, 0, x, self.__height)
					
				for y in ytics:
					if not y == 0:
						x, y = self.world2screen(0, y)
						qp.drawLine(0, y, self.__width, y)


	def wheelEvent(self, event):
		# PyQt5 code:
		# numPixels = event.pixelDelta()
		# numDegrees = event.angleDelta() / 8

		# if not numPixels.isNull():
		# 	delta = numPixels.x() + numPixels.y()
		# else:			
		# 	numSteps = numDegrees / 15
		# 	delta = numSteps.x() + numSteps.y()
		
		# PyQt4 code:
		delta = event.delta()

		if delta > 0:
			self.__zoom += 1
		else:
			self.__zoom -= 1

		self.setLimits(self.__preferred_xmin, self.__preferred_xmax, 
									 self.__preferred_ymin, self.__preferred_ymax, 
									 self.__dx, self.__dy,
									 self.__zoom, 
									 self.__equalAxis)


	def mousePressEvent(self, ev):
			self.__mouse_dragging = False;
			self.__mouse_pressed = True;
			self.__mouse_start_x = ev.pos().x()
			self.__mouse_start_y = ev.pos().y()


	def mouseMoveEvent(self, ev):
		if self.__mouse_pressed:
			self.__mouse_dragging = True
	
	
	def mouseReleaseEvent(self, ev):
		if self.__mouse_dragging:
			self.__mouse_dragging = False
			sx, sy = self.screen2world(self.__mouse_start_x, self.__mouse_start_y)
			ex, ey = self.screen2world(ev.pos().x(), ev.pos().y())
			dx, dy = ex - sx, ey - sy
			self.setLimits(self.__preferred_xmin, self.__preferred_xmax, 
                           self.__preferred_ymin, self.__preferred_ymax, 
                           self.__dx-dx, self.__dy-dy,
                           self.__zoom, 
                           self.__equalAxis)
			return Operation(self.featurespace, "CoordinateSystem.move", (dx, dy))


	def move(self, dx, dy):
		# undo/redo operation
		self.setLimits(self.__preferred_xmin, self.__preferred_xmax,
					self.__preferred_ymin, self.__preferred_ymax, 
					self.__dx-dx, self.__dy-dy,
					self.__zoom,
					self.__equalAxis)
		
