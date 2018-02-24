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


import cvxopt.info
import locale
import matplotlib
import numpy
import scipy
import sip
import sklearn
from PyQt4 import Qt, QtCore, QtGui
import PyQt4.QtGui as QtWidgets
import platform

import version


class InfoDialog(QtWidgets.QDialog):

	def __init__(self, parent):
		super(InfoDialog, self).__init__(parent)

		colWidth = 150
		grid0 = QtWidgets.QGridLayout()
		grid0.setSpacing(10)
		grid0.setColumnMinimumWidth(0, colWidth)
		i = 0
		saved = locale.setlocale(locale.LC_ALL)
		locale.setlocale(locale.LC_ALL, 'C')
		s = "{0:04d},  {1}".format(version.__build__, version.__versiondate__.strftime('%B %d, %Y'))		
		locale.setlocale(locale.LC_ALL, saved)
		grid0.addWidget(QtWidgets.QLabel('Build'), i, 0)
		grid0.addWidget(QtWidgets.QLabel(s), i, 1)
		
		box0 = QtWidgets.QGroupBox()
		box0.setTitle('Python Classification Toolbox')
		box0.setLayout(grid0)
		
		grid1 = QtWidgets.QGridLayout();
		grid1.setSpacing(10)
		grid1.setColumnMinimumWidth(0, colWidth)
		i = 0
		grid1.addWidget(QtWidgets.QLabel('Qt'), i, 0)
		grid1.addWidget(QtWidgets.QLabel(QtCore.QT_VERSION_STR), i, 1)
		i += 1		
		grid1.addWidget(QtWidgets.QLabel('SIP'), i, 0)
		grid1.addWidget(QtWidgets.QLabel(sip.SIP_VERSION_STR), i, 1)
		i += 1
		grid1.addWidget(QtWidgets.QLabel('Python'), i, 0)
		grid1.addWidget(QtWidgets.QLabel(platform.python_version()), i, 1)
		
		box1 = QtWidgets.QGroupBox()
		box1.setTitle('Software')
		box1.setLayout(grid1)

		grid2 = QtWidgets.QGridLayout();
		grid2.setSpacing(10)
		grid2.setColumnMinimumWidth(0, colWidth)
		i = 0
		grid2.addWidget(QtWidgets.QLabel('cvxopt'), i, 0)
		grid2.addWidget(QtWidgets.QLabel(cvxopt.info.version), i, 1)
		i += 1
		grid2.addWidget(QtWidgets.QLabel('Matplotlib'), i, 0)
		grid2.addWidget(QtWidgets.QLabel(matplotlib.__version__), i, 1)
		i += 1
		grid2.addWidget(QtWidgets.QLabel('NumPy'), i, 0)
		grid2.addWidget(QtWidgets.QLabel(numpy.__version__), i, 1)
		i += 1		
		grid2.addWidget(QtWidgets.QLabel('PyQt4'), i, 0)
		grid2.addWidget(QtWidgets.QLabel(Qt.PYQT_VERSION_STR), i, 1)
		i += 1
		grid2.addWidget(QtWidgets.QLabel('scikit-learn'), i, 0)
		grid2.addWidget(QtWidgets.QLabel(sklearn.__version__), i, 1)
		i += 1
		grid2.addWidget(QtWidgets.QLabel('SciPy'), i, 0)
		grid2.addWidget(QtWidgets.QLabel(scipy.__version__), i, 1)
		i += 1
		
		box2 = QtWidgets.QGroupBox()
		box2.setTitle('Python packages')
		box2.setLayout(grid2)

		# OK button
		button = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok, QtCore.Qt.Horizontal)
		button.accepted.connect(self.accept)

		frame = QtWidgets.QVBoxLayout(self)
		frame.addWidget(box0)
		frame.addWidget(box1)
		frame.addWidget(box2)
		frame.addStretch(1)
		frame.addWidget(button)
		frame.setSizeConstraint(QtGui.QLayout.SetFixedSize)
		
		self.setWindowTitle('Version info...')

