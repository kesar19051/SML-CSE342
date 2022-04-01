# -*- coding: utf-8 -*-
"""SML3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QZkNaBlPDYE_e4Xo5Xd9JN1s0GABR_MM
"""

from google.colab import drive
drive.mount('/content/drive/')

import tarfile
import os
import numpy as np
import pickle
from google.colab.patches import cv2_imshow
import cv2 as cv
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score
import gzip
import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA

"""#Question1

#(a)
"""

# open file
file = tarfile.open('/content/drive/MyDrive/SML/cifar-10-python.tar.gz')
# extract files
file.extractall('Files')
# close file
file.close()

def unpickle(file, typ):
  with open(file, 'rb') as fo:
    dict = pickle.load(fo, encoding=typ)
    return dict

def displayImage(image):
  image = image.reshape(3,32,32)
  image = image.transpose(1,2,0)
  image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
  cv2_imshow(image)

def visualise(num):
  path = '/content/Files/cifar-10-batches-py/data_batch_'
  path += str(num)
  print('data_batch_'+str(num))
  data = unpickle(path,'latin1')
  for i in range(10):
    print('Class: '+str(i))
    count = 0
    for j in range(len(data['labels'])):
      if data['labels'][j]==i:
        count += 1
        displayImage(data['data'][j])
        if count==5:
          break

for i in range(5):
  visualise(i+1)

"""#(b)

Creating dataset
"""

batch_1 = unpickle('/content/Files/cifar-10-batches-py/data_batch_1', 'bytes')
batch_2 = unpickle('/content/Files/cifar-10-batches-py/data_batch_2', 'bytes')
batch_3 = unpickle('/content/Files/cifar-10-batches-py/data_batch_3', 'bytes')
batch_4 = unpickle('/content/Files/cifar-10-batches-py/data_batch_4', 'bytes')
batch_5 = unpickle('/content/Files/cifar-10-batches-py/data_batch_5', 'bytes')

test_data = unpickle('/content/Files/cifar-10-batches-py/test_batch', 'bytes')

X_train = []
X_train.extend(batch_1[b'data'])
X_train.extend(batch_2[b'data'])
X_train.extend(batch_3[b'data'])
X_train.extend(batch_4[b'data'])
X_train.extend(batch_5[b'data'])
X_train = np.array(X_train)
# X_train = X_train.reshape(X_train.shape[0],3,32,32)
y_train = []
y_train.extend(batch_1[b'labels'])
y_train.extend(batch_2[b'labels'])
y_train.extend(batch_3[b'labels'])
y_train.extend(batch_4[b'labels'])
y_train.extend(batch_5[b'labels'])
y_train = np.array(y_train)
print(X_train.shape,y_train.shape)
X_test = test_data[b'data']
y_test = test_data[b"labels"]
# X_test = X_test.reshape(X_test.shape[0],3,32,32)
y_test = np.array(y_test)
print(X_test.shape,y_test.shape)

def lda(xtrain, ytrain, xtest):
  clf = LinearDiscriminantAnalysis()
  clf.fit(xtrain, ytrain)
  return clf.predict(xtest)

y_pred = lda(X_train, y_train, X_test)

"""#(c)

Accuracy
"""

accuracy_score(y_test, y_pred)

"""Class-wise accuracy"""

pred = []
test = []
for i in range(10):
  pred.append([])
  test.append([])

for i in range(len(y_pred)):
  cls = y_test[i]
  pred[cls].append(y_test[i])
  test[cls].append(y_pred[i])

for i in range(10):
  print('Class'+str(i), end = ' ')
  print(accuracy_score(test[i],pred[i]))

"""#Question2"""

def images_file_read(file_name):
    with gzip.open(file_name, 'r') as f:
        # first 4 bytes is a magic number
        magic_number = int.from_bytes(f.read(4), 'big')
        # second 4 bytes is the number of images
        image_count = int.from_bytes(f.read(4), 'big')
        # third 4 bytes is the row count
        row_count = int.from_bytes(f.read(4), 'big')
        # fourth 4 bytes is the column count
        column_count = int.from_bytes(f.read(4), 'big')
        # rest is the image pixel data, each pixel is stored as an unsigned byte
        # pixel values are 0 to 255
        image_data = f.read()
        images = np.frombuffer(image_data, dtype=np.uint8)\
            .reshape((image_count, row_count, column_count))
        return images
def labels_file_read(file_name):
    with gzip.open(file_name, 'r') as f:
        # first 4 bytes is a magic number
        magic_number = int.from_bytes(f.read(4), 'big')
        # second 4 bytes is the number of labels
        label_count = int.from_bytes(f.read(4), 'big')
        # rest is the label data, each label is stored as unsigned byte
        # label values are 0 to 9
        label_data = f.read()
        labels = np.frombuffer(label_data, dtype=np.uint8)
        return labels

X_train = images_file_read("/content/drive/MyDrive/SML/mnist/train-images-idx3-ubyte.gz")
print(X_train.shape)
y_train = labels_file_read("/content/drive/MyDrive/SML/mnist/train-labels-idx1-ubyte.gz")
X_test = images_file_read("/content/drive/MyDrive/SML/mnist/t10k-images-idx3-ubyte.gz")
print(X_test.shape)
y_test = labels_file_read("/content/drive/MyDrive/SML/mnist/t10k-labels-idx1-ubyte.gz")

X_train = X_train.reshape(60000,28*28)
X_test = X_test.reshape(10000,28*28)

def pca(num, xtrain, xtest):
  pca = PCA(n_components = num)
  pca.fit(xtrain)
  return pca.transform(xtrain), pca.transform(xtest)

x_list = [15,8,3]
y_list = []

for n in x_list:
  train, test = pca(n,X_train,X_test)
  pred = lda(train, y_train, test)
  y_list.append(accuracy_score(y_test, pred))

plt.plot(x_list, y_list)
plt.xlabel('num_components')
plt.ylabel('accuracy')
plt.show()