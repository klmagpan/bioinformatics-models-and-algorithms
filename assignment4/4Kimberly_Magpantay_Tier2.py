# Name: Kimberly Magpantay (klmagpan)
# BME205 Fall 2024
# Assignment 4
# Goal: Apply Hierarchical Clustering on MNIST dataset
# Usage: python Kimberly_Magpantay_Tier2.py
# Output: MNIST_denodegram.png

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from collections import Counter

# Helper function to calculate misclassification error
def calculate_misclassification_error(labels, true_labels, n_clusters):
    misclassifications = 0
    for cluster in range(n_clusters):
        # Get the indices of the samples in this cluster
        cluster_indices = np.where(labels == cluster)[0]
        
        if len(cluster_indices) == 0:
            continue
        
        # Get the true labels of the samples in this cluster
        true_labels_in_cluster = true_labels[cluster_indices]
        
        # Find the most common true label in the cluster (majority label)
        most_common_label, _ = Counter(true_labels_in_cluster).most_common(1)[0]
        
        # Count the number of misclassified samples (samples that don't match the majority label)
        misclassifications += np.sum(true_labels_in_cluster != most_common_label)
    
    return misclassifications

# Perform hierarchical clustering with average linkage
def hierarchical_clustering(X, k):
    clustering = AgglomerativeClustering(n_clusters=k, linkage='ward') # Least error vs. linkage/complete
    cluster_labels = clustering.fit_predict(X)
    return cluster_labels, clustering

# Helper function to visualize the dendrogram using linkage matrix
def plot_dendrogram(linkage_matrix, labels, filename):
    plt.figure(figsize=(10, 7))
    dendrogram(linkage_matrix, labels=labels, truncate_mode='level', p=10)
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Sample index')
    plt.ylabel('Distance')
    
    # Save the figure
    plt.savefig(filename)
    plt.close()

# Load the MNIST subset (6000 samples, 28x28 pixels)
MNIST_X = np.load('MNIST_X_subset.npy')
MNIST_y = np.load('MNIST_y_subset.npy')

# Perform hierarchical clustering with k=10
k = 10
hierarchical_labels, hierarchical_model = hierarchical_clustering(MNIST_X, k)

# Calculate misclassification error using the same function
misclassification_error = calculate_misclassification_error(hierarchical_labels, MNIST_y, k)

# Output the clustering error
print(f"K={k} Error={misclassification_error}")

# Generate the linkage matrix using scipy's linkage function
linkage_matrix = linkage(MNIST_X, method='average')

# Visualize the dendrogram and save it as MNIST_dendrogram.png
plot_dendrogram(linkage_matrix, MNIST_y, 'MNIST_dendrogram.png')