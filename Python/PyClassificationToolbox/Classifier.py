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
import sklearn
from sklearn import ensemble, neighbors, neural_network, svm, tree #, naive_bayes
from PyQt4 import QtGui

from DecisionTree import DecisionTree
from GaussianClassifier import GaussianClassifier
from GMMClassifier import GMMClassifier
from HardMarginSVM import HardMarginSVM
from kNearestNeighbor import kNearestNeighbor
from KernelSVM import KernelSVM
from LinearRegression import LinearRegression
from MyColors import MyColors
from NearestNeighbor import NearestNeighbor
from NormClassifier import NormClassifier
import Parameters
from Perceptron import Perceptron
from RandomForest import RandomForest
from SoftMarginSVM import SoftMarginSVM
from LinearLogisticRegression import LinearLogisticRegression


class Classifier(object):

	# classifiers with parameters
	LogReg = 1
	Norm = 2
	GMM = 3 
	kNN = 4
	LinReg = 5
	Perceptron = 6
	MLP = 7
	SVM = 8
	DecisionTree = 9
	RandomForest = 10
	
	# classifiers without parameters
	NaiveBayes = 100
	Gauss = 101
	
	
	def __init__(self, classifier, parameters, featurespace):
		super(Classifier, self).__init__()
		
		self.__classifier = classifier
		self.__parameters = parameters
		self.__featurespace = featurespace
		self.__clf = None


	def copy(self):
		return Classifier(self.__classifier, self.__parameters, self.__featurespace)


	def initialize(self):
		self.__samples, self.__labels = self.__featurespace.getSamples()
		if len(self.__labels) == 0:
			self.__clf = None
			return

		if self.__classifier == self.LogReg:
			maxIter = self.__parameters.getLogRegMaxNumIterations()
			learningRate = self.__parameters.getLogRegLearningRate()
			self.__clf = LinearLogisticRegression(learningRate = learningRate, maxIterations = maxIter)
			self.__clf.fit(self.__samples, self.__labels)

		elif self.__classifier == self.Norm:
			norm = self.__parameters.getNormNorm()
			self.__clf = NormClassifier(norm)
			self.__clf.fit(self.__samples, self.__labels)		

		elif self.__classifier == self.NaiveBayes:
