# Usage: python Kimberly_Magpantay_assignment7_Tier3.py --pop_size 100000 --sample_size 10 --replicates 1000

import argparse
import numpy as np

def simulate_eighth_coalescent_event(pop_size, sample_size):
    """
    Simulate the waiting time until the eighth coalescent event in a sample
    using Coalescent theory.
    """
    lineages = sample_size
    cumulative_time = 0
    coalescent_event = 0

    while coalescent_event < 8:
        # Calculate the coalescent rate
        coalescent_rate = lineages * (lineages - 1) / (2 * pop_size)
        # Sample time to next coalescent event
        waiting_time = np.random.exponential(1 / coalescent_rate)
        cumulative_time += waiting_time
        # Record the coalescent event
        coalescent_event += 1
        # Reduce the number of lineages by one as two lineages coalesce
        lineages -= 1

    return cumulative_time

def main():
    parser = argparse.ArgumentParser(description="Simulate the time to the eighth coalescent event.")
    parser.add_argument("--pop_size", type=int, required=True, help="The population size.")
    parser.add_argument("--sample_size", type=int, required=True, help="The sample size.")
    parser.add_argument("--replicates", type=int, default=1000, help="Number of replicates for simulation.")
    args = parser.parse_args()

    # Run the simulation over multiple replicates
    coalescent_times = [simulate_eighth_coalescent_event(args.pop_size, args.sample_size) for _ in range(args.replicates)]

    # Calculate mean and variance of the coalescent times
    mean_generations = np.mean(coalescent_times)
    variance_generations = np.var(coalescent_times)

    # Output the results
    print(f"Time to eighth coalescent event: {mean_generations:.2f}. Variance: {variance_generations:.2f}")

if __name__ == "__main__":
    main()
