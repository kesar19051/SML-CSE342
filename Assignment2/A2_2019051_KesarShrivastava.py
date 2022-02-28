# -*- coding: utf-8 -*-
"""SML2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z72es4U3wN2lqHaVlT7wJzuVLDglUWl2
"""

from scipy.stats import bernoulli
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
import pandas as pd
from mpl_toolkits import mplot3d
from math import *
import sympy as sp
sp.init_printing(use_unicode=True)

"""# Question 1

# (a)
"""

#uij = mean of i-th class and j-th dimension
u11 = 0.5
u12 = 0.8
u21 = 0.9
u22 = 0.2

rv11 = bernoulli.rvs(u11,size = 100)
rv12 = bernoulli.rvs(u12,size = 100)
rv21 = bernoulli.rvs(u21,size = 100)
rv22 = bernoulli.rvs(u22,size = 100)

data1 = {}
data2 = {}

c1 = [1]*100
c2 = [2]*100

data1['f1'] = list(rv11)
data1['f2'] = list(rv12)
data1['class'] = c1
data2['f1'] = list(rv21)
data2['f2'] = list(rv22)
data2['class']= c2

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

print('Data generation')
print(df1)
print(df2)

def computeMLE(xi, n):
  return sum(xi[:n])/n

def plotN_MLE(l,s):

  x = []
  y = []

  for i in range(1,51):
    x.append(i)
    y.append(computeMLE(l,i))

  plt.plot(x, y)
  plt.xlabel("n")  
  plt.ylabel("MLE")  
  plt.title(s)  
  plt.show()

"""# (b)"""

# split a dataset into train and test sets
features1 = df1.loc[ : , df1.columns != 'class']
labels1 = pd.DataFrame(df1['class'])

# split into train test sets
X_train1, X_test1, y_train1, y_test1 = train_test_split(features1, labels1, test_size=0.50, random_state = 0)

u11_mle = computeMLE(X_train1['f1'].tolist(),50)
u12_mle = computeMLE(X_train1['f2'].tolist(),50)
u1_mle = np.array([u11_mle,u12_mle])
print('The MLE for class 1 is')
print(u1_mle)

plotN_MLE(X_train1['f1'].tolist(),'Class 1 Dimension 1')
plotN_MLE(X_train1['f2'].tolist(),'Class 1 Dimension 2')

"""# (c)"""

# split a dataset into train and test sets
features2 = df2.loc[ : , df2.columns != 'class']
labels2 = pd.DataFrame(df2['class'])

# split into train test sets
X_train2, X_test2, y_train2, y_test2 = train_test_split(features2, labels2, test_size=0.50, random_state = 0)

u21_mle = computeMLE(X_train2['f1'].tolist(),50)
u22_mle = computeMLE(X_train2['f2'].tolist(),50)
u2_mle = np.array([u21_mle,u22_mle])
print('The MLE for class 2 is')
print(u2_mle)

plotN_MLE(X_train2['f1'].tolist(),'Class 2 Dimension 1')
plotN_MLE(X_train2['f2'].tolist(),'Class 2 Dimension 2')

"""Yes, the final answer matches the theoretically calculated values.

# (d)
"""

fig = plt.figure(figsize=(12,10))
ax = plt.axes(projection ='3d')

z = []
for i in range(0,50):
  z.append(i+1)

x = X_train1['f1'].tolist()
y = X_train1['f2'].tolist()

# plotting
ax.scatter3D(x, y, z, label='Class 1')

x = X_train2['f2'].tolist()
y = X_train2['f2'].tolist()

ax.scatter3D(x, y, z, label='Class 2')

ax.set_xlabel('D1')
ax.set_ylabel('D2')
ax.set_zlabel('n')
ax.set_title('Training samples')
plt.legend()
plt.show()

"""# (e)"""

def discriminant(mu11, mu12, mu21, mu22, x1, x2):
  d1 = np.log(pow(mu11, x1)*pow(1-mu11, 1-x1)*pow(mu12, x2)*pow(1-mu12, 1-x2))
  d2 = np.log(pow(mu21, x1)*pow(1-mu21, 1-x1)*pow(mu22, x2)*pow(1-mu22, 1-x2))
  if d1>=d2:
    return 1
  else:
    return 2

X_test1_f1 = X_test1['f1'].tolist()
X_test1_f2 = X_test1['f2'].tolist()
pred1 = []
for i in range(50):
  d = discriminant(u11_mle, u12_mle, u21_mle, u22_mle, X_test1_f1[i], X_test1_f2[i])
  pred1.append(d)

