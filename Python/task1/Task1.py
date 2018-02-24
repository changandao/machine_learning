# -*- coding: utf-8 -*-
"""
Task1 Curse of Dimensionality
Created on Sat May 13 22:15:24 2017
@author: hangXu
"""

import time
import numpy as np
import matplotlib.pyplot as plt

# Class Samples to get the random vectors
class Samples:
    
    def __init__(self, m, d):
        self.m=m #m samples
        self.d=d #d dimensions
    
    #Generate random vector
    def GenerateRandoms(self):
        sample=2*np.random.rand(self.m,self.d)-1
        
        return sample
    
#Class Angle to calculate the mean of min angle
class Angle:
    
    def __init__(self, sample, m, d):
        self.m=m #m samples
        self.d=d #d dimensions
        self.sample=sample
    
    #Calculate the angle
    def AngleCalculate(self):
        min_angle=np.full((self.m,1),100,dtype=float)
        
        for i in range(self.m):
            temp_angle=1000000
            L1=np.sqrt(self.sample[i,].dot(self.sample[i,]))
            for j in range(self.m):
                if i!=j:                    
                    L2=np.sqrt(self.sample[j,].dot(self.sample[j,]))
                    cos_angle=self.sample[i,].dot(self.sample[j,])/(L1*L2)
                    angle=np.arccos(cos_angle)
                    if angle<temp_angle:
                        temp_angle=angle
            min_angle[i,]=temp_angle
        ave=np.mean(min_angle)
        #return the average of min angle
        return ave

  
averageMinAngle=np.full((999,1),100,dtype=float) #Matrix for average min angle of d dimension

start = time.clock()
for d in range(2,1001): #d dimensions

    sampInstance=Samples(numSamp,d)
    samp=sampInstance.GenerateRandoms()
    minAngleInstance=Angle(samp,numSamp,d)
    minAngle=minAngleInstance.AngleCalculate()

    averageMinAngle[d-2,]=minAngle

#Draw the image
finish = time.clock()

timeint = finish - start
print(timeint)
print('done')
x=np.arange(2,1001,1)
plt.plot(x,averageMinAngle)
plt.show()
