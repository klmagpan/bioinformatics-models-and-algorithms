# '''
# Name: Kimberly Magpantay (klmagpan)
# BME205 Fall 2024
# Assignment 3
# Goal: Determine number of overlapping bases b/w SetA and SetB
# Usage: python Kimberly_Magpantay_Tier1.py Tier1_Files/SetA.bed Tier1_Files/SetB.bed Tier1_Files/genome.fa.fai

# Files
# SetA: Regions associated w/ high expression of gene under drought conditions
# SetB: Regions associated with binding sites of transcription factor known to be under drought response
# .bed: Chromosome, start, stop
# Fai.fa: Length, offset (from start), # bases per line, # bytes
# Goal: Determine whather number of overlapping bases b/w ranges is significant

import sys
import numpy as np
import random

'''Read BED File'''
def read_bed(file_path):
    ranges = []
    with open(file_path, 'r') as file: # Open BED file for reading
        for line in file:
            chrom, start, end = line.strip().split()[:3] # Chromosome name, start position, end position
            ranges.append((chrom, int(start), int(end)))
    return ranges

'''Read fasta index (genome.fa.fai) file'''
def read_fai(file_path):
    chrom_lengths = {}
    with open(file_path, 'r') as file: # Open file for reading
        for line in file:
            chrom, length = line.strip().split()[:2] # Chromosome, length
            chrom_lengths[chrom] = int(length)
    return chrom_lengths

'''Merge overlapping or adjacent ranges'''
def merge_ranges(ranges):
    if not ranges: # Checks if input is empty
        return []
    
    ranges.sort(key=lambda x: (x[0], x[1])) # Sort ranges by chromosome then by start
    merged = [ranges[0]]  # Start with the first range
    
    for current in ranges[1:]: # Iterate through the other ranges
        prev_chrom, prev_start, prev_end = merged[-1] # Get the last merged range
        curr_chrom, curr_start, curr_end = current # Now, current range
        
        if curr_chrom == prev_chrom and curr_start <= prev_end:  # Overlapping or adjacent ranges
            merged[-1] = (prev_chrom, prev_start, max(prev_end, curr_end))  # Merge the ranges
        else:
            merged.append(current) # Adds current range as a new entry
    
    return merged

'''Compute overlapped bases b/w A and B ranges'''
def compute_overlap(setA, setB):
    mergedA = merge_ranges(setA)
    mergedB = merge_ranges(setB)
    
    overlap_bases = 0
    i, j = 0, 0  # Pointers to mergedA and mergedB
    
    while i < len(mergedA) and j < len(mergedB):
        chromA, startA, endA = mergedA[i] # Current range A
        chromB, startB, endB = mergedB[j] # Current range B
        
        if chromA == chromB: #
            overlap_start = max(startA, startB)
            overlap_end = min(endA, endB)
            
            if overlap_start < overlap_end: # If there's actual overlap
                overlap_bases += overlap_end - overlap_start  # Add the number of overlapping bases
            
            # Move the pointer of the range that finishes first
            if endA < endB:
                i += 1
            else:
                j += 1
        elif chromA < chromB: # If chromA comes before chromB
            i += 1 # Pointer to next range in A
        else:
            j += 1 # Pointer to next range B
    
    return overlap_bases

"""Shuffle ranges within smaller windows fairly"""
def shuffle_ranges(set_b, chrom_sizes, window_size=50000):
    shuffled = []
    for chrom, start, end in set_b: # Iterate through each range
        chrom_size = chrom_sizes[chrom] 
        range_length = end - start 
        
        # Constrain shuffle to within a window around the original start
        window_start = max(0, start - window_size)
        window_end = min(chrom_size - range_length, start + window_size)
        
        new_start = random.randint(window_start, window_end) # Random new start
        new_end = new_start + range_length # New end based on range length
        shuffled.append((chrom, new_start, new_end)) # Add new range to shuffled list
    return shuffled

'''Permutation test on union of ranges for overlap calculation.'''
def permutation_test(setA, setB, chrom_lengths, num_permutations=10000):
    mergedA = merge_ranges(setA)
    mergedB = merge_ranges(setB)
    
    observed_overlap = compute_overlap(mergedA, mergedB)
    
    overlaps = []
    
    for _ in range(num_permutations):
        # Shuffle Set A randomly over the genome
        shuffled_setA = shuffle_ranges(setA, chrom_lengths)
        merged_shuffledA = merge_ranges(shuffled_setA)
        
        # Compute overlap for shuffled Set A with Set B
        overlap = compute_overlap(merged_shuffledA, mergedB)
        overlaps.append(overlap)
    
    # Calculate p-value
    p_value = np.mean([1 if overlap >= observed_overlap else 0 for overlap in overlaps])
    
    return observed_overlap, p_value

'''Main'''
def main():
    # Parse command-line arguments
    if len(sys.argv) < 4: # Check for minimum number fo arguments
        print("Usage: python submission.py path/to/SetA.bed path/to/SetB.bed path/to/genome.fa.fai [num_permutations]")
        return
    
    setA_path = sys.argv[1]
    setB_path = sys.argv[2]
    genome_fai_path = sys.argv[3]
    num_permutations = int(sys.argv[4]) if len(sys.argv) > 4 else 10000 # Default 10,000, Optional

    # Read input files
    setA = read_bed(setA_path)
    setB = read_bed(setB_path)
    chrom_lengths = read_fai(genome_fai_path)

    # Perform permutation test
    observed_overlap, p_value = permutation_test(setA, setB, chrom_lengths, num_permutations)

    # Output the result
    print(f"Number of overlapping bases observed: {observed_overlap}, p value: {p_value}")

if __name__ == "__main__":
    main()