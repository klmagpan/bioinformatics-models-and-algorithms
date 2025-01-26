# Assignment 3: Permutation Test for Overlaps

## Overview
This repository contains the solution for Assignment 3: Permutation Test for Overlaps from the Bioinformatics Models and Algorithms course (BME 205). In this assignment, we implemented a permutation test to analyze the overlap between two sets of genomic ranges. The goal was to determine whether the observed overlap between regions associated with gene expression under drought conditions and transcription factor binding sites was statistically significant.

## Assignment Description
The task involves performing a permutation test on two sets of genomic ranges stored in BED files. The first set (Set A) represents regions of the genome associated with high expression levels of a gene under drought conditions, while the second set (Set B) corresponds to regions associated with binding sites of a transcription factor involved in drought response. The hypothesis is to test whether the transcription factor binding sites (Set B) overlap with the regions of high gene expression (Set A) more than what would be expected by chance.

## Learning Objectives
Understand the principles of permutation tests.
Implement a permutation test algorithm in Python.
Analyze and interpret the results of permutation tests for genomic data.
Files
SetA.bed: Genomic regions associated with high expression levels of a gene under drought conditions.
SetB.bed: Genomic regions associated with transcription factor binding sites.
genome.fa.fai: Fasta index file that describes the lengths of chromosomes.
Instructions
### Tier 1 (Required for Full Credit)
Implement a Python program to perform a permutation test on two sets of genomic ranges: SetA.bed and SetB.bed, using the genome.fa.fai file for chromosome lengths.
The program should calculate the number of overlapping bases between the two sets and determine if the overlap is statistically significant by performing a permutation test.
### Tier 2 (Extra Credit)
Improve your permutation test by accounting for multiple chromosomes in the BED files. Ensure that the permutation process considers the chromosome structure to avoid inflation of the p-value.