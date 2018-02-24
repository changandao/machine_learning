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



import numpy
import numpy.matlib


class LinearLogisticRegression(object):

    def __init__(self, learningRate = 0.5, maxIterations = 100):
        self.learningrate = learningRate
        self.maxIterations = maxIterations

    def fit(self, X, y):
        self.X = X
        self.y = y
        self.__m = len(X)
        self.__mMax = 1e8

    def gFunc(self, X, theta):
        temp = numpy.dot(theta, X.transpose())
        result = 1/(1-numpy.exp(-temp))
        return result

    def predict(self, X):
        Z = numpy.zeros(0)
        Xdim = X.shape[1]
        theta = numpy.random.random(Xdim)
        for i in range(self.maxIterations):
            g = self.gFunc(X, theta)
            gradg = g * (1 - g)
            tempgl = self.y - g
            gradL = numpy.dot(tempgl, X)
            H = -  numpy.dot(numpy.dot(gradg, X).transpose(), numpy.dot(gradg,X))
            Hmat = numpy.mat(H)
            Hinv = Hmat.I
            Hinv = numpy.array(Hinv)
            theta = theta - self.learningrate*Hinv*gradL

        D = self.gFunc(theta, X)
        Z = numpy.append(Z, self.y[D > 0.5])
        return Z



if __name__ == '__main__':

    NN = LinearLogisticRegression()
    X=numpy.array([[1,1],[1,2],[2,1],[2,2],[4,5],[5,4],[5,5],[4,4]])
    #print(type(numpy.dot(X.transpose, X)))
    y=numpy.array([0,0,0,0,1,1,1,1])
    NN.fit(X,y)
    newpredict = NN.predict(X)
    print(newpredict)





