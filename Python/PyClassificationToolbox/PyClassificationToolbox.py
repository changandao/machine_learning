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


import sys
from PyQt4 import QtCore, QtGui
import PyQt4.QtGui as QtWidgets
from sklearn import neural_network

from AboutDialog import AboutDialog
from Classifier import Classifier
from ClassifierParameters import ClassifierParameters
from Clustering import Clustering
from ClusteringParameters import ClusteringParameters
from CreateSamplesProperties import CreateSamplesProperties
from DensityEstimation import DensityEstimation
from DensityEstimationParameters import DensityEstimationParameters
from DimensionalityReduction import DimensionalityReduction
from DimensionalityReductionParameters import DimensionalityReductionParameters
from FeatureSpace import FeatureSpace
from InfoDialog import InfoDialog
from LicenseDialog import LicenseDialog
from Operation import Operation
from OperationStack import OperationStack
from Parameters import resource_path
from ProbabilityDensityViewer import ProbabilityDensityViewer
from Regression import Regression
from RegressionParameters import RegressionParameters


class PyClassificationToolbox(QtWidgets.QMainWindow):

	def __init__(self):
		super(PyClassificationToolbox, self).__init__()

		self.initUI()

		try:
			self.featurespace.loadDefaultFeatureSpace('.featurespace.pyct')
		except:
			print("could not open default feature space")


	def initUI(self):
		self.clusteringParameters = ClusteringParameters(self)
		self.dimRedParameters = DimensionalityReductionParameters(self)
		self.classifierParameters = ClassifierParameters(self)
		self.regressionParameters = RegressionParameters(self)
		self.densityEstimationParameters = DensityEstimationParameters(self)
		self.probabilityDensityViewer = ProbabilityDensityViewer(self)
		self.licenseDialog = LicenseDialog(self)
		self.aboutDialog = AboutDialog(self, self.licenseDialog)
		self.infoDialog = InfoDialog(self)
		self.operationStack = OperationStack(self)

		self.createSamplesDockWidget = CreateSamplesProperties(self)
		self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.createSamplesDockWidget)

		self.statusbar = QtWidgets.QStatusBar()
		self.setStatusBar(self.statusbar)

		self.featurespace = FeatureSpace(self, self.statusbar, self.createSamplesDockWidget)		
		self.setCentralWidget(self.featurespace)
		
		self.classifier = None
		self.regressor = None
		self.densityEstimator = None

		
		featureSpaceNewAction = QtWidgets.QAction('&New', self)
		featureSpaceNewAction.setShortcut('Ctrl+N')
		featureSpaceNewAction.setStatusTip('Create empty feature space')
		featureSpaceNewAction.triggered.connect(self.newFeatureSpace)

		featureSpaceOpenAction = QtWidgets.QAction('&Open...', self)
		featureSpaceOpenAction.setShortcut('Ctrl+O')
		featureSpaceOpenAction.setStatusTip('Load a feature space')
		featureSpaceOpenAction.triggered.connect(self.openFeatureSpace)

		featureSpaceSaveAction = QtWidgets.QAction('&Save', self)
		featureSpaceSaveAction.setShortcut('Ctrl+S')
		featureSpaceSaveAction.setStatusTip('Save the feature space')
		featureSpaceSaveAction.triggered.connect(self.saveFeatureSpace)

		featureSpaceSaveAsAction = QtWidgets.QAction('Save &as...', self)
		featureSpaceSaveAsAction.setStatusTip('Save the feature space to a new file')
		featureSpaceSaveAsAction.triggered.connect(self.saveAsFeatureSpace)

		featureSpaceImportAction = QtWidgets.QAction('&Import samples...', self)
		featureSpaceImportAction.setStatusTip('Read feature vectors from an ASCII file')
		featureSpaceImportAction.triggered.connect(self.importFeatureSpace)

		featureSpaceExportAction = QtWidgets.QAction('&Export samples...', self)
		featureSpaceExportAction.setStatusTip('Write the feature vectors to an ASCII file')
		featureSpaceExportAction.triggered.connect(self.exportFeatureSpace)
		
		featureSpaceSaveImageAction = QtWidgets.QAction('Export as image...', self)
		featureSpaceSaveImageAction.setStatusTip('Export the feature space as image')
		featureSpaceSaveImageAction.triggered.connect(self.exportFeatureSpaceAsImage)

		self.__featureSpaceHideSamplesAction = QtWidgets.QAction('Hide samples', self)
		self.__featureSpaceHideSamplesAction.setStatusTip('Hide all samples')
		self.__featureSpaceHideSamplesAction.setShortcut('F8')
		self.__featureSpaceHideSamplesAction.triggered.connect(self.hideSamples)
		self.__featureSpaceHideSamplesAction.setCheckable(True)
		self.__featureSpaceHideSamplesAction.setChecked(False)

		exitAction = QtWidgets.QAction('&Quit', self)
		exitAction.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
		exitAction.setStatusTip('Exit the Python Classification Toolbox')
		exitAction.triggered.connect(self.close)

		menubar = self.menuBar()
		menubar.setNativeMenuBar(False)
		featureSpaceMenu = menubar.addMenu('&Feature Space')
		featureSpaceMenu.addAction(featureSpaceNewAction)
		featureSpaceMenu.addAction(featureSpaceOpenAction)
		featureSpaceMenu.addAction(featureSpaceSaveAction)
		featureSpaceMenu.addAction(featureSpaceSaveAsAction)
		featureSpaceMenu.addSeparator()
		featureSpaceMenu.addAction(featureSpaceImportAction)
		featureSpaceMenu.addAction(featureSpaceExportAction)
		featureSpaceMenu.addAction(featureSpaceSaveImageAction)
		featureSpaceMenu.addSeparator()
		featureSpaceMenu.addAction(self.__featureSpaceHideSamplesAction)
		featureSpaceMenu.addSeparator()
		featureSpaceMenu.addAction(exitAction)


		clusteringKMeansAction = QtWidgets.QAction('k-Means Clustering...', self)
		clusteringKMeansAction.setStatusTip('k-Means Clustering')
		clusteringKMeansAction.triggered.connect(lambda: self.clusterWithParameters(Clustering.kMeans))

		clusteringGMMAction = QtWidgets.QAction('Gaussian Mixture Model...', self)
		clusteringGMMAction.setStatusTip('Gaussian Mixture Model')
		clusteringGMMAction.triggered.connect(lambda: self.clusterWithParameters(Clustering.GMM))

		clusteringParametersAction = QtWidgets.QAction('Parameters...', self)
		clusteringParametersAction.setStatusTip('Edit the parameters of the clustering algorithms')
		clusteringParametersAction.triggered.connect(self.editClusteringParameters)
		
		clusteringMenu = menubar.addMenu('C&lustering')
		clusteringMenu.addAction(clusteringKMeansAction)
		clusteringMenu.addAction(clusteringGMMAction)
		clusteringMenu.addSeparator()
		clusteringMenu.addAction(clusteringParametersAction)


		dimRedPCAAction = QtWidgets.QAction('Principal Component Analysis...', self)
		dimRedPCAAction.setStatusTip('Principal Component Analysis (PCA)')
		dimRedPCAAction.triggered.connect(lambda: self.reduceDimensionalityWithParameters(DimensionalityReduction.PCA))

		dimRedMenu = menubar.addMenu('&Dimensionality Reduction')
		dimRedMenu.addAction(dimRedPCAAction)


		classificationLogRegAction = QtWidgets.QAction('Linear Logistic Regression...', self)
		classificationLogRegAction.setStatusTip('Linear Logistic Regression classifier')
		classificationLogRegAction.triggered.connect(lambda: self.classifyWithParameters(Classifier.LogReg))

		classificationNormAction = QtWidgets.QAction('Norm classifier...', self)
		classificationNormAction.setStatusTip('Classification based on the distance to the class centers')
		classificationNormAction.triggered.connect(lambda: self.classifyWithParameters(Classifier.Norm))

		classificationNaiveBayesAction = QtWidgets.QAction('Naive Bayes', self)
		classificationNaiveBayesAction.setStatusTip('Naive Bayes classifier')
		classificationNaiveBayesAction.triggered.connect(lambda: self.classify(Classifier.NaiveBayes))

		classificationGaussianAction = QtWidgets.QAction('Gaussian classifier', self)
		classificationGaussianAction.setStatusTip('Gaussian classifier')
		classificationGaussianAction.triggered.connect(lambda: self.classify(Classifier.Gauss))

		classificationGMMAction = QtWidgets.QAction('GMM classifier...', self)
		classificationGMMAction.setStatusTip('Gaussian Mixture Model classifier')
		classificationGMMAction.triggered.connect(lambda: self.classifyWithParameters(Classifier.GMM))

		classificationKNNAction = QtWidgets.QAction('kNN...', self)
		classificationKNNAction.setStatusTip('k Nearest Neighbor classifier')
		classificationKNNAction.triggered.connect(lambda: self.classifyWithParameters(Classifier.kNN))

		classificationLinRegAction = QtWidgets.QAction('Linear Regression...', self)
		classificationLinRegAction.setStatusTip('Linear Regression classifier')
		classificationLinRegAction.triggered.connect(lambda: self.classifyWithParameters(Classifier.LinReg))
		
		classificationPerceptronAction = QtWidgets.QAction('Rosenblatt\'s Perceptron...', self)
		classificationPerceptronAction.setStatusTip('Rosenblatt\'s Perceptron')
		classificationPerceptronAction.triggered.connect(lambda: self.classifyWithParameters(Classifier.Perceptron))

		classificationMLPAction = QtWidgets.QAction('Multilayer Perceptron...', self)
		classificationMLPAction.setStatusTip('Multilayer Perceptron')
		classificationMLPAction.triggered.connect(lambda: self.classifyWithParameters(Classifier.MLP))
		try:
			# requires sklearn >= 0.18.dev0
			neural_network.MLPClassifier()
		except:
			classificationMLPAction.setEnabled(False)

		classificationSVMAction = QtWidgets.QAction('SVM...', self)
		classificationSVMAction.setStatusTip('Support Vector Machine')
		classificationSVMAction.triggered.connect(lambda: self.classifyWithParameters(Classifier.SVM))
		
		classificationDecisionTreeAction = QtWidgets.QAction('Decision Tree...', self)
		classificationDecisionTreeAction.setStatusTip('Decision Tree classifier')
		classificationDecisionTreeAction.triggered.connect(lambda: self.classifyWithParameters(Classifier.DecisionTree))

		classificationRandomForestAction = QtWidgets.QAction('Random Forest...', self)
		classificationRandomForestAction.setStatusTip('Random Forest classifier')
		classificationRandomForestAction.triggered.connect(lambda: self.classifyWithParameters(Classifier.RandomForest))

		classificationParametersAction = QtWidgets.QAction('Parameters...', self)
		classificationParametersAction.setStatusTip('Edit the parameters of the classification algorithms')
		classificationParametersAction.triggered.connect(self.editClassificationParameters)

		classificationNoneAction = QtWidgets.QAction('None', self)
		classificationNoneAction.setStatusTip('Delete classification results')
		classificationNoneAction.triggered.connect(self.unsetClassifier)

		classificationMenu = menubar.addMenu('&Classification')
		classificationMenu.addAction(classificationLogRegAction)
		classificationMenu.addAction(classificationNormAction)
		classificationMenu.addAction(classificationNaiveBayesAction)
		classificationMenu.addAction(classificationGaussianAction)
		classificationMenu.addAction(classificationGMMAction)
		classificationMenu.addAction(classificationKNNAction)
		classificationMenu.addAction(classificationLinRegAction)
		classificationMenu.addAction(classificationPerceptronAction)
		classificationMenu.addAction(classificationMLPAction)
		classificationMenu.addAction(classificationSVMAction)
		classificationMenu.addAction(classificationDecisionTreeAction)
		classificationMenu.addAction(classificationRandomForestAction)
		classificationMenu.addSeparator()
		classificationMenu.addAction(classificationParametersAction)
		classificationMenu.addAction(classificationNoneAction)


		regressionLinRegAction = QtWidgets.QAction('Linear Regression...', self)
		regressionLinRegAction.setStatusTip('Linear Regression')
		regressionLinRegAction.triggered.connect(lambda: self.regressionWithParameters(Regression.LinearRegression))

		regressionSVRAction = QtWidgets.QAction('Support Vector Regression...', self)
		regressionSVRAction.setStatusTip('Support Vector Regression (SVR)')
		regressionSVRAction.triggered.connect(lambda: self.regressionWithParameters(Regression.SVR))
		
		regressionRegressionTreeAction = QtWidgets.QAction('Regression Tree...', self)
		regressionRegressionTreeAction.setStatusTip('Regression Tree')
		regressionRegressionTreeAction.triggered.connect(lambda: self.regressionWithParameters(Regression.RegressionTree))
		
		regressionRegressionForestAction = QtWidgets.QAction('Regression Forest...', self)
		regressionRegressionForestAction.setStatusTip('Regression Forest')
		regressionRegressionForestAction.triggered.connect(lambda: self.regressionWithParameters(Regression.RegressionForest))
		
		regressionParametersAction = QtWidgets.QAction('Parameters...', self)
		regressionParametersAction.setStatusTip('Edit the parameters of the regression algorithms')
		regressionParametersAction.triggered.connect(self.editRegressionParameters)

		regressionNoneAction = QtWidgets.QAction('None', self)
		regressionNoneAction.setStatusTip('Delete regression result')
		regressionNoneAction.triggered.connect(self.unsetRegressor)

		regressionMenu = menubar.addMenu('&Regression')
		regressionMenu.addAction(regressionLinRegAction)
		regressionMenu.addAction(regressionSVRAction)
		regressionMenu.addAction(regressionRegressionTreeAction)
		regressionMenu.addAction(regressionRegressionForestAction)
		regressionMenu.addSeparator()
		regressionMenu.addAction(regressionParametersAction)
		regressionMenu.addAction(regressionNoneAction)


		densityEstimationHistogramAction = QtWidgets.QAction('Histogram...', self)
		densityEstimationHistogramAction.setStatusTip('Histogram estimation')
		densityEstimationHistogramAction.triggered.connect(lambda: self.densityEstimationWithParameters(DensityEstimation.Histogram))

		densityEstimationSphereAction = QtWidgets.QAction('Sphere Density Estimation...', self)
		densityEstimationSphereAction.setStatusTip('Sphere Density Estimation')
		densityEstimationSphereAction.triggered.connect(lambda: self.densityEstimationWithParameters(DensityEstimation.SphereDensityEstimation))

		densityEstimationKernelAction = QtWidgets.QAction('Kernel Density Estimation...', self)
		densityEstimationKernelAction.setStatusTip('Kernel Density Estimation')
		densityEstimationKernelAction.triggered.connect(lambda: self.densityEstimationWithParameters(DensityEstimation.KernelDensityEstimation))

		densityEstimationParametersAction = QtWidgets.QAction('Parameters...', self)
		densityEstimationParametersAction.setStatusTip('Edit the parameters of the density estimation algorithms')
		densityEstimationParametersAction.triggered.connect(self.editDensityEstimationParameters)

		densityEstimationNoneAction = QtWidgets.QAction('None', self)
		densityEstimationNoneAction.setStatusTip('Delete density estimation result')
		densityEstimationNoneAction.triggered.connect(self.unsetDensityEstimation)

		densityEstimationMenu = menubar.addMenu('Density &Estimation')
		densityEstimationMenu.addAction(densityEstimationHistogramAction)
		densityEstimationMenu.addAction(densityEstimationSphereAction)
		densityEstimationMenu.addAction(densityEstimationKernelAction)
		densityEstimationMenu.addSeparator()
		densityEstimationMenu.addAction(densityEstimationParametersAction)
		densityEstimationMenu.addAction(densityEstimationNoneAction)

		aboutAction = QtWidgets.QAction('About...', self)
		aboutAction.setStatusTip('About this software')
		aboutAction.triggered.connect(self.aboutDialog.exec_)

		licenseAction = QtWidgets.QAction('License...', self)
		licenseAction.setStatusTip('GNU General Public License')
		licenseAction.triggered.connect(self.licenseDialog.showLicense)

		infoAction = QtWidgets.QAction('Info...', self)
		infoAction.setStatusTip('Information about the Python distribution')
		infoAction.triggered.connect(self.infoDialog.exec_)

		helpMenu = menubar.addMenu('&Help')
		helpMenu.addAction(aboutAction)
		helpMenu.addAction(licenseAction)
		helpMenu.addAction(infoAction)

