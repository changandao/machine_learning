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


import PyQt4.QtGui as QtWidgets

from GaussianMixtureModel import GaussianMixtureModel
from KMeansClustering import KMeansClustering
import Parameters

class Clustering(object):
	
	kMeans = 1
	GMM = 2


	def __init__(self, method, parameters, featurespace):
		super(Clustering, self).__init__()
		
		self.__method = method
		self.__parameters = parameters
		self.__featurespace = featurespace
		self.__clt = None


	def initialize(self):
		NoG = self.__featurespace.getNumberOfGaussians()
		if NoG > 0:
			QtWidgets.QMessageBox.warning(self.__featurespace, 'Error',
				'Samples from a Gaussian distribution all share the same class label. ' +
				'The k-means clustering assigns individual labels to all samples and thus cannot be applied to Gaussians. ' +
				'Convert Gaussians to individual samples first.',
				QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)	
			return
		
		NoC = self.__featurespace.getNumberOfClasses()
		if NoC > 1:
			reply = QtWidgets.QMessageBox.question(self.__featurespace, 'Confirmation',
				'The samples are from different classes. ' +
				'The k-means clustering will assign new class labels. ' +
				'Do you want to continue?', 
				QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
				QtWidgets.QMessageBox.No)

			if reply == QtWidgets.QMessageBox.No:
				return

		
		self.__samples, self.__labels = self.__featurespace.getSamples()
		if len(self.__labels) == 0:
			self.__clf = None
			return
		
		if self.__method == self.kMeans:
			k = self.__parameters.getKMeansK()
			self.__clt = KMeansClustering(k) 
			Z = self.__clt.fit(self.__samples)
			Z *= int(Parameters.NUMBER_SUPPORTED_CLASSES / k)
			self.__featurespace.setLabels(Z)
		elif self.__method == self.GMM:
			k = self.__parameters.getGmmK()
			maxNumIterations = self.__parameters.getGmmMaxNumIterations()
			self.__clt = GaussianMixtureModel(k, maxNumIterations)
			self.__clt.fit(self.__samples)
			Z = self.__clt.getComponents(self.__samples)
			Z *= int(Parameters.NUMBER_SUPPORTED_CLASSES / k)
			self.__featurespace.setLabels(Z)			
		else:
			print("Unsupported clustering method")

