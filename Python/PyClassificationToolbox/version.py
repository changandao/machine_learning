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


from datetime import date
import json

from Parameters import resource_path

__build__ = 8
__versiondate__ = date(2016, 5, 10)

def readVersionInfo():
	global __build__
	global __versiondate__
	try:
		with open(resource_path('./version.json')) as f:
			info = json.load(f)
			__build__ = int(info['build'])
			__versiondate__ = date.fromordinal(int(info['date']))	
	except:
		print("Error: could not read version info from file 'version.json'")


def writeVersionInfo():
	try:
		with open(resource_path('./version.json'), 'w') as f:
			info = {'build': __build__, 'date': __versiondate__.toordinal()}
			json.dump(info, f)
	except:
		print("Error: could not write version info to file 'version.json'")


def incVersion():
	global __build__
	global __versiondate__
	__build__ += 1
	__versiondate__ = date.today()


def main():
	global __build__
	global __versiondate__
	readVersionInfo()
	incVersion()
	print("Incrementing the build number to {0} and updating the version date to {1}.".format(__build__, __versiondate__))
	writeVersionInfo()

if __name__ == '__main__':
	main()

readVersionInfo()

