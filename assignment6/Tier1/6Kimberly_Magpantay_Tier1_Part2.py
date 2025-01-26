# Name: Kimberly Magpantay (klmagpan)
# BME205 Fall 2024
# Assignment 6 Tier 1 Part 2
# Goal: Non-Negative Matrix Factorization on Dogs Dataset
# Usage: python Kimberly_Magpantay_Tier1_Part2.py dogs_X.npy dogs_clades.npy

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF

def nmf_analysis(dog_X_file, dog_clades_file):
    # Load datasets
    # Load the interaction matrix (X) and clade labels from the provided files
    X = np.load(dog_X_file, allow_pickle=True)
    clades = np.load(dog_clades_file, allow_pickle=True)
    
    # Step 2: Apply NMF with n_components=5
    # Initialize NMF with 5 components, random initialization, fixed random state for reproducibility
    # Set max_iter to 500 to allow convergence for large datasets
    nmf = NMF(n_components=5, init='random', random_state=42, max_iter=500, tol=1e-4)
    W = nmf.fit_transform(X)   # W: coefficients matrix representing dogs in terms of components
    H = nmf.components_         # H: basis matrix representing components in terms of original features
    
    # Step 3: Normalize W for proportions
    # Normalize rows of W so each row sums to 1, converting values to proportions
    W_normalized = W / W.sum(axis=1, keepdims=True)
    
    # Step 4: Identify dominant cluster for each dog
    # Find the component with the highest proportion for each dog (dominant cluster)
    dominant_clusters = np.argmax(W_normalized, axis=1)
    # Retrieve the highest proportion for each dog, representing the strength of the dominant cluster
    dominant_proportions = np.max(W_normalized, axis=1)
    
    # Step 5: Sort dogs by dominant cluster and proportion
    # Sort indices first by dominant cluster, then by proportion within each cluster in descending order
    sorted_indices = np.lexsort((-dominant_proportions, dominant_clusters))
    # Reorder the W matrix based on sorted indices to arrange for visualization
    W_sorted = W_normalized[sorted_indices]
    
    # Step 6: Create stacked bar plot
    # Visualize the proportions in W as a stacked bar plot, representing each component across sorted dogs
    plt.figure(figsize=(12, 6))
    plt.stackplot(range(len(W_sorted)), W_sorted.T, labels=[f'Component {i+1}' for i in range(W_sorted.shape[1])])
    plt.xlabel('Dogs')
    plt.ylabel('Proportion')
    plt.legend(loc='upper right')
    plt.title('NMF Proportion Stacked Plot for Dogs Dataset')
    plt.savefig('NMF_Dogs.png')  # Save the plot as an image
    plt.close()  # Close the plot to free up memory
    
    # Step 7: Identify dominant component in Basenji and Wolf samples
    # Locate indices where clade is Basenji or Wolf
    basenji_indices = np.where(clades == '**Basenji')[0]
    wolf_indices = np.where(clades == 'Wolf')[0]
    
    # Get the dominant component for each Basenji and Wolf sample
    basenji_dominant_components = dominant_clusters[basenji_indices]
    wolf_dominant_components = dominant_clusters[wolf_indices]
    
    # Find any common dominant component between Basenji and Wolf
    common_component = np.intersect1d(basenji_dominant_components, wolf_dominant_components)
    
    # Print the shared dominant component, if any, between Basenji and Wolf samples
    print("Dominant component in Basenji and Wolf samples:", common_component)

if __name__ == "__main__":
    # Command-line arguments for files: dog_X_file and dog_clades_file
    dog_X_file = sys.argv[1]
    dog_clades_file = sys.argv[2]
    
    # Run the NMF analysis with the specified files
    nmf_analysis(dog_X_file, dog_clades_file)
