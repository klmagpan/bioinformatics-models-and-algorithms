# Name: Kimberly Magpantay (klmagpan)
# BME205 Fall 2024
# Assignment 6 Tier 1 Part 1
# Goal: Fibonacci Sequence Using Eigenvalues and Eigenvectors
# Usage: python Kimberly_Magpantay_Tier1_Part1.py

import sys
import math

'''
Part 1
- Find eigenvalues and determinant: det[1-lambda 1, 1 -lambda]
    - lambda^2 - lambda - 1 = 0
    - Eigenvalues = (1 + root(5))/2 , (1 - root(5))/2 (golden ratio)
- Find eigenvectors
    - psi [1-psi 1, 1 -psi][x y]
    - phi [1-phi 1, 1 -phi][x y]
    - Eigenvectors: [1 (root(5)-1)/2] [1 -(root(5)-1)/2]
- Diagonalize: A = PDP^-1
    - P = [1 1, psi-1  psi-1] D = [phi 0, 0 psi]
- Apply A^n to find Formula
    - phi^n - psi^n / root(5)
- A and B for initial conditions/coefficients
- Does not use recursion b/c it's direct calculation, computing in single step
    - No repeated function calls
'''

def fibonacci_term(a, b, n):
    # Define the eigenvalues (the golden ratio 'phi' and its conjugate 'psi')
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    psi = (1 - math.sqrt(5)) / 2  # Conjugate of the golden ratio

    # Calculate constants 'alpha' and 'beta' using the initial conditions (a, b)
    alpha = (b - psi * a) / (phi - psi)  # Contribution of phi based on initial conditions
    beta = (phi * a - b) / (phi - psi)   # Contribution of psi based on initial conditions

    # Compute the nth term of the Fibonacci sequence using the closed-form formula
    # We calculate the term as the weighted sum of phi and psi to the (n-1) power [indexing]
    term = int(round(alpha * phi**(n-1) + beta * psi**(n-1)))
    return term

if __name__ == "__main__":
    # Parse command-line arguments
    a = int(sys.argv[1])  # First term
    b = int(sys.argv[2])  # Second term
    n = int(sys.argv[3])  # Term number to find
    
    # Print the nth term in the generalized Fibonacci sequence
    print(fibonacci_term(a, b, n))