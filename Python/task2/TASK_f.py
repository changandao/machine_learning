# assignment 2
# Hang Xu, Sen Wang, Zhenglei Hu, Jianxiang Feng

import os, glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time


# global parameters
data_dir = '/Users/samwang/Documents/TUM/1stSemester/InfoRetrv/task2/yaleBfaces'
print_vec = True


class kpca_3nn(object):
	def __init__(self):
		pass

	def train(self, training_set_dir):
		# inputs: training_set_dir: path of training set
		self.X_train = []
		self.y_train = []
		os.chdir(training_set_dir)
		s0_list = glob.glob('*.png')
		for f in s0_list:
			img = Image.open(f).convert('L')
			img = np.array(img) / 255.
			# get data of every image in training set and vectorize
			self.X_train.append(img[:, :].ravel())
			# get corresponding labels
			self.y_train.append(int(os.path.split(f)[1].split('person')[-1][:2]))
		# convert T and T_label into array
		# T.shape: d*n, where d is dimension and n is number of samples
		self.X_train = np.asarray(self.X_train).T
		# T_label.shape: (n,)
		self.y_train = np.asarray(self.y_train)

	def predict(self, X_test, k, y_test=None, start_from=0):
		# inputs: X_test: test data with shape d*n, y_test: label with shape(n,), k: number of PCs
		# return: if y_test are given, return the misclassification rate
		n_test = X_test.shape[1]
		n_train = self.X_train.shape[1]
		self.u = get_k_SigVec(self.X_train, k, start_from=start_from)  # shape: d*k
		# extract k PCs from training set, which will be applied in test set
		kpca_X_train = self.u.T.dot(self.X_train)  # shape: k*n_train
		# extract k PCs from test set
		kpca_X_test = self.u.T.dot(X_test)  # shape: k*n_test

		# compute distance matrix between training set and test set
		dis_matrix = np.zeros((n_test, n_train))
		sum_tr = np.sum(kpca_X_train ** 2, axis=0)
		sum_te = np.sum(kpca_X_test ** 2, axis=0)
		dis_matrix = np.sqrt(sum_tr[None, :] + sum_te[:, None] - 2 * kpca_X_test.T.dot(kpca_X_train))

		# predict labels of test samples based on 3 nearest neighbour in dis_matrix
		y_pre = np.zeros(n_test)
		sorted_idx = np.argsort(dis_matrix, axis=1)  # values are sorted in ascending order
		for i in xrange(n_test):
			closest_y = []
			closest_y.extend(self.y_train[sorted_idx[i, :3]])
			# print closest_y
			count = np.zeros(11)
			for j in closest_y:
				count[j] += 1
			y_pre[i] = np.argsort(count)[-1]

		# if test labels are given, compute the misclassification rate(error rate)
		# print y_test.shape, len(y_pre)
		if y_test != None:
			error_rate = 1 - np.sum(y_test == y_pre, dtype=float) / n_test
			return error_rate


def get_k_SigVec(X, k, start_from=0):
	# input param: X: raw data in vectorized form with shape d*n, k:number of the first singular vectors in U
	# return: k PC vectors
	# nomarlize the raw data
	X_mean = X - np.mean(X, axis=1)[:, None]
	X_std = X / np.sqrt(np.sum(X_mean ** 2, axis=1))[:, None]
	u, s, v = np.linalg.svd(X_std)
	return u[:, start_from:k + start_from]


start = time.clock()
training_set_dir = data_dir + '/subset0'
###(1)
# extract k PC from raw data X
k = 20
X_train = []
y_train = []
os.chdir(training_set_dir)
s0_list = glob.glob('*.png')
for f in s0_list:
	img = Image.open(f).convert('L')
	img = np.array(img) / 255.
	# get data of every image in training set and vectorize
	X_train.append(img[:, :].ravel())
	# get corresponding labels
	y_train.append(int(os.path.split(f)[1].split('person')[-1][:2]))
