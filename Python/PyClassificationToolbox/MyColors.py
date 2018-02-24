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


# from matplotlib.colors import ListedColormap
from PyQt4 import QtCore, QtGui

import Parameters


class MyColors(object):
	
#	mycolors = ListedColormap([
#				'#fce7e7', '#ffb7b7', '#830000', # shades of red
#				'#e7f2e7', '#cce7cc', '#3e9f3e', # shades of green
#				'#e7ebf1', '#ccd7e0', '#003366', # shades of blue
#				'#e7ddc5', '#ddd3ac', '#beb091', '#ac9879', # shades of brown
#				'#c5c5c5', '#7c7c7c', '#4f4f4f', '#3e3e3e' # shades of gray
#		])
	
#	r1, r2, r3, g1, g2, g3, b1, b2, b3, br1, br2, br3, br4, gr1, gr2, gr3, gr4 = mycolors.colors
	
	myColors = [int(i * 360 / Parameters.NUMBER_SUPPORTED_CLASSES) for i in range(Parameters.NUMBER_SUPPORTED_CLASSES)]


#	@staticmethod
#	def qcolor(name):
#		return QtGui.QColor(name)


#	@staticmethod
#	def rgb(name):
#		return QtGui.QColor(name).rgb()


#	@staticmethod
#	def qcolorsForClassOld(classId):
#		if classId == -1:
#			return MyColors.qcolor(MyColors.gr2), MyColors.qcolor(MyColors.gr3), MyColors.qcolor(MyColors.gr3)			
#		elif classId == 0:
#			return MyColors.qcolor(MyColors.b2), MyColors.qcolor(MyColors.b3), MyColors.qcolor(MyColors.b3)
#		elif classId == 1:
#			return MyColors.qcolor(MyColors.r2), MyColors.qcolor(MyColors.r3), MyColors.qcolor(MyColors.r3)
#		elif classId == 2:
#			return MyColors.qcolor(MyColors.g2), MyColors.qcolor(MyColors.g3), MyColors.qcolor(MyColors.g3)
#		else:
#			return QtCore.Qt.black, QtCore.Qt.black, QtCore.Qt.black


	@staticmethod
	def qcolorsForClass(classId):
		if classId < 0:
			return QtGui.QColor('#c5c5c5'), QtGui.QColor('#7c7c7c'), QtGui.QColor('#4f4f4f')
		elif classId < len(MyColors.myColors):
			# 0 <= h < 360, 0 <= s, v < 256
			h = MyColors.myColors[classId] 			
			c3 = QtGui.QColor.fromHsv(h, 255, 128) # dark
			c2 = QtGui.QColor.fromHsv(h,  51, 230) # medium
			c1 = QtGui.QColor.fromHsv(h,  26, 242) # light
			return c1, c2, c3
		else:
			return QtCore.Qt.black, QtCore.Qt.black, QtCore.Qt.black


	@staticmethod
	def rgbForClass(classId):
		c1, c2, c3 = MyColors.qcolorsForClass(classId)
		return c1.rgb(), c2.rgb(), c3.rgb()
