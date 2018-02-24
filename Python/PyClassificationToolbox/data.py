from sklearn import datasets


iris = datasets.load_iris()
X = iris.data[:, :2] # 4-dimensional data; we use only the first two dimensions
y = iris.target

for (p, label) in zip(X, y):
    x = p[0]
    y = p[1]
    print('{0:f},{1:f},{2:d}'.format(x, y, int(label)))