# convert T and T_label into array
# T.shape: d*n, where d is dimension and n is number of samples
X_train = np.asarray(X_train).T
u_k = get_k_SigVec(X_train, k)
# print out the first three sigular vector
if print_vec:
	for i in range(3):
		sig_vec = u_k[:, i].reshape((50, 50))
		plt.subplot(1, 3, i + 1)
		plt.imshow(sig_vec)

###(2)
# construct classifier
kpca_3nn_classifier = kpca_3nn()
kpca_3nn_classifier.train(training_set_dir)

# get test data from subset1-4 and predict
### start from 1th
k_num = 20
error_rate = np.zeros((4, k_num))
fig, ax = plt.subplots()
for i in range(4):
	test_set_dir = data_dir + '/subset' + str(i + 1)
	os.chdir(test_set_dir)
	s_list = glob.glob('*.png')
	X_test = []
	y_test = []
	for f in s_list:
		img = Image.open(f).convert('L')
		img = np.array(img) / 255.
		# get data of every image in test set and vectorize
		X_test.append(img[:, :].ravel())
		# get corresponding labels
		y_test.append(int(os.path.split(f)[1].split('person')[-1][:2]))

	X_test = np.array(X_test).T
	y_test = np.array(y_test)
	for k in range(k_num):
		error_rate[i, k] = kpca_3nn_classifier.predict(X_test, k + 1, y_test=y_test)
	# plot the error rate of this subset
	ax.plot(np.arange(k_num), error_rate[i], '*-', label="subset" + str(i + 1))

ax.set_xlabel('number of PCs')
ax.set_ylabel('error_rate')
ax.set_title('error_rate of subset1-4 starting from the 1st PC')
ax.legend(loc=0)  # upper left corner
plt.show()

### start from 3th
k_num = 17
error_rate = np.zeros((4, k_num))
fig, ax = plt.subplots()
for i in range(4):
	test_set_dir = data_dir + '/subset' + str(i + 1)
	os.chdir(test_set_dir)
	s_list = glob.glob('*.png')
	X_test = []
	y_test = []
	for f in s_list:
		img = Image.open(f).convert('L')
		img = np.array(img) / 255.
		# get data of every image in test set and vectorize
		X_test.append(img[:, :].ravel())
		# get corresponding labels
		y_test.append(int(os.path.split(f)[1].split('person')[-1][:2]))

	X_test = np.array(X_test).T
	y_test = np.array(y_test)
	for k in range(k_num):
		error_rate[i, k] = kpca_3nn_classifier.predict(X_test, k + 1, y_test=y_test, start_from=3)
	# plot the error rate of this subset
	ax.plot(np.arange(k_num), error_rate[i], '*-', label="subset" + str(i + 1))

ax.set_xlabel('number of PCs')
ax.set_ylabel('error_rate')
ax.set_title('error_rate of subset1-4 starting from the 3th PC')
ax.legend(loc=0);  # upper left corner
plt.show()

### start from 5th
k_num = 17
error_rate = np.zeros((4, k_num))
fig, ax = plt.subplots()
for i in range(4):
	test_set_dir = data_dir + '/subset' + str(i + 1)
	os.chdir(test_set_dir)
	s_list = glob.glob('*.png')
	X_test = []
	y_test = []
	for f in s_list:
		img = Image.open(f).convert('L')
		img = np.array(img) / 255.
		# get data of every image in test set and vectorize
		X_test.append(img[:, :].ravel())
		# get corresponding labels
		y_test.append(int(os.path.split(f)[1].split('person')[-1][:2]))

	X_test = np.array(X_test).T
	y_test = np.array(y_test)
	for k in range(k_num):
		error_rate[i, k] = kpca_3nn_classifier.predict(X_test, k + 1, y_test=y_test, start_from=5)
	# plot the error rate of this subset
	ax.plot(np.arange(k_num), error_rate[i], '*-', label="subset" + str(i + 1))

ax.set_xlabel('number of PCs')
ax.set_ylabel('error_rate')
ax.set_title('error_rate of subset1-4 starting from the 5th PC')
ax.legend(loc=0)  # upper left corner
plt.show()
finish = time.clock()
timeintv = finish - start
print timeintv