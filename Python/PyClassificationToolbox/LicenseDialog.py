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
	
	
from PyQt4 import QtCore, QtGui
import PyQt4.QtGui as QtWidgets

from Parameters import resource_path


class LicenseDialog(QtWidgets.QDialog):

	def __init__(self, parent):
		super(LicenseDialog, self).__init__(parent)
		
		self.info = QtWidgets.QTextBrowser(self)
		self.info.setReadOnly(True)
		self.info.setOpenLinks(False)
		self.info.setOpenExternalLinks(False)
		
		# text = open(resource_path('./GPLv3.html')).read()
		# self.info.setHtml(text)
		self.info.setSource(QtCore.QUrl.fromLocalFile(resource_path('GPLv3.html')))

		# OK button
		self.button = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
		self.button.accepted.connect(self.accept)

		layout = QtWidgets.QVBoxLayout(self)
		layout.addWidget(self.info)
		#layout.addStretch(1)
		layout.addWidget(self.button)
		
		self.setWindowTitle('GNU General Public License...')
		self.resize(500, 600)


	def showLicense(self):
		url = QtCore.QUrl.fromLocalFile(resource_path('GPLv3.html'))
		self.info.setSource(url)
		self.exec_()


	def showWarranty(self):
		# three backslashes needed for Windows
		url = QtCore.QUrl("file:///" + resource_path('GPLv3.html') + "#section15")		
		self.info.setSource(url)
		self.exec_()

