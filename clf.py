
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
#from sklearn.neighbors import KNeighborsClassifier
import os

'''
def compute_accumulated_cost_matrix(x, y) -> np.array:
    """Compute accumulated cost matrix for warp path using Euclidean distance
    """
    distances = compute_euclidean_distance_matrix(x, y)

    # Initialization
    cost = np.zeros((len(y), len(x)))
    cost[0,0] = distances[0,0]
    
    for i in range(1, len(y)):
        cost[i, 0] = distances[i, 0] + cost[i-1, 0]  
        
    for j in range(1, len(x)):
        cost[0, j] = distances[0, j] + cost[0, j-1]  

    # Accumulated warp path cost
    for i in range(1, len(y)):
        for j in range(1, len(x)):
            cost[i, j] = min(
                cost[i-1, j],    # insertion
                cost[i, j-1],    # deletion
                cost[i-1, j-1]   # match
            ) + distances[i, j] 
            
    return cost




#time series reading in from the web stream (input )
ts1 = np.random.rand(10, 18)
ts2 = np.random.rand(15, 18)

# Define a custom distance function for DTW
def distance(x, y):
    return euclidean(x, y)

# Compute the DTW distance and alignment path
distance, path = fastdtw(ts1, ts2, dist=distance)

print("DTW Distance:", distance)
print("Alignment Path:", path)
'''
#in this method, we use dynamic time warping to compute similarity metric 
#between time series, and treat these DTW distances as features for
#improved time series classification, as demonstrated to be effectie in (Kate, 2014)
#We are able to compress the need for training data via this efficient tradining method. 
#given a small, centralized training set of ground truth points,

# Assuming train_data is a list of training time series, test_point is the test time series,
# and train_labels are the corresponding labels for the training data.
#0 = good shot
#1 = bad shot forearm angle
#2 = bad shot 3batui

clfdict = {}
train_data = []
train_labels = []
for file in os.listdir('good_data'):
    with open(os.path.join('good_data',file),"r") as f:
        point = []
        for line in f:
            point.append([float(x) for x in line.split(',')[1:]])
        train_data.append(point)
        train_labels.append(0) 
clfdict.update({0:'good'})
        
badidx = 1
for subdir in os.listdir():
    if ('(bad)') in subdir:
#for file in os.listdir('*(bad)'):
        for file in os.listdir(subdir):
            with open(os.path.join(subdir,file),"r") as f:
                point = []
                for line in f:
        #            point.append(line.split(',')[1:])
                    point.append([float(x) for x in line.split(',')[1:]])
                train_data.append(point)
                train_labels.append(badidx)
                
        clfdict.update({badidx:subdir})
        badidx = badidx + 1





train_data, train_labels = shuffle(train_data, train_labels)
#print(len(train_data))
#print(len(train_labels))
test_data = train_data[:test_split]
test_labels = train_labels[:test_split]
train_data = train_data[test_split:]
train_labels = train_labels[test_split:]



# Compute DTW distances
def NNDTW(test_point):
    dtw_distances = []
    #print(test_point)

    print(type(test_point))

#    print(test_point.shape)
    for train_point in train_data:
        dtw_distance, _ = fastdtw(test_point, train_point)
        dtw_distances.append(dtw_distance)

    # 1-Nearest Neighbors classification
    #knn_classifier = KNeighborsClassifier(n_neighbors=1, metric='precomputed')
    #knn_classifier.fit([[d] for d in dtw_distances], train_labels)
    nearestidx = np.argmin(dtw_distances)
    nearestneighbor = train_labels[nearestidx]

    # Classify the test point
    #predicted_label = knn_classifier.predict([[min(dtw_distances)]])
#    print("Predicted label:", predicted_label[0])
#    return predicted_label[0]
    #print("Predicted label:", nearestneighbor)
    print(nearestidx)
    return nearestneighbor
    

#print(test_data)
print(clfdict)

for idx, pt in enumerate(test_data):
#    print(pt)
    pred = NNDTW(pt)
    print('predicted: ', pred)
    print('actual: ', test_labels[idx])



