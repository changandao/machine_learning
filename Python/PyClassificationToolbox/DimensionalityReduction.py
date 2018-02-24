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

from PrincipalComponentAnalysis import PrincipalComponentAnalysis


class DimensionalityReduction(object):
	
	PCA = 1
	
	
	def __init__(self, method, parameters, featurespace):
		super(DimensionalityReduction, self).__init__()
		
		self.__method = method
		self.__parameters = parameters
		self.__featurespace = featurespace
		self.__dimred = None


	def initialize(self):
		NoG = self.__featurespace.getNumberOfGaussians()
		if NoG > 0:
			QtWidgets.QMessageBox.warning(self.__featurespace, 'Error',
				'These techniques change the coordinates of the samples. ' +
				'Convert Gaussians to individual samples first.',
				QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)	
			return		
		
		self.__samples, self.__labels = self.__featurespace.getSamples()
		if len(self.__labels) == 0:
			self.__dimred = None
			return
		
		if self.__method == self.PCA:
			dimReduction = self.__parameters.getPCARedDim()
			secondComponent = self.__parameters.getPCASecondComponent()
			backprojection = self.__parameters.getPCABackproject()
			
			self.__dimred = PrincipalComponentAnalysis(dimReduction, secondComponent, backprojection)
			Z = self.__dimred.fit(self.__samples)
			self.__featurespace.setSamples(Z)
			
		else:
			print("Unsupported dimensionality reduction method")

