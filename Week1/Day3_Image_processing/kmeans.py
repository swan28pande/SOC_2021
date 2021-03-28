import random
import numpy as np

def kmeans(dataset,n_clusters):
    dataset = dataset.astype(float)

    n_datapoints = dataset.shape[0]
    if(n_clusters > n_datapoints):
        n_clusters = n_datapoints
 
    centroids = []
    shuffled_idx = list(range(n_datapoints))
    random.shuffle(shuffled_idx)

    for cluster_id in range(n_clusters):
        centroids.append(dataset[shuffled_idx[cluster_id]])

    n_iterations = 1

    for iteration in range(n_iterations):
        cluster_ids = []
        for idx in range(n_datapoints):
            cluster_id = 0
            best_dist = np.sum(np.abs(centroids[0]-dataset[idx]))
            for i in range(1,n_clusters):
                dist = np.sum(np.abs(centroids[i]-dataset[idx]))
                if(dist<best_dist):
                    best_dist = best_dist
                    cluster_id = i
            cluster_ids.append(cluster_id)
        
        cluster_sums = [np.zeros_like(dataset[0]) for i in range(n_clusters)]
        cluster_items = [0.0 for i in range(n_clusters)]
        for idx,cluster_idx in enumerate(cluster_ids):
            cluster_sums[cluster_idx] += dataset[idx]
            cluster_items[cluster_idx] += 1

        new_centroids = []
        eps = 1e-3
        for idx,cluster_sum in enumerate(cluster_sums):
            new_centroids.append(cluster_sum/(eps+cluster_items[idx]))
    
        centroids = new_centroids

    return centroids,cluster_ids