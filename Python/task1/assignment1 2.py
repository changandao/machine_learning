# coding = utf-8
"""
Task1 Curse of Dimensionality
Created on Sat May 13 22:15:24 2017
@author: Hang Xu, Sen Wang, Zhenglei Hu, Jianxiang Feng.
"""
import time
import numpy as np
import matplotlib.pyplot as plt
import math

def minAle(sample, d):
	x = np.random.random((sample, d)) * 2 - 1
	normofx = np.linalg.norm(x, axis=1) # the norm of every sample
	Normx = 1/normofx # the riprocal of the norm
	Normx = Normx.reshape((sample, 1)) 
	cosofx = np.dot(x, x.T)*np.dot(Normx, Normx.T) # the matrix of the cosine of different samples  
	cosofx = cosofx - 2 * np.diag(np.diag(cosofx)) # eliminate the influnce of the cosine of the same vector
	average = np.sum(np.max(cosofx,axis=1))/sample # average
	return(average)

start = time.clock() # recording the running time
minangle = []
numSamp = 100; # samples #
D =1000; # The dimension of the vector
for i in range(2,D+1):
	minangle.append(math.acos(minAle(numSamp, i))*180/np.pi)
finish = time.clock()
indeavel = finish-start
print(indeavel)
plt.figure(1)
plt.plot(range(2,D+1), minangle)
plt.xlabel('Dimension d')
plt.ylabel('Minimum angle in degrees')
plt.title('Sample size: {}'.format(numSamp))
plt.show()

print('done')
