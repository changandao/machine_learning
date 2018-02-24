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


import numpy
from PyQt4 import QtCore, QtGui

from MyColors import MyColors
from Operation import Operation


class Samples2D(object):
	
	POINT = 1
	CROSS = 2
	SQUARE = 3
	CIRCLE = 4
	
	def __init__(self, mainwidget, featurespace, dock):
		super(Samples2D, self).__init__()
		
		self.__mainwidget = mainwidget
		self.__featurespace = featurespace
		self.__dock = dock
		self.__samples = numpy.empty(shape = (3, 0), dtype = numpy.float64)
		self.myInit()


	def myInit(self):
		self.__spanRectPen = QtGui.QPen(QtCore.Qt.black)
		self.__spanRectPen.setWidth(1)
		self.__spanRectPen.setStyle(QtCore.Qt.DashLine)
		
		self.__pens = list()
		self.__brushes = list()
		for i in range (10):
			pen, brush = self.createPenAndBrush(i)
			self.__pens.append(pen)
			self.__brushes.append(brush)
		
		self.__pointstyle = self.SQUARE
		self.__pointsize = 2
		self.__areaSelected = False
		self.__area_x1 = 0
		self.__area_x2 = 0
		self.__area_y1 = 0
		self.__area_y2 = 0
		self.move_samples = False


	def setWidgets(self, mainwidget, featurespace, dock):
		self.__mainwidget = mainwidget
		self.__featurespace = featurespace
		self.__dock = dock
		self.deselectArea()


	def __getstate__(self):
		return (self.__samples)


	def __setstate__(self, state):
		(self.__samples) = state
		self.myInit()	


	def createPenAndBrush(self, classId):
		_, _, color = MyColors.qcolorsForClass(classId)
		
		pen = QtGui.QPen()
		pen.setWidth(1)
		pen.setStyle(QtCore.Qt.SolidLine)
		pen.setBrush(color)
		
		brush = QtGui.QBrush(color)

		return (pen, brush)
		

	def clear(self):
		self.__samples = numpy.empty(shape = (3, 0), dtype = numpy.float64)
		self.deselectArea()


	def getSamples(self):
		return self.__samples.T


	def setSamples(self, samples):
		self.__samples[0:2] = samples


	def getLabels(self):
		return self.__samples[2]


	def setLabels(self, labels):
		self.__samples[2] = labels


	def paint(self, qp, coordinateSystem):

		w = 2 * self.__pointsize
		
		for (x1, x2, classId) in self.__samples.T:
			classId = int(classId)
			qp.setPen(self.__pens[classId])
			qp.setBrush(self.__brushes[classId])
			
			x1, x2 = coordinateSystem.world2screen(x1, x2)
			
			if self.__pointstyle == self.CROSS:
				qp.drawLine(x1 - self.__pointsize, x2, x1 + self.__pointsize, x2)
				qp.drawLine(x1, x2 - self.__pointsize, x1, x2 + self.__pointsize)
			elif self.__pointstyle == self.SQUARE:
				qp.drawRect(x1 - self.__pointsize, x2 - self.__pointsize, w, w)
			elif self.__pointstyle == self.CIRCLE:
				qp.drawEllipse(x1 - self.__pointsize, x2 - self.__pointsize, w, w)
			else:
				qp.drawPoint(x1, x2)
		
		if self.__areaSelected:
			qp.setPen(self.__spanRectPen)
			qp.setBrush(QtCore.Qt.NoBrush)
			x1, y1 = coordinateSystem.world2screen(self.__area_x1, self.__area_y1)
			x2, y2 = coordinateSystem.world2screen(self.__area_x2, self.__area_y2)
			qp.drawRect(x1, y1, x2 - x1, y2 - y1)


	def mouseReleaseEvent(self, ev, widget, coordinateSystem):
		if ev.button() == QtCore.Qt.LeftButton:
			mx = ev.pos().x()
			my = ev.pos().y()
			ex, ey = coordinateSystem.screen2world(mx, my)
			ex = int(ex * 100 + 0.5) / 100.0
			ey = int(ey * 100 + 0.5) / 100.0
			classId = self.__dock.getProperties()
			self.addNewSample(ex, ey, classId)


	def addNewSample(self, ex, ey, classId):		
		newSample = numpy.array([[ex], [ey], [classId]])
		self.__samples = numpy.append(self.__samples, newSample, axis = 1)
		self.__mainwidget.runFeatureSpaceComputations(initialize = True)
		op = Operation(self.__featurespace, "Samples2D.addNewSample", newSample)
		self.__featurespace.getWidget().operationStack.add(op)


	def appendNewSample(self, newSample):
		self.__samples = numpy.append(self.__samples, newSample, axis = 1)
		if not self.__mainwidget.runFeatureSpaceComputations(initialize = True):
			self.__mainwidget.featurespace.repaint()


	def addNewSamples(self, samples):
		self.__samples = numpy.append(self.__samples, samples, axis = 1)
		if not self.__mainwidget.runFeatureSpaceComputations(initialize = True):
			self.__mainwidget.featurespace.repaint()


	def removeNewSamples(self, n):
		# undo operation; removes the last n samples
		self.__samples = numpy.delete(self.__samples, numpy.s_[-n:], 1)
		if not self.__mainwidget.runFeatureSpaceComputations(initialize = True):
			self.__mainwidget.featurespace.repaint()


	def countSamplesInSelectedArea(self):
		if not self.__areaSelected:
			return 0
		
		count = 0
		labels = set()
		for sample in self.__samples.T:
			x = sample[0]
			y = sample[1]
			label = int(sample[2])
			if x >= self.__area_x1 and x <= self.__area_x2 and y >= self.__area_y1 and y <= self.__area_y2:
				count += 1
				labels.add(label)
		return (count, labels)


	def areaSelected(self):
		return self.__areaSelected


	def mouseInSelectedArea(self, mx, my):
		if not self.__areaSelected:
			return False
		if mx >= self.__area_x1 and mx <= self.__area_x2 and my >= self.__area_y1 and my <= self.__area_y2:
			return True
		return False


	def selectArea(self, x1, y1, x2, y2):
		if (x2 < x1):
			x1, x2 = x2, x1
		if (y2 < y1):
			y1, y2 = y2, y1
			
		self.__area_x1 = x1
		self.__area_y1 = y1
		self.__area_x2 = x2
		self.__area_y2 = y2
		
		self.__areaSelected = True
		self.__updateList = self.getUpdateList()


	def deselectArea(self):
		self.__areaSelected = False
		self.__dock.assignButton.setEnabled(False)
		self.__dock.deleteButton.setEnabled(False)
		self.__updateList = None



	def getUpdateList(self):
		updateList = list()
		for i, sample in enumerate(self.__samples.T):
			x = sample[0]
			y = sample[1]
			if x >= self.__area_x1 and x <= self.__area_x2 and y >= self.__area_y1 and y <= self.__area_y2:
				updateList.append(i)
		return updateList

		
	def deleteSamplesInSelectedArea(self):
		if self.__areaSelected:
			removeList = self.__updateList
			if len(removeList) > 0:
				area = (self.__area_x1, self.__area_y1, self.__area_x2, self.__area_y2)
				removeSamples = self.__samples[:, removeList]
				self.__samples = numpy.delete(self.__samples, removeList, axis = 1)		
		
				res = self.__mainwidget.runFeatureSpaceComputations(initialize = True)
				if not res:
					self.__featurespace.repaint()

				op = Operation(self.__featurespace, "Samples2D.deleteSamples", (removeSamples, removeList, area))
				self.__featurespace.getWidget().operationStack.add(op)

			self.__areaSelected = False
			self.__dock.deleteButton.setEnabled(False)

			return len(removeList)
		return 0	


	def deleteSamples(self, removeList):
		self.__samples = numpy.delete(self.__samples, removeList, axis = 1)				
		self.__areaSelected = False
		self.__dock.deleteButton.setEnabled(False)
		res = self.__mainwidget.runFeatureSpaceComputations(initialize = True)
		if not res:
			self.__featurespace.repaint()


	def insertSamples(self, samples, removeList, area):
		# undo operation
		self.__area_x1, self.__area_y1, self.__area_x2, self.__area_y2 = area
		self.__updateList = removeList
		self.__areaSelected = True
		self.__dock.deleteButton.setEnabled(True)
		
		# deleted samples have to be inserted at their original positions
		for sample, ind in zip(samples.T, removeList):
			self.__samples = numpy.insert(self.__samples, ind, sample, axis = 1)
		res = self.__mainwidget.runFeatureSpaceComputations(initialize = True)
		if not res:
			self.__featurespace.repaint()


	def assignNewClassLabelInSelectedArea(self, classId):
		if self.__areaSelected:
			updateList = self.__updateList
			if len(updateList) > 0:
				oldLabels = self.__samples[2, updateList]
				area = (self.__area_x1, self.__area_y1, self.__area_x2, self.__area_y2)
				self.__samples[2, updateList] = classId

				res = self.__mainwidget.runFeatureSpaceComputations(initialize = True)
				if not res:
					self.__featurespace.repaint()

				op = Operation(self.__featurespace, "Samples2D.assignClassLabel", (updateList, classId, oldLabels, area))
				self.__featurespace.getWidget().operationStack.add(op)
			return len(updateList)
		return 0


	def assignNewClassLabel(self, updateList, classId, area):
		# in case of an undo/redo operation:
		self.__area_x1, self.__area_y1, self.__area_x2, self.__area_y2 = area
		self.__updateList = updateList
		self.__areaSelected = True
		
		self.__samples[2, updateList] = classId
		res = self.__mainwidget.runFeatureSpaceComputations(initialize = True)
		if not res:
			self.__featurespace.repaint()


	def moveSamplesInSelectedArea(self, dx, dy):
		if self.__areaSelected:			
			updateList = self.__updateList
			m = len(updateList)
			if m > 0:
				oldArea = (self.__area_x1, self.__area_y1, self.__area_x2, self.__area_y2)
				newArea = (self.__area_x1 + dx, self.__area_y1 + dy, self.__area_x2 + dx, self.__area_y2 + dy)
				self.moveSamples(updateList, dx, dy, newArea)
				op = Operation(self.__featurespace, "Samples2D.moveSamples", (updateList, dx, dy, newArea, oldArea))
				self.__featurespace.getWidget().operationStack.add(op)
			else:
				self.__area_x1 += dx
				self.__area_y1 += dy
				self.__area_x2 += dx
				self.__area_y2 += dy				

			return m
		return 0


	def moveSamples(self, updateList, dx, dy, area):
		# in case of an undo/redo operation:
		self.__area_x1, self.__area_y1, self.__area_x2, self.__area_y2 = area
		self.__updateList = updateList
		self.__areaSelected = True
						
		self.__samples[0, updateList] += dx
		self.__samples[1, updateList] += dy
				
		res = self.__mainwidget.runFeatureSpaceComputations(initialize = True)
		if not res:
			self.__featurespace.repaint()



