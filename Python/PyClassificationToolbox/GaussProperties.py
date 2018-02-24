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
from PyQt4 import QtCore
import PyQt4.QtGui as QtWidgets

import Parameters


class GaussProperties(QtWidgets.QDialog):
	
	def __init__(self, classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded, parent = None):
		super(GaussProperties, self).__init__(parent)
		
		layout = QtWidgets.QVBoxLayout(self)

		classLabel = QtWidgets.QLabel('class label')
		numSamplesLabel = QtWidgets.QLabel('number of samples')
		mean1Label = QtWidgets.QLabel('x1')
		mean2Label = QtWidgets.QLabel('x2')
		cov11Label = QtWidgets.QLabel('cov(x1, x1)')
		cov22Label = QtWidgets.QLabel('cov(x2, x2)')
		cov12Label = QtWidgets.QLabel('cov(x1, x2)')
		
		self.classComboBox = QtWidgets.QComboBox()
		for i in range(Parameters.NUMBER_SUPPORTED_CLASSES):
			self.classComboBox.addItem('Class {0}'.format(i + 1))
		
		self.numSamplesEdit = QtWidgets.QLineEdit()
		self.isIncludedCheckBox = QtWidgets.QCheckBox("included in the feature space")
		self.isIncludedCheckBox.setChecked(isIncluded)
		self.mean1Edit = QtWidgets.QLineEdit()
		self.mean2Edit = QtWidgets.QLineEdit()
		self.cov11Edit = QtWidgets.QLineEdit()
		self.cov22Edit = QtWidgets.QLineEdit()
		self.cov12Edit = QtWidgets.QLineEdit()

		classFrame = QtWidgets.QGroupBox(self)
		classFrame.setTitle('General information')
		classGrid = QtWidgets.QGridLayout();
		classGrid.setSpacing(10)
		classGrid.addWidget(classLabel, 0, 0)
		classGrid.addWidget(self.classComboBox, 0, 1)
		classGrid.addWidget(numSamplesLabel, 1, 0)
		classGrid.addWidget(self.numSamplesEdit, 1, 1)
		classGrid.addWidget(self.isIncludedCheckBox, 2, 0, 1, 2, QtCore.Qt.AlignLeft)
		classFrame.setLayout(classGrid)
		
		meanFrame = QtWidgets.QGroupBox(self)
		meanFrame.setTitle('Mean vector')
		meanGrid = QtWidgets.QGridLayout();
		meanGrid.setSpacing(10)
		meanGrid.addWidget(mean1Label, 0, 0)
		meanGrid.addWidget(self.mean1Edit, 0, 1)
		meanGrid.addWidget(mean2Label, 1, 0)
		meanGrid.addWidget(self.mean2Edit, 1, 1)
		meanFrame.setLayout(meanGrid)
		
		covFrame = QtWidgets.QGroupBox(self)
		covFrame.setTitle('Covariance matrix')
		covGrid = QtWidgets.QGridLayout();
		covGrid.setSpacing(10)
		covGrid.addWidget(cov11Label, 0, 0)
		covGrid.addWidget(self.cov11Edit, 0, 1)
		covGrid.addWidget(cov22Label, 1, 0)
		covGrid.addWidget(self.cov22Edit, 1, 1)
		covGrid.addWidget(cov12Label, 2, 0)
		covGrid.addWidget(self.cov12Edit, 2, 1)
		covFrame.setLayout(covGrid)
		
		layout.addWidget(classFrame)
		layout.addWidget(meanFrame)
		layout.addWidget(covFrame)		
		
		self.setProperties(classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded)

		# OK and Cancel buttons
		self.buttons = QtWidgets.QDialogButtonBox(
			QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
			QtCore.Qt.Horizontal, self)
		layout.addWidget(self.buttons)

		self.buttons.accepted.connect(self.onAccept)
		self.buttons.rejected.connect(self.reject)
		
		self.setWindowTitle('Gaussian properties')

	
	def onAccept(self):
		try:
			int(self.numSamplesEdit.text())
		except:
			QtWidgets.QMessageBox.warning(self, 'Error',
                                          "The number of samples is not a valid integer value!", 
                                          QtWidgets.QMessageBox.Ok, 
                                          QtWidgets.QMessageBox.Ok)
			return
		
		try:
			float(self.mean1Edit.text())
			float(self.mean2Edit.text())
		except:
			QtWidgets.QMessageBox.warning(self, 'Error',
                                          "The components of the mean vector are not valid float values!", 
                                          QtWidgets.QMessageBox.Ok, 
                                          QtWidgets.QMessageBox.Ok)
			return
				
		try:
			cov11 = float(self.cov11Edit.text())
			cov22 = float(self.cov22Edit.text())
			cov12 = float(self.cov12Edit.text())
		except:
			QtWidgets.QMessageBox.warning(self, 'Error',
                                          "The components of the covariance matrix are not valid float values!", 
                                          QtWidgets.QMessageBox.Ok, 
                                          QtWidgets.QMessageBox.Ok)
			return
		
		if cov11 < 0 or cov22 < 0:
			QtWidgets.QMessageBox.warning(self, 'Error',
                                          "The components on the main diagonal of the covariance matrix have to be non-negative values!", 
                                          QtWidgets.QMessageBox.Ok, 
                                          QtWidgets.QMessageBox.Ok)
			return
		
		if math.fabs(cov12) > math.sqrt(cov11 * cov22):
			QtWidgets.QMessageBox.warning(self, 'Error',
                                          "Invalid value for cov(x1, x2)!", 
                                          QtWidgets.QMessageBox.Ok, 
                                          QtWidgets.QMessageBox.Ok)
			return

		super(GaussProperties, self).accept() 


	def setProperties(self, classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded):
		self.classComboBox.setCurrentIndex(classId)
		self.numSamplesEdit.setText(str(numSamples))
		self.isIncludedCheckBox.setChecked(isIncluded)
		self.mean1Edit.setText(str(mean1))
		self.mean2Edit.setText(str(mean2))
		self.cov11Edit.setText(str(cov11))
		self.cov22Edit.setText(str(cov22))
		self.cov12Edit.setText(str(cov12))


	def getProperties(self):
		classId = self.classComboBox.currentIndex()
		numSamples = int(self.numSamplesEdit.text())
		mean1 = float(self.mean1Edit.text())
		mean2 = float(self.mean2Edit.text())
		cov11 = float(self.cov11Edit.text())
		cov22 = float(self.cov22Edit.text())
		cov12 = float(self.cov12Edit.text())
		isIncluded = self.isIncludedCheckBox.isChecked()
		
		return (classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded)
