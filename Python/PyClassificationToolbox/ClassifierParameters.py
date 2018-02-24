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
from PyQt4 import QtCore
import PyQt4.QtGui as QtWidgets

import Parameters


class ClassifierParameters(QtWidgets.QDialog):
	
	def __init__(self, parent):
		super(ClassifierParameters, self).__init__(parent)
		
		self.__parent = parent
		self.__currentTab = 0
		
		# Linear Logistic Regression
		LogRegNumIterationsLabel = QtWidgets.QLabel('Maximum number of iterations')
		LogRegLearningRateLabel = QtWidgets.QLabel('Learning rate')
		self.LogRegNumIterationsEdit = QtWidgets.QLineEdit('100')
		self.LogRegLearningRateEdit = QtWidgets.QLineEdit('0.5')
		
		LogRegGrid = QtWidgets.QGridLayout();
		LogRegGrid.setSpacing(10)
		LogRegGrid.addWidget(LogRegNumIterationsLabel, 0, 0)
		LogRegGrid.addWidget(self.LogRegNumIterationsEdit, 0, 1)
		LogRegGrid.addWidget(LogRegLearningRateLabel, 1, 0)
		LogRegGrid.addWidget(self.LogRegLearningRateEdit, 1, 1)
		
		LogRegFrame = QtWidgets.QGroupBox()
		LogRegFrame.setTitle('Linear Logistic Regression')		
		LogRegFrame.setLayout(LogRegGrid)
		
		LogRegLayout = QtWidgets.QVBoxLayout()
		LogRegLayout.addWidget(LogRegFrame)
		LogRegLayout.addStretch(1)
		
		self.LogRegTab = QtWidgets.QWidget()
		self.LogRegTab.setLayout(LogRegLayout)


		# Norm properties
		NormNormLabel = QtWidgets.QLabel('Norm')
		self.NormNormCombobox = QtWidgets.QComboBox()
		self.NormNormCombobox.addItem('l1 norm')
		self.NormNormCombobox.addItem('l2 norm')
		self.NormNormCombobox.addItem('Mahalanobis distance')
		self.NormNormCombobox.setCurrentIndex(1) # l2 norm

		NormGrid = QtWidgets.QGridLayout();
		NormGrid.setSpacing(10)
		NormGrid.addWidget(NormNormLabel, 0, 0)
		NormGrid.addWidget(self.NormNormCombobox, 0, 1)
		
		NormFrame = QtWidgets.QGroupBox()
		NormFrame.setTitle('Norm classifier')		
		NormFrame.setLayout(NormGrid)
		
		NormLayout = QtWidgets.QVBoxLayout()
		NormLayout.addWidget(NormFrame)
		NormLayout.addStretch(1)
		
		self.NormTab = QtWidgets.QWidget()
		self.NormTab.setLayout(NormLayout)


		# GMM tab
		GmmKLabel = QtWidgets.QLabel('Number of clusters for each class')
		GmmNumIterationsLabel = QtWidgets.QLabel('Maximum number of iterations')
		self.GmmKEdit = QtWidgets.QLineEdit('')
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


		# kNN properties
		KNNAlgorithmLabel = QtWidgets.QLabel('Algorithm')
		KNNNumNeighborsLabel = QtWidgets.QLabel('Number of neighbors')
		KNNWeightsLabel = QtWidgets.QLabel('Weight function')
		self.KNNAlgorithmCombobox = QtWidgets.QComboBox()
		self.KNNAlgorithmCombobox.addItem('kNN (scikit-learn)')
		self.KNNAlgorithmCombobox.addItem('kNN')
		self.KNNAlgorithmCombobox.currentIndexChanged.connect(self.onKNNAlgorithmChanged)
		self.KNNNumNeighborsEdit = QtWidgets.QLineEdit('1')
		self.KNNWeightsCombobox = QtWidgets.QComboBox()
		self.KNNWeightsCombobox.addItem('uniform')
		self.KNNWeightsCombobox.addItem('distance')
		
		KNNGrid = QtWidgets.QGridLayout();
		KNNGrid.setSpacing(10)
		KNNGrid.addWidget(KNNAlgorithmLabel, 0, 0)
		KNNGrid.addWidget(self.KNNAlgorithmCombobox, 0, 1)
		KNNGrid.addWidget(KNNNumNeighborsLabel, 1, 0)
		KNNGrid.addWidget(self.KNNNumNeighborsEdit, 1, 1)
		KNNGrid.addWidget(KNNWeightsLabel, 2, 0)
		KNNGrid.addWidget(self.KNNWeightsCombobox, 2, 1)
		
		KNNFrame = QtWidgets.QGroupBox()
		KNNFrame.setTitle('k Nearest Neighbor classifier')		
		KNNFrame.setLayout(KNNGrid)
		
		KNNLayout = QtWidgets.QVBoxLayout()
		KNNLayout.addWidget(KNNFrame)
		KNNLayout.addStretch(1)
		
		self.KNNTab = QtWidgets.QWidget()
		self.KNNTab.setLayout(KNNLayout)


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


		# Rosenblatt's Perceptron
		PerceptronNumIterationsLabel = QtWidgets.QLabel('Maximum number of iterations')
		PerceptronLearningRateLabel = QtWidgets.QLabel('Learning rate')
		PerceptronBatchModeLabel = QtWidgets.QLabel('Batch mode')
		self.PerceptronNumIterationsEdit = QtWidgets.QLineEdit('2000')
		self.PerceptronLearningRateEdit = QtWidgets.QLineEdit('0.1')
		self.PerceptronBatchModeCombobox = QtWidgets.QComboBox()
		self.PerceptronBatchModeCombobox.addItem('on')
		self.PerceptronBatchModeCombobox.addItem('off')
		
		PerceptronGrid = QtWidgets.QGridLayout();
		PerceptronGrid.setSpacing(10)
		PerceptronGrid.addWidget(PerceptronNumIterationsLabel, 0, 0)
		PerceptronGrid.addWidget(self.PerceptronNumIterationsEdit, 0, 1)
		PerceptronGrid.addWidget(PerceptronLearningRateLabel, 1, 0)
		PerceptronGrid.addWidget(self.PerceptronLearningRateEdit, 1, 1)
		PerceptronGrid.addWidget(PerceptronBatchModeLabel, 2, 0)
		PerceptronGrid.addWidget(self.PerceptronBatchModeCombobox, 2, 1)
		
		PerceptronFrame = QtWidgets.QGroupBox()
		PerceptronFrame.setTitle('Rosenblatt\'s Perceptron')		
		PerceptronFrame.setLayout(PerceptronGrid)
		
		PerceptronLayout = QtWidgets.QVBoxLayout()
		PerceptronLayout.addWidget(PerceptronFrame)
		PerceptronLayout.addStretch(1)
		
		self.PerceptronTab = QtWidgets.QWidget()
		self.PerceptronTab.setLayout(PerceptronLayout)


		# MLP properties
		MLPHiddenLayersLabel = QtWidgets.QLabel('Number of neurons in each hidden layer')
		MLPActivationLabel = QtWidgets.QLabel('Activation function for the hidden layer(s)')
		MLPAlgorithmLabel = QtWidgets.QLabel('Weight optimization algorithm')
		MLPAlphaLabel = QtWidgets.QLabel('Alpha')
		MLPLearningRateLabel = QtWidgets.QLabel('Learning rate')

		self.MLPHiddenLayersEdit = QtWidgets.QLineEdit('(2,)')
		
		self.MLPActivationFunctionCombobox = QtWidgets.QComboBox()
		self.MLPActivationFunctionCombobox.addItem('logistic')
		self.MLPActivationFunctionCombobox.addItem('tanh')
		self.MLPActivationFunctionCombobox.addItem('relu')
		self.MLPActivationFunctionCombobox.setCurrentIndex(2)
		
		self.MLPAlgorithmCombobox = QtWidgets.QComboBox()
		self.MLPAlgorithmCombobox.addItem('l-bfgs')
		self.MLPAlgorithmCombobox.addItem('sgd')
		self.MLPAlgorithmCombobox.addItem('adam')
		self.MLPAlgorithmCombobox.setCurrentIndex(2)
		
		self.MLPAlphaEdit = QtWidgets.QLineEdit('0.0001')
		self.MLPAlphaEdit.setToolTip('L2 penalty (regularization term) parameter')
		self.MLPLearningRateCombobox = QtWidgets.QComboBox()
		self.MLPLearningRateCombobox.addItem('constant')
		self.MLPLearningRateCombobox.addItem('invscaling')
		self.MLPLearningRateCombobox.addItem('adaptive')
		self.MLPLearningRateCombobox.setCurrentIndex(0)
		
		MLPGrid = QtWidgets.QGridLayout();
		MLPGrid.setSpacing(10)
		MLPGrid.addWidget(MLPHiddenLayersLabel, 0, 0)
		MLPGrid.addWidget(self.MLPHiddenLayersEdit, 0, 1)
		MLPGrid.addWidget(MLPActivationLabel, 1, 0)
		MLPGrid.addWidget(self.MLPActivationFunctionCombobox, 1, 1)
		MLPGrid.addWidget(MLPAlgorithmLabel, 2, 0)
		MLPGrid.addWidget(self.MLPAlgorithmCombobox, 2, 1)
		MLPGrid.addWidget(MLPAlphaLabel, 3, 0)
		MLPGrid.addWidget(self.MLPAlphaEdit, 3, 1)
		MLPGrid.addWidget(MLPLearningRateLabel, 4, 0)
		MLPGrid.addWidget(self.MLPLearningRateCombobox, 4, 1)
		
		MLPFrame = QtWidgets.QGroupBox()
		MLPFrame.setTitle('Multilayer Perceptron')
		MLPFrame.setLayout(MLPGrid)
		
		MLPLayout = QtWidgets.QVBoxLayout()
		MLPLayout.addWidget(MLPFrame)
		MLPLayout.addStretch(1)
		
		self.MLPTab = QtWidgets.QWidget()
		self.MLPTab.setLayout(MLPLayout)


		# SVM properties
		SVMAlgorithmLabel = QtWidgets.QLabel('Algorithm')
		SVMKernelLabel = QtWidgets.QLabel('Kernel')
		SVMCLabel = QtWidgets.QLabel('C')
		SVMGammaLabel = QtWidgets.QLabel('Gamma')
		SVMCoef0Label = QtWidgets.QLabel('Coef0')
		SVMDegreeLabel = QtWidgets.QLabel('Degree')
		self.SVMAlgorithmCombobox = QtWidgets.QComboBox()
		self.SVMAlgorithmCombobox.addItem('LinearSVC (scikit-learn)')
		self.SVMAlgorithmCombobox.addItem('SVC (scikit-learn)')
		self.SVMAlgorithmCombobox.addItem('Hard Margin SVM')
		self.SVMAlgorithmCombobox.addItem('Soft Margin SVM')		
		self.SVMAlgorithmCombobox.addItem('Kernel SVM')		
		self.SVMAlgorithmCombobox.currentIndexChanged.connect(self.onSVMAlgorithmChanged)
		
		self.SVMKernelCombobox = QtWidgets.QComboBox()
		self.SVMKernelCombobox.addItem('linear')
		self.SVMKernelCombobox.addItem('polynomial')
		self.SVMKernelCombobox.addItem('radial basis functions')
		self.SVMKernelCombobox.addItem('sigmoid')
		self.SVMKernelCombobox.currentIndexChanged.connect(self.onSVMKernelChanged)
		self.SVMCEdit = QtWidgets.QLineEdit('1.0')
		self.SVMCEdit.setToolTip('Penalty parameter of the error term')
		self.SVMGammaEdit = QtWidgets.QLineEdit('0.5')
		self.SVMGammaEdit.setToolTip('Kernel coefficient')
		self.SVMCoef0Edit = QtWidgets.QLineEdit('0.0')
		self.SVMCoef0Edit.setToolTip('Independent term in kernel function')
		self.SVMDegreeEdit = QtWidgets.QLineEdit('3')
		self.SVMDegreeEdit.setToolTip('Degree of the polynomial kernel function')
		self.onSVMAlgorithmChanged(0)
		self.onSVMKernelChanged(0)
		
		SVMGrid = QtWidgets.QGridLayout();
		SVMGrid.setSpacing(10)
		SVMGrid.addWidget(SVMAlgorithmLabel, 0, 0)
		SVMGrid.addWidget(self.SVMAlgorithmCombobox, 0, 1)
		SVMGrid.addWidget(SVMKernelLabel, 1, 0)
		SVMGrid.addWidget(self.SVMKernelCombobox, 1, 1)
		SVMGrid.addWidget(SVMCLabel, 2, 0)
		SVMGrid.addWidget(self.SVMCEdit, 2, 1)
		SVMGrid.addWidget(SVMGammaLabel, 3, 0)
		SVMGrid.addWidget(self.SVMGammaEdit, 3, 1)
		SVMGrid.addWidget(SVMCoef0Label, 4, 0)
		SVMGrid.addWidget(self.SVMCoef0Edit, 4, 1)
		SVMGrid.addWidget(SVMDegreeLabel, 5, 0)
		SVMGrid.addWidget(self.SVMDegreeEdit, 5, 1)
		
		SVMFrame = QtWidgets.QGroupBox()
		SVMFrame.setTitle('Support Vector Classification')
		SVMFrame.setLayout(SVMGrid)
		
		SVMLayout = QtWidgets.QVBoxLayout()
		SVMLayout.addWidget(SVMFrame)
		SVMLayout.addStretch(1)
		
		self.SVMTab = QtWidgets.QWidget()
		self.SVMTab.setLayout(SVMLayout)
		
		
		# Decision Tree
		DecisionTreeAlgorithmLabel = QtWidgets.QLabel('Algorithm')
		DecisionTreeCriterionLabel = QtWidgets.QLabel('Quality criterion')
		DecisionTreeSplitterLabel = QtWidgets.QLabel('Splitting strategy')
		DecisionTreeMaxDepthLabel = QtWidgets.QLabel('Maximum tree depth')
		DecisionTreeMinSamplesSplitLabel = QtWidgets.QLabel('Minimum samples required to split internal node')
		DecisionTreeMinSamplesLeafLabel = QtWidgets.QLabel('Minimum samples required at leaf node')
		DecisionTreeMinWeightedFractionLeafLabel = QtWidgets.QLabel('Minimum weighted fraction at leaf node')
		DecisionTreeMaxLeafNodesLabel = QtWidgets.QLabel('Maximum leaf nodes')
		DecisionTreeNumTrialsPerSplitLabel = QtWidgets.QLabel('Number of trials to split a node')
		self.DecisionTreeAlgorithmCombobox = QtWidgets.QComboBox()
		self.DecisionTreeAlgorithmCombobox.addItem('DecisionTreeClassifier (scikit-learn)')
		self.DecisionTreeAlgorithmCombobox.addItem('Decision Tree')
		self.DecisionTreeAlgorithmCombobox.currentIndexChanged.connect(self.onDecisionTreeAlgorithmChanged)
		self.DecisionTreeCriterionCombobox = QtWidgets.QComboBox()
		self.DecisionTreeCriterionCombobox.addItem('Gini impurity')
		self.DecisionTreeCriterionCombobox.addItem('Information gain')
		self.DecisionTreeSplitterCombobox = QtWidgets.QComboBox()
		self.DecisionTreeSplitterCombobox.addItem('best')
		self.DecisionTreeSplitterCombobox.addItem('random')
		self.DecisionTreeMaxDepthCombobox = QtWidgets.QComboBox()
		self.DecisionTreeMaxDepthCombobox.addItem('None')
		self.DecisionTreeMaxDepthCombobox.addItems([str(x) for x in range(1, 10)])
		self.DecisionTreeMaxDepthCombobox.setEditable(True)
		self.DecisionTreeMaxDepthCombobox.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)		
		self.DecisionTreeMinSamplesSplitEdit = QtWidgets.QLineEdit('2')
		self.DecisionTreeMinSamplesLeafEdit = QtWidgets.QLineEdit('1')
		self.DecisionTreeMinWeightedFractionLeafEdit = QtWidgets.QLineEdit('0.')
		self.DecisionTreeMaxLeafNodesCombobox = QtWidgets.QComboBox()
		self.DecisionTreeMaxLeafNodesCombobox.addItems(['None', '10', '20', '30', '40', '50'])
		self.DecisionTreeMaxLeafNodesCombobox.setEditable(True)
		self.DecisionTreeMaxLeafNodesCombobox.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
		self.DecisionTreeMaxLeafNodesCombobox.currentIndexChanged.connect(self.onDecisionTreeMaxLeafNodesChanged)
		self.DecisionTreeNumTrialsPerSplitEdit = QtWidgets.QLineEdit('10')
		self.DecisionTreeNumTrialsPerSplitEdit.setEnabled(False)
		
		DecisionTreeGrid = QtWidgets.QGridLayout();
		DecisionTreeGrid.setSpacing(10)
		DecisionTreeGrid.addWidget(DecisionTreeAlgorithmLabel, 0, 0)
		DecisionTreeGrid.addWidget(self.DecisionTreeAlgorithmCombobox, 0, 1)
		DecisionTreeGrid.addWidget(DecisionTreeCriterionLabel, 1, 0)
		DecisionTreeGrid.addWidget(self.DecisionTreeCriterionCombobox, 1, 1)
		DecisionTreeGrid.addWidget(DecisionTreeSplitterLabel, 2, 0)
		DecisionTreeGrid.addWidget(self.DecisionTreeSplitterCombobox, 2, 1)
		DecisionTreeGrid.addWidget(DecisionTreeMaxDepthLabel, 3, 0)
		DecisionTreeGrid.addWidget(self.DecisionTreeMaxDepthCombobox, 3, 1)
		DecisionTreeGrid.addWidget(DecisionTreeMinSamplesSplitLabel, 4, 0)
		DecisionTreeGrid.addWidget(self.DecisionTreeMinSamplesSplitEdit, 4, 1)
		DecisionTreeGrid.addWidget(DecisionTreeMinSamplesLeafLabel, 5, 0)
		DecisionTreeGrid.addWidget(self.DecisionTreeMinSamplesLeafEdit, 5, 1)
		DecisionTreeGrid.addWidget(DecisionTreeMinWeightedFractionLeafLabel, 6, 0)
		DecisionTreeGrid.addWidget(self.DecisionTreeMinWeightedFractionLeafEdit, 6, 1)
		DecisionTreeGrid.addWidget(DecisionTreeMaxLeafNodesLabel, 7, 0)
		DecisionTreeGrid.addWidget(self.DecisionTreeMaxLeafNodesCombobox, 7, 1)
		DecisionTreeGrid.addWidget(DecisionTreeNumTrialsPerSplitLabel, 8, 0)
		DecisionTreeGrid.addWidget(self.DecisionTreeNumTrialsPerSplitEdit, 8, 1)
		
		DecisionTreeFrame = QtWidgets.QGroupBox()
		DecisionTreeFrame.setTitle('Decision Trees')		
		DecisionTreeFrame.setLayout(DecisionTreeGrid)
		
		DecisionTreeLayout = QtWidgets.QVBoxLayout()
		DecisionTreeLayout.addWidget(DecisionTreeFrame)
		DecisionTreeLayout.addStretch(1)
		
		self.DecisionTreeTab = QtWidgets.QWidget()
		self.DecisionTreeTab.setLayout(DecisionTreeLayout)


		# Random Forests
		RandomForestAlgorithmLabel = QtWidgets.QLabel('Algorithm')
		RandomForestNumTreesLabel = QtWidgets.QLabel('Number of trees')
		RandomForestCriterionLabel = QtWidgets.QLabel('Quality criterion')
		RandomForestMaxDepthLabel = QtWidgets.QLabel('Maximum tree depth')
		RandomForestMinSamplesSplitLabel = QtWidgets.QLabel('Minimum samples required to split internal node')
		RandomForestMinSamplesLeafLabel = QtWidgets.QLabel('Minimum samples required at leaf node')
		RandomForestMinWeightedFractionLeafLabel = QtWidgets.QLabel('Minimum weighted fraction at leaf node')
		RandomForestMaxLeafNodesLabel = QtWidgets.QLabel('Maximum leaf nodes')
		RandomForestNumTrialsPerSplitLabel = QtWidgets.QLabel('Number of trials to split a node')
		self.RandomForestAlgorithmCombobox = QtWidgets.QComboBox()
		self.RandomForestAlgorithmCombobox.addItem('RandomForestClassifier (scikit-learn)')
		self.RandomForestAlgorithmCombobox.addItem('Random Forest')
		self.RandomForestAlgorithmCombobox.currentIndexChanged.connect(self.onRandomForestAlgorithmChanged)
		self.RandomForestNumTreesEdit = QtWidgets.QLineEdit('10')
		self.RandomForestCriterionCombobox = QtWidgets.QComboBox()
		self.RandomForestCriterionCombobox.addItem('Gini impurity')
		self.RandomForestCriterionCombobox.addItem('Information gain')
		self.RandomForestMaxDepthCombobox = QtWidgets.QComboBox()
		self.RandomForestMaxDepthCombobox.addItem('None')
		self.RandomForestMaxDepthCombobox.addItems([str(x) for x in range(1, 10)])
		self.RandomForestMaxDepthCombobox.setEditable(True)
		self.RandomForestMaxDepthCombobox.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)		
		self.RandomForestMinSamplesSplitEdit = QtWidgets.QLineEdit('2')
		self.RandomForestMinSamplesLeafEdit = QtWidgets.QLineEdit('1')
		self.RandomForestMinWeightedFractionLeafEdit = QtWidgets.QLineEdit('0.')
		self.RandomForestMaxLeafNodesCombobox = QtWidgets.QComboBox()
		self.RandomForestMaxLeafNodesCombobox.addItems(['None', '10', '20', '30', '40', '50'])
		self.RandomForestMaxLeafNodesCombobox.setEditable(True)
		self.RandomForestMaxLeafNodesCombobox.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
		self.RandomForestMaxLeafNodesCombobox.currentIndexChanged.connect(self.onRandomForestMaxLeafNodesChanged)
		self.RandomForestNumTrialsPerSplitEdit = QtWidgets.QLineEdit('10')
		self.RandomForestNumTrialsPerSplitEdit.setEnabled(False)
		
		RandomForestGrid = QtWidgets.QGridLayout();
		RandomForestGrid.setSpacing(10)
		RandomForestGrid.addWidget(RandomForestAlgorithmLabel, 0, 0)
		RandomForestGrid.addWidget(self.RandomForestAlgorithmCombobox, 0, 1)
		RandomForestGrid.addWidget(RandomForestNumTreesLabel, 1, 0)
		RandomForestGrid.addWidget(self.RandomForestNumTreesEdit, 1, 1)
		RandomForestGrid.addWidget(RandomForestCriterionLabel, 2, 0)
		RandomForestGrid.addWidget(self.RandomForestCriterionCombobox, 2, 1)
		RandomForestGrid.addWidget(RandomForestMaxDepthLabel, 3, 0)
		RandomForestGrid.addWidget(self.RandomForestMaxDepthCombobox, 3, 1)
		RandomForestGrid.addWidget(RandomForestMinSamplesSplitLabel, 4, 0)
		RandomForestGrid.addWidget(self.RandomForestMinSamplesSplitEdit, 4, 1)
		RandomForestGrid.addWidget(RandomForestMinSamplesLeafLabel, 5, 0)
		RandomForestGrid.addWidget(self.RandomForestMinSamplesLeafEdit, 5, 1)
		RandomForestGrid.addWidget(RandomForestMinWeightedFractionLeafLabel, 6, 0)
		RandomForestGrid.addWidget(self.RandomForestMinWeightedFractionLeafEdit, 6, 1)
		RandomForestGrid.addWidget(RandomForestMaxLeafNodesLabel, 7, 0)
		RandomForestGrid.addWidget(self.RandomForestMaxLeafNodesCombobox, 7, 1)
		RandomForestGrid.addWidget(RandomForestNumTrialsPerSplitLabel, 8, 0)
		RandomForestGrid.addWidget(self.RandomForestNumTrialsPerSplitEdit, 8, 1)
		
		RandomForestFrame = QtWidgets.QGroupBox()
		RandomForestFrame.setTitle('Random Forests')		
		RandomForestFrame.setLayout(RandomForestGrid)
		
		RandomForestLayout = QtWidgets.QVBoxLayout()
		RandomForestLayout.addWidget(RandomForestFrame)
		RandomForestLayout.addStretch(1)
		
		self.RandomForestTab = QtWidgets.QWidget()
		self.RandomForestTab.setLayout(RandomForestLayout)


		# Create notebook tabs		
		self.notebook = QtWidgets.QTabWidget()
		self.notebook.addTab(self.LogRegTab, "LogReg")
		self.notebook.addTab(self.NormTab, "Norm")
		self.notebook.addTab(self.GmmTab, "GMM")
		self.notebook.addTab(self.KNNTab, "kNN")
		self.notebook.addTab(self.linRegTab, "LinReg")
		self.notebook.addTab(self.PerceptronTab, "Perceptron")
		self.notebook.addTab(self.MLPTab, "MLP")
		self.notebook.addTab(self.SVMTab, "SVM")
		self.notebook.addTab(self.DecisionTreeTab, "Tree")
		self.notebook.addTab(self.RandomForestTab, "Forest")
		self.notebook.currentChanged.connect(self.onTabChanged)
		
		
		# OK and Cancel buttons
		self.buttons = QtWidgets.QDialogButtonBox(
			QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
			QtCore.Qt.Horizontal, self)
		self.buttons.button(QtWidgets.QDialogButtonBox.Cancel).setText("Cancel")
		self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Classify")

		self.buttons.accepted.connect(self.onAccept)
		self.buttons.rejected.connect(self.onReject)
		

		layout = QtWidgets.QVBoxLayout(self)
		layout.addWidget(self.notebook)		
		layout.addWidget(self.buttons)
		
		self.setWindowTitle('Classifier parameters')
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
		if tab == 0: # Linear Logistic Regression parameters
			if not self.testParameter(self.getLogRegMaxNumIterations, 'The maximum number of iterations has to be an integer number!'):
				return False
			
			if not self.testParameter(self.getLogRegLearningRate, 'The learning rate has to be a floating point number!'):
				return False

			maxNumIter = self.getLogRegMaxNumIterations()
			if maxNumIter < 1:
				self.errorMsg('The maximum number of iterations has to be positive!')
				return False

			rate = self.getLogRegLearningRate()
			if rate <= 0:
				self.errorMsg('The learning rate has to be positive!')
				return False
		elif tab == 1: # Norm paramters
			pass
		elif tab == 2: # GMM
			if not self.testParameter(self.getGmmNumComponentsPerClass, 'The number of components has to be a positive integer number!'):
				return False
			
			if not self.testParameter(self.getGmmMaxNumIterations, 'The maximum number of iterations has to be an integer number!'):
				return False
			
			k = self.getGmmNumComponentsPerClass()
			if len(k) != self.__numClasses: 
				self.errorMsg('Wrong specification of the number of GMM components for each class!')
				return False

			maxNumIter = self.getGmmMaxNumIterations()
			if maxNumIter < 1:
				self.errorMsg('The maximum number of iterations has to be positive!')
				return False
		elif tab == 3: # kNN paramters
			if not self.testParameter(self.getKNNNumberOfNeighbors, 'The number of neighbors has to be an integer number!'):
				return False
			
			k = self.getKNNNumberOfNeighbors()
			if k < 1:
				self.errorMsg('The number of neighbors has to be at least 1!')
				return False
		elif tab == 4: # Linear Regression parameters
			if not self.testParameter(self.getLinRegLossFunctionParam, 'The parameter of the loss function has to be a floating point number!'):
				return False
			
			a = self.getLinRegLossFunctionParam()
			if a <= 0: 
				self.errorMsg('The parameter of the loss function has to be positive!')
				return False
		elif tab == 5: # Rosenblatt's Perceptron parameters
			if not self.testParameter(self.getPerceptronMaxNumIterations, 'The maximum number of iterations has to be an integer number!'):
				return False
			
			if not self.testParameter(self.getPerceptronLearningRate, 'The learning rate has to be a floating point number!'):
				return False
			
			maxNumIter = self.getPerceptronMaxNumIterations()
			if maxNumIter < 1:
				self.errorMsg('The maximum number of iterations has to be positive!')
				return False
			
			rate = self.getPerceptronLearningRate()
			if rate <= 0:
				self.errorMsg('The learning rate has to be positive!')
				return False
		elif tab == 6: # MLP parameters
			if not self.testParameter(self.getMLPAlpha, 'The Alpha parameter has to be a floating point number!'):
				return False
			
		elif tab == 7: # SVM parameters
			if not self.testParameter(self.getSVMC, 'The penalty parameter C has to be a floating point number!'):
				return False
		
			if not self.testParameter(self.getSVMGamma, 'The kernel parameter Gamma has to be a floating point number!'):
				return False

			if not self.testParameter(self.getSVMCoef0, 'The independent term in the kernel function Coef0 has to be a floating point number!'):
				return False
		
			if not self.testParameter(self.getSVMDegree, 'The degree of the polynomial kernel function has to be an integer number!'):
				return False
		
			degree = self.getSVMDegree()
			if degree < 1:
				self.errorMsg('The degree of the polynomial kernel has to be at least 1!')
				return False
			
			C = self.getSVMC()
			if C <= 0:
				self.errorMsg('The penalty parameter C has to be positive!')
				return False
			
			gamma = self.getSVMGamma()
			if gamma <= 0:
				self.errorMsg('The kernel parameter Gamma has to be positive!')
				return False

		elif tab == 8: # Decision Tree parameters
			if not self.testParameter(self.getDecisionTreeMaxDepth, 'The maximum depth of the tree has to be None or an integer number!'):
				return False

			if not self.testParameter(self.getDecisionTreeMaxLeafNodes, 'The maximum number of leaf nodes has to be None or an integer number!'):
				return False

			if not self.testParameter(self.getDecisionTreeMinSamplesSplit, 'The minimum number of samples required to split an internal node has to be an integer number!'):
				return False

			if not self.testParameter(self.getDecisionTreeMinSamplesLeaf, 'The minimum number of samples required to be at a leaf node has to be an integer number!'):
				return False

			if not self.testParameter(self.getDecisionTreeMinWeightedFractionLeaf, 'The minimum weighted fraction of the input samples required to be at a leaf node has to be a real number!'):
				return False

			if not self.testParameter(self.getDecisionTreeNumTrialsPerSplit, 'The number of trials to split a node has to be an integer number!'):
				return False

			depth = self.getDecisionTreeMaxDepth()
			if not(depth == None) and (depth < 1):
				self.errorMsg('The maximum depth of the tree has to be at least 1!')
				return False

			leafNodes = self.getDecisionTreeMaxLeafNodes()
			if not(leafNodes == None) and (leafNodes < 2):
				self.errorMsg('The maximum number of leaf nodes has to be at least 2!')
				return False

			split = self.getDecisionTreeMinSamplesSplit()
			if split < 2:
				self.errorMsg('The minimum number of samples required to split an internal node has to be at least 2!')
				return False

			leaf = self.getDecisionTreeMinSamplesLeaf()
			if leaf < 1:
				self.errorMsg('The minimum number of samples required to be at a leaf node has to be at least 1!')
				return False

			fraction = self.getDecisionTreeMinWeightedFractionLeaf()
			if (fraction < 0) or (fraction > 0.5):
				self.errorMsg('The minimum weighted fraction of the input samples required to be at a leaf node has to be between 0.0 and 0.5!')
				return False

			trials = self.getDecisionTreeNumTrialsPerSplit()
			if trials < 1:
				self.errorMsg('The number of trials to split a node has to be at least 1!')
				return False

		elif tab == 9: # Random Forest parameters
			if not self.testParameter(self.getRandomForestNumTrees, 'The number of trees in the forest has to be an integer number!'):
				return False

			if not self.testParameter(self.getRandomForestMaxDepth, 'The maximum depth of the tree has to be None or an integer number!'):
				return False

			if not self.testParameter(self.getRandomForestMaxLeafNodes, 'The maximum number of leaf nodes has to be None or an integer number!'):
				return False

			if not self.testParameter(self.getRandomForestMinSamplesSplit, 'The minimum number of samples required to split an internal node has to be an integer number!'):
				return False

			if not self.testParameter(self.getRandomForestMinSamplesLeaf, 'The minimum number of samples required to be at a leaf node has to be an integer number!'):
				return False

			if not self.testParameter(self.getRandomForestMinWeightedFractionLeaf, 'The minimum weighted fraction of the input samples required to be at a leaf node has to be a real number!'):
				return False

			if not self.testParameter(self.getRandomForestNumTrialsPerSplit, 'The number of trials to split a node has to be an integer number!'):
				return False

			trees = self.getRandomForestNumTrees()
			if trees < 1:
				self.errorMsg('The number of trees in the forest has to be at least 1!')
				return False			

			depth = self.getRandomForestMaxDepth()
			if not(depth == None) and (depth < 1):
				self.errorMsg('The maximum depth of the tree has to be at least 1!')
				return False

			leafNodes = self.getRandomForestMaxLeafNodes()
			if not(leafNodes == None) and (leafNodes < 2):
				self.errorMsg('The maximum number of leaf nodes has to be at least 2!')
				return False

			split = self.getRandomForestMinSamplesSplit()
			if split < 2:
				self.errorMsg('The minimum number of samples required to split an internal node has to be at least 2!')
				return False

			leaf = self.getRandomForestMinSamplesLeaf()
			if leaf < 1:
				self.errorMsg('The minimum number of samples required to be at a leaf node has to be at least 1!')
				return False

			fraction = self.getRandomForestMinWeightedFractionLeaf()
			if (fraction < 0) or (fraction > 0.5):
				self.errorMsg('The minimum weighted fraction of the input samples required to be at a leaf node has to be between 0.0 and 0.5!')
				return False

			trials = self.getRandomForestNumTrialsPerSplit()
			if trials < 1:
				self.errorMsg('The number of trials to split a node has to be at least 1!')
				return False

		return True


	def onAccept(self):
		if not self.checkParameters(self.notebook.currentIndex()):
			return		
		super(ClassifierParameters, self).accept()


	def onReject(self):
		self.restoreParameters()
		super(ClassifierParameters, self).reject()


	def showEvent(self, event):
		self.__parameters = self.getParameters()
		self.__numClasses = self.__parent.featurespace.getNumberOfClasses()
		self.GmmAdjustNumComponentsPerClass()


	def getParameters(self):
		params = {}
		params['LogReg_maxnumiterations'] = self.LogRegNumIterationsEdit.text()
		params['LogReg_learningrate'] = self.LogRegLearningRateEdit.text()
		params['norm_norm'] = self.NormNormCombobox.currentIndex()
		params['GMM_k'] = self.GmmKEdit.text()
		params['GMM_iterations'] = self.GmmNumIterationsEdit.text()
		params['knn_algo'] = self.KNNAlgorithmCombobox.currentIndex()
		params['knn_k'] = self.KNNNumNeighborsEdit.text()
		params['knn_weights'] = self.KNNWeightsCombobox.currentIndex()
		params['LinReg_loss_function'] = self.linRegLossFunctionCombobox.currentIndex()
		params['LinReg_loss_function_param'] = self.linRegLossFunctionParameterEdit.text()
		params['perceptron_maxnumiterations'] = self.PerceptronNumIterationsEdit.text()
		params['perceptron_learningrate'] = self.PerceptronLearningRateEdit.text()
		params['perceptron_batchmode'] = self.PerceptronBatchModeCombobox.currentIndex()
		params['mlp_hiddenlayers'] = self.MLPHiddenLayersEdit.text()
		params['mlp_activation'] = self.MLPActivationFunctionCombobox.currentIndex()
		params['mlp_algo'] = self.MLPAlgorithmCombobox.currentIndex()
		params['mlp_alpha'] = self.MLPAlphaEdit.text()
		params['mlp_learningrate'] = self.MLPLearningRateCombobox.currentIndex()
		params['svm_algo'] = self.SVMAlgorithmCombobox.currentIndex()
		params['svm_kernel'] = self.SVMKernelCombobox.currentIndex()
		params['svm_c'] = self.SVMCEdit.text()
		params['svm_gamma'] = self.SVMGammaEdit.text()
		params['svm_coef0'] = self.SVMCoef0Edit.text()
		params['svm_degree'] = self.SVMDegreeEdit.text()
		params['decision_tree_algo'] = self.DecisionTreeAlgorithmCombobox.currentIndex()
		params['decision_tree_criterion'] = self.DecisionTreeCriterionCombobox.currentIndex()
		params['decision_tree_splitter'] = self.DecisionTreeSplitterCombobox.currentIndex()
		params['decision_tree_max_depth'] = self.DecisionTreeMaxDepthCombobox.currentIndex()
		params['decision_tree_min_samples_split'] = self.DecisionTreeMinSamplesSplitEdit.text()
		params['decision_tree_min_samples_leaf'] = self.DecisionTreeMinSamplesLeafEdit.text()
		params['decision_tree_min_weighted_fraction_leaf'] = self.DecisionTreeMinWeightedFractionLeafEdit.text()
		params['decision_tree_max_leaf_nodes'] = self.DecisionTreeMaxDepthCombobox.currentIndex()
		params['decision_tree_num_trials_per_split'] = self.DecisionTreeNumTrialsPerSplitEdit.text()
		params['random_forest_algo'] = self.RandomForestAlgorithmCombobox.currentIndex()
		params['random_forest_numtrees'] = self.RandomForestNumTreesEdit.text()
		params['random_forest_criterion'] = self.RandomForestCriterionCombobox.currentIndex()
		params['random_forest_max_depth'] = self.RandomForestMaxDepthCombobox.currentIndex()
		params['random_forest_min_samples_split'] = self.RandomForestMinSamplesSplitEdit.text()
		params['random_forest_min_samples_leaf'] = self.RandomForestMinSamplesLeafEdit.text()
		params['random_forest_min_weighted_fraction_leaf'] = self.RandomForestMinWeightedFractionLeafEdit.text()
		params['random_forest_max_leaf_nodes'] = self.RandomForestMaxDepthCombobox.currentIndex()
		params['random_forest_num_trials_per_split'] = self.RandomForestNumTrialsPerSplitEdit.text()
		return params

		
	def restoreParameters(self):
		params = self.__parameters
		self.LogRegNumIterationsEdit.setText(params['LogReg_maxnumiterations'])
		self.LogRegLearningRateEdit.setText(params['LogReg_learningrate'])
		self.NormNormCombobox.setCurrentIndex(params['norm_norm'])
		self.GmmKEdit.setText(params['GMM_k'])
		self.GmmNumIterationsEdit.setText(params['GMM_iterations'])
		self.KNNAlgorithmCombobox.setCurrentIndex(params['knn_algo'])
		self.KNNNumNeighborsEdit.setText(params['knn_k'])
		self.KNNWeightsCombobox.setCurrentIndex(params['knn_weights'])
		self.linRegLossFunctionCombobox.setCurrentIndex(params['LinReg_loss_function'])
		self.linRegLossFunctionParameterEdit.setText(params['LinReg_loss_function_param'])
		self.SVMAlgorithmCombobox.setCurrentIndex(params['svm_algo'])
		self.SVMKernelCombobox.setCurrentIndex(params['svm_kernel'])
		self.PerceptronNumIterationsEdit.setText(params['perceptron_maxnumiterations'])
		self.PerceptronLearningRateEdit.setText(params['perceptron_learningrate'])
		self.PerceptronBatchModeCombobox.setCurrentIndex(params['perceptron_batchmode'])
		self.MLPHiddenLayersEdit.setText(params['mlp_hiddenlayers'])
		self.MLPActivationFunctionCombobox.setCurrentIndex(params['mlp_activation'])
		self.MLPAlgorithmCombobox.setCurrentIndex(params['mlp_algo'])
		self.MLPAlphaEdit.setText(params['mlp_alpha'])
		self.MLPLearningRateCombobox.setCurrentIndex(params['mlp_learningrate'])
		self.SVMCEdit.setText(params['svm_c'])
		self.SVMGammaEdit.setText(params['svm_gamma'])
		self.SVMCoef0Edit.setText(params['svm_coef0'])
		self.SVMDegreeEdit.setText(params['svm_degree'])
		self.DecisionTreeAlgorithmCombobox.setCurrentIndex(params['decision_tree_algo'])
		self.DecisionTreeCriterionCombobox.setCurrentIndex(params['decision_tree_criterion'])
		self.DecisionTreeSplitterCombobox.setCurrentIndex(params['decision_tree_splitter'])
		self.DecisionTreeMaxDepthCombobox.setCurrentIndex(params['decision_tree_max_depth'])
		self.DecisionTreeMinSamplesSplitEdit.setText(params['decision_tree_min_samples_split'])
		self.DecisionTreeMinSamplesLeafEdit.setText(params['decision_tree_min_samples_leaf'])
		self.DecisionTreeMinWeightedFractionLeafEdit.setText(params['decision_tree_min_weighted_fraction_leaf'])
		self.DecisionTreeMaxDepthCombobox.setCurrentIndex(params['decision_tree_max_leaf_nodes'])
		self.DecisionTreeNumTrialsPerSplitEdit.setText(params['decision_tree_num_trials_per_split'])
		self.RandomForestAlgorithmCombobox.setCurrentIndex(params['random_forest_algo'])
		self.RandomForestNumTreesEdit.setText(params['random_forest_numtrees'])
		self.RandomForestCriterionCombobox.setCurrentIndex(params['random_forest_criterion'])
		self.RandomForestMaxDepthCombobox.setCurrentIndex(params['random_forest_max_depth'])
		self.RandomForestMinSamplesSplitEdit.setText(params['random_forest_min_samples_split'])
		self.RandomForestMinSamplesLeafEdit.setText(params['random_forest_min_samples_leaf'])
		self.RandomForestMinWeightedFractionLeafEdit.setText(params['random_forest_min_weighted_fraction_leaf'])
		self.RandomForestMaxDepthCombobox.setCurrentIndex(params['random_forest_max_leaf_nodes'])
		self.RandomForestNumTrialsPerSplitEdit.setText(params['random_forest_num_trials_per_split'])


	def onTabChanged(self, idx):
		if not self.checkParameters(self.__currentTab):
			currentTab = self.__currentTab
			self.__currentTab = idx
			self.notebook.setCurrentIndex(currentTab)
		else:
			self.__currentTab = idx


	def onKNNAlgorithmChanged(self, idx):
		if idx == 0: # kNN (scikit-learn)
			self.KNNWeightsCombobox.setEnabled(True)
		else: # kNN
			self.KNNWeightsCombobox.setCurrentIndex(0) # uniform weighting
			self.KNNWeightsCombobox.setEnabled(False)


	def onSVMAlgorithmChanged(self, idx):
		if idx == 0: # LinearSVC
			self.SVMKernelCombobox.setCurrentIndex(0) # linear
			self.SVMKernelCombobox.setEnabled(False)
			self.SVMCEdit.setEnabled(True)
		elif idx == 1: # SVC
			self.SVMKernelCombobox.setEnabled(True)
			self.SVMCEdit.setEnabled(True)
		elif idx == 2: # Hard Margin SVM
			self.SVMKernelCombobox.setCurrentIndex(0) # linear
			self.SVMKernelCombobox.setEnabled(False)			
			self.SVMCEdit.setEnabled(False)
		elif idx == 3: # Soft Margin SVM
			self.SVMKernelCombobox.setCurrentIndex(0) # linear
			self.SVMKernelCombobox.setEnabled(False)
			self.SVMCEdit.setEnabled(True)
		else: # Kernel SVM
			self.SVMKernelCombobox.setCurrentIndex(2) # RBF
			self.SVMKernelCombobox.setEnabled(False)
			self.SVMCEdit.setEnabled(True)


	def onSVMKernelChanged(self, idx):
		if idx == 0: # linear
			self.SVMGammaEdit.setEnabled(False)
			self.SVMCoef0Edit.setEnabled(False)
			self.SVMDegreeEdit.setEnabled(False)
		elif idx == 1: # polynomial
			self.SVMGammaEdit.setEnabled(True)
			self.SVMCoef0Edit.setEnabled(True)
			self.SVMDegreeEdit.setEnabled(True)
		elif idx == 2: # rbf
			self.SVMGammaEdit.setEnabled(True)
			self.SVMCoef0Edit.setEnabled(False)
			self.SVMDegreeEdit.setEnabled(False)
		else: # sigmoid
			self.SVMGammaEdit.setEnabled(True)
			self.SVMCoef0Edit.setEnabled(True)
			self.SVMDegreeEdit.setEnabled(False)


	def onLinRegLossFunctionChanged(self, idx):
		if idx == 0: # l2 norm
			self.linRegLossFunctionParameterEdit.setEnabled(False)
		else: # Huber loss
			self.linRegLossFunctionParameterEdit.setEnabled(True)


	def onDecisionTreeAlgorithmChanged(self, idx):
		if idx == 0: # DecisionTreeClassifier (scikit-learn)
			self.DecisionTreeCriterionCombobox.setEnabled(True) 
			self.DecisionTreeSplitterCombobox.setEnabled(True) 
			self.DecisionTreeMinSamplesSplitEdit.setEnabled(True)
			self.DecisionTreeMinWeightedFractionLeafEdit.setEnabled(True)
			self.DecisionTreeMaxLeafNodesCombobox.setEnabled(True)
			self.DecisionTreeNumTrialsPerSplitEdit.setEnabled(False)
		else: # Decision Tree
			self.DecisionTreeCriterionCombobox.setCurrentIndex(1) # information gain
			self.DecisionTreeCriterionCombobox.setEnabled(False)
			self.DecisionTreeSplitterCombobox.setCurrentIndex(0) # best
			self.DecisionTreeSplitterCombobox.setEnabled(False)
			self.DecisionTreeMinSamplesSplitEdit.setEnabled(False)
			self.DecisionTreeMinWeightedFractionLeafEdit.setEnabled(False)
			self.DecisionTreeMaxLeafNodesCombobox.setCurrentIndex(0) # None
			self.DecisionTreeMaxLeafNodesCombobox.setEnabled(False)
			if self.DecisionTreeMaxDepthCombobox.currentText().lower() == 'none':
				idx = self.DecisionTreeMaxDepthCombobox.findText('1')
				self.DecisionTreeMaxDepthCombobox.setCurrentIndex(idx)
			self.DecisionTreeNumTrialsPerSplitEdit.setEnabled(True)


	def onDecisionTreeMaxLeafNodesChanged(self, idx):
		if self.DecisionTreeMaxLeafNodesCombobox.currentText() == 'None':
			self.DecisionTreeMaxDepthCombobox.setEnabled(True)
		else:
			self.DecisionTreeMaxDepthCombobox.setEnabled(False)


	def onRandomForestAlgorithmChanged(self, idx):
		if idx == 0: # RandomForestClassifier (scikit-learn)
			self.RandomForestCriterionCombobox.setEnabled(True) 
			self.RandomForestMinSamplesSplitEdit.setEnabled(True)
			self.RandomForestMinWeightedFractionLeafEdit.setEnabled(True)
			self.RandomForestMaxLeafNodesCombobox.setEnabled(True)
			self.RandomForestNumTrialsPerSplitEdit.setEnabled(False)
		else: # Random Forest
			self.RandomForestCriterionCombobox.setCurrentIndex(1) # information gain
			self.RandomForestCriterionCombobox.setEnabled(False)
			self.RandomForestMinSamplesSplitEdit.setEnabled(False)
			self.RandomForestMinWeightedFractionLeafEdit.setEnabled(False)
			self.RandomForestMaxLeafNodesCombobox.setCurrentIndex(0) # None
			self.RandomForestMaxLeafNodesCombobox.setEnabled(False)
			if self.RandomForestMaxDepthCombobox.currentText().lower() == 'none':
				idx = self.RandomForestMaxDepthCombobox.findText('1')
				self.RandomForestMaxDepthCombobox.setCurrentIndex(idx)
			self.RandomForestNumTrialsPerSplitEdit.setEnabled(True)


	def onRandomForestMaxLeafNodesChanged(self, idx):
		if self.RandomForestMaxLeafNodesCombobox.currentText() == 'None':
			self.RandomForestMaxDepthCombobox.setEnabled(True)
		else:
			self.RandomForestMaxDepthCombobox.setEnabled(False)


	def setTab(self, tab):
		if tab >= 0:
			self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Classify")
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


	def getLogRegMaxNumIterations(self):
		return int(self.LogRegNumIterationsEdit.text())


	def getLogRegLearningRate(self):
		return float(self.LogRegLearningRateEdit.text())


	def getNormNorm(self):
		idx = self.NormNormCombobox.currentIndex()
		if idx == 0:
			return 'l1'
		elif idx == 1:
			return 'l2'
		else:
			return 'Mahalanobis'


	def getGmmNumComponentsPerClass(self):
		desc = self.GmmKEdit.text().strip()
		if len(desc) > 0 and desc[0] == '[':
			desc = desc[1:]
		if len(desc) > 0 and desc[-1] == ']':
			desc = desc[:-1]
		if len(desc) == 0:
			return list()
		desc = desc.replace(',', ' ')
		numComponents = numpy.fromstring(desc, dtype = numpy.int, sep = ' ')
		for k in numComponents:
			assert k > 0

		return numComponents


	def GmmAdjustNumComponentsPerClass(self):
		k = self.getGmmNumComponentsPerClass()
		if len(k) != self.__numClasses:
			default = str(numpy.ones(self.__numClasses, dtype = numpy.int))
			self.GmmKEdit.setText(default)
		else:
			self.GmmKEdit.setText(str(k))
			

	def getGmmMaxNumIterations(self):
		return int(self.GmmNumIterationsEdit.text())


	def getKNNAlgorithm(self):
		idx = self.KNNAlgorithmCombobox.currentIndex()
		if idx == 0:
			return 'scikit-learn'
		elif idx == 1:
			return 'own'
		else:
			return None


	def getKNNNumberOfNeighbors(self):
		return int(self.KNNNumNeighborsEdit.text())


	def getKNNWeightFunction(self):
		return self.KNNWeightsCombobox.currentText()


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


	def getPerceptronMaxNumIterations(self):
		return int(self.PerceptronNumIterationsEdit.text())


	def getPerceptronLearningRate(self):
		return float(self.PerceptronLearningRateEdit.text())


	def getPerceptronBatchMode(self):
		batchmode = self.PerceptronBatchModeCombobox.currentIndex()
		if batchmode == 0:
			return True
		else:
			return False


	def getMLPHiddenLayers(self):
		desc = self.MLPHiddenLayersEdit.text().strip()
		if len(desc) > 0 and desc[0] == '(':
			desc = desc[1:]
		if len(desc) > 0 and desc[-1] == ')':
			desc = desc[:-1]
		if len(desc) == 0:
			return list()
		desc = desc.replace(',', ' ')
		numComponents = numpy.fromstring(desc, dtype = numpy.int, sep = ' ')
		for k in numComponents:
			assert k > 0

		return numComponents


	def getMLPActivationFunction(self):
		return self.MLPActivationFunctionCombobox.currentText()


	def getMLPOptimizationAlgorithm(self):
		return self.MLPAlgorithmCombobox.currentText()


	def getMLPAlpha(self):
		return float(self.MLPAlphaEdit.text())


	def getMLPLearningRate(self):
		return self.MLPLearningRateCombobox.currentText()


	def getSVMAlgorithm(self):
		idx = self.SVMAlgorithmCombobox.currentIndex()
		if idx == 0:
			return 'LinearSVC'
		elif idx == 1:
			return 'SVC'
		elif idx == 2:
			return 'HardMarginSVM'
		elif idx == 3:
			return 'SoftMarginSVM'
		else:
			return None


	def getSVMKernel(self):
		kernel = self.SVMKernelCombobox.currentIndex()
		if kernel == 0:
			return 'linear'
		elif kernel == 1:
			return 'poly'
		elif kernel == 2:
			return 'rbf'
		else:
			return 'sigmoid'

	def getSVMC(self):
		return float(self.SVMCEdit.text())


	def getSVMGamma(self):
		return float(self.SVMGammaEdit.text())


	def getSVMCoef0(self):
		return float(self.SVMCoef0Edit.text())


	def getSVMDegree(self):
		return int(self.SVMDegreeEdit.text())


	def getDecisionTreeAlgorithm(self):
		idx = self.DecisionTreeAlgorithmCombobox.currentIndex()
		if idx == 0:
			return 'sklearn'
		elif idx == 1:
			return 'DecisionTree'
		else:
			return None


	def getDecisionTreeCriterion(self):
		criterion = self.DecisionTreeCriterionCombobox.currentIndex()
		if criterion == 0:
			return 'gini'
		else:
			return 'entropy'


	def getDecisionTreeSplitter(self):
		splitter = self.DecisionTreeSplitterCombobox.currentIndex()
		if splitter == 0:
			return 'best'
		else:
			return 'random'


	def getDecisionTreeMaxDepth(self):
		if not self.DecisionTreeMaxDepthCombobox.isEnabled():
			return None
		value = self.DecisionTreeMaxDepthCombobox.currentText()
		if value.lower() == 'none':
			return None
		return int(value)


	def getDecisionTreeMinSamplesSplit(self):
		return int(self.DecisionTreeMinSamplesSplitEdit.text())


	def getDecisionTreeMinSamplesLeaf(self):
		return int(self.DecisionTreeMinSamplesLeafEdit.text())


	def getDecisionTreeMinWeightedFractionLeaf(self):
		return float(self.DecisionTreeMinWeightedFractionLeafEdit.text())


	def getDecisionTreeMaxLeafNodes(self):
		value = self.DecisionTreeMaxLeafNodesCombobox.currentText()
		if value.lower() == 'none':
			return None
		return int(value)


	def getDecisionTreeNumTrialsPerSplit(self):
		return int(self.DecisionTreeNumTrialsPerSplitEdit.text())

		
	def getRandomForestAlgorithm(self):
		idx = self.RandomForestAlgorithmCombobox.currentIndex()
		if idx == 0:
			return 'sklearn'
		elif idx == 1:
			return 'RandomForest'
		else:
			return None


	def getRandomForestNumTrees(self):
		return int(self.RandomForestNumTreesEdit.text())


	def getRandomForestCriterion(self):
		criterion = self.RandomForestCriterionCombobox.currentIndex()
		if criterion == 0:
			return 'gini'
		else:
			return 'entropy'


	def getRandomForestMaxDepth(self):
		if not self.RandomForestMaxDepthCombobox.isEnabled():
			return None
		value = self.RandomForestMaxDepthCombobox.currentText()
		if value.lower() == 'none':
			return None
		return int(value)


	def getRandomForestMinSamplesSplit(self):
		return int(self.RandomForestMinSamplesSplitEdit.text())


	def getRandomForestMinSamplesLeaf(self):
		return int(self.RandomForestMinSamplesLeafEdit.text())


	def getRandomForestMinWeightedFractionLeaf(self):
		return float(self.RandomForestMinWeightedFractionLeafEdit.text())


	def getRandomForestMaxLeafNodes(self):
		value = self.RandomForestMaxLeafNodesCombobox.currentText()
		if value.lower() == 'none':
			return None
		return int(value)


	def getRandomForestNumTrialsPerSplit(self):
		return int(self.RandomForestNumTrialsPerSplitEdit.text())


