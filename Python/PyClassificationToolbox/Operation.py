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


class Operation(object):

	def __init__(self, featurespace, operation, args):
		self.featurespace = featurespace
		self.operation = operation
		self.args = args


	def undo(self):
		if self.operation == "CoordinateSystem.move":
			(dx, dy) = self.args
			self.featurespace.coordinateSystem.move(-dx, -dy)
		elif self.operation == "Samples2D.setSamples":
			(_, samplesOld) = self.args
			self.featurespace.samples.setSamples(samplesOld)
			self.featurespace.repaint()
		elif self.operation == "Samples2D.setLabels":
			(_, labelsOld) = self.args
			self.featurespace.samples.setLabels(labelsOld)
			self.featurespace.repaint()
		elif self.operation == "Samples2D.addNewSample":
			self.featurespace.samples.removeNewSamples(1)
		elif self.operation == "Samples2D.deleteSamples":
			(removedSamples, indices, area) = self.args
			self.featurespace.samples.insertSamples(removedSamples, indices, area)
		elif self.operation == "Samples2D.assignClassLabel":
			(updateList, _, oldLabels, area) = self.args
			self.featurespace.samples.assignNewClassLabel(updateList, oldLabels, area)
		elif self.operation == "Samples2D.moveSamples":
			(updateList, dx, dy, _, oldArea) = self.args
			self.featurespace.samples.moveSamples(updateList, -dx, -dy, oldArea)
		elif self.operation == "FeatureSpace.createGaussian":
			(gaussianId) = self.args
			self.featurespace.deleteGaussian(gaussianId, confirmation = False)
		elif self.operation == "FeatureSpace.deleteGaussian":
			(gaussianId) = self.args
			self.featurespace.undeleteGaussian(gaussianId)
		elif self.operation == "FeatureSpace.convertGaussian":
			(gaussianId, n) = self.args
			self.featurespace.undeleteGaussian(gaussianId)
			self.featurespace.samples.removeNewSamples(n)
		elif self.operation == "FeatureSpace.importFile":
			(samples) = self.args
			_, n = samples.shape
			self.featurespace.samples.removeNewSamples(n)
		elif self.operation == "Gaussian2D.editProperties":
			(gaussianId, _, oldParams) = self.args
			gaussian = self.featurespace.getGaussian(gaussianId)
			(classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded) = oldParams
			gaussian.setProperties(classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded)
			self.featurespace.repaint()
		elif self.operation == "Gaussian2D.setClassId":
			(gaussianId, _, oldClassId) = self.args
			gaussian = self.featurespace.getGaussian(gaussianId)
			gaussian.setClassId(oldClassId, undoOperation = True)
		elif self.operation == "Gaussian2D.toggleExclusion":
			(gaussianId) = self.args
			gaussian = self.featurespace.getGaussian(gaussianId)
			gaussian.toggleExclusion(undoOperation = True)
			self.featurespace.repaint()
		elif self.operation == "Gaussian2D.setMean":
			(gaussianId, _, oldParams) = self.args
			(ex, ey) = oldParams
			gaussian = self.featurespace.getGaussian(gaussianId)
			gaussian.setMean(ex, ey)
			self.featurespace.repaint()
		elif self.operation == "Gaussian2D.setSigma":
			(gaussianId, dim, _, oldSigma) = self.args
			gaussian = self.featurespace.getGaussian(gaussianId)
			gaussian.setSigma(dim, oldSigma)
			self.featurespace.repaint()
		elif self.operation == "Gaussian2D.setCov12":
			(gaussianId, _, oldCov12) = self.args
			gaussian = self.featurespace.getGaussian(gaussianId)
			gaussian.setCov12(oldCov12)
			self.featurespace.repaint()
		elif self.operation == "dummy":
			pass
		else:
			print("error: unknown operation '{0}' cannot be undone".format(self.operation))


	def redo(self):
		if self.operation == "CoordinateSystem.move":
			(dx, dy) = self.args
			self.featurespace.coordinateSystem.move(dx, dy)
		elif self.operation == "Samples2D.setSamples":
			(samplesNew, _) = self.args
			self.featurespace.samples.setSamples(samplesNew)
			self.featurespace.repaint()
		elif self.operation == "Samples2D.setLabels":
			(labelsNew, _) = self.args
			self.featurespace.samples.setLabels(labelsNew)
			self.featurespace.repaint()
		elif self.operation == "Samples2D.addNewSample":
			newSample = self.args
			self.featurespace.samples.appendNewSample(newSample)
			self.featurespace.repaint()
		elif self.operation == "Samples2D.deleteSamples":
			(_, removeList, _) = self.args
			self.featurespace.samples.deleteSamples(removeList)
		elif self.operation == "Samples2D.assignClassLabel":
			(updateList, newLabel, _, area) = self.args
			self.featurespace.samples.assignNewClassLabel(updateList, newLabel, area)
		elif self.operation == "Samples2D.moveSamples":
			(updateList, dx, dy, newArea, _) = self.args
			self.featurespace.samples.moveSamples(updateList, dx, dy, newArea)
		elif self.operation == "FeatureSpace.createGaussian":
			(gaussianId) = self.args
			self.featurespace.undeleteGaussian(gaussianId)
		elif self.operation == "FeatureSpace.deleteGaussian":
			(gaussianId) = self.args
			self.featurespace.deleteGaussian(gaussianId, confirmation = False)
		elif self.operation == "FeatureSpace.convertGaussian":
			(gaussianId, _) = self.args
			self.featurespace.convertGaussian(gaussianId, redoOperation = True)
		elif self.operation == "FeatureSpace.importFile":
			(samples) = self.args
			self.featurespace.samples.addNewSamples(samples)
		elif self.operation == "Gaussian2D.editProperties":
			(gaussianId, newParams, _) = self.args
			gaussian = self.featurespace.getGaussian(gaussianId)
			(classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded) = newParams
			gaussian.setProperties(classId, numSamples, mean1, mean2, cov11, cov22, cov12, isIncluded)
			self.featurespace.repaint()
		elif self.operation == "Gaussian2D.setClassId":
			(gaussianId, newClassId, _) = self.args
			gaussian = self.featurespace.getGaussian(gaussianId)
			gaussian.setClassId(newClassId, undoOperation = True)
		elif self.operation == "Gaussian2D.toggleExclusion":
			(gaussianId) = self.args
			gaussian = self.featurespace.getGaussian(gaussianId)
			gaussian.toggleExclusion(undoOperation = True)
			self.featurespace.repaint()
		elif self.operation == "Gaussian2D.setMean":
			(gaussianId, newParams, _) = self.args
			(ex, ey) = newParams
			gaussian = self.featurespace.getGaussian(gaussianId)
			gaussian.setMean(ex, ey)
			self.featurespace.repaint()
		elif self.operation == "Gaussian2D.setSigma":
			(gaussianId, dim, newSigma, _) = self.args
			gaussian = self.featurespace.getGaussian(gaussianId)
			gaussian.setSigma(dim, newSigma)
			self.featurespace.repaint()
		elif self.operation == "Gaussian2D.setCov12":
			(gaussianId, newCov12, _) = self.args
			gaussian = self.featurespace.getGaussian(gaussianId)
			gaussian.setCov12(newCov12)
			self.featurespace.repaint()
		elif self.operation == "dummy":
			pass
		else:
			print("error: unknown operation '{0}' cannot be redone".format(self.operation))



