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


from Operation import Operation


class OperationStack(object):
	
	def __init__(self, toolbox):
		self.toolbox = toolbox
		self.clear()


	def clear(self):
		self.__stack = list()
		self.__idx = -1


	def add(self, operation):
		# print("add op")
		if self.__idx + 1 != len(self.__stack):
			del self.__stack[self.__idx+1:]
		toolboxImage = self.toolbox.getToolboxImage()
		self.__stack.append((toolboxImage, operation))
		self.__idx += 1
		# print("add ToolboxImage ", self.__idx, len(self.__stack))


	def undo(self):
		if self.__idx >= 0:
			(_, ops) = self.__stack[self.__idx]
			self.__idx -= 1
			if isinstance(ops, Operation): # single operation
				ops.undo()
			else: # list of operations
				for op in reversed(ops):
					op.undo()

			if self.__idx < 0:
				toolboxImage = (None, None, None, None)
			else:
				(toolboxImage, _) = self.__stack[self.__idx]
			self.toolbox.setToolboxImage(toolboxImage)
			# print("use ToolboxImage ", self.__idx, len(self.__stack))


	def redo(self):
		if self.__idx + 1 < len(self.__stack):
			self.__idx += 1
			(toolboxImage, ops) = self.__stack[self.__idx]
			if isinstance(ops, Operation): # single operation
				ops.redo()
			else: # list of operations
				for op in ops:
					op.redo()
			self.toolbox.setToolboxImage(toolboxImage)
			# print("use ToolboxImage ", self.__idx, len(self.__stack))


