# '''
# Name: Kimberly Magpantay (klmagpan)
# BME205 Fall 2024
# Assignment 3
# Goal: Determine number of overlapping bases b/w SetA and SetB
# Usage: python Kimberly_Magpantay_Tier2.py Tier2_Files/SetA.bed Tier2_Files/SetB.bed Tier2_Files/genome.fa.fai

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

'''Merge overlapping/adjacent ranges'''
def merge_ranges(ranges):
    if not ranges: # If empty
        return []
    
    # Sort ranges by chromosome, then by start position
    ranges.sort(key=lambda x: (x[0], x[1]))
    merged = [ranges[0]]  # Start with the first range
    
    for current in ranges[1:]: # Iterate through other ranges
        prev_chrom, prev_start, prev_end = merged[-1] # Last merged range
        curr_chrom, curr_start, curr_end = current # Current range
        
        if curr_chrom == prev_chrom and curr_start <= prev_end:  # Overlapping or adjacent ranges
            merged[-1] = (prev_chrom, prev_start, max(prev_end, curr_end))  # Merge the ranges by updating end
        else:
            merged.append(current) 
    
    return merged

'''Computes overlapped bases b/w A and B ranges'''
def compute_overlap(setA, setB):
    mergedA = merge_ranges(setA)
    mergedB = merge_ranges(setB)
    
    overlap_bases = 0
    i, j = 0, 0  # Pointers to mergedA and mergedB
    
    while i < len(mergedA) and j < len(mergedB): 
        chromA, startA, endA = mergedA[i] # Current A
        chromB, startB, endB = mergedB[j] # Current B
        
        if chromA == chromB: #
            # Find the overlap between the current ranges
            overlap_start = max(startA, startB)
            overlap_end = min(endA, endB)
            
            if overlap_start < overlap_end: # If there's overlap
                overlap_bases += overlap_end - overlap_start # Overlap
            
            # Move the pointer of the range that finishes first
            if endA < endB: 
                i += 1
            else:
                j += 1
        elif chromA < chromB: #
            i += 1 # A
        else:
            j += 1 # B
    
    return overlap_bases

'''Randomly shuffles ranges'''
def shuffle_ranges(set_b, chrom_sizes):
    shuffled = []
    ranges_by_chrom = {}

    # Organize the ranges by chromosome
    for chrom, start, end in set_b:
        if chrom not in ranges_by_chrom: #
            ranges_by_chrom[chrom] = []
        ranges_by_chrom[chrom].append((start, end))

    # Shuffle ranges chromosome by chromosome
    for chrom, ranges in ranges_by_chrom.items():
        chrom_size = chrom_sizes[chrom]
        for start, end in ranges:
            range_length = end - start
            new_start = random.randint(0, chrom_size - range_length)
            new_end = new_start + range_length # Create new end based on range length
            shuffled.append((chrom, new_start, new_end))

    return shuffled

'''Permutation test on union of ranges for overlap'''
def permutation_test(setA, setB, chrom_lengths, num_permutations=10000):
    # Merge ranges for both sets A and B before starting permutations
    mergedA = merge_ranges(setA)
    mergedB = merge_ranges(setB)
    
    # Compute observed overlap between merged Set A and Set B
    observed_overlap = compute_overlap(mergedA, mergedB)
    
    overlaps = [] # Overlaps from permutations
    
    for _ in range(num_permutations):
        # Shuffle Set A randomly over the genome
        shuffled_setA = shuffle_ranges(setA, chrom_lengths)
        merged_shuffledA = merge_ranges(shuffled_setA)
        
        # Compute overlap for shuffled Set A with Set B
        overlap = compute_overlap(merged_shuffledA, mergedB)
        overlaps.append(overlap)
    
    # Calculate p-value based on permutations
    p_value = np.mean([1 if overlap >= observed_overlap else 0 for overlap in overlaps])
    return observed_overlap, p_value

'''Main'''
def main():
    # Parse command-line arguments
    if len(sys.argv) < 4:
        print("Usage: python submission.py path/to/SetA.bed path/to/SetB.bed path/to/genome.fa.fai [num_permutations]")
        return
    
    setA_path = sys.argv[1]
    setB_path = sys.argv[2]
    genome_fai_path = sys.argv[3]
    num_permutations = int(sys.argv[4]) if len(sys.argv) > 4 else 10000

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