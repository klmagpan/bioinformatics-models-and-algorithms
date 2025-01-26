# Name: Kimberly Magpantay (klmagpan)
# BME205 Fall 2024
# Assignment 5 Tier 2
# Goal: Apply MDS on Molecular Data and Plot
# Usage: python Kimberly_Magpantay_Tier2.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_molecular_data(file_path):
    # Load molecular data from the TSV file
    data = pd.read_csv(file_path, sep='\t')
    distances = data.iloc[:, 2:].values  # Distance matrix starts from column index 2
    atom_types = data['Element'].values
    atomic_numbers = data['Element'].astype(int).values  # Convert element numbers from the 2nd column
    return distances, atom_types, atomic_numbers

def apply_mds(distances):
    from sklearn.manifold import MDS
    mds = MDS(n_components=3, dissimilarity='precomputed')
    coordinates = mds.fit_transform(distances)
    return coordinates

def cpk_color_mapping(atomic_numbers):
    # CPK color mapping based on atomic numbers
    color_map = {
        1: 'white',    # Hydrogen
        6: 'black',    # Carbon
        7: 'blue',     # Nitrogen
        8: 'red',      # Oxygen
        15: 'orange',  # Phosphorus
        16: 'yellow',  # Sulfur
        17: 'green',   # Chlorine
        # Add more elements as needed
    }
    return [color_map.get(num, 'gray') for num in atomic_numbers]  # Default to gray for unknown elements

def atom_size_mapping(atomic_numbers):
    # Example mapping for sizes based on atomic number
    sizes = {
        1: 100,   # H
        6: 200,   # C
        7: 250,   # N
        8: 300,   # O
        9: 350,   # F
        17: 350,  # Cl
        35: 400,  # Br
        53: 450,  # I
        15: 300,  # P
        16: 350,  # S
        # Add more as needed
        'default': 200  # Default size
    }
    return [sizes.get(num, sizes['default']) for num in atomic_numbers]

def visualize_molecule(coordinates, atom_types, atomic_numbers, distances):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Get CPK colors for each atom based on atomic numbers
    colors = cpk_color_mapping(atomic_numbers)
    sizes = atom_size_mapping(atomic_numbers)

    # Plot the atoms
    ax.scatter(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2], c=colors, s=sizes)

    # Draw lines between atoms based on distance
    for i in range(len(distances)):
        for j in range(i + 1, len(distances)):
            if distances[i, j] < 1.6:  # Adjust the threshold as needed
                ax.plot([coordinates[i, 0], coordinates[j, 0]], 
                        [coordinates[i, 1], coordinates[j, 1]], 
                        [coordinates[i, 2], coordinates[j, 2]], 
                        color='gray', alpha=0.5)  # Draw bonds

    ax.set_title('3D Molecular Structure')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')

    plt.savefig('molecule_3D_plot.png')
    plt.show()

def main():
    # Load molecular distance matrix and atom types
    distances, atom_types, atomic_numbers = load_molecular_data('molecule_distances.tsv')

    # Apply MDS to obtain 3D coordinates
    coordinates = apply_mds(distances)

    # Visualize the molecule
    visualize_molecule(coordinates, atom_types, atomic_numbers, distances)

if __name__ == '__main__':
    main()