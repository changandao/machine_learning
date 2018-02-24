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
import numpy
from PyQt4 import QtGui
from sklearn import neighbors

from HistogramDensityEstimation import HistogramDensityEstimation
from KernelDensityEstimation import KernelDensityEstimation
from SphereDensityEstimation import SphereDensityEstimation


class DensityEstimation(object):

	Histogram = 1
	SphereDensityEstimation = 2
	KernelDensityEstimation = 3

	def __init__(self, estimator, parameters, featurespace, viewer):
		super(DensityEstimation, self).__init__()

		self.__estimator = estimator
		self.__parameters = parameters
		self.__featurespace = featurespace
		self.__viewer = viewer
		self.__est = None
		self.__colormap = cm.Greys


	def initialize(self):
		self.__samples, self.__labels = self.__featurespace.getSamples()
		if len(self.__labels) == 0:
			self.__est = None
			return

		if self.__estimator == self.Histogram:
			binsX = self.__parameters.getHistogramBinsX()
			binsY = self.__parameters.getHistogramBinsY()
			self.__colormap = self.__parameters.getHistogramColormap()
			self.__est = HistogramDensityEstimation(binsX, binsY, self.__featurespace.coordinateSystem)
			self.__est.fit(self.__samples)

		elif self.__estimator == self.SphereDensityEstimation:
			k = self.__parameters.getSphereDensityEstimationNeighbors()
			self.__colormap = self.__parameters.getSphereDensityEstimationColormap()
			self.__est = SphereDensityEstimation(k, self.__featurespace.coordinateSystem)
			self.__est.fit(self.__samples)

		elif self.__estimator == self.KernelDensityEstimation:
			algorithm = self.__parameters.getKernelDensityEstimationAlgorithm()
			kernel = self.__parameters.getKernelDensityEstimationKernel()
			bandwidth = self.__parameters.getKernelDensityEstimationBandwidth()
			self.__colormap = self.__parameters.getKernelDensityEstimationColormap()
			if algorithm == "sklearn":
				self.__est = neighbors.kde.KernelDensity(kernel = kernel, bandwidth = bandwidth)
			else:
				self.__est = KernelDensityEstimation(bandwidth) 
			self.__est.fit(self.__samples)

		else:
			print("unsupported density estimator")


	def runFeatureSpaceComputations(self):
		if self.__est:
			x_min, y_min, x_max, y_max = self.__featurespace.coordinateSystem.getLimits()
			ppuX, ppuY = self.__featurespace.coordinateSystem.getPixelsPerUnit()
		
			stepsize = 1.0 / ppuX
			# stepsize = (x_max - x_min) / 100.0
			xrange = numpy.arange(x_min, x_max, stepsize)
			w = len(xrange)
		
			stepsize = 1.0 / ppuY
			# stepsize = (y_max - y_min) / 100.0
			yrange = numpy.arange(y_max, y_min, -stepsize)
			h = len(yrange)
		
			xx, yy = numpy.meshgrid(xrange, yrange)
				
			data = numpy.c_[xx.ravel(), yy.ravel()]
		
			Z = self.__est.score_samples(data)
			
			if Z is None:
				return None

			numpy.exp(Z, Z)
						
			Z = Z.reshape((h, w))
			
			#self.__viewer.plot(xx, yy, Z)
			#self.__viewer.show()

			mapping = cm.ScalarMappable(cmap = self.__colormap) # gray, coolwarm
			rgba = mapping.to_rgba(Z, bytes = True)
			rgba = rgba.astype(numpy.int32)
			rgb = (rgba[:,:,0] << 16) + (rgba[:,:,1] << 8) + rgba[:,:,2]
			img = QtGui.QImage(rgb, w, h, QtGui.QImage.Format_RGB32)
			# img.save('test.png')

			return img
		
		else:
			return None
