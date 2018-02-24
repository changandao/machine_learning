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


import math
import numpy as np
import numpy.matlib
import scipy.optimize


class SoftMarginSVM(object):
    def __init__(self, C=1.0):
        self._C = C

    def fit(self, X, y):
        self._X = X
        self._y = y
        self._m = len(X)

    def predict(self, X):
        ## prepare the input variables for the optimization
        dim = self._X.shape[1]
        x = np.zeros(dim + 1 + self._m)
        tempX = np.append(self._X, np.ones((self._m, 1)), axis=1)
        tempy = self._y.reshape(self._m, 1)
        A = tempX * tempy
        tempA = np.zeros((self._m, dim + 1))
        tempA = np.append(tempA, np.identity(self._m), axis = 1)
        A = np.append(A, np.identity(self._m), axis=1)
        A = np.append(A, tempA, axis=0)
        b = np.ones(self._m)
        b = np.append(b, np.zeros(self._m))
        fun = lambda x: math.pow(np.linalg.norm(x[0:dim]),2)/2 + self._C * np.sum(x[dim+1:])  # objective function

        cons = ({'type': 'ineq', 'fun': lambda x: np.dot(A, x.reshape(dim + 1 + self._m, 1)).reshape(self._m*2) - b})
        ##OPTIMIZATION
        res = scipy.optimize.minimize(fun, x, method=None, constraints=cons)
        print(res)

        ##predict
        newdim = len(X)
        newX = np.append(X, np.ones((newdim, 1)), axis=1)
        newy = np.dot(newX, res.x[0:dim+1].reshape((dim+1,1)))
        newy = newy.reshape(newdim)
        newy[newy > 1] = 1
        newy[newy < -1] = -1
        return newy

if __name__ == '__main__':
    SSVM = SoftMarginSVM()
    X = numpy.array([[1, 1], [1, 2], [2, 1], [2, 2], [4, 5], [5, 4], [5, 5], [4, 4]])
    y = numpy.array([-1, -1, -1, -1, 1, 1, 1, 1])
    SSVM.fit(X, y)
    newpredict = SSVM.predict(X)
    print(newpredict)