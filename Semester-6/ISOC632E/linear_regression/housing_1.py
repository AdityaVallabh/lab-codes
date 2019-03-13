import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def err(yy, y):
    diff = yy - y
    return np.sum(np.power(diff, 2))/(2*len(y))
    # return sum(np.abs(diff)/y)/len(y)

def pre_process(data, cols):
    # for col in cols:
    #     data.loc[data[col] == 'yes', [col]] = 1
    #     data.loc[data[col] == 'no', [col]] = 0
    data = data.drop(cols, axis=1)
    data = (data - data.mean())/data.std()
    return data

def train(x, y):
    X = np.ones((x.shape[0],x.shape[1]+1))
    X[:,1:] = x
    Y = np.array(y)

    XX = X.T.dot(X)
    XY = X.T.dot(Y)

    W = np.linalg.inv(XX).dot(XY)
    return W

def predict(x, W):
    X = np.ones((x.shape[0],x.shape[1]+1))
    X[:,1:] = x
    pred = []
    for t in X:
        pred.append(t.dot(W))
    return np.array(pred)

data = pd.read_csv('dataset.csv', index_col=0)
# data = data.sample(50)
data = pre_process(data, ['driveway', 'recroom', 'fullbase', 'gashw', 'airco', 'prefarea'])

x = data.loc[:, data.columns != 'price'].values
y = data['price'].values
W = train(x, y)
# print(W)
yy = predict(x, W)
norm_err = err(yy, y)
print('Normal Equations Error: {}'.format(norm_err))

def gradient_descent(x, y, w=None, epochs=20, learning_rate=1e-1):
    errs = []
    X = np.ones((x.shape[0],x.shape[1]+1))
    X[:,1:] = x
    if not w:
        w = np.zeros(X.shape[1])
    N = float(len(y))
    for i in range(epochs):
        y_current = (X.dot(w))
        errs.append(err(y_current, y))
        diff = y_current - y
        Z = (X.T.dot(diff))
        w_gradient = (1/N) * Z
        w -= (learning_rate * w_gradient)
    return w, errs

W2, errs = gradient_descent(x, y)
yy = predict(x, W2)
print('Gradient Descent Error: {}'.format(err(yy, y)))
# print(W2)
plt.plot(range(len(errs)), errs, '-r')
plt.plot(range(len(errs)), [norm_err]*len(errs), '-g')
plt.grid()
plt.show()
