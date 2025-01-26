# Name: Kimberly Magpantay (klmagpan)
# BME205 Fall 2024
# Assignment 6 Tier 2
# Goal: Apply MDS on Molecular Data and Plot
# Usage: python Kimberly_Magpantay_Tier2.py protein_links.tsv

import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Protein-Protein Interaction Data
def load_data(filepath):
    # Read the TSV file into a DataFrame
    protein_data = pd.read_csv(filepath, sep='\t')
    return protein_data

# Create a symmetric interaction matrix from protein interaction scores
def create_symmetric_matrix(protein_data):
    # Get a unique list of proteins
    proteins = np.unique(protein_data[['protein1', 'protein2']].values)
    protein_index = {protein: idx for idx, protein in enumerate(proteins)}
    n_proteins = len(proteins)

    # Initialize the interaction matrix with zeros
    interaction_matrix = np.zeros((n_proteins, n_proteins))
    
    # Populate the matrix with interaction scores, assuming undirected interactions
    for _, row in protein_data.iterrows():
        p1, p2 = protein_index[row['protein1']], protein_index[row['protein2']]
        score = row['combined_score']
        interaction_matrix[p1, p2] = score
        interaction_matrix[p2, p1] = score  # Symmetry

    return interaction_matrix, proteins

# Apply Non-Negative Matrix Factorization (NMF) to the interaction matrix
def apply_nmf(matrix, n_components=10, random_state=42):
    # Ensure non-negativity for NMF
    nmf_model = NMF(n_components=n_components, init='random', random_state=random_state, max_iter=500)
    W = nmf_model.fit_transform(matrix)
    H = nmf_model.components_
    return W, H

# Assign proteins to clusters based on the highest component in W
def assign_proteins_to_clusters(W):
    protein_clusters = np.argmax(W, axis=1)  # Cluster with the highest component value
    cluster_counts = np.bincount(protein_clusters)
    smallest_cluster_id = np.argmin(cluster_counts)
    smallest_cluster_indices = np.where(protein_clusters == smallest_cluster_id)[0]
    return protein_clusters, smallest_cluster_id, smallest_cluster_indices

# Filter proteins in the selected cluster and create a submatrix for interaction strengths
def filter_cluster(matrix, smallest_cluster_indices):
    smallest_cluster_matrix = matrix[np.ix_(smallest_cluster_indices, smallest_cluster_indices)]
    return smallest_cluster_matrix

# Perform hierarchical clustering and visualize using a heatmap
def visualize_cluster(matrix, proteins):
    # Calculate distance matrix by inverting interaction strengths
    max_value = np.max(matrix)
    distance_matrix = max_value - matrix  # Convert scores to distances
    np.fill_diagonal(distance_matrix, 0)  # Set diagonal to zero for self-distances

    # Condense the distance matrix for linkage computation
    condensed_distance_matrix = squareform(distance_matrix)
    
    # Perform hierarchical clustering using Ward's method
    linkage_matrix = linkage(condensed_distance_matrix, method='ward')

    # Plot and save the heatmap with a dendrogram
    sns.clustermap(matrix, row_linkage=linkage_matrix, col_linkage=linkage_matrix,
                   cmap='viridis', xticklabels=False, yticklabels=False, figsize=(12, 10))
    plt.title('Interaction Strengths for Proteins in Smallest Cluster')
    plt.savefig('Protein_Cluster_Heatmap.png')
    plt.close()

# Main function to execute the entire process
def main(filepath):
    # Load and preprocess data
    protein_data = load_data(filepath)
    interaction_matrix, proteins = create_symmetric_matrix(protein_data)
    
    # Apply NMF to decompose the matrix into W and H matrices
    W, H = apply_nmf(interaction_matrix)
    
    # Assign proteins to clusters and select the smallest cluster
    protein_clusters, smallest_cluster_id, smallest_cluster_indices = assign_proteins_to_clusters(W)
    
    # Filter interaction matrix for proteins in the smallest cluster
    smallest_cluster_matrix = filter_cluster(interaction_matrix, smallest_cluster_indices)
    
    # Visualize the smallest cluster with hierarchical clustering and heatmap
    visualize_cluster(smallest_cluster_matrix, proteins)

# Entry point for command-line execution
if __name__ == "__main__":
    import sys
    main(sys.argv[1])
