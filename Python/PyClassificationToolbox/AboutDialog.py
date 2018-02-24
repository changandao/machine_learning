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


class AboutDialog(QtWidgets.QDialog):

    def __init__(self, parent, licenseDialog):
        super(AboutDialog, self).__init__(parent)
        
        self.licenseDialog = licenseDialog
        
        pixmap = QtGui.QPixmap(resource_path('./img/about.png'))
        img = QtWidgets.QLabel(self)
        img.setPixmap(pixmap)
        
        self.info = QtWidgets.QTextBrowser(self)
        self.info.setReadOnly(True)
        self.info.setFixedWidth(560)
        self.info.setFixedHeight(192)
        self.info.setHtml('<h3>Python Classification Toolbox</h3>' +
                     '<font color="#909090"><i>Study popular machine learning algorithms and create your own implementations in Python for a deeper understanding of the algorithms!</i></font><br><br>'
                     'Copyright &copy; 2016 Stefan Steidl<br>' +
                     'Pattern Recognition Lab<br>' +
                     'Computer Science Department 5<br>'+
                     'Friedrich-Alexander University Erlangen-Nuremberg<br>' +
                     '<a href="mailto:steidl@cs.fau.de">steidl@cs.fau.de</a><br><br>' +
                     'This program comes with ABSOLUTELY NO WARRANTY; for details click <a href="func://warranty">here</a>. ' + 
                     'This is free software, and you are welcome to redistribute it ' +
                     'under certain conditions; click <a href="func://gpl">here</a> for details.'
                     )
        self.info.anchorClicked.connect(self.onInfoClicked)
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(img)
        layout.addWidget(self.info)
        layout.addStretch(1)
        
        box = QtWidgets.QWidget()
        box.setLayout(layout)
        
        # OK button
        self.button = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        self.button.accepted.connect(self.accept)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(box)
        layout.addStretch(1)
        layout.addWidget(self.button)
        layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        
        self.setWindowTitle('About...')


    def onInfoClicked(self, url):
        self.info.setSource(QtCore.QUrl())
        text = str(url.toString())
        if text == "func://gpl":
            self.licenseDialog.showLicense()
        elif text == "func://warranty":
            self.licenseDialog.showWarranty()
            


