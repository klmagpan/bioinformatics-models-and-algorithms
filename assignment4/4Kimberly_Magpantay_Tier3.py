# Name: Kimberly Magpantay (klmagpan)
# BME205 Fall 2024
# Assignment 4
# Goal: Apply Hierarchical Clustering on MNIST dataset
# Usage: python Kimberly_Magpantay_Tier2.py
# Output: MNIST_denodegram.png

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from collections import Counter

# Load the Dogs dataset with allow_pickle=True for clades
dogs_X = np.load('dogs_X.npy')  # SNP data (1355 samples, 784 SNPs each)
dogs_clades = np.load('dogs_clades.npy', allow_pickle=True)  # Clade information for each dog sample

# Perform hierarchical clustering using average linkage
hierarchical_model = AgglomerativeClustering(n_clusters=30, metric='euclidean', linkage='complete') # ward # complete
hierarchical_model.fit(dogs_X)

# Compute the clustering error based on the clades
def compute_clustering_error(model_labels, true_labels, num_clusters):
    error = 0
    for i in range(num_clusters):
        # Get all samples that belong to the current cluster
        cluster_indices = np.where(model_labels == i)[0]
        cluster_clades = true_labels[cluster_indices]
        
        # Find the most common clade in the cluster
        most_common_clade = Counter(cluster_clades).most_common(1)[0][0]
        
        # Count the number of misclassified samples in this cluster
        cluster_error = np.sum(cluster_clades != most_common_clade)
        error += cluster_error

    return error

# Compute and print the clustering error
clustering_error = compute_clustering_error(hierarchical_model.labels_, dogs_clades, 30)
print(f"K=30 Clustering Error: {clustering_error}")

# Create linkage matrix for dendrogram
Z = linkage(dogs_X, method='complete')

# Plot dendrogram
plt.figure(figsize=(10, 7))
dendrogram(Z, truncate_mode='lastp', p=30, show_leaf_counts=True)
plt.title('Hierarchical Clustering Dendrogram (Dogs)')
plt.xlabel('Sample index or (Cluster size)')
plt.ylabel('Distance')
plt.savefig('Dogs_dendrogram.png')
plt.show()

