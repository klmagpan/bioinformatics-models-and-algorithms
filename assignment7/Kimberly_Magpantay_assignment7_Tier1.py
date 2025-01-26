# Usage: python Kimberly_Magpantay_assignment7_Tier1.py --allele_freq 0.1 --pop_size 100 --fitness 1.05 --replicates 1000

import argparse
import numpy as np

def simulate_wright_fisher(allele_freq, pop_size, fitness, replicates): # For specific number of replicates
    fixation_times = [] # # of generations until fixation
    loss_times = []
    
    for _ in range(replicates):
        freq = allele_freq
        generations = 0
        
        while 0 < freq < 1: # Continue until reaches loss (0) or fixation(1)
            generations += 1
            
            # Calculate adjusted fitness-based probability
            # Fitness = How allele contributes to reproductive success relative to other alleles
            prob_allele = freq * fitness / (freq * fitness + (1 - freq)) # Denominator ensures that probability is normalized (0-1)
            
            # Simulate allele counts based on binomial sampling
            next_gen_alleles = np.random.binomial(pop_size, prob_allele) / pop_size # Binomial: Inherit or doesn't inherit
            freq = next_gen_alleles
            
        if freq == 1:
            fixation_times.append(generations)
        elif freq == 0:
            loss_times.append(generations)
    
    return fixation_times, loss_times

def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="Wright-Fisher model with selection simulation")
    parser.add_argument("--allele_freq", type=float, required=True, help="Initial frequency of the allele (0-1)")
    parser.add_argument("--pop_size", type=int, required=True, help="Population size (haploid individuals)")
    parser.add_argument("--fitness", type=float, required=True, help="Relative fitness of the allele (fitness=1 is neutral)")
    parser.add_argument("--replicates", type=int, required=True, help="Number of Monte Carlo simulation replicates")

    args = parser.parse_args()

    # Run simulation
    fixation_times, loss_times = simulate_wright_fisher(args.allele_freq, args.pop_size, args.fitness, args.replicates)

    # Compute results for fixation
    if fixation_times: # All individuals in population carry that allele
        mean_fixation = np.mean(fixation_times)
        var_fixation = np.var(fixation_times)
        print(f"Allele was fixed in {mean_fixation:.2f} generations. Variance: {var_fixation:.2f}")

    # Compute results for loss
    if loss_times: # Allele is no longer present
        mean_loss = np.mean(loss_times)
        var_loss = np.var(loss_times)
        print(f"Allele was lost in {mean_loss:.2f} generations. Variance: {var_loss:.2f}")

if __name__ == "__main__":
    main()
