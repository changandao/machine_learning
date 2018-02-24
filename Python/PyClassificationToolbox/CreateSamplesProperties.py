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

import Parameters


class CreateSamplesProperties(QtWidgets.QDockWidget):
    
    def __init__(self, parent):
        super(CreateSamplesProperties, self).__init__(parent)
        
        self.__parent = parent
        
        self.classComboBox = QtWidgets.QComboBox()
        for i in range(Parameters.NUMBER_SUPPORTED_CLASSES):
            self.classComboBox.addItem('Class {0}'.format(i + 1))
        
        self.assignButton = QtWidgets.QPushButton('Assign class label')
        self.assignButton.setEnabled(False)
        self.assignButton.clicked.connect(self.onAssignClassLabel)
        
        self.deleteButton = QtWidgets.QPushButton('Delete samples')
        self.deleteButton.setEnabled(False)
        self.deleteButton.clicked.connect(self.onDeleteSamples)
               
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.addWidget(self.classComboBox)
        layout.addWidget(self.assignButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch(1)
        
        widget = QtWidgets.QWidget()        
        widget.setLayout(layout)
        
        self.setWidget(widget)
        self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.setTitleBarWidget(QtWidgets.QWidget(self));
        self.setHidden(True)        


    def getProperties(self):
        return (self.classComboBox.currentIndex())


    def onDeleteSamples(self):
        self.__parent.featurespace.samples.deleteSamplesInSelectedArea()


    def onAssignClassLabel(self):
        self.__parent.featurespace.samples.assignNewClassLabelInSelectedArea(self.classComboBox.currentIndex())


