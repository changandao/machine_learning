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
from sklearn import ensemble, svm, tree

from RegressionForest import RegressionForest
from RegressionTree import RegressionTree
from LinearRegression import LinearRegression


class Regression(object):

	LinearRegression = 1
	SVR = 2
	RegressionTree = 3
	RegressionForest = 4


	def __init__(self, regressor, parameters, featurespace):
		return None



	def initialize(self):
		self.__samples, self.__labels = self.__featurespace.getSamples()
		if len(self.__labels) == 0:
			self.__reg = None
			return
		
		if self.__regressor == self.LinearRegression:
			lossFunc = self.__parameters.getLinRegLossFunction()
			a = self.__parameters.getLinRegLossFunctionParam()
			self.__reg = LinearRegression(lossFunc, a)
			self.__reg.fit(self.__samples[:,0], self.__samples[:,1])

		elif self.__regressor == self.SVR:
			_ = self.__parameters.getSVRAlgorithm() # there's just one algorithm right now
			kernel = self.__parameters.getSVRKernel()
			C = self.__parameters.getSVRC()
			epsilon = self.__parameters.getSVREpsilon()
			gamma = self.__parameters.getSVRGamma()
			coef0 = self.__parameters.getSVRCoef0()
			degree = self.__parameters.getSVRDegree()
			self.__reg = svm.SVR(kernel = kernel, degree = degree, gamma = gamma, coef0 = coef0, C = C, epsilon = epsilon)
			self.__reg.fit(self.__samples[:,0].reshape(-1,1), self.__samples[:,1])

		elif self.__regressor == self.RegressionTree:
			algorithm = self.__parameters.getRegressionTreeAlgorithm()
			_ = self.__parameters.getRegressionTreeCriterion() # currently there's just one quality criterion implemented
			splitter = self.__parameters.getRegressionTreeSplitter()
			maxDepth = self.__parameters.getRegressionTreeMaxDepth()
			minSamplesSplit = self.__parameters.getRegressionTreeMinSamplesSplit()
			minSamplesLeaf = self.__parameters.getRegressionTreeMinSamplesLeaf()
			minWeightedFractionLeaf = self.__parameters.getRegressionTreeMinWeightedFractionLeaf()
			maxLeafNodes = self.__parameters.getRegressionTreeMaxLeafNodes()
			trials = self.__parameters.getRegressionTreeNumTrialsPerSplit()
			# print('Max depth: {0}'.format(maxDepth))
			# print('Min samples split: {0}'.format(minSamplesSplit))
			# print('Min samples leaf: {0}'.format(minSamplesLeaf))
			# print('Min weighted fraction leaf: {0}'.format(minWeightedFractionLeaf))
			# print('Max leaf nodes: {0}'.format(maxLeafNodes))
			# print('Num trials per split: {0}'.format(trials))
			if algorithm == 'sklearn':
				self.__reg = tree.DecisionTreeRegressor(splitter = splitter, 
													max_features = 1, 
													max_depth = maxDepth, 
													min_samples_split = minSamplesSplit, 
													min_samples_leaf = minSamplesLeaf,
													min_weight_fraction_leaf = minWeightedFractionLeaf, 
													max_leaf_nodes = maxLeafNodes)
			else:
				self.__reg = RegressionTree(maxDepth, minSamplesLeaf, trials)
			self.__reg.fit(self.__samples[:,0].reshape(-1,1), self.__samples[:,1])

		elif self.__regressor == self.RegressionForest:
			algorithm = self.__parameters.getRegressionForestAlgorithm()
			numTrees = self.__parameters.getRegressionForestNumTrees()
			_ = self.__parameters.getRegressionForestCriterion() # currently there's just one quality criterion implemented
			maxDepth = self.__parameters.getRegressionForestMaxDepth()
			minSamplesSplit = self.__parameters.getRegressionForestMinSamplesSplit()
			minSamplesLeaf = self.__parameters.getRegressionForestMinSamplesLeaf()
			minWeightedFractionLeaf = self.__parameters.getRegressionForestMinWeightedFractionLeaf()
			maxLeafNodes = self.__parameters.getRegressionForestMaxLeafNodes()
			trials = self.__parameters.getRegressionForestNumTrialsPerSplit()
			if algorithm == 'sklearn':
				self.__reg = ensemble.RandomForestRegressor(n_estimators = numTrees, 
														max_features = 1, 
														max_depth = maxDepth, 
														min_samples_split = minSamplesSplit, 
														min_samples_leaf = minSamplesLeaf,
														min_weight_fraction_leaf = minWeightedFractionLeaf, 
														max_leaf_nodes = maxLeafNodes)
			else:
				self.__reg = RegressionForest(numTrees, maxDepth, minSamplesLeaf, trials)
			self.__reg.fit(self.__samples[:,0].reshape(-1,1), self.__samples[:,1])
			
				
		else:
			print("unsupported regressor")


	def paint(self, qp):
		if self.__reg:
			qp.setPen(self.__pen)
			if self.__regressor == self.LinearRegression:
				self.__reg.paint(qp, self.__featurespace)
			elif (self.__regressor == self.SVR) or (self.__regressor == self.RegressionTree) or (self.__regressor == self.RegressionForest):
				x_min, _, x_max, _ = self.__featurespace.coordinateSystem.getLimits()
				ppuX, _ = self.__featurespace.coordinateSystem.getPixelsPerUnit()

				stepsize = 1.0 / ppuX
				X = numpy.arange(x_min, x_max, stepsize).reshape(-1, 1)

				Z = self.__reg.predict(X)

				points = list()
				for x, y in zip(X[:,0], Z):
					x, y = self.__featurespace.coordinateSystem.world2screen(x, y)
					points.append(QtCore.QPoint(x, y))

				polygon = QtGui.QPolygon(points)
				qp.drawPolyline(polygon)


