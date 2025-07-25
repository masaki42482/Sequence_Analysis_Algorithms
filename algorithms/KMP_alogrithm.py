import time
import math

from resource_monitor import ResourceMonitor
from text_loader import load_text, load_pattern_and_positions, compare_matches


def compute_lps_table(pattern: str) -> list[int]:
    """
    Compute the Longest Prefix Suffix (LPS) table for the KMP algorithm.

    Args:
        pattern (str): The pattern for which to compute the LPS table.

    Returns:
        list[int]: The computed LPS table.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Search the pattern in the text using the KMP algorithm.

    Args:
        text (str): The text in which to search for the pattern.
        pattern (str): The pattern to search for .
        both text and pattern should be strings of characters (e.g., 'A', 'C', 'G', 'T').
    Returns:
        list[int]: The starting positions (0-indexed) where the pattern is found.
    """
    
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return []
    if n < m:
        return []

    lps = compute_lps_table(pattern)
    
    results = []
    i = 0  # pointer for text
    j = 0  # pointer for pattern

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            results.append(i - j)
            # Update j to continue searching for the next occurrence
            j = lps[j - 1]

        # If a mismatch occurs
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                # Roll back j (keep i the same)
                j = lps[j - 1]
            else:
                i += 1
                
    return results

def main():
    dna_text_file = "dna_text.txt"
    dna_positions_file = "dna_positions.txt"
    
    dna_sequence = load_text(dna_text_file)
    pattern, correct_positions = load_pattern_and_positions(dna_positions_file)
    
    print(f"Text length: {len(dna_sequence):,}")
    print(f"Pattern length: {len(pattern):,}")
    print("\nRunning KMP algorithm with resource monitoring...")

    monitor = ResourceMonitor(interval=0.1)
    monitor.start()
    
    start_time = time.time()
    found_positions = kmp_search(dna_sequence, pattern)
    end_time = time.time()
    
    monitor.stop()
    n = int(math.log10(len(dna_sequence)))
    m = len(pattern)
    monitor.save_log(f'KMP_{n}_{m}_resource_log.csv')

    print(f"\nFinished in {end_time - start_time:.4f} seconds.")
    print(f"Found {len(found_positions):,} matches.")
    compare_matches(correct_positions, found_positions)
    
if __name__ == "__main__":
    main()