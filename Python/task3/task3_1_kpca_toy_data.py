import numpy as np
import matplotlib.pyplot as plt


def gkappa(X,Y):
    sigma = 0.5
    temp = np.dot((X - Y).T, (X-Y))
    k_row = np.exp(- np.sum(temp, axis=0) / (2 * sigma ** 2))
    return k_row


def kgram(X, kappa):
    p, N_X = X.shape
    K = np.zeros((N_X, N_X))
    for ip in range(N_X):
        YY = np.outer(X[:, ip], np.ones(N_X - ip))
        K[ip, ip:] = kappa(X[:, ip:], YY)

    return K + np.tril(K.T, k=-1)


# %% KPCA
def kpca(X, kappa, k):
    p, N_X = X.shape
    K = kgram(X, kappa)
    H = np.eye(N_X) - np.ones((N_X, N_X)) / N_X
    K_centered = H.dot(K).dot(H)
    u, s, Vt = np.linalg.svd(K_centered)
    s = np.sqrt(s)
    S = np.dot(np.diag(s[:k]), Vt[:k, :])

    return (S, u)

if __name__ == '__main__':
    m = 50
    n = 200
    X = np.random.randn(2, m) / 10

    for idx in range(n):
        t = np.random.randn(2, 2)
        tmp = t[:, 0:1] / np.linalg.norm(t[:, 0]) + t[:, 1] / np.linalg.norm(t[:, 1:2]) / 10
        X = np.hstack((X, tmp))

    (reduced_x, u) = kpca(X, gkappa, 1)
    reduced_x = np.dot(u[:, 0:1], reduced_x)
    plt.figure()
    plt.scatter(reduced_x[0, m+1:m+n], reduced_x[1, m+1:m+n])
    plt.scatter(reduced_x[0, 1:m], reduced_x[1, 1:m], c='r')

    plt.show()