import csv
import numpy as np
import matplotlib.pyplot as plt
import cvxopt
from scipy.spatial.distance import cdist, pdist, squareform

M = np.array([0,0,0])
with open('task3_2_data.txt') as csvfile:
    filereader = csv.reader(csvfile, delimiter=' ')
    for row in filereader:
        b = [float(c) for c in row]
        M = np.vstack((M, np.array(b)))
        
M = M[1:,:]

X = M[:, 1:]
y = M[:, 0:1]

plt.figure()
plt.scatter(X[:,0], X[:,1], c=y)
plt.show()

# Train SVM

N = X.shape[0]
# N: number of samples

# rewrite the optimization problem (8.53) in notes on kernel SVM available 
# on Moodle as a problem that the cvxopt quadratic problem solver can solve it
# cvxopt.solvers.qp(H, h, G, h, Aeq, ceq) solves problems of the form 
# min 0.5*x'*H*x + f'*x 
# subject to G*x <= h, Aeq*x = ceq

###################
# Note that the SVM optimization problem in its standard formulation does not
# have standard inequality constraints. However, there are constraints on the
# values of x, i.e. lb <= x <= ub. In order to put this into the cvxopt solver
# we have to rewrite this to -I * x <= -lb and I * x <= ub
# and then concatenate them to G = [-I; I], h = [-lb; ub].
# I already implemented this in lines 63 & 64, you only have to define lb and ub
# x, f, lb, ub in R^N, H in R^{N x N}, Aeq in R^{1 x N}
###################

C = 1 # parameter that penalizes violation of separation

# CHANGE HERE:
sigma = 1 # parameter used in the Gaussian kernel

# MISSING Compute the matrix H according to the Gaussian kernel 
#(either with a for loop or a faster implementation)
# Hint: the function pdist(.) computes pairwise distances
# use squareform to reshape the resulting vector to a matrix
H = 

#MISSING define other parameters required for the cvxopt solver
f = 
Aeq = 
ceq = 
lb = 
ub = 

# these variables are required for the cvxopt solver
G = np.vstack([-np.eye(N), np.eye(N)])
h = np.hstack([-lb, ub])

# use cvxopt to determine Lagrange mutliplier
# define the solver
sol = cvxopt.solvers.qp(cvxopt.matrix(H), cvxopt.matrix(f), 
                        cvxopt.matrix(G), cvxopt.matrix(h), 
                        cvxopt.matrix(Aeq), cvxopt.matrix(ceq))

# find the solution
lambd = np.array(sol['x'])

# determine index of support vectors
idx1 = (lambd>1e-9)
idx2 = (lambd<(C - 1e-9))
idx = (idx1==idx2).ravel()

# MISSING: compute b (see equation (8.55) in the notes on kernel SVM)
b = 

# THIS PART PLOTS THE CLASSIFICATION REGIONS
idx = (lambd>1e-6).ravel()

X_sup = X[idx,:]
y_sup = y[idx]
lambd_sup = lambd[idx]

# generate meshgrid
xgv = np.linspace(-0.7, 0.3, 50)
ygv = np.linspace(-0.8, 0.6, 70)
[meshX, meshY] = np.meshgrid(xgv, ygv)
Z = np.vstack((meshX.ravel('F'), meshY.ravel('F'))).T

# compute labels
tmp = np.dot(np.exp(cdist(Z, X_sup)**2 / (-2*sigma**2)), (lambd_sup * y_sup)) - b
# linear
#tmp = np.sum((np.dot(Z, X_sup.T) * y_sup.ravel() * lambd_sup.ravel()), axis=1) - b
label = np.sign(tmp)

plt.figure()
plt.scatter(Z[:,0], Z[:,1], c=label, s=10)
plt.show()