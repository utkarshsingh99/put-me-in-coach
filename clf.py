
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from sklearn.utils import shuffle
import time
import os
'''
in this method, we use dynamic time warping to compute similarity metric
between time series, and treat these DTW distances as features for
improved time series classification, as demonstrated to be effectie in (Kate, 2014)
We are able to compress the need for training data via this efficient tradining method.
given a small, centralized training set of ground truth points,

Assuming train_data is a list of training time series, test_point is the test time series,
and train_labels are the corresponding labels for the training data.
Ex: for some current labels.
#0 = good shot
#1 = bad shot forearm angle
#2 = bad shot 3batui
'''
clfdict = {}
train_data = []
train_labels = []

#aggregate training samples for good data
for file in os.listdir('good_data'):
    with open(os.path.join('good_data',file),"r") as f:
        point = []
        for line in f:
            point.append([float(x) for x in line.split(',')[1:]])
        train_data.append(point)
        train_labels.append(0)
clfdict.update({0:'good'})


badidx = 1

#aggregate training samples for any number of "bad form" classes, and assign a corresponding class label
for subdir in os.listdir():
    if ('(bad)') in subdir:
        for file in os.listdir(subdir):
            with open(os.path.join(subdir,file),"r") as f:
                point = []
                for line in f:
                    point.append([float(x) for x in line.split(',')[1:]])
                train_data.append(point)
                train_labels.append(badidx)

        clfdict.update({badidx:subdir})
        badidx = badidx + 1



test_split = 6

train_data, train_labels = shuffle(train_data, train_labels)
test_data = train_data[:test_split]
test_labels = train_labels[:test_split]
train_data = train_data[test_split:]
train_labels = train_labels[test_split:]



# Compute DTW distances
def NNDTW(test_point):
    dtw_distances = []
    #print(test_point)
    for train_point in train_data:
        dtw_distance, _ = fastdtw(test_point, train_point)
        dtw_distances.append(dtw_distance)

    # 1-Nearest Neighbors classification to classify our given test point relative to training points.
    nearestidx = np.argmin(dtw_distances)
    nearestneighbor = train_labels[nearestidx]

    # print(nearestidx)
    return nearestneighbor

print(clfdict)

#for all test points: validate performance and that prediction is accurate when only mapping against train points (which exclude itself).
start_time = time.time()
passes = 0
num_test = 0
for idx, pt in enumerate(test_data):
    pred = NNDTW(pt)
    # print('predicted: ', pred)
    # print('actual: ', test_labels[idx])
    num_test += 1
    if pred == test_labels[idx]:
        passes += 1
    else:
        print(f"FAIL: {pt}, prediction: {pred}, actual{test_labels[idx]}")
print(f"passes: {100*passes/num_test}%, tests run: {num_test}")
print(f"Time: {time.time() - start_time}")



