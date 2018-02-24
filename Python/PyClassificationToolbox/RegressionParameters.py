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


class RegressionParameters(QtWidgets.QDialog):
	
	def __init__(self, parent):
		super(RegressionParameters, self).__init__(parent)
		
		self.__parent = parent
		self.__currentTab = 0
		
		# Linear Regression tab
		linRegLossFunctionLabel = QtWidgets.QLabel('Loss function')
		linRegLossFunctionParameterLabel = QtWidgets.QLabel('Parameter of the loss function')
		self.linRegLossFunctionCombobox = QtWidgets.QComboBox()
		self.linRegLossFunctionCombobox.addItem('l2 norm')
		self.linRegLossFunctionCombobox.addItem('Huber loss')
		self.linRegLossFunctionCombobox.currentIndexChanged.connect(self.onLinRegLossFunctionChanged)
		self.linRegLossFunctionParameterEdit = QtWidgets.QLineEdit('0.001')
		self.linRegLossFunctionParameterEdit.setEnabled(False)
		
		linRegGrid = QtWidgets.QGridLayout();
		linRegGrid.setSpacing(10)
		linRegGrid.addWidget(linRegLossFunctionLabel, 0, 0)
		linRegGrid.addWidget(self.linRegLossFunctionCombobox, 0, 1)
		linRegGrid.addWidget(linRegLossFunctionParameterLabel, 1, 0)
		linRegGrid.addWidget(self.linRegLossFunctionParameterEdit, 1, 1)
		
		linRegFrame = QtWidgets.QGroupBox()
		linRegFrame.setTitle('Linear Regression')		
		linRegFrame.setLayout(linRegGrid)
		
		linRegLayout = QtWidgets.QVBoxLayout()
		linRegLayout.addWidget(linRegFrame)
		linRegLayout.addStretch(1)
		
		self.linRegTab = QtWidgets.QWidget()
		self.linRegTab.setLayout(linRegLayout)
		
		# SVR properties
		SVRAlgorithmLabel = QtWidgets.QLabel('Algorithm')
		SVRKernelLabel = QtWidgets.QLabel('Kernel')
		SVRCLabel = QtWidgets.QLabel('C')
		SVREpsilonLabel = QtWidgets.QLabel('Epsilon')
		SVRGammaLabel = QtWidgets.QLabel('Gamma')
		SVRCoef0Label = QtWidgets.QLabel('Coef0')
		SVRDegreeLabel = QtWidgets.QLabel('Degree')
		self.SVRAlgorithmCombobox = QtWidgets.QComboBox()
		self.SVRAlgorithmCombobox.addItem('SVR (scikit-learn)')
		
		self.SVRKernelCombobox = QtWidgets.QComboBox()
		self.SVRKernelCombobox.addItem('linear')
		self.SVRKernelCombobox.addItem('polynomial')
		self.SVRKernelCombobox.addItem('radial basis functions')
		self.SVRKernelCombobox.addItem('sigmoid')
		self.SVRKernelCombobox.currentIndexChanged.connect(self.onSVRKernelChanged)
		self.SVRCEdit = QtWidgets.QLineEdit('1.0')
		self.SVRCEdit.setToolTip('Penalty parameter of the error term')
		self.SVREpsilonEdit = QtWidgets.QLineEdit('0.1')
		self.SVREpsilonEdit.setToolTip('Specifies the epsilon-tube within which no penalty is associated in the training loss function with points predicted within a distance epsilon from the actual value.')
		self.SVRGammaEdit = QtWidgets.QLineEdit('0.5')
		self.SVRGammaEdit.setToolTip('Kernel coefficient')
		self.SVRCoef0Edit = QtWidgets.QLineEdit('0.0')
		self.SVRCoef0Edit.setToolTip('Independent term in kernel function')
		self.SVRDegreeEdit = QtWidgets.QLineEdit('3')
		self.SVRDegreeEdit.setToolTip('Degree of the polynomial kernel function')
		self.onSVRKernelChanged(0)
		
		SVRGrid = QtWidgets.QGridLayout();
		SVRGrid.setSpacing(10)
		SVRGrid.addWidget(SVRAlgorithmLabel, 0, 0)
		SVRGrid.addWidget(self.SVRAlgorithmCombobox, 0, 1)
		SVRGrid.addWidget(SVRKernelLabel, 1, 0)
		SVRGrid.addWidget(self.SVRKernelCombobox, 1, 1)
		SVRGrid.addWidget(SVRCLabel, 2, 0)
		SVRGrid.addWidget(self.SVRCEdit, 2, 1)
		SVRGrid.addWidget(SVREpsilonLabel, 3, 0)
		SVRGrid.addWidget(self.SVREpsilonEdit, 3, 1)
		SVRGrid.addWidget(SVRGammaLabel, 4, 0)
		SVRGrid.addWidget(self.SVRGammaEdit, 4, 1)
		SVRGrid.addWidget(SVRCoef0Label, 5, 0)
		SVRGrid.addWidget(self.SVRCoef0Edit, 5, 1)
		SVRGrid.addWidget(SVRDegreeLabel, 6, 0)
		SVRGrid.addWidget(self.SVRDegreeEdit, 6, 1)
		
		SVRFrame = QtWidgets.QGroupBox()
		SVRFrame.setTitle('Support Vector Regression')
		SVRFrame.setLayout(SVRGrid)
		
		SVRLayout = QtWidgets.QVBoxLayout()
		SVRLayout.addWidget(SVRFrame)
		SVRLayout.addStretch(1)
		
		self.SVRTab = QtWidgets.QWidget()
		self.SVRTab.setLayout(SVRLayout)
		
		
		# Regression Tree
		RegressionTreeAlgorithmLabel = QtWidgets.QLabel('Algorithm')
		RegressionTreeCriterionLabel = QtWidgets.QLabel('Quality criterion')
		RegressionTreeSplitterLabel = QtWidgets.QLabel('Splitting strategy')
		RegressionTreeMaxDepthLabel = QtWidgets.QLabel('Maximum tree depth')
		RegressionTreeMinSamplesSplitLabel = QtWidgets.QLabel('Minimum samples required to split internal node')
		RegressionTreeMinSamplesLeafLabel = QtWidgets.QLabel('Minimum samples required at leaf node')
		RegressionTreeMinWeightedFractionLeafLabel = QtWidgets.QLabel('Minimum weighted fraction at leaf node')
		RegressionTreeMaxLeafNodesLabel = QtWidgets.QLabel('Maximum leaf nodes')
		RegressionTreeNumTrialsPerSplitLabel = QtWidgets.QLabel('Number of trials to split a node')
		self.RegressionTreeAlgorithmCombobox = QtWidgets.QComboBox()
		self.RegressionTreeAlgorithmCombobox.addItem('RegressionTreeRegressor (scikit-learn)')
		self.RegressionTreeAlgorithmCombobox.addItem('Regression Tree')
		self.RegressionTreeAlgorithmCombobox.currentIndexChanged.connect(self.onRegressionTreeAlgorithmChanged)
		self.RegressionTreeCriterionCombobox = QtWidgets.QComboBox()
		self.RegressionTreeCriterionCombobox.addItem('mean squared error (mse)')
		self.RegressionTreeCriterionCombobox.setEnabled(False)
		self.RegressionTreeSplitterCombobox = QtWidgets.QComboBox()
		self.RegressionTreeSplitterCombobox.addItem('best')
		self.RegressionTreeSplitterCombobox.addItem('random')
		self.RegressionTreeMaxDepthCombobox = QtWidgets.QComboBox()
		self.RegressionTreeMaxDepthCombobox.addItem('None')
		self.RegressionTreeMaxDepthCombobox.addItems([str(x) for x in range(1, 10)])
		self.RegressionTreeMaxDepthCombobox.setEditable(True)
		self.RegressionTreeMaxDepthCombobox.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)		
		self.RegressionTreeMinSamplesSplitEdit = QtWidgets.QLineEdit('2')
		self.RegressionTreeMinSamplesLeafEdit = QtWidgets.QLineEdit('1')
		self.RegressionTreeMinWeightedFractionLeafEdit = QtWidgets.QLineEdit('0.')
		self.RegressionTreeMaxLeafNodesCombobox = QtWidgets.QComboBox()
		self.RegressionTreeMaxLeafNodesCombobox.addItems(['None', '10', '20', '30', '40', '50'])
		self.RegressionTreeMaxLeafNodesCombobox.setEditable(True)
		self.RegressionTreeMaxLeafNodesCombobox.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
		self.RegressionTreeMaxLeafNodesCombobox.currentIndexChanged.connect(self.onRegressionTreeMaxLeafNodesChanged)
		self.RegressionTreeNumTrialsPerSplitEdit = QtWidgets.QLineEdit('10')
		self.RegressionTreeNumTrialsPerSplitEdit.setEnabled(False)
		
		RegressionTreeGrid = QtWidgets.QGridLayout();
		RegressionTreeGrid.setSpacing(10)
		RegressionTreeGrid.addWidget(RegressionTreeAlgorithmLabel, 0, 0)
		RegressionTreeGrid.addWidget(self.RegressionTreeAlgorithmCombobox, 0, 1)
		RegressionTreeGrid.addWidget(RegressionTreeCriterionLabel, 1, 0)
		RegressionTreeGrid.addWidget(self.RegressionTreeCriterionCombobox, 1, 1)
		RegressionTreeGrid.addWidget(RegressionTreeSplitterLabel, 2, 0)
		RegressionTreeGrid.addWidget(self.RegressionTreeSplitterCombobox, 2, 1)
		RegressionTreeGrid.addWidget(RegressionTreeMaxDepthLabel, 3, 0)
		RegressionTreeGrid.addWidget(self.RegressionTreeMaxDepthCombobox, 3, 1)
		RegressionTreeGrid.addWidget(RegressionTreeMinSamplesSplitLabel, 4, 0)
		RegressionTreeGrid.addWidget(self.RegressionTreeMinSamplesSplitEdit, 4, 1)
		RegressionTreeGrid.addWidget(RegressionTreeMinSamplesLeafLabel, 5, 0)
		RegressionTreeGrid.addWidget(self.RegressionTreeMinSamplesLeafEdit, 5, 1)
		RegressionTreeGrid.addWidget(RegressionTreeMinWeightedFractionLeafLabel, 6, 0)
		RegressionTreeGrid.addWidget(self.RegressionTreeMinWeightedFractionLeafEdit, 6, 1)
		RegressionTreeGrid.addWidget(RegressionTreeMaxLeafNodesLabel, 7, 0)
		RegressionTreeGrid.addWidget(self.RegressionTreeMaxLeafNodesCombobox, 7, 1)
		RegressionTreeGrid.addWidget(RegressionTreeNumTrialsPerSplitLabel, 8, 0)
		RegressionTreeGrid.addWidget(self.RegressionTreeNumTrialsPerSplitEdit, 8, 1)
		
		RegressionTreeFrame = QtWidgets.QGroupBox()
		RegressionTreeFrame.setTitle('Regression Trees')		
		RegressionTreeFrame.setLayout(RegressionTreeGrid)
		
		RegressionTreeLayout = QtWidgets.QVBoxLayout()
		RegressionTreeLayout.addWidget(RegressionTreeFrame)
		RegressionTreeLayout.addStretch(1)
		
		self.RegressionTreeTab = QtWidgets.QWidget()
		self.RegressionTreeTab.setLayout(RegressionTreeLayout)


		# Regression Forests
		RegressionForestAlgorithmLabel = QtWidgets.QLabel('Algorithm')
		RegressionForestNumTreesLabel = QtWidgets.QLabel('Number of trees')
		RegressionForestCriterionLabel = QtWidgets.QLabel('Quality criterion')
		RegressionForestMaxDepthLabel = QtWidgets.QLabel('Maximum tree depth')
		RegressionForestMinSamplesSplitLabel = QtWidgets.QLabel('Minimum samples required to split internal node')
		RegressionForestMinSamplesLeafLabel = QtWidgets.QLabel('Minimum samples required at leaf node')
		RegressionForestMinWeightedFractionLeafLabel = QtWidgets.QLabel('Minimum weighted fraction at leaf node')
		RegressionForestMaxLeafNodesLabel = QtWidgets.QLabel('Maximum leaf nodes')
		RegressionForestNumTrialsPerSplitLabel = QtWidgets.QLabel('Number of trials to split a node')
		self.RegressionForestAlgorithmCombobox = QtWidgets.QComboBox()
		self.RegressionForestAlgorithmCombobox.addItem('RegressionForestRegressor (scikit-learn)')
		self.RegressionForestAlgorithmCombobox.addItem('Regression Forest')
		self.RegressionForestAlgorithmCombobox.currentIndexChanged.connect(self.onRegressionForestAlgorithmChanged)
		self.RegressionForestNumTreesEdit = QtWidgets.QLineEdit('10')
		self.RegressionForestCriterionCombobox = QtWidgets.QComboBox()
		self.RegressionForestCriterionCombobox.addItem('mean squared error (mse)')
		self.RegressionForestCriterionCombobox.setEnabled(False)
		self.RegressionForestMaxDepthCombobox = QtWidgets.QComboBox()
		self.RegressionForestMaxDepthCombobox.addItem('None')
		self.RegressionForestMaxDepthCombobox.addItems([str(x) for x in range(1, 10)])
		self.RegressionForestMaxDepthCombobox.setEditable(True)
		self.RegressionForestMaxDepthCombobox.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)		
		self.RegressionForestMinSamplesSplitEdit = QtWidgets.QLineEdit('2')
		self.RegressionForestMinSamplesLeafEdit = QtWidgets.QLineEdit('1')
		self.RegressionForestMinWeightedFractionLeafEdit = QtWidgets.QLineEdit('0.')
		self.RegressionForestMaxLeafNodesCombobox = QtWidgets.QComboBox()
		self.RegressionForestMaxLeafNodesCombobox.addItems(['None', '10', '20', '30', '40', '50'])
		self.RegressionForestMaxLeafNodesCombobox.setEditable(True)
		self.RegressionForestMaxLeafNodesCombobox.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
		self.RegressionForestMaxLeafNodesCombobox.currentIndexChanged.connect(self.onRegressionForestMaxLeafNodesChanged)
		self.RegressionForestNumTrialsPerSplitEdit = QtWidgets.QLineEdit('10')
		self.RegressionForestNumTrialsPerSplitEdit.setEnabled(False)
		
		RegressionForestGrid = QtWidgets.QGridLayout();
		RegressionForestGrid.setSpacing(10)
		RegressionForestGrid.addWidget(RegressionForestAlgorithmLabel, 0, 0)
		RegressionForestGrid.addWidget(self.RegressionForestAlgorithmCombobox, 0, 1)
		RegressionForestGrid.addWidget(RegressionForestNumTreesLabel, 1, 0)
		RegressionForestGrid.addWidget(self.RegressionForestNumTreesEdit, 1, 1)
		RegressionForestGrid.addWidget(RegressionForestCriterionLabel, 2, 0)
		RegressionForestGrid.addWidget(self.RegressionForestCriterionCombobox, 2, 1)
		RegressionForestGrid.addWidget(RegressionForestMaxDepthLabel, 3, 0)
		RegressionForestGrid.addWidget(self.RegressionForestMaxDepthCombobox, 3, 1)
		RegressionForestGrid.addWidget(RegressionForestMinSamplesSplitLabel, 4, 0)
		RegressionForestGrid.addWidget(self.RegressionForestMinSamplesSplitEdit, 4, 1)
		RegressionForestGrid.addWidget(RegressionForestMinSamplesLeafLabel, 5, 0)
		RegressionForestGrid.addWidget(self.RegressionForestMinSamplesLeafEdit, 5, 1)
		RegressionForestGrid.addWidget(RegressionForestMinWeightedFractionLeafLabel, 6, 0)
		RegressionForestGrid.addWidget(self.RegressionForestMinWeightedFractionLeafEdit, 6, 1)
		RegressionForestGrid.addWidget(RegressionForestMaxLeafNodesLabel, 7, 0)
		RegressionForestGrid.addWidget(self.RegressionForestMaxLeafNodesCombobox, 7, 1)
		RegressionForestGrid.addWidget(RegressionForestNumTrialsPerSplitLabel, 8, 0)
		RegressionForestGrid.addWidget(self.RegressionForestNumTrialsPerSplitEdit, 8, 1)
		
		RegressionForestFrame = QtWidgets.QGroupBox()
		RegressionForestFrame.setTitle('Regression Forests')		
		RegressionForestFrame.setLayout(RegressionForestGrid)
		
		RegressionForestLayout = QtWidgets.QVBoxLayout()
		RegressionForestLayout.addWidget(RegressionForestFrame)
		RegressionForestLayout.addStretch(1)
		
		self.RegressionForestTab = QtWidgets.QWidget()
		self.RegressionForestTab.setLayout(RegressionForestLayout)


		# Create notebook tabs		
		self.notebook = QtWidgets.QTabWidget()
		self.notebook.addTab(self.linRegTab, "LinReg")
		self.notebook.addTab(self.SVRTab, "SVR")
		self.notebook.addTab(self.RegressionTreeTab, "Tree")
		self.notebook.addTab(self.RegressionForestTab, "Forest")
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
		
		self.setWindowTitle('Regression parameters')
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
		if tab == 0: # Linear Regression parameters
			if not self.testParameter(self.getLinRegLossFunctionParam, 'The parameter of the loss function has to be a floating point number!'):
				return False
			
			a = self.getLinRegLossFunctionParam()
			if a <= 0: 
				self.errorMsg('The parameter of the loss function has to be positive!')
				return False

		elif tab == 1: # SVR parameters
			if not self.testParameter(self.getSVRC, 'The penalty parameter C has to be a floating point number!'):
				return False
		
			if not self.testParameter(self.getSVREpsilon, 'The Epsilon parameter has to be a floating point number!'):
				return False
		
			if not self.testParameter(self.getSVRGamma, 'The kernel parameter Gamma has to be a floating point number!'):
				return False

			if not self.testParameter(self.getSVRCoef0, 'The independent term in the kernel function Coef0 has to be a floating point number!'):
				return False
		
			if not self.testParameter(self.getSVRDegree, 'The degree of the polynomial kernel function has to be an integer number!'):
				return False
		
			degree = self.getSVRDegree()
			if degree < 1:
				self.errorMsg('The degree of the polynomial kernel has to be at least 1!')
				return False
			
			C = self.getSVRC()
			if C <= 0:
				self.errorMsg('The penalty parameter C has to be positive!')
				return False
			
			eps = self.getSVREpsilon()
			if eps <= 0:
				self.errorMsg('The Epsilon parameter has to be positive!')
				return False
			
			gamma = self.getSVRGamma()
			if gamma <= 0:
				self.errorMsg('The kernel parameter Gamma has to be positive!')
				return False

		elif tab == 2: # Regression Tree parameters
			if not self.testParameter(self.getRegressionTreeMaxDepth, 'The maximum depth of the tree has to be None or an integer number!'):
				return False

			if not self.testParameter(self.getRegressionTreeMaxLeafNodes, 'The maximum number of leaf nodes has to be None or an integer number!'):
				return False

			if not self.testParameter(self.getRegressionTreeMinSamplesSplit, 'The minimum number of samples required to split an internal node has to be an integer number!'):
				return False

			if not self.testParameter(self.getRegressionTreeMinSamplesLeaf, 'The minimum number of samples required to be at a leaf node has to be an integer number!'):
				return False

			if not self.testParameter(self.getRegressionTreeMinWeightedFractionLeaf, 'The minimum weighted fraction of the input samples required to be at a leaf node has to be a real number!'):
				return False

			if not self.testParameter(self.getRegressionTreeNumTrialsPerSplit, 'The number of trials to split a node has to be an integer number!'):
				return False

			depth = self.getRegressionTreeMaxDepth()
			if not(depth == None) and (depth < 1):
				self.errorMsg('The maximum depth of the tree has to be at least 1!')
				return False

			leafNodes = self.getRegressionTreeMaxLeafNodes()
			if not(leafNodes == None) and (leafNodes < 2):
				self.errorMsg('The maximum number of leaf nodes has to be at least 2!')
				return False

			split = self.getRegressionTreeMinSamplesSplit()
			if split < 2:
				self.errorMsg('The minimum number of samples required to split an internal node has to be at least 2!')
				return False

			leaf = self.getRegressionTreeMinSamplesLeaf()
			if leaf < 1:
				self.errorMsg('The minimum number of samples required to be at a leaf node has to be at least 1!')
				return False

			fraction = self.getRegressionTreeMinWeightedFractionLeaf()
			if (fraction < 0) or (fraction > 0.5):
				self.errorMsg('The minimum weighted fraction of the input samples required to be at a leaf node has to be between 0.0 and 0.5!')
				return False

			trials = self.getRegressionTreeNumTrialsPerSplit()
			if trials < 1:
				self.errorMsg('The number of trials to split a node has to be at least 1!')
				return False

		elif tab == 3: # Regression Forest parameters
			if not self.testParameter(self.getRegressionForestNumTrees, 'The number of trees in the forest has to be an integer number!'):
				return False

			if not self.testParameter(self.getRegressionForestMaxDepth, 'The maximum depth of the tree has to be None or an integer number!'):
				return False

			if not self.testParameter(self.getRegressionForestMaxLeafNodes, 'The maximum number of leaf nodes has to be None or an integer number!'):
				return False

			if not self.testParameter(self.getRegressionForestMinSamplesSplit, 'The minimum number of samples required to split an internal node has to be an integer number!'):
				return False

			if not self.testParameter(self.getRegressionForestMinSamplesLeaf, 'The minimum number of samples required to be at a leaf node has to be an integer number!'):
				return False

			if not self.testParameter(self.getRegressionForestMinWeightedFractionLeaf, 'The minimum weighted fraction of the input samples required to be at a leaf node has to be a real number!'):
				return False

			if not self.testParameter(self.getRegressionForestNumTrialsPerSplit, 'The number of trials to split a node has to be an integer number!'):
				return False

			trees = self.getRegressionForestNumTrees()
			if trees < 1:
				self.errorMsg('The number of trees in the forest has to be at least 1!')
				return False			

			depth = self.getRegressionForestMaxDepth()
			if not(depth == None) and (depth < 1):
				self.errorMsg('The maximum depth of the tree has to be at least 1!')
				return False

			leafNodes = self.getRegressionForestMaxLeafNodes()
			if not(leafNodes == None) and (leafNodes < 2):
				self.errorMsg('The maximum number of leaf nodes has to be at least 2!')
				return False

			split = self.getRegressionForestMinSamplesSplit()
			if split < 2:
				self.errorMsg('The minimum number of samples required to split an internal node has to be at least 2!')
				return False

			leaf = self.getRegressionForestMinSamplesLeaf()
			if leaf < 1:
				self.errorMsg('The minimum number of samples required to be at a leaf node has to be at least 1!')
				return False

			fraction = self.getRegressionForestMinWeightedFractionLeaf()
			if (fraction < 0) or (fraction > 0.5):
				self.errorMsg('The minimum weighted fraction of the input samples required to be at a leaf node has to be between 0.0 and 0.5!')
				return False

			trials = self.getRegressionForestNumTrialsPerSplit()
			if trials < 1:
				self.errorMsg('The number of trials to split a node has to be at least 1!')
				return False

		return True


	def onAccept(self):
		if not self.checkParameters(self.notebook.currentIndex()):
			return		
		super(RegressionParameters, self).accept()


	def onReject(self):
		self.restoreParameters()
		super(RegressionParameters, self).reject()


	def showEvent(self, event):
		self.__parameters = self.getParameters()


	def getParameters(self):
		params = {}
		params['LinReg_loss_function'] = self.linRegLossFunctionCombobox.currentIndex()
		params['LinReg_loss_function_param'] = self.linRegLossFunctionParameterEdit.text()
		params['svr_algo'] = self.SVRAlgorithmCombobox.currentIndex()
		params['svr_kernel'] = self.SVRKernelCombobox.currentIndex()
		params['svr_c'] = self.SVRCEdit.text()
		params['svr_epsilon'] = self.SVREpsilonEdit.text()
		params['svr_gamma'] = self.SVRGammaEdit.text()
		params['svr_coef0'] = self.SVRCoef0Edit.text()
		params['svr_degree'] = self.SVRDegreeEdit.text()
		params['regression_tree_algo'] = self.RegressionTreeAlgorithmCombobox.currentIndex()
		params['regression_tree_criterion'] = self.RegressionTreeCriterionCombobox.currentIndex()
		params['regression_tree_splitter'] = self.RegressionTreeSplitterCombobox.currentIndex()
		params['regression_tree_max_depth'] = self.RegressionTreeMaxDepthCombobox.currentIndex()
		params['regression_tree_min_samples_split'] = self.RegressionTreeMinSamplesSplitEdit.text()
		params['regression_tree_min_samples_leaf'] = self.RegressionTreeMinSamplesLeafEdit.text()
		params['regression_tree_min_weighted_fraction_leaf'] = self.RegressionTreeMinWeightedFractionLeafEdit.text()
		params['regression_tree_max_leaf_nodes'] = self.RegressionTreeMaxDepthCombobox.currentIndex()
		params['regression_tree_num_trials_per_split'] = self.RegressionTreeNumTrialsPerSplitEdit.text()
		params['regression_forest_algo'] = self.RegressionForestAlgorithmCombobox.currentIndex()
		params['regression_forest_numtrees'] = self.RegressionForestNumTreesEdit.text()
		params['regression_forest_criterion'] = self.RegressionForestCriterionCombobox.currentIndex()
		params['regression_forest_max_depth'] = self.RegressionForestMaxDepthCombobox.currentIndex()
		params['regression_forest_min_samples_split'] = self.RegressionForestMinSamplesSplitEdit.text()
		params['regression_forest_min_samples_leaf'] = self.RegressionForestMinSamplesLeafEdit.text()
		params['regression_forest_min_weighted_fraction_leaf'] = self.RegressionForestMinWeightedFractionLeafEdit.text()
		params['regression_forest_max_leaf_nodes'] = self.RegressionForestMaxDepthCombobox.currentIndex()
		params['regression_forest_num_trials_per_split'] = self.RegressionForestNumTrialsPerSplitEdit.text()
		return params

		
	def restoreParameters(self):
		params = self.__parameters
		self.linRegLossFunctionCombobox.setCurrentIndex(params['LinReg_loss_function'])
		self.linRegLossFunctionParameterEdit.setText(params['LinReg_loss_function_param'])
		self.SVRAlgorithmCombobox.setCurrentIndex(params['svr_algo'])
		self.SVRKernelCombobox.setCurrentIndex(params['svr_kernel'])
		self.SVRCEdit.setText(params['svr_c'])
		self.SVREpsilonEdit.setText(params['svr_epsilon'])
		self.SVRGammaEdit.setText(params['svr_gamma'])
		self.SVRCoef0Edit.setText(params['svr_coef0'])
		self.SVRDegreeEdit.setText(params['svr_degree'])
		self.RegressionTreeAlgorithmCombobox.setCurrentIndex(params['regression_tree_algo'])
		self.RegressionTreeCriterionCombobox.setCurrentIndex(params['regression_tree_criterion'])
		self.RegressionTreeSplitterCombobox.setCurrentIndex(params['regression_tree_splitter'])
		self.RegressionTreeMaxDepthCombobox.setCurrentIndex(params['regression_tree_max_depth'])
		self.RegressionTreeMinSamplesSplitEdit.setText(params['regression_tree_min_samples_split'])
		self.RegressionTreeMinSamplesLeafEdit.setText(params['regression_tree_min_samples_leaf'])
		self.RegressionTreeMinWeightedFractionLeafEdit.setText(params['regression_tree_min_weighted_fraction_leaf'])
		self.RegressionTreeMaxDepthCombobox.setCurrentIndex(params['regression_tree_max_leaf_nodes'])
		self.RegressionTreeNumTrialsPerSplitEdit.setText(params['regression_tree_num_trials_per_split'])
		self.RegressionForestAlgorithmCombobox.setCurrentIndex(params['regression_forest_algo'])
		self.RegressionForestNumTreesEdit.setText(params['regression_forest_numtrees'])
		self.RegressionForestCriterionCombobox.setCurrentIndex(params['regression_forest_criterion'])
		self.RegressionForestMaxDepthCombobox.setCurrentIndex(params['regression_forest_max_depth'])
		self.RegressionForestMinSamplesSplitEdit.setText(params['regression_forest_min_samples_split'])
		self.RegressionForestMinSamplesLeafEdit.setText(params['regression_forest_min_samples_leaf'])
		self.RegressionForestMinWeightedFractionLeafEdit.setText(params['regression_forest_min_weighted_fraction_leaf'])
		self.RegressionForestMaxDepthCombobox.setCurrentIndex(params['regression_forest_max_leaf_nodes'])
		self.RegressionForestNumTrialsPerSplitEdit.setText(params['regression_forest_num_trials_per_split'])


	def onTabChanged(self, idx):
		if not self.checkParameters(self.__currentTab):
			currentTab = self.__currentTab
			self.__currentTab = idx
			self.notebook.setCurrentIndex(currentTab)
		else:
			self.__currentTab = idx


	def onLinRegLossFunctionChanged(self, idx):
		if idx == 0: # l2 norm
			self.linRegLossFunctionParameterEdit.setEnabled(False)
		else: # Huber loss
			self.linRegLossFunctionParameterEdit.setEnabled(True)


	def onSVRKernelChanged(self, idx):
		if idx == 0: # linear
			self.SVRGammaEdit.setEnabled(False)
			self.SVRCoef0Edit.setEnabled(False)
			self.SVRDegreeEdit.setEnabled(False)
		elif idx == 1: # polynomial
			self.SVRGammaEdit.setEnabled(True)
			self.SVRCoef0Edit.setEnabled(True)
			self.SVRDegreeEdit.setEnabled(True)
		elif idx == 2: # rbf
			self.SVRGammaEdit.setEnabled(True)
			self.SVRCoef0Edit.setEnabled(False)
			self.SVRDegreeEdit.setEnabled(False)
		else: # sigmoid
			self.SVRGammaEdit.setEnabled(True)
			self.SVRCoef0Edit.setEnabled(True)
			self.SVRDegreeEdit.setEnabled(False)


	def onRegressionTreeAlgorithmChanged(self, idx):
		if idx == 0: # RegressionTreeRegressor (scikit-learn)
			self.RegressionTreeSplitterCombobox.setEnabled(True) 
			self.RegressionTreeMinSamplesSplitEdit.setEnabled(True)
			self.RegressionTreeMinWeightedFractionLeafEdit.setEnabled(True)
			self.RegressionTreeMaxLeafNodesCombobox.setEnabled(True)
			self.RegressionTreeNumTrialsPerSplitEdit.setEnabled(False)
		else: # Regression Tree
			self.RegressionTreeSplitterCombobox.setCurrentIndex(0) # best
			self.RegressionTreeSplitterCombobox.setEnabled(False)
			self.RegressionTreeMinSamplesSplitEdit.setEnabled(False)
			self.RegressionTreeMinWeightedFractionLeafEdit.setEnabled(False)
			self.RegressionTreeMaxLeafNodesCombobox.setCurrentIndex(0) # None
			self.RegressionTreeMaxLeafNodesCombobox.setEnabled(False)
			if self.RegressionTreeMaxDepthCombobox.currentText().lower() == 'none':
				idx = self.RegressionTreeMaxDepthCombobox.findText('1')
				self.RegressionTreeMaxDepthCombobox.setCurrentIndex(idx)
			self.RegressionTreeNumTrialsPerSplitEdit.setEnabled(True)


	def onRegressionTreeMaxLeafNodesChanged(self, idx):
		if self.RegressionTreeMaxLeafNodesCombobox.currentText() == 'None':
			self.RegressionTreeMaxDepthCombobox.setEnabled(True)
		else:
			self.RegressionTreeMaxDepthCombobox.setEnabled(False)


	def onRegressionForestAlgorithmChanged(self, idx):
		if idx == 0: # RegressionForestRegressor (scikit-learn)
			self.RegressionForestMinSamplesSplitEdit.setEnabled(True)
			self.RegressionForestMinWeightedFractionLeafEdit.setEnabled(True)
			self.RegressionForestMaxLeafNodesCombobox.setEnabled(True)
			self.RegressionForestNumTrialsPerSplitEdit.setEnabled(False)
		else: # Regression Forest
			self.RegressionForestMinSamplesSplitEdit.setEnabled(False)
			self.RegressionForestMinWeightedFractionLeafEdit.setEnabled(False)
			self.RegressionForestMaxLeafNodesCombobox.setCurrentIndex(0) # None
			self.RegressionForestMaxLeafNodesCombobox.setEnabled(False)
			if self.RegressionForestMaxDepthCombobox.currentText().lower() == 'none':
				idx = self.RegressionForestMaxDepthCombobox.findText('1')
				self.RegressionForestMaxDepthCombobox.setCurrentIndex(idx)
			self.RegressionForestNumTrialsPerSplitEdit.setEnabled(True)


	def onRegressionForestMaxLeafNodesChanged(self, idx):
		if self.RegressionForestMaxLeafNodesCombobox.currentText() == 'None':
			self.RegressionForestMaxDepthCombobox.setEnabled(True)
		else:
			self.RegressionForestMaxDepthCombobox.setEnabled(False)


	def setTab(self, tab):
		if tab >= 0:
			self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Compute regression")
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


	def getLinRegLossFunction(self):
		idx = self.linRegLossFunctionCombobox.currentIndex()
		if idx == 0:
			return 'l2'
		elif idx == 1:
			return 'huber'
		else:
			return None


	def getLinRegLossFunctionParam(self):
		return float(self.linRegLossFunctionParameterEdit.text())


	def getSVRAlgorithm(self):
		idx = self.SVRAlgorithmCombobox.currentIndex()
		if idx == 0:
			return 'SVR'
		else:
			return None


	def getSVRKernel(self):
		kernel = self.SVRKernelCombobox.currentIndex()
		if kernel == 0:
			return 'linear'
		elif kernel == 1:
			return 'poly'
		elif kernel == 2:
			return 'rbf'
		else:
			return 'sigmoid'


	def getSVRC(self):
		return float(self.SVRCEdit.text())


	def getSVREpsilon(self):
		return float(self.SVREpsilonEdit.text())


	def getSVRGamma(self):
		return float(self.SVRGammaEdit.text())


	def getSVRCoef0(self):
		return float(self.SVRCoef0Edit.text())


	def getSVRDegree(self):
		return int(self.SVRDegreeEdit.text())


	def getRegressionTreeAlgorithm(self):
		idx = self.RegressionTreeAlgorithmCombobox.currentIndex()
		if idx == 0:
			return 'sklearn'
		elif idx == 1:
			return 'RegressionTree'
		else:
			return None


	def getRegressionTreeCriterion(self):
		idx = self.RegressionTreeAlgorithmCombobox.currentIndex()
		if idx == 0:
			return 'mse'
		else:
			return None


	def getRegressionTreeSplitter(self):
		splitter = self.RegressionTreeSplitterCombobox.currentIndex()
		if splitter == 0:
			return 'best'
		else:
			return 'random'


	def getRegressionTreeMaxDepth(self):
		if not self.RegressionTreeMaxDepthCombobox.isEnabled():
			return None
		value = self.RegressionTreeMaxDepthCombobox.currentText()
		if value.lower() == 'none':
			return None
		return int(value)


	def getRegressionTreeMinSamplesSplit(self):
		return int(self.RegressionTreeMinSamplesSplitEdit.text())


	def getRegressionTreeMinSamplesLeaf(self):
		return int(self.RegressionTreeMinSamplesLeafEdit.text())


	def getRegressionTreeMinWeightedFractionLeaf(self):
		return float(self.RegressionTreeMinWeightedFractionLeafEdit.text())


	def getRegressionTreeMaxLeafNodes(self):
		value = self.RegressionTreeMaxLeafNodesCombobox.currentText()
		if value.lower() == 'none':
			return None
		return int(value)

		
	def getRegressionTreeNumTrialsPerSplit(self):
		return int(self.RegressionTreeNumTrialsPerSplitEdit.text())

		
	def getRegressionForestAlgorithm(self):
		idx = self.RegressionForestAlgorithmCombobox.currentIndex()
		if idx == 0:
			return 'sklearn'
		elif idx == 1:
			return 'RegressionForest'
		else:
			return None


	def getRegressionForestNumTrees(self):
		return int(self.RegressionForestNumTreesEdit.text())


	def getRegressionForestCriterion(self):
		idx = self.RegressionForestAlgorithmCombobox.currentIndex()
		if idx == 0:
			return 'mse'
		else:
			return None


	def getRegressionForestMaxDepth(self):
		if not self.RegressionForestMaxDepthCombobox.isEnabled():
			return None
		value = self.RegressionForestMaxDepthCombobox.currentText()
		if value.lower() == 'none':
			return None
		return int(value)


	def getRegressionForestMinSamplesSplit(self):
		return int(self.RegressionForestMinSamplesSplitEdit.text())


	def getRegressionForestMinSamplesLeaf(self):
		return int(self.RegressionForestMinSamplesLeafEdit.text())


	def getRegressionForestMinWeightedFractionLeaf(self):
		return float(self.RegressionForestMinWeightedFractionLeafEdit.text())


	def getRegressionForestMaxLeafNodes(self):
		value = self.RegressionForestMaxLeafNodesCombobox.currentText()
		if value.lower() == 'none':
			return None
		return int(value)

		
	def getRegressionForestNumTrialsPerSplit(self):
		return int(self.RegressionForestNumTrialsPerSplitEdit.text())




