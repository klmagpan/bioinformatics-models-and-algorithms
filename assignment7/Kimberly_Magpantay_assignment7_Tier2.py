# Usage: python Kimberly_Magpantay_assignment7_Tier2.py --allele_freq 0.1 --pop_size_file popsize.tsv --fitness 1.05 --replicates 1000

import argparse
import numpy as np
import pandas as pd

def load_population_schedule(pop_size_file):
    """
    Load population size schedule from a TSV file into a dictionary.
    """
    pop_schedule = pd.read_csv(pop_size_file, sep='\t', header=None, names=['generation', 'popsize'])
    pop_size_dict = dict(zip(pop_schedule['generation'], pop_schedule['popsize']))
    return pop_size_dict

def get_population_size(generation, pop_size_dict):
    """
    Get the population size for the current generation based on the schedule.
    """
    # Find the closest generation that is less than or equal to the current generation
    applicable_generations = [gen for gen in pop_size_dict.keys() if gen <= generation]
    if applicable_generations:
        return pop_size_dict[max(applicable_generations)]
    else:
        raise ValueError("Population schedule does not cover the required generation range.")

def simulate_generation(allele_freq, pop_size, fitness):
    """
    Simulates a single generation under the Wright-Fisher model with selection.
    """
    effective_freq = allele_freq * fitness / ((allele_freq * fitness) + (1 - allele_freq))
    next_gen_count = np.random.binomial(pop_size, effective_freq)
    return next_gen_count / pop_size

def wright_fisher_simulation(allele_freq, fitness, pop_size_dict):
    """
    Runs the Wright-Fisher simulation until fixation or loss, adjusting population size as specified.
    """
    generations = 0
    while 0 < allele_freq < 1:
        pop_size = get_population_size(generations, pop_size_dict)
        allele_freq = simulate_generation(allele_freq, pop_size, fitness)
        generations += 1
    return generations, allele_freq

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Wright-Fisher Model with Selection and Variable Population Size")
    parser.add_argument("--allele_freq", type=float, required=True, help="Initial frequency of the allele (0 < freq < 1)")
    parser.add_argument("--pop_size_file", type=str, required=True, help="TSV file with generation-specific population sizes")
    parser.add_argument("--fitness", type=float, required=True, help="Relative fitness of the allele (1 for neutral, >1 positive selection, <1 negative selection)")
    parser.add_argument("--replicates", type=int, required=True, help="Number of Monte Carlo simulation replicates")
    args = parser.parse_args()

    # Load population size schedule
    pop_size_dict = load_population_schedule(args.pop_size_file)

    # Initialize results for fixation and loss
    fixation_generations = []
    loss_generations = []

    # Run simulations
    for _ in range(args.replicates):
        generations, final_freq = wright_fisher_simulation(args.allele_freq, args.fitness, pop_size_dict)
        if final_freq == 1:
            fixation_generations.append(generations)
        elif final_freq == 0:
            loss_generations.append(generations)

    # Calculate mean and variance for fixation and loss times
    if fixation_generations:
        mean_fixation = np.mean(fixation_generations)
        var_fixation = np.var(fixation_generations)
        print(f"Allele was fixed in {mean_fixation:.2f} generations. Variance: {var_fixation:.2f}")
    if loss_generations:
        mean_loss = np.mean(loss_generations)
        var_loss = np.var(loss_generations)
        print(f"Allele was lost in {mean_loss:.2f} generations. Variance: {var_loss:.2f}")

if __name__ == "__main__":
    main()
