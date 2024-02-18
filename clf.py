
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from sklearn.neighbors import KNeighborsClassifier
import os

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

#in this method, we use dynamic time warping to compute similarity metric 
#between time series, and treat these DTW distances as features for
#improved time series classification, as demonstrated to be effectie in (Kate, 2014)
#We are able to compress the need for training data via this efficient tradining method. 
#given a small, centralized training set of ground truth points,

from sklearn.neighbors import KNeighborsClassifier

# Assuming train_data is a list of training time series, test_point is the test time series,
# and train_labels are the corresponding labels for the training data.

train_good = os.listdir('')


# Compute DTW distances
dtw_distances = []
for train_point in train_data:
    dtw_distance, _ = dtw(test_point, train_point)
    dtw_distances.append(dtw_distance)

# 1-Nearest Neighbors classification
knn_classifier = KNeighborsClassifier(n_neighbors=1, metric='precomputed')
knn_classifier.fit([[d] for d in dtw_distances], train_labels)

# Classify the test point
predicted_label = knn_classifier.predict([[min(dtw_distances)]])
print("Predicted label:", predicted_label[0])