#		exitAction = QtGui.QAction(QtGui.QIcon('./img/exit.png'), 'Exit', self)
#		exitAction.setShortcut('Ctrl+Q')
#		exitAction.triggered.connect(QtGui.qApp.quit)

#		coordinateSystemAction = QtGui.QAction(QtGui.QIcon('./img/coord.png'), 'Move coordinate system', self)
#		coordinateSystemAction.triggered.connect(self.onMoveCoordinateSystem)

#		gaussCreateAction = QtGui.QAction(QtGui.QIcon('./img/create_gauss.png'), 'Create Gaussians', self)
#		gaussCreateAction.triggered.connect(self.onCreateGaussians)

#		gaussModifyAction = QtGui.QAction(QtGui.QIcon('./img/modify_gauss.png'), 'Modify Gaussians', self)
#		gaussModifyAction.triggered.connect(self.onModifyGaussians)

		self.moveCoordinateSystemButton = QtWidgets.QToolButton()
		self.moveCoordinateSystemButton.setIcon(QtGui.QIcon(resource_path('./img/coord.png')))
		self.moveCoordinateSystemButton.setStatusTip('Move the coordinate system by dragging the mouse or zoom in or out using the mouse scroll wheel')
		self.moveCoordinateSystemButton.setCheckable(True)
		self.moveCoordinateSystemButton.setChecked(True)
		self.moveCoordinateSystemButton.clicked.connect(self.onMoveCoordinateSystem)

		self.createGaussButton = QtWidgets.QToolButton()
		self.createGaussButton.setIcon(QtGui.QIcon(resource_path('./img/create_gauss.png')))
		self.createGaussButton.setStatusTip('Create samples drawn from a new Gaussian pdf by spanning the bounding box of the covariance matrix')
		self.createGaussButton.setCheckable(True)
		self.createGaussButton.clicked.connect(self.onCreateGaussians)

		self.modifyGaussButton = QtWidgets.QToolButton()
		self.modifyGaussButton.setIcon(QtGui.QIcon(resource_path('./img/modify_gauss.png')))
		self.modifyGaussButton.setStatusTip('Modify existing Gaussian pdfs by left of right clicking on the center')
		self.modifyGaussButton.setCheckable(True)
		self.modifyGaussButton.clicked.connect(self.onModifyGaussians)

		self.createSamplesButton = QtWidgets.QToolButton()
		self.createSamplesButton.setIcon(QtGui.QIcon(resource_path('./img/samples.png')))
		self.createSamplesButton.setStatusTip('Create and modify individual samples by spanning a rectangle that contains one or more samples')
		self.createSamplesButton.setCheckable(True)
		self.createSamplesButton.clicked.connect(self.onCreateSamples)
		
		self.toolbar =	QtWidgets.QToolBar(self)
		self.toolbar.setIconSize(QtCore.QSize(48, 48))
		self.addToolBar(QtCore.Qt.RightToolBarArea, self.toolbar)
		# self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		# self.toolbar.addAction(coordinateSystemAction)
		# self.toolbar.addAction(gaussCreateAction)
		# self.toolbar.addAction(gaussModifyAction)
		self.toolbar.addWidget(self.moveCoordinateSystemButton)
		self.toolbar.addWidget(self.createGaussButton)
		self.toolbar.addWidget(self.modifyGaussButton)
		self.toolbar.addWidget(self.createSamplesButton)
		
		QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Z"), self, self.undo)
		QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self, self.redo)
		
		self.printLicenseMessage()
		

	def printLicenseMessage(self):
		print("The Python Classification Toolbox is free software:")
		print("you can redistribute it and/or modify it under the terms of the")
		print("GNU General Public License as published by the Free Software Foundation,")
		print("either version 3 of the License, or (at your option) any later version.\n")

		print("The Python Classification Toolbox is distributed in the hope that") 
		print("it will be useful, but WITHOUT ANY WARRANTY; without even the implied")
		print("warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.")  
		print("See the GNU General Public License for more details.\n")

		print("You should have received a copy of the GNU General Public License")
		print("along with the Python Classification Toolbox.")  
		print("If not, see <http://www.gnu.org/licenses/>.")

		
	def closeEvent(self, event):
		try:
			self.featurespace.saveDefaultFeatureSpace('.featurespace.pyct')
		except:
			print("could not save default feature space")
			
		event.accept()


	def undo(self):
		self.operationStack.undo()


	def redo(self):
		self.operationStack.redo()


	def newFeatureSpace(self):
		self.classifier = None
		self.regressor = None
		self.densityEstimator = None
		self.__featureSpaceHideSamplesAction.setChecked(False)
		self.featurespace.new()
		self.operationStack.clear()


	def openFeatureSpace(self):
		self.classifier = None
		self.regressor = None
		self.densityEstimator = None
		self.__featureSpaceHideSamplesAction.setChecked(False)
		self.featurespace.open()
		self.operationStack.clear()


	def saveFeatureSpace(self):
		self.featurespace.save()


	def saveAsFeatureSpace(self):
		self.featurespace.saveAs()


	def exportFeatureSpace(self):
		self.featurespace.exportFile()


	def exportFeatureSpaceAsImage(self):
		self.featurespace.exportImage()


	def importFeatureSpace(self):
		self.featurespace.importFile()


	def hideSamples(self):
		hide = self.__featureSpaceHideSamplesAction.isChecked()
		self.featurespace.hideSamples(hide)


	def onMoveCoordinateSystem(self):
		self.moveCoordinateSystemButton.setChecked(True)
		self.createGaussButton.setChecked(False)
		self.modifyGaussButton.setChecked(False)
		self.createSamplesButton.setChecked(False)
		self.createSamplesDockWidget.setHidden(True)
		self.featurespace.changeAction(self.featurespace.ACTION_COORDINATE_SYSTEM)
		self.statusbar.showMessage('')


	def onCreateGaussians(self):
		self.moveCoordinateSystemButton.setChecked(False)
		self.createGaussButton.setChecked(True)
		self.modifyGaussButton.setChecked(False)
		self.createSamplesButton.setChecked(False)
		self.createSamplesDockWidget.setHidden(True)
		self.featurespace.changeAction(self.featurespace.ACTION_CREATE_GAUSSIAN)


	def onModifyGaussians(self):
		self.moveCoordinateSystemButton.setChecked(False)
		self.createGaussButton.setChecked(False)
		self.modifyGaussButton.setChecked(True)
		self.createSamplesButton.setChecked(False)
		self.createSamplesDockWidget.setHidden(True)
		self.featurespace.changeAction(self.featurespace.ACTION_MODIFY_GAUSSIAN)
		self.statusbar.showMessage('')

	def onCreateSamples(self):
		self.moveCoordinateSystemButton.setChecked(False)
		self.createGaussButton.setChecked(False)
		self.modifyGaussButton.setChecked(False)
		self.createSamplesButton.setChecked(True)
		self.createSamplesDockWidget.setHidden(False)
		self.featurespace.changeAction(self.featurespace.ACTION_CREATE_SAMPLES)
		self.statusbar.showMessage('')


	def clusterWithParameters(self, method):
		self.clusteringParameters.setTab(method)
		result = self.clusteringParameters.exec_()
		if result == QtWidgets.QDialog.Accepted:
			self.classifier = None
			self.featurespace.setClassificationImage(None)
			self.regressor = None
			self.densityEstimator = None
			self.clusterer = Clustering(method, self.clusteringParameters, self.featurespace)
			try:
				self.clusterer.initialize()
			except AssertionError as e:
				QtWidgets.QMessageBox.warning(self, 'Error', str(e), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)		
			self.repaint()


	def editClusteringParameters(self):
		self.clusteringParameters.setTab(-1)
		self.clusteringParameters.exec_()


	def reduceDimensionalityWithParameters(self, method):
		self.dimRedParameters.setTab(method)
		result = self.dimRedParameters.exec_()
		if result == QtWidgets.QDialog.Accepted:
			self.classifier = None
			self.featurespace.setClassificationImage(None)
			self.regressor = None
			self.densityEstimator = None
			self.dimreduction = DimensionalityReduction(method, self.dimRedParameters, self.featurespace)
			self.dimreduction.initialize()
			self.repaint()


	def classify(self, classifier):
		self.regressor = None
		self.densityEstimator = None
		self.classifier = Classifier(classifier, self.classifierParameters, self.featurespace)
		try:
			self.classifier.initialize()
			self.runFeatureSpaceComputations()
			op = Operation(self, "dummy", None)
			self.operationStack.add(op)
		except Exception as e:
			QtWidgets.QMessageBox.warning(self, 'Error', str(e), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)		
			


	def classifyWithParameters(self, classifier):
		self.regressor = None
		self.densityEstimator = None
		self.classifierParameters.setTab(classifier)
		result = self.classifierParameters.exec_()
		if result == QtWidgets.QDialog.Accepted:
			self.classifier = Classifier(classifier, self.classifierParameters, self.featurespace)
			try:
				self.classifier.initialize()
				self.runFeatureSpaceComputations()
				op = Operation(self, "dummy", None)
				self.operationStack.add(op)
			except AssertionError as e:
				QtWidgets.QMessageBox.warning(self, 'Error', str(e), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)


	def unsetClassifier(self):
		self.classifier = None
		self.featurespace.setClassificationImage(None)
		op = Operation(self, "dummy", None)
		self.operationStack.add(op)
		self.repaint()


	def runFeatureSpaceComputations(self, initialize = False):
		changes = False
		if self.classifier:
			self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			self.statusbar.showMessage('')

			img = None
			if initialize:
				try:
					self.classifier = self.classifier.copy()
					self.classifier.initialize()
					img = self.classifier.runFeatureSpaceComputations()
				except AssertionError as e:
					QtWidgets.QMessageBox.warning(self, 'Error', str(e), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
			else:
				img = self.classifier.runFeatureSpaceComputations()

			self.featurespace.setClassificationImage(img)
			self.featurespace.repaint()
			self.statusbar.showMessage('classification done')
			self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			changes = True
			
		elif self.regressor:
			self.statusbar.showMessage('')

			if initialize:
				self.regressor.initialize()

			self.featurespace.repaint()
			
		elif self.densityEstimator:
			self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			self.statusbar.showMessage('')

			img = None
			if initialize:
				try:
					self.densityEstimator.initialize()
					img = self.densityEstimator.runFeatureSpaceComputations()
				except AssertionError as e:
					QtWidgets.QMessageBox.warning(self, 'Error', str(e), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
			else:
				img = self.densityEstimator.runFeatureSpaceComputations()

			self.featurespace.setClassificationImage(img)
			self.featurespace.repaint()
			self.statusbar.showMessage('density estimation done')
			self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			changes = True			

		return changes


	def editClassificationParameters(self):
		self.classifierParameters.setTab(-1)
		self.classifierParameters.exec_()


	def regression(self, regressor):
		self.classifier = None
		self.densityEstimator = None
		self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		self.statusbar.showMessage('')
		self.regressor = Regression(regressor, self.regressionParameters, self.featurespace)
		self.regressor.initialize()
		self.featurespace.setClassificationImage(None)
		op = Operation(self, "dummy", None)
		self.operationStack.add(op)
		self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
		self.statusbar.showMessage('regression done')
		self.repaint()


	def regressionWithParameters(self, regressor):
		self.classifier = None
		self.densityEstimator = None
		self.regressionParameters.setTab(regressor)
		result = self.regressionParameters.exec_()
		if result == QtWidgets.QDialog.Accepted:
			self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			self.statusbar.showMessage('')
			self.regressor = Regression(regressor, self.regressionParameters, self.featurespace)
			try:
				self.regressor.initialize()
				self.featurespace.setClassificationImage(None)
				op = Operation(self, "dummy", None)
				self.operationStack.add(op)
			except AssertionError as e:
				QtWidgets.QMessageBox.warning(self, 'Error', str(e), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
			
			self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			self.statusbar.showMessage('regression done')
			self.repaint()


	def paintRegressor(self, qp):
		if self.regressor:
			self.regressor.paint(qp)


	def unsetRegressor(self):
		self.regressor = None
		op = Operation(self, "dummy", None)
		self.operationStack.add(op)
		self.repaint()


	def editRegressionParameters(self):
		self.regressionParameters.setTab(-1)
		self.regressionParameters.exec_()


	def densityEstimationWithParameters(self, estimator):
		self.classifier = None
		self.regressor = None
		self.densityEstimationParameters.setTab(estimator)
		result = self.densityEstimationParameters.exec_()
		if result == QtWidgets.QDialog.Accepted:
			self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			self.statusbar.showMessage('')
			self.densityEstimator = DensityEstimation(estimator, self.densityEstimationParameters, self.featurespace, self.probabilityDensityViewer)
			try:
				self.densityEstimator.initialize()
				self.runFeatureSpaceComputations()
				op = Operation(self, "dummy", None)
				self.operationStack.add(op)
			except AssertionError as e:
				QtWidgets.QMessageBox.warning(self, 'Error', str(e), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
			self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			self.statusbar.showMessage('density estimation done')
			self.repaint()
				

	def editDensityEstimationParameters(self):
		self.densityEstimationParameters.setTab(-1)
		self.densityEstimationParameters.exec_()


	def unsetDensityEstimation(self):
		self.densityEstimator = None
		self.featurespace.setClassificationImage(None)
		op = Operation(self, "dummy", None)
		self.operationStack.add(op)
		self.repaint()


	def getToolboxImage(self):
		img = self.featurespace.getClassificationImage()
		# print("getToolboxImage: ", img)
		return (self.classifier, self.regressor, self.densityEstimator, img)


	def setToolboxImage(self, image):
		(self.classifier, self.regressor, self.densityEstimator, classificationImage) = image
		self.featurespace.setClassificationImage(classificationImage)
		self.featurespace.repaint()



def main():
	app = QtWidgets.QApplication(sys.argv)
	win = PyClassificationToolbox()
	win.setWindowTitle("Python Classification Toolbox")
	win.show()	
	sys.exit(app.exec_())


if __name__=="__main__":
	main()
