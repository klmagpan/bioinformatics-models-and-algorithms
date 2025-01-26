# Name: Kimberly Magpantay (klmagpan)
# BME205 Fall 2024
# Assignment 5 Tier 1
# Goal: Apply PCA on MNIST/Dogs dataset and MDS
# Usage: python Kimberly_Magpantay_Tier1.py

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.manifold import MDS

def load_data(X_path, y_path):
    """Load the MNIST subset from given paths."""
    X = np.load(X_path)
    y = np.load(y_path)
    # Normalize the data
    X = X / 255.0
    return X, y

def load_dogs_data(X_path, y_path):
    """Load the Dogs SNP dataset from given paths."""
    X = np.load(X_path)
    y = np.load(y_path, allow_pickle=True)
    return X, y

def load_molecular_data(file_path):
    """Load the molecular distance matrix and atom types."""
    data = pd.read_csv(file_path, sep='\t')
    
    # Exclude the first two columns for distances
    distances = data.iloc[:, 2:].values  # Exclude 'Atom Index' and 'Element'
    atom_types = data.iloc[:, 1].values   # Second column contains atom types or elements
    
    # Check if distances is a square matrix
    if distances.shape[0] != distances.shape[1]:
        raise ValueError(f"Distance matrix is not square: shape = {distances.shape}")
    
    return distances, atom_types

def apply_pca(X, n_components=2):
    """Apply PCA to reduce dimensions."""
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
    return X_pca, pca

def apply_mds(distances, n_components=3):
    """Apply MDS to obtain coordinates from the distance matrix."""
    mds = MDS(n_components=n_components, dissimilarity='precomputed', random_state=42)
    coordinates = mds.fit_transform(distances)
    return coordinates

def visualize_pca(X_pca, y, save_path='MNIST_PCA_2D.png'):
    """Visualize the PCA-transformed data."""
    
    # Encode the labels as integers
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)  # Convert categorical labels to integers

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_encoded, cmap='Spectral', alpha=0.5)
    plt.legend(*scatter.legend_elements(), title="Classes")
    plt.title("PCA Visualization")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.colorbar()
    plt.savefig(save_path)
    plt.close()  # Close the figure to prevent it from displaying

def reconstruct_image(pca, image, n_components=2):
    """Reconstruct an image using the PCA model."""
    # Project onto the first n_components
    reduced = pca.transform(image.reshape(1, -1))
    # Reconstruct the image
    reconstructed = pca.inverse_transform(reduced)
    return reconstructed

def save_and_show_image(image, title, save_path):
    """Display and save an image."""
    plt.imshow(image.reshape(28, 28), cmap='gray')
    plt.title(title)
    plt.savefig(save_path)
    plt.close()

def save_coordinates_to_csv(coordinates, atom_types, save_path='molecule_coordinates.csv'):
    """Save the 3D coordinates and atom types to a CSV file."""
    df = pd.DataFrame(coordinates, columns=['X', 'Y', 'Z'])
    df['Atom Type'] = atom_types
    df.to_csv(save_path, index=False)

def main():
    '''Part 1: PCA on MNIST subset'''
    # Load MNIST subset
    X_mnist_subset, y_mnist_subset = load_data('MNIST_X_subset.npy', 'MNIST_y_subset.npy')

    # Apply PCA to reduce dimensions to 2
    X_mnist_pca, pca = apply_pca(X_mnist_subset)

    # Save transformed data
    np.save('MNIST_X_pca.npy', X_mnist_pca)

    # Visualize the 2D PCA-transformed data
    visualize_pca(X_mnist_pca, y_mnist_subset)

    # Reconstruct the first image using the first 2 principal components
    example_index = 0
    example_image = X_mnist_subset[example_index]
    
    # Save original image
    save_and_show_image(example_image, "Original Image", 'MNIST_original.png')

    # Reconstruct the image
    reconstructed_image = reconstruct_image(pca, example_image)
    save_and_show_image(reconstructed_image, "Reconstructed Image with 2 Principal Components", 'MNIST_reconstructed_2PC.png')

    # Reconstruct an image from a selected 2D point
    chosen_2d_point = np.array([[0, 0]])  # You can change this point
    reconstructed_from_coord = pca.inverse_transform(chosen_2d_point)
    save_and_show_image(reconstructed_from_coord, "Reconstructed Image from (0, 0) in 2D PCA Space", 'MNIST_reconstructed_1_from_coord.png')

    '''Part 2: PCA on Dogs SNP dataset '''
    # Load Dogs SNP dataset
    X_dogs, y_dogs = load_dogs_data('dogs_X.npy', 'dogs_clades.npy')

    # Apply PCA to reduce dimensions to 2
    X_dogs_pca, pca_dogs = apply_pca(X_dogs)

    # Save transformed data
    np.save('dogs_X_pca.npy', X_dogs_pca)

    # Visualize the 2D PCA-transformed data for Dogs
    visualize_pca(X_dogs_pca, y_dogs, save_path='Dogs_PCA_2D.png')

    '''Part 3: MDS on molecular distance matrix'''
    # Load molecular distance matrix and atom types
    distances, atom_types = load_molecular_data('molecule_distances.tsv')

    # Apply MDS to reconstruct 3D coordinates
    coordinates = apply_mds(distances)

    # Save coordinates to CSV
    save_coordinates_to_csv(coordinates, atom_types, save_path='molecule_coordinates.csv')

if __name__ == "__main__":
    main()