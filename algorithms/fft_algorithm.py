import numpy as np
from scipy.signal import fftconvolve
import time
import math

from resource_monitor import ResourceMonitor
from text_loader import load_text, load_pattern_and_positions, compare_matches

def fft_string_matching_optimized(text: str, pattern: str):
    n = len(text)
    m = len(pattern)

    if n < m:
        raise ValueError("Pattern length must be less than or equal to text length.")

    total_match_score = np.zeros(n - m + 1)
    reversed_pattern = pattern[::-1]

    for base in "ACGT":
        t_vec = (np.array(list(text)) == base).astype(int)
        p_vec = (np.array(list(reversed_pattern)) == base).astype(int)

        base_match_score = fftconvolve(t_vec, p_vec, mode='valid')
        total_match_score += base_match_score

    rounded_scores = np.round(total_match_score)
    match_indices = np.where(rounded_scores == m)[0].tolist()
    return match_indices

def main():
    dna_text_file = "dna_text.txt"
    dna_positions_file = "dna_positions.txt"

    dna_sequence = load_text(dna_text_file)
    pattern, correct_positions = load_pattern_and_positions(dna_positions_file)

    print(f"Text length: {len(dna_sequence):,}")
    print(f"Pattern length: {len(pattern):,}")
    print("\nRunning fft-convolution matching with resource monitoring...")

    monitor = ResourceMonitor(interval=0.1)
    monitor.start()

    start_time = time.time()
    found_positions = fft_string_matching_optimized(dna_sequence, pattern)
    end_time = time.time()

    monitor.stop()
    n = int(math.log10(len(dna_sequence)))
    m = len(pattern)
    monitor.save_log(f'FFT_{n}_{m}_resource_log.csv')

    print(f"\nFinished in {end_time - start_time:.4f} seconds.")
    print(f"Found {len(found_positions):,} matches.")
    compare_matches(correct_positions, found_positions)

if __name__ == "__main__":
    main()
