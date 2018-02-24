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

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt


class ProbabilityDensityViewer(QtWidgets.QDialog):

	def __init__(self, parent = None):
		super(ProbabilityDensityViewer, self).__init__(parent)

		self.figure = plt.figure()
		self.ax = self.figure.gca(projection = '3d')
		self.canvas = FigureCanvas(self.figure)
		# self.toolbar = NavigationToolbar(self.canvas, self)

		layout = QtWidgets.QVBoxLayout()
		# layout.addWidget(self.toolbar)
		layout.addWidget(self.canvas)
		self.setLayout(layout)
		self.setWindowTitle('Probability density function')


	def plot(self, X, Y, Z):
		azimuth = self.ax.azim
		elevation = self.ax.elev

		self.figure.clear()
		self.ax = self.figure.gca(projection = '3d')
		self.ax.view_init(elevation, azimuth)
			
		surface = self.ax.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap = cm.coolwarm, linewidth = 0, antialiased = False)
		# ax.set_zlim(-1.01, 1.01)
		self.ax.zaxis.set_major_locator(LinearLocator(10))
		self.ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
		self.figure.colorbar(surface, shrink = 0.5, aspect = 5)

		self.canvas.draw()
		# self.figure.savefig('probabilitymap.png')
			


