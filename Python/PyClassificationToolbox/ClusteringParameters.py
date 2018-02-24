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


from PyQt4 import QtCore
import PyQt4.QtGui as QtWidgets

import Parameters


class ClusteringParameters(QtWidgets.QDialog):

	def __init__(self, parent):
		super(ClusteringParameters, self).__init__(parent)
		
		self.__parent = parent
		self.__currentTab = 0
		
		# k-means tab
		kMeansKLabel = QtWidgets.QLabel('Number of clusters')
		self.kMeansKEdit = QtWidgets.QLineEdit('3')
		
		kMeansGrid = QtWidgets.QGridLayout();
		kMeansGrid.setSpacing(10)
		kMeansGrid.addWidget(kMeansKLabel, 0, 0)
		kMeansGrid.addWidget(self.kMeansKEdit, 0, 1)
		
		kMeansFrame = QtWidgets.QGroupBox()
		kMeansFrame.setTitle('k-Means Clustering')		
		kMeansFrame.setLayout(kMeansGrid)
		
		kMeansLayout = QtWidgets.QVBoxLayout()
		kMeansLayout.addWidget(kMeansFrame)
		kMeansLayout.addStretch(1)
		
		self.kMeansTab = QtWidgets.QWidget()
		self.kMeansTab.setLayout(kMeansLayout)
		
		# GMM tab
		GmmKLabel = QtWidgets.QLabel('Number of clusters')
		GmmNumIterationsLabel = QtWidgets.QLabel('Maximum number of iterations')
		self.GmmKEdit = QtWidgets.QLineEdit('3')
		self.GmmNumIterationsEdit = QtWidgets.QLineEdit('500')
		
		GmmGrid = QtWidgets.QGridLayout();
		GmmGrid.setSpacing(10)
		GmmGrid.addWidget(GmmKLabel, 0, 0)
		GmmGrid.addWidget(self.GmmKEdit, 0, 1)
		GmmGrid.addWidget(GmmNumIterationsLabel, 1, 0)
		GmmGrid.addWidget(self.GmmNumIterationsEdit, 1, 1)
		
		GmmFrame = QtWidgets.QGroupBox()
		GmmFrame.setTitle('Gaussian Mixture Model')		
		GmmFrame.setLayout(GmmGrid)
		
		GmmLayout = QtWidgets.QVBoxLayout()
		GmmLayout.addWidget(GmmFrame)
		GmmLayout.addStretch(1)
		
		self.GmmTab = QtWidgets.QWidget()
		self.GmmTab.setLayout(GmmLayout)


		# Create notebook tabs		
		self.notebook = QtWidgets.QTabWidget()
		self.notebook.addTab(self.kMeansTab, "k-Means")
		self.notebook.addTab(self.GmmTab, "GMM")
		self.notebook.currentChanged.connect(self.onTabChanged)
		
		
		# OK and Cancel buttons
		self.buttons = QtWidgets.QDialogButtonBox(
			QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
			QtCore.Qt.Horizontal, self)
		self.buttons.button(QtWidgets.QDialogButtonBox.Cancel).setText("Cancel")
		self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Compute regression")

		self.buttons.accepted.connect(self.onAccept)
		self.buttons.rejected.connect(self.onReject)
		

		layout = QtWidgets.QVBoxLayout(self)
		layout.addWidget(self.notebook)		
		layout.addWidget(self.buttons)
		
		self.setWindowTitle('Clustering parameters')
		self.reject = self.onReject

	
	def errorMsg(self, msg):
		QtWidgets.QMessageBox.warning(self, 'Error', msg, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)


	def testParameter(self, func, msg):
		try:
			func()
		except:
			self.errorMsg(msg)
			return False
		return True


	def checkParameters(self, tab):
		if tab == 0: # k-means
			if not self.testParameter(self.getKMeansK, 'The number of clusters has to be an integer number!'):
				return False
			
			k = self.getKMeansK()
			if k <= 0: 
				self.errorMsg('The number of clusters has to be positive!')
				return False
			if k > Parameters.NUMBER_SUPPORTED_CLASSES: 
				self.errorMsg('Currently a maximum number of {0} clusters is supported!'.format(Parameters.NUMBER_SUPPORTED_CLASSES))
				return False
		elif tab == 1: # GMM
			if not self.testParameter(self.getGmmK, 'The number of clusters has to be an integer number!'):
				return False

			if not self.testParameter(self.getGmmMaxNumIterations, 'The maximum number of iterations has to be an integer number!'):
				return False
			
			k = self.getGmmK()
			if k <= 0: 
				self.errorMsg('The number of clusters has to be positive!')
				return False
			if k > Parameters.NUMBER_SUPPORTED_CLASSES: 
				self.errorMsg('Currently a maximum number of {0} clusters is supported!'.format(Parameters.NUMBER_SUPPORTED_CLASSES))
				return False

			maxNumIter = self.getGmmMaxNumIterations()
			if maxNumIter < 1:
				self.errorMsg('The maximum number of iterations has to be positive!')
				return False

		return True


	def onAccept(self):
		if not self.checkParameters(self.notebook.currentIndex()):
			return		
		super(ClusteringParameters, self).accept()


	def onReject(self):
		self.restoreParameters()
		super(ClusteringParameters, self).reject()


	def showEvent(self, event):
		self.__parameters = self.getParameters()


	def getParameters(self):
		params = {}
		params['kMeans_k'] = self.kMeansKEdit.text()
		params['GMM_k'] = self.GmmKEdit.text()
		params['GMM_iterations'] = self.GmmNumIterationsEdit.text()
		return params

		
	def restoreParameters(self):
		params = self.__parameters
		self.kMeansKEdit.setText(params['kMeans_k'])
		self.GmmKEdit.setText(params['GMM_k'])
		self.GmmNumIterationsEdit.setText(params['GMM_iterations'])


	def onTabChanged(self, idx):
		if not self.checkParameters(self.__currentTab):
			currentTab = self.__currentTab
			self.__currentTab = idx
			self.notebook.setCurrentIndex(currentTab)
		else:
			self.__currentTab = idx


	def setTab(self, tab):
		if tab >= 0:
			self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Compute clusters")
			self.notebook.setCurrentIndex(tab - 1)
			self.__currentTab = tab - 1
			for i in range(self.notebook.count()):
				if i == tab - 1:
					self.notebook.setTabEnabled(i, True)
				else:
					self.notebook.setTabEnabled(i, False)
		else:
			self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Ok")
			self.notebook.setCurrentIndex(0)
			self.__currentTab = 0
			for i in range(self.notebook.count()):
				self.notebook.setTabEnabled(i, True)


	def getKMeansK(self):
		return int(self.kMeansKEdit.text())


	def getGmmK(self):
		return int(self.GmmKEdit.text())


	def getGmmMaxNumIterations(self):
		return int(self.GmmNumIterationsEdit.text())


