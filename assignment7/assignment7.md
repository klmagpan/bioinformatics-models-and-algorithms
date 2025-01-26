# Assignment 7: Monte Carlo Simulation of Allele Fixation in a Wright-Fisher Model
## Overview
This assignment involves simulating allele frequency dynamics in a Wright-Fisher population of haploids using Monte Carlo simulations. The goal is to estimate the expected number of generations until an allele either fixes (frequency = 1) or is lost (frequency = 0) under different initial conditions, population sizes, and selection pressures.

## Assignment Breakdown
### Tier 1: Wright-Fisher Simulation with Selection
Implement the Wright-Fisher model with selection, where each generation simulates allele frequencies based on current allele frequency and fitness values.
Track the number of generations until an allele either reaches fixation or loss.
Accept command-line arguments to define:
Initial allele frequency
Population size
Fitness value
Number of replicates (simulations)
Output:
Mean number of generations until fixation or loss
Variance in fixation time across replicates

### Tier 2: Complex Demography
Modify the script to accept a population size file (popsize.tsv), which defines population size changes at specific generations.
Simulate allele fixation or loss considering these population size changes over time.
Output:
Same as Tier 1, but with population size changes over time.

### Tier 3: Coalescent Simulation
Simulate the backward-in-time processes using Coalescent theory to determine the expected time and variance of the eighth coalescent event for a sample of size (--sample_size) in a larger population (--pop_size).
Output:
Expected time and variance for the eighth coalescent event.
