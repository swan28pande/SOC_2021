import matplotlib.pyplot as plt
import numpy as np
from kmeans import kmeans

dataset = np.random.randn(100,2)
centroids,cluster_ids = kmeans(dataset,3)

plt.scatter(dataset[:,0],dataset[:,1],c=cluster_ids)
plt.show()

