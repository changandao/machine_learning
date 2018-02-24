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


from matplotlib import cm
from PyQt4 import QtCore
import PyQt4.QtGui as QtWidgets


class DensityEstimationParameters(QtWidgets.QDialog):


	def __init__(self, parent):
		super(DensityEstimationParameters, self).__init__(parent)
		
		self.__parent = parent
		self.__currentTab = 0
		
		# Histogram tab
		histogramBinsXLabel = QtWidgets.QLabel('Number of bins per unit in x direction')
		histogramBinsYLabel = QtWidgets.QLabel('Number of bins per unit in y direction')
		histogramColormapLabel = QtWidgets.QLabel('Color map')
		self.histogramColormapCombobox = self.createColormapCombobox()
		self.histogramBinsXEdit = QtWidgets.QLineEdit('1')
		self.histogramBinsYEdit = QtWidgets.QLineEdit('1')

		histogramGrid = QtWidgets.QGridLayout();
		histogramGrid.setSpacing(10)
		histogramGrid.addWidget(histogramBinsXLabel, 0, 0)
		histogramGrid.addWidget(self.histogramBinsXEdit, 0, 1)
		histogramGrid.addWidget(histogramBinsYLabel, 1, 0)
		histogramGrid.addWidget(self.histogramBinsYEdit, 1, 1)
		histogramGrid.addWidget(histogramColormapLabel, 2, 0)
		histogramGrid.addWidget(self.histogramColormapCombobox, 2, 1)

		histogramFrame = QtWidgets.QGroupBox()
		histogramFrame.setTitle('Histogram estimation')		
		histogramFrame.setLayout(histogramGrid)
		
		histogramLayout = QtWidgets.QVBoxLayout()
		histogramLayout.addWidget(histogramFrame)
		histogramLayout.addStretch(1)
		
		self.histogramTab = QtWidgets.QWidget()
		self.histogramTab.setLayout(histogramLayout)


		# Sphere Density Estimation tab
		sphereNeighborsLabel = QtWidgets.QLabel('Number of neighbors inside the sphere')
		sphereColormapLabel = QtWidgets.QLabel('Color map')
		self.sphereNeighborsEdit = QtWidgets.QLineEdit('1')
		self.sphereColormapCombobox = self.createColormapCombobox()

		sphereGrid = QtWidgets.QGridLayout();
		sphereGrid.setSpacing(10)
		sphereGrid.addWidget(sphereNeighborsLabel, 0, 0)
		sphereGrid.addWidget(self.sphereNeighborsEdit, 0, 1)
		sphereGrid.addWidget(sphereColormapLabel, 2, 0)
		sphereGrid.addWidget(self.sphereColormapCombobox, 2, 1)

		sphereFrame = QtWidgets.QGroupBox()
		sphereFrame.setTitle('Sphere Density Estimation')		
		sphereFrame.setLayout(sphereGrid)
		
		sphereLayout = QtWidgets.QVBoxLayout()
		sphereLayout.addWidget(sphereFrame)
		sphereLayout.addStretch(1)
		
		self.sphereTab = QtWidgets.QWidget()
		self.sphereTab.setLayout(sphereLayout)


		# Kernel Density Estimation tab
		kernelDensityEstimationAlgorithmLabel = QtWidgets.QLabel('Algorithm') 
		kernelDensityEstimationKernelLabel = QtWidgets.QLabel('Kernel function')
		kernelDensityEstimationBandwidthLabel = QtWidgets.QLabel('Bandwidth')
		kernelDensityEstimationColormapLabel = QtWidgets.QLabel('Color map')
		self.kernelDensityEstimationAlgorithmCombobox = QtWidgets.QComboBox()
		self.kernelDensityEstimationAlgorithmCombobox.addItem('KernelDensity (scikit-learn)')
		self.kernelDensityEstimationAlgorithmCombobox.addItem('Kernel Density Estimation')
		self.kernelDensityEstimationAlgorithmCombobox.currentIndexChanged.connect(self.onKernelDensityEstimationAlgorithmChanged)
		self.kernelDensityEstimationKernelCombobox = QtWidgets.QComboBox()
		self.kernelDensityEstimationKernelCombobox.addItem('Gaussian')
		self.kernelDensityEstimationKernelCombobox.addItem('Tophat')
		self.kernelDensityEstimationKernelCombobox.addItem('Epanechnikov')
		self.kernelDensityEstimationKernelCombobox.addItem('Exponential')
		self.kernelDensityEstimationKernelCombobox.addItem('Linear')
		self.kernelDensityEstimationKernelCombobox.addItem('Cosine')
		self.kernelDensityEstimationBandwidthEdit = QtWidgets.QLineEdit('1.0')
		self.kernelDensityEstimationColormapCombobox = self.createColormapCombobox()
		
		kernelDensityEstimationGrid = QtWidgets.QGridLayout();
		kernelDensityEstimationGrid.setSpacing(10)
		kernelDensityEstimationGrid.addWidget(kernelDensityEstimationAlgorithmLabel, 0, 0)
		kernelDensityEstimationGrid.addWidget(self.kernelDensityEstimationAlgorithmCombobox, 0, 1)
		kernelDensityEstimationGrid.addWidget(kernelDensityEstimationKernelLabel, 1, 0)
		kernelDensityEstimationGrid.addWidget(self.kernelDensityEstimationKernelCombobox, 1, 1)
		kernelDensityEstimationGrid.addWidget(kernelDensityEstimationBandwidthLabel, 2, 0)
		kernelDensityEstimationGrid.addWidget(self.kernelDensityEstimationBandwidthEdit, 2, 1)
		kernelDensityEstimationGrid.addWidget(kernelDensityEstimationColormapLabel, 3, 0)
		kernelDensityEstimationGrid.addWidget(self.kernelDensityEstimationColormapCombobox, 3, 1)
		
		kernelDensityEstimationFrame = QtWidgets.QGroupBox()
		kernelDensityEstimationFrame.setTitle('Kernel Density Estimation')		
		kernelDensityEstimationFrame.setLayout(kernelDensityEstimationGrid)
		
		kernelDensityEstimationLayout = QtWidgets.QVBoxLayout()
		kernelDensityEstimationLayout.addWidget(kernelDensityEstimationFrame)
		kernelDensityEstimationLayout.addStretch(1)
		
		self.kernelDensityEstimationTab = QtWidgets.QWidget()
		self.kernelDensityEstimationTab.setLayout(kernelDensityEstimationLayout)

		# Create notebook tabs		
		self.notebook = QtWidgets.QTabWidget()
		self.notebook.addTab(self.histogramTab, "Histogram")
		self.notebook.addTab(self.sphereTab, "Sphere")
		self.notebook.addTab(self.kernelDensityEstimationTab, "Kernel")
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
		
		self.setWindowTitle('Density estimation parameters')
		self.reject = self.onReject


	def createColormapCombobox(self):
		box = QtWidgets.QComboBox()
		box.addItem('Greys (white to black)')
		box.addItem('gray (black to white)')
		box.addItem('Blues (white to blue)')
		box.addItem('Purples (white to purple)')
		box.addItem('Greens (white to green)')
		box.addItem('Reds (white to red)')
		box.addItem('Coolwarm (blue to red)')
		box.addItem('YlOrRd (yellow to red)')
		box.setCurrentIndex(7) # YlOrRd
		return box


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
		if tab == 0: # Histogram parameters
			if not self.testParameter(self.getHistogramBinsX, 'The number of bins per unit in x direction has to be a floating point number!'):
				return False
			
			if not self.testParameter(self.getHistogramBinsY, 'The number of bins per unit in y direction has to be a floating point number!'):
				return False
			
			n = self.getHistogramBinsX()
			if n <= 0: 
				self.errorMsg('The number of bins per unit in x direction has to be positive!')
				return False

			n = self.getHistogramBinsY()
			if n <= 0: 
				self.errorMsg('The number of bins per unit in y direction has to be positive!')
				return False

		elif tab == 1: # Sphere Density Estimation parameters
			if not self.testParameter(self.getSphereDensityEstimationNeighbors, 'The number of neighbors has to be an integer number!'):
				return False

			n = self.getSphereDensityEstimationNeighbors()
			if n <= 0: 
				self.errorMsg('The number of neighbors inside the sphere has to be positive!')
				return False

		elif tab == 2: # Kernel Density Estimation parameters
			if not self.testParameter(self.getKernelDensityEstimationBandwidth, 'The bandwidth of the kernel function has to be a floating point number!'):
				return False
			
			w = self.getKernelDensityEstimationBandwidth()
			if w <= 0: 
				self.errorMsg('The bandwidth of the kernel function has to be positive!')
				return False

		return True


	def onAccept(self):
		if not self.checkParameters(self.notebook.currentIndex()):
			return		
		super(DensityEstimationParameters, self).accept()


	def onReject(self):
		self.restoreParameters()
		super(DensityEstimationParameters, self).reject()


	def showEvent(self, event):
		self.__parameters = self.getParameters()


	def getParameters(self):
		params = {}
		params['histo_binsx'] = self.histogramBinsXEdit.text()
		params['histo_binsy'] = self.histogramBinsYEdit.text()
		params['histo_colormap'] = self.histogramColormapCombobox.currentIndex()
		params['sphere_neighbors'] = self.sphereNeighborsEdit.text()
		params['sphere_colormap'] = self.sphereColormapCombobox.currentIndex()
		params['kde_algorithm'] = self.kernelDensityEstimationAlgorithmCombobox.currentIndex()
		params['kde_kernel'] = self.kernelDensityEstimationKernelCombobox.currentIndex()
		params['kde_bandwidth'] = self.kernelDensityEstimationBandwidthEdit.text()
		params['kde_colormap'] = self.kernelDensityEstimationColormapCombobox.currentIndex()
		return params


	def restoreParameters(self):
		params = self.__parameters
		self.histogramBinsXEdit.setText(params['histo_binsx'])
		self.histogramBinsYEdit.setText(params['histo_binsy'])
		self.histogramColormapCombobox.setCurrentIndex(params['histo_colormap'])
		self.sphereNeighborsEdit.setText(params['sphere_neighbors'])
		self.sphereColormapCombobox.setCurrentIndex(params['sphere_colormap'])
		self.kernelDensityEstimationAlgorithmCombobox.setCurrentIndex(params['kde_algorithm'])
		self.kernelDensityEstimationKernelCombobox.setCurrentIndex(params['kde_kernel'])
		self.kernelDensityEstimationBandwidthEdit.setText(params['kde_bandwidth'])
		self.kernelDensityEstimationColormapCombobox.setCurrentIndex(params['kde_colormap'])


	def onTabChanged(self, idx):
		if not self.checkParameters(self.__currentTab):
			currentTab = self.__currentTab
			self.__currentTab = idx
			self.notebook.setCurrentIndex(currentTab)
		else:
			self.__currentTab = idx


	def setTab(self, tab):
		if tab >= 0:
			self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Estimate density")
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


	def getHistogramBinsX(self):
		return float(self.histogramBinsXEdit.text())


	def getHistogramBinsY(self):
		return float(self.histogramBinsYEdit.text())


	def getHistogramColormap(self):
		idx = self.histogramColormapCombobox.currentIndex()
		return self.idx2Colormap(idx)


	def getSphereDensityEstimationNeighbors(self):
		return int(self.sphereNeighborsEdit.text())


	def getSphereDensityEstimationColormap(self):
		idx = self.sphereColormapCombobox.currentIndex()
		return self.idx2Colormap(idx)


	def onKernelDensityEstimationAlgorithmChanged(self, idx):
		if idx == 0: # KernelDensity (scikit-learn)
			self.kernelDensityEstimationKernelCombobox.setEnabled(True) 
		else: # Kernel Density Estimation
			self.kernelDensityEstimationKernelCombobox.setEnabled(False)
			self.kernelDensityEstimationKernelCombobox.setCurrentIndex(0) # Gaussian


	def getKernelDensityEstimationAlgorithm(self):
		idx = self.kernelDensityEstimationAlgorithmCombobox.currentIndex()
		if idx == 0:
			return "sklearn"
		else:
			return "KernelDensityEstimation"


	def getKernelDensityEstimationKernel(self):
		return self.kernelDensityEstimationKernelCombobox.currentText().lower()


	def getKernelDensityEstimationBandwidth(self):
		return float(self.kernelDensityEstimationBandwidthEdit.text())


	def getKernelDensityEstimationColormap(self):
		idx = self.kernelDensityEstimationColormapCombobox.currentIndex()
		return self.idx2Colormap(idx)


	def idx2Colormap(self, idx):
		if idx == 0: # Greys (from white to black)
			return cm.Greys
		elif idx == 1: # gray (from black to white)
			return cm.gray
		elif idx == 2: # Blues (from white to blue)
			return cm.Blues
		elif idx == 3: # Purples (from white to purple)
			return cm.Purples
		elif idx == 4: # Greens (from white to green)
			return cm.Greens
		elif idx == 5: # Reds (from white to green)
			return cm.Reds
		elif idx == 6: # coolwarm (from blue to red)
			return cm.coolwarm
		else: # YlOrRd (from yellow to red)
			return cm.YlOrRd



