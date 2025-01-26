# Assignment 5: Dimensionality Reduction and Visualization

## Overview
This repository contains the solution for Assignment 5, which focuses on applying dimensionality reduction techniques (PCA and MDS) to visualize and reconstruct data from high-dimensional datasets, including the MNIST, Dogs SNP, and a molecular distance matrix.

## Datasets
MNIST: A dataset of 6000 images of handwritten digits (0-9).
Dogs SNP: A dataset with genetic data from 1355 dogs, each with 784 SNP features.
Molecular Data: A distance matrix between atoms in a molecule and their element types.

## Assignment Breakdown
Part 1: PCA on MNIST
Apply PCA to reduce the MNIST dataset from 784 dimensions to 2.
Visualize the data in 2D and save the plot.
Reconstruct an image using the first two principal components and save it.
Manually reconstruct a new handwritten-like digit by selecting a point in the PCA-transformed space.
Part 2: PCA on Dogs SNP
Apply PCA to reduce the SNP data from 784 dimensions to 2.
Visualize the data in 2D and save the plot with color-coding based on clade labels.
Part 3: MDS on Molecular Distance Matrix
Perform MDS on a given molecular distance matrix to obtain 3D coordinates.
Output the coordinates in a CSV file.

Extra Credit 1 (Tier 2)
Visualize the 3D molecular structure using the reconstructed coordinates.
Color-code atoms and draw bonds if their distances are below a threshold.

Extra Credit 2 (Tier 3)
Identify the molecule based on the 3D structure and atom types.
Research the tree on campus where the molecule can be found, and bring a leaf from it.