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
import numpy.matlib
from PyQt4 import QtCore, QtGui
import PyQt4.QtGui as QtWidgets

from GaussProperties import GaussProperties
from MyColors import MyColors
from Operation import Operation
import Parameters


class Gaussian2D(object):

	# class attribute
	
	POINT = 1
	CROSS = 2
	SQUARE = 3
	CIRCLE = 4
	
	ACTION_MOVE = 11
	ACTION_CHANGE_COVMAT = 12
	
	NONE = 21
	MOVING_CENTER = 22
	MOVING_SIGMA1 = 23
	MOVING_SIGMA2 = 24
	MOVING_COR = 25
	
	# maximum number of samples that being displayed during a mouse move; used to speed up the paint method
	maxNumSamplesDisplayed = 0
	
	numGaussians = 0
	

	def __init__(self, widget, classId, num_samples = 1000, mean = numpy.zeros(2), covmat = numpy.eye(2), isIncluded = True, raw_samples = None, statusbar = None):
		super(Gaussian2D, self).__init__()
				
		self.__classId = classId
		self.__num_samples = num_samples
		
		# IMPORTANT: make sure not to work with integers even if the user initially provides integer values
		self.__mean = mean.astype(numpy.float64)
		self.__covmat = covmat.astype(numpy.float64)
		
		if raw_samples == None:
			self.__raw_samples = self.mvnrdn(self.__num_samples)
		else:
			self.__raw_samples = raw_samples
			
		self.__excluded = not isIncluded
			
		self.__widget = widget
		self.__statusbar = statusbar
		
		self.myInit()		
		self.__createContextMenu(widget)


	def myInit(self):
		self.__id = self.numGaussians
		type(self).numGaussians += 1
		# print("new Gaussian with ID {0}".format(self.__id))
				
		if self.__covmat[0, 0] < 1e-10:
			self.__covmat[0, 0] = 1e-10
			
		if self.__covmat[1, 1] < 1e-10:
			self.__covmat[1, 1] = 1e-10
			
		maxcor = math.sqrt(self.__covmat[0, 0] * self.__covmat[1, 1])
		if self.__covmat[0, 1] > maxcor - 1e-10:
			self.__covmat[0, 1] = maxcor - 1e-10
		elif self.__covmat[0, 1] < -maxcor + 1e-10:
			self.__covmat[0, 1] = -maxcor + 1e-10		
		self.__covmat[1, 0] = self.__covmat[0, 1]
			
		self.__sigma1 = math.sqrt(self.__covmat[0, 0])
		self.__sigma2 = math.sqrt(self.__covmat[1, 1])
		self.__maxcor = math.sqrt(self.__covmat[0, 0] * self.__covmat[1, 1])
		self.__samples = self.mvnrdn(len(self.__raw_samples[0]), self.__mean, self.__covmat, self.__raw_samples)
		self.__mean_estimated = numpy.mean(self.__samples, 1)
		self.__covmat_estimated = numpy.cov(self.__samples)

		self.__pointstyle = self.SQUARE
		self.__pointsize = 1
		
		self.__pen = QtGui.QPen()		
		self.__pen.setWidth(1)
		self.__pen.setStyle(QtCore.Qt.SolidLine)
		self.__pen.setBrush(QtCore.Qt.gray)
		
		self.__brush = QtGui.QBrush(QtCore.Qt.gray)
		
		self.__ellipsePen = QtGui.QPen()		
		self.__ellipsePen.setWidth(2)
		self.__ellipsePen.setStyle(QtCore.Qt.SolidLine)
		self.__ellipsePen.setBrush(QtCore.Qt.black)
		
		self.__ellipseBrush = QtGui.QBrush(QtCore.Qt.black)
		
		c = 200
		self.__inactivePen = QtGui.QPen()
		self.__inactivePen.setWidth(1)
		self.__inactivePen.setStyle(QtCore.Qt.SolidLine)
		self.__inactivePen.setBrush(QtGui.QColor(c, c, c))
		
		self.__inactiveBrush = QtGui.QBrush(QtGui.QColor(c, c, c))
		
		c = 230
		self.__inactiveSamplesPen = QtGui.QPen()
		self.__inactiveSamplesPen.setWidth(1)
		self.__inactiveSamplesPen.setStyle(QtCore.Qt.SolidLine)
		self.__inactiveSamplesPen.setBrush(QtGui.QColor(c, c, c))
		
		self.__inactiveSamplesBrush = QtGui.QBrush(QtGui.QColor(c, c, c))
		
		self.__controlPen = QtGui.QPen()
		self.__controlPen.setWidth(2)
		self.__controlPen.setStyle(QtCore.Qt.SolidLine)
		self.__controlPen.setBrush(QtCore.Qt.black)
		
		self.__controlBrush = QtGui.QBrush(QtCore.Qt.black)

		self.setColors()
		
		self.__mouse_pressed = False;
		self.__mouse_dragging = False;
		self.__action = self.ACTION_MOVE
		self.__mouse_operation = self.NONE
		self.__active = True
	
	
	def __getstate__(self):
		return (self.__classId, self.__num_samples, self.__mean, self.__covmat, self.__raw_samples, self.__excluded)
	
	
	def __setstate__(self, state):
		(self.__classId, self.__num_samples, self.__mean, self.__covmat, self.__raw_samples, self.__excluded) = state
		self.myInit()
	
		
	def __createContextMenu(self, widget):
		self.contextMenu = QtWidgets.QMenu(widget)
		
		self.propertyAction = self.contextMenu.addAction("Properties")
		# self.propertyAction.setEnabled(False)
		
		menu = self.contextMenu.addMenu("Class labels")
		
		group = QtWidgets.QActionGroup(widget, exclusive = True)
		self.classActions = list()
		for i in range(Parameters.NUMBER_SUPPORTED_CLASSES):
			action = group.addAction(QtWidgets.QAction("Class {0}".format(i + 1), widget, checkable = True))
			self.classActions.append(action)
			menu.addAction(action)
		
		self.classActions[self.__classId].setChecked(True)
				
		self.contextMenu.addMenu(menu)		
		self.contextMenu.addSeparator()		
		self.excludeAction = self.contextMenu.addAction("Exclude Gaussian")		
		self.convertAction = self.contextMenu.addAction("Convert to samples")		
		self.deleteAction = self.contextMenu.addAction("Delete Gaussian")


	def setWidgets(self, widget, statusbar):
		self.__widget = widget
		self.__statusbar = statusbar
		self.__createContextMenu(widget)
		
		
	def __setColor(self, color):
		self.__pen.setBrush(color)
		self.__brush.setColor(color)
		
	def __getColor(self):
		return self.__pen.color()
	
	def __setEllipseColor(self, color):
		self.__ellipsePen.setBrush(color)
		self.__ellipseBrush.setColor(color)
		
	def __getEllipseColor(self):
		return self.__ellipsePen.color()
	
	def __setControlColor(self, color):
		self.__controlPen.setBrush(color)
		self.__controlBrush.setColor(color)
		
	def __getControlColor(self):
		return self.__controlPen.color()
	
	color = property(__getColor, __setColor)
	ellipseColor = property(__getEllipseColor, __setEllipseColor)
	controlColor = property(__getControlColor, __setControlColor)


	def setColors(self, classId = None):
		if classId == None:
			classId = self.__classId
		_, c2, c3 = MyColors.qcolorsForClass(classId)
		self.color, self.ellipseColor, self.controlColor = c2, c3, c3


	def getId(self):
		return self.__id


	def setClassId(self, classId, undoOperation = False):
		if self.__classId != classId:
			oldClassId = self.__classId
			self.__classId = classId
			self.setColors()

			if not undoOperation:
				return Operation(self.__widget, "Gaussian2D.setClassId", (self.__id, self.__classId, oldClassId))

		return None


	def getClassId(self):
		return self.__classId


	def setNumSamples(self, numSamples):
		if numSamples < 1 or numSamples == self.__num_samples:
			return
		
		if numSamples <= len(self.__samples[0]):
			self.__num_samples = numSamples
		else:
			n = numSamples -	len(self.__samples[0])
			new_raw_samples = self.mvnrdn(n)
			new_samples = self.mvnrdn(n, self.__mean, self.__covmat, new_raw_samples)
			self.__raw_samples = numpy.append(self.__raw_samples, new_raw_samples, axis = 1)
			self.__samples =	numpy.append(self.__samples, new_samples, axis = 1)
			self.__num_samples = len(self.__samples[0])

		self.__widget.repaint()
			

	def setAction(self, action):
		if self.__action == action:
			return False
		self.__action = action
		return True


	def deactivate(self):
		if not self.__active:
			return False
		self.__active = False
		return True


	def activate(self):
		if self.__active:
			return False
		self.__active = True
		return True


	def normrdn_generator(self):
		twopi	= 2 * numpy.pi
		while True:
			u1 = numpy.random.random()
			u2 = numpy.random.random()
			h = math.sqrt(-2.0 * math.log(u1))
			z0 = h * math.cos(twopi * u2)
			z1 = h * math.sin(twopi * u2)
			yield z0
			yield z1
			
	
	def normrdn(self, n = 1, mu = 0, sigma = 1):
		values = numpy.zeros(n)
		generator = self.normrdn_generator()
		for i in range(n):
			values[i] = next(generator)
		return sigma * values + mu


	def mvnrdn(self, n = 1, mean = numpy.zeros(2), covmat = numpy.eye(2), values = None):
		d = len(mean)
		assert len(covmat) == len(covmat[0]), "The covariance matrix must be quadratic"
		assert d == len(covmat), "The dimensions of the mean vector and the covariance matrix do not match"
		L = numpy.linalg.cholesky(covmat)
		if values is None:
			values = numpy.zeros((d, n))
			for i in range(d):
				values[i] = self.normrdn(n, 0, 1)
		return numpy.dot(L, values) + numpy.matlib.repmat(mean.reshape((d, 1)), 1, n)


	def setMean(self, x, y):
		self.__mean = numpy.array([x, y])
		self.__samples = self.mvnrdn(len(self.__samples[0]), self.__mean, self.__covmat, self.__raw_samples)
		self.__mean_estimated = numpy.mean(self.__samples, 1)
	
	
	def setSigma(self, component, sigma):
		ratio = self.__covmat[0, 1] / self.__maxcor
		if sigma < 1e-5:
			sigma = 1e-5
		if component == 0:
			self.__sigma1 = sigma
		else:	
			self.__sigma2 = sigma
		self.__covmat[component, component] = sigma * sigma
		self.__maxcor = math.sqrt(self.__covmat[0, 0] * self.__covmat[1, 1])
		self.__covmat[0, 1] = self.__covmat[1, 0] = ratio * self.__maxcor
		self.__samples = self.mvnrdn(len(self.__samples[0]), self.__mean, self.__covmat, self.__raw_samples)
		self.__covmat_estimated = numpy.cov(self.__samples)


	def setCov12(self, ratio):
		limit = 1 - 1e-16
		if ratio > limit:
			ratio = limit
		elif ratio < -limit:
			ratio = -limit
		self.__covmat[0, 1] = self.__covmat[1, 0] = ratio * self.__maxcor
		self.__samples = self.mvnrdn(len(self.__samples[0]), self.__mean, self.__covmat, self.__raw_samples)
		self.__covmat_estimated = numpy.cov(self.__samples)


	def getSamples(self):
		if self.__excluded:
			return numpy.empty((0, 2))
		else:
			return self.__samples[:,0:self.__num_samples].T
		

	def cov_ellipse(self, n = 100, mean = None, covmat = None):
		if mean is None:
			mean = self.__mean
		if covmat is None:
			covmat = self.__covmat
		a1 = math.sqrt(covmat[0, 0]);
		a3 = covmat[0, 1] / a1;
		a2 = math.sqrt(covmat[1, 1] - a3 * a3);
		t = numpy.linspace(0, 2 * numpy.pi, n)
		x1 = a1 * numpy.cos(t) + mean[0]
		x2 = a3 * numpy.cos(t) + a2 * numpy.sin(t) + mean[1]
		return numpy.r_['0,2', x1, x2]


	def paint(self, qp, coordinateSystem):
		if self.__excluded:
			self.setColors(classId = -1)
		else:
			self.setColors()
		
		# draw samples
		if self.__active:
			qp.setPen(self.__pen)
			qp.setBrush(self.__brush)
		else:
			qp.setPen(self.__inactiveSamplesPen)
			qp.setBrush(self.__inactiveSamplesBrush)
			
		if not self.__excluded:
			w = 2 * self.__pointsize
			display_max_samples = self.__num_samples
			if self.maxNumSamplesDisplayed > 0 and display_max_samples > self.maxNumSamplesDisplayed:
				display_max_samples = self.maxNumSamplesDisplayed
			for (x1, x2) in self.__samples[:,0:display_max_samples].T:
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

		# draw covariance ellipse
		if not self.__active or self.__action == self.ACTION_CHANGE_COVMAT:
			qp.setPen(self.__inactivePen)
		else:
			qp.setPen(self.__ellipsePen)
		ellipse = self.cov_ellipse()
		x1_old = 0
		x2_old = 0
		for i, (x1, x2) in enumerate(ellipse.T):
			x1, x2 = coordinateSystem.world2screen(x1, x2)
			if i > 0:
				qp.drawLine(x1_old, x2_old, x1, x2)
				
			x1_old = x1
			x2_old = x2
		
		# draw center
		self.__cx, self.__cy = coordinateSystem.world2screen(self.__mean[0], self.__mean[1])
		ellipsePenWidth = self.__ellipsePen.width()
		if not self.__active or self.__action == self.ACTION_CHANGE_COVMAT:
			qp.setPen(self.__inactivePen)
		else:
			self.__ellipsePen.setWidth(1)
			qp.setPen(self.__ellipsePen)
		qp.setBrush(QtCore.Qt.NoBrush)
		r = 5
		qp.drawEllipse(self.__cx - r, self.__cy - r, 2 * r, 2 * r)
		if not self.__active or self.__action == self.ACTION_CHANGE_COVMAT:
			qp.setBrush(self.__inactiveBrush)
		else:	
			qp.setBrush(self.__ellipseBrush)
		r = 3
		qp.drawEllipse(self.__cx - r, self.__cy - r, 2 * r, 2 * r)
		self.__ellipsePen.setWidth(ellipsePenWidth)
		
		# draw controls
		if self.__action == self.ACTION_CHANGE_COVMAT:
			self.__sigma1 = math.sqrt(self.__covmat[0, 0])
			self.__sigma2 = math.sqrt(self.__covmat[1, 1])
			x1, y1 = coordinateSystem.world2screen(self.__mean[0] - self.__sigma1, self.__mean[1] - self.__sigma2)
			x2, y2 = coordinateSystem.world2screen(self.__mean[0] + self.__sigma1, self.__mean[1] + self.__sigma2)
			w = x2 - x1
			h = y2 - y1
			controlPenWidth = self.__controlPen.width()
			qp.setPen(self.__controlPen)
			qp.setBrush(QtCore.Qt.NoBrush)
			qp.drawRect(x1, y1, w, h)
			qp.drawLine(x1, y1, x1 + w, y1 + h)
		
			ratio = self.__covmat[0, 1] / self.__maxcor
			self.__rx = int(x1 + (1 + ratio) * w / 2)
			self.__ry = int(y1 + (1 + ratio) * h / 2)
			r = 5
			self.__controlPen.setWidth(1)
			qp.setPen(self.__controlPen)
			qp.drawEllipse(self.__rx - r, self.__ry - r, 2 * r, 2 * r)
			qp.setBrush(self.__controlBrush)
			r = 3
			qp.drawEllipse(self.__rx - r, self.__ry - r, 2 * r, 2 * r)		
			self.__controlPen.setWidth(controlPenWidth)
				

	def mouseNearCenter(self, mx, my):
		return self.__action == self.ACTION_MOVE and math.pow(mx - self.__cx, 2) + math.pow(my - self.__cy, 2) < 25
	
	
	def mouseNearRatioButton(self, mx, my):	
		return self.__action == self.ACTION_CHANGE_COVMAT and math.pow(mx - self.__rx, 2) + math.pow(my - self.__ry, 2) < 25
	
	
	def mouseNearSigma1Boundary(self, mx, my, coordinateSystem):
		if self.__action == self.ACTION_CHANGE_COVMAT:
			x1, y1 = coordinateSystem.world2screen(self.__mean[0] - self.__sigma1, self.__mean[1] + self.__sigma2)
			x2, y2 = coordinateSystem.world2screen(self.__mean[0] + self.__sigma1, self.__mean[1] - self.__sigma2)
			if math.fabs(mx - x1) < 2 and my > y1 and my < y2: # left edge of the bounding box
				return True
			if math.fabs(mx - x2) < 2 and my > y1 and my < y2: # right edge of the bounding box
				return True
		return False

	
	def mouseNearSigma2Boundary(self, mx, my, coordinateSystem):
		if self.__action == self.ACTION_CHANGE_COVMAT:
			x1, y1 = coordinateSystem.world2screen(self.__mean[0] - self.__sigma1, self.__mean[1] + self.__sigma2)
			x2, y2 = coordinateSystem.world2screen(self.__mean[0] + self.__sigma1, self.__mean[1] - self.__sigma2)
			if math.fabs(my - y1) < 2 and mx > x1 and mx < x2: # top edge of the bounding box
				return True
			if math.fabs(my - y2) < 2 and mx > x1 and mx < x2: # bottom edge of the bounding box
				return True
		return False
		

	def mousePressEvent(self, ev, widget, coordinateSystem):
		if not self.paintReady():
			return (False, None)
		
		self.__mouse_operation = self.NONE
		
		mx = ev.pos().x()
		my = ev.pos().y()
		
		if ev.button() == QtCore.Qt.LeftButton:
			if self.mouseNearCenter(mx, my):
				self.__mouse_operation = self.MOVING_CENTER
			elif self.mouseNearRatioButton(mx, my):
				self.__mouse_operation = self.MOVING_COR
			elif self.mouseNearSigma1Boundary(mx, my, coordinateSystem):
				self.__mouse_operation = self.MOVING_SIGMA1
			elif self.mouseNearSigma2Boundary(mx, my, coordinateSystem):
				self.__mouse_operation = self.MOVING_SIGMA2

			if not self.__mouse_operation == self.NONE:
				self.__oldProperties = self.getProperties()
				self.__mouse_pressed = True
				self.__mouse_dragging = False
				self.__mouse_start_x = mx
				self.__mouse_start_y = my
				return (True, None)
		elif ev.button() == QtCore.Qt.RightButton:
			if self.mouseNearCenter(mx, my):
				self.updateContextMenu()
				action = self.contextMenu.exec_(widget.mapToGlobal(ev.pos()))
				if action == self.propertyAction:
					return self.editProperties()
				elif action == self.excludeAction:
					op = self.toggleExclusion()
					return (True, op)
				elif action == self.convertAction:
					widget.convertGaussian(self.__id)
				elif action == self.deleteAction:
					return widget.deleteGaussian(self.__id)
				else:
					for i, clAction in enumerate(self.classActions):
						if action == clAction:
							op = self.setClassId(i)
							return (True, op)
			
		return (False, None)


	def updateContextMenu(self):
		if self.__excluded:
			self.excludeAction.setText("Include Gaussian")
		else:
			self.excludeAction.setText("Exclude Gaussian")

		for i, clAction in enumerate(self.classActions):
			if i == self.__classId:
				clAction.setChecked(True)
			else:
				clAction.setChecked(False)


	def toggleExclusion(self, undoOperation = False):
		self.__excluded = not self.__excluded

		if not undoOperation:
			return Operation(self.__widget, "Gaussian2D.toggleExclusion", (self.__id))

		return None



	def isExcluded(self):
		return self.__excluded

	
	def isIncluded(self):
		return not self.__excluded


	def mouseMoveEvent(self, ev, widget, coordinateSystem):
		if not self.paintReady():
			return False
		
		mx = ev.pos().x()
		my = ev.pos().y()
		
		if self.__mouse_pressed:
			self.__mouse_dragging = True
			type(self).maxNumSamplesDisplayed = 2000
			
			ex, ey = coordinateSystem.screen2world(mx, my)
			ex = int(ex * 100 + 0.5) / 100.0
			ey = int(ey * 100 + 0.5) / 100.0
			
			if self.__action == self.ACTION_MOVE and self.__mouse_operation == self.MOVING_CENTER:
				self.setMean(ex, ey)
				self.__statusbar.showMessage("Center at ({0}, {1})".format(ex, ey))
				widget.repaint()
			elif self.__action == self.ACTION_CHANGE_COVMAT and self.__mouse_operation == self.MOVING_SIGMA1:
				sigma = int(math.fabs(ex - self.__mean[0]) * 100 + 0.5) / 100.0
				self.setSigma(0, sigma)
				self.__statusbar.showMessage("Sigma1 = {0}".format(sigma))
				widget.repaint()
			elif self.__action == self.ACTION_CHANGE_COVMAT and self.__mouse_operation == self.MOVING_SIGMA2:
				sigma = int(math.fabs(ey - self.__mean[1]) * 100 + 0.5) / 100.0
				self.setSigma(1, sigma)
				self.__statusbar.showMessage("Sigma2 = {0}".format(sigma))
				widget.repaint()
			elif self.__action == self.ACTION_CHANGE_COVMAT and self.__mouse_operation == self.MOVING_COR:
				cov12 = (ex - self.__mean[0]) / self.__sigma1
				if cov12 > 1.0:
					cov12 = 1.0
				elif cov12 < -1.0:
					cov12 = -1.0
				self.setCov12(cov12)
				self.__statusbar.showMessage("Correlation = {0:0.2f}".format(cov12))				
				widget.repaint()
				
			return True
		else:
			# change mouse cursors
			if self.mouseNearCenter(mx, my):
				widget.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
				return True
			elif self.mouseNearRatioButton(mx, my):
				widget.setCursor(QtGui.QCursor(QtCore.Qt.SizeBDiagCursor))
				return True
			elif self.mouseNearSigma1Boundary(mx, my, coordinateSystem):
				widget.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
				return True
			elif self.mouseNearSigma2Boundary(mx, my, coordinateSystem):
				widget.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
				self.__mouse_operation = self.MOVING_SIGMA2
				return True
		return False


	def mouseReleaseEvent(self, ev, coordinateSystem):
		if not self.paintReady():
			return (False, None)
		
		if ev.button() == QtCore.Qt.LeftButton and not self.__mouse_operation == self.NONE:
			mx = ev.pos().x()
			my = ev.pos().y()
			
			self.__mouse_pressed = False
			
			if self.__mouse_dragging:
				self.__mouse_dragging = False
				type(self).maxNumSamplesDisplayed = 0
				
				ex, ey = coordinateSystem.screen2world(mx, my)
				ex = int(ex * 100 + 0.5) / 100.0
				ey = int(ey * 100 + 0.5) / 100.0
				
				if self.__action == self.ACTION_MOVE and self.__mouse_operation == self.MOVING_CENTER:
					(_, _, ex2, ey2, _, _, _, _) = self.__oldProperties
					oldParams = (ex2, ey2)
					newParams = (ex, ey)
					self.setMean(ex, ey)
					self.__statusbar.showMessage('')
					op = Operation(self.__widget, "Gaussian2D.setMean", (self.__id, newParams, oldParams))
					return (True, op)
				elif self.__action == self.ACTION_CHANGE_COVMAT and self.__mouse_operation == self.MOVING_SIGMA1:
					sigma = int(math.fabs(ex - self.__mean[0]) * 100 + 0.5) / 100.0
					self.setSigma(0, sigma)
					self.__statusbar.showMessage('')
					(_, _, _, _, oldSigma, _, _, _) = self.__oldProperties
					op = Operation(self.__widget, "Gaussian2D.setSigma", (self.__id, 0, sigma, oldSigma))
					return (True, op)
				elif self.__action == self.ACTION_CHANGE_COVMAT and self.__mouse_operation == self.MOVING_SIGMA2:
					sigma = int(math.fabs(ey - self.__mean[1]) * 100 + 0.5) / 100.0
					self.setSigma(1, sigma)
					self.__statusbar.showMessage('')
					(_, _, _, _, _, oldSigma, _, _) = self.__oldProperties
					op = Operation(self.__widget, "Gaussian2D.setSigma", (self.__id, 1, sigma, oldSigma))
					return (True, op)
				elif self.__action == self.ACTION_CHANGE_COVMAT and self.__mouse_operation == self.MOVING_COR:
					cov12 = (ex - self.__mean[0]) / self.__sigma1
					self.setCov12(cov12)
					self.__statusbar.showMessage('')
					(_, _, _, _, _, _, oldCov12, _) = self.__oldProperties
					op = Operation(self.__widget, "Gaussian2D.setCov12", (self.__id, cov12, oldCov12))
					return (True, op)
			else:
				if math.pow(mx - self.__cx, 2) + math.pow(my - self.__cy, 2) < 25:
					if self.__action == self.ACTION_MOVE:
						self.__action = self.ACTION_CHANGE_COVMAT
					else:
						self.__action = self.ACTION_MOVE
					return (True, None)
		return (False, None)


	def paintReady(self):
		# make sure that these two attributes are defined by paint
		try:
			_ = self.__cx
			_ = self.__cy
		except:
			return False
		return True


	def editProperties(self):			
		propertyForm = GaussProperties(self.__classId, self.__num_samples, 
																	 self.__mean[0], self.__mean[1], 
																	 self.__covmat[0, 0], self.__covmat[1, 1], self.__covmat[0, 1],
																	 not self.__excluded, 
																	 self.__widget)
		result = propertyForm.exec_()
			
		if result == QtWidgets.QDialog.Accepted:					 
			(classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded) = propertyForm.getProperties()
			
			if cov11 < 1e-10:
				cov11 = 1e-10
			if cov22 < 1e-10:
				cov22 = 1e-10
			maxcor = math.sqrt(cov11 * cov22)
			if cov12 > maxcor - 1e-10:
				cov12 = maxcor - 1e-10
			elif cov12 < -maxcor + 1e-10:
				cov12 = -maxcor + 1e-10

			oldParams = (self.__classId, self.__num_samples, self.__mean[0], self.__mean[1], 
						self.__covmat[0, 0], self.__covmat[1, 1], self.__covmat[0, 1], not self.__excluded)
			newParams = (classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded)
			if (oldParams != newParams):
				self.setProperties(classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded)
			
				op = Operation(self.__widget, "Gaussian2D.editProperties", (self.__id, newParams, oldParams))
			
				return (True, op)
			
		return (False, None)


	def setProperties(self, classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded):
			self.__classId = classId
			self.setColors()			
			
			self.setNumSamples(numSamples)
			
			self.__excluded = not isIncluded

			self.__mean[0] = mean1
			self.__mean[1] = mean2
			self.__covmat[0, 0] = cov11
			self.__covmat[1, 1] = cov22
			self.__covmat[1, 0] = cov12
			self.__covmat[0, 1] = cov12

			self.__samples = self.mvnrdn(len(self.__samples[0]), self.__mean, self.__covmat, self.__raw_samples)
			self.__mean_estimated = numpy.mean(self.__samples, 1)
			self.__covmat_estimated = numpy.cov(self.__samples)


	def getProperties(self):
		return (self.__classId, self.__num_samples, self.__mean[0], self.__mean[1], self.__covmat[0, 0], self.__covmat[1, 1], self.__covmat[0, 1], not self.__excluded)



