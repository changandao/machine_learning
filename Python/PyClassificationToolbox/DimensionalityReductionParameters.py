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


from PyQt4 import QtCore
import PyQt4.QtGui as QtWidgets


class DimensionalityReductionParameters(QtWidgets.QDialog):

    def __init__(self, parent):
        super(DimensionalityReductionParameters, self).__init__(parent)
        
        self.__parent = parent
        self.__currentTab = 0
        
        # PCA tab
        self.PCARedDimCheckbox = QtWidgets.QCheckBox('Reduce dimensionality to 1')
        self.PCARedDimCheckbox.stateChanged.connect(self.onPCARedDimChanged)
        self.PCASecondComponentCheckbox = QtWidgets.QCheckBox('Select second component')
        self.PCABackprojectCheckbox = QtWidgets.QCheckBox('Backproject into 2-D')
        self.PCABackprojectCheckbox.setEnabled(False)
        
        PCAGrid = QtWidgets.QGridLayout();
        PCAGrid.setSpacing(10)
        PCAGrid.addWidget(self.PCARedDimCheckbox, 0, 0)
        PCAGrid.addWidget(self.PCASecondComponentCheckbox, 1, 0)
        PCAGrid.addWidget(self.PCABackprojectCheckbox, 2, 0)
        
        PCAFrame = QtWidgets.QGroupBox()
        PCAFrame.setTitle('Principal Component Analysis')        
        PCAFrame.setLayout(PCAGrid)
        
        PCALayout = QtWidgets.QVBoxLayout()
        PCALayout.addWidget(PCAFrame)
        PCALayout.addStretch(1)
        
        self.PCATab = QtWidgets.QWidget()
        self.PCATab.setLayout(PCALayout)
        
        # Create notebook tabs        
        self.notebook = QtWidgets.QTabWidget()
        self.notebook.addTab(self.PCATab, "PCA")
        self.notebook.currentChanged.connect(self.onTabChanged)
        
        
        # OK and Cancel buttons
        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.button(QtWidgets.QDialogButtonBox.Cancel).setText("Cancel")
        self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Apply")

        self.buttons.accepted.connect(self.onAccept)
        self.buttons.rejected.connect(self.onReject)


        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.notebook)        
        layout.addWidget(self.buttons)
        
        self.setWindowTitle('Dimensionality reduction parameters')
        self.reject = self.onReject

    
    def errorMsg(self, msg):
        QtWidgets.QMessageBox.warning(self, 'Error', msg, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)


    def testParameter(self, func, msg):
        try:
            func()
        except:
            self.errorMsg(msg)
            return False
        return True


    def checkParameters(self, tab):
        if tab == 0: # PCA
            pass
                    
        return True


    def onAccept(self):
        if not self.checkParameters(self.notebook.currentIndex()):
            return        
        super(DimensionalityReductionParameters, self).accept()


    def onReject(self):
        self.restoreParameters()
        super(DimensionalityReductionParameters, self).reject()


    def showEvent(self, event):
        self.__parameters = self.getParameters()


    def getParameters(self):
        params = {}
        params['pca_redDim'] = self.PCARedDimCheckbox.isChecked()
        params['pca_secondcomponent'] = self.PCASecondComponentCheckbox.isChecked()
        params['pca_backproject'] = self.PCABackprojectCheckbox.isChecked()
        return params

        
    def restoreParameters(self):
        params = self.__parameters
        self.PCARedDimCheckbox.setChecked(params['pca_redDim'])
        self.PCASecondComponentCheckbox.setChecked(params['pca_secondcomponent'])
        self.PCABackprojectCheckbox.setChecked(params['pca_backproject'])


    def onTabChanged(self, idx):
        if not self.checkParameters(self.__currentTab):
            currentTab = self.__currentTab
            self.__currentTab = idx
            self.notebook.setCurrentIndex(currentTab)
        else:
            self.__currentTab = idx


    def setTab(self, tab):
        if tab >= 0:
            self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Apply")
            self.notebook.setCurrentIndex(tab - 1)
            self.__currentTab = tab - 1
            for i in range(self.notebook.count()):
                if i == tab - 1:
                    self.notebook.setTabEnabled(i, True)
                else:
                    self.notebook.setTabEnabled(i, False)
        else:
            self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Ok")
            self.notebook.setCurrentIndex(0)
            self.__currentTab = 0
            for i in range(self.notebook.count()):
                self.notebook.setTabEnabled(i, True)


    def onPCARedDimChanged(self, state):
        if state == QtCore.Qt.Unchecked:
            self.PCASecondComponentCheckbox.setEnabled(False)
            self.PCABackprojectCheckbox.setEnabled(False)
        else:
            self.PCASecondComponentCheckbox.setEnabled(True)
            self.PCABackprojectCheckbox.setEnabled(True)
            

    def getPCARedDim(self):
        return self.PCARedDimCheckbox.isChecked()


    def getPCASecondComponent(self):
        return self.PCASecondComponentCheckbox.isChecked()


    def getPCABackproject(self):
        return self.PCABackprojectCheckbox.isChecked()

