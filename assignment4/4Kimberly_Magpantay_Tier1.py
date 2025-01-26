# Name: Kimberly Magpantay (klmagpan)
# BME205 Fall 2024
# Assignment 4
# Goal: Apply K-Means on MNIST dataset
# Usage: python Kimberly_Magpantay_Tier1.py
# Output: centroids_k10.png, centroids_k11.png

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter

# Load the MNIST subset
MNIST_X = np.load('MNIST_X_subset.npy')  # 6000 images (28*28 pixels flattened)
MNIST_y = np.load('MNIST_y_subset.npy')  # Corresponding labels

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
            # Counts the number of instances of each label in true_labels_in_cluster
        
        # Count the number of misclassified samples (samples that don't match the majority label)
        misclassifications += np.sum(true_labels_in_cluster != most_common_label)
    
    return misclassifications

# Function to plot and save centroids
def save_centroids(kmeans, K, filename):
    centroids = kmeans.cluster_centers_.reshape(K, 28, 28)  # Reshape centroids to 28x28 images
    
    # Adjust the subplot grid depending on the value of K
    if K == 10:
        rows, cols = 2, 5  # 2 rows, 5 columns
    elif K == 11:
        rows, cols = 2, 6  # 2 rows, 6 columns (for 11 centroids)
    
    plt.figure(figsize=(10, 5))  # Adjust the figure size for proper layout
    for i in range(K):
        plt.subplot(rows, cols, i + 1)  # Adjust the number of columns based on K
        plt.imshow(centroids[i], cmap='gray')
        plt.title(f'Centroid {i + 1}')
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(filename)  # Save the figure as a PNG file
    plt.close()  # Close the figure to avoid display when running in a loop or notebook

# K-Means clustering with K=10 and K=11
for K in [10, 11]:
    kmeans = KMeans(n_clusters=K, random_state=42) # Specifies # K , random number generator (get same results consistenly)
    kmeans.fit(MNIST_X) # Fits line to model data
    
    # Predicted cluster labels
    cluster_labels = kmeans.labels_
    
    # Calculate misclassification error
    misclassification_error = calculate_misclassification_error(cluster_labels, MNIST_y, K)

    # Print the results in the required format
    print(f"K={K} Error={misclassification_error}")
    
    # Save centroids to PNG file with the required naming convention
    save_centroids(kmeans, K, f'centroids_k{K}.png')