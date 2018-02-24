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
import numpy
import pickle
import re
import sys
from PyQt4 import QtCore, QtGui
import PyQt4.QtGui as QtWidgets

from CoordinateSystem import CoordinateSystem
from Gaussian2D import Gaussian2D
from GaussProperties import GaussProperties
from Operation import Operation
from Samples2D import Samples2D


class FeatureSpace(QtWidgets.QWidget):

	ACTION_COORDINATE_SYSTEM = 1
	ACTION_CREATE_GAUSSIAN = 2
	ACTION_MODIFY_GAUSSIAN = 3
	ACTION_CREATE_SAMPLES = 4
	

	def __init__(self, widget, statusbar, dock):
		super(FeatureSpace, self).__init__()
		
		self.__widget = widget
		self.__statusbar = statusbar
		self.__dock = dock
		self.__mouse_pressed = False
		self.__mouse_dragging = False
		self.__hideSamples = False
		self.__filename = None
		self.__dir = ''
		self.__classificationImage = None
		
		w = self.size().width()
		h = self.size().height()
		self.buffer = QtGui.QPixmap(w, h)
		
		self.setMouseTracking(True) # fires MouseMoveEvents even if no mouse button is pressed
		
		self.coordinateSystem = CoordinateSystem(self, w, h, -5.1, 5.1, -5.1, 5.1)
		
		self.__action = self.ACTION_COORDINATE_SYSTEM		
		# self.__action = self.ACTION_MODIFY_GAUSSIAN
		# self.__action = self.ACTION_CREATE_GAUSSIAN  
		self.setMouseCursor()		
		
		self.gaussians = list()
		self.deletedGaussians = list()
		
		self.samples = Samples2D(widget, self, dock)
		
		self.__spanRectPen = QtGui.QPen(QtCore.Qt.black)
		self.__spanRectPen.setWidth(1)
		self.__spanRectPen.setStyle(QtCore.Qt.DashLine)


	def sizeHint(self):
		return QtCore.QSize(1024, 1024)


	def setClassificationImage(self, img):
		self.__classificationImage = img
	

	def getClassificationImage(self):
		return self.__classificationImage


	def loadDefaultFeatureSpace(self, filename):
		with open(filename, 'rb') as f:
			(self.gaussians, self.samples) = pickle.load(f)
		for gaussian in self.gaussians:
			gaussian.setWidgets(self, self.__statusbar)
		self.samples.setWidgets(self.__widget, self, self.__dock)


	def saveDefaultFeatureSpace(self, filename):
		with open(filename, 'wb') as f:
			data = (self.gaussians, self.samples)
			pickle.dump(data, f)


	def new(self):
		self.__filename = None
		self.__classificationImage = None
		self.__hideSamples = False
		self.gaussians = list()
		self.samples.clear()
		self.repaint()


	def open(self):
		filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', self.__dir, 'Python Pickle file (*.p)')
		
		if filename:
			try:
				with open(filename, 'rb') as f:
					(self.gaussians, self.samples) = pickle.load(f)
			
				self.__filename = filename					
				self.__dir = QtCore.QFileInfo(filename).absoluteDir().absolutePath()
				self.__classificationImage = None
				self.__hideSamples = False
			
				for gaussians in self.gaussians:
					gaussians.setWidgets(self, self.__statusbar)
				self.samples.setWidgets(self.__widget, self, self.__dock)
				self.repaint()
			except Exception as e:			
				QtWidgets.QMessageBox.warning(self, 'Error',
                                              "Error reading the feature space from {0}: {1}".format(filename, e),
                                              QtWidgets.QMessageBox.Ok,
                                              QtWidgets.QMessageBox.Ok)
				self.new()


	def save(self):
		if self.__filename == None:
			self.saveAs()
		else:
			self.saveFile(self.__filename)
		
	
	def saveAs(self):
		filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', self.__dir, 'Python Pickle file (*.p)')

		if filename:
			self.saveFile(filename)
		
		
	def saveFile(self, filename):	
		try:
			with open(filename, 'wb') as f:
				data = (self.gaussians, self.samples)
				pickle.dump(data, f)

			self.__filename = filename
			self.__dir = QtCore.QFileInfo(filename).absoluteDir().absolutePath()
		except:
			self.__filename = None
			QtWidgets.QMessageBox.warning(self, 'Error',
										  "Error writing the feature space to {0}".format(filename),
										  QtWidgets.QMessageBox.Ok,
										  QtWidgets.QMessageBox.Ok)
		
	
	def exportFile(self):
		filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', self.__dir, 'CSV (*.csv);;ASCII (*.txt);; all files (*.*)')

		if filename:
			try:
				with open(filename, 'w') as f:
					for gaussian in self.gaussians:
						label = gaussian.getClassId()
						samples = gaussian.getSamples()
						for sample in samples:
							f.write("{0:.10f},{1:.10f},{2:d}\n".format(sample[0], sample[1], label))
					samples = self.samples.getSamples()
					for sample in samples:
						f.write("{0:.10f},{1:.10f},{2:d}\n".format(sample[0], sample[1], int(sample[2])))

			except:
				QtWidgets.QMessageBox.warning(self, 'Error',
											  "Error exporting the feature space to {0}".format(filename),
											  QtWidgets.QMessageBox.Ok,
											  QtWidgets.QMessageBox.Ok)		


	def exportImage(self):
		filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', self.__dir, 'Portable Network Graphics (*.png);;JPEG (*.jpg);;Windows Bitmap (*.bmp);;all files (*.*)')
		
		if filename:
			try:
				w = self.size().width()
				h = self.size().height()
				buf = self.buffer.copy(QtCore.QRect(0, 0, w, h))
				buf.save(filename)
			except:
				QtWidgets.QMessageBox.warning(self, 'Error',
											  "Error saving the feature space as image to file {0}".format(filename),
											  QtWidgets.QMessageBox.Ok,
											  QtWidgets.QMessageBox.Ok)		

	def importFile(self):
		filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', self.__dir, 'CSV (*.csv);;ASCII (*.txt);;all files(*.*)')

		if filename:
			i = 0
			try:
				samples = numpy.empty(shape = (3, 0), dtype = numpy.float64)
				with open(filename, 'r') as f:
					for line in f.readlines():
						i += 1
						line = line.strip()
						parts = re.split('[, \t]+', line)
						x = float(parts[0])
						y = float(parts[1])
						l = int(parts[2])
						sample = numpy.array([[x], [y], [l]])
						if len(parts) == 3:
							samples = numpy.append(samples, sample, axis = 1)
						else:
							print('Corrupt line: {0}'.format(line), file=sys.stderr)
							
				op = Operation(self, "FeatureSpace.importFile", (samples))
				self.__widget.operationStack.add(op)

				self.samples.addNewSamples(samples)
			except:
				if i > 0:
					msg = "Error importing feature space from {0} in line {1}: {2}".format(filename, i, line)
				else:
					msg = "Error importing feature space from {0}".format(filename)
				QtWidgets.QMessageBox.warning(self, 'Error', msg, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)		


	def setMouseCursor(self):
		if self.__action == self.ACTION_COORDINATE_SYSTEM:
			self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
		else:
			self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
	

	def getNumberOfGaussians(self):
		NoG = 0
		for gaussian in self.gaussians:
			if gaussian.isIncluded():
				NoG += 1
		return NoG


	def getNumberOfClasses(self):
		classes = set()
		for gaussian in self.gaussians:
			classes.add(gaussian.getClassId())
		classes.update(self.samples.getSamples()[:, 2])
		return len(classes)


	def getSamples(self):
		samples = numpy.empty(shape = (0, 2), dtype = numpy.float64)
		labels = numpy.empty(shape = (0), dtype = numpy.int)

		for gaussian in self.gaussians:
			newSamples = gaussian.getSamples()
			newLabel = gaussian.getClassId()
			newLabels = newLabel * numpy.ones(len(newSamples), dtype = numpy.int)
			samples = numpy.append(samples, newSamples, axis = 0)
			labels = numpy.append(labels, newLabels, axis = 0)
			
		newSamples = self.samples.getSamples()[:, 0:2]
		newLabels = self.samples.getSamples()[:, 2]
		samples = numpy.append(samples, newSamples, axis = 0)
		labels = numpy.append(labels, newLabels, axis = 0)			

		return (samples, labels)


	def setLabels(self, labels):
		labelsOld = self.samples.getLabels().copy()		
		self.samples.setLabels(labels)
		op = Operation(self, "Samples2D.setLabels", (labels, labelsOld))
		self.__widget.operationStack.add(op)


	def setSamples(self, samples):
		samplesOld = self.samples.getSamples()[:,0:2].copy()
		self.samples.setSamples(samples)
		op = Operation(self, "Samples2D.setSamples", (samples, samplesOld.T))
		self.__widget.operationStack.add(op)


	def hideSamples(self, hide):
		if self.__hideSamples != hide:
			self.__hideSamples = hide
			self.repaint()


	def paintEvent(self, ev):
		qp = QtGui.QPainter()

		if not self.__mouse_dragging:
			qp.begin(self.buffer)
			if not self.__classificationImage:
				qp.setPen(QtCore.Qt.white)
				qp.setBrush(QtCore.Qt.white)
				qp.drawRect(0, 0, self.size().width(), self.size().height())
			else:
				qp.drawImage(0, 0, self.__classificationImage)
		
			self.coordinateSystem.paint(qp, CoordinateSystem.GRID)


			if not self.__hideSamples:		
				for gaussian in reversed(self.gaussians):
					gaussian.paint(qp, self.coordinateSystem)

				self.samples.paint(qp, self.coordinateSystem)


			self.__widget.paintRegressor(qp)

			self.coordinateSystem.paint(qp, CoordinateSystem.COORDINATE_SYSTEM)
			qp.end()
			
		qp.begin(self)
		qp.drawPixmap(0, 0, self.buffer)
		
		if self.__mouse_dragging:
			if self.__action != self.ACTION_CREATE_SAMPLES or not self.samples.move_samples:
				qp.setPen(self.__spanRectPen)
				w = self.__mouse_end_x - self.__mouse_start_x
				h = self.__mouse_end_y - self.__mouse_start_y
				qp.drawRect(self.__mouse_start_x, self.__mouse_start_y, w, h)
		
		qp.end()


	def resizeEvent(self, ev):
		size = ev.size()
		w = size.width()
		h = size.height()
		
		self.coordinateSystem.setWidgetSize(w, h)
		
		nw = max(int(numpy.ceil(w / 100.0) * 100), self.buffer.width())
		nh = max(int(numpy.ceil(h / 100.0) * 100), self.buffer.height())
		if nw > self.buffer.width() or nh > self.buffer.height():
			self.buffer = QtGui.QPixmap(nw, nh)
		
		qp = QtGui.QPainter()
		qp.begin(self.buffer)
		qp.setPen(QtCore.Qt.white)
		qp.setBrush(QtCore.Qt.white)
		qp.drawRect(0, 0, w, h)		
		qp.end()
		
		if not(self.__widget.densityEstimator is None):
			# resizing requires histogram re-estimation
			self.__widget.runFeatureSpaceComputations(initialize = True)
		else:
			self.__widget.runFeatureSpaceComputations(initialize = False)
		
		
	def mousePressEvent(self, ev):
		if self.__action == self.ACTION_COORDINATE_SYSTEM:
			self.coordinateSystem.mousePressEvent(ev)
		elif self.__action == self.ACTION_CREATE_GAUSSIAN:
			self.__mouse_pressed = True
			self.__mouse_dragging = False
			self.__mouse_start_x = ev.pos().x()
			self.__mouse_start_y = ev.pos().y()
			sx, sy = self.coordinateSystem.screen2world(self.__mouse_start_x, self.__mouse_start_y)
			self.__sx = int(sx * 100 + 0.5) / 100.0
			self.__sy = int(sy * 100 + 0.5) / 100.0
		elif self.__action == self.ACTION_CREATE_SAMPLES:
			self.__mouse_pressed = True
			self.__mouse_dragging = False
			self.__mouse_start_x = ev.pos().x()
			self.__mouse_start_y = ev.pos().y()
			self.__sx, self.__sy = self.coordinateSystem.screen2world(self.__mouse_start_x, self.__mouse_start_y)
			if self.samples.mouseInSelectedArea(self.__sx, self.__sy):
				self.samples.move_samples = True
		elif self.__action == self.ACTION_MODIFY_GAUSSIAN:
			for gaussian in self.gaussians:
				(handled, op) = gaussian.mousePressEvent(ev, self, self.coordinateSystem)
				if handled:
					break
			if handled:
				if not op is None:
					if not self.__widget.runFeatureSpaceComputations(initialize = True):
						self.repaint()
					self.__widget.operationStack.add(op)
			else:
				for gaussian in self.gaussians:
					if gaussian.setAction(gaussian.ACTION_MOVE):
						self.repaint()
						break


	def mouseMoveEvent(self, ev):
		if self.__action == self.ACTION_COORDINATE_SYSTEM:
			self.coordinateSystem.mouseMoveEvent(ev)
		elif self.__action == self.ACTION_CREATE_GAUSSIAN:
			self.__mouse_end_x = ev.pos().x()
			self.__mouse_end_y = ev.pos().y()
			self.__ex, self.__ey = self.coordinateSystem.screen2world(self.__mouse_end_x, self.__mouse_end_y)
			self.__ex = int(self.__ex * 100 + 0.5) / 100.0
			self.__ey = int(self.__ey * 100 + 0.5) / 100.0
			if self.__mouse_pressed:
				self.__mouse_dragging = True
				w = math.fabs(self.__ex - self.__sx)
				h = math.fabs(self.__ey - self.__sy)
				self.__statusbar.showMessage("{0:.2f}, {1:.2f} to {2:.2f}, {3:.2f}; width: {4:.2f}, height: {5:.2f}".format(self.__sx, self.__sy, self.__ex, self.__ey, w, h))
				self.repaint()
			else:
				self.__statusbar.showMessage("{0:.2f}, {1:.2f}".format(self.__ex, self.__ey))
		elif self.__action == self.ACTION_MODIFY_GAUSSIAN:
			handled = False
			for gaussian in self.gaussians:
				if gaussian.mouseMoveEvent(ev, self, self.coordinateSystem):
					handled = True
					break
			if not handled:
				self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
		elif self.__action == self.ACTION_CREATE_SAMPLES:
			self.__mouse_end_x = ev.pos().x()
			self.__mouse_end_y = ev.pos().y()
			self.__ex, self.__ey = self.coordinateSystem.screen2world(self.__mouse_end_x, self.__mouse_end_y)
			if self.__mouse_pressed:
				dx = int(math.fabs(self.__mouse_end_x - self.__mouse_start_x))
				dy = int(math.fabs(self.__mouse_end_y - self.__mouse_start_y))
				if self.samples.move_samples:
					self.__mouse_dragging = True					
				elif dx > 7 or dy > 7: 
					self.__mouse_dragging = True
					self.repaint()
			else:
				if self.samples.mouseInSelectedArea(self.__ex, self.__ey):
					self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
				else:
					self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

				
	def mouseReleaseEvent(self, ev):
		if self.__action == self.ACTION_COORDINATE_SYSTEM:
			op = self.coordinateSystem.mouseReleaseEvent(ev)
			if not(self.__widget.densityEstimator is None):
				# resizing requires histogram re-estimation
				repaint = self.__widget.runFeatureSpaceComputations(initialize = True)
			else:
				repaint = self.__widget.runFeatureSpaceComputations(initialize = False)

			if not op is None:
				self.__widget.operationStack.add(op)

			if not repaint:
				self.repaint()
		elif self.__action == self.ACTION_CREATE_GAUSSIAN:
			self.__mouse_pressed = False	  
			if self.__mouse_dragging:
				self.__mouse_dragging = False
				self.__mouse_end_x = ev.pos().x()
				self.__mouse_end_y = ev.pos().y()				
				self.__ex, self.__ey = self.coordinateSystem.screen2world(self.__mouse_end_x, self.__mouse_end_y)
				self.__ex = int(self.__ex * 100 + 0.5) / 100.0
				self.__ey = int(self.__ey * 100 + 0.5) / 100.0
				(created, op) = self.createGaussian(self.__sx, self.__sy, self.__ex, self.__ey)
				if created:
					if not self.__widget.runFeatureSpaceComputations(initialize = True):
						self.repaint()
					if not op is None:
						self.__widget.operationStack.add(op)
					
		elif self.__action == self.ACTION_MODIFY_GAUSSIAN:
			for gaussian in self.gaussians:
				(handled, op) = gaussian.mouseReleaseEvent(ev, self.coordinateSystem)
				if handled:
					break
			if handled:
				if op is None:
					self.repaint()
				else:
					if not self.__widget.runFeatureSpaceComputations(initialize = True):
						self.repaint()
					self.__widget.operationStack.add(op)
		elif self.__action == self.ACTION_CREATE_SAMPLES:
			self.__mouse_pressed = False
			if self.__mouse_dragging:
				self.__mouse_dragging = False
				self.__mouse_end_x = ev.pos().x()
				self.__mouse_end_y = ev.pos().y()				
				self.__ex, self.__ey = self.coordinateSystem.screen2world(self.__mouse_end_x, self.__mouse_end_y)
				if self.samples.move_samples:
					dx = self.__mouse_end_x - self.__mouse_start_x 
					dy = self.__mouse_end_y - self.__mouse_start_y 
					self.__mouse_start_x += dx
					self.__mouse_start_y += dy
					self.__mouse_end_x += dx
					self.__mouse_end_y += dy
					dx = self.__ex - self.__sx
					dy = self.__ey - self.__sy
					self.samples.moveSamplesInSelectedArea(dx, dy)
					self.samples.move_samples = False
				else:
					self.samples.selectArea(self.__sx, self.__sy, self.__ex, self.__ey)
					count, labels = self.samples.countSamplesInSelectedArea()
					if count == 0:
						self.__statusbar.showMessage('No samples selected')
					elif count == 1:
						self.__statusbar.showMessage('1 sample selected'.format(count))
					elif len(labels) == 1:
						self.__statusbar.showMessage('{0} samples of the same class selected'.format(count))
					else:
						self.__statusbar.showMessage('{0} samples of {1} classes selected'.format(count, len(labels)))
					
					if count > 0:
						self.__dock.assignButton.setEnabled(True)
						self.__dock.deleteButton.setEnabled(True)
					else:
						self.__dock.assignButton.setEnabled(False)
						self.__dock.deleteButton.setEnabled(False)
					
				self.repaint()
			elif self.samples.areaSelected():
				self.samples.deselectArea()
				self.__statusbar.showMessage('')
				self.repaint()
			else:
				self.samples.mouseReleaseEvent(ev, self, self.coordinateSystem)
				if not(self.__widget.densityEstimator is None):
					# resizing requires histogram re-estimation
					repaintDone = self.__widget.runFeatureSpaceComputations(initialize = True)
				else:
					repaintDone = self.__widget.runFeatureSpaceComputations(initialize = False)
				if not repaintDone:
					self.repaint()


	def mouseDoubleClickEvent(self, ev):
		pass

	
	def wheelEvent(self, event):
		if self.__action == self.ACTION_COORDINATE_SYSTEM:
			self.coordinateSystem.wheelEvent(event)
			if not(self.__widget.densityEstimator is None):
				# resizing requires histogram re-estimation
				repaint = self.__widget.runFeatureSpaceComputations(initialize = True)
			else:
				repaint = self.__widget.runFeatureSpaceComputations(initialize = False)

			if not repaint:
				self.repaint()


	def changeAction(self, action):
		self.__action = action
		self.setMouseCursor()
		changes = False

		if action == self.ACTION_CREATE_SAMPLES:			
			for gaussian in self.gaussians:
				if gaussian.deactivate():
					changes = True
		else:
			self.samples.deselectArea()
			for gaussian in self.gaussians:
				if gaussian.activate():
					changes = True
	
		if not action == self.ACTION_MODIFY_GAUSSIAN:
			for gaussian in self.gaussians:
				if gaussian.setAction(gaussian.ACTION_MOVE):
					changes = True
		if changes:
			self.repaint()		  


	def convertGaussian(self, gaussianId, redoOperation = False):
		for i, gaussian in enumerate(self.gaussians):
			if gaussian.getId() == gaussianId:
				break
		samples = self.gaussians[i].getSamples()
		label = self.gaussians[i].getClassId()
		labels = label * numpy.ones((1, len(samples)), dtype = numpy.int)
		samples = numpy.vstack((samples.T, labels))
		_, m = samples.shape
		
		self.samples.addNewSamples(samples)

		self.deletedGaussians.append(self.gaussians[i])
		del self.gaussians[i]

		if not redoOperation:
			op = Operation(self, "FeatureSpace.convertGaussian", (gaussianId, m))
			self.__widget.operationStack.add(op)
		
		self.repaint()


	def getGaussian(self, gaussianId):
		for gaussian in self.gaussians:
			if gaussian.getId() == gaussianId:
				return gaussian


	def deleteGaussian(self, gaussianId, confirmation = True):
		reply = QtWidgets.QMessageBox.Yes
		if confirmation:
			reply = QtWidgets.QMessageBox.question(self, 'Confirmation',
												"Do you really want to delete this Gaussian?", 
												QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
												QtWidgets.QMessageBox.No)

		if reply == QtWidgets.QMessageBox.Yes:

			for i, gaussian in enumerate(self.gaussians):
				if gaussian.getId() == gaussianId:
					break

			self.deletedGaussians.append(self.gaussians[i])
			del self.gaussians[i]
			
			if confirmation:
				# if confirmation == False, the Gaussian was deleted by a redo operation
				op = Operation(self, "FeatureSpace.deleteGaussian", (gaussianId))
				#self.__widget.operationStack.add(op)
				return (True, op)
			
			#self.repaint()

		return (False, None)


	def undeleteGaussian(self, gaussianId):
		# undo operation
		gaussian = self.deletedGaussians.pop()
		self.gaussians.append(gaussian)
		self.repaint()


	def createGaussian(self, x1, y1, x2, y2):
		classId = 0
		numSamples = 1000
		mean1 = int(0.5 * (x1 + x2) * 100) / 100.0
		mean2 = int(0.5 * (y1 + y2) * 100) / 100.0
		cov11 = int(math.pow(0.5 * math.fabs(x2 - x1), 2) * 100) / 100.0
		cov22 = int(math.pow(0.5 * math.fabs(y2 - y1), 2) * 100) / 100.0
		cov12 = 0

		propertyForm = GaussProperties(classId, numSamples, mean1, mean2, cov11, cov22, cov12, True, self)
		result = propertyForm.exec_()

		if result == QtWidgets.QDialog.Accepted:	  
			classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded = propertyForm.getProperties()
			gaussian = Gaussian2D(self, classId, numSamples, numpy.array([mean1, mean2]), numpy.array([[cov11, cov12], [cov12, cov22]]), isIncluded, None, self.__statusbar)
			self.gaussians.append(gaussian)
			gaussianId = len(self.gaussians)
		
			op = Operation(self, "FeatureSpace.createGaussian", (gaussianId))
			# self.__widget.operationStack.add(op)
			
			return (True, op)

		return (False, None)


	def getWidget(self):
		return self.__widget


