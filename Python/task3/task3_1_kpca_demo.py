# kpca_demo
import numpy as np
import matplotlib.pyplot as plt

# data generation

# the following code generates 2 dimensional data. specifically, for each vector the first component is
# between 0 and alpha, while the second is between 0 and 1
n = 1000                       # number of data points
alpha = 2                      # length/width ratio
s = np.array([alpha,1])
X = np.diag(s).dot(np.random.rand(2,n))          # uniformly distributed points on a rectangle

H = np.eye(n) - np.ones((n,n))/n           # create centering matrix

def custom_sdist(X):
	"""
	Funktion that given a matrix X returns the squared pairwise distances 
	of the column vectors in matrix form
	"""
	XX = np.dot(X.T, X)
	pdists = np.outer(np.diag(XX), np.ones(XX.shape[1]).T) + np.outer(np.ones(XX.shape[0]), np.diag(XX).T) - 2*XX
	return pdists

sigma = 1

def K(X):
	# MISSING: kernel function for Gaussian kernel
	K  = np.exp(-custom_sdist(X)/(2*sigma))
	return K

k = 2                                   # number of eigenvectors

# MISSING
# MISSING
# MISSING
# MISSING
oroginal_K = K(X)
center_K = H.dot(oroginal_K.dot(H))
w,v = np.linalg.eig(center_K)
w[k:-1] = w[k:-1] - w[k:-1]
v[:,k:-1] = v[:,k:-1] - v[:,k:-1]

Y = np.dot(v,np.dot(np.diag(w),v.T))# projection of the kernel matrix K onto the first two principal components


fig, axs = plt.subplots(1,2,figsize=(15,6), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace=.5, wspace=.1)
axs = axs.ravel()
for ip in range(k):
	im = axs[ip].scatter(X[0,:], X[1,:], c=Y[ip,:])
	axs[ip].set_title('Color indicates value of PC {} at this point'.format(ip+1))
    
fig.colorbar(im)
plt.show()