#			self.__clf = naive_bayes.GaussianNB()
#			self.__clf.fit(self.__samples, self.__labels)
			self.__clf = GaussianClassifier(samplesIndependent = True)
			self.__clf.fit(self.__samples, self.__labels)

		elif self.__classifier == self.Gauss:
			self.__clf = GaussianClassifier(samplesIndependent = False)
			self.__clf.fit(self.__samples, self.__labels)

		elif self.__classifier == self.GMM:
			numComponents = self.__parameters.getGmmNumComponentsPerClass()
			maxIterations = self.__parameters.getGmmMaxNumIterations()
			self.__clf = GMMClassifier(numComponents, maxIterations)
			self.__clf.fit(self.__samples, self.__labels)
							
		elif self.__classifier == self.kNN:
			algo = self.__parameters.getKNNAlgorithm()
			k = self.__parameters.getKNNNumberOfNeighbors()
			w = self.__parameters.getKNNWeightFunction()
			if algo == 'scikit-learn':				
				self.__clf = neighbors.KNeighborsClassifier(k, weights=w)
			else: # 'own'
				if k == 1:
					self.__clf = NearestNeighbor()
				else:
					self.__clf = kNearestNeighbor(k)
			self.__clf.fit(self.__samples, self.__labels)

		elif self.__classifier == self.LinReg:
			lossFunc = self.__parameters.getLinRegLossFunction()
			a = self.__parameters.getLinRegLossFunctionParam()
			self.__clf = LinearRegression(lossFunc, a, True)
			self.__clf.fit(self.__samples, self.__labels)
			
		elif self.__classifier == self.Perceptron:
			maxIter = self.__parameters.getPerceptronMaxNumIterations()
			learningRate = self.__parameters.getPerceptronLearningRate()
			batchMode = self.__parameters.getPerceptronBatchMode()
			self.__clf = Perceptron(batchMode = batchMode, learningRate = learningRate, maxIterations = maxIter)
			self.__clf.fit(self.__samples, self.__labels)

		elif self.__classifier == self.MLP:
			layers = self.__parameters.getMLPHiddenLayers()
			act = self.__parameters.getMLPActivationFunction()
			algo = self.__parameters.getMLPOptimizationAlgorithm()
			alpha = self.__parameters.getMLPAlpha()
			rate = self.__parameters.getMLPLearningRate()
			self.__clf = sklearn.neural_network.MLPClassifier(hidden_layer_sizes = layers, activation = act, algorithm = algo, alpha = alpha, learning_rate = rate)
			self.__clf.fit(self.__samples, self.__labels)

		elif self.__classifier == self.SVM:
			algorithm = self.__parameters.getSVMAlgorithm()
			kernel = self.__parameters.getSVMKernel()
			C = self.__parameters.getSVMC()
			gamma = self.__parameters.getSVMGamma()
			coef0 = self.__parameters.getSVMCoef0()
			degree = self.__parameters.getSVMDegree()
			if algorithm == 'LinearSVC':
				self.__clf = svm.LinearSVC(C = C)
			elif algorithm == 'SVC':
				self.__clf = svm.SVC(kernel = kernel, C = C, gamma = gamma, coef0 = coef0, degree = degree)
			elif algorithm == 'HardMarginSVM':
				self.__clf = HardMarginSVM()
			elif algorithm == 'SoftMarginSVM':
				self.__clf = SoftMarginSVM(C = C)
			else:
				self.__clf = KernelSVM(C = C, gamma = gamma)
			self.__clf.fit(self.__samples, self.__labels)

		elif self.__classifier == self.DecisionTree:
			algorithm = self.__parameters.getDecisionTreeAlgorithm()
			criterion = self.__parameters.getDecisionTreeCriterion()
			splitter = self.__parameters.getDecisionTreeSplitter()
			maxDepth = self.__parameters.getDecisionTreeMaxDepth()
			minSamplesSplit = self.__parameters.getDecisionTreeMinSamplesSplit()
			minSamplesLeaf = self.__parameters.getDecisionTreeMinSamplesLeaf()
			minWeightedFractionLeaf = self.__parameters.getDecisionTreeMinWeightedFractionLeaf()
			maxLeafNodes = self.__parameters.getDecisionTreeMaxLeafNodes()
			trials = self.__parameters.getDecisionTreeNumTrialsPerSplit()
			if algorithm == 'sklearn':
				self.__clf = tree.DecisionTreeClassifier(criterion = criterion, 
														splitter = splitter, 
														max_features = 2, 
														max_depth = maxDepth, 
														min_samples_split = minSamplesSplit,
														min_samples_leaf = minSamplesLeaf,
														min_weight_fraction_leaf = minWeightedFractionLeaf,
														max_leaf_nodes = maxLeafNodes)
			else:
				self.__clf = DecisionTree(maxDepth, minSamplesLeaf, trials)
			self.__clf.fit(self.__samples, self.__labels)

		elif self.__classifier == self.RandomForest:
			algorithm = self.__parameters.getRandomForestAlgorithm()
			numTrees = self.__parameters.getRandomForestNumTrees()
			criterion = self.__parameters.getRandomForestCriterion()
			maxDepth = self.__parameters.getRandomForestMaxDepth()
			minSamplesSplit = self.__parameters.getRandomForestMinSamplesSplit()
			minSamplesLeaf = self.__parameters.getRandomForestMinSamplesLeaf()
			minWeightedFractionLeaf = self.__parameters.getRandomForestMinWeightedFractionLeaf()
			maxLeafNodes = self.__parameters.getRandomForestMaxLeafNodes()
			trials = self.__parameters.getRandomForestNumTrialsPerSplit()
			# print('Num trees: {0}'.format(numTrees))
			# print('Max depth: {0}'.format(maxDepth))
			# print('Min samples split: {0}'.format(minSamplesSplit))
			# print('Min samples leaf: {0}'.format(minSamplesLeaf))
			# print('Min weighted fraction leaf: {0}'.format(minWeightedFractionLeaf))
			# print('Max leaf nodes: {0}'.format(maxLeafNodes))
			# print('Num trials per node: {0}'.format(trials))
			if algorithm == 'sklearn':
				self.__clf = ensemble.RandomForestClassifier(n_estimators = numTrees, 
															criterion = criterion, 
															max_features = 2, 
															max_depth = maxDepth,
															min_samples_split = minSamplesSplit,
															min_samples_leaf = minSamplesLeaf,
															min_weight_fraction_leaf = minWeightedFractionLeaf,
															max_leaf_nodes = maxLeafNodes)
			else:
				self.__clf = RandomForest(numTrees, maxDepth, minSamplesLeaf, trials)
			self.__clf.fit(self.__samples, self.__labels)
			
			
		else:
			print("unsupported classifier")


	def runFeatureSpaceComputations(self):
		if self.__clf:
			x_min, y_min, x_max, y_max = self.__featurespace.coordinateSystem.getLimits()
			ppuX, ppuY = self.__featurespace.coordinateSystem.getPixelsPerUnit()
		
			stepsize = 1.0 / ppuX
			xrange = numpy.arange(x_min, x_max, stepsize)
			w = len(xrange)
		
			stepsize = 1.0 / ppuY
			yrange = numpy.arange(y_max, y_min, -stepsize)
			h = len(yrange)
		
			xx, yy = numpy.meshgrid(xrange, yrange)
				
			data = numpy.c_[xx.ravel(), yy.ravel()]
		
			Z = self.__clf.predict(data)
			
			if Z is None:
				return None
		
			Z = Z.astype(numpy.int64)
			for k in range(Parameters.NUMBER_SUPPORTED_CLASSES):
				col, _, _ = MyColors.rgbForClass(k)
				Z = numpy.where(Z == k, col, Z)
			Z = Z.astype(numpy.int32)
		
			img = QtGui.QImage(Z, w, h, QtGui.QImage.Format_RGB32)
			# img.save('test.png')
		
			return img
		
		else:
			return None
		
		