X_test2_f1 = X_test2['f1'].tolist()
X_test2_f2 = X_test2['f2'].tolist()
pred2 = []
for i in range(50):
  d = discriminant(u11_mle, u12_mle, u21_mle, u22_mle, X_test2_f1[i], X_test2_f2[i])
  pred2.append(d)

num1 = 0
num2 = 0

for i in range(50):
  if pred1[i]==1:
    num1 += 1
  if pred2[i]==2:
    num2 += 1

print('Number of samples correctly classified in class 1')
print(num1)
print('Number of samples correctly classified in class 2')
print(num2)

"""# Question 3

# (c)
"""

X = np.array([[2,4],[6,8]])
mu = np.array([[3],[7]])

print('X')
print(X)

print()

print('Mean')
print(mu)

Xc = np.array([[-1,1],[-1,1]])
print('Centralised X')
print(Xc)

S = 0.5*(np.dot(Xc,np.transpose(Xc)))
print('The covariance')
print(S)

e1, e2 = np.linalg.eig(S)

print('Eigenvalue 1')
print(e1[0])
print('Eigenvalue 2')
print(e1[1])

print()
print('The eigenvectors are')

print('       1           2')
print(e2)

U = e2

print('U')
print(U)

U1 = U[:,:1]

Y = np.dot(np.transpose(U1),Xc)
print('Y')
print(Y)

X_ = np.dot(U1,Y)
print(X_)
print()

X_[0][0] += 3
X_[0][1] += 3
X_[1][0] += 7
X_[1][1] += 7

print('After adding mean')
print(X_)

mse = 0
for i in range(2):
  for j in range(2):
    mse += pow(X_[i][j]-X[i][j],2)
mse /= 4
print('MSE = ',mse)

Y = np.dot(np.transpose(U),Xc)
print('Y')
print(Y)

X_ = np.dot(U,Y)
print(X_)
print()

X_[0][0] += 3
X_[0][1] += 3
X_[1][0] += 7
X_[1][1] += 7

print('After adding mean')
print(X_)

mse = 0
for i in range(2):
  for j in range(2):
    mse += pow(X_[i][j]-X[i][j],2)
mse /= 4
print('MSE = ',mse)

"""# (d)"""

d = 3
N = 100
mu = np.array([66, 60, 60])
sigma = np.array([[630, 450, 225], [450, 450, 0], [225, 0, 900]])
X = np.random.multivariate_normal(mu, sigma, N)
X = X.T
X

"""# (e)"""

Xc = np.empty((d,N))
for i in range(d):
  for j in range(N):
    Xc[i][j] = X[i][j]-mu[i]

print('Xc = ', Xc)

S = np.cov(Xc)
print('S = ', S)

eigenValues, eigenVectors = np.linalg.eig(S)

idx = eigenValues.argsort()[::-1]   
eigenValues = eigenValues[idx]
eigenVectors = eigenVectors[:,idx]

print('Eigenvalues = ',eigenValues)
print('U = ', eigenVectors)

"""# (f)"""

def computeMSE(X1, X2, ro, col):
  mse = np.square(np.subtract(X1, X2))
  mse = np.mean(mse)
  return mse

def computeY(U,xc,p):
  U = U[:,:p]
  # print('UUUU = ', U)
  Y = np.dot(np.transpose(U),xc)
  return Y

def computeFinalX(u,y,mean,p,d,N):
  u = u[:,:p]
  x = np.dot(u,y)
  # print(x)
  for i in range(d):
    for j in range(N):
      x[i][j] += mean[i]
  return x

Y = computeY(eigenVectors,Xc,d)
print(Y)
X_ = computeFinalX(eigenVectors,Y,mu,d,d,N)
print(X_)
mse = computeMSE(X_,X,d,N)
print(mse)

"""# (g)"""

x_axis = []
y_axis = []

for i in range(min(d,N)):
  x_axis.append(i+1)
  Y = computeY(eigenVectors,Xc,i+1)
  X_ = computeFinalX(eigenVectors,Y,mu,i+1,d,N)
  mse = computeMSE(X_,X,i+1,N)
  y_axis.append(mse)

plt.plot(x_axis, y_axis)
plt.xlabel('No. of principal components')
plt.ylabel('MSE')
plt.